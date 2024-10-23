'use client';

import { Card } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Switch } from '@/components/ui/switch';
import { Label } from '@/components/ui/label';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Github, BookOpen, MessagesSquare, Bot } from 'lucide-react';

const sources = [
  {
    id: 'github',
    name: 'GitHub',
    icon: Github,
    description: 'Track AI repositories and discussions',
    apiKeyRequired: true,
    options: {
      scanFrequency: ['hourly', 'daily', 'weekly'],
      topicFilters: ['machine-learning', 'nlp', 'computer-vision', 'llm'],
    },
  },
  {
    id: 'arxiv',
    name: 'ArXiv',
    icon: BookOpen,
    description: 'Latest AI research papers',
    apiKeyRequired: false,
    options: {
      categories: ['cs.AI', 'cs.LG', 'cs.CL', 'cs.CV'],
      updateFrequency: ['daily', 'weekly'],
    },
  },
  {
    id: 'reddit',
    name: 'Reddit',
    icon: MessagesSquare,
    description: 'AI community discussions',
    apiKeyRequired: true,
    options: {
      subreddits: ['MachineLearning', 'artificial', 'deeplearning'],
      sortBy: ['hot', 'new', 'top'],
    },
  },
  {
    id: 'huggingface',
    name: 'HuggingFace',
    icon: Bot,
    description: 'Model updates and implementations',
    apiKeyRequired: true,
    options: {
      modelTypes: ['all', 'text', 'vision', 'audio'],
      updateFrequency: ['daily', 'weekly'],
    },
  },
];

export function SourcesManager() {
  return (
    <div className="space-y-8">
      {sources.map((source) => (
        <Card key={source.id} className="p-6">
          <div className="space-y-6">
            {/* Header */}
            <div className="flex items-start justify-between">
              <div className="flex items-start gap-4">
                <source.icon className="h-8 w-8" />
                <div>
                  <h3 className="font-medium">{source.name}</h3>
                  <p className="text-sm text-muted-foreground">
                    {source.description}
                  </p>
                </div>
              </div>
              <Switch />
            </div>

            {/* Settings */}
            <div className="space-y-4 border-t pt-4">
              {source.apiKeyRequired && (
                <div className="space-y-2">
                  <Label htmlFor={`${source.id}-api-key`}>API Key</Label>
                  <Input
                    id={`${source.id}-api-key`}
                    type="password"
                    placeholder={`Enter ${source.name} API Key`}
                    className="max-w-md"
                  />
                </div>
              )}

              {/* Source-specific options */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {Object.entries(source.options).map(([key, values]) => (
                  <div key={key} className="space-y-2">
                    <Label htmlFor={`${source.id}-${key}`}>
                      {key
                        .replace(/([A-Z])/g, ' $1')
                        .replace(/^./, (str) => str.toUpperCase())}
                    </Label>
                    <Select>
                      <SelectTrigger id={`${source.id}-${key}`}>
                        <SelectValue placeholder={`Select ${key}`} />
                      </SelectTrigger>
                      <SelectContent>
                        {values.map((value: string) => (
                          <SelectItem key={value} value={value}>
                            {value
                              .replace(/([A-Z])/g, ' $1')
                              .replace(/^./, (str) => str.toUpperCase())}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </Card>
      ))}
    </div>
  );
}
