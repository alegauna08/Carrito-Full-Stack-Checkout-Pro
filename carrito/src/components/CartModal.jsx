export function CartModal({ cart, total, totalItems, message, isLoading, onClose, onRemove, onQuantity, onCheckout }) {
  return (
    <div className="cart-modal-backdrop" onClick={onClose}>
      <div className="cart-modal" onClick={event => event.stopPropagation()}>
        <div className="cart-modal-header">
          <div>
            <h2>Carrito</h2>
            <span className="pill">{totalItems} unidades</span>
          </div>
          <button className="ghost modal-close" onClick={onClose}>Cerrar</button>
        </div>

        {message && <p className="message">{message}</p>}

        {cart.length === 0 ? (
          <p className="empty">El carrito está vacío.</p>
        ) : (
          <div className="cart-items">
            {cart.map(item => (
              <div key={item.id} className="cart-item">
                <div>
                  <strong>{item.title}</strong>
                  <p>{item.artist}</p>
                </div>
                <div className="cart-actions">
                  <button onClick={() => onQuantity(item.id, -1)}>-</button>
                  <span>{item.quantity}</span>
                  <button onClick={() => onQuantity(item.id, 1)}>+</button>
                </div>
                <button className="ghost" onClick={() => onRemove(item.id)}>Quitar</button>
              </div>
            ))}
          </div>
        )}

        <div className="summary">
          <div>
            <span>Total</span>
            <strong>${total.toFixed(2)}</strong>
          </div>
          <button onClick={onCheckout} disabled={cart.length === 0 || isLoading}>
            {isLoading ? 'Procesando...' : 'Comprar'}
          </button>
        </div>
      </div>
    </div>
  )
}
