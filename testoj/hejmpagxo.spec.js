const { expect, test } = require('@playwright/test');

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
  expect(html).not.toContain('hejmo-subtitolo');
});

test('angla lingva startpaĝo montras kursan enkondukon', async ({ page }) => {
  await page.goto('/en/');

  await expect(page.locator('.lingva-startpagxo-logo')).toHaveAttribute(
    'src',
    '/assets/img/logo/logo-256.png',
  );
  await expect(page.getByRole('heading', { name: 'Learn Esperanto in 12 Lessons' })).toBeVisible();
  await expect(page.getByText('The Fastest Basics Course')).toBeVisible();
  await expect(page.getByText('most important 500 words')).toBeVisible();
  await expect(page.getByText('without registration')).toBeVisible();
  await expect(page.getByRole('link', { name: 'flashcard deck' })).toHaveAttribute(
    'href',
    '/en/eksporto/en.apkg',
  );
  await expect(page.getByRole('link', { name: 'Anki' })).toHaveAttribute(
    'href',
    'https://apps.ankiweb.net/',
  );
  await expect(page.getByRole('link', { name: 'Anki' })).toHaveAttribute('target', '_blank');
  await expect(page.getByRole('link', { name: 'Anki' })).toHaveAttribute('rel', 'noopener');
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
  await expect(page.locator('.lingva-startpagxo-lingvoj').getByRole('link', { name: 'English' })).toBeVisible();

  const speakerLink = page.getByRole('link', { name: 'Find Esperanto speakers' });
  await expect(speakerLink).toHaveAttribute(
    'href',
    '/en/post',
  );
  await expect(page.locator('.lingva-startpagxo-parolantoj')).toHaveClass(/text-center/);
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

test('startpaĝa instalbutono helpas en Firefox por Android', async ({ browser }) => {
  const context = await browser.newContext({
    userAgent: 'Mozilla/5.0 (Android 14; Mobile; rv:144.0) Gecko/144.0 Firefox/144.0',
  });
  const page = await context.newPage();

  await page.goto('/en/');

  const installButton = page.locator('[data-pwa-install]');
  await expect(installButton).toBeVisible();

  const dialogPromise = page.waitForEvent('dialog');
  const clickPromise = installButton.click();
  const dialog = await dialogPromise;
  expect(dialog.message()).toContain('Firefox cannot open the install prompt directly.');
  expect(dialog.message()).toContain('Add to Home screen');
  await dialog.accept();
  await clickPromise;

  await context.close();
});

test('startpaĝa lingvoelektilo vicigxas kun la titoloj', async ({ page }) => {
  await page.goto('/en/');

  const logo = page.locator('.lingva-startpagxo-logo');
  const title = page.getByRole('heading', { name: 'Learn Esperanto in 12 Lessons' });
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
