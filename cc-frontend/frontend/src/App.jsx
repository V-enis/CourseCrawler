import { useState } from 'react'
import { Routes, Route, Link, Navigate } from "react-router-dom"
import { Toaster } from 'react-hot-toast';
import './css/App.css'
import Dashboard from './pages/Dashboard'
import DegreeList from './pages/DegreeList'
import DegreeDetail from './pages/DegreeDetail'
import LandingPage from './pages/LandingPage'
import Login from './pages/Login'
import Register from './pages/Register'
import Profile from './pages/Profile';
import AboutPage from './pages/AboutPage';
import NavBar from './components/Navbar'
import ProtectedRoute from './components/PrivateRoute'


function Logout() {
  localStorage.clear()
  return <Navigate to="/login/" />
}

function RegisterAndLogout() {
  localStorage.clear()
  return <Register />
}

function App() {


  return (
    <>
      <NavBar />
      <Toaster
        position="top-center"
        reverseOrder={false}
        toastOptions={{
          style: {
            background: '#333',
            color: '#fff',
          },
        }}
      />
      <main className="main-content">
        <Routes>
          <Route path="/" element={<LandingPage />} />

          <Route path="/login" element={<Login />} />
          <Route path="/logout" element={<Logout />} />
          <Route path="/register" element={<RegisterAndLogout />} />

          <Route path="/degrees" element={<DegreeList />} />
          <Route path="/degrees/:slug" element={<DegreeDetail />} />
          <Route path="/about" element={<AboutPage />} />

          <Route path="/profile" element={
            <ProtectedRoute>
              <Profile />
            </ProtectedRoute>
          }
          />

          <Route path="/dashboard" element={
            <ProtectedRoute>
              <Dashboard />
            </ProtectedRoute>
          } />
        </Routes>
      </main>
    </>
  )
}

export default App
