import { ApiClient } from "../client";

export interface WorkflowCreateRequest {
  user_id: string;
  request: string;
  metadata?: Record<string, unknown>;
}

export interface ExecutionContext {
  workflow_id: string;
  user_id: string;
  request: string;
  status: string;
  metadata: Record<string, unknown>;
}

export const WorkflowService = {
  async create(data: WorkflowCreateRequest): Promise<ExecutionContext> {
    return ApiClient.post<ExecutionContext>("/workflows", data);
  },
  
  async get(workflowId: string): Promise<ExecutionContext> {
    return ApiClient.get<ExecutionContext>(`/workflows/${workflowId}`);
  },

  async getGraph(workflowId: string): Promise<unknown> {
    return ApiClient.get<unknown>(`/workflows/${workflowId}/graph`);
  }
};
