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

test('ŝvebi super teksta vorto montras tradukan ŝprucfenestron', async ({ page }) => {
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
});
