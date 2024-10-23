'use client';

import { CompanyOverview } from '@/components/company-overview';
import { ActiveProjects } from '@/components/active-projects';
import { RelevantUpdates } from '@/components/relevant-updates';
import { useKafkaConsumer } from '@/hooks/use-kafka-consumer';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { AlertCircle } from 'lucide-react';

export default function DashboardPage() {
  const company = {
    name: 'Nexus AI',
    description:
      'Transforming tomorrow through intelligent automation and adaptive AI solutions',
    focus: ['Machine Learning', 'NLP', 'Computer Vision'],
  };

  return (
    <div className="max-w-6xl mx-auto space-y-8">
      <CompanyOverview company={company} />
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <ActiveProjects />
        </div>
        <div>
          <RelevantUpdates />
        </div>
      </div>
    </div>
  );
}
