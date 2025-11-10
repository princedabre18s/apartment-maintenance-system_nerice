import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import RequestList from './pages/RequestList';
import RequestDetails from './pages/RequestDetails';
import CreateRequest from './pages/CreateRequest';
import TenantsList from './pages/TenantsList';
import StaffList from './pages/StaffList';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Dashboard />} />
          <Route path="requests" element={<RequestList />} />
          <Route path="requests/:id" element={<RequestDetails />} />
          <Route path="requests/new" element={<CreateRequest />} />
          <Route path="tenants" element={<TenantsList />} />
          <Route path="staff" element={<StaffList />} />
        </Route>
      </Routes>
    </Router>
  );
}

export default App;
