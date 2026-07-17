import { useEffect } from 'react'

export function Toast({ message, variant, onClose }: { message: string; variant: 'success' | 'error'; onClose: () => void }) {
  useEffect(() => { const timer = window.setTimeout(onClose, 4000); return () => window.clearTimeout(timer) }, [onClose])
  return <div className={`toast toast--${variant}`} role="status"><span>{variant === 'success' ? '✓' : '!'}</span>{message}<button onClick={onClose} aria-label="Dismiss notification">×</button></div>
}
