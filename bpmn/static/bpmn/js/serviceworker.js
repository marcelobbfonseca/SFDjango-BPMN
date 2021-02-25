// Set this to true for production.
var doCache = false;

var staticCacheName = 'S-SMMS';

var filesToCache = [
  '/',
];

self.addEventListener('activate', function(e) {
  e.waitUntil(
    caches.keys().then(function(keyList) {
      return Promise.all(keyList.map(function(key) {
        if (key !== staticCacheName) {
          return caches.delete(key);
        }
      }));
    })
  );
});

self.addEventListener('install', function(event) {
  if (doCache) {
    self.skipWaiting();
    event.waitUntil(
      caches.open(staticCacheName).then(function (cache) {
        return cache.addAll(filesToCache);
      })
    );
  }
});

self.addEventListener('fetch', function(event) {
    if (doCache) {
      event.respondWith(
          caches.match(event.request).then(function(response) {
              return response || fetch(event.request);
          })
      );
    }
});