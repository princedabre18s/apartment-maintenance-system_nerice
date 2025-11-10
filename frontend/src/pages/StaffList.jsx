import { useState, useEffect } from 'react';
import { UserCog, Mail, Phone, Briefcase, CheckCircle, XCircle } from 'lucide-react';
import { staffAPI } from '../services';

export default function StaffList() {
  const [staff, setStaff] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadStaff();
  }, []);

  const loadStaff = async () => {
    try {
      const response = await staffAPI.getAll();
      setStaff(response.data);
    } catch (error) {
      console.error('Error loading staff:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Staff Members</h1>
        <p className="text-gray-600 mt-1">Manage maintenance staff and assignments</p>
      </div>

      <div className="card">
        {loading ? (
          <div className="text-center py-12 text-gray-600">Loading staff...</div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {staff.map(member => (
              <div key={member.id} className="border border-gray-200 rounded-lg p-6 hover:shadow-lg transition-shadow">
                <div className="flex items-start justify-between mb-4">
                  <div className="flex items-center space-x-3">
                    <div className="bg-purple-100 p-3 rounded-full">
                      <UserCog className="h-6 w-6 text-purple-600" />
                    </div>
                    <div>
                      <h3 className="text-lg font-bold text-gray-900">{member.full_name}</h3>
                      <p className="text-sm text-gray-600">{member.role}</p>
                    </div>
                  </div>
                  {member.active ? (
                    <CheckCircle className="h-5 w-5 text-green-500" />
                  ) : (
                    <XCircle className="h-5 w-5 text-red-500" />
                  )}
                </div>
                <div className="space-y-2">
                  <div className="flex items-center space-x-2 text-sm text-gray-600">
                    <Mail className="h-4 w-4" />
                    <span>{member.email}</span>
                  </div>
                  {member.phone && (
                    <div className="flex items-center space-x-2 text-sm text-gray-600">
                      <Phone className="h-4 w-4" />
                      <span>{member.phone}</span>
                    </div>
                  )}
                  {member.specialties && member.specialties.length > 0 && (
                    <div className="mt-3">
                      <p className="text-xs text-gray-500 mb-1">Specialties:</p>
                      <div className="flex flex-wrap gap-1">
                        {member.specialties.map((specialty, idx) => (
                          <span
                            key={idx}
                            className="px-2 py-1 bg-blue-100 text-blue-700 text-xs rounded-full"
                          >
                            {specialty}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
