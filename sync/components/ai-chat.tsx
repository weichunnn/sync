'use client';

import { useState } from 'react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Brain } from 'lucide-react';

export function AIChat() {
  const [query, setQuery] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    // Implement your AI query logic here
    await new Promise((resolve) => setTimeout(resolve, 1000)); // Simulate API call
    setIsLoading(false);
  };

  return (
    <Card className="p-6">
      <form onSubmit={handleSubmit} className="space-y-4">
        <Textarea
          placeholder="Ask about your projects or get recommendations..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="min-h-[100px]"
        />
        <Button disabled={isLoading} className="w-full">
          <Brain className="mr-2 h-4 w-4" />
          {isLoading ? 'Thinking...' : 'Ask AI Assistant'}
        </Button>
      </form>

      {/* Response area will be implemented here */}
      <div className="mt-6 space-y-4">
        {/* AI responses will appear here */}
      </div>
    </Card>
  );
}
