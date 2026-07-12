const { expect, test } = require('@playwright/test');

test('malsupra pagxilo havas apartigan linion', async ({ page }) => {
  await page.goto('/en/02/');

  await expect(page.locator('ul.pager')).toHaveCSS('border-top-style', 'solid');
});

test('helpo malfermigxas kiel ekstera ligilo', async ({ page }) => {
  await page.goto('/en/01/');

  const helpLink = page.locator('ul.pager .help a');
  await expect(helpLink).toHaveAttribute(
    'href',
    'https://www.google.com/search?hl=en&udm=50&aep=11&q=Estu+babilroboto+por+la+enhavo+de+responde+al+miaj+demandoj+pri+https%3A%2F%2Fesperanto12.net%2Fen%2Fllms-full.txt.+Skribu+bonvenigan+mesa%C4%9Don+por+tio+en+%5Ben%5D',
  );
  await expect(helpLink).toHaveAttribute('target', '_blank');
  await expect(helpLink).toHaveAttribute('rel', 'noopener');
  await expect(page.locator('ul.pager .comments a')).toHaveCount(0);
  await expect(page.locator('#disqus_thread')).toHaveCount(0);
  await expect(page.locator('script[src*="disqus.com/embed.js"]')).toHaveCount(0);
});

test('malsupra pagxilo uzas sagojn kun tradukitaj konsiletoj', async ({ page }) => {
  await page.goto('/en/02/');

  const pager = page.locator('ul.pager');
  await expect(pager.getByRole('link', { name: 'Back' })).toHaveText('◀︎');
  await expect(pager.getByRole('link', { name: 'Back' })).toHaveAttribute('title', 'back');
  await expect(pager.getByRole('link', { name: 'Forward' })).toHaveText('▶︎');
  await expect(pager.getByRole('link', { name: 'Forward' })).toHaveAttribute('title', 'forward');
});
