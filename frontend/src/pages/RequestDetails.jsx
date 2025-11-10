import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, User, Building, Calendar, Clock, AlertCircle, X } from 'lucide-react';
import { requestsAPI, staffAPI } from '../services';

export default function RequestDetails() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [request, setRequest] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  // Modal states
  const [showStatusModal, setShowStatusModal] = useState(false);
  const [showAssignModal, setShowAssignModal] = useState(false);
  const [showNoteModal, setShowNoteModal] = useState(false);
  
  // Form states
  const [newStatus, setNewStatus] = useState('');
  const [resolutionNotes, setResolutionNotes] = useState('');
  const [selectedStaffId, setSelectedStaffId] = useState('');
  const [assignmentNotes, setAssignmentNotes] = useState('');
  const [noteBody, setNoteBody] = useState('');
  const [noteAuthorName, setNoteAuthorName] = useState('');
  const [noteAuthorType, setNoteAuthorType] = useState('staff');
  
  // Staff list
  const [staffList, setStaffList] = useState([]);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    loadRequest();
    loadStaff();
  }, [id]);

  const loadStaff = async () => {
    try {
      const response = await staffAPI.getAll({ active: true });
      setStaffList(response.data);
    } catch (error) {
      console.error('Error loading staff:', error);
    }
  };

  const loadRequest = async () => {
    try {
      setLoading(true);
      setError(null);
      console.log('Loading request with ID:', id);
      const response = await requestsAPI.getById(id);
      console.log('Request loaded:', response.data);
      setRequest(response.data);
    } catch (error) {
      console.error('Error loading request:', error);
      console.error('Error details:', error.response?.data);
      setError(error.response?.data?.detail || error.message || 'Failed to load request');
    } finally {
      setLoading(false);
    }
  };

  const handleUpdateStatus = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      const updateData = { status: newStatus };
      if (resolutionNotes.trim()) {
        updateData.resolution_notes = resolutionNotes;
      }
      await requestsAPI.update(id, updateData);
      setShowStatusModal(false);
      setNewStatus('');
      setResolutionNotes('');
      await loadRequest();
      alert('Status updated successfully!');
    } catch (error) {
      console.error('Error updating status:', error);
      alert('Failed to update status: ' + (error.response?.data?.detail || error.message));
    } finally {
      setSubmitting(false);
    }
  };

  const handleAssignStaff = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      const assignData = {
        staff_id: selectedStaffId,
        notes: assignmentNotes.trim() || undefined
      };
      await requestsAPI.assign(id, assignData);
      setShowAssignModal(false);
      setSelectedStaffId('');
      setAssignmentNotes('');
      await loadRequest();
      alert('Staff assigned successfully!');
    } catch (error) {
      console.error('Error assigning staff:', error);
      alert('Failed to assign staff: ' + (error.response?.data?.detail || error.message));
    } finally {
      setSubmitting(false);
    }
  };

  const handleAddNote = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      const noteData = {
        author_type: noteAuthorType,
        author_id: noteAuthorType === 'staff' ? selectedStaffId : request.tenant_id,
        author_name: noteAuthorName,
        body: noteBody
      };
      await requestsAPI.addNote(id, noteData);
      setShowNoteModal(false);
      setNoteBody('');
      setNoteAuthorName('');
      setSelectedStaffId('');
      await loadRequest();
      alert('Note added successfully!');
    } catch (error) {
      console.error('Error adding note:', error);
      alert('Failed to add note: ' + (error.response?.data?.detail || error.message));
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-gray-600">Loading request details...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-12">
        <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg inline-block">
          <p className="text-red-800">
            <strong>Error:</strong> {error}
          </p>
        </div>
        <div className="space-x-4">
          <button onClick={loadRequest} className="btn-secondary">
            Try Again
          </button>
          <button onClick={() => navigate('/requests')} className="btn-primary">
            Back to Requests
          </button>
        </div>
      </div>
    );
  }

  if (!request) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-600">Request not found</p>
        <button onClick={() => navigate('/requests')} className="btn-primary mt-4">
          Back to Requests
        </button>
      </div>
    );
  }

  const getStatusColor = (status) => {
    const colors = {
      'OPEN': 'bg-blue-100 text-blue-800',
      'IN_PROGRESS': 'bg-yellow-100 text-yellow-800',
      'PENDING': 'bg-purple-100 text-purple-800',
      'COMPLETED': 'bg-green-100 text-green-800',
      'CLOSED': 'bg-gray-100 text-gray-800'
    };
    return colors[status] || 'bg-gray-100 text-gray-800';
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <button
            onClick={() => navigate('/requests')}
            className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
          >
            <ArrowLeft className="h-6 w-6 text-gray-600" />
          </button>
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Request Details</h1>
            <p className="text-gray-600 mt-1">{request.external_id || `ID: ${(request.id || request._id).slice(-8)}`}</p>
          </div>
        </div>
        <span className={`px-4 py-2 text-sm font-semibold rounded-full ${getStatusColor(request.status)}`}>
          {request.status.replace('_', ' ')}
        </span>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Main Details */}
        <div className="lg:col-span-2 space-y-6">
          {/* Basic Information */}
          <div className="card">
            <h2 className="text-xl font-bold text-gray-900 mb-4">Request Information</h2>
            <dl className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <dt className="text-sm font-medium text-gray-600">Issue Type</dt>
                <dd className="mt-1 text-sm text-gray-900">{request.issue_type}</dd>
              </div>
              <div>
                <dt className="text-sm font-medium text-gray-600">Priority</dt>
                <dd className="mt-1 text-sm font-semibold text-gray-900">{request.priority}</dd>
              </div>
              <div>
                <dt className="text-sm font-medium text-gray-600">Created</dt>
                <dd className="mt-1 text-sm text-gray-900">
                  {new Date(request.created_at).toLocaleString()}
                </dd>
              </div>
              <div>
                <dt className="text-sm font-medium text-gray-600">Last Updated</dt>
                <dd className="mt-1 text-sm text-gray-900">
                  {new Date(request.updated_at).toLocaleString()}
                </dd>
              </div>
              <div className="md:col-span-2">
                <dt className="text-sm font-medium text-gray-600">Description</dt>
                <dd className="mt-1 text-sm text-gray-900">{request.description}</dd>
              </div>
              {request.resolution_notes && (
                <div className="md:col-span-2">
                  <dt className="text-sm font-medium text-gray-600">Resolution Notes</dt>
                  <dd className="mt-1 text-sm text-gray-900">{request.resolution_notes}</dd>
                </div>
              )}
            </dl>
          </div>

          {/* Assignments */}
          {request.assignments && request.assignments.length > 0 && (
            <div className="card">
              <h2 className="text-xl font-bold text-gray-900 mb-4">Staff Assignments</h2>
              <div className="space-y-4">
                {request.assignments.map((assignment, index) => (
                  <div key={index} className="border border-gray-200 rounded-lg p-4">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="font-medium text-gray-900">Staff ID: {assignment.staff_id.slice(-8)}</p>
                        <p className="text-sm text-gray-600 mt-1">
                          Assigned: {new Date(assignment.assigned_at).toLocaleString()}
                        </p>
                        {assignment.completed_at && (
                          <p className="text-sm text-green-600 mt-1">
                            Completed: {new Date(assignment.completed_at).toLocaleString()}
                          </p>
                        )}
                      </div>
                      {assignment.completed_at ? (
                        <span className="text-green-600 font-medium">Completed</span>
                      ) : (
                        <span className="text-yellow-600 font-medium">In Progress</span>
                      )}
                    </div>
                    {assignment.notes && (
                      <p className="text-sm text-gray-600 mt-2 italic">{assignment.notes}</p>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Notes */}
          {request.notes && request.notes.length > 0 && (
            <div className="card">
              <h2 className="text-xl font-bold text-gray-900 mb-4">Communication Notes</h2>
              <div className="space-y-4">
                {request.notes.map((note, index) => (
                  <div key={note.id || note._id || index} className="border-l-4 border-primary-500 pl-4 py-2">
                    <div className="flex items-center justify-between mb-2">
                      <span className="font-medium text-gray-900">{note.author_name}</span>
                      <span className="text-sm text-gray-500">
                        {new Date(note.created_at).toLocaleString()}
                      </span>
                    </div>
                    <p className="text-sm text-gray-700">{note.body}</p>
                    <span className="inline-block mt-1 text-xs text-gray-500 capitalize">
                      {note.author_type}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* SLA Information */}
          <div className="card bg-blue-50 border-l-4 border-blue-500">
            <div className="flex items-start space-x-3">
              <Clock className="h-6 w-6 text-blue-600 flex-shrink-0 mt-1" />
              <div>
                <h3 className="font-bold text-gray-900">SLA Target</h3>
                <p className="text-2xl font-bold text-blue-600 mt-1">
                  {request.target_sla_hours}h
                </p>
                <p className="text-sm text-gray-600 mt-1">Expected resolution time</p>
              </div>
            </div>
          </div>

          {/* Location */}
          {request.location_details && (
            <div className="card">
              <h3 className="font-bold text-gray-900 mb-3">Location Details</h3>
              <div className="space-y-2">
                {request.location_details.neighborhood && (
                  <div className="flex items-center space-x-2 text-sm">
                    <Building className="h-4 w-4 text-gray-500" />
                    <span className="text-gray-700">{request.location_details.neighborhood}</span>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Quick Actions */}
          <div className="card">
            <h3 className="font-bold text-gray-900 mb-3">Quick Actions</h3>
            <div className="space-y-2">
              <button 
                onClick={() => {
                  setNewStatus(request.status);
                  setShowStatusModal(true);
                }}
                className="w-full btn-primary text-left px-4 py-2"
              >
                Update Status
              </button>
              <button 
                onClick={() => setShowAssignModal(true)}
                className="w-full btn-secondary text-left px-4 py-2"
              >
                Assign Staff
              </button>
              <button 
                onClick={() => setShowNoteModal(true)}
                className="w-full btn-secondary text-left px-4 py-2"
              >
                Add Note
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Update Status Modal */}
      {showStatusModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg shadow-xl max-w-md w-full p-6">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-xl font-bold text-gray-900">Update Status</h3>
              <button 
                onClick={() => setShowStatusModal(false)}
                className="text-gray-400 hover:text-gray-600"
              >
                <X className="h-6 w-6" />
              </button>
            </div>
            <form onSubmit={handleUpdateStatus}>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    New Status *
                  </label>
                  <select
                    value={newStatus}
                    onChange={(e) => setNewStatus(e.target.value)}
                    className="input-field"
                    required
                  >
                    <option value="OPEN">Open</option>
                    <option value="IN_PROGRESS">In Progress</option>
                    <option value="PENDING">Pending</option>
                    <option value="COMPLETED">Completed</option>
                    <option value="CLOSED">Closed</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Resolution Notes (optional)
                  </label>
                  <textarea
                    value={resolutionNotes}
                    onChange={(e) => setResolutionNotes(e.target.value)}
                    className="input-field"
                    rows="4"
                    placeholder="Enter resolution details if completing or closing..."
                  />
                </div>
              </div>
              <div className="flex space-x-3 mt-6">
                <button
                  type="button"
                  onClick={() => setShowStatusModal(false)}
                  className="btn-secondary flex-1"
                  disabled={submitting}
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="btn-primary flex-1"
                  disabled={submitting}
                >
                  {submitting ? 'Updating...' : 'Update Status'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Assign Staff Modal */}
      {showAssignModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg shadow-xl max-w-md w-full p-6">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-xl font-bold text-gray-900">Assign Staff</h3>
              <button 
                onClick={() => setShowAssignModal(false)}
                className="text-gray-400 hover:text-gray-600"
              >
                <X className="h-6 w-6" />
              </button>
            </div>
            <form onSubmit={handleAssignStaff}>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Select Staff Member *
                  </label>
                  <select
                    value={selectedStaffId}
                    onChange={(e) => setSelectedStaffId(e.target.value)}
                    className="input-field"
                    required
                  >
                    <option value="">Choose staff...</option>
                    {staffList.map((staff) => (
                      <option key={staff._id || staff.id} value={staff._id || staff.id}>
                        {staff.full_name} - {staff.role}
                      </option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Assignment Notes (optional)
                  </label>
                  <textarea
                    value={assignmentNotes}
                    onChange={(e) => setAssignmentNotes(e.target.value)}
                    className="input-field"
                    rows="3"
                    placeholder="Add any special instructions..."
                  />
                </div>
              </div>
              <div className="flex space-x-3 mt-6">
                <button
                  type="button"
                  onClick={() => setShowAssignModal(false)}
                  className="btn-secondary flex-1"
                  disabled={submitting}
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="btn-primary flex-1"
                  disabled={submitting}
                >
                  {submitting ? 'Assigning...' : 'Assign Staff'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Add Note Modal */}
      {showNoteModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg shadow-xl max-w-md w-full p-6">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-xl font-bold text-gray-900">Add Note</h3>
              <button 
                onClick={() => setShowNoteModal(false)}
                className="text-gray-400 hover:text-gray-600"
              >
                <X className="h-6 w-6" />
              </button>
            </div>
            <form onSubmit={handleAddNote}>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Author Type *
                  </label>
                  <select
                    value={noteAuthorType}
                    onChange={(e) => setNoteAuthorType(e.target.value)}
                    className="input-field"
                    required
                  >
                    <option value="staff">Staff</option>
                    <option value="tenant">Tenant</option>
                  </select>
                </div>
                {noteAuthorType === 'staff' && (
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Staff Member *
                    </label>
                    <select
                      value={selectedStaffId}
                      onChange={(e) => setSelectedStaffId(e.target.value)}
                      className="input-field"
                      required
                    >
                      <option value="">Choose staff...</option>
                      {staffList.map((staff) => (
                        <option key={staff._id || staff.id} value={staff._id || staff.id}>
                          {staff.full_name}
                        </option>
                      ))}
                    </select>
                  </div>
                )}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Your Name *
                  </label>
                  <input
                    type="text"
                    value={noteAuthorName}
                    onChange={(e) => setNoteAuthorName(e.target.value)}
                    className="input-field"
                    placeholder="Enter your name"
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Note *
                  </label>
                  <textarea
                    value={noteBody}
                    onChange={(e) => setNoteBody(e.target.value)}
                    className="input-field"
                    rows="4"
                    placeholder="Enter your note or comment..."
                    required
                    maxLength="2000"
                  />
                  <p className="text-xs text-gray-500 mt-1">
                    {noteBody.length}/2000 characters
                  </p>
                </div>
              </div>
              <div className="flex space-x-3 mt-6">
                <button
                  type="button"
                  onClick={() => setShowNoteModal(false)}
                  className="btn-secondary flex-1"
                  disabled={submitting}
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="btn-primary flex-1"
                  disabled={submitting}
                >
                  {submitting ? 'Adding...' : 'Add Note'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
