import React, { useState, useEffect } from 'react'
import { fetchSongs, useSongs } from './clase9-10/backend/cancion'

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export async function fetchSongs() {
  const res = await fetch(`${API_BASE}/songs`)
  if (!res.ok) throw new Error('Error fetching songs')
  return res.json()
}

export function useSongs() {
  const [songs, setSongs] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    let cancelled = false
    setLoading(true)
    fetchSongs()
      .then(data => {
        if (!cancelled) {
          setSongs(data)
          setLoading(false)
        }
      })
      .catch(err => {
        if (!cancelled) {
          setError(err)
          setLoading(false)
        }
      })

    return () => {
      cancelled = true
    }
  }, [])

  async function refetch() {
    setLoading(true)
    setError(null)
    try {
      const data = await fetchSongs()
      setSongs(data)
    } catch (err) {
      setError(err)
    } finally {
      setLoading(false)
    }
  }

  return { songs, loading, error, refetch }
}

export default function Cancion() {
  const { songs, loading, error } = useSongs()

  if (loading) return <div>Cargando...</div>
  if (error) return <div>Error cargando canciones</div>

  return (
    <div>
      <h3>Lista de canciones</h3>
      <ul>
        {songs.map(s => (
          <li key={s.id}>{s.title} — {s.artist}</li>
        ))}
      </ul>
    </div>
  )
}
