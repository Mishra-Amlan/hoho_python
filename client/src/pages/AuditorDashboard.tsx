import React, { useState } from 'react';
import { Navigation } from '@/components/Navigation';
import { AuditChecklistModal } from '@/components/AuditChecklistModal';
import { PhotoUploadModal } from '@/components/PhotoUploadModal';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { 
  Camera, 
  CheckSquare, 
  Clock, 
  MapPin, 
  AlertCircle,
  Upload,
  Save
} from 'lucide-react';

export default function AuditorDashboard() {
  const [showChecklistModal, setShowChecklistModal] = useState(false);
  const [showPhotoModal, setShowPhotoModal] = useState(false);

  const currentAudit = {
    id: 'AUD-2024-007',
    property: 'Grand Hotel Downtown',
    address: '123 Main Street, Downtown',
    checkInTime: '09:00 AM',
    estimatedDuration: '4 hours',
    status: 'In Progress',
    completedItems: 45,
    totalItems: 78,
    photosUploaded: 23
  };

  const auditSections = [
    { name: 'Lobby & Reception', items: 12, completed: 12, status: 'completed' },
    { name: 'Guest Rooms', items: 25, completed: 18, status: 'in-progress' },
    { name: 'Dining Areas', items: 15, completed: 15, status: 'completed' },
    { name: 'Facilities & Amenities', items: 18, completed: 0, status: 'pending' },
    { name: 'Exterior & Grounds', items: 8, completed: 0, status: 'pending' }
  ];

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed': return 'bg-green-100 text-green-800';
      case 'in-progress': return 'bg-blue-100 text-blue-800';
      case 'pending': return 'bg-gray-100 text-gray-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed': return <CheckSquare className="w-4 h-4 text-green-600" />;
      case 'in-progress': return <Clock className="w-4 h-4 text-blue-600" />;
      case 'pending': return <AlertCircle className="w-4 h-4 text-gray-600" />;
      default: return <Clock className="w-4 h-4 text-gray-600" />;
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Navigation role="auditor" />
      
      <main className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Auditor Dashboard
          </h1>
          <p className="text-gray-600">
            Conduct on-site audits, take photos, and complete checklists
          </p>
        </div>

        {/* Current Audit Info */}
        <Card className="mb-8 border-l-4 border-l-blue-500">
          <CardHeader>
            <CardTitle className="flex items-center justify-between">
              <span>Current Audit: {currentAudit.id}</span>
              <Badge className="bg-blue-100 text-blue-800">
                {currentAudit.status}
              </Badge>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              <div className="flex items-center space-x-2">
                <MapPin className="w-4 h-4 text-gray-600" />
                <div>
                  <p className="font-medium">{currentAudit.property}</p>
                  <p className="text-sm text-gray-600">{currentAudit.address}</p>
                </div>
              </div>
              <div className="flex items-center space-x-2">
                <Clock className="w-4 h-4 text-gray-600" />
                <div>
                  <p className="font-medium">Started: {currentAudit.checkInTime}</p>
                  <p className="text-sm text-gray-600">Est. {currentAudit.estimatedDuration}</p>
                </div>
              </div>
              <div className="flex items-center space-x-2">
                <CheckSquare className="w-4 h-4 text-gray-600" />
                <div>
                  <p className="font-medium">{currentAudit.completedItems}/{currentAudit.totalItems} Items</p>
                  <p className="text-sm text-gray-600">
                    {Math.round((currentAudit.completedItems / currentAudit.totalItems) * 100)}% Complete
                  </p>
                </div>
              </div>
              <div className="flex items-center space-x-2">
                <Camera className="w-4 h-4 text-gray-600" />
                <div>
                  <p className="font-medium">{currentAudit.photosUploaded} Photos</p>
                  <p className="text-sm text-gray-600">Uploaded</p>
                </div>
              </div>
            </div>

            <div className="mt-6 flex flex-wrap gap-4">
              <Button 
                onClick={() => setShowChecklistModal(true)}
                className="bg-blue-600 hover:bg-blue-700"
              >
                <CheckSquare className="w-4 h-4 mr-2" />
                Open Checklist
              </Button>
              <Button 
                variant="outline"
                onClick={() => setShowPhotoModal(true)}
              >
                <Camera className="w-4 h-4 mr-2" />
                Take Photos
              </Button>
              <Button variant="outline">
                <Upload className="w-4 h-4 mr-2" />
                Upload Files
              </Button>
              <Button variant="outline">
                <Save className="w-4 h-4 mr-2" />
                Save Progress
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* Audit Sections */}
        <Card>
          <CardHeader>
            <CardTitle>Audit Sections</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {auditSections.map((section, index) => (
                <div key={index} className="flex items-center justify-between p-4 border rounded-lg hover:bg-gray-50">
                  <div className="flex items-center space-x-3">
                    {getStatusIcon(section.status)}
                    <div>
                      <h3 className="font-medium">{section.name}</h3>
                      <p className="text-sm text-gray-600">
                        {section.completed}/{section.items} items completed
                      </p>
                    </div>
                  </div>
                  <div className="flex items-center space-x-3">
                    <Badge className={getStatusColor(section.status)}>
                      {section.status.charAt(0).toUpperCase() + section.status.slice(1).replace('-', ' ')}
                    </Badge>
                    <Button 
                      size="sm" 
                      variant="outline"
                      onClick={() => setShowChecklistModal(true)}
                    >
                      {section.status === 'completed' ? 'Review' : 'Continue'}
                    </Button>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </main>

      {/* Modals */}
      <AuditChecklistModal 
        isOpen={showChecklistModal}
        onOpenChange={setShowChecklistModal}
        auditId={1}
        propertyName="Grand Hotel Downtown"
      />
      <PhotoUploadModal 
        isOpen={showPhotoModal}
        onOpenChange={setShowPhotoModal}
        auditId={1}
        propertyName="Grand Hotel Downtown"
      />
    </div>
  );
}