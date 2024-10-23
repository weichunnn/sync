import { Card } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { BookOpen, ArrowUpRight } from 'lucide-react';

export function ProjectPapers({ papers }) {
  return (
    <div className="space-y-4">
      {papers.map((paper) => (
        <Card key={paper.title} className="p-6">
          <div className="space-y-4">
            <div className="flex items-start justify-between">
              <div className="space-y-1">
                <div className="flex items-center gap-2">
                  <BookOpen className="h-4 w-4 text-primary" />
                  <Badge variant="outline">
                    {Math.round(paper.relevance * 100)}% relevant
                  </Badge>
                </div>
                <h3 className="font-medium">{paper.title}</h3>
                <p className="text-sm text-muted-foreground">
                  {paper.authors.join(', ')}
                </p>
              </div>
              <Button variant="ghost" size="sm">
                Read Paper
                <ArrowUpRight className="ml-2 h-4 w-4" />
              </Button>
            </div>
            <p className="text-sm text-muted-foreground">{paper.summary}</p>
            <div className="flex items-center justify-between text-xs text-muted-foreground">
              <span>{paper.date}</span>
              <span>{paper.source}</span>
            </div>
          </div>
        </Card>
      ))}
    </div>
  );
}
