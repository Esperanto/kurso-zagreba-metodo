const CACHE_NAME = '__CACHE_NAME__';
const PRECACHE_URLS = __PRECACHE_URLS__;

self.addEventListener('install', function (event) {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(function (cache) {
        return cache.addAll(PRECACHE_URLS);
      })
      .then(function () {
        return self.skipWaiting();
      })
  );
});

self.addEventListener('activate', function (event) {
  event.waitUntil(
    caches.keys()
      .then(function (names) {
        return Promise.all(names.map(function (name) {
          if (name.startsWith('esperanto12-') && name !== CACHE_NAME) {
            return caches.delete(name);
          }
          return Promise.resolve();
        }));
      })
      .then(function () {
        return self.clients.claim();
      })
  );
});

function normalizedPathname(request) {
  const url = new URL(request.url);
  let pathname = url.pathname;
  const filename = pathname.split('/').pop();

  if (pathname.endsWith('/')) {
    return pathname + 'index.html';
  }
  if (!filename.includes('.')) {
    return pathname + '/index.html';
  }
  return pathname;
}

function fromCache(request) {
  return caches.open(CACHE_NAME).then(function (cache) {
    return cache.match(request, {ignoreSearch: true}).then(function (directMatch) {
      if (directMatch) {
        return directMatch;
      }
      return cache.match(normalizedPathname(request), {ignoreSearch: true});
    });
  });
}

function offlineResponse(request) {
  return fromCache(request).then(function (cached) {
    if (cached) {
      return cached;
    }
    return caches.match('/index.html');
  });
}

self.addEventListener('fetch', function (event) {
  const request = event.request;
  const url = new URL(request.url);

  if (request.method !== 'GET' || url.origin !== self.location.origin) {
    return;
  }

  if (request.mode === 'navigate') {
    event.respondWith(
      fetch(request).catch(function () {
        return offlineResponse(request);
      })
    );
    return;
  }

  event.respondWith(
    fromCache(request).then(function (cached) {
      if (cached) {
        return cached;
      }
      return fetch(request);
    })
  );
});
