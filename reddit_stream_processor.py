from confluent_kafka import Consumer, Producer, KafkaError
import json
import xml.etree.ElementTree as ET
from datetime import datetime
import time
import logging
from dotenv import load_dotenv
from confluent_kafka.admin import AdminClient, NewTopic
from reddit_client import RedditClient
from sentiment_analyzer import SentimentAnalyzer
load_dotenv()

class RedditStreamProcessor:
    def __init__(self, 
                 bootstrap_servers: str,
                 api_key: str,
                 api_secret: str,
                 reddit_client_id: str,
                 reddit_client_secret: str,
                 reddit_user_agent: str):
        
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
        self.reddit_client = RedditClient(
            reddit_client_id,
            reddit_client_secret,
            reddit_user_agent
        )
        self.sentiment_analyzer = SentimentAnalyzer()
        self.admin_client = AdminClient(self.producer_config)
        
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)


    def create_topic_if_not_exists(self, topic_name: str, num_partitions: int = 1, 
                                 replication_factor: int = 3):
        """Create a Kafka topic if it doesn't already exist"""
        topics = self.admin_client.list_topics().topics
        if topic_name not in topics:
            new_topic = NewTopic(topic_name, num_partitions, replication_factor)
            try:
                self.admin_client.create_topics([new_topic])
                self.logger.info(f"Created topic: {topic_name}")
                time.sleep(5)  # Wait for topic creation to propagate
            except Exception as e:
                self.logger.error(f"Error creating topic {topic_name}: {e}")

    def stream_reddit_data(self, output_topic: str):
        """Stream Reddit posts to Kafka topic"""
        self.create_topic_if_not_exists(output_topic)
        
        while True:
            try:
                posts = self.reddit_client.fetch_posts()
                processed = 0
                
                for post in posts:
                    try:
                        self.producer.produce(
                            output_topic,
                            key=post['id'],
                            value=json.dumps(post)
                        )
                        processed += 1
                    except Exception as e:
                        self.logger.error(f"Error producing message for post {post['id']}: {e}")
                
                self.producer.flush()
                self.logger.info(f"Processed {processed} Reddit posts")
                
                # Wait before next fetch to respect Reddit's rate limits
                time.sleep(300)  # 5 minutes
                
            except Exception as e:
                self.logger.error(f"Error in Reddit streaming: {e}")
                time.sleep(60)

    
    def process_sentiment(self, input_topic: str, output_topic: str):
        """Process posts and generate detailed sentiment analysis"""
        self.create_topic_if_not_exists(input_topic)
        self.create_topic_if_not_exists(output_topic)
        self.consumer.subscribe([input_topic])
        
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
                sentiment_analysis = self.sentiment_analyzer.analyze_sentiment(post)
                
                analysis = {
                    'post_id': post['id'],
                    'subreddit': post['subreddit'],
                    'title': post['title'],
                    'analysis': sentiment_analysis,
                    'timestamp': datetime.now().isoformat()
                }
                
                try:
                    json_str = json.dumps(analysis)
                    self.producer.produce(
                        output_topic,
                        key=post['id'],
                        value=json_str
                    )
                    
                    self.producer.flush()
                    self.logger.info(f"Generated sentiment analysis for post: {post['title'][:50]}...")
                    
                    # Print analysis summary
                    print(f"\nSentiment Analysis Summary:")
                    print(f"Subreddit: r/{analysis['subreddit']}")
                    print(f"Title: {analysis['title'][:100]}...")
                    print(f"Overall Sentiment: {sentiment_analysis['summary_stats']['overall_sentiment']}")
                    print(f"Dominant Aspect: {sentiment_analysis['summary_stats']['dominant_aspect']}")
                    print(f"Engagement Score: {sentiment_analysis['engagement_metrics']['engagement_score']:.2f}")
                    
                    if sentiment_analysis['feature_requests']:
                        print("\nTop Feature Requests:")
                        for request in sentiment_analysis['feature_requests']:
                            print(f"- {request}")
                    
                    print("-" * 80)
                    
                except TypeError as e:
                    self.logger.error(f"JSON serialization error: {e}")
                    continue
                    
            except Exception as e:
                self.logger.error(f"Error processing sentiment: {e}")
                time.sleep(60)