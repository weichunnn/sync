from confluent_kafka import Consumer, Producer, KafkaError
import json
import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import time
from typing import List, Dict, Optional
import logging
from dotenv import load_dotenv
from confluent_kafka.admin import AdminClient, NewTopic
from llm_client import LLMClient
from paper_filter import PaperFilter

load_dotenv()


class ArxivStreamProcessor:
    def __init__(
        self, bootstrap_servers: str, api_key: str, api_secret: str, llm_api_key: str
    ):
        self.producer_config = {
            "bootstrap.servers": bootstrap_servers,
            "security.protocol": "SASL_SSL",
            "sasl.mechanisms": "PLAIN",
            "sasl.username": api_key,
            "sasl.password": api_secret,
        }

        self.consumer_config = {
            **self.producer_config,
            "group.id": "arxiv_processor",
            "auto.offset.reset": "earliest",
        }

        self.producer = Producer(self.producer_config)
        self.consumer = Consumer(self.consumer_config)
        self.llm_client = LLMClient(llm_api_key)

        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self.admin_client = AdminClient(self.producer_config)
        self.processed_paper_ids = set()

    def create_topic_if_not_exists(
        self, topic_name: str, num_partitions: int = 1, replication_factor: int = 3
    ):
        """Create a Kafka topic if it doesn't already exist"""
        topics = self.admin_client.list_topics().topics
        if topic_name not in topics:
            new_topic = NewTopic(topic_name, num_partitions, replication_factor)
            try:
                self.admin_client.create_topics([new_topic])
                self.logger.info(f"Created topic: {topic_name}")

                time.sleep(5)
            except Exception as e:
                self.logger.error(f"Error creating topic {topic_name}: {e}")

    def fetch_arxiv_papers(
        self, categories: List[str], max_results: int = 10
    ) -> List[Dict]:
        """Fetch recent papers from arXiv API with enhanced metadata"""
        base_url = "http://export.arxiv.org/api/query?"

        last_processed_date = datetime.now() - timedelta(days=7)
        date_query = last_processed_date.strftime("%Y%m%d")

        category_query = " OR ".join(f"cat:{cat}" for cat in categories)
        query = f"search_query=({category_query})&sortBy=submittedDate&sortOrder=descending&max_results={max_results}"

        print(f"Fetching papers with query: {query}")   


        try:
            response = requests.get(base_url + query)
            root = ET.fromstring(response.content)

            papers = []
            for entry in root.findall("{http://www.w3.org/2005/Atom}entry"):
                authors = [
                    author.find("{http://www.w3.org/2005/Atom}name").text
                    for author in entry.findall("{http://www.w3.org/2005/Atom}author")
                ]

                paper = {
                    "id": entry.find("{http://www.w3.org/2005/Atom}id").text,
                    "title": entry.find(
                        "{http://www.w3.org/2005/Atom}title"
                    ).text.replace("\n", " "),
                    "summary": entry.find(
                        "{http://www.w3.org/2005/Atom}summary"
                    ).text.replace("\n", " "),
                    "categories": [
                        cat.get("term")
                        for cat in entry.findall(
                            "{http://www.w3.org/2005/Atom}category"
                        )
                    ],
                    "authors": authors,
                    "published": entry.find(
                        "{http://www.w3.org/2005/Atom}published"
                    ).text,
                    "updated": entry.find("{http://www.w3.org/2005/Atom}updated").text,
                    "link": entry.find("{http://www.w3.org/2005/Atom}id").text,
                }
                papers.append(paper)
            
            if papers:
                self.last_processed_date = datetime.strptime(papers[0]['updated'], "%Y-%m-%dT%H:%M:%SZ")

            print(f"Fetched {len(papers)} papers")
            return papers
        except Exception as e:
            self.logger.error(f"Error fetching papers: {e}")
            return []

    def categorize_rank(self, paper: Dict, context: Dict) -> Optional[Dict]:
        """Generate relevance score for a paper based on the given context"""
        is_company_context = "industry" in context
        context_type = "Company" if is_company_context else "Project"

        prompt = f"""
        Paper Analysis:
        Title: {paper['title']}
        Authors: {', '.join(paper['authors'])}
        Summary: {paper['summary']}
        Categories: {', '.join(paper['categories'])}
        
        {context_type} Profile:
        {"Industry: " + context['industry'] if is_company_context else "Project Name: " + context['name']}
        {"Research Focus Areas: " + ', '.join(context['research_focus']) if is_company_context else "Project Goals: " + ', '.join(context['goals'])}
        {"Active Projects: " + ', '.join(context['current_projects']) if is_company_context else "Current Challenges: " + ', '.join(context['challenges'])}
        {"Core Technologies: " + ', '.join(context.get('core_technologies', [])) if is_company_context else "Key Technologies: " + ', '.join(context.get('key_technologies', []))}
        {"Available Resources: " + ', '.join(context.get('available_resources', [])) if is_company_context else ""}
        
        Based on this information, please provide a relevance score from 0 to 100, where 100 is extremely relevant to the {context_type.lower()}'s goals and 0 is not relevant at all.
        
        Output only the numeric score (0-100) with no additional text or explanation.
        """

        response = self.llm_client.generate(prompt)
        if response:
            try:
                relevance_score = int(response.strip())
                if 0 <= relevance_score <= 100:
                    result = {
                        "paper_id": paper["id"],
                        "paper_title": paper["title"],
                        "paper_link": paper["link"],
                        "relevance_score": relevance_score,
                        "timestamp": datetime.now().isoformat(),
                        "context_type": context_type,
                    }
                    return result
            except ValueError:
                self.logger.error(f"Invalid relevance score: {response}")
        return None

    def stream_papers_to_kafka(
        self, categories: List[str], topic: str, company_context: Dict
    ):
        """Stream relevant papers to Kafka topic"""
        self.create_topic_if_not_exists(topic)

        while True:
            try:
                papers = self.fetch_arxiv_papers(categories=categories)
            
                for paper in papers:
                    self.producer.produce(
                        topic, key=paper["id"], value=json.dumps(paper)
                    )
                

                self.producer.flush()
                self.logger.info(
                    f"Fetched {len(papers)} papers successfully"
                )

                if len(self.processed_paper_ids) > 10000:
                    self.processed_paper_ids = set(
                        list(self.processed_paper_ids)[-10000:]
                    )

                time.sleep(120)

            except Exception as e:
                self.logger.error(f"Error in paper streaming: {e}")
                time.sleep(120)

    def process_ideas(
        self,
        input_topic: str,
        company: str,
        company_context: Dict,
        projects: Dict[str, Dict],
    ):
        """Process papers and generate ideas with separate company and project outputs"""
        self.create_topic_if_not_exists(input_topic)
        self.create_topic_if_not_exists(company)
        for topic in projects.keys():
            self.create_topic_if_not_exists(f"{company}_{topic}")
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
                
                # Check if the paper has already been processed
                if paper["id"] in self.processed_paper_ids:
                    self.logger.info(f"Skipping already processed paper: {paper['id']}")
                    self.consumer.commit(msg)
                    continue

                company_idea = self.categorize_rank(paper, company_context)

                if company_idea:
                    self._produce_relevance(company, paper["id"], company_idea)

                for topic, context in projects.items():
                    project_idea = self.categorize_rank(paper, context)
                    if project_idea:
                        self._produce_relevance(f"{company}_{topic}", paper["id"], project_idea)

                # Mark the paper as processed
                self.processed_paper_ids.add(paper["id"])
                self._log_generated_idea(f"Project ({topic})", project_idea)

                # Commit the offset after processing the message
                self.consumer.commit(msg)
            except Exception as e:
                self.logger.error(f"Error processing ideas: {e}")
                time.sleep(60)

    def _produce_relevance(self, topic: str, key: str, idea: Dict):
        """Helper method to produce an idea to a Kafka topic"""
        try:
            json_str = json.dumps(idea)
            self.producer.produce(topic, key=key, value=json_str)
            self.producer.flush()
            self.logger.info(
                f"Generated relevance for paper: {idea['paper_title']} in topic: {topic}"
            )
        except TypeError as e:
            self.logger.error(f"JSON serialization error: {e}")

    def _log_generated_idea(self, idea_type: str, idea: Dict):
        """Helper method to log generated ideas"""
        print(f"Paper Title: {idea['paper_title']}")
        print(f"Context Type: {idea['context_type']}")
        print(f"Relevance Score: {idea['relevance_score']}")
        print("-" * 80)
