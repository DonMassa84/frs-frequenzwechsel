const navButton = document.querySelector('.menu');
const nav = document.querySelector('#links');
navButton?.addEventListener('click', () => {
  const open = nav.classList.toggle('open');
  navButton.setAttribute('aria-expanded', String(open));
});
nav?.querySelectorAll('a').forEach(a => a.addEventListener('click', () => nav.classList.remove('open')));

const descriptions = {
  'set_01_ankommen.m3u': ['SET 01 · ANKOMMEN', 'Warm starten, Raum öffnen.', 'Eine weiche Rampe in die Sendung. Zwischen den Titeln kurze Begrüßung, dann den Groove stehen lassen.', '../sendung_01/audio/25__COSMIC GIRL.mp3'],
  'set_02_house_electro.m3u': ['SET 02 · HOUSE / ELECTRO', 'Die Stadt wird heller.', 'Mehr Bewegung und klare Bässe. Das Moderationsfenster liegt zwischen Groove und Verdichtung.', '../sendung_01/audio/03__17 Flo Jam.mp3'],
  'set_03_nachtfahrt.m3u': ['SET 03 · NACHTFAHRT', 'Jetzt zieht die Sendung.', 'Techno, Psy und Trance übernehmen. Wenige Worte, viel Raum für die Übergänge.', '../sendung_01/audio/09__o.mp3'],
  'set_04_peak_time.m3u': ['SET 04 · PEAK TIME', 'Ein kurzer letzter Schub.', 'Das Finale darf kompakt sein. Danach Abspann, Titelmeldung und Ausblick auf die nächste Folge.', '../sendung_01/audio/21__HotWuk.mp3']
};
const buttons = document.querySelectorAll('.set');
const label = document.querySelector('#set-label');
const title = document.querySelector('#player-title');
const copy = document.querySelector('#player-copy');
const player = document.querySelector('#player');
buttons.forEach(button => button.addEventListener('click', () => {
  buttons.forEach(b => b.classList.remove('active')); button.classList.add('active');
  const data = descriptions[button.dataset.set];
  label.textContent = data[0]; title.textContent = data[1]; copy.textContent = data[2];
  // Browser support for M3U differs; the playlist remains available beside the site.
  player.src = data[3]; player.load();
}));
