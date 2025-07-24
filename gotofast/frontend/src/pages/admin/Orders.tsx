import React from 'react';
import AdminLayout from '../../components/admin/AdminLayout';

const Orders: React.FC = () => {
  return (
    <AdminLayout>
      <div className="bg-white rounded-xl shadow p-6">
        <h2 className="text-2xl font-bold text-brand-blue mb-4">Orders</h2>
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gradient-to-r from-brand-blue/80 to-brand-red/80 text-white">
            <tr>
              <th className="px-4 py-2 text-left">Order ID</th>
              <th className="px-4 py-2 text-left">Customer</th>
              <th className="px-4 py-2 text-left">Status</th>
              <th className="px-4 py-2 text-left">Amount</th>
              <th className="px-4 py-2 text-left">Date</th>
            </tr>
          </thead>
          <tbody>
            <tr className="hover:bg-gray-50">
              <td className="px-4 py-2">#1001</td>
              <td className="px-4 py-2">John Doe</td>
              <td className="px-4 py-2"><span className="px-2 py-1 rounded bg-yellow-100 text-yellow-800">Pending</span></td>
              <td className="px-4 py-2">₹1200</td>
              <td className="px-4 py-2">2024-06-01</td>
            </tr>
            <tr className="hover:bg-gray-50">
              <td className="px-4 py-2">#1002</td>
              <td className="px-4 py-2">Jane Smith</td>
              <td className="px-4 py-2"><span className="px-2 py-1 rounded bg-green-100 text-green-800">Delivered</span></td>
              <td className="px-4 py-2">₹800</td>
              <td className="px-4 py-2">2024-06-02</td>
            </tr>
          </tbody>
        </table>
      </div>
    </AdminLayout>
  );
};

export default Orders; 