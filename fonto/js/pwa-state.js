(function () {
  'use strict';

  var DB_NAME = 'esperanto12-pwa-state';
  var DB_VERSION = 1;
  var PAGE_STORE = 'pages';
  var INPUT_STORE = 'inputs';
  var INPUT_DEBOUNCE_MS = 400;
  var SCROLL_DEBOUNCE_MS = 500;

  function hasPwaManifest() {
    return !!document.querySelector('link[rel="manifest"]');
  }

  function isStandalonePwa() {
    var iOSStandalone = window.navigator.standalone === true;
    var displayModeStandalone = window.matchMedia
      && window.matchMedia('(display-mode: standalone)').matches;
    var markedStandalone = document.documentElement.classList.contains('pwa-standalone');
    return iOSStandalone || displayModeStandalone || markedStandalone;
  }

  function detectLanguage() {
    var match = window.location.pathname.match(/^\/([^/]+)\//);
    return match ? match[1] : null;
  }

  function normalizePath(pathname) {
    var normalized = pathname || '/';
    if (normalized.endsWith('/index.html')) {
      normalized = normalized.slice(0, -'index.html'.length);
    }

    var basename = normalized.split('/').pop();
    if (normalized !== '/' && !normalized.endsWith('/') && basename.indexOf('.') === -1) {
      normalized += '/';
    }
    return normalized;
  }

  function pageUrl() {
    return window.location.pathname + window.location.search + window.location.hash;
  }

  function sameOriginReferrer() {
    if (!document.referrer) {
      return false;
    }

    try {
      return new URL(document.referrer).origin === window.location.origin;
    } catch (error) {
      return false;
    }
  }

  function logStorageError(error) {
    if (window.console && console.warn) {
      console.warn('Ne eblis konservi PWA-staton.', error);
    }
  }

  var lingvo = detectLanguage();
  var path = normalizePath(window.location.pathname);

  if (!hasPwaManifest() || !isStandalonePwa() || !lingvo || !window.indexedDB) {
    return;
  }
  if (path.indexOf('/' + lingvo + '/') !== 0) {
    return;
  }

  var dbPromise = openDb();
  var pendingInputs = {};
  var pendingInputTimer = null;
  var scrollTimer = null;
  var restoringInputs = false;

  function openDb() {
    return new Promise(function (resolve, reject) {
      var request = window.indexedDB.open(DB_NAME, DB_VERSION);

      request.onupgradeneeded = function () {
        var db = request.result;
        if (!db.objectStoreNames.contains(PAGE_STORE)) {
          db.createObjectStore(PAGE_STORE, { keyPath: 'key' });
        }
        if (!db.objectStoreNames.contains(INPUT_STORE)) {
          db.createObjectStore(INPUT_STORE, { keyPath: 'key' });
        }
      };

      request.onsuccess = function () {
        resolve(request.result);
      };
      request.onerror = function () {
        reject(request.error);
      };
      request.onblocked = function () {
        reject(request.error || new Error('IndexedDB open request blocked'));
      };
    });
  }

  function withStore(storeName, mode, callback) {
    return dbPromise.then(function (db) {
      return new Promise(function (resolve, reject) {
        var transaction = db.transaction(storeName, mode);
        var store = transaction.objectStore(storeName);
        var result;

        transaction.oncomplete = function () {
          resolve(result);
        };
        transaction.onerror = function () {
          reject(transaction.error);
        };
        transaction.onabort = function () {
          reject(transaction.error);
        };

        try {
          result = callback(store);
        } catch (error) {
          transaction.abort();
          reject(error);
        }
      });
    });
  }

  function readRecord(storeName, key) {
    return withStore(storeName, 'readonly', function (store) {
      return new Promise(function (resolve, reject) {
        var request = store.get(key);
        request.onsuccess = function () {
          resolve(request.result || null);
        };
        request.onerror = function () {
          reject(request.error);
        };
      });
    });
  }

  function putRecord(storeName, record) {
    return withStore(storeName, 'readwrite', function (store) {
      store.put(record);
    });
  }

  function deleteRecord(storeName, key) {
    return withStore(storeName, 'readwrite', function (store) {
      store.delete(key);
    });
  }

  function lastPageKey() {
    return lingvo + '|last';
  }

  function currentPageKey() {
    return lingvo + '|page|' + path;
  }

  function inputKey(input) {
    return lingvo + '|input|' + path + '|' + input.id;
  }

  function inputKeyById(inputId) {
    return lingvo + '|input|' + path + '|' + inputId;
  }

  function pageRecord(key) {
    return {
      key: key,
      lingvo: lingvo,
      path: path,
      url: pageUrl(),
      scrollY: window.scrollY || window.pageYOffset || 0,
      updatedAt: Date.now()
    };
  }

  function isLanguageRoot() {
    return path === '/' + lingvo + '/';
  }

  function isSafePageUrl(urlValue) {
    try {
      var url = new URL(urlValue, window.location.origin);
      return url.origin === window.location.origin
        && normalizePath(url.pathname).indexOf('/' + lingvo + '/') === 0;
    } catch (error) {
      return false;
    }
  }

  function savePageState() {
    var record = pageRecord(currentPageKey());
    return Promise.all([
      putRecord(PAGE_STORE, record),
      putRecord(PAGE_STORE, Object.assign({}, record, { key: lastPageKey() }))
    ]).catch(logStorageError);
  }

  function schedulePageSave() {
    window.clearTimeout(scrollTimer);
    scrollTimer = window.setTimeout(savePageState, SCROLL_DEBOUNCE_MS);
  }

  function restoreScrollPosition() {
    if (window.location.hash) {
      return Promise.resolve();
    }

    return readRecord(PAGE_STORE, currentPageKey()).then(function (record) {
      if (!record || typeof record.scrollY !== 'number' || record.scrollY <= 0) {
        return;
      }

      window.requestAnimationFrame(function () {
        window.scrollTo(0, record.scrollY);
      });
    }).catch(logStorageError);
  }

  function allExerciseInputs() {
    return Array.prototype.slice.call(document.querySelectorAll('input[data-solvo][id]'));
  }

  function restoreInputValues() {
    var inputs = allExerciseInputs();
    if (inputs.length === 0) {
      return Promise.resolve();
    }

    restoringInputs = true;
    return Promise.all(inputs.map(function (input) {
      return readRecord(INPUT_STORE, inputKey(input)).then(function (record) {
        if (!record || typeof record.value !== 'string') {
          return;
        }
        input.value = record.value;
        input.dispatchEvent(new Event('input', { bubbles: true }));
      });
    })).catch(logStorageError).then(function () {
      restoringInputs = false;
    });
  }

  function flushInput(inputId, value) {
    var key = inputKeyById(inputId);
    if (value === '') {
      return deleteRecord(INPUT_STORE, key);
    }

    return putRecord(INPUT_STORE, {
      key: key,
      lingvo: lingvo,
      path: path,
      inputId: inputId,
      value: value,
      updatedAt: Date.now()
    });
  }

  function flushPendingInputs() {
    var values = pendingInputs;
    pendingInputs = {};
    window.clearTimeout(pendingInputTimer);
    pendingInputTimer = null;

    var inputIds = Object.keys(values);
    if (inputIds.length === 0) {
      return Promise.resolve();
    }

    return Promise.all(inputIds.map(function (inputId) {
      return flushInput(inputId, values[inputId]);
    })).catch(logStorageError);
  }

  function queueInput(input, flushNow) {
    if (restoringInputs || !input.id) {
      return;
    }

    pendingInputs[input.id] = input.value;
    if (flushNow) {
      flushPendingInputs();
      return;
    }

    window.clearTimeout(pendingInputTimer);
    pendingInputTimer = window.setTimeout(flushPendingInputs, INPUT_DEBOUNCE_MS);
  }

  function bindInputPersistence() {
    var inputs = allExerciseInputs();
    inputs.forEach(function (input) {
      if (window.jQuery) {
        window.jQuery(input)
          .on('input.pwaState', function () {
            queueInput(input, false);
          })
          .on('change.pwaState blur.pwaState', function () {
            queueInput(input, true);
          });
      } else {
        input.addEventListener('input', function () {
          queueInput(input, false);
        });
        input.addEventListener('change', function () {
          queueInput(input, true);
        });
        input.addEventListener('blur', function () {
          queueInput(input, true);
        });
      }
    });
  }

  function bindButtonFlushes() {
    if (!window.jQuery) {
      return;
    }

    window.jQuery('.solvu, .forigu').on('click.pwaState', function () {
      window.setTimeout(flushPendingInputs, 0);
    });
  }

  function bindPagePersistence() {
    window.addEventListener('scroll', schedulePageSave, { passive: true });
    window.addEventListener('pagehide', function () {
      flushPendingInputs();
      savePageState();
    });
    document.addEventListener('visibilitychange', function () {
      if (document.visibilityState === 'hidden') {
        flushPendingInputs();
        savePageState();
      }
    });
  }

  function resumeLastPageIfNeeded() {
    if (!isLanguageRoot() || window.location.hash || sameOriginReferrer()) {
      return Promise.resolve(false);
    }

    return readRecord(PAGE_STORE, lastPageKey()).then(function (record) {
      if (!record || !record.url || !isSafePageUrl(record.url)) {
        return false;
      }
      if (record.url === pageUrl()) {
        return false;
      }

      window.location.replace(record.url);
      return true;
    }).catch(function (error) {
      logStorageError(error);
      return false;
    });
  }

  resumeLastPageIfNeeded().then(function (redirecting) {
    if (redirecting) {
      return;
    }

    bindInputPersistence();
    bindButtonFlushes();
    bindPagePersistence();
    restoreInputValues()
      .then(restoreScrollPosition)
      .then(savePageState)
      .catch(logStorageError);
  }).catch(logStorageError);
}());
