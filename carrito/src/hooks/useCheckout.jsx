import { useState } from 'react'

export function useCheckout({ cart, mpInstance, sandboxMode, sendToBackend }) {
  const [message, setMessage] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  const checkout = async () => {
    if (!cart.length) return setMessage('El carrito está vacío')
    setIsLoading(true)
    setMessage('Generando el pago...')

    try {
      const data = await sendToBackend(cart)
      const preferenceId = data?.preference_id
      const initPoint = sandboxMode ? data?.sandbox_init_point : data?.init_point

      if (!preferenceId && !initPoint) throw new Error('No se pudo iniciar el pago.')
      if (sandboxMode && initPoint) return (window.location.href = initPoint)
      if (mpInstance && preferenceId) {
        mpInstance.checkout({ preference: { id: preferenceId }, autoOpen: true })
        setMessage('Redirigiendo a Mercado Pago...')
        return
      }
      if (initPoint) return (window.location.href = initPoint)
      throw new Error('No se pudo iniciar el pago.')
    } catch (err) {
      setMessage(err instanceof Error ? err.message : 'Error al iniciar pago')
    } finally {
      setIsLoading(false)
    }
  }

  return { checkout, message, isLoading }
}
