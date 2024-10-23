from confluent_kafka import Consumer, Producer, KafkaError
import json
import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import time
from typing import List, Dict, Optional
from anthropic import Anthropic
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import logging
import os
from dotenv import load_dotenv
from confluent_kafka.admin import AdminClient, NewTopic

load_dotenv()

class LLMClient:
    def __init__(self, api_key: str):
        self.client = Anthropic(api_key=api_key)
        
    def generate(self, prompt: str) -> str:
        try:
            message = self.client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=1024,
                temperature=0.7,
                system="You are a research expert tasked with generating innovative research ideas. Focus on practical, impactful suggestions that build upon existing research while considering business context and feasibility.",
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )
            return message.content
        except Exception as e:
            logging.error(f"LLM generation error: {e}")
            return None

class PaperFilter:
    def __init__(self, company_context: Dict):
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.company_focus = ' '.join([
            company_context['industry'],
            ' '.join(company_context['research_focus']),
            ' '.join(company_context['current_projects'])
        ])
        self.min_similarity_threshold = 0.05

    def calculate_relevance(self, paper: Dict) -> float:
        """Calculate relevance score between paper and company focus"""
        paper_text = f"{paper['title']} {paper['summary']}"
        try:
            tfidf_matrix = self.vectorizer.fit_transform([self.company_focus, paper_text])
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            return float(similarity)
        except Exception as e:
            logging.error(f"Relevance calculation error: {e}")
            return 0.0

    def is_relevant(self, paper: Dict) -> bool:
        """Determine if paper is relevant enough to process"""
        relevance_score = self.calculate_relevance(paper)
        return relevance_score >= self.min_similarity_threshold

class ArxivStreamProcessor:
    def __init__(self, bootstrap_servers: str, api_key: str, api_secret: str, 
                 llm_api_key: str):
        self.producer_config = {
            'bootstrap.servers': bootstrap_servers,
            'security.protocol': 'SASL_SSL',
            'sasl.mechanisms': 'PLAIN',
            'sasl.username': api_key,
            'sasl.password': api_secret
        }

        
        self.consumer_config = {
            **self.producer_config,
            'group.id': 'arxiv_processor',
            'auto.offset.reset': 'earliest'
        }
        
        self.producer = Producer(self.producer_config)
        self.consumer = Consumer(self.consumer_config)
        self.llm_client = LLMClient(llm_api_key)
        
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self.admin_client = AdminClient(self.producer_config)

    def create_topic_if_not_exists(self, topic_name: str, num_partitions: int = 1, replication_factor: int = 3):
        """Create a Kafka topic if it doesn't already exist"""
        topics = self.admin_client.list_topics().topics
        if topic_name not in topics:
            new_topic = NewTopic(topic_name, num_partitions, replication_factor)
            try:
                self.admin_client.create_topics([new_topic])
                self.logger.info(f"Created topic: {topic_name}")
                # Wait for topic creation to propagate
                time.sleep(5)
            except Exception as e:
                self.logger.error(f"Error creating topic {topic_name}: {e}")


    def fetch_arxiv_papers(self, categories: List[str], max_results: int = 100) -> List[Dict]:
        """Fetch recent papers from arXiv API with enhanced metadata"""
        base_url = 'http://export.arxiv.org/api/query?'
        
        yesterday = datetime.now() - timedelta(days=1)
        date_query = yesterday.strftime('%Y%m%d')
        
        category_query = ' OR '.join(f'cat:{cat}' for cat in categories)
        query = (f'search_query={category_query}&sortBy=lastUpdatedDate'
                f'&sortOrder=descending&max_results={max_results}')
        
        try:
            response = requests.get(base_url + query)
            root = ET.fromstring(response.content)
            
            papers = []
            for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
                # Enhanced metadata extraction
                authors = [author.find('{http://www.w3.org/2005/Atom}name').text 
                          for author in entry.findall('{http://www.w3.org/2005/Atom}author')]
                
                paper = {
                    'id': entry.find('{http://www.w3.org/2005/Atom}id').text,
                    'title': entry.find('{http://www.w3.org/2005/Atom}title').text.replace('\n', ' '),
                    'summary': entry.find('{http://www.w3.org/2005/Atom}summary').text.replace('\n', ' '),
                    'categories': [cat.get('term') for cat in entry.findall('{http://www.w3.org/2005/Atom}category')],
                    'authors': authors,
                    'published': entry.find('{http://www.w3.org/2005/Atom}published').text,
                    'updated': entry.find('{http://www.w3.org/2005/Atom}updated').text,
                    'link': entry.find('{http://www.w3.org/2005/Atom}id').text
                }
                papers.append(paper)
            
            return papers
        except Exception as e:
            self.logger.error(f"Error fetching papers: {e}")
            return []

    def generate_research_idea(self, paper: Dict, company_context: Dict) -> Optional[Dict]:
        """Generate research ideas using enhanced prompt"""
        prompt = f"""
        Paper Analysis:
        Title: {paper['title']}
        Authors: {', '.join(paper['authors'])}
        Summary: {paper['summary']}
        Categories: {', '.join(paper['categories'])}
        
        Company Profile:
        Industry: {company_context['industry']}
        Research Focus Areas: {', '.join(company_context['research_focus'])}
        Active Projects: {', '.join(company_context['current_projects'])}
        Core Technologies: {', '.join(company_context.get('core_technologies', []))}
        Available Resources: {', '.join(company_context.get('available_resources', []))}
        
        Based on this information, please generate an innovative research idea that:
        1. Extends or applies the paper's findings in a novel way
        2. Aligns with the company's expertise and goals
        3. Has clear commercial potential
        4. Can be executed with available resources
        5. Addresses a specific market need or technical challenge
        
        Provide your response in the following structured format:
        
        IDEA TITLE:
        [A concise, descriptive title for the research idea]
        
        PROBLEM STATEMENT:
        [Clear articulation of the problem or opportunity being addressed]
        
        TECHNICAL APPROACH:
        - Key Innovation Points:
          [List 2-3 main technical innovations]
        - Methodology:
          [Step-by-step research approach]
        - Integration with Existing Work:
          [How it builds on the paper's findings]
        
        BUSINESS IMPACT:
        - Market Opportunity:
          [Specific applications and target markets]
        - Competitive Advantage:
          [Why this approach is unique]
        - Success Metrics:
          [How to measure progress and impact]
        
        EXECUTION REQUIREMENTS:
        - Team Expertise:
          [Required skills and knowledge]
        - Technical Resources:
          [Required equipment, data, or infrastructure]
        - Timeline:
          [Estimated research and development phases]
        - Risk Assessment:
          [Key technical and market risks]
        
        NEXT STEPS:
        [3-5 concrete actions to initiate this research]
        """
        
        response = self.llm_client.generate(prompt)
        if response:
            return {
                'paper_id': paper['id'],
                'paper_title': paper['title'],
                'paper_link': paper['link'],
                'generated_idea': response,
                'timestamp': datetime.now().isoformat(),
                'relevance_score': paper.get('relevance_score', 0)
            }
        return None

    def stream_papers_to_kafka(self, categories: List[str], topic: str, 
                             company_context: Dict):
        """Stream relevant papers to Kafka topic"""
        self.create_topic_if_not_exists(topic)
        paper_filter = PaperFilter(company_context)
        
        while True:
            try:
                papers = self.fetch_arxiv_papers(categories)
                relevant_papers = []
                
                for paper in papers:
                    if paper_filter.is_relevant(paper):
                        paper['relevance_score'] = paper_filter.calculate_relevance(paper)
                        relevant_papers.append(paper)
                
                # Sort by relevance score
                relevant_papers.sort(key=lambda x: x['relevance_score'], reverse=True)
                
                for paper in relevant_papers:
                    self.producer.produce(
                        topic,
                        key=paper['id'],
                        value=json.dumps(paper)
                    )
                
                self.producer.flush()
                self.logger.info(f"Processed {len(relevant_papers)} relevant papers out of {len(papers)} total papers")
                
                time.sleep(3600)  # Fetch every hour
                
            except Exception as e:
                self.logger.error(f"Error in paper streaming: {e}")
                time.sleep(300)  # Wait 5 minutes before retrying

    def process_ideas(self, input_topic: str, output_topic: str, 
                 company_context: Dict):
        """Process papers and generate ideas with error handling"""
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
                        
                paper = json.loads(msg.value())
                idea = self.generate_research_idea(paper, company_context)
                
                if idea:
                    self.producer.produce(
                        output_topic,
                        key=paper['id'],
                        value=json.dumps(idea)
                    )
                    
                    self.producer.flush()
                    self.logger.info(f"Generated idea for paper: {paper['title']}")
                    
                    # Print the generated idea
                    print(f"\nGenerated Research Idea:")
                    print(f"Paper Title: {idea['paper_title']}")
                    print(f"Paper Link: {idea['paper_link']}")
                    print(f"Idea:\n{idea['generated_idea']}")
                    print(f"Relevance Score: {idea['relevance_score']}")
                    print("-" * 80)
                
            except Exception as e:
                self.logger.error(f"Error processing ideas: {e}")
                time.sleep(60)  # Wait before retrying

# Example usage
if __name__ == "__main__":
    # Enhanced configuration
    config = {
        'bootstrap_servers': os.getenv('CONFLUENT_BOOTSTRAP_SERVERS'),
        'api_key': os.getenv('CONFLUENT_API_KEY'),
        'api_secret': os.getenv('CONFLUENT_API_SECRET'),
        'llm_api_key': os.getenv('ANTHROPIC_API_KEY')
    }
    
    # Enhanced company context
    company_context = {
        'industry': 'Biotechnology',
        'research_focus': [
            'Drug Discovery',
            'Computational Biology',
            'Protein Engineering'
        ],
        'current_projects': [
            'Protein Folding Prediction',
            'Drug-Target Interaction Modeling',
            'Antibody Design'
        ],
        'core_technologies': [
            'Machine Learning',
            'Molecular Dynamics',
            'High-throughput Screening'
        ],
        'available_resources': [
            'GPU Cluster',
            'Wet Lab Facilities',
            'Proprietary Datasets',
            'Clinical Trial Network'
        ]
    }
    
    # Initialize processor
    processor = ArxivStreamProcessor(**config)

    processor.create_topic_if_not_exists('arxiv_papers')
    processor.create_topic_if_not_exists('research_ideas')
    
    # Start paper streaming in a separate thread
    import threading
    
    categories = [
        'q-bio',  # Quantitative Biology
        'cs.AI',  # Artificial Intelligence
        'cs.LG',  # Machine Learning
        'stat.ML',  # Statistics - Machine Learning
        'physics.bio-ph'  # Biological Physics
    ]
    
    streaming_thread = threading.Thread(
        target=processor.stream_papers_to_kafka,
        args=(categories, 'arxiv_papers', company_context)
    )
    streaming_thread.daemon = True
    streaming_thread.start()
    
    # Process ideas in main thread
    processor.process_ideas(
        'arxiv_papers',
        'research_ideas',
        company_context
    )