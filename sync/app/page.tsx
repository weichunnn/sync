import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import {
  ArrowRight,
  Github,
  BookOpen,
  MessagesSquare,
  Bot,
} from 'lucide-react';

export default function Home() {
  const sources = [
    {
      name: 'ArXiv Papers',
      icon: BookOpen,
      description: 'Latest research papers in AI and Machine Learning',
    },
    {
      name: 'Reddit Discussions',
      icon: MessagesSquare,
      description: 'Community insights and trending topics',
    },
    {
      name: 'HuggingFace',
      icon: Bot,
      description: 'New models and implementations',
    },
    {
      name: 'GitHub Projects',
      icon: Github,
      description: 'Open source developments and trends',
    },
  ];

  return (
    <div className="flex flex-col min-h-screen">
      {/* Navigation */}
      <header className="border-b">
        <div className="container mx-auto px-4 h-14 flex items-center justify-between">
          <h1 className="font-semibold">Re:Sync</h1>
          <Link href="/dashboard">
            <Button variant="outline">
              Open Dashboard
              <ArrowRight className="ml-2 h-4 w-4" />
            </Button>
          </Link>
        </div>
      </header>

      {/* Hero Section */}
      <section className="flex-1">
        <div className="container mx-auto px-4 py-20">
          <div className="max-w-2xl mx-auto text-center mb-16">
            <h2 className="text-4xl font-bold tracking-tight mb-4">
              Stay Ahead with Re:Sync
            </h2>
            <p className="text-lg text-gray-600 mb-8">
              Aggregate insights from multiple sources to power your AI
              initiatives
            </p>
            <Link href="/dashboard">
              <Button size="lg">
                View Re:Sync Dashboard
                <ArrowRight className="ml-2 h-4 w-4" />
              </Button>
            </Link>
          </div>

          {/* Source Grid */}
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-4">
            {sources.map((source) => (
              <Card key={source.name} className="p-6">
                <source.icon className="h-8 w-8 mb-4" />
                <h3 className="font-semibold mb-2">{source.name}</h3>
                <p className="text-sm text-gray-600">{source.description}</p>
              </Card>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}
