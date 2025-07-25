import { z } from "zod";

// TypeScript interfaces for MS SQL Server data models
export interface User {
  id: number;
  username: string;
  password: string;
  role: string; // 'admin', 'auditor', 'reviewer', 'corporate', 'hotelgm'
  name: string;
  email: string;
  createdAt?: Date;
}

export interface HotelGroup {
  id: number;
  name: string; // e.g., "Taj Hotels", "Marriott", "Hilton"
  description?: string;
  defaultSopFiles?: string; // JSON array of default SOP file paths
  createdAt?: Date;
}

export interface Property {
  id: number;
  name: string;
  location: string;
  hotelGroupId: number;
  managerName?: string;
  managerEmail?: string;
  status: string; // 'active', 'inactive'
  overallScore?: number;
  lastAuditDate?: Date;
  createdAt?: Date;
}

export interface Audit {
  id: number;
  propertyId: number;
  auditorId?: number;
  reviewerId?: number;
  hotelGroupId: number;
  sop?: string; // Hotel group SOP snapshot at audit time
  sopFiles?: string; // JSON array of SOP file paths for this audit
  status: string; // 'scheduled', 'in_progress', 'submitted', 'reviewed', 'completed', 'approved'
  overallScore?: number;
  cleanlinessScore?: number;
  brandingScore?: number;
  operationalScore?: number;
  complianceZone?: string; // 'green', 'amber', 'red'
  findings?: string; // JSON as text
  actionPlan?: string; // JSON as text
  submittedAt?: Date;
  reviewedAt?: Date;
  createdAt?: Date;
}

export interface AuditItem {
  id: number;
  auditId: number;
  category: string;
  item: string;
  score?: number;
  comments?: string;
  aiAnalysis?: string; // AI-generated analysis and insights
  photos?: string; // JSON as text
  status: string; // 'pending', 'completed'
}

// Zod schemas for validation
export const insertUserSchema = z.object({
  username: z.string().min(1),
  password: z.string().min(1),
  role: z.string().min(1),
  name: z.string().min(1),
  email: z.string().email(),
});

export const insertHotelGroupSchema = z.object({
  name: z.string().min(1),
  description: z.string().optional(),
  defaultSopFiles: z.string().optional(),
});

export const insertPropertySchema = z.object({
  name: z.string().min(1),
  location: z.string().min(1),
  hotelGroupId: z.number(),
  managerName: z.string().optional(),
  managerEmail: z.string().email().optional(),
  status: z.string().default('active'),
});

export const insertAuditSchema = z.object({
  propertyId: z.number(),
  auditorId: z.number().optional(),
  reviewerId: z.number().optional(),
  hotelGroupId: z.number(),
  sop: z.string().optional(),
  sopFiles: z.string().optional(),
});

export const insertAuditItemSchema = z.object({
  auditId: z.number(),
  category: z.string().min(1),
  item: z.string().min(1),
  score: z.number().optional(),
  comments: z.string().optional(),
  photos: z.string().optional(),
});

// Type exports
export type InsertUser = z.infer<typeof insertUserSchema>;
export type InsertHotelGroup = z.infer<typeof insertHotelGroupSchema>;
export type InsertProperty = z.infer<typeof insertPropertySchema>;
export type InsertAudit = z.infer<typeof insertAuditSchema>;
export type InsertAuditItem = z.infer<typeof insertAuditItemSchema>;

export type UserRole = 'admin' | 'auditor' | 'reviewer' | 'corporate' | 'hotelgm';
export type ComplianceZone = 'green' | 'amber' | 'red';
export type AuditStatus = 'scheduled' | 'in_progress' | 'submitted' | 'reviewed' | 'completed' | 'approved' | 'needs_revision';
