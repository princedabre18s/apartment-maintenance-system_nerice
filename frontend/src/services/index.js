import apiClient from './api';

// Metrics API
export const metricsAPI = {
  getOverview: () => apiClient.get('/metrics/overview'),
  getRequestsByStatus: () => apiClient.get('/metrics/requests-by-status'),
  getRequestsByPriority: () => apiClient.get('/metrics/requests-by-priority'),
  getRequestsOverTime: (days = 30) => apiClient.get(`/metrics/requests-over-time?days=${days}`),
  getBuildingPerformance: () => apiClient.get('/metrics/building-performance'),
  getStaffPerformance: () => apiClient.get('/metrics/staff-performance'),
};

// Requests API
export const requestsAPI = {
  getAll: (params = {}) => {
    // Filter out empty string values
    const filteredParams = Object.fromEntries(
      Object.entries(params).filter(([_, value]) => value !== '' && value !== null && value !== undefined)
    );
    return apiClient.get('/requests/', { params: filteredParams });
  },
  getById: (id) => apiClient.get(`/requests/${id}`),
  create: (data) => apiClient.post('/requests/', data),
  update: (id, data) => apiClient.put(`/requests/${id}`, data),
  delete: (id) => apiClient.delete(`/requests/${id}`),
  assign: (id, staffData) => apiClient.post(`/requests/${id}/assign`, staffData),
  addNote: (id, noteData) => apiClient.post(`/requests/${id}/notes`, noteData),
  complete: (id, staffId) => apiClient.post(`/requests/${id}/complete?staff_id=${staffId}`),
};

// Buildings API
export const buildingsAPI = {
  getAll: (params = {}) => apiClient.get('/buildings/', { params }),
  getById: (id) => apiClient.get(`/buildings/${id}`),
  create: (data) => apiClient.post('/buildings/', data),
  update: (id, data) => apiClient.put(`/buildings/${id}`, data),
  delete: (id) => apiClient.delete(`/buildings/${id}`),
};

// Units API
export const unitsAPI = {
  getAll: (params = {}) => apiClient.get('/units/', { params }),
  getById: (id) => apiClient.get(`/units/${id}`),
  create: (data) => apiClient.post('/units/', data),
  update: (id, data) => apiClient.put(`/units/${id}`, data),
  delete: (id) => apiClient.delete(`/units/${id}`),
};

// Tenants API
export const tenantsAPI = {
  getAll: (params = {}) => apiClient.get('/tenants/', { params }),
  getById: (id) => apiClient.get(`/tenants/${id}`),
  create: (data) => apiClient.post('/tenants/', data),
  update: (id, data) => apiClient.put(`/tenants/${id}`, data),
  delete: (id) => apiClient.delete(`/tenants/${id}`),
};

// Staff API
export const staffAPI = {
  getAll: (params = {}) => apiClient.get('/staff/', { params }),
  getById: (id) => apiClient.get(`/staff/${id}`),
  create: (data) => apiClient.post('/staff/', data),
  update: (id, data) => apiClient.put(`/staff/${id}`, data),
  delete: (id) => apiClient.delete(`/staff/${id}`),
};
