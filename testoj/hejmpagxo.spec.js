const { expect, test } = require('@playwright/test');

async function readPwaRecord(page, key) {
  return page.evaluate((recordKey) => new Promise((resolve, reject) => {
    const request = window.indexedDB.open('esperanto12-pwa-state', 1);

    request.onupgradeneeded = () => {
      const db = request.result;
      if (!db.objectStoreNames.contains('pages')) {
        db.createObjectStore('pages', { keyPath: 'key' });
      }
      if (!db.objectStoreNames.contains('inputs')) {
        db.createObjectStore('inputs', { keyPath: 'key' });
      }
    };
    request.onerror = () => reject(request.error);
    request.onsuccess = () => {
      const db = request.result;
      const transaction = db.transaction('pages', 'readonly');
      const store = transaction.objectStore('pages');
      const getRequest = store.get(recordKey);

      getRequest.onerror = () => reject(getRequest.error);
      getRequest.onsuccess = () => {
        const record = getRequest.result;
        db.close();
        resolve(record || null);
      };
    };
  }), key);
}

async function readPwaLastUrl(page) {
  const record = await readPwaRecord(page, 'en|last');
  return record && record.url;
}

async function readPwaLastRecord(page) {
  return readPwaRecord(page, 'en|last');
}

async function emulateStandalonePwa(page) {
  await page.addInitScript(() => {
    const originalMatchMedia = window.matchMedia.bind(window);
    window.matchMedia = (query) => {
      if (query !== '(display-mode: standalone)') {
        return originalMatchMedia(query);
      }

      return {
        matches: true,
        media: query,
        onchange: null,
        addListener() {},
        removeListener() {},
        addEventListener() {},
        removeEventListener() {},
        dispatchEvent() {
          return false;
        },
      };
    };
  });
}

test('hejmpaĝo plusendas al la retumila lingvo', async ({ browser }) => {
  const context = await browser.newContext({ locale: 'de-DE' });
  await context.addInitScript(() => {
    Object.defineProperty(navigator, 'languages', { get: () => ['de-DE', 'en-US'] });
    Object.defineProperty(navigator, 'language', { get: () => 'de-DE' });
  });
  const page = await context.newPage();

  await page.goto('/');
  await expect(page).toHaveURL(/\/de\/$/);

  await context.close();
});

test('hejmpaĝo plusendas nekonatan lingvon al la angla', async ({ browser }) => {
  const context = await browser.newContext({ locale: 'zz-ZZ' });
  await context.addInitScript(() => {
    Object.defineProperty(navigator, 'languages', { get: () => ['zz-ZZ'] });
    Object.defineProperty(navigator, 'language', { get: () => 'zz-ZZ' });
  });
  const page = await context.newPage();

  await page.goto('/');
  await expect(page).toHaveURL(/\/en\/$/);

  await context.close();
});

test('hejmpaĝo signalas la lingvoversiojn al serĉiloj', async ({ page }) => {
  const response = await page.request.get('/');
  const html = await response.text();

  expect(html).toContain('Learn Esperanto');
  // La lingvoversioj estas signalitaj al serĉiloj per hreflang-alternativoj
  // en la kapo (la hejmpaĝo mem estas JS-lingvoelektilo kun plusendo).
  expect(html).toContain('rel="alternate" hreflang="en" href="https://esperanto12.net/en/"');
  expect(html).toContain('rel="alternate" hreflang="de" href="https://esperanto12.net/de/"');
  expect(html).toContain('rel="alternate" hreflang="no" href="https://esperanto12.net/no/"');
  expect(html).not.toContain('hejmo-subtitolo');
});

test('angla lingva startpaĝo montras kursan enkondukon', async ({ page }) => {
  await page.goto('/en/');

  await expect(page.locator('.lingva-startpagxo-logo')).toHaveAttribute(
    'src',
    '/assets/img/logo/logo-256.png',
  );
  await expect(page.getByRole('heading', { name: 'Learn Esperanto in 12 Hours' })).toBeVisible();
  await expect(page.getByText('The Fastest Basics Course')).toBeVisible();
  await expect(page.getByText('Learn the 500 most important words')).toBeVisible();
  await expect(page.getByText('Understand 95 % of spoken Esperanto')).toBeVisible();
  await expect(page.getByText('Free and no sign-up')).toBeVisible();
  await expect(page.getByText('follow simple conversations')).toBeVisible();
  await expect(page.getByRole('link', { name: 'next Esperanto meetup' })).toHaveAttribute(
    'href',
    'https://eventaservo.org/',
  );
  await expect(page.getByRole('link', { name: 'Start' })).toHaveAttribute('href', '/en/01');
  const installButton = page.locator('[data-pwa-install]');
  await expect(installButton).toHaveText('Install app');
  await expect(installButton).toHaveClass(/btn-outline-primary/);
  await expect(installButton).toBeHidden();

  const languageButton = page.locator('.lingva-startpagxo-titoloj .dropdown-toggle');
  await expect(languageButton).toContainText('🌐');
  await expect(languageButton).toContainText(/languages/);
  await expect(languageButton).toHaveClass(/btn-outline-secondary/);
  await languageButton.click();
  await expect(page.locator('.lingva-startpagxo-lingvoj').getByRole('link', { name: 'English (en)' })).toBeVisible();

  const speakerLink = page.getByRole('link', { name: 'Find Esperanto speakers' });
  await expect(speakerLink).toHaveAttribute(
    'href',
    '/en/post',
  );
  await expect(page.locator('.lingva-startpagxo-parolantoj')).toHaveClass(/text-center/);
});

test('norvega beta-startpaĝo montras AI-averton', async ({ page }) => {
  await page.goto('/no/');

  const warning = page.locator('.lingva-startpagxo-beta-averto');
  await expect(page.getByRole('heading', { name: 'Lær esperanto på 12 timer' })).toBeVisible();
  await expect(warning).toBeVisible();
  await expect(warning.locator('.lingva-startpagxo-beta-averto-ikono')).toHaveText('⚠️');
  await expect(warning).toContainText('Dette språket er oversatt med KI.');
  const warningLink = warning.getByRole('link', { name: 'gi oss gjerne beskjed' });
  await expect(warningLink).toHaveAttribute('href', 'https://demandilo.typeform.com/to/wJxiycNC');
  await expect(warningLink).toHaveAttribute('target', '_blank');
  await expect(warningLink).toHaveAttribute('rel', 'noopener');

  const languageButton = page.locator('.lingva-startpagxo-titoloj .dropdown-toggle');
  await languageButton.click();
  await expect(page.locator('.lingva-startpagxo-lingvoj').getByRole('link', { name: 'Norsk (no)' })).toBeVisible();

  await page.goto('/no/01/');
  const navbarLanguageButton = page.locator('.navbar-lingvoelektilo .dropdown-toggle');
  await navbarLanguageButton.click();
  const navbarLanguages = page.locator('.navbar-lingvoj');
  await expect(navbarLanguages.getByRole('link', { name: 'Norsk (no)' })).toBeVisible();
  await expect(navbarLanguages).not.toContainText('test: norvega (no)');
});

test('tagaloga beta-startpaĝo montras AI-averton sub parolanta butono', async ({ page }) => {
  await page.goto('/tl/');

  const speakerButton = page.locator('.lingva-startpagxo-parolantoj');
  const warning = page.locator('.lingva-startpagxo-beta-averto');
  await expect(speakerButton).toBeVisible();
  await expect(warning).toBeVisible();
  await expect(warning.locator('.lingva-startpagxo-beta-averto-teksto > p')).toBeVisible();
  await expect(warning.locator('p > .lingva-startpagxo-beta-averto-ikono')).toHaveText('⚠️');
  await expect(warning).toContainText('Ang wikang ito ay isinalin ng AI.');
  const warningLink = warning.getByRole('link', { name: 'pakisabi sa amin' });
  await expect(warningLink).toHaveAttribute('href', 'https://demandilo.typeform.com/to/wJxiycNC');
  await expect(warningLink).toHaveAttribute('target', '_blank');
  await expect(warningLink).toHaveAttribute('rel', 'noopener');

  const followsSpeakerButton = await page.evaluate(() => {
    const speaker = document.querySelector('.lingva-startpagxo-parolantoj');
    const warning = document.querySelector('.lingva-startpagxo-beta-averto');
    return Boolean(speaker && warning && speaker.compareDocumentPosition(warning) & Node.DOCUMENT_POSITION_FOLLOWING);
  });
  expect(followsSpeakerButton).toBe(true);

  const speakerBox = await speakerButton.boundingBox();
  const warningBox = await warning.boundingBox();
  expect(speakerBox).not.toBeNull();
  expect(warningBox).not.toBeNull();
  expect(warningBox.y).toBeGreaterThanOrEqual(speakerBox.y + speakerBox.height - 1);
});

test('startpaĝa instalbutono malfermas la PWA-inviton', async ({ page }) => {
  await page.goto('/en/');

  await page.evaluate(() => {
    window.__pwaPromptCalls = 0;
    const event = new Event('beforeinstallprompt', { cancelable: true });
    event.prompt = () => {
      window.__pwaPromptCalls += 1;
      return Promise.resolve();
    };
    event.userChoice = Promise.resolve({ outcome: 'accepted', platform: 'web' });
    window.dispatchEvent(event);
  });

  const installButton = page.locator('[data-pwa-install]');
  await expect(installButton).toBeVisible();
  await installButton.click();
  await expect.poll(() => page.evaluate(() => window.__pwaPromptCalls)).toBe(1);
  await expect(installButton).toBeHidden();
});

test('startpaĝa instalbutono helpas sen beforeinstallprompt', async ({ page }) => {
  await page.addInitScript(() => {
    delete window.onbeforeinstallprompt;
  });

  await page.goto('/en/');

  const installButton = page.locator('[data-pwa-install]');
  const installHelp = page.locator('[data-pwa-install-help]');
  await expect(installButton).toBeVisible();
  await expect(installButton).toHaveAttribute('aria-expanded', 'false');
  await expect(installHelp).toBeHidden();

  await installButton.click();
  await expect(installButton).toHaveAttribute('aria-expanded', 'true');
  await expect(installHelp).toBeVisible();
  await expect(installHelp).toHaveCSS('animation-name', 'pwa-instala-helpo-aufsxovo');
  await expect(installHelp).toHaveText(
    'Open the browser menu and choose "Install" or "Add to Home screen".',
  );
});

test('PWA-logoligilo iras al startpaĝo anstataŭ rekomenci konservitan paĝon', async ({ page }) => {
  await emulateStandalonePwa(page);
  await page.setViewportSize({ width: 390, height: 667 });

  await page.goto('/en/');
  await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
  await expect.poll(() => page.evaluate(() => window.scrollY)).toBeGreaterThan(100);
  await expect.poll(async () => {
    const record = await readPwaLastRecord(page);
    return record && record.url === '/en/' && record.scrollY;
  }).toBeGreaterThan(100);
  await expect.poll(() => readPwaRecord(page, 'en|page|/en/')).toBe(null);

  await page.goto('/en/06/gramatiko/');

  await expect.poll(() => readPwaLastUrl(page)).toBe('/en/06/gramatiko/');

  const logoLink = page.locator('.navbar-brand');
  await expect(logoLink).toHaveAttribute('data-pwa-root-link', '');
  await logoLink.evaluate((link) => link.setAttribute('rel', 'noreferrer'));
  await logoLink.click();

  await expect(page).toHaveURL(/\/en\/$/);
  await page.waitForTimeout(600);
  await expect(page).toHaveURL(/\/en\/$/);
  await expect.poll(() => page.evaluate(() => window.scrollY)).toBe(0);
});

test('PWA ekstera remalfermo rekomencas lastan paĝon kaj rulpozicion', async ({ page }) => {
  await emulateStandalonePwa(page);
  await page.setViewportSize({ width: 390, height: 667 });
  await page.goto('/en/06/gramatiko/');

  await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
  await expect.poll(() => page.evaluate(() => window.scrollY)).toBeGreaterThan(100);
  await expect.poll(async () => {
    const record = await readPwaLastRecord(page);
    return record && record.url === '/en/06/gramatiko/' && record.scrollY;
  }).toBeGreaterThan(100);
  await expect.poll(() => readPwaRecord(page, 'en|page|/en/06/gramatiko/')).toBe(null);

  const reopenedPage = await page.context().newPage();
  await emulateStandalonePwa(reopenedPage);
  await reopenedPage.goto('/en/');

  await expect(reopenedPage).toHaveURL(/\/en\/06\/gramatiko\/$/);
  await expect.poll(() => reopenedPage.evaluate(() => window.scrollY)).toBeGreaterThan(100);
  await reopenedPage.close();
});

test('startpaĝa lingvoelektilo vicigxas kun la titoloj', async ({ page }) => {
  await page.goto('/en/');

  const logo = page.locator('.lingva-startpagxo-logo');
  const title = page.getByRole('heading', { name: 'Learn Esperanto in 12 Hours' });
  const languageButton = page.locator('.lingva-startpagxo-titoloj .dropdown-toggle');

  const logoBox = await logo.boundingBox();
  const titleBox = await title.boundingBox();
  const desktopButtonBox = await languageButton.boundingBox();

  expect(Math.abs(desktopButtonBox.x - titleBox.x)).toBeLessThan(1);
  expect(desktopButtonBox.x).toBeGreaterThan(logoBox.x + logoBox.width);

  await page.setViewportSize({ width: 375, height: 667 });
  await page.goto('/en/');
  const mobileTitleBox = await title.boundingBox();
  const mobileButtonBox = await languageButton.boundingBox();

  const mobileTitleCenter = mobileTitleBox.x + mobileTitleBox.width / 2;
  const mobileButtonCenter = mobileButtonBox.x + mobileButtonBox.width / 2;
  expect(Math.abs(mobileButtonCenter - mobileTitleCenter)).toBeLessThan(1);
});
