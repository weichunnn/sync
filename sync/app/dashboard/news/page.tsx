import { NewsFeed } from '@/components/news-feed';

export default async function NewsPage() {
  return (
    <div className="max-w-6xl mx-auto space-y-8">
      <div>
        <h1 className="text-2xl font-semibold">News Feed</h1>
        <p className="text-muted-foreground">Latest updates from AI sources</p>
      </div>
      <NewsFeed />
    </div>
  );
}
