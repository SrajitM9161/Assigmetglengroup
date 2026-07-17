export const formatTime = (iso: string) => new Intl.DateTimeFormat(undefined, { hour: '2-digit', minute: '2-digit' }).format(new Date(iso))
export const formatDate = (iso: string) => new Intl.DateTimeFormat(undefined, { month: 'short', day: 'numeric', year: 'numeric' }).format(new Date(iso))
export const formatSlot = (start: string, end: string) => `${formatDate(start)} · ${formatTime(start)}–${formatTime(end)}`

export function mondayOf(date: Date) {
  const result = new Date(date); const weekday = result.getDay() || 7
  result.setDate(result.getDate() - weekday + 1); result.setHours(0, 0, 0, 0); return result
}
export function addDays(date: Date, days: number) { const result = new Date(date); result.setDate(result.getDate() + days); return result }
export function isSameDay(first: Date, second: Date) { return first.toDateString() === second.toDateString() }
export function monthDays(anchor: Date) {
  const first = new Date(anchor.getFullYear(), anchor.getMonth(), 1)
  const offset = (first.getDay() + 6) % 7
  return Array.from({ length: 42 }, (_, index) => addDays(first, index - offset))
}
