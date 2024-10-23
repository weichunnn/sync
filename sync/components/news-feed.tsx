'use client';

import { useState } from 'react';
import { Card } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { ScrollArea } from '@/components/ui/scroll-area';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { BookOpen, MessageSquare, Github, Bot, Search } from 'lucide-react';

interface NewsItem {
  id: string;
  source: 'arxiv' | 'reddit' | 'github' | 'huggingface';
  title: string;
  summary: string;
  timestamp: string;
  url: string;
  category: string;
  engagement: number;
  sourceIcon: any;
}
export const MOCK_NEWS: NewsItem[] = [
  {
    id: '1',
    source: 'arxiv',
    title: 'Efficient Fine-Tuning Strategies for Large Language Models',
    summary:
      'New research demonstrates 40% improvement in training efficiency through selective layer fine-tuning and adaptive learning rates. The paper introduces a novel approach called "Dynamic LoRA" that automatically adjusts adaptation parameters during training.',
    timestamp: '2h ago',
    url: '#',
    category: 'LLM',
    engagement: 156,
    sourceIcon: BookOpen,
  },
  {
    id: '2',
    source: 'reddit',
    title: 'Community Discussion: Best Practices for RAG in Production',
    summary:
      'Comprehensive thread discussing various approaches to production RAG systems. Topics include chunk size optimization, embedding model selection, and real-world performance metrics from different vector stores.',
    timestamp: '4h ago',
    url: '#',
    category: 'LLM',
    engagement: 324,
    sourceIcon: MessageSquare,
  },
  {
    id: '3',
    source: 'github',
    title: 'LangChain Releases New Memory Management System',
    summary:
      'Latest release includes improved context window management, better token counting, and a new system for handling long-running conversations with LLMs. Performance improvements show 30% reduction in token usage.',
    timestamp: '6h ago',
    url: '#',
    category: 'Tools',
    engagement: 892,
    sourceIcon: Github,
  },
  {
    id: '4',
    source: 'huggingface',
    title: 'New Open Source Code LLM Released: CodeWizard-34B',
    summary:
      'A new open-source code generation model trained on 2T tokens of code. Benchmarks show performance comparable to closed-source alternatives. Includes improved type inference and documentation generation.',
    timestamp: '8h ago',
    url: '#',
    category: 'LLM',
    engagement: 1247,
    sourceIcon: Bot,
  },
  {
    id: '5',
    source: 'arxiv',
    title: 'Attention Mechanism Breakthrough for Computer Vision',
    summary:
      'Researchers propose a new variant of self-attention specifically designed for vision tasks. Results show 25% improvement in computational efficiency while maintaining accuracy on standard benchmarks.',
    timestamp: '12h ago',
    url: '#',
    category: 'Computer Vision',
    engagement: 432,
    sourceIcon: BookOpen,
  },
  {
    id: '6',
    source: 'github',
    title: 'Major Update to MLflow Tracking System',
    summary:
      'Version 2.8 introduces new features for distributed training tracking, improved artifact management, and native support for popular LLM frameworks. Includes new dashboards for monitoring training progress.',
    timestamp: '1d ago',
    url: '#',
    category: 'MLOps',
    engagement: 567,
    sourceIcon: Github,
  },
  {
    id: '7',
    source: 'reddit',
    title: 'Discussion: Real-world Experiences with Model Quantization',
    summary:
      'Engineers share experiences implementing 4-bit and 8-bit quantization in production. Includes performance comparisons, memory usage statistics, and tips for maintaining model quality.',
    timestamp: '1d ago',
    url: '#',
    category: 'MLOps',
    engagement: 789,
    sourceIcon: MessageSquare,
  },
  {
    id: '8',
    source: 'huggingface',
    title: 'New Dataset Released: MultiModal-Instruct-200K',
    summary:
      'Large-scale dataset for training instruction-following models on multi-modal tasks. Includes image-text pairs, structured data, and code snippets with detailed instructions and responses.',
    timestamp: '1d ago',
    url: '#',
    category: 'Research',
    engagement: 645,
    sourceIcon: Bot,
  },
  {
    id: '9',
    source: 'arxiv',
    title: 'Scaling Laws of Domain-Specific LLM Training',
    summary:
      'Comprehensive study on how model performance scales with domain-specific training data. Reveals optimal strategies for data curation and model size selection based on domain characteristics.',
    timestamp: '2d ago',
    url: '#',
    category: 'Research',
    engagement: 892,
    sourceIcon: BookOpen,
  },
  {
    id: '10',
    source: 'github',
    title: 'TensorFlow Releases Advanced LLM Training Tools',
    summary:
      'New toolkit includes distributed training optimizations, automatic sharding strategies, and improved memory management for training large models on commodity hardware.',
    timestamp: '2d ago',
    url: '#',
    category: 'Tools',
    engagement: 1023,
    sourceIcon: Github,
  },
  {
    id: '11',
    source: 'reddit',
    title: 'Implementing RLHF: A Practical Guide',
    summary:
      'Detailed discussion on implementing RLHF in production, including reward model training, policy optimization, and handling human feedback collection. Includes case studies from multiple organizations.',
    timestamp: '2d ago',
    url: '#',
    category: 'LLM',
    engagement: 567,
    sourceIcon: MessageSquare,
  },
  {
    id: '12',
    source: 'huggingface',
    title: 'Vision Transformer Pre-trained on 1B Images',
    summary:
      'New vision transformer model demonstrates state-of-the-art performance on 25 downstream tasks. Includes pre-trained weights and fine-tuning scripts for common use cases.',
    timestamp: '3d ago',
    url: '#',
    category: 'Computer Vision',
    engagement: 789,
    sourceIcon: Bot,
  },
  {
    id: '13',
    source: 'arxiv',
    title: 'Emergent Abilities in Instruction-Tuned LLMs',
    summary:
      'Research reveals new emergent abilities in LLMs when fine-tuned on high-quality instruction data. Includes analysis of task complexity thresholds and model scale requirements.',
    timestamp: '3d ago',
    url: '#',
    category: 'Research',
    engagement: 1234,
    sourceIcon: BookOpen,
  },
  {
    id: '14',
    source: 'github',
    title: 'Ray Introduces New Distributed Training Framework',
    summary:
      'Latest release includes improved fault tolerance, dynamic resource allocation, and native integration with popular ML frameworks. Shows 2x speedup in distributed training scenarios.',
    timestamp: '4d ago',
    url: '#',
    category: 'MLOps',
    engagement: 445,
    sourceIcon: Github,
  },
  {
    id: '15',
    source: 'reddit',
    title: 'Vector Database Benchmarks: 2024 Edition',
    summary:
      'Comprehensive comparison of popular vector databases including Pinecone, Weaviate, and Milvus. Includes performance metrics, scaling characteristics, and cost analysis.',
    timestamp: '4d ago',
    url: '#',
    category: 'Tools',
    engagement: 678,
    sourceIcon: MessageSquare,
  },
];

const categories = [
  'All',
  'LLM',
  'Computer Vision',
  'MLOps',
  'Research',
  'Tools',
];
const sources = ['All', 'arxiv', 'reddit', 'github', 'huggingface'];
const sortOptions = ['Latest', 'Most Engaged', 'Trending'];

export function NewsFeed({ fullHeight = false }) {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [selectedSource, setSelectedSource] = useState('All');
  const [sortBy, setSortBy] = useState('Latest');

  const filteredNews = MOCK_NEWS.filter((item) => {
    if (selectedCategory !== 'All' && item.category !== selectedCategory)
      return false;
    if (selectedSource !== 'All' && item.source !== selectedSource)
      return false;
    if (
      searchQuery &&
      !item.title.toLowerCase().includes(searchQuery.toLowerCase())
    )
      return false;
    return true;
  }).sort((a, b) => {
    if (sortBy === 'Most Engaged') return b.engagement - a.engagement;
    // Add more sorting logic as needed
    return 0;
  });

  return (
    <Card className="p-6">
      <div className="space-y-4">
        {/* Search and Filters */}
        <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
          <div className="relative flex-1">
            <Search className="absolute left-2 top-2.5 h-4 w-4 text-muted-foreground" />
            <Input
              placeholder="Search updates..."
              className="pl-8"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>
          <div className="flex gap-2">
            <Select
              value={selectedCategory}
              onValueChange={setSelectedCategory}
            >
              <SelectTrigger className="w-[140px]">
                <SelectValue placeholder="Category" />
              </SelectTrigger>
              <SelectContent>
                {categories.map((category) => (
                  <SelectItem key={category} value={category}>
                    {category}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>

            <Select value={selectedSource} onValueChange={setSelectedSource}>
              <SelectTrigger className="w-[140px]">
                <SelectValue placeholder="Source" />
              </SelectTrigger>
              <SelectContent>
                {sources.map((source) => (
                  <SelectItem key={source} value={source}>
                    {source}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>

            <Select value={sortBy} onValueChange={setSortBy}>
              <SelectTrigger className="w-[140px]">
                <SelectValue placeholder="Sort by" />
              </SelectTrigger>
              <SelectContent>
                {sortOptions.map((option) => (
                  <SelectItem key={option} value={option}>
                    {option}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
        </div>

        {/* News Items */}
        <ScrollArea className={fullHeight ? 'h-[800px]' : 'h-[600px]'}>
          <div className="space-y-4">
            {filteredNews.map((item) => (
              <Card key={item.id} className="p-4">
                <div className="flex items-start gap-4">
                  <div className="flex-1 space-y-2">
                    <div className="flex items-center gap-2">
                      <item.sourceIcon className="h-4 w-4 text-muted-foreground" />
                      <Badge variant="secondary" className="capitalize">
                        {item.source}
                      </Badge>
                      <Badge variant="outline">{item.category}</Badge>
                      <span className="text-sm text-muted-foreground">
                        {item.timestamp}
                      </span>
                    </div>
                    <h3 className="font-medium">{item.title}</h3>
                    <p className="text-sm text-muted-foreground">
                      {item.summary}
                    </p>
                    <div className="flex items-center gap-4">
                      <span className="text-sm text-muted-foreground">
                        {item.engagement} engagements
                      </span>
                      <Button variant="ghost" size="sm">
                        Read More
                      </Button>
                    </div>
                  </div>
                </div>
              </Card>
            ))}
          </div>
        </ScrollArea>
      </div>
    </Card>
  );
}
