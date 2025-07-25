import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { apiRequest } from '@/lib/queryClient';

// Audit Items hooks
export function useAuditItems(auditId: number) {
  return useQuery({
    queryKey: ['audit-items', auditId],
    queryFn: () => apiRequest(`/audits/${auditId}/items`),
    enabled: !!auditId,
  });
}

export function useUpdateAuditItem() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (data: { id: number; score: number; comments: string; status: string }) =>
      apiRequest(`/audit-items/${data.id}`, {
        method: 'PATCH',
        body: JSON.stringify(data),
      }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['audit-items'] });
    },
  });
}

// Properties hooks
export function useProperties() {
  return useQuery({
    queryKey: ['properties'],
    queryFn: () => apiRequest('/properties/'),
  });
}

// Audits hooks
export function useAudits() {
  return useQuery({
    queryKey: ['audits'],
    queryFn: () => apiRequest('/audits/'),
  });
}

// Hotel Groups hooks
export function useHotelGroups() {
  return useQuery({
    queryKey: ['hotel-groups'],
    queryFn: () => apiRequest('/hotel-groups/'),
  });
}