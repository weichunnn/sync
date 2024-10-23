import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Plus, Brain, Search } from 'lucide-react';
import Link from 'next/link';

export function QuickActions() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
      <Link href="/dashboard/projects/new">
        <Card className="p-4 hover:bg-accent transition-colors cursor-pointer">
          <div className="flex items-center gap-3">
            <Plus className="h-5 w-5" />
            <div>
              <h3 className="font-medium">New Project</h3>
              <p className="text-sm text-muted-foreground">
                Start a new AI project
              </p>
            </div>
          </div>
        </Card>
      </Link>
      <Link href="/dashboard/assistant">
        <Card className="p-4 hover:bg-accent transition-colors cursor-pointer">
          <div className="flex items-center gap-3">
            <Brain className="h-5 w-5" />
            <div>
              <h3 className="font-medium">AI Assistant</h3>
              <p className="text-sm text-muted-foreground">
                Get AI recommendations
              </p>
            </div>
          </div>
        </Card>
      </Link>
      <Link href="/dashboard/projects">
        <Card className="p-4 hover:bg-accent transition-colors cursor-pointer">
          <div className="flex items-center gap-3">
            <Search className="h-5 w-5" />
            <div>
              <h3 className="font-medium">Browse Projects</h3>
              <p className="text-sm text-muted-foreground">View all projects</p>
            </div>
          </div>
        </Card>
      </Link>
    </div>
  );
}
