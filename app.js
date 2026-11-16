const navButton = document.querySelector('.menu');
const nav = document.querySelector('#links');

function setMenu(open) {
  nav.classList.toggle('open', open);
  navButton.setAttribute('aria-expanded', String(open));
}

navButton.addEventListener('click', () => setMenu(!nav.classList.contains('open')));
nav.querySelectorAll('a').forEach(link => link.addEventListener('click', () => setMenu(false)));

const descriptions = {
  'set_01_ankommen.m3u': ['SET 01 · ANKOMMEN', 'Warm starten, Raum öffnen.', 'Eine weiche Rampe in die Sendung. Zwischen den Titeln kurze Begrüßung, dann den Groove stehen lassen.'],
  'set_02_house_electro.m3u': ['SET 02 · HOUSE / ELECTRO', 'Die Stadt wird heller.', 'Mehr Bewegung und klare Bässe. Das Moderationsfenster liegt zwischen Groove und Verdichtung.'],
  'set_03_nachtfahrt.m3u': ['SET 03 · NACHTFAHRT', 'Jetzt zieht die Sendung.', 'Techno, Psy und Trance übernehmen. Wenige Worte, viel Raum für die Übergänge.'],
  'set_04_peak_time.m3u': ['SET 04 · PEAK TIME', 'Ein kurzer letzter Schub.', 'Das Finale darf kompakt sein. Danach Abspann, Titelmeldung und Ausblick auf die nächste Folge.']
};

const buttons = document.querySelectorAll('.set');
const label = document.querySelector('#set-label');
const title = document.querySelector('#player-title');
const copy = document.querySelector('#player-copy');
const player = document.querySelector('#player');
const localPreview = ['localhost', '127.0.0.1', '[::1]'].includes(location.hostname);

async function loadPreview(button) {
  player.pause();
  player.hidden = true;
  player.removeAttribute('src');
  player.load();

  try {
    const url = new URL('../playlists/' + button.dataset.set, location.href);
    const playlist = await fetch(url);
    if (!playlist.ok) return;
    const tracks = (await playlist.text()).split(/\r?\n/);
    const firstTrack = tracks.find(line => line.startsWith('../sendung_01/audio/'));
    if (!firstTrack || button.getAttribute('aria-pressed') !== 'true') return;
    player.src = new URL(firstTrack, url);
    player.hidden = false;
  } catch {
    // Public hosting and local servers without the playlists still show the set description.
  }
}

buttons.forEach(button => button.addEventListener('click', () => {
  buttons.forEach(item => {
    const active = item === button;
    item.classList.toggle('active', active);
    item.setAttribute('aria-pressed', String(active));
  });
  const [setLabel, setTitle, setDescription] = descriptions[button.dataset.set];
  label.textContent = setLabel;
  title.textContent = setTitle;
  copy.textContent = setDescription;
  if (localPreview) loadPreview(button);
}));
