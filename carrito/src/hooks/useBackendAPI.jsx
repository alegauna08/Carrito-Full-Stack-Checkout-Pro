import { useState } from 'react'

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export default function useBackendAPI() {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const sendToBackend = async cart => {
    setLoading(true)
    setError(null)

    try {
      const response = await fetch(`${API_BASE}/carrito/pago`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ items: cart.map(item => ({ song_id: item.id, quantity: item.quantity })) }),
      })

      const data = await response.json().catch(() => ({}))

      if (!response.ok) throw new Error(data.detail || data.message || 'No se pudo procesar el pedido')

      return data
    } catch (err) {
      const message = err instanceof Error ? err.message : 'No se pudo procesar el pedido'
      setError(message)
      throw new Error(message)
    } finally {
      setLoading(false)
    }
  }

  return { sendToBackend, loading, error }
}