'use client';

import { Card } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { ArrowRight } from 'lucide-react';
import Link from 'next/link';

const projects = [
  {
    id: 1,
    name: 'Customer Support AI',
    description: 'LLM-powered support automation system',
    status: 'active',
    lastUpdated: '2 hours ago',
    techStack: ['LangChain', 'GPT-4'],
    insights: 3,
  },
  {
    id: 2,
    name: 'Vision Analytics Pipeline',
    description: 'Computer vision for quality control',
    status: 'active',
    lastUpdated: '1 day ago',
    techStack: ['PyTorch', 'OpenCV'],
    insights: 2,
  },
];

export function ProjectsOverview() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-semibold">Active Projects</h2>
        <Link href="/dashboard/projects">
          <Button variant="ghost" size="sm">
            View All
            <ArrowRight className="ml-2 h-4 w-4" />
          </Button>
        </Link>
      </div>

      <div className="space-y-4">
        {projects.map((project) => (
          <Link key={project.id} href={`/dashboard/projects/${project.id}`}>
            <Card className="p-4 hover:bg-accent/50 transition-colors">
              <div className="flex items-start justify-between">
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <h3 className="font-medium">{project.name}</h3>
                    {project.insights > 0 && (
                      <Badge>{project.insights} new insights</Badge>
                    )}
                  </div>
                  <p className="text-sm text-muted-foreground">
                    {project.description}
                  </p>
                  <div className="flex gap-2">
                    {project.techStack.map((tech) => (
                      <Badge key={tech} variant="secondary">
                        {tech}
                      </Badge>
                    ))}
                  </div>
                </div>
                <span className="text-sm text-muted-foreground">
                  {project.lastUpdated}
                </span>
              </div>
            </Card>
          </Link>
        ))}
      </div>
    </div>
  );
}
