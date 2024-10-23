import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/button';
import Link from 'next/link';
import { LayoutDashboard, Newspaper, Brain, Radio } from 'lucide-react';

const navigation = [
  {
    name: 'Overview',
    href: '/dashboard',
    icon: LayoutDashboard,
  },
  {
    name: 'News Feed',
    href: '/dashboard/news',
    icon: Newspaper,
  },
  {
    name: 'AI Assistant',
    href: '/dashboard/assistant',
    icon: Brain,
  },
  {
    name: 'Sources',
    href: '/dashboard/sources',
    icon: Radio,
  },
];

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="min-h-screen flex">
      <div className="hidden md:flex w-64 flex-col fixed inset-y-0 z-50 bg-white border-r">
        <div className="p-6 border-b">
          <h1 className="text-xl font-semibold">Re:Sync</h1>
        </div>
        <nav className="flex-1 flex flex-col gap-2 p-4">
          {navigation.map((item) => (
            <Link key={item.name} href={item.href}>
              <Button variant="ghost" className="w-full justify-start gap-2">
                <item.icon className="h-4 w-4" />
                {item.name}
              </Button>
            </Link>
          ))}
        </nav>
      </div>
      <div className="flex-1 md:pl-64">
        <div className="h-full p-8">{children}</div>
      </div>
    </div>
  );
}
