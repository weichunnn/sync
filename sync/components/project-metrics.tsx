'use client';

import { Card } from '@/components/ui/card';
import {
  LineChart,
  BarChart,
  Activity,
  Timer,
  Target,
  Users,
} from 'lucide-react';

interface MetricsProps {
  metrics: {
    accuracy?: string;
    responseTime?: string;
    processingTime?: string;
    dailyQueries?: string;
    dailyImages?: string;
    [key: string]: string | undefined;
  };
}

export function ProjectMetrics({ metrics }: MetricsProps) {
  // Helper function to get the appropriate icon for each metric
  const getMetricIcon = (key: string) => {
    switch (key) {
      case 'accuracy':
        return Target;
      case 'responseTime':
      case 'processingTime':
        return Timer;
      case 'dailyQueries':
      case 'dailyImages':
        return Activity;
      default:
        return LineChart;
    }
  };

  // Helper function to format metric names
  const formatMetricName = (key: string) => {
    return key
      .replace(/([A-Z])/g, ' $1')
      .replace(/^./, (str) => str.toUpperCase())
      .replace(/Time/g, 'Time');
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      {Object.entries(metrics).map(([key, value]) => {
        const Icon = getMetricIcon(key);

        return (
          <Card key={key} className="p-6">
            <div className="flex items-center gap-4">
              <div className="p-2 bg-primary/10 rounded-full">
                <Icon className="h-6 w-6 text-primary" />
              </div>
              <div>
                <p className="text-sm text-muted-foreground">
                  {formatMetricName(key)}
                </p>
                <p className="text-2xl font-semibold">{value}</p>
              </div>
            </div>
          </Card>
        );
      })}

      {/* Historical Performance Card */}
      <Card className="p-6 md:col-span-2">
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="font-medium">Historical Performance</h3>
            <select className="text-sm border rounded-md px-2 py-1">
              <option>Last 7 days</option>
              <option>Last 30 days</option>
              <option>Last 90 days</option>
            </select>
          </div>
          <div className="h-[200px] flex items-center justify-center text-muted-foreground">
            {/* Placeholder for actual chart */}
            <BarChart className="h-8 w-8" />
            <span className="ml-2">Chart visualization coming soon</span>
          </div>
        </div>
      </Card>
    </div>
  );
}
