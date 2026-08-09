const cfg = window.INVITE_CONFIG;

const openingScreen = document.getElementById('openingScreen');
const openInvitation = document.getElementById('openInvitation');
const audio = document.getElementById('weddingAudio');
const playButton = document.getElementById('playButton');
const playIcon = document.getElementById('playIcon');
const waveform = document.querySelector('.waveform');
const musicTime = document.getElementById('musicTime');
const toast = document.getElementById('toast');

let selectedGift = 150;

function showToast(message, duration = 2800) {
  toast.textContent = message;
  toast.classList.add('show');
  window.clearTimeout(showToast.timeout);
  showToast.timeout = window.setTimeout(() => toast.classList.remove('show'), duration);
}

function formatTime(seconds) {
  if (!Number.isFinite(seconds)) return '00:00';
  const min = Math.floor(seconds / 60).toString().padStart(2, '0');
  const sec = Math.floor(seconds % 60).toString().padStart(2, '0');
  return `${min}:${sec}`;
}

async function copyText(value, successMessage) {
  try {
    if (navigator.clipboard && window.isSecureContext) {
      await navigator.clipboard.writeText(value);
    } else {
      const area = document.createElement('textarea');
      area.value = value;
      area.setAttribute('readonly', '');
      area.style.position = 'fixed';
      area.style.opacity = '0';
      document.body.appendChild(area);
      area.select();
      document.execCommand('copy');
      area.remove();
    }
    showToast(successMessage);
    return true;
  } catch {
    showToast('Não foi possível copiar. Selecione e copie a chave manualmente.', 3600);
    return false;
  }
}

function renderMonogram(element) {
  if (!element) return;
  element.setAttribute('aria-label', `Monograma ${cfg.monogram}`);
  element.innerHTML = '<span class="letter">I</span><span class="letter">M</span>';
}

function setupContent() {
  ['mapsLink', 'mapsCardLink', 'mobileMap'].forEach(id => {
    const element = document.getElementById(id);
    if (element) element.href = cfg.ceremony.mapsUrl;
  });

  document.querySelectorAll('.wax-seal__monogram, .brand-mark, .hero-monogram, .closing-monogram').forEach(renderMonogram);

  document.getElementById('pixKeyDisplay').textContent = cfg.pix.displayKey;
  document.getElementById('giftPixKey').textContent = cfg.pix.displayKey;
  audio.src = cfg.music.file;
}

async function tryPlayMusic(showFeedback = true) {
  try {
    await audio.play();
    playIcon.textContent = '❚❚';
    waveform.classList.add('is-playing');
    return true;
  } catch {
    if (showFeedback) showToast('O instrumental ainda precisa ser adicionado na pasta assets.', 3000);
    return false;
  }
}

function openCover() {
  openingScreen.classList.add('is-opening');
  document.body.classList.remove('no-scroll');
  window.setTimeout(() => openingScreen.classList.add('is-open'), 720);
  tryPlayMusic(false);
}

openInvitation.addEventListener('click', openCover);

playButton.addEventListener('click', async () => {
  if (audio.paused) await tryPlayMusic(true);
  else {
    audio.pause();
    playIcon.textContent = '▶';
    waveform.classList.remove('is-playing');
  }
});

audio.addEventListener('timeupdate', () => {
  musicTime.textContent = formatTime(audio.currentTime);
});

audio.addEventListener('ended', () => {
  playIcon.textContent = '▶';
  waveform.classList.remove('is-playing');
});

audio.addEventListener('error', () => {
  musicTime.textContent = '—:—';
  document.getElementById('musicCard').classList.add('is-disabled');
  const subtitle = document.querySelector('.music-meta span');
  if (subtitle) subtitle.textContent = 'Instrumental em breve';
});

const menuToggle = document.getElementById('menuToggle');
const navMenu = document.getElementById('navMenu');
menuToggle.addEventListener('click', () => {
  const open = navMenu.classList.toggle('is-open');
  menuToggle.setAttribute('aria-expanded', String(open));
});
navMenu.querySelectorAll('a').forEach(link => link.addEventListener('click', () => {
  navMenu.classList.remove('is-open');
  menuToggle.setAttribute('aria-expanded', 'false');
}));
document.addEventListener('click', event => {
  const clickedInside = navMenu.contains(event.target) || menuToggle.contains(event.target);
  if (!clickedInside && navMenu.classList.contains('is-open')) {
    navMenu.classList.remove('is-open');
    menuToggle.setAttribute('aria-expanded', 'false');
  }
});

function openDialog(id) {
  const dialog = document.getElementById(id);
  if (dialog && typeof dialog.showModal === 'function') dialog.showModal();
}

['openRsvp', 'openRsvpBottom', 'mobileRsvp'].forEach(id => { const el = document.getElementById(id); if (el) el.addEventListener('click', () => openDialog('rsvpModal')); });

document.querySelectorAll('[data-close]').forEach(button => {
  button.addEventListener('click', () => document.getElementById(button.dataset.close).close());
});

document.querySelectorAll('dialog').forEach(dialog => {
  dialog.addEventListener('click', event => {
    const rect = dialog.getBoundingClientRect();
    const inside = event.clientX >= rect.left && event.clientX <= rect.right && event.clientY >= rect.top && event.clientY <= rect.bottom;
    if (!inside) dialog.close();
  });
});

function showGift(amount) {
  const gift = cfg.pix.gifts[String(amount)];
  if (!gift) return;
  selectedGift = Number(amount);
  document.getElementById('giftModalTitle').textContent = `Presentear com R$ ${amount}`;
  document.getElementById('giftAmount').textContent = gift.amountLabel;
  const qr = document.getElementById('giftQr');
  qr.src = gift.qr;
  qr.alt = `QR Code Pix no valor de ${gift.amountLabel}`;
  openDialog('giftModal');
}

document.querySelectorAll('[data-gift]').forEach(card => {
  card.addEventListener('click', () => showGift(card.dataset.gift));
});

document.getElementById('copyPixKey').addEventListener('click', () => {
  copyText(cfg.pix.key, 'Chave Pix copiada.');
});
document.getElementById('copyGiftKey').addEventListener('click', () => {
  copyText(cfg.pix.key, 'Chave Pix copiada.');
});
document.getElementById('copyGiftPix').addEventListener('click', () => {
  const gift = cfg.pix.gifts[String(selectedGift)];
  copyText(gift.payload, `Pix de ${gift.amountLabel} copiado.`);
});

const rsvpForm = document.getElementById('rsvpForm');
rsvpForm.addEventListener('submit', async event => {
  event.preventDefault();
  const name = document.getElementById('guestName').value.trim();
  const status = document.getElementById('guestStatus').value;
  const message = document.getElementById('guestMessage').value.trim();
  const text = `Olá, Ihanny e Marcos Ryan!%0A%0AConfirmação de presença:%0ANome: ${encodeURIComponent(name)}%0AResposta: ${encodeURIComponent(status)}${message ? `%0AMensagem: ${encodeURIComponent(message)}` : ''}`;

  if (cfg.whatsappNumber) {
    window.open(`https://wa.me/${cfg.whatsappNumber}?text=${text}`, '_blank', 'noopener,noreferrer');
    document.getElementById('formNote').textContent = 'Abrimos o WhatsApp com a mensagem pronta.';
  } else {
    const plain = `Olá, Ihanny e Marcos Ryan!\n\nConfirmação de presença:\nNome: ${name}\nResposta: ${status}${message ? `\nMensagem: ${message}` : ''}`;
    const copied = await copyText(plain, 'Confirmação copiada para enviar aos noivos.');
    document.getElementById('formNote').textContent = copied
      ? 'A mensagem foi copiada. Adicione o WhatsApp em config.js para envio automático.'
      : 'Adicione o WhatsApp em config.js para ativar o envio.';
  }
});

function updateCountdown() {
  const now = new Date();
  const target = new Date(cfg.dateISO);
  let diff = target - now;
  if (diff < 0) diff = 0;
  const days = Math.floor(diff / 86400000);
  const hours = Math.floor((diff % 86400000) / 3600000);
  const minutes = Math.floor((diff % 3600000) / 60000);
  const seconds = Math.floor((diff % 60000) / 1000);
  document.getElementById('days').textContent = String(days).padStart(3, '0');
  document.getElementById('hours').textContent = String(hours).padStart(2, '0');
  document.getElementById('minutes').textContent = String(minutes).padStart(2, '0');
  document.getElementById('seconds').textContent = String(seconds).padStart(2, '0');
}

const observer = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      observer.unobserve(entry.target);
    }
  });
}, { threshold: .12 });
document.querySelectorAll('.reveal').forEach(el => observer.observe(el));

setupContent();
updateCountdown();
window.setInterval(updateCountdown, 1000);
document.body.classList.add('no-scroll');

if (new URLSearchParams(window.location.search).has('preview')) {
  window.setTimeout(openCover, 100);
}

if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => navigator.serviceWorker.register('sw.js?v=7').catch(() => {}));
}
