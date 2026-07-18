const { expect, test } = require('@playwright/test');

test('vortaro montras tradukon dum tajpado', async ({ page }) => {
  await page.goto('/en/01/');

  await page.locator('#vortaro').fill('est');

  const suggestion = page.locator('.tt-menu .tt-suggestion').filter({
    hasText: 'esti',
  }).filter({
    hasText: 'to be',
  }).first();

  await expect(suggestion).toBeVisible();
});

test('vortaro restas kompakta en la supra navigilo', async ({ page }) => {
  await page.goto('/en/01/');

  const dictionaryBox = await page.locator('#vortaro').boundingBox();
  expect(dictionaryBox.width).toBeLessThanOrEqual(170);
});

test('poŝtelefone vortaro restas inter logo kaj cxiamaj butonoj en unu linio', async ({ page }) => {
  for (const width of [320, 360, 390]) {
    await page.setViewportSize({ width, height: 720 });
    await page.goto('/en/01/');

    const dictionary = page.locator('#vortaro');
    await expect(dictionary).toBeVisible();
    await expect(page.getByRole('button', { name: 'Toggle navigation' })).toHaveCount(0);
    await expect(page.locator('.navbar-brand')).toHaveAttribute('href', '/en/');

    const logoBox = await page.locator('.navbar-brand').boundingBox();
    const dictionaryBox = await dictionary.boundingBox();
    const languageBox = await page.getByRole('button', { name: 'Elekti alian lingvon' }).boundingBox();
    const navbarBox = await page.locator('.navbar').boundingBox();

    expect(dictionaryBox.x).toBeGreaterThan(logoBox.x + logoBox.width - 1);
    expect(dictionaryBox.x + dictionaryBox.width).toBeLessThan(languageBox.x + 1);
    expect(languageBox.x + languageBox.width).toBeLessThanOrEqual(width);
    expect(Math.abs((dictionaryBox.y + dictionaryBox.height / 2) - (logoBox.y + logoBox.height / 2))).toBeLessThan(3);
    expect(Math.abs((dictionaryBox.y + dictionaryBox.height / 2) - (languageBox.y + languageBox.height / 2))).toBeLessThan(3);
    expect(navbarBox.height).toBeLessThan(60);
  }

  await page.locator('#vortaro').fill('est');

  const suggestion = page.locator('.tt-menu .tt-suggestion').filter({
    hasText: 'esti',
  }).filter({
    hasText: 'to be',
  }).first();

  await expect(suggestion).toBeVisible();
});
