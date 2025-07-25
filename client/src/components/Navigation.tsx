import { useAuth } from '@/contexts/AuthContext';
import { Button } from '@/components/ui/button';
import { useLocation } from 'wouter';

interface NavigationProps {
  role?: string;
}

export function Navigation({ role }: NavigationProps = {}) {
  const { user, logout } = useAuth();
  const [, setLocation] = useLocation();

  const handleLogout = () => {
    logout();
    setLocation('/');
  };

  if (!user) return null;

  const roleColors = {
    admin: 'border-orange-500',
    auditor: 'border-green-500',
    reviewer: 'border-purple-500',
    corporate: 'border-amber-500',
    hotelgm: 'border-blue-600'
  };

  const roleBadgeColors = {
    admin: 'bg-orange-500',
    auditor: 'bg-green-500', 
    reviewer: 'bg-purple-500',
    corporate: 'bg-amber-500',
    hotelgm: 'bg-blue-600'
  };

  const roleNames = {
    admin: 'Admin',
    auditor: 'Guest Auditor',
    reviewer: 'QA Reviewer', 
    corporate: 'QA Corporate',
    hotelgm: 'Hotel GM'
  };

  const currentRole = role || user?.role || 'admin';
  
  return (
    <nav className={`bg-white shadow-lg border-b-4 ${roleColors[currentRole] || 'border-blue-500'}`}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <i className="fas fa-hotel text-2xl text-blue-600 mr-3"></i>
            <span className="text-xl font-bold text-gray-800">Hotel Audit Platform</span>
            <span className={`ml-4 px-3 py-1 ${roleBadgeColors[currentRole] || 'bg-blue-500'} text-white text-sm rounded-full`}>
              {roleNames[currentRole] || 'User'}
            </span>
          </div>
          <div className="flex items-center space-x-4">
            <span className="text-sm text-gray-600">Welcome, {user.name}</span>
            <button className="text-gray-600 hover:text-gray-800">
              <i className="fas fa-bell"></i>
            </button>
            <button className="text-gray-600 hover:text-gray-800">
              <i className="fas fa-user-circle"></i>
            </button>
            <Button 
              variant="outline" 
              size="sm"
              onClick={handleLogout}
            >
              Logout
            </Button>
          </div>
        </div>
      </div>
    </nav>
  );
}