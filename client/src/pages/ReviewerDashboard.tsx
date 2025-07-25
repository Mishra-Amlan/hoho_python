import React from 'react';
import { Navigation } from '@/components/Navigation';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { CheckCircle, AlertTriangle, Eye, FileText } from 'lucide-react';

export default function ReviewerDashboard() {
  const pendingReviews = [
    { id: 'AUD-001', property: 'Grand Hotel', auditor: 'John Smith', score: 85, status: 'pending' },
    { id: 'AUD-002', property: 'Seaside Resort', auditor: 'Jane Doe', score: 92, status: 'pending' },
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      <Navigation role="reviewer" />
      <main className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">Reviewer Dashboard</h1>
        
        <Card>
          <CardHeader>
            <CardTitle>Pending Reviews</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {pendingReviews.map((audit) => (
                <div key={audit.id} className="flex items-center justify-between p-4 border rounded-lg">
                  <div>
                    <h3 className="font-medium">{audit.property}</h3>
                    <p className="text-sm text-gray-600">Auditor: {audit.auditor}</p>
                    <p className="text-sm text-gray-600">Score: {audit.score}%</p>
                  </div>
                  <div className="flex space-x-2">
                    <Button size="sm">
                      <Eye className="w-4 h-4 mr-2" />
                      Review
                    </Button>
                    <Button size="sm" variant="outline">
                      <FileText className="w-4 h-4 mr-2" />
                      Report
                    </Button>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </main>
    </div>
  );
}