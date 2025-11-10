import { useState, useEffect } from 'react';
import { Users, Mail, Phone, Home } from 'lucide-react';
import { tenantsAPI } from '../services';

export default function TenantsList() {
  const [tenants, setTenants] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadTenants();
  }, []);

  const loadTenants = async () => {
    try {
      const response = await tenantsAPI.getAll();
      setTenants(response.data);
    } catch (error) {
      console.error('Error loading tenants:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Tenants</h1>
        <p className="text-gray-600 mt-1">Manage tenant information</p>
      </div>

      <div className="card">
        {loading ? (
          <div className="text-center py-12 text-gray-600">Loading tenants...</div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {tenants.map(tenant => (
              <div key={tenant.id} className="border border-gray-200 rounded-lg p-6 hover:shadow-lg transition-shadow">
                <div className="flex items-center space-x-3 mb-4">
                  <div className="bg-primary-100 p-3 rounded-full">
                    <Users className="h-6 w-6 text-primary-600" />
                  </div>
                  <h3 className="text-lg font-bold text-gray-900">{tenant.full_name}</h3>
                </div>
                <div className="space-y-2">
                  <div className="flex items-center space-x-2 text-sm text-gray-600">
                    <Mail className="h-4 w-4" />
                    <span>{tenant.email}</span>
                  </div>
                  {tenant.phone && (
                    <div className="flex items-center space-x-2 text-sm text-gray-600">
                      <Phone className="h-4 w-4" />
                      <span>{tenant.phone}</span>
                    </div>
                  )}
                  <div className="flex items-center space-x-2 text-sm text-gray-600">
                    <Home className="h-4 w-4" />
                    <span>Unit: {tenant.unit_id.slice(-8)}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
