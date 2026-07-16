(function () {
  'use strict';

  var DB_NAME = 'esperanto12-pwa-state';
  var DB_VERSION = 1;
  var PAGE_STORE = 'pages';
  var INPUT_STORE = 'inputs';
  var INPUT_DEBOUNCE_MS = 400;
  var SCROLL_DEBOUNCE_MS = 500;
  var IN_APP_NAVIGATION_PREFIX = 'esperanto12-pwa-in-app-navigation:';
  var RESUME_TARGET_PREFIX = 'esperanto12-pwa-resume-target:';

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

  function normalizedUrlKey(urlValue) {
    try {
      var url = new URL(urlValue, window.location.origin);
      return normalizePath(url.pathname) + url.search + url.hash;
    } catch (error) {
      return null;
    }
  }

  function currentUrlKey() {
    return normalizedUrlKey(pageUrl());
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
  var inAppNavigationStarted = false;
  var inAppNavigationTaken = false;
  var resumeTarget = null;

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

  function inputKey(input) {
    return lingvo + '|input|' + path + '|' + input.id;
  }

  function inputKeyById(inputId) {
    return lingvo + '|input|' + path + '|' + inputId;
  }

  function pageRecord() {
    return {
      key: lastPageKey(),
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

  function isInternalPageUrl(urlValue) {
    try {
      var url = new URL(urlValue, window.location.origin);
      var normalizedPath = normalizePath(url.pathname);
      return url.origin === window.location.origin
        && normalizedPath.indexOf('/' + lingvo + '/') === 0
        && normalizedPath.endsWith('/');
    } catch (error) {
      return false;
    }
  }

  function isSameDocumentUrl(urlValue) {
    try {
      var url = new URL(urlValue, window.location.origin);
      return url.origin === window.location.origin
        && normalizePath(url.pathname) === path
        && url.search === window.location.search;
    } catch (error) {
      return false;
    }
  }

  function savePageState() {
    if (inAppNavigationStarted) {
      return Promise.resolve();
    }

    return putRecord(PAGE_STORE, pageRecord()).catch(logStorageError);
  }

  function clearPageState() {
    return deleteRecord(PAGE_STORE, lastPageKey()).catch(logStorageError);
  }

  function schedulePageSave() {
    window.clearTimeout(scrollTimer);
    scrollTimer = window.setTimeout(savePageState, SCROLL_DEBOUNCE_MS);
  }

  function disableBrowserScrollRestoration() {
    if ('scrollRestoration' in window.history) {
      window.history.scrollRestoration = 'manual';
    }
  }

  function scrollToPosition(scrollY) {
    return new Promise(function (resolve) {
      window.requestAnimationFrame(function () {
        window.scrollTo(0, scrollY);
        resolve();
      });
    });
  }

  function inAppNavigationKey() {
    return IN_APP_NAVIGATION_PREFIX + lingvo;
  }

  function resumeTargetKey() {
    return RESUME_TARGET_PREFIX + lingvo;
  }

  function rememberInAppNavigation(urlValue) {
    var target = normalizedUrlKey(urlValue);
    if (!target) {
      return;
    }

    try {
      window.sessionStorage.setItem(inAppNavigationKey(), target);
    } catch (error) {
      logStorageError(error);
    }
  }

  function takeInAppNavigation() {
    try {
      var key = inAppNavigationKey();
      var target = window.sessionStorage.getItem(key);
      window.sessionStorage.removeItem(key);
      inAppNavigationTaken = target === currentUrlKey();
      return inAppNavigationTaken;
    } catch (error) {
      logStorageError(error);
      return false;
    }
  }

  function rememberResumeTarget(record) {
    try {
      window.sessionStorage.setItem(resumeTargetKey(), JSON.stringify({
        url: record.url,
        scrollY: record.scrollY || 0
      }));
    } catch (error) {
      logStorageError(error);
    }
  }

  function takeResumeTarget() {
    try {
      var key = resumeTargetKey();
      var serializedTarget = window.sessionStorage.getItem(key);
      window.sessionStorage.removeItem(key);
      if (!serializedTarget) {
        return null;
      }
      var target = JSON.parse(serializedTarget);
      if (target
        && normalizedUrlKey(target.url) === currentUrlKey()
        && typeof target.scrollY === 'number') {
        return target;
      }
    } catch (error) {
      logStorageError(error);
    }
    return null;
  }

  function applyInitialScrollPosition() {
    disableBrowserScrollRestoration();
    if (window.location.hash) {
      return Promise.resolve();
    }

    var target = resumeTarget || takeResumeTarget();
    if (target && target.scrollY > 0) {
      return scrollToPosition(target.scrollY);
    }

    return scrollToPosition(0);
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

  function bindInAppNavigation() {
    document.addEventListener('click', function (event) {
      if (event.defaultPrevented || event.button !== 0) {
        return;
      }
      if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) {
        return;
      }

      var link = event.target.closest && event.target.closest('a[href]');
      if (!link
        || link.hasAttribute('download')
        || (link.target && link.target !== '_self')) {
        return;
      }
      if (!isInternalPageUrl(link.href) || isSameDocumentUrl(link.href)) {
        return;
      }

      inAppNavigationStarted = true;
      rememberInAppNavigation(link.href);
      clearPageState();
    }, true);
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
    if (!isLanguageRoot() || window.location.hash) {
      return Promise.resolve(false);
    }
    if (inAppNavigationTaken || sameOriginReferrer()) {
      return Promise.resolve(false);
    }

    return readRecord(PAGE_STORE, lastPageKey()).then(function (record) {
      if (!record || !record.url || !isSafePageUrl(record.url)) {
        return false;
      }
      if (record.url === pageUrl()) {
        resumeTarget = record;
        return false;
      }

      rememberResumeTarget(record);
      window.location.replace(record.url);
      return true;
    }).catch(function (error) {
      logStorageError(error);
      return false;
    });
  }

  bindInAppNavigation();
  takeInAppNavigation();

  resumeLastPageIfNeeded().then(function (redirecting) {
    if (redirecting) {
      return;
    }

    bindInputPersistence();
    bindButtonFlushes();
    bindPagePersistence();
    restoreInputValues()
      .then(applyInitialScrollPosition)
      .then(savePageState)
      .catch(logStorageError);
  }).catch(logStorageError);
}());
