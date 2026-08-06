export function SongCatalog({ songs, total, query, onSearch, onAdd }) {
  return (
    <section className="catalog-card">
      <div className="section-head">
        <div>
          <h2>Canciones disponibles</h2>
          <span className="pill">{songs.length} de {total} items</span>
        </div>
        <input
          className="search-input"
          placeholder="Buscar canción o artista"
          value={query}
          onChange={event => onSearch(event.target.value)}
        />
      </div>
      <div className="song-list">
        {songs.map(song => (
          <article key={song.id} className="song-card">
            <div>
              <h3>{song.title}</h3>
              <p>{song.artist} — {song.album}</p>
              <small>{song.genre} · {song.year}</small>
            </div>
            <button onClick={() => onAdd(song)}>Agregar</button>
          </article>
        ))}
      </div>
    </section>
  )
}
