import { AIChat } from '@/components/ai-chat';

export default function AssistantPage() {
  return (
    <div className="max-w-4xl mx-auto space-y-8">
      <div>
        <h1 className="text-2xl font-semibold">AI Assistant</h1>
        <p className="text-muted-foreground">
          Ask questions about your projects and sources
        </p>
      </div>
      <AIChat />
    </div>
  );
}
