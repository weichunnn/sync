from confluent_kafka import Consumer, Producer, KafkaError
import json
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Dict
import time
from datetime import timedelta
import logging
import os
from dotenv import load_dotenv
from confluent_kafka.admin import AdminClient, NewTopic
from reddit_client import RedditClient
from sentiment_analyzer import SentimentAnalyzer
load_dotenv()

class RedditStreamProcessor:
    def __init__(self, bootstrap_servers: str, api_key: str, api_secret: str):
        self.producer_config = {
            'bootstrap.servers': bootstrap_servers,
            'security.protocol': 'SASL_SSL',
            'sasl.mechanisms': 'PLAIN',
            'sasl.username': api_key,
            'sasl.password': api_secret
        }
        
        self.consumer_config = {
            **self.producer_config,
            'group.id': 'reddit_processor',
            'auto.offset.reset': 'earliest'
        }
        
        self.producer = Producer(self.producer_config)
        self.consumer = Consumer(self.consumer_config)
        self.admin_client = AdminClient(self.producer_config)
        self.processed_posts = {}  # Changed to dict to store timestamps
        
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def clean_old_post_ids(self):
        """Clean up processed post IDs older than 48 hours"""
        try:
            current_time = datetime.now()
            cutoff_time = current_time - timedelta(hours=48)
            
            # Create a new dict with only recent posts
            self.processed_posts = {
                post_id: timestamp 
                for post_id, timestamp in self.processed_posts.items()
                if timestamp > cutoff_time
            }
            
            cleaned_count = len(self.processed_posts)
            self.logger.debug(f"Cleaned processed posts cache. Remaining entries: {cleaned_count}")
            
        except Exception as e:
            self.logger.error(f"Error cleaning old post IDs: {e}")

    def create_topic_if_not_exists(self, topic_name: str, num_partitions: int = 1, 
                                 replication_factor: int = 3):
        """Create a Kafka topic if it doesn't already exist"""
        try:
            # Get existing topics
            metadata = self.admin_client.list_topics(timeout=10)
            
            # Check if topic exists
            if topic_name not in metadata.topics:
                # Create new topic configuration
                new_topic = NewTopic(
                    topic_name,
                    num_partitions=num_partitions,
                    replication_factor=replication_factor
                )
                
                # Create the topic
                futures = self.admin_client.create_topics([new_topic])
                
                # Wait for topic creation
                for topic, future in futures.items():
                    try:
                        future.result(timeout=30)  # Wait up to 30 seconds
                        self.logger.info(f"Created topic: {topic}")
                    except Exception as e:
                        self.logger.error(f"Failed to create topic {topic}: {e}")
                        raise
                
                # Wait for topic creation to propagate
                time.sleep(5)
            else:
                self.logger.info(f"Topic {topic_name} already exists")
                
                # Optionally verify topic configuration
                topic_config = metadata.topics[topic_name]
                current_partitions = len(topic_config.partitions)
                if current_partitions != num_partitions:
                    self.logger.warning(
                        f"Topic {topic_name} exists with {current_partitions} partitions "
                        f"(expected {num_partitions})"
                    )
                    
        except Exception as e:
            self.logger.error(f"Error managing topic {topic_name}: {e}")
            raise

    def stream_reddit_data(self, output_topic: str, company_context: Dict):
        """Stream Reddit posts to Kafka topic"""
        self.create_topic_if_not_exists(output_topic)
        reddit_client = RedditClient(
            os.getenv('REDDIT_CLIENT_ID'),
            os.getenv('REDDIT_CLIENT_SECRET'),
            'RedditAnalyzer/1.0',
            ""  # Empty prompt as we're using company context instead
        )
        
        while True:
            try:
                posts = reddit_client.fetch_posts(company_context)
                processed = 0
                current_time = datetime.now()
                
                for post in posts:
                    post_id = post['metadata']['id']
                    if post_id not in self.processed_posts:
                        try:
                            self.producer.produce(
                                output_topic,
                                key=post_id,
                                value=json.dumps(post)
                            )
                            self.processed_posts[post_id] = current_time
                            processed += 1
                        except Exception as e:
                            self.logger.error(f"Error producing message for post {post_id}: {e}")
                
                self.producer.flush()
                self.logger.info(f"Processed {processed} Reddit posts")
                
                # Clean up old post IDs from memory
                self.clean_old_post_ids()
                
                time.sleep(300)  # 5 minutes
                
            except Exception as e:
                self.logger.error(f"Error in Reddit streaming: {e}")
                time.sleep(60)
    
    def calculate_industry_relevance(self, post: Dict, company_context: Dict) -> float:
        """Calculate relevance to company industry"""
        try:
            # Create industry-specific keywords
            industry = company_context['industry'].lower()
            industry_keywords = {
                'biotechnology': [
                    'biotech', 'biological', 'drug', 'therapeutic', 'clinical',
                    'pharmaceutical', 'molecule', 'protein', 'enzyme', 'antibody',
                    'genomic', 'cell', 'tissue', 'assay', 'screening'
                ],
                'artificial intelligence': [
                    'ai', 'machine learning', 'neural network', 'deep learning',
                    'algorithm', 'model', 'prediction', 'classification',
                    'training', 'inference', 'optimization'
                ]
            }
            
            # Get relevant keywords for the industry
            keywords = industry_keywords.get(industry.lower(), [])
            if not keywords:
                keywords = [industry]  # Use industry name if no specific keywords
            
            # Combine post title and content
            text = f"{post['content']['title']} {post['content']['selftext']}".lower()
            
            # Count keyword matches
            matches = sum(1 for keyword in keywords if keyword in text)
            
            # Calculate normalized score
            score = matches / len(keywords) if keywords else 0
            
            return min(1.0, score)  # Cap at 1.0
            
        except Exception as e:
            self.logger.error(f"Error calculating industry relevance: {e}")
            return 0.0

    def calculate_technology_relevance(self, post: Dict, company_context: Dict) -> float:
        """Calculate relevance to company technologies"""
        try:
            # Get company technologies and create related terms
            tech_terms = []
            for tech in company_context.get('core_technologies', []):
                tech_lower = tech.lower()
                tech_terms.extend([
                    tech_lower,
                    tech_lower.replace(' ', ''),
                    tech_lower.replace('-', ' ')
                ])
            
            # Add common variations and related terms
            tech_related = {
                'machine learning': ['ml', 'deep learning', 'neural network', 'ai model'],
                'molecular dynamics': ['md simulation', 'molecular simulation', 'atomistic'],
                'high-throughput screening': ['hts', 'screening', 'automated testing']
            }
            
            for tech in company_context.get('core_technologies', []):
                if tech.lower() in tech_related:
                    tech_terms.extend(tech_related[tech.lower()])
            
            # Combine post title and content
            text = f"{post['content']['title']} {post['content']['selftext']}".lower()
            
            # Calculate matches
            matches = sum(1 for term in tech_terms if term in text)
            
            # Normalize score
            score = matches / (len(tech_terms) * 0.5) if tech_terms else 0  # Adjust threshold
            
            return min(1.0, score)  # Cap at 1.0
            
        except Exception as e:
            self.logger.error(f"Error calculating technology relevance: {e}")
            return 0.0

    def calculate_combined_relevance(self, post: Dict, company_context: Dict) -> Dict:
        """Calculate combined relevance metrics"""
        try:
            industry_score = self.calculate_industry_relevance(post, company_context)
            tech_score = self.calculate_technology_relevance(post, company_context)
            
            # Calculate combined score with weights
            combined_score = (0.6 * industry_score) + (0.4 * tech_score)
            
            return {
                'industry_match': float(industry_score),
                'technology_match': float(tech_score),
                'combined_score': float(combined_score)
            }
            
        except Exception as e:
            self.logger.error(f"Error calculating combined relevance: {e}")
            return {
                'industry_match': 0.0,
                'technology_match': 0.0,
                'combined_score': 0.0
            }

    def process_sentiment(self, input_topic: str, output_topic: str, company_context: Dict):
        """Process posts and generate sentiment analysis"""
        try:
            # Ensure both topics exist
            self.create_topic_if_not_exists(input_topic)
            self.create_topic_if_not_exists(output_topic)
            
            # Subscribe to input topic
            self.consumer.subscribe([input_topic])
            sentiment_analyzer = SentimentAnalyzer()
            
            while True:
                try:
                    msg = self.consumer.poll(1.0)
                    
                    if msg is None:
                        continue
                    if msg.error():
                        if msg.error().code() == KafkaError._PARTITION_EOF:
                            continue
                        else:
                            self.logger.error(f"Consumer error: {msg.error()}")
                            break
                    
                    post = json.loads(msg.value())
                    sentiment_analysis = sentiment_analyzer.analyze_sentiment(post['content'])
                    relevance_scores = self.calculate_combined_relevance(post, company_context)
                    
                    analysis = {
                        'metadata': post['metadata'],
                        'content': post['content'],
                        'analysis': {
                            'sentiment': sentiment_analysis,
                            'timestamp': datetime.now().isoformat(),
                            'relevance': relevance_scores
                        }
                    }
                    
                    # Log relevance scores for debugging
                    self.logger.info(f"\nRelevance Scores for post '{post['content']['title'][:50]}...':")
                    self.logger.info(f"Industry Match: {relevance_scores['industry_match']:.3f}")
                    self.logger.info(f"Technology Match: {relevance_scores['technology_match']:.3f}")
                    self.logger.info(f"Combined Score: {relevance_scores['combined_score']:.3f}")
                    
                    try:
                        json_str = json.dumps(analysis)
                        self.producer.produce(
                            output_topic,
                            key=post['metadata']['id'],
                            value=json_str
                        )
                        
                        self.producer.flush()
                        self.print_analysis_summary(analysis, company_context)
                        
                    except TypeError as e:
                        self.logger.error(f"JSON serialization error: {e}")
                        continue
                        
                except Exception as e:
                    self.logger.error(f"Error processing message: {e}")
                    time.sleep(60)
                    
        except Exception as e:
            self.logger.error(f"Fatal error in process_sentiment: {e}")
            raise
    
    def print_analysis_summary(self, analysis: Dict, company_context: Dict):
        """Print detailed analysis summary with company context relevance"""
        try:
            metadata = analysis['metadata']
            content = analysis['content']
            sentiment = analysis['analysis']['sentiment']
            relevance = analysis['analysis']['relevance']
            
            print("\nPost Analysis Summary:")
            print(f"Subreddit: r/{metadata['subreddit']}")
            print(f"Title: {content['title'][:100]}...")
            print(f"URL: {metadata['url']}")
            print(f"Created: {datetime.fromtimestamp(metadata['created_utc']).strftime('%Y-%m-%d %H:%M:%S')}")
            
            print("\nRelevance Scores:")
            print(f"Initial Relevance: {metadata['relevance_score']:.2f}")
            print(f"Industry Match: {relevance['industry_match']:.2f}")
            print(f"Technology Match: {relevance['technology_match']:.2f}")
            print(f"Combined Score: {relevance['combined_score']:.2f}")
            
            print("\nSentiment Analysis:")
            print(f"Overall Sentiment: {sentiment['summary_stats']['overall_sentiment']}")
            print(f"Dominant Aspect: {sentiment['summary_stats']['dominant_aspect']}")
            print(f"Engagement Score: {sentiment['engagement_metrics']['engagement_score']:.2f}")
            
            if sentiment['feature_requests']:
                print("\nTop Feature Requests:")
                for request in sentiment['feature_requests']:
                    print(f"- {request}")
            
            print("\nAspect Sentiments:")
            for aspect, data in sentiment['aspect_sentiments'].items():
                if data['example_quotes']:
                    print(f"\n{aspect.capitalize()}:")
                    print(f"Sentiment Score: {data['sentiment_score']:.2f}")
                    print("Example Quote:", data['example_quotes'][0])
            
            print("-" * 80)
            
        except Exception as e:
            self.logger.error(f"Error printing analysis summary: {e}")
            print("Error occurred while printing analysis summary")