import type { Assignment, Employee, Job } from '../types/domain'

const baseUrl = import.meta.env.VITE_API_BASE_URL ?? 'http://127.0.0.1:3000/api'

interface ApiEnvelope<T> { success: true; message?: string; data: T }
interface ApiErrorEnvelope { success: false; error: { code: string; message: string } }

export class ApiError extends Error {
  constructor(public readonly code: string, message: string) { super(message) }
}

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const response = await fetch(`${baseUrl}${path}`, {
    ...options,
    headers: { 'Content-Type': 'application/json', 'X-Role': 'scheduler', ...options.headers },
  })
  const payload = await response.json().catch(() => null) as ApiEnvelope<T> | ApiErrorEnvelope | null
  if (!response.ok || !payload || !payload.success) {
    const error = payload && 'error' in payload ? payload.error : undefined
    throw new ApiError(error?.code ?? 'NETWORK_ERROR', error?.message ?? 'Unable to reach the scheduling service.')
  }
  return payload.data
}

export const schedulingApi = {
  employees: () => request<Employee[]>('/employees'),
  jobs: () => request<Job[]>('/jobs'),
  schedule: () => request<Assignment[]>('/schedule'),
  assign: (employeeId: string, jobId: string) => request<Assignment>('/assign', {
    method: 'POST', body: JSON.stringify({ employeeId, jobId }),
  }),
  removeAssignment: (assignmentId: string) => request<Record<string, never>>(`/assign/${assignmentId}`, { method: 'DELETE' }),
}
