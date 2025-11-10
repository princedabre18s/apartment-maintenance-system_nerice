import { Outlet, Link, useLocation } from 'react-router-dom';
import { Home, FileText, Users, UserCog, Building } from 'lucide-react';

export default function Layout() {
  const location = useLocation();
  
  const isActive = (path) => {
    if (path === '/') return location.pathname === '/';
    return location.pathname.startsWith(path);
  };
  
  const navItems = [
    { path: '/', label: 'Dashboard', icon: Home },
    { path: '/requests', label: 'Requests', icon: FileText },
    { path: '/tenants', label: 'Tenants', icon: Users },
    { path: '/staff', label: 'Staff', icon: UserCog },
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center space-x-3">
              <Building className="h-8 w-8 text-primary-600" />
              <h1 className="text-2xl font-bold text-gray-900">
                Apartment Maintenance System
              </h1>
            </div>
          </div>
        </div>
      </header>

      {/* Navigation */}
      <nav className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex space-x-8">
            {navItems.map(({ path, label, icon: Icon }) => (
              <Link
                key={path}
                to={path}
                className={`flex items-center space-x-2 py-4 px-2 border-b-2 transition-colors ${
                  isActive(path)
                    ? 'border-primary-600 text-primary-600'
                    : 'border-transparent text-gray-600 hover:text-gray-900 hover:border-gray-300'
                }`}
              >
                <Icon className="h-5 w-5" />
                <span className="font-medium">{label}</span>
              </Link>
            ))}
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Outlet />
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <p className="text-center text-gray-600 text-sm">
            PA55: Applied Database Technologies - Fall 2025
          </p>
          <p className="text-center text-gray-500 text-xs mt-1">
            AI Tool Acknowledgment: Portions developed using GitHub Copilot (GPT-4), November 7, 2025
          </p>
        </div>
      </footer>
    </div>
  );
}
