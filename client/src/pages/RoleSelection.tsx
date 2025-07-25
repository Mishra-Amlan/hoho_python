import React from 'react';
import { useLocation } from 'wouter';
import { useAuth } from '@/contexts/AuthContext';
import { RoleCard } from '@/components/RoleCard';
import { Button } from '@/components/ui/button';
import { LogOut, Shield, UserCheck, Search, Building, Hotel } from 'lucide-react';

const roles = [
  {
    id: 'admin',
    title: 'Vendor Admin / Audit Coordinator',
    description: 'Manage audit schedules, coordinate teams, and oversee audit processes',
    icon: Shield,
    color: 'bg-red-500',
    path: '/admin'
  },
  {
    id: 'auditor',
    title: 'Guest Auditor (Vendor)',
    description: 'Conduct on-site audits, take photos, and complete checklists',
    icon: UserCheck,
    color: 'bg-blue-500',
    path: '/auditor'
  },
  {
    id: 'reviewer',
    title: 'Final Reviewer (Vendor)',
    description: 'Review completed audits, provide feedback, and approve reports',
    icon: Search,
    color: 'bg-green-500',
    path: '/reviewer'
  },
  {
    id: 'corporate',
    title: 'Corporate User (Client)',
    description: 'View analytics, download reports, and monitor compliance',
    icon: Building,
    color: 'bg-purple-500',
    path: '/corporate'
  },
  {
    id: 'hotelgm',
    title: 'Hotel GM / Manager (Client)',
    description: 'Access property-specific reports and compliance data',
    icon: Hotel,
    color: 'bg-orange-500',
    path: '/hotel-gm'
  }
];

export default function RoleSelection() {
  const [, setLocation] = useLocation();
  const { user, logout } = useAuth();

  const handleRoleSelect = (path: string) => {
    setLocation(path);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      <div className="container mx-auto px-4 py-8">
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">
              Welcome, {user?.name || user?.username}!
            </h1>
            <p className="text-gray-600 mt-2">
              Select your role to access the appropriate dashboard
            </p>
          </div>
          <Button variant="outline" onClick={logout}>
            <LogOut className="w-4 h-4 mr-2" />
            Sign Out
          </Button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 max-w-6xl mx-auto">
          {roles.map((role) => (
            <RoleCard
              key={role.id}
              {...role}
              onClick={() => handleRoleSelect(role.path)}
            />
          ))}
        </div>

        <div className="mt-12 text-center">
          <div className="bg-white rounded-lg shadow-sm p-6 max-w-2xl mx-auto">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">
              Demo Navigation
            </h2>
            <div className="flex flex-wrap gap-4 justify-center">
              <Button 
                variant="outline" 
                onClick={() => setLocation('/ai-demo')}
              >
                AI Photo Analysis Demo
              </Button>
              <Button 
                variant="outline" 
                onClick={() => setLocation('/user-flow-demo')}
              >
                User Flow Demo
              </Button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}