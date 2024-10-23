'use client';

import { Card } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Plus, ArrowRight } from 'lucide-react';

const projects = [
  {
    id: 1,
    name: 'Customer Support AI',
    description: 'LLM-powered support automation system',
    status: 'active',
    lastUpdated: '2 hours ago',
    techStack: ['LangChain', 'GPT-4'],
    updates: 2,
  },
  // ... other projects
];

export function ProjectsList() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-semibold">Your Projects</h2>
          <p className="text-sm text-muted-foreground">
            Manage and monitor your AI projects
          </p>
        </div>
        <Button>
          <Plus className="mr-2 h-4 w-4" />
          New Project
        </Button>
      </div>

      {projects.map((project) => (
        <Card
          key={project.id}
          className="p-4 hover:bg-accent/50 transition-colors"
        >
          <div className="flex items-start justify-between">
            <div className="space-y-1">
              <div className="flex items-center gap-2">
                <h3 className="font-medium">{project.name}</h3>
                {project.updates > 0 && (
                  <Badge>{project.updates} updates</Badge>
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
            <Button variant="ghost" size="sm">
              View Details
              <ArrowRight className="ml-2 h-4 w-4" />
            </Button>
          </div>
        </Card>
      ))}
    </div>
  );
}
