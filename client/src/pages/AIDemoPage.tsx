import React from 'react';
import { Navigation } from '@/components/Navigation';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Camera, Brain, CheckCircle } from 'lucide-react';

export default function AIDemoPage() {
  return (
    <div className="min-h-screen bg-gray-50">
      <Navigation />
      <main className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">AI Photo Analysis Demo</h1>
        
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <Brain className="w-6 h-6 mr-2" />
              AI-Powered Analysis
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-gray-600">
              Upload photos and get AI compliance assessments with automated scoring.
            </p>
          </CardContent>
        </Card>
      </main>
    </div>
  );
}