import { useEffect, useState } from 'react'

const STORAGE_KEY = 'music-cart-v1'
const ITEM_PRICE = 15

export function useCart() {
  const [cart, setCart] = useState(() => {
    if (typeof window === 'undefined') return []
    try {
      return JSON.parse(window.localStorage.getItem(STORAGE_KEY) || '[]')
    } catch {
      return []
    }
  })

  useEffect(() => {
    if (typeof window !== 'undefined') window.localStorage.setItem(STORAGE_KEY, JSON.stringify(cart))
  }, [cart])

  const addToCart = song =>
    setCart(prev => {
      const existing = prev.find(item => item.id === song.id)
      return existing
        ? prev.map(item => (item.id === song.id ? { ...item, quantity: item.quantity + 1 } : item))
        : [...prev, { ...song, quantity: 1 }]
    })

  const removeFromCart = songId => setCart(prev => prev.filter(item => item.id !== songId))

  const updateQuantity = (songId, delta) =>
    setCart(prev =>
      prev.flatMap(item => {
        if (item.id !== songId) return [item]
        const nextQuantity = item.quantity + delta
        return nextQuantity > 0 ? [{ ...item, quantity: nextQuantity }] : []
      }),
    )

  return {
    cart,
    total: cart.reduce((sum, item) => sum + item.quantity * ITEM_PRICE, 0),
    totalItems: cart.reduce((sum, item) => sum + item.quantity, 0),
    addToCart,
    removeFromCart,
    updateQuantity,
  }
}
