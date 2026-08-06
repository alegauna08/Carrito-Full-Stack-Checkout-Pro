# Backend de canciones

Este backend está pensado para soportar la tienda musical de la app. Expone una API REST con FastAPI que permite administrar canciones, recibir el carrito desde el frontend y preparar el flujo de pago.

## ¿Qué hace esta parte?

- Sirve el catálogo de canciones mediante endpoints REST.
- Permite listar, crear, actualizar y eliminar canciones.
- Recibe los productos seleccionados por el usuario en el carrito y devuelve un resumen con subtotales y totales.
- Integra Mercado Pago para generar una preferencia de pago cuando hay credenciales configuradas.
- Si no hay credenciales válidas, el sistema entra en modo demo para no romper la experiencia de prueba.

## Flujo de funcionamiento

1. El frontend consulta las canciones en `GET /songs`.
2. El usuario agrega canciones al carrito desde la interfaz.
3. El backend recibe ese carrito en `POST /carrito` y calcula:
   - cantidad total de items
   - subtotal por canción
   - precio total final
4. Si las variables de Mercado Pago están configuradas, prepara una preferencia de pago. Si no, devuelve una respuesta de demostración.

## Requisitos

- Python 3.10 o superior
- Entorno virtual activado

## Ejecutar localmente

```bash
cd backend
source ../env/bin/activate
uvicorn api:app --reload --port 8000
```

La API quedará disponible en `http://localhost:8000`.

## Endpoints principales

- `GET /songs`: devuelve todas las canciones.
- `GET /songs/{song_id}`: obtiene una canción por su ID.
- `POST /songs`: crea una nueva canción.
- `PUT /songs/{song_id}`: actualiza una canción existente.
- `DELETE /songs/{song_id}`: elimina una canción.
- `POST /carrito`: recibe el carrito y devuelve el resumen de compra.

## Variables de entorno

Puedes configurar estas variables antes de probar el flujo de pago real:

- `MERCADO_PAGO_ACCESS_TOKEN`
- `MERCADO_PAGO_ACCESS_TOKEN_SANDBOX`
- `MERCADO_PAGO_PUBLIC_KEY`
- `MERCADO_PAGO_PUBLIC_KEY_SANDBOX`
- `MERCADO_PAGO_USE_SANDBOX`
- `MERCADO_PAGO_SUCCESS_URL`
- `MERCADO_PAGO_FAILURE_URL`
- `MERCADO_PAGO_PENDING_URL`
- `MERCADO_PAGO_NOTIFY_URL`
