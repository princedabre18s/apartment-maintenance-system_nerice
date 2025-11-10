import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft } from 'lucide-react';
import { requestsAPI, tenantsAPI, unitsAPI, buildingsAPI } from '../services';

export default function CreateRequest() {
  const navigate = useNavigate();
  const [buildings, setBuildings] = useState([]);
  const [units, setUnits] = useState([]);
  const [tenants, setTenants] = useState([]);
  const [loading, setLoading] = useState(false);
  
  const [formData, setFormData] = useState({
    tenant_id: '',
    unit_id: '',
    building_id: '',
    issue_type: 'Plumbing',
    priority: 'Medium',
    description: '',
    target_sla_hours: 72
  });

  // Show all units when building is selected (don't filter strictly)
  // This allows for more flexibility in case relationships aren't perfect
  const availableUnits = units;
  const availableTenants = tenants;

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [buildingsRes, unitsRes, tenantsRes] = await Promise.all([
        buildingsAPI.getAll(),
        unitsAPI.getAll(),
        tenantsAPI.getAll()
      ]);
      console.log('Loaded buildings:', buildingsRes.data);
      console.log('Loaded units:', unitsRes.data);
      console.log('Loaded tenants:', tenantsRes.data);
      setBuildings(buildingsRes.data);
      setUnits(unitsRes.data);
      setTenants(tenantsRes.data);
    } catch (error) {
      console.error('Error loading data:', error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      // Prepare data with proper format
      const requestData = {
        tenant_id: formData.tenant_id,
        unit_id: formData.unit_id,
        building_id: formData.building_id,
        issue_type: formData.issue_type,
        priority: formData.priority,
        description: formData.description,
        target_sla_hours: parseInt(formData.target_sla_hours),
        status: 'OPEN'
      };

      console.log('Form data:', formData);
      console.log('Submitting request:', requestData);
      console.log('Selected tenant ID:', formData.tenant_id);
      console.log('Selected unit ID:', formData.unit_id);
      console.log('Selected building ID:', formData.building_id);
      
      const response = await requestsAPI.create(requestData);
      console.log('Request created successfully:', response.data);
      navigate('/requests');
    } catch (error) {
      console.error('Error creating request:', error);
      console.error('Error response:', error.response?.data);
      alert(`Failed to create request: ${JSON.stringify(error.response?.data?.detail || error.message)}`);
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center space-x-4">
        <button
          onClick={() => navigate('/requests')}
          className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
        >
          <ArrowLeft className="h-6 w-6 text-gray-600" />
        </button>
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Create New Request</h1>
          <p className="text-gray-600 mt-1">Submit a new maintenance request</p>
        </div>
      </div>

      <form onSubmit={handleSubmit} className="card max-w-3xl">
        <div className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Building *
              </label>
              <select
                name="building_id"
                value={formData.building_id}
                onChange={handleChange}
                required
                className="input-field"
              >
                <option value="">Select Building</option>
                {buildings.map(building => (
                  <option key={building.id || building._id} value={building.id || building._id}>
                    {building.name}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Unit *
              </label>
              <select
                name="unit_id"
                value={formData.unit_id}
                onChange={handleChange}
                required
                className="input-field"
              >
                <option value="">Select Unit</option>
                {availableUnits.map(unit => (
                  <option key={unit.id || unit._id} value={unit.id || unit._id}>
                    Unit {unit.unit_number} {unit.floor ? `- Floor ${unit.floor}` : ''}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Tenant *
              </label>
              <select
                name="tenant_id"
                value={formData.tenant_id}
                onChange={handleChange}
                required
                className="input-field"
              >
                <option value="">Select Tenant</option>
                {availableTenants.map(tenant => (
                  <option key={tenant.id || tenant._id} value={tenant.id || tenant._id}>
                    {tenant.full_name} ({tenant.email})
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Issue Type *
              </label>
              <select
                name="issue_type"
                value={formData.issue_type}
                onChange={handleChange}
                required
                className="input-field"
              >
                <option value="Plumbing">Plumbing</option>
                <option value="Electrical">Electrical</option>
                <option value="HVAC">HVAC</option>
                <option value="Appliances">Appliances</option>
                <option value="Cleaning">Cleaning</option>
                <option value="Pest Control">Pest Control</option>
                <option value="Security">Security</option>
                <option value="Structural">Structural</option>
                <option value="Other">Other</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Priority *
              </label>
              <select
                name="priority"
                value={formData.priority}
                onChange={handleChange}
                required
                className="input-field"
              >
                <option value="Low">Low</option>
                <option value="Medium">Medium</option>
                <option value="High">High</option>
                <option value="Emergency">Emergency</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                SLA Target (hours) *
              </label>
              <input
                type="number"
                name="target_sla_hours"
                value={formData.target_sla_hours}
                onChange={handleChange}
                required
                min="1"
                className="input-field"
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Description *
            </label>
            <textarea
              name="description"
              value={formData.description}
              onChange={handleChange}
              required
              rows="4"
              className="input-field"
              placeholder="Describe the issue in detail..."
            />
          </div>

          <div className="flex space-x-4">
            <button
              type="submit"
              disabled={loading}
              className="btn-primary"
            >
              {loading ? 'Creating...' : 'Create Request'}
            </button>
            <button
              type="button"
              onClick={() => navigate('/requests')}
              className="btn-secondary"
            >
              Cancel
            </button>
          </div>
        </div>
      </form>
    </div>
  );
}
