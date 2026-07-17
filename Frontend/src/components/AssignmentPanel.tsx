import { useMemo, useState } from 'react'
import type { Employee, Job, Role } from '../types/domain'
import { formatSlot } from '../utils/date'

interface Props {
  employees: Employee[]; jobs: Job[]; busy: boolean
  onAssign: (employeeId: string, jobId: string) => void
}

export function AssignmentPanel({ employees, jobs, busy, onAssign }: Props) {
  const [search, setSearch] = useState(''); const [role, setRole] = useState<'All' | Role>('All')
  const [availability, setAvailability] = useState<'All' | 'Available' | 'Unavailable'>('All')
  const [employeeId, setEmployeeId] = useState(''); const [jobId, setJobId] = useState('')
  const selectedJob = jobs.find(job => job.id === jobId)
  const selectedEmployee = employees.find(employee => employee.id === employeeId)
  const filtered = useMemo(() => employees.filter(employee =>
    employee.name.toLowerCase().includes(search.toLowerCase()) &&
    (role === 'All' || employee.role === role) &&
    (availability === 'All' || employee.availability === (availability === 'Available'))
  ), [employees, search, role, availability])
  const mismatch = Boolean(selectedEmployee && selectedJob?.requiredRole && selectedEmployee.role !== selectedJob.requiredRole)
  const disabled = busy || !selectedEmployee || !selectedJob || !selectedEmployee.availability || mismatch
  const helper = !selectedEmployee ? 'Select an employee.' : !selectedJob ? 'Select a job.' : !selectedEmployee.availability ? 'This employee is unavailable.' : mismatch ? `This job requires a ${selectedJob?.requiredRole}.` : null

  return <section className="assignment-grid">
    <div className="panel"><div className="panel__heading"><h2>Employee selection</h2><span>{filtered.length} people</span></div>
      <input className="input" value={search} onChange={event => setSearch(event.target.value)} placeholder="Search employee name" aria-label="Search employees" />
      <div className="filter-row"><select value={role} onChange={event => setRole(event.target.value as 'All' | Role)}><option>All</option><option>TCP</option><option>LCT</option><option>Supervisor</option></select><select value={availability} onChange={event => setAvailability(event.target.value as 'All' | 'Available' | 'Unavailable')}><option>All</option><option>Available</option><option>Unavailable</option></select></div>
      <div className="employee-list">{filtered.map(employee => <button key={employee.id} className={`employee ${employee.id === employeeId ? 'employee--selected' : ''} ${!employee.availability ? 'employee--unavailable' : ''}`} onClick={() => employee.availability && setEmployeeId(employee.id)}>
        <span className="avatar">{employee.name.split(' ').map(part => part[0]).join('').slice(0, 2)}</span><span><strong>{employee.name}</strong><small>{employee.role}</small></span><em>{employee.availability ? 'Available' : 'Unavailable'}</em>
      </button>)}</div>
    </div>
    <div className="panel"><div className="panel__heading"><h2>Job selection</h2></div>
      <select className="input" value={jobId} onChange={event => setJobId(event.target.value)} aria-label="Select job"><option value="">Select a job</option>{jobs.map(job => <option key={job.id} value={job.id}>{job.name} — {formatSlot(job.startTime, job.endTime)}</option>)}</select>
      {selectedJob ? <div className="job-detail"><h3>{selectedJob.name}</h3><p>{formatSlot(selectedJob.startTime, selectedJob.endTime)}</p><p>Required role: <b>{selectedJob.requiredRole ?? 'Any role'}</b></p></div> : <div className="job-detail job-detail--empty">Select a job to view its shift details.</div>}
      <p className="helper">{helper ?? 'This selection is ready to assign.'}</p>
      <button className="primary" disabled={disabled} onClick={() => selectedEmployee && selectedJob && onAssign(selectedEmployee.id, selectedJob.id)}>{busy ? 'Assigning…' : 'Assign employee'}</button>
    </div>
  </section>
}
