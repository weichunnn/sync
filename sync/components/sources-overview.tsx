'use client';

import { Card } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { BookOpen, MessageSquare, Github, Box } from 'lucide-react';

interface Source {
  name: string;
  icon: any;
  count: number;
  total: number;
}

const sources: Source[] = [
  {
    name: 'ArXiv',
    icon: BookOpen,
    count: 156,
    total: 200,
  },
  {
    name: 'Reddit',
    icon: MessageSquare,
    count: 89,
    total: 100,
  },
  // Add more sources...
];

export function SourcesOverview() {
  return (
    <Card className="p-6">
      <h2 className="text-lg font-semibold mb-4">Sources</h2>
      <div className="space-y-4">
        {sources.map((source) => (
          <div key={source.name} className="space-y-2">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <source.icon className="h-4 w-4 text-muted-foreground" />
                <span className="font-medium">{source.name}</span>
              </div>
              <span className="text-sm text-muted-foreground">
                {source.count}/{source.total}
              </span>
            </div>
            <Progress value={(source.count / source.total) * 100} />
          </div>
        ))}
      </div>
    </Card>
  );
}
