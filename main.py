import os
from dotenv import load_dotenv
from arxiv_stream_processor import ArxivStreamProcessor

load_dotenv()

# Test cases
if __name__ == "__main__":
    # Set up configuration
    config = {
        'bootstrap_servers': os.getenv('CONFLUENT_BOOTSTRAP_SERVERS'),
        'api_key': os.getenv('CONFLUENT_API_KEY'),
        'api_secret': os.getenv('CONFLUENT_API_SECRET'),
        'llm_api_key': os.getenv('ANTHROPIC_API_KEY')
    }
    
    # Take in company context
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
    
    # Start paper streaming in multi-threaded mode
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