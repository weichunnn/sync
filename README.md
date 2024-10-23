# Re:Sync

A real-time AI project monitoring platform built with Next.js and Confluent Kafka.

## Overview

Re:Sync helps organizations track their AI initiatives by aggregating insights from multiple sources in real-time. It provides a unified interface for monitoring project metrics, related research, and community discussions.

## Features

- **Real-time Project Monitoring**: Track AI project metrics and updates via Kafka streams
- **Research Integration**: Automatically aggregates relevant papers from ArXiv
- **Community Insights**: Monitors Reddit discussions and GitHub issues
- **Source Management**: Configure and manage multiple data sources
- **AI Assistant**: Get contextual help and insights about your projects

## Tech Stack

- **Frontend**: Next.js 15, React, Tailwind CSS, shadcn/ui
- **Backend**: Confluent Kafka for real-time data streaming
- **Data Sources**:
  - ArXiv API
  - Reddit API
  - GitHub API
  - HuggingFace Hub

## Getting Started

```bash
# Install dependencies
npm install

# Run the development server
npm run dev

# Build for production
npm run build
```

## Project Structure

```
app/
├── dashboard/           # Main dashboard views
│   ├── projects/       # Project management
│   ├── sources/        # Data source configuration
│   └── assistant/      # AI assistant interface
├── components/         # Reusable components
└── data/              # Mock data and types
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT License - see LICENSE.md for details
