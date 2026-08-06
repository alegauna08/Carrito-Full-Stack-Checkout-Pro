import React from 'react'

export default function MercadoButton({ href, label = 'Pagar con Mercado Pago', disabled = false, loading = false, onClick }) {
  if (href) {
    return (
      <a className="summary-button" href={href} target="_blank" rel="noreferrer">
        {label}
      </a>
    )
  }

  return (
    <button onClick={onClick} disabled={disabled || loading}>
      {loading ? 'Procesando...' : label}
    </button>
  )
}
