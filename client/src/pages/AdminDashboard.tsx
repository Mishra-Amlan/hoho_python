import React, { useState } from 'react';
import { Navigation } from '@/components/Navigation';
import { AnalyticsDashboard } from '@/components/AnalyticsDashboard';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { 
  Calendar, 
  Users, 
  Building, 
  CheckCircle, 
  AlertTriangle, 
  Clock,
  Plus,
  Filter
} from 'lucide-react';

export default function AdminDashboard() {
  const [activeTab, setActiveTab] = useState('overview');

  const stats = [
    { title: 'Total Properties', value: '24', icon: Building, trend: '+2 this month' },
    { title: 'Active Audits', value: '8', icon: Clock, trend: '3 in progress' },
    { title: 'Completed Audits', value: '156', icon: CheckCircle, trend: '+12 this week' },
    { title: 'Active Auditors', value: '15', icon: Users, trend: '2 on leave' },
  ];

  const recentAudits = [
    { id: '001', property: 'Grand Hotel Downtown', status: 'In Progress', auditor: 'John Smith', date: '2024-07-25' },
    { id: '002', property: 'Seaside Resort', status: 'Completed', auditor: 'Jane Doe', date: '2024-07-24' },
    { id: '003', property: 'Mountain Lodge', status: 'Scheduled', auditor: 'Mike Johnson', date: '2024-07-26' },
    { id: '004', property: 'City Center Inn', status: 'Under Review', auditor: 'Sarah Wilson', date: '2024-07-23' },
  ];

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'Completed': return 'bg-green-100 text-green-800';
      case 'In Progress': return 'bg-blue-100 text-blue-800';
      case 'Scheduled': return 'bg-yellow-100 text-yellow-800';
      case 'Under Review': return 'bg-purple-100 text-purple-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Navigation role="admin" />
      
      <main className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Admin Dashboard
          </h1>
          <p className="text-gray-600">
            Manage audit schedules, coordinate teams, and oversee audit processes
          </p>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {stats.map((stat, index) => (
            <Card key={index}>
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600">{stat.title}</p>
                    <p className="text-2xl font-bold text-gray-900">{stat.value}</p>
                    <p className="text-xs text-gray-500 mt-1">{stat.trend}</p>
                  </div>
                  <stat.icon className="h-8 w-8 text-blue-600" />
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Action Buttons */}
        <div className="flex flex-wrap gap-4 mb-8">
          <Button className="bg-blue-600 hover:bg-blue-700">
            <Plus className="w-4 h-4 mr-2" />
            Schedule New Audit
          </Button>
          <Button variant="outline">
            <Calendar className="w-4 h-4 mr-2" />
            View Calendar
          </Button>
          <Button variant="outline">
            <Users className="w-4 h-4 mr-2" />
            Manage Auditors
          </Button>
          <Button variant="outline">
            <Filter className="w-4 h-4 mr-2" />
            Filter Results
          </Button>
        </div>

        {/* Recent Audits Table */}
        <Card className="mb-8">
          <CardHeader>
            <CardTitle>Recent Audits</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b">
                    <th className="text-left py-3 px-4 font-medium text-gray-600">Audit ID</th>
                    <th className="text-left py-3 px-4 font-medium text-gray-600">Property</th>
                    <th className="text-left py-3 px-4 font-medium text-gray-600">Status</th>
                    <th className="text-left py-3 px-4 font-medium text-gray-600">Auditor</th>
                    <th className="text-left py-3 px-4 font-medium text-gray-600">Date</th>
                  </tr>
                </thead>
                <tbody>
                  {recentAudits.map((audit) => (
                    <tr key={audit.id} className="border-b hover:bg-gray-50">
                      <td className="py-3 px-4 font-mono text-sm">{audit.id}</td>
                      <td className="py-3 px-4">{audit.property}</td>
                      <td className="py-3 px-4">
                        <Badge className={getStatusColor(audit.status)}>
                          {audit.status}
                        </Badge>
                      </td>
                      <td className="py-3 px-4">{audit.auditor}</td>
                      <td className="py-3 px-4">{audit.date}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </CardContent>
        </Card>

        {/* Analytics Dashboard */}
        <AnalyticsDashboard />
      </main>
    </div>
  );
}