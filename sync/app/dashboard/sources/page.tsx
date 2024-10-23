import { SourcesManager } from '@/components/sources-manager';

export default function SourcesPage() {
  return (
    <div className="max-w-4xl mx-auto space-y-8">
      <div>
        <h1 className="text-2xl font-semibold">Sources</h1>
        <p className="text-muted-foreground">
          Manage your AI intelligence sources
        </p>
      </div>
      <SourcesManager />
    </div>
  );
}
