import { useCallback, useEffect, useState } from 'react'
import { ApiError, schedulingApi } from './api/client'
import { AssignmentPanel } from './components/AssignmentPanel'
import { ScheduleView } from './components/ScheduleView'
import { Toast } from './components/Toast'
import type { Assignment, Employee, Job } from './types/domain'
import './styles.css'

const userMessage = (error: unknown) => {
  const code = error instanceof ApiError ? error.code : 'NETWORK_ERROR'
  return ({ EMPLOYEE_UNAVAILABLE: 'This employee is unavailable.', ROLE_MISMATCH: 'This employee does not have the required role.', DUPLICATE_ASSIGNMENT: 'This employee is already assigned to this job.', SCHEDULE_OVERLAP: 'This employee already has a shift during this time.' } as Record<string, string>)[code] ?? 'Something went wrong. Please try again.'
}

export default function App() {
  const [employees, setEmployees] = useState<Employee[]>([])
  const [jobs, setJobs] = useState<Job[]>([])
  const [schedule, setSchedule] = useState<Assignment[]>([])
  const [loading, setLoading] = useState(true)
  const [assigning, setAssigning] = useState(false)
  const [deleting, setDeleting] = useState<Assignment | null>(null)
  const [toast, setToast] = useState<{ message: string; variant: 'success' | 'error' } | null>(null)

  const load = useCallback(async () => {
    setLoading(true)
    try {
      const [employeeData, jobData, scheduleData] = await Promise.all([
        schedulingApi.employees(), schedulingApi.jobs(), schedulingApi.schedule(),
      ])
      setEmployees(employeeData)
      setJobs(jobData)
      setSchedule(scheduleData)
    } catch (error) {
      setToast({ message: userMessage(error), variant: 'error' })
    } finally {
      setLoading(false)
    }
  }, [])
  useEffect(() => { void load() }, [load])
  const assign = async (employeeId: string, jobId: string) => {
    setAssigning(true)
    try {
      const assignment = await schedulingApi.assign(employeeId, jobId)
      setSchedule(current => [...current, assignment])
      setToast({ message: 'Assignment created successfully.', variant: 'success' })
    } catch (error) {
      setToast({ message: userMessage(error), variant: 'error' })
    } finally { setAssigning(false) }
  }
  const remove = async () => {
    if (!deleting) return
    try {
      await schedulingApi.removeAssignment(deleting.id)
      setSchedule(current => current.filter(assignment => assignment.id !== deleting.id))
      setToast({ message: 'Assignment deleted successfully.', variant: 'success' })
    } catch (error) {
      setToast({ message: userMessage(error), variant: 'error' })
    } finally { setDeleting(null) }
  }
  return <><header className="topbar"><div><span className="eyebrow">Operations</span><h1>Mini Scheduling System</h1></div><span className="user">Scheduler</span></header><main className="shell">{loading ? <p className="empty">Loading scheduling data…</p> : <><AssignmentPanel employees={employees} jobs={jobs} busy={assigning} onAssign={assign} /><ScheduleView assignments={schedule} busy={false} onDelete={setDeleting} /></>}</main>{deleting && <div className="modal"><div className="dialog"><h2>Remove assignment?</h2><p>Remove <b>{deleting.employeeName}</b> from <b>{deleting.jobName}</b>?</p><div><button className="button" onClick={() => setDeleting(null)}>Cancel</button><button className="button button--danger" onClick={() => void remove()}>Delete assignment</button></div></div></div>}{toast && <Toast {...toast} onClose={() => setToast(null)} />}</>
}
