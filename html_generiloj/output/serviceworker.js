const version = 'V0.01';
const staticCacheName = version + 'staticfiles';

addEventListener('install', function(event) {
    skipWaiting();
    event.waitUntil(
        caches.open(staticCacheName).then(function(staticCache) {
            return staticCache.addAll([
                'https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css',
                'https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js',
                'https://cdnjs.cloudflare.com/ajax/libs/jqueryui/1.11.4/jquery-ui.min.js',
                'https://cdnjs.cloudflare.com/ajax/libs/corejs-typeahead/0.11.1/typeahead.bundle.min.js',

                'http://localhost:8000/en/01/gramatiko/',
                'http://localhost:8000/en/02/gramatiko/',
                'http://localhost:8000/en/03/gramatiko/',
                'http://localhost:8000/en/04/gramatiko/',
                'http://localhost:8000/en/05/gramatiko/',
                'http://localhost:8000/en/06/gramatiko/',
                'http://localhost:8000/en/07/gramatiko/',
                'http://localhost:8000/en/08/gramatiko/',
                'http://localhost:8000/en/09/gramatiko/',
                'http://localhost:8000/en/10/gramatiko/',
                'http://localhost:8000/en/11/gramatiko/',
                'http://localhost:8000/en/12/gramatiko/',

                'http://localhost:8000/cs/01/gramatiko/',
                'http://localhost:8000/cs/02/gramatiko/',
                'http://localhost:8000/cs/03/gramatiko/',
                'http://localhost:8000/cs/04/gramatiko/',
                'http://localhost:8000/cs/05/gramatiko/',
                'http://localhost:8000/cs/06/gramatiko/',
                'http://localhost:8000/cs/07/gramatiko/',
                'http://localhost:8000/cs/08/gramatiko/',
                'http://localhost:8000/cs/09/gramatiko/',
                'http://localhost:8000/cs/10/gramatiko/',
                'http://localhost:8000/cs/11/gramatiko/',
                'http://localhost:8000/cs/12/gramatiko/',

                'http://localhost:8000/he/01/gramatiko/',
                'http://localhost:8000/he/02/gramatiko/',
                'http://localhost:8000/he/03/gramatiko/',
                'http://localhost:8000/he/04/gramatiko/',
                'http://localhost:8000/he/05/gramatiko/',
                'http://localhost:8000/he/06/gramatiko/',
                'http://localhost:8000/he/07/gramatiko/',
                'http://localhost:8000/he/08/gramatiko/',
                'http://localhost:8000/he/09/gramatiko/',
                'http://localhost:8000/he/10/gramatiko/',
                'http://localhost:8000/he/11/gramatiko/',
                'http://localhost:8000/he/12/gramatiko/'
            ]);
        }).catch(function(err) {
            console.log('Error while populating cache: '+err);
        })
    );
});

addEventListener('activate', activateEvent => {
  activateEvent.waitUntil(
    caches.keys()
    .then( cacheNames => {
      return Promise.all(
        cacheNames.map( cacheName => {
          if (cacheName != staticCacheName) {
            return caches.delete(cacheName);
          } // end if
        }) // end map
      ); // end return Promise.all
    }) // end keys then
    .then( () => {
      return clients.claim();
    }) // end then
  ); // end waitUntil
}); // end addEventListener

addEventListener('fetch',function(event) {
   console.log(event.request);
   const req = event.request;
   event.respondWith(caches.match(req).then(function(responseFromCache) {
        return responseFromCache || fetch(req);
   }).catch(function(err) {
        console.log(err);
        return new Response(
            '<h1>Oops!</h1> <p>Something went wrong.</p>',
            {
                headers: {'Content-type': 'text/html; charset=utf-8'}
            }
        );
   })
   );
   /*if (req.url.includes('01/ekzerco1/')) {
       event.respondWith(new Response('<h2>Hello, world!</h2>', {
           headers: {'Content-Type':'text/html; charset=utf-8'}
       }))
   }
   else {
       fetch(req).then(function(resp) {
           event.respondWith(resp);
       }).catch(function(err) {
           console.log('error '+err);
       });
   }*/
});