import os
from pathlib import Path
from typing import List
import mercadopago
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

MERCADO_PAGO_USE_SANDBOX = os.getenv("MERCADO_PAGO_USE_SANDBOX", "false").strip().lower() in ("1", "true", "yes")
MERCADO_PAGO_ACCESS_TOKEN = os.getenv("MERCADO_PAGO_ACCESS_TOKEN", "")
MERCADO_PAGO_ACCESS_TOKEN_SANDBOX = os.getenv("MERCADO_PAGO_ACCESS_TOKEN_SANDBOX", "")
MERCADO_PAGO_PUBLIC_KEY = os.getenv("MERCADO_PAGO_PUBLIC_KEY", "")
MERCADO_PAGO_PUBLIC_KEY_SANDBOX = os.getenv("MERCADO_PAGO_PUBLIC_KEY_SANDBOX", "")
MERCADO_PAGO_SUCCESS_URL = os.getenv("MERCADO_PAGO_SUCCESS_URL", "http://localhost:5173/")
MERCADO_PAGO_FAILURE_URL = os.getenv("MERCADO_PAGO_FAILURE_URL", "http://localhost:5173/")
MERCADO_PAGO_PENDING_URL = os.getenv("MERCADO_PAGO_PENDING_URL", "http://localhost:5173/")
MERCADO_PAGO_NOTIFY_URL = os.getenv("MERCADO_PAGO_NOTIFY_URL", "")
ITEM_PRICE = 1500


def get_mercado_pago_sdk() -> mercadopago.SDK:
    token = MERCADO_PAGO_ACCESS_TOKEN_SANDBOX if MERCADO_PAGO_USE_SANDBOX else MERCADO_PAGO_ACCESS_TOKEN
    return mercadopago.SDK(token)

app = FastAPI(
    title="Music API",
    description="API REST para administrar canciones",
    version="1.0.0"
)

# Habilitar CORS: por defecto permite todo en desarrollo,
# pero puede configurarse vía la variable de entorno ALLOW_ORIGINS
ALLOW_ORIGINS_ENV = os.getenv("ALLOW_ORIGINS", "").strip()
if ALLOW_ORIGINS_ENV:
    ALLOW_ORIGINS = [o.strip() for o in ALLOW_ORIGINS_ENV.split(",") if o.strip()]
else:
    ALLOW_ORIGINS = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Song(BaseModel):
    id: int
    title: str
    artist: str
    album: str
    genre: str
    year: int

class CartItem(BaseModel):
    song_id: int
    quantity: int = 1

class CartRequest(BaseModel):
    items: List[CartItem]

class CartSummaryItem(BaseModel):
    song_id: int
    title: str
    artist: str
    quantity: int
    subtotal: float

class CartResponse(BaseModel):
    items: List[CartSummaryItem]
    total_items: int
    total_price: float


def is_placeholder_value(value: str | None) -> bool:
    if not value:
        return True
    normalized = value.strip().lower()
    return "xxxx" in normalized or normalized.startswith("app_usr-xxxxxxxx") or normalized.startswith("test-xxxxxxxx")


def _is_secure_url(url: str | None) -> bool:
    return bool(url and url.lower().startswith("https://"))


def build_payment_payload(
    request: CartRequest,
    songs: List[dict],
    success_url: str | None = None,
    failure_url: str | None = None,
    pending_url: str | None = None,
    notification_url: str | None = None,
) -> dict:
    items = []
    for item in request.items:
        song = next((s for s in songs if s["id"] == item.song_id), None)
        if song:
            items.append({"title": song["title"], "quantity": item.quantity, "currency_id": "ARS", "unit_price": round(item.quantity * ITEM_PRICE, 2)})

    success = success_url or MERCADO_PAGO_SUCCESS_URL
    payload = {"items": items, "back_urls": {"success": success, "failure": failure_url or MERCADO_PAGO_FAILURE_URL, "pending": pending_url or MERCADO_PAGO_PENDING_URL}}
    if _is_secure_url(success):
        payload["auto_return"] = "approved"
    if notification_url:
        payload["notification_url"] = notification_url
    return payload


def build_payment_response(mercado_pago_response: dict, public_key: str | None = None) -> dict:
    return {
        "preference_id": mercado_pago_response.get("id"),
        "id": mercado_pago_response.get("id"),
        "init_point": mercado_pago_response.get("init_point"),
        "sandbox_init_point": mercado_pago_response.get("sandbox_init_point"),
        "public_key": public_key or MERCADO_PAGO_PUBLIC_KEY,
    }


songs = [
    {"id": 1, "title": "Bohemian Rhapsody", "artist": "Queen", "album": "A Night at the Opera", "genre": "Rock", "year": 1975},
    {"id": 2, "title": "Billie Jean", "artist": "Michael Jackson", "album": "Thriller", "genre": "Pop", "year": 1982},
    {"id": 3, "title": "Imagine", "artist": "John Lennon", "album": "Imagine", "genre": "Rock", "year": 1971},
    {"id": 4, "title": "Hotel California", "artist": "Eagles", "album": "Hotel California", "genre": "Rock", "year": 1976},
    {"id": 5, "title": "Smells Like Teen Spirit", "artist": "Nirvana", "album": "Nevermind", "genre": "Grunge", "year": 1991},
    {"id": 6, "title": "Wonderwall", "artist": "Oasis", "album": "(What's the Story) Morning Glory?", "genre": "Britpop", "year": 1995},
    {"id": 7, "title": "Lose Yourself", "artist": "Eminem", "album": "8 Mile", "genre": "Hip Hop", "year": 2002},
    {"id": 8, "title": "Rolling in the Deep", "artist": "Adele", "album": "21", "genre": "Pop", "year": 2010},
    {"id": 9, "title": "Shape of You", "artist": "Ed Sheeran", "album": "÷", "genre": "Pop", "year": 2017},
    {"id": 10, "title": "Blinding Lights", "artist": "The Weeknd", "album": "After Hours", "genre": "Synthwave", "year": 2019},
    {"id": 11, "title": "Thriller", "artist": "Michael Jackson", "album": "Thriller", "genre": "Pop", "year": 1982},
    {"id": 12, "title": "Stairway to Heaven", "artist": "Led Zeppelin", "album": "Led Zeppelin IV", "genre": "Rock", "year": 1971},
    {"id": 13, "title": "Sweet Child O' Mine", "artist": "Guns N' Roses", "album": "Appetite for Destruction", "genre": "Hard Rock", "year": 1987},
    {"id": 14, "title": "Nothing Else Matters", "artist": "Metallica", "album": "Metallica", "genre": "Metal", "year": 1991},
    {"id": 15, "title": "Numb", "artist": "Linkin Park", "album": "Meteora", "genre": "Nu Metal", "year": 2003},
    {"id": 16, "title": "Viva La Vida", "artist": "Coldplay", "album": "Viva la Vida", "genre": "Alternative", "year": 2008},
    {"id": 17, "title": "Radioactive", "artist": "Imagine Dragons", "album": "Night Visions", "genre": "Alternative", "year": 2012},
    {"id": 18, "title": "Believer", "artist": "Imagine Dragons", "album": "Evolve", "genre": "Alternative", "year": 2017},
    {"id": 19, "title": "Counting Stars", "artist": "OneRepublic", "album": "Native", "genre": "Pop Rock", "year": 2013},
    {"id": 20, "title": "Take on Me", "artist": "a-ha", "album": "Hunting High and Low", "genre": "Synth Pop", "year": 1985},
    {"id": 21, "title": "Africa", "artist": "Toto", "album": "Toto IV", "genre": "Rock", "year": 1982},
    {"id": 22, "title": "Livin' on a Prayer", "artist": "Bon Jovi", "album": "Slippery When Wet", "genre": "Rock", "year": 1986},
    {"id": 23, "title": "Eye of the Tiger", "artist": "Survivor", "album": "Eye of the Tiger", "genre": "Rock", "year": 1982},
    {"id": 24, "title": "Another One Bites the Dust", "artist": "Queen", "album": "The Game", "genre": "Rock", "year": 1980},
    {"id": 25, "title": "Back in Black", "artist": "AC/DC", "album": "Back in Black", "genre": "Hard Rock", "year": 1980},
    {"id": 26, "title": "Highway to Hell", "artist": "AC/DC", "album": "Highway to Hell", "genre": "Hard Rock", "year": 1979},
    {"id": 27, "title": "Yesterday", "artist": "The Beatles", "album": "Help!", "genre": "Rock", "year": 1965},
    {"id": 28, "title": "Hey Jude", "artist": "The Beatles", "album": "Single", "genre": "Rock", "year": 1968},
    {"id": 29, "title": "Let It Be", "artist": "The Beatles", "album": "Let It Be", "genre": "Rock", "year": 1970},
    {"id": 30, "title": "Paint It Black", "artist": "The Rolling Stones", "album": "Aftermath", "genre": "Rock", "year": 1966},
    {"id": 31, "title": "Zombie", "artist": "The Cranberries", "album": "No Need to Argue", "genre": "Alternative Rock", "year": 1994},
    {"id": 32, "title": "Creep", "artist": "Radiohead", "album": "Pablo Honey", "genre": "Alternative Rock", "year": 1992},
    {"id": 33, "title": "Yellow", "artist": "Coldplay", "album": "Parachutes", "genre": "Alternative", "year": 2000},
    {"id": 34, "title": "Fix You", "artist": "Coldplay", "album": "X&Y", "genre": "Alternative", "year": 2005},
    {"id": 35, "title": "Chasing Cars", "artist": "Snow Patrol", "album": "Eyes Open", "genre": "Alternative", "year": 2006},
    {"id": 36, "title": "Demons", "artist": "Imagine Dragons", "album": "Night Visions", "genre": "Alternative", "year": 2012},
    {"id": 37, "title": "Someone Like You", "artist": "Adele", "album": "21", "genre": "Pop", "year": 2011},
    {"id": 38, "title": "Bad Romance", "artist": "Lady Gaga", "album": "The Fame Monster", "genre": "Pop", "year": 2009},
    {"id": 39, "title": "Poker Face", "artist": "Lady Gaga", "album": "The Fame", "genre": "Pop", "year": 2008},
    {"id": 40, "title": "Firework", "artist": "Katy Perry", "album": "Teenage Dream", "genre": "Pop", "year": 2010},
    {"id": 41, "title": "Uptown Funk", "artist": "Mark Ronson ft. Bruno Mars", "album": "Uptown Special", "genre": "Funk Pop", "year": 2014},
    {"id": 42, "title": "Locked Out of Heaven", "artist": "Bruno Mars", "album": "Unorthodox Jukebox", "genre": "Pop", "year": 2012},
    {"id": 43, "title": "Happy", "artist": "Pharrell Williams", "album": "Girl", "genre": "Pop", "year": 2013},
    {"id": 44, "title": "Can't Stop the Feeling!", "artist": "Justin Timberlake", "album": "Trolls", "genre": "Pop", "year": 2016},
    {"id": 45, "title": "Dance Monkey", "artist": "Tones and I", "album": "The Kids Are Coming", "genre": "Pop", "year": 2019},
    {"id": 46, "title": "Levitating", "artist": "Dua Lipa", "album": "Future Nostalgia", "genre": "Disco Pop", "year": 2020},
    {"id": 47, "title": "As It Was", "artist": "Harry Styles", "album": "Harry's House", "genre": "Pop", "year": 2022},
    {"id": 48, "title": "Flowers", "artist": "Miley Cyrus", "album": "Endless Summer Vacation", "genre": "Pop", "year": 2023},
    {"id": 49, "title": "Anti-Hero", "artist": "Taylor Swift", "album": "Midnights", "genre": "Pop", "year": 2022},
    {"id": 50, "title": "Espresso", "artist": "Sabrina Carpenter", "album": "Short n' Sweet", "genre": "Pop", "year": 2024}
]

# Obtener todas las canciones
@app.get("/songs", response_model=List[Song])
def get_songs():
    return songs

# Obtener una canción por ID
@app.get("/songs/{song_id}", response_model=Song)
def get_song(song_id: int):
    for song in songs:
        if song["id"] == song_id:
            return song
    raise HTTPException(status_code=404, detail="Canción no encontrada")

# Crear una canción
@app.post("/songs", response_model=Song, status_code=201)
def create_song(song: Song):
    for s in songs:
        if s["id"] == song.id:
            raise HTTPException(status_code=400, detail="El ID ya existe")

    songs.append(song.dict())
    return song

# Actualizar una canción
@app.put("/songs/{song_id}", response_model=Song)
def update_song(song_id: int, updated_song: Song):
    for index, song in enumerate(songs):
        if song["id"] == song_id:
            songs[index] = updated_song.dict()
            return updated_song

    raise HTTPException(status_code=404, detail="Canción no encontrada")

# Eliminar una canción
@app.delete("/songs/{song_id}")
def delete_song(song_id: int):
    for index, song in enumerate(songs):
        if song["id"] == song_id:
            songs.pop(index)
            return {"message": "Canción eliminada"}

    raise HTTPException(status_code=404, detail="Canción no encontrada")

# Procesar carrito de compras
@app.post("/carrito", response_model=CartResponse)
def checkout_cart(request: CartRequest):
    cart_items = []
    total_items = 0
    total_price = 0.0
    for item in request.items:
        song = next((s for s in songs if s["id"] == item.song_id), None)
        if not song:
            continue
        subtotal = round(item.quantity * ITEM_PRICE, 2)
        cart_items.append(CartSummaryItem(song_id=song["id"], title=song["title"], artist=song["artist"], quantity=item.quantity, subtotal=subtotal))
        total_items += item.quantity
        total_price += subtotal
    return CartResponse(items=cart_items, total_items=total_items, total_price=round(total_price, 2))


async def _create_payment_response(request: CartRequest):
    access_token = os.getenv("MERCADO_PAGO_ACCESS_TOKEN", "")
    if is_placeholder_value(access_token):
        return {
            **build_payment_response(
                {"id": "demo-preference", "init_point": "http://localhost:5173/pago-simulado"},
                MERCADO_PAGO_PUBLIC_KEY or "TEST-PLACEHOLDER",
            ),
            "message": "Modo demo activado: usa un token real de Mercado Pago para generar un checkout real.",
        }

    payload = build_payment_payload(
        request,
        songs,
        success_url=MERCADO_PAGO_SUCCESS_URL,
        failure_url=MERCADO_PAGO_FAILURE_URL,
        pending_url=MERCADO_PAGO_PENDING_URL,
        notification_url=MERCADO_PAGO_NOTIFY_URL or None,
    )

    try:
        preference_response = get_mercado_pago_sdk().preference().create(payload)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Error al crear la preferencia de pago: {exc}")

    status = preference_response.get("status")
    response_data = preference_response.get("response") if isinstance(preference_response, dict) else None

    if not response_data or (status and status >= 400):
        detail = None
        if isinstance(response_data, dict):
            detail = response_data.get("message") or response_data.get("error")
        raise HTTPException(status_code=status or 500, detail=detail or "Error al crear la preferencia de pago")

    public_key = (
        MERCADO_PAGO_PUBLIC_KEY_SANDBOX
        if MERCADO_PAGO_USE_SANDBOX and MERCADO_PAGO_PUBLIC_KEY_SANDBOX
        else MERCADO_PAGO_PUBLIC_KEY
    )
    return build_payment_response(response_data, public_key)


@app.post("/carrito/pago")
async def create_cart_payment(request: CartRequest):
    return await _create_payment_response(request)


@app.post("/crear-pago")
async def create_payment(request: CartRequest):
    return await _create_payment_response(request)