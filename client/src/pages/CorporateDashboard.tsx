import React from 'react';
import { Navigation } from '@/components/Navigation';
import { AnalyticsDashboard } from '@/components/AnalyticsDashboard';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Building, TrendingUp, Download, Filter } from 'lucide-react';
import { Button } from '@/components/ui/button';

export default function CorporateDashboard() {
  return (
    <div className="min-h-screen bg-gray-50">
      <Navigation role="corporate" />
      <main className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">Corporate Dashboard</h1>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <Card>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Total Properties</p>
                  <p className="text-2xl font-bold text-gray-900">24</p>
                </div>
                <Building className="h-8 w-8 text-blue-600" />
              </div>
            </CardContent>
          </Card>
          
          <Card>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Average Score</p>
                  <p className="text-2xl font-bold text-gray-900">87%</p>
                </div>
                <TrendingUp className="h-8 w-8 text-green-600" />
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-6 flex justify-center">
              <Button>
                <Download className="w-4 h-4 mr-2" />
                Export Reports
              </Button>
            </CardContent>
          </Card>
        </div>

        <AnalyticsDashboard audits={[]} properties={[]} />
      </main>
    </div>
  );
}