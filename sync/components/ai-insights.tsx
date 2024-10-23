'use client';

import { Card } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import {
  Brain,
  TrendingUp,
  AlertCircle,
  Lightbulb,
  ArrowRight,
} from 'lucide-react';

interface Insight {
  id: string;
  type: 'trend' | 'alert' | 'recommendation';
  title: string;
  description: string;
  impact: 'high' | 'medium' | 'low';
  timestamp: string;
}

const insights: Insight[] = [
  {
    id: '1',
    type: 'trend',
    title: 'Rising Interest in LLM Fine-tuning',
    description:
      'Significant increase in research papers and discussions about efficient LLM fine-tuning methods.',
    impact: 'high',
    timestamp: '2h ago',
  },
  {
    id: '2',
    type: 'alert',
    title: 'New Breakthrough in Computer Vision',
    description:
      'Novel architecture achieving SOTA results on ImageNet with 50% less compute.',
    impact: 'medium',
    timestamp: '4h ago',
  },
  {
    id: '3',
    type: 'recommendation',
    title: 'Consider Implementing RAG',
    description:
      'Based on your stack, implementing Retrieval Augmented Generation could improve accuracy.',
    impact: 'high',
    timestamp: '6h ago',
  },
];

const typeIcons = {
  trend: TrendingUp,
  alert: AlertCircle,
  recommendation: Lightbulb,
};

export default function AIInsights() {
  return (
    <Card className="p-6">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-2">
          <Brain className="h-5 w-5 text-primary" />
          <h2 className="font-semibold">AI Insights</h2>
        </div>
        <Button variant="ghost" size="sm" className="gap-2">
          View All <ArrowRight className="h-4 w-4" />
        </Button>
      </div>

      <div className="space-y-4">
        {insights.map((insight) => {
          const Icon = typeIcons[insight.type];
          return (
            <div
              key={insight.id}
              className="p-4 rounded-lg border bg-card hover:bg-accent transition-colors"
            >
              <div className="flex items-start gap-4">
                <div className="rounded-full p-2 bg-primary/10">
                  <Icon className="h-4 w-4 text-primary" />
                </div>
                <div className="flex-1 space-y-1">
                  <div className="flex items-center justify-between">
                    <Badge
                      variant={
                        insight.impact === 'high'
                          ? 'destructive'
                          : insight.impact === 'medium'
                          ? 'default'
                          : 'secondary'
                      }
                    >
                      {insight.impact} impact
                    </Badge>
                    <span className="text-sm text-muted-foreground">
                      {insight.timestamp}
                    </span>
                  </div>
                  <h3 className="font-medium">{insight.title}</h3>
                  <p className="text-sm text-muted-foreground">
                    {insight.description}
                  </p>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </Card>
  );
}
