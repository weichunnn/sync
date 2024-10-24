'use client';

import { Card } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import Link from 'next/link';
import { projects } from '@/data/projects';

export function ActiveProjects() {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-xl font-semibold">Active Projects</h2>
        <p className="text-sm text-muted-foreground">
          Your current AI initiatives
        </p>
      </div>

      <div className="space-y-4">
        {projects.map((project, index) => (
          <div key={project.id}>
            <Link href={`/dashboard/projects/${project.id}`}>
              <Card className="p-4 hover:bg-accent/50 transition-colors">
                <div className="space-y-2">
                  <div className="flex items-center justify-between">
                    <h3 className="font-medium">{project.name}</h3>
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
              </Card>
            </Link>
            {index < projects.length - 1 && (
              <div className="h-px bg-border mt-4" />
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
