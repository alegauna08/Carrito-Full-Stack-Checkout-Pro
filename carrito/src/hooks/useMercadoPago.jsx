import { useEffect, useState } from 'react'

export function useMercadoPago(publicKey) {
  const [mpInstance, setMpInstance] = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    if (typeof window === 'undefined' || !publicKey) return

    const init = () => {
      try {
        setMpInstance(new window.MercadoPago(publicKey, { locale: 'es-AR' }))
      } catch {
        setError('No se pudo inicializar Mercado Pago.')
      }
    }

    if (window.MercadoPago) return init()

    const script = document.createElement('script')
    script.src = 'https://sdk.mercadopago.com/js/v2'
    script.defer = true
    script.onload = init
    script.onerror = () => setError('No se pudo cargar el SDK de Mercado Pago.')
    document.body.appendChild(script)

    return () => script.remove()
  }, [publicKey])

  return { mpInstance, error }
}
