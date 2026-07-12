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

  const languageButton = page.locator('.lingva-startpagxo-agoj .dropdown-toggle');
  await expect(languageButton).toContainText('🌐');
  await expect(languageButton).toContainText(/languages/);
  await languageButton.click();
  await expect(page.locator('.lingva-startpagxo-lingvoj').getByRole('link', { name: 'English' })).toBeVisible();

  const speakerLink = page.getByRole('link', { name: 'Find Esperanto speakers' });
  await expect(speakerLink).toHaveAttribute(
    'href',
    '/en/post',
  );
  await expect(page.locator('.lingva-startpagxo-parolantoj')).toHaveClass(/text-center/);
});
