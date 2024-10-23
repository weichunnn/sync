# ArXiv Stream Processor

## Description

ArXiv Stream Processor is a Python-based application that streams and processes papers from ArXiv, focusing on specific categories related to Artificial Intelligence and Machine Learning. It uses Apache Kafka for streaming and processes the papers to generate research ideas based on the company's context and current projects.

## Features

- Streams papers from ArXiv in real-time
- Processes papers using AI to generate research ideas
- Utilizes Apache Kafka for efficient data streaming
- Supports multiple AI and ML categories (cs.AI, cs.CL, cs.CV, cs.LG, stat.ML)
- Configurable company context and project settings

## Prerequisites

- Python 3.x
- Apache Kafka
- Confluent Kafka Python client
- Anthropic API access (for AI processing)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/arxiv-stream-processor.git
   cd arxiv-stream-processor
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up your environment variables in a `.env` file:
   ```
   CONFLUENT_BOOTSTRAP_SERVERS=your_kafka_bootstrap_servers
   CONFLUENT_API_KEY=your_confluent_api_key
   CONFLUENT_API_SECRET=your_confluent_api_secret
   ANTHROPIC_API_KEY=your_anthropic_api_key
   ```

## Usage

Run the main script to start streaming and processing papers:

  ```
  python main.py

  ```

The script will:
1. Create necessary Kafka topics if they don't exist
2. Start streaming ArXiv papers to the "arxiv_papers" topic
3. Process the papers and generate research ideas based on the company context and project settings

## Configuration

You can modify the following in the `main.py` file:
- Company context
- Project contexts
- ArXiv categories to stream

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License

## Acknowledgements

- ArXiv for providing access to research papers
- Confluent Cloud for robust data streaming capabilities
- Anthropic for AI processing capabilities