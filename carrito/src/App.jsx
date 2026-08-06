import { useState } from 'react'
import './App.css'
import { CartModal } from './components/CartModal'
import { SongCatalog } from './components/SongCatalog'
import useBackendAPI from './hooks/useBackendAPI'
import { useCart } from './hooks/useCart'
import { useCheckout } from './hooks/useCheckout'
import { useMercadoPago } from './hooks/useMercadoPago'
import { useSongs } from './hooks/useSongs'

export default function App() {
  const { songs, loading, error } = useSongs()
  const { sendToBackend } = useBackendAPI()
  const { cart, total, totalItems, addToCart, removeFromCart, updateQuantity } = useCart()
  const [query, setQuery] = useState('')
  const [showCart, setShowCart] = useState(false)
  const publicKey = import.meta.env.VITE_MERCADO_PAGO_PUBLIC_KEY || ''
  const sandboxMode = import.meta.env.VITE_MERCADO_PAGO_SANDBOX === 'true'
  const { mpInstance, error: mpError } = useMercadoPago(publicKey)
  const { checkout, message, isLoading } = useCheckout({ cart, mpInstance, sandboxMode, sendToBackend })

  const filteredSongs = query
    ? songs.filter(song => `${song.title} ${song.artist} ${song.album}`.toLowerCase().includes(query.toLowerCase()))
    : songs

  if (loading) return <div className="status">Cargando canciones...</div>
  if (error) return <div className="status error">Error: {error.message}</div>

  return (
    <div className="app-shell">
      <header className="hero-card">
        <div>
          <p className="eyebrow">Fullstack · React + FastAPI</p>
          <h1>Carrito de discos de música</h1>
          <p>Explora canciones, agrégalas al carrito y confirma tu pedido.</p>
        </div>
        <button className="secondary-button" onClick={() => setShowCart(prev => !prev)}>
          {showCart ? 'Ocultar carrito' : 'Mostrar carrito'}
        </button>
      </header>

      <SongCatalog songs={filteredSongs} total={songs.length} query={query} onSearch={setQuery} onAdd={addToCart} />

      {showCart && (
        <CartModal
          cart={cart}
          total={total}
          totalItems={totalItems}
          message={mpError || message}
          isLoading={isLoading}
          onClose={() => setShowCart(false)}
          onRemove={removeFromCart}
          onQuantity={updateQuantity}
          onCheckout={checkout}
        />
      )}
    </div>
  )
}