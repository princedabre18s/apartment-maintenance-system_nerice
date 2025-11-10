import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { BarChart, Bar, PieChart, Pie, LineChart, Line, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { FileText, CheckCircle, Clock, AlertTriangle, TrendingUp, Users } from 'lucide-react';
import { metricsAPI } from '../services';

const COLORS = ['#0ea5e9', '#8b5cf6', '#f59e0b', '#10b981', '#ef4444'];

export default function Dashboard() {
  const [metrics, setMetrics] = useState(null);
  const [statusData, setStatusData] = useState([]);
  const [priorityData, setPriorityData] = useState([]);
  const [timeData, setTimeData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      const [metricsRes, statusRes, priorityRes, timeRes] = await Promise.all([
        metricsAPI.getOverview(),
        metricsAPI.getRequestsByStatus(),
        metricsAPI.getRequestsByPriority(),
        metricsAPI.getRequestsOverTime(30)
      ]);

      setMetrics(metricsRes.data);
      setStatusData(statusRes.data);
      setPriorityData(priorityRes.data);
      setTimeData(timeRes.data);
    } catch (error) {
      console.error('Error loading dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-gray-600">Loading dashboard...</div>
      </div>
    );
  }

  const kpiCards = [
    {
      title: 'Total Open Requests',
      value: metrics?.total_open_requests || 0,
      icon: FileText,
      color: 'blue',
      bgColor: 'bg-blue-50',
      iconColor: 'text-blue-600'
    },
    {
      title: 'Total Closed Requests',
      value: metrics?.total_closed_requests || 0,
      icon: CheckCircle,
      color: 'green',
      bgColor: 'bg-green-50',
      iconColor: 'text-green-600'
    },
    {
      title: 'Avg Resolution Time',
      value: `${metrics?.average_resolution_time || 0}h`,
      icon: Clock,
      color: 'purple',
      bgColor: 'bg-purple-50',
      iconColor: 'text-purple-600'
    },
    {
      title: 'SLA Breaches',
      value: metrics?.sla_breach_count || 0,
      icon: AlertTriangle,
      color: 'red',
      bgColor: 'bg-red-50',
      iconColor: 'text-red-600'
    },
    {
      title: 'Completion Rate',
      value: `${metrics?.completion_rate || 0}%`,
      icon: TrendingUp,
      color: 'indigo',
      bgColor: 'bg-indigo-50',
      iconColor: 'text-indigo-600'
    },
    {
      title: 'Total Requests',
      value: metrics?.total_requests || 0,
      icon: Users,
      color: 'gray',
      bgColor: 'bg-gray-50',
      iconColor: 'text-gray-600'
    }
  ];

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
          <p className="text-gray-600 mt-1">Maintenance request analytics and insights</p>
        </div>
        <Link to="/requests/new" className="btn-primary">
          + New Request
        </Link>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {kpiCards.map((card, index) => (
          <div key={index} className={`card ${card.bgColor} border-l-4 border-${card.color}-500`}>
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">{card.title}</p>
                <p className="text-3xl font-bold text-gray-900 mt-2">{card.value}</p>
              </div>
              <card.icon className={`h-12 w-12 ${card.iconColor}`} />
            </div>
          </div>
        ))}
      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Requests by Status */}
        <div className="card">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Requests by Status</h2>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={statusData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ status, count }) => `${status}: ${count}`}
                outerRadius={100}
                fill="#8884d8"
                dataKey="count"
              >
                {statusData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Requests by Priority */}
        <div className="card">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Requests by Priority</h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={priorityData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="priority" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="count" fill="#0ea5e9" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Requests Over Time */}
      <div className="card">
        <h2 className="text-xl font-bold text-gray-900 mb-4">Requests Over Time (Last 30 Days)</h2>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={timeData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey="count" stroke="#8b5cf6" strokeWidth={2} />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* Top Issue Types */}
      <div className="card">
        <h2 className="text-xl font-bold text-gray-900 mb-4">Top Issue Types</h2>
        <div className="space-y-4">
          {metrics?.top_issue_types?.map((issue, index) => (
            <div key={index} className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <span className="text-2xl font-bold text-gray-400">#{index + 1}</span>
                <span className="text-gray-900 font-medium">{issue.issue_type}</span>
              </div>
              <span className="text-gray-600 bg-gray-100 px-3 py-1 rounded-full text-sm font-medium">
                {issue.count} requests
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
