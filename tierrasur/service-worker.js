const cacheName = 'tierrasur-v1';
const filesToCache = [
    '/',
    '/templates/base.html',
    '/templates/login.html',
    '/templates/register.html',
    '/static/style.css',
    '/static/style_home.css',
    '/script.js',
    '/manifest.json',
    'static/images/tierrasur.png'
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
