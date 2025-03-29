import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { Box } from '@mui/material';
import { useAuth } from './context/AuthContext';

// 布局组件
import Layout from './components/Layout';

// 页面组件
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import PatientList from './pages/PatientList';
import PatientDetail from './pages/PatientDetail';
import PatientAnalysis from './pages/PatientAnalysis';
import TreatmentGuidelines from './pages/TreatmentGuidelines';
import LiteratureSearch from './pages/LiteratureSearch';
import Profile from './pages/Profile';
import NotFound from './pages/NotFound';

// 受保护的路由组件
const ProtectedRoute = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();
  
  if (loading) {
    return <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>加载中...</Box>;
  }
  
  if (!isAuthenticated) {
    return <Navigate to="/login" />;
  }
  
  return children;
};

function App() {
  return (
    <Routes>
      {/* 公共路由 */}
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      
      {/* 受保护的路由 */}
      <Route path="/" element={
        <ProtectedRoute>
          <Layout />
        </ProtectedRoute>
      }>
        <Route index element={<Dashboard />} />
        <Route path="patients" element={<PatientList />} />
        <Route path="patients/:id" element={<PatientDetail />} />
        <Route path="analysis" element={<PatientAnalysis />} />
        <Route path="guidelines" element={<TreatmentGuidelines />} />
        <Route path="literature" element={<LiteratureSearch />} />
        <Route path="profile" element={<Profile />} />
      </Route>
      
      {/* 404页面 */}
      <Route path="*" element={<NotFound />} />
    </Routes>
  );
}

export default App;
