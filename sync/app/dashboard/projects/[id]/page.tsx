import { ProjectDetail } from '@/components/project-detail';
import { projects } from '@/data/projects';
import { notFound } from 'next/navigation';

export default async function ProjectPage({
  params,
}: {
  params: { id: string };
}) {
  const project = projects.find((p) => p.id === parseInt(params.id));

  if (!project) {
    notFound();
  }

  return (
    <div className="max-w-7xl mx-auto space-y-8">
      <ProjectDetail project={project} />
    </div>
  );
}
