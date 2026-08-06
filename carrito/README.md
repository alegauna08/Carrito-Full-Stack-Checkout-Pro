# Frontend de carrito de música

Esta interfaz permite navegar un catálogo musical, agregar canciones al carrito y completar un flujo de compra simple desde el navegador.

## ¿Cómo funciona la app?

- Muestra un catálogo de canciones cargado desde el backend.
- Permite buscar canciones por título, artista o álbum.
- Cada canción puede agregarse al carrito con una cantidad específica.
- El usuario puede ver el resumen del carrito, modificar cantidades o eliminar elementos.
- Al hacer checkout, la app envía el carrito al backend y obtiene el resultado del proceso de compra.

## Flujo de uso

1. El backend debe estar corriendo en `http://localhost:8000`.
2. Al abrir la app en `http://localhost:5173`, se solicita el catálogo al backend.
3. El usuario explora las canciones, las busca y las agrega al carrito.
4. Desde el modal o vista del carrito puede ajustar cantidades o quitar productos.
5. Al confirmar la compra, la aplicación envía la selección al backend y muestra el resultado del checkout.

## Requisitos

- Bun instalado
- El backend corriendo en `http://localhost:8000`

## Ejecutar con Bun

```bash
cd carrito
bun install
bun run dev
```

La app quedará disponible en `http://localhost:5173`.

## Variables de entorno

Si necesitas cambiar la URL del backend, puedes definir:

```bash
export VITE_API_URL=http://localhost:8000
```

Si querés probar el flujo de pago real con Mercado Pago, también puedes definir:

```bash
export VITE_MERCADO_PAGO_PUBLIC_KEY=tu_clave_publica
export VITE_MERCADO_PAGO_SANDBOX=true
```

## Estructura principal

- `src/components`: componentes visuales como el catálogo y el carrito.
- `src/hooks`: lógica para consumir el backend y manejar el estado del carrito.
- `src/App.jsx`: punto principal de la aplicación.
