import { useMemo, useState } from 'react'
import type { Assignment, Role } from '../types/domain'
import { addDays, formatSlot, formatTime, isSameDay, mondayOf, monthDays } from '../utils/date'

interface Props { assignments: Assignment[]; busy: boolean; onDelete: (assignment: Assignment) => void }
export function ScheduleView({ assignments, busy, onDelete }: Props) {
  const [view, setView] = useState<'table' | 'calendar'>('table'); const [calendarView, setCalendarView] = useState<'week' | 'month'>('week')
  const [date, setDate] = useState(new Date()); const [role, setRole] = useState<'All' | Role>('All')
  const visible = useMemo(() => assignments.filter(assignment => role === 'All' || assignment.role === role), [assignments, role])
  return <section className="panel schedule"><header className="schedule__header"><div><h2>Assigned schedule</h2><span>{visible.length} assignment{visible.length === 1 ? '' : 's'}</span></div><div className="tabs"><button className={view === 'table' ? 'active' : ''} onClick={() => setView('table')}>Table</button><button className={view === 'calendar' ? 'active' : ''} onClick={() => setView('calendar')}>Calendar</button></div></header>
    <div className="toolbar"><select value={role} onChange={event => setRole(event.target.value as 'All' | Role)}><option>All</option><option>TCP</option><option>LCT</option><option>Supervisor</option></select>{view === 'calendar' && <><div className="tabs"><button className={calendarView === 'week' ? 'active' : ''} onClick={() => setCalendarView('week')}>Week</button><button className={calendarView === 'month' ? 'active' : ''} onClick={() => setCalendarView('month')}>Month</button></div><button className="button button--quiet" onClick={() => setDate(new Date())}>Today</button><button className="button button--quiet" onClick={() => setDate(addDays(date, calendarView === 'week' ? -7 : -30))}>←</button><strong>{calendarView === 'week' ? `Week of ${mondayOf(date).toLocaleDateString(undefined, { month: 'short', day: 'numeric' })}` : date.toLocaleDateString(undefined, { month: 'long', year: 'numeric' })}</strong><button className="button button--quiet" onClick={() => setDate(addDays(date, calendarView === 'week' ? 7 : 30))}>→</button></>}</div>
    {busy ? <p className="empty">Loading schedule…</p> : view === 'table' ? <ScheduleTable assignments={visible} onDelete={onDelete} /> : <Calendar assignments={visible} anchor={date} mode={calendarView} onDelete={onDelete} />}
  </section>
}

function ScheduleTable({ assignments, onDelete }: { assignments: Assignment[]; onDelete: (assignment: Assignment) => void }) {
  if (!assignments.length) return <p className="empty">No assignments yet. Create the first assignment above.</p>
  return <div className="table-wrap"><table><thead><tr><th>Employee</th><th>Role</th><th>Job</th><th>Time slot</th><th>Status</th><th /></tr></thead><tbody>{assignments.map(assignment => <tr key={assignment.id}><td><b>{assignment.employeeName}</b></td><td><span className="badge">{assignment.role}</span></td><td>{assignment.jobName}</td><td>{formatSlot(assignment.startTime, assignment.endTime)}</td><td><span className={`status status--${assignment.status}`}>{assignment.status}</span></td><td><button className="delete" onClick={() => onDelete(assignment)}>Delete</button></td></tr>)}</tbody></table></div>
}

function Calendar({ assignments, anchor, mode, onDelete }: { assignments: Assignment[]; anchor: Date; mode: 'week' | 'month'; onDelete: (assignment: Assignment) => void }) {
  const days = mode === 'week' ? Array.from({ length: 7 }, (_, index) => addDays(mondayOf(anchor), index)) : monthDays(anchor)
  return <div className={`calendar calendar--${mode}`}>{days.map((day, index) => { const dayAssignments = assignments.filter(assignment => isSameDay(new Date(assignment.startTime), day)); return <div className={`calendar__day ${mode === 'month' && day.getMonth() !== anchor.getMonth() ? 'calendar__day--muted' : ''}`} key={`${day.toISOString()}-${index}`}><div className="calendar__date">{day.toLocaleDateString(undefined, { weekday: mode === 'week' ? 'short' : undefined, day: 'numeric' })}</div>{dayAssignments.map(assignment => <button className={`event event--${assignment.role.toLowerCase()}`} key={assignment.id} title={`${assignment.employeeName}: ${assignment.jobName}`} onClick={() => onDelete(assignment)}><b>{assignment.jobName}</b><span>{assignment.employeeName} · {formatTime(assignment.startTime)}</span></button>)}</div>})}</div>
}
