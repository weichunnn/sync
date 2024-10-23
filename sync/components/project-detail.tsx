'use client';

import { Card } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { RelevantUpdates } from '@/components/relevant-updates';
import { Clock, AlertCircle, CheckCircle2, Circle } from 'lucide-react';

export function ProjectDetail({ project }) {
  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'open':
        return <Circle className="h-4 w-4 text-green-500" />;
      case 'in_progress':
        return <Clock className="h-4 w-4 text-yellow-500" />;
      default:
        return <CheckCircle2 className="h-4 w-4 text-gray-500" />;
    }
  };

  const getPriorityBadge = (priority: string) => {
    switch (priority) {
      case 'high':
        return <Badge variant="destructive">High</Badge>;
      case 'medium':
        return <Badge variant="default">Medium</Badge>;
      default:
        return <Badge variant="secondary">Low</Badge>;
    }
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <div className="lg:col-span-2 space-y-6">
        {/* Project Header */}
        <div>
          <div className="flex items-center gap-3 mb-4">
            <div>
              <h1 className="text-2xl font-semibold">{project.name}</h1>
              <p className="text-muted-foreground">{project.description}</p>
            </div>
          </div>
          <div className="flex gap-2">
            {project.techStack.map((tech) => (
              <Badge key={tech} variant="secondary">
                {tech}
              </Badge>
            ))}
          </div>
        </div>

        {/* Issues List */}
        <Card className="p-6">
          <h3 className="font-medium mb-4">Active Issues</h3>
          <div className="space-y-4">
            {project.issues.map((issue) => (
              <div
                key={issue.title}
                className="flex items-start justify-between border-b last:border-0 pb-4 last:pb-0"
              >
                <div className="flex items-start gap-3">
                  {getStatusIcon(issue.status)}
                  <div>
                    <h4 className="font-medium">{issue.title}</h4>
                    <div className="flex items-center gap-2 mt-1 text-sm text-muted-foreground">
                      <span>Opened {issue.created}</span>
                      <span>•</span>
                      <span>Assigned to {issue.assignee}</span>
                    </div>
                  </div>
                </div>
                {getPriorityBadge(issue.priority)}
              </div>
            ))}
          </div>
        </Card>

        {/* Team Members */}
        <Card className="p-6">
          <h3 className="font-medium mb-4">Team</h3>
          <div className="space-y-4">
            {project.teamMembers.map((member) => (
              <div key={member.name} className="flex items-center gap-3">
                <img
                  src={member.avatar}
                  alt={member.name}
                  className="h-8 w-8 rounded-full"
                />
                <div>
                  <p className="font-medium">{member.name}</p>
                  <p className="text-sm text-muted-foreground">{member.role}</p>
                </div>
              </div>
            ))}
          </div>
        </Card>
      </div>

      {/* Right Sidebar */}
      <div>
        <RelevantUpdates />
      </div>
    </div>
  );
}
