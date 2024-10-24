'use client';

import { Card } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Clock, ArrowUpRight } from 'lucide-react';
import { KafkaMessage } from '@/types/kafka';

// This would come from your API
const updates = [
  {
    id: '1',
    title: 'New RAG Implementation Method',
    source: 'arxiv/2402.12345',
    relevanceScore: 0.95,
    timestamp: '2 hours ago',
    type: 'research',
    relatedProject: 'Customer Support AI',
  },
  {
    id: '2',
    title: 'Improved Vision Transformers',
    source: 'github/microsoft/vision',
    relevanceScore: 0.93,
    timestamp: '1 day ago',
    type: 'code',
    relatedProject: 'Vision Analytics Pipeline',
  },
  {
    id: '3',
    title: 'Optimized Parameter Tuning Framework',
    source: 'huggingface/optimizers',
    relevanceScore: 0.9,
    timestamp: '4 hours ago',
    type: 'code',
    relatedProject: 'Model Performance Optimization',
  },
  {
    id: '4',
    title: 'Attention Mechanism Efficiency Study',
    source: 'arxiv/2402.12789',
    relevanceScore: 0.85,
    timestamp: '12 hours ago',
    type: 'research',
    relatedProject: 'Model Performance Optimization',
  },
];

interface RelevantUpdatesProps {
  messages: KafkaMessage[];
}

export function RelevantUpdates() {
  return (
    <Card className="p-6">
      <div className="flex items-center justify-between mb-6">
        <h2 className="font-semibold">Relevant Updates</h2>
      </div>

      <div className="space-y-4">
        {updates.map((update) => (
          <div
            key={update.id}
            className="p-4 rounded-lg border bg-card hover:bg-accent/50 transition-colors"
          >
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <Badge variant="outline">
                  {Math.round(update.relevanceScore * 100)}% match
                </Badge>
                <span className="text-xs text-muted-foreground">
                  {update.type}
                </span>
              </div>
              <p className="font-medium">{update.title}</p>
              <div className="flex items-center justify-between text-xs text-muted-foreground">
                <div className="flex items-center gap-2">
                  <Clock className="h-3 w-3" />
                  {update.timestamp}
                </div>
                <div className="flex items-center gap-1">
                  <span>{update.source}</span>
                  <ArrowUpRight className="h-3 w-3" />
                </div>
              </div>
              <div className="text-xs text-muted-foreground">
                Related to: {update.relatedProject}
              </div>
            </div>
          </div>
        ))}
      </div>
    </Card>
  );
}

//export function RelevantUpdates({ messages = [] }: RelevantUpdatesProps) {
//  return (
//    <Card className="p-6">
//      <div className="flex items-center justify-between mb-6">
//        <h2 className="font-semibold">Relevant Updates</h2>
//      </div>

//      <div className="space-y-4">
//        {messages.map((message, index) => {
//          const update = JSON.parse(message.value);
//          return (
//            <div
//              key={index}
//              className="p-4 rounded-lg border bg-card hover:bg-accent/50 transition-colors"
//            >
//              <div className="space-y-2">
//                <div className="flex items-center justify-between">
//                  <Badge variant="outline">{message.topic}</Badge>
//                </div>
//                <p className="font-medium">{update.title}</p>
//                <div className="flex items-center justify-between text-xs text-muted-foreground">
//                  <div className="flex items-center gap-2">
//                    <Clock className="h-3 w-3" />
//                    {new Date(Number(message.timestamp)).toRelativeTimeString()}
//                  </div>
//                  {update.source && (
//                    <div className="flex items-center gap-1">
//                      <span>{update.source}</span>
//                      <ArrowUpRight className="h-3 w-3" />
//                    </div>
//                  )}
//                </div>
//              </div>
//            </div>
//          );
//        })}

//        {messages.length === 0 && (
//          <div className="text-sm text-muted-foreground text-center py-4">
//            No updates yet
//          </div>
//        )}
//      </div>
//    </Card>
//  );
//}
