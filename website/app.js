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

const handoffAddress = 'roman@coloradio.org';
const supportUrl = 'https://www.freies-radio.de/foerderverein';
const chatForm = document.querySelector('#chat-form');
const chatLog = document.querySelector('#chat-log');
const chatMessage = document.querySelector('#chat-message');
const chatStatus = document.querySelector('#chat-status');
const handoffButton = document.querySelector('#handoff-button');
const guestForm = document.querySelector('#guest-form');
const guestStatus = document.querySelector('#guest-status');

function openMail(subject, body) {
  window.location.href = `mailto:${handoffAddress}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
}

chatForm?.addEventListener('submit', event => {
  event.preventDefault();
  const message = chatMessage.value.trim();
  if (!message) return;
  const bubble = document.createElement('div');
  bubble.className = 'chat-bubble you';
  bubble.innerHTML = `<b>Du</b><p>${message.replace(/[&<>"']/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[char]))}</p>`;
  chatLog.appendChild(bubble);
  chatMessage.value = '';
  chatStatus.textContent = 'Nachricht lokal ergänzt. Übergabe an die Crew ist bereit.';
  chatLog.scrollTop = chatLog.scrollHeight;
});

handoffButton?.addEventListener('click', () => {
  const messages = [...chatLog.querySelectorAll('.chat-bubble p')].map(item => item.textContent).join('\n');
  openMail('Frequenzwechsel · Handoff aus dem Live Chat', `Hallo Roman / Redaktion,\n\nich möchte mein Anliegen aus dem Nachhall-Live-Chat übergeben.\n\nChat-Verlauf:\n${messages}\n\nViele Grüße`);
});

guestForm?.addEventListener('submit', event => {
  event.preventDefault();
  const form = new FormData(guestForm);
  const body = [
    'Hallo Roman / Redaktion,', '',
    'ich möchte mich als Gast-DJ für Frequenzwechsel bewerben.', '',
    `Name / DJ-Name: ${form.get('name')}`,
    `E-Mail: ${form.get('email')}`,
    `Stil / Set: ${form.get('style')}`,
    `Verfügbarkeit: ${form.get('availability') || 'nicht angegeben'}`,
    `Audio-/Video-Sample: ${form.get('sample')}`, '',
    'Erfahrung und Idee:', String(form.get('message')), '',
    'Viele Grüße'
  ].join('\n');
  guestStatus.textContent = 'Bewerbung vorbereitet. Dein E-Mail-Programm öffnet sich jetzt; du entscheidest selbst über den Versand.';
  openMail('Gast-DJ-Bewerbung · Frequenzwechsel', body);
});

document.querySelectorAll('a[href="' + supportUrl + '"]').forEach(link => link.setAttribute('aria-label', 'Offizielle FRS-Fördervereinsseite zum Unterstützen und Spenden'));
