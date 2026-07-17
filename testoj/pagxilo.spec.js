const { expect, test } = require('@playwright/test');

test('malsupra pagxilo havas apartigan linion', async ({ page }) => {
  await page.goto('/en/02/');

  await expect(page.locator('ul.pager')).toHaveCSS('border-top-style', 'solid');
});

test('helpo kaj komentejo malfermigxas kiel eksteraj ligiloj', async ({ page }) => {
  await page.goto('/en/01/');

  const helpLink = page.locator('ul.pager a.help');
  await expect(helpLink).toHaveAttribute(
    'href',
    'https://www.google.com/search?hl=en&udm=50&aep=11&q=Estu+babilroboto+por+la+enhavo+de+responde+al+miaj+demandoj+pri+https%3A%2F%2Fesperanto12.net%2Fen%2Fllms-full.txt.+Skribu+bonvenigan+mesa%C4%9Don+por+tio+en+%5Ben%5D',
  );
  await expect(helpLink).toHaveAttribute('target', '_blank');
  await expect(helpLink).toHaveAttribute('rel', 'noopener');
  const commentsLink = page.locator('ul.pager a.comments');
  await expect(commentsLink).toHaveAttribute(
    'href',
    'https://github.com/Esperanto/kurso-zagreba-metodo/discussions/categories/en',
  );
  await expect(commentsLink).toHaveAttribute('target', '_blank');
  await expect(commentsLink).toHaveAttribute('rel', 'noopener');
  const helpBox = await helpLink.boundingBox();
  const commentsBox = await commentsLink.boundingBox();
  expect(helpBox).not.toBeNull();
  expect(commentsBox).not.toBeNull();
  expect(commentsBox.x).toBeGreaterThan(helpBox.x);
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
