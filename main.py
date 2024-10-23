import os
from dotenv import load_dotenv
from arxiv_stream_processor import ArxivStreamProcessor

load_dotenv()

if __name__ == "__main__":
    config = {
        "bootstrap_servers": os.getenv("CONFLUENT_BOOTSTRAP_SERVERS"),
        "api_key": os.getenv("CONFLUENT_API_KEY"),
        "api_secret": os.getenv("CONFLUENT_API_SECRET"),
        "llm_api_key": os.getenv("ANTHROPIC_API_KEY"),
    }

    company_context = {
        "industry": "Artificial Intelligence",
        "research_focus": [
            "Natural Language Processing",
            "Computer Vision",
            "Reinforcement Learning",
        ],
        "current_projects": [
            "Large Language Model Development",
            "Multi-modal AI Systems",
            "AI-assisted Code Generation",
        ],
        "core_technologies": [
            "Transformer Architecture",
            "Deep Learning",
            "Federated Learning",
        ],
        "available_resources": [
            "GPU/TPU Clusters",
            "Massive Text Corpora",
            "Proprietary Datasets",
            "Cloud Computing Infrastructure",
        ],
    }

    processor = ArxivStreamProcessor(**config)

    processor.create_topic_if_not_exists("arxiv_papers_v5")
    processor.create_topic_if_not_exists("research_ideas")

    import threading

    categories = ["cs.AI", "cs.CL", "cs.CV", "cs.LG", "stat.ML"]

    streaming_thread = threading.Thread(
        target=processor.stream_papers_to_kafka,
        args=(categories, "arxiv_papers_v5", company_context),
    )
    streaming_thread.daemon = True
    streaming_thread.start()

    project_contexts = {
        "llm_development": {
            "name": "Large Language Model Development",
            "goals": ["Improve model efficiency", "Enhance multi-lingual capabilities"],
            "challenges": [
                "Reducing training time and costs",
                "Addressing bias in language models",
            ],
        },
        "multimodal_ai": {
            "name": "Multi-modal AI Systems",
            "goals": ["Integrate vision and language understanding", "Develop cross-modal reasoning"],
            "challenges": [
                "Aligning different modalities",
                "Handling diverse data types efficiently",
            ],
        },
    }

    processor.process_ideas(
        input_topic="arxiv_papers_v7",
        company="sonnet_ai",
        company_context=company_context,
        projects=project_contexts
    )