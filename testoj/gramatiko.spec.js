const { expect, test } = require('@playwright/test');

test('gramatika enhavtabelo aperas dekstre sur labortablo', async ({ page }) => {
  await page.setViewportSize({ width: 1024, height: 720 });
  await page.goto('/en/01/gramatiko/');

  const toc = page.locator('.gramatika-enhavtabelo');
  await expect(toc).toBeVisible();
  await expect(toc.getByRole('link', { name: 'Alphabet' })).toHaveAttribute('href', '#alphabet');
  await expect(toc.getByRole('link', { name: 'Pronunciation' })).toHaveAttribute('href', '#pronunciation');
  await expect(toc.getByRole('link', { name: 'Ĉu?' })).toBeVisible();
  await expect(toc).not.toContainText('*Ĉu?*');
  await expect(page.locator('h3#alphabet')).toHaveText('Alphabet');
  await expect(page.locator('.gramatika-reenligo')).toHaveCount(0);
  await expect(toc).toHaveCSS('position', 'sticky');

  const boxes = await page.evaluate(() => {
    const content = document.querySelector('main .col-sm-12').getBoundingClientRect();
    const tocBox = document.querySelector('.gramatika-enhavtabelo').getBoundingClientRect();
    return {
      contentLeft: content.left,
      contentRight: content.right,
      tocLeft: tocBox.left,
      tocRight: tocBox.right,
    };
  });

  expect(boxes.tocLeft).toBeGreaterThan(boxes.contentLeft + 0.5 * (boxes.contentRight - boxes.contentLeft));
  expect(boxes.tocRight).toBeLessThanOrEqual(boxes.contentRight + 1);

  const desktopItems = await page.locator('.gramatika-enhavtabelo li').evaluateAll((items) => {
    return items.slice(0, 2).map((item) => {
      const box = item.getBoundingClientRect();
      return {
        display: getComputedStyle(item).display,
        y: box.y,
      };
    });
  });

  expect(desktopItems[0].display).toBe('list-item');
  expect(desktopItems[1].display).toBe('list-item');
  expect(desktopItems[1].y).toBeGreaterThan(desktopItems[0].y + 8);
});

test('gramatika enhavtabelo restas horizontala sur poŝtelefono', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 720 });
  await page.goto('/en/01/gramatiko/');

  const first = page.locator('.gramatika-enhavtabelo li').first();
  const second = page.locator('.gramatika-enhavtabelo li').nth(1);
  const boxes = await Promise.all([
    first.boundingBox(),
    second.boundingBox(),
  ]);

  expect(Math.abs(boxes[0].y - boxes[1].y)).toBeLessThan(8);
  expect(boxes[1].x).toBeGreaterThan(boxes[0].x);
  await expect(first).toHaveCSS('display', 'list-item');
});
