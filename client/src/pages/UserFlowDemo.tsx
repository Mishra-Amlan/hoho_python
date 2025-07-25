import React from 'react';
import { Navigation } from '@/components/Navigation';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Users, ArrowRight } from 'lucide-react';

export default function UserFlowDemo() {
  return (
    <div className="min-h-screen bg-gray-50">
      <Navigation />
      <main className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">User Flow Demo</h1>
        
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <Users className="w-6 h-6 mr-2" />
              Interactive Workflow
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-gray-600">
              Experience the complete audit workflow from different user perspectives.
            </p>
          </CardContent>
        </Card>
      </main>
    </div>
  );
}