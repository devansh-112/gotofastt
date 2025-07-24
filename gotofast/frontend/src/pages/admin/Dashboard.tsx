import React from 'react';
import AdminLayout from '../../components/admin/AdminLayout';

const Dashboard: React.FC = () => {
  return (
    <AdminLayout>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white rounded-xl shadow p-6 flex flex-col items-center">
          <div className="text-4xl font-bold text-brand-blue mb-2">42</div>
          <div className="text-lg text-gray-700">Total Orders</div>
        </div>
        <div className="bg-white rounded-xl shadow p-6 flex flex-col items-center">
          <div className="text-4xl font-bold text-brand-red mb-2">7</div>
          <div className="text-lg text-gray-700">Pending Orders</div>
        </div>
        <div className="bg-white rounded-xl shadow p-6 flex flex-col items-center">
          <div className="text-4xl font-bold text-green-600 mb-2">35</div>
          <div className="text-lg text-gray-700">Delivered</div>
        </div>
      </div>
    </AdminLayout>
  );
};

export default Dashboard; 