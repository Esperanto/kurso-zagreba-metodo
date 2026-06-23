const { expect, test } = require('@playwright/test');

test('ĉefpaĝo montras UEA-subtenon sen vortaro', async ({ page }) => {
  await page.goto('/');

  await expect(page.getByText('Subtenita de la Universala Esperanto Asocio')).toBeVisible();
  await expect(page.locator('#vortaro')).toHaveCount(0);
});

test('supra vortaro estas videbla kaj restas post rulumo', async ({ page }) => {
  await page.goto('/en/01/');

  const vortaro = page.locator('#vortaro');
  await expect(vortaro).toBeVisible();

  await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
  await expect(vortaro).toBeVisible();

  const box = await vortaro.boundingBox();
  expect(box.y).toBeLessThan(90);
});

test('poŝtelefona vortaro restas videbla sen malfermi menuon', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto('/en/01/');

  await expect(page.locator('#vortaro')).toBeVisible();
  await expect(page.locator('#site-navigation')).not.toBeVisible();

  await page.locator('#vortaro').fill('est');

  const suggestion = page.locator('.tt-menu .tt-suggestion').filter({
    hasText: 'esti',
  }).filter({
    hasText: 'to be',
  }).first();

  await expect(suggestion).toBeVisible();
});

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

test('ŝvebi super tekstaj vortoj montras tradukajn ŝprucfenestrojn', async ({ page }) => {
  await page.goto('/en/01/');

  await page.getByRole('heading', { name: /1\.\s*Amiko Marko/ })
    .getByText('Amiko')
    .hover();

  const popover = page.locator('.popover').filter({
    hasText: 'friend',
  }).filter({
    hasText: 'Noun',
  });

  await expect(popover).toBeVisible();

  await page.getByRole('link', { name: 'estas' }).first().hover();

  const verbPopover = page.locator('.popover').filter({
    hasText: 'to be',
  }).filter({
    hasText: 'Verb in present tense',
  });

  await expect(verbPopover).toBeVisible();
});
