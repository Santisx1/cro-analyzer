import React from 'react';
import './DashboardLayout.css';

interface DashboardLayoutProps {
  children: React.ReactNode;
  onLogout: () => void;
}

export default function DashboardLayout({ children, onLogout }: DashboardLayoutProps) {
  const userEmail = typeof window !== 'undefined' ? localStorage.getItem('userEmail') : '';

  return (
    <div className="dashboard-layout">
      <header className="dashboard-header-nav">
        <div className="header-logo">
          <h2>🎯 CRO Analyzer</h2>
        </div>
        <div className="header-user">
          <span>{userEmail}</span>
          <button className="btn-logout" onClick={onLogout}>
            Sair
          </button>
        </div>
      </header>
      <main className="dashboard-main">{children}</main>
    </div>
  );
}
