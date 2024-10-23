'use client';

import { Card } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Clock, ArrowRight } from 'lucide-react';
import Link from 'next/link';

interface RecentInsight {
  id: string;
  title: string;
  source: string;
  timestamp: string;
  type: 'paper' | 'discussion' | 'repository';
  relevance: 'high' | 'medium' | 'low';
}

const mockInsights: RecentInsight[] = [
  {
    id: '1',
    title: 'Improved RAG Techniques for Customer Support',
    source: 'arxiv/2402.12345',
    timestamp: '2 hours ago',
    type: 'paper',
    relevance: 'high',
  },
  {
    id: '2',
    title: 'New LangChain Integration Methods',
    source: 'github/langchain-ai/langchain',
    timestamp: '1 day ago',
    type: 'repository',
    relevance: 'medium',
  },
];

export function RecentInsights({ projectId }: { projectId?: string }) {
  return (
    <Card className="p-6">
      <div className="flex items-center justify-between mb-6">
        <h2 className="font-semibold">Recent Updates</h2>
        <Link href="/dashboard/insights">
          <Button variant="ghost" size="sm">
            View All
            <ArrowRight className="ml-2 h-4 w-4" />
          </Button>
        </Link>
      </div>

      <div className="space-y-4">
        {mockInsights.map((insight) => (
          <div
            key={insight.id}
            className="p-4 rounded-lg border bg-card hover:bg-accent/50 transition-colors"
          >
            <div className="flex items-start justify-between gap-4">
              <div className="space-y-1">
                <div className="flex items-center gap-2">
                  <Badge
                    variant={
                      insight.relevance === 'high'
                        ? 'destructive'
                        : insight.relevance === 'medium'
                        ? 'default'
                        : 'secondary'
                    }
                  >
                    {insight.type}
                  </Badge>
                  <span className="text-xs text-muted-foreground">
                    {insight.source}
                  </span>
                </div>
                <p className="font-medium">{insight.title}</p>
                <div className="flex items-center gap-2 text-xs text-muted-foreground">
                  <Clock className="h-3 w-3" />
                  {insight.timestamp}
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </Card>
  );
}
