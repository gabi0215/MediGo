import { Routes, Route, Navigate } from 'react-router-dom'
import { Box } from '@mui/material'
import Layout from './components/Layout'
import HomePage from './pages/HomePage'
import LoginPage from './pages/LoginPage'
import OrderPage from './pages/OrderPage'
import OrderListPage from './pages/OrderListPage'
import OrderDetailPage from './pages/OrderDetailPage'
import ProfilePage from './pages/ProfilePage'
import { useAuthStore } from './stores/authStore'

function App() {
  const { isAuthenticated } = useAuthStore()

  return (
    <Box sx={{ minHeight: '100vh', bgcolor: 'background.default' }}>
      <Routes>
        {/* Public routes */}
        <Route path="/login" element={<LoginPage />} />

        {/* Protected routes */}
        <Route element={<Layout />}>
          <Route
            path="/"
            element={
              isAuthenticated ? <HomePage /> : <Navigate to="/login" replace />
            }
          />
          <Route
            path="/order"
            element={
              isAuthenticated ? <OrderPage /> : <Navigate to="/login" replace />
            }
          />
          <Route
            path="/orders"
            element={
              isAuthenticated ? (
                <OrderListPage />
              ) : (
                <Navigate to="/login" replace />
              )
            }
          />
          <Route
            path="/orders/:orderId"
            element={
              isAuthenticated ? (
                <OrderDetailPage />
              ) : (
                <Navigate to="/login" replace />
              )
            }
          />
          <Route
            path="/profile"
            element={
              isAuthenticated ? (
                <ProfilePage />
              ) : (
                <Navigate to="/login" replace />
              )
            }
          />
        </Route>

        {/* 404 */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Box>
  )
}

export default App

