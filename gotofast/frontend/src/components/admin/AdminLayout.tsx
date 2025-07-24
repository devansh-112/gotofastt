import React from 'react';

const AdminLayout: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <div className="min-h-screen flex bg-admin-bg">
    {/* Sidebar */}
    <aside className="w-64 bg-gradient-to-b from-brand-blue/90 to-brand-red/80 text-white flex flex-col">
      <div className="p-6 text-2xl font-bold tracking-wide">GotoFast Admin</div>
      <nav className="flex-1 px-4 space-y-2">
        <a href="/admin/dashboard" className="block py-2 px-3 rounded hover:bg-white/10">Dashboard</a>
        <a href="/admin/orders" className="block py-2 px-3 rounded hover:bg-white/10">Orders</a>
        <a href="/admin/partners" className="block py-2 px-3 rounded hover:bg-white/10">Partners</a>
        <a href="/admin/settings" className="block py-2 px-3 rounded hover:bg-white/10">Settings</a>
      </nav>
    </aside>
    {/* Main Content */}
    <main className="flex-1 p-8">
      <header className="mb-8">
        <h1 className="text-3xl font-extrabold text-brand-blue">Admin Dashboard</h1>
      </header>
      {children}
    </main>
  </div>
);

export default AdminLayout; 