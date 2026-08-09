const CACHE = 'convite-ihanny-ryan-v7';
const ASSETS = [
  './',
  './index.html',
  './styles.css?v=6',
  './script.js?v=6',
  './config.js?v=6',
  './manifest.webmanifest',
  './assets/church-watercolor.svg',
  './assets/leaf-corner.svg',
  './assets/icon.svg',
  './assets/pix-150.png',
  './assets/pix-200.png',
  './assets/pix-300.png'
];

self.addEventListener('install', event => {
  self.skipWaiting();
  event.waitUntil(caches.open(CACHE).then(cache => cache.addAll(ASSETS)));
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(key => key !== CACHE).map(key => caches.delete(key))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', event => {
  if (event.request.method !== 'GET') return;
  event.respondWith(
    fetch(event.request)
      .then(response => {
        const copy = response.clone();
        caches.open(CACHE).then(cache => cache.put(event.request, copy));
        return response;
      })
      .catch(() => caches.match(event.request))
  );
});
