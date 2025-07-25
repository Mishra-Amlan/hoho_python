import { Card, CardContent } from '@/components/ui/card';
import { LucideIcon } from 'lucide-react';

interface RoleCardProps {
  id: string;
  title: string;
  description: string;
  icon: LucideIcon;
  color: string;
  path: string;
  onClick: () => void;
}

export function RoleCard({ id, title, description, icon: Icon, color, onClick }: RoleCardProps) {
  return (
    <Card 
      className="cursor-pointer transition-all hover:shadow-lg hover:scale-105 border-2 border-gray-200 hover:border-blue-300"
      onClick={onClick}
    >
      <CardContent className="p-6">
        <div className="text-center">
          <div className={`w-16 h-16 ${color} rounded-full flex items-center justify-center mx-auto mb-4`}>
            <Icon className="text-white text-2xl w-8 h-8" />
          </div>
          <h3 className="text-xl font-semibold text-gray-800 mb-2">{title}</h3>
          <p className="text-gray-600 text-sm">{description}</p>
        </div>
      </CardContent>
    </Card>
  );
}
