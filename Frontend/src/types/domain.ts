export type Role = 'TCP' | 'LCT' | 'Supervisor'
export type AssignmentStatus = 'assigned' | 'pending'

export interface Employee {
  id: string
  name: string
  role: Role
  availability: boolean
}

export interface Job {
  id: string
  name: string
  startTime: string
  endTime: string
  requiredRole?: Role | null
}

export interface Assignment {
  id: string
  employeeId: string
  jobId: string
  employeeName: string
  role: Role
  jobName: string
  startTime: string
  endTime: string
  status: AssignmentStatus
}
