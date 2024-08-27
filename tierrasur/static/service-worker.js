const cacheName = 'tierrasur-v1';
const filesToCache = [
    '/',
    '/static/style.css',
    '/static/images/tierrasur.png'
];

self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(cacheName)
        .then(cache => {
            return cache.addAll(filesToCache);
        })
    );
});

self.addEventListener('fetch', event => {
    event.respondWith(
        caches.match(event.request)
        .then(response => {
            return response || fetch(event.request);
        })
    );
});
