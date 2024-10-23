'use client';

import { Card } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Brain, TrendingUp, AlertCircle } from 'lucide-react';

// This would come from your API
const insights = [
  {
    id: '1',
    type: 'recommendation',
    title: 'Consider implementing RAG',
    description: 'Recent papers show 30% improvement in response accuracy',
    source: 'arxiv/2402.12345',
    impact: 'high',
  },
  {
    id: '2',
    type: 'trend',
    title: 'New LLM Fine-tuning Method',
    description: 'More efficient training for customer support scenarios',
    source: 'github/microsoft/deepspeed',
    impact: 'medium',
  },
];

export function ProjectInsights({ id }: { id: string }) {
  return (
    <Card className="p-6">
      <div className="flex items-center gap-2 mb-6">
        <Brain className="h-5 w-5 text-primary" />
        <h2 className="font-semibold">AI Insights</h2>
      </div>

      <div className="space-y-4">
        {insights.map((insight) => (
          <div
            key={insight.id}
            className="p-4 rounded-lg border bg-card hover:bg-accent transition-colors"
          >
            <div className="flex items-start gap-4">
              <div className="space-y-1">
                <div className="flex items-center gap-2">
                  <Badge
                    variant={
                      insight.impact === 'high' ? 'destructive' : 'secondary'
                    }
                  >
                    {insight.impact} impact
                  </Badge>
                  <span className="text-xs text-muted-foreground">
                    {insight.source}
                  </span>
                </div>
                <h3 className="font-medium">{insight.title}</h3>
                <p className="text-sm text-muted-foreground">
                  {insight.description}
                </p>
              </div>
            </div>
          </div>
        ))}
      </div>
    </Card>
  );
}
