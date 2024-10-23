import { Card } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Building2, Cpu, GitBranch, Users } from 'lucide-react';

interface CompanyOverviewProps {
  company: {
    name: string;
    description: string;
    focus: string[];
  };
}

export function CompanyOverview({ company }: CompanyOverviewProps) {
  return (
    <Card className="p-6">
      <div className="space-y-6">
        {/* Company Header */}
        <div className="space-y-2">
          <div className="flex items-center gap-2">
            <Building2 className="h-5 w-5 text-primary" />
            <h1 className="text-2xl font-semibold">{company.name}</h1>
          </div>
          <p className="text-muted-foreground">{company.description}</p>
        </div>

        {/* Focus Areas */}
        <div className="space-y-2">
          <h2 className="text-sm font-medium text-muted-foreground">
            Focus Areas
          </h2>
          <div className="flex flex-wrap gap-2">
            {company.focus.map((area) => (
              <Badge key={area} variant="secondary">
                {area}
              </Badge>
            ))}
          </div>
        </div>
      </div>
    </Card>
  );
}
