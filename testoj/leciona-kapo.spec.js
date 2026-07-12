const { expect, test } = require('@playwright/test');

test('aldona kaj lingva menuoj restas cxiam atingeblaj', async ({ page }) => {
  await page.setViewportSize({ width: 580, height: 720 });
  await page.goto('/en/01/');

  // La apendico estas atingebla kiel «13a leciono» el la lecionmenuo.
  await page.getByRole('button', { name: /1\./ }).click();
  const lessonMenu = page.locator('.leciona-menuo-listo.show');
  await expect(lessonMenu).toBeVisible();
  await expect(lessonMenu.getByRole('link', { name: 'Appendix' })).toHaveAttribute(
    'href',
    '/en/tabelvortoj',
  );

  await page.getByRole('button', { name: /1\./ }).click();
  await page.getByRole('button', { name: 'Elekti alian lingvon' }).click();
  const languageMenu = page.locator('.dropdown-menu.show').filter({
    hasText: 'Deutsch',
  });
  await expect(languageMenu).toBeVisible();
  await expect(languageMenu.getByRole('link', { name: 'Deutsch' })).toHaveAttribute('href', '/de/');
});

test('navigilo restas supre dum rulumado', async ({ page }) => {
  await page.goto('/en/01/');

  await page.evaluate(() => window.scrollTo(0, 700));
  await expect.poll(() => page.evaluate(() => window.scrollY)).toBeGreaterThan(0);

  const navbarBox = await page.locator('.navbar').boundingBox();
  expect(navbarBox.y).toBe(0);
});

test('leciona titolo malfermas lecionliston', async ({ page }) => {
  await page.goto('/en/01/');

  await expect(page.getByRole('link', { name: 'Lessons' })).toHaveCount(0);

  const lessonButton = page.getByRole('button', { name: /1\./ });
  await expect(lessonButton).toBeVisible();
  await expect(lessonButton).toHaveClass(/btn-light/);
  await expect(lessonButton).toHaveClass(/dropdown-toggle/);
  await expect(lessonButton).toHaveCSS('background-color', 'rgb(255, 255, 255)');
  await lessonButton.click();

  const lessonMenu = page.locator('.leciona-menuo-listo.show');
  await expect(lessonMenu.getByRole('link', { name: /^1\.\s*Amiko Marko/ })).toHaveAttribute('href', '/en/01');
  await expect(lessonMenu.getByRole('link', { name: /^12\./ })).toHaveAttribute('href', '/en/12');
});

test('lecionaj sagoj estas apud centrita titolo', async ({ page }) => {
  await page.goto('/en/01/');

  const header = page.locator('.leciona-kapo');
  await expect(header.getByRole('link', { name: 'Forward' })).toHaveText('▶︎');
  await expect(header.getByRole('link', { name: 'Forward' })).toHaveAttribute('title', 'forward');
  await expect(header.getByRole('link', { name: 'Back' })).toHaveCount(0);

  const metrics = await header.evaluate((row) => {
    const title = row.querySelector('.leciona-titolo').getBoundingClientRect();
    const next = row.querySelector('.leciona-sago-sekva .btn').getBoundingClientRect();
    const rowBox = row.getBoundingClientRect();

    return {
      nextCenterSpread: Math.abs((next.top + next.height / 2) - (title.top + title.height / 2)),
      nextRightSpread: Math.abs(rowBox.right - next.right),
      titleCenterSpread: Math.abs((title.left + title.width / 2) - (rowBox.left + rowBox.width / 2)),
    };
  });

  expect(metrics.nextCenterSpread).toBeLessThanOrEqual(2);
  expect(metrics.nextRightSpread).toBeLessThanOrEqual(2);
  expect(metrics.titleCenterSpread).toBeLessThanOrEqual(2);

  await page.goto('/en/02/');
  const secondHeader = page.locator('.leciona-kapo');
  await expect(secondHeader.getByRole('link', { name: 'Back' })).toHaveText('◀︎');
  await expect(secondHeader.getByRole('link', { name: 'Back' })).toHaveAttribute('title', 'back');
  await expect(secondHeader.getByRole('link', { name: 'Forward' })).toHaveText('▶︎');
  await expect(secondHeader.getByRole('link', { name: 'Forward' })).toHaveAttribute('title', 'forward');

  const edgeMetrics = await secondHeader.evaluate((row) => {
    const previous = row.querySelector('.leciona-sago-antauxa .btn').getBoundingClientRect();
    const next = row.querySelector('.leciona-sago-sekva .btn').getBoundingClientRect();
    const rowBox = row.getBoundingClientRect();

    return {
      previousLeftSpread: Math.abs(previous.left - rowBox.left),
      nextRightSpread: Math.abs(rowBox.right - next.right),
    };
  });

  expect(edgeMetrics.previousLeftSpread).toBeLessThanOrEqual(2);
  expect(edgeMetrics.nextRightSpread).toBeLessThanOrEqual(2);
});

test('leciona titolo ne falas sub la butonon dum linisalto', async ({ page }) => {
  await page.setViewportSize({ width: 260, height: 720 });
  await page.goto('/en/09/');

  const titleMetrics = await page.locator('.leciona-titolo').evaluate((heading) => {
    const menuBox = heading.querySelector('.leciona-menuo').getBoundingClientRect();
    const textBox = heading.querySelector('.leciona-titolo-teksto').getBoundingClientRect();
    const wordBoxes = [...heading.querySelectorAll('.leciona-titolo-teksto > a')]
      .map((word) => word.getBoundingClientRect());
    const wordRows = new Set(wordBoxes.map((box) => Math.round(box.top))).size;

    return {
      centerSpread: Math.abs((menuBox.top + menuBox.height / 2) - (textBox.top + textBox.height / 2)),
      leftSpread: Math.min(...wordBoxes.map((box) => box.left)) - textBox.left,
      menuRight: menuBox.right,
      textLeft: textBox.left,
      wordRows,
    };
  });

  expect(titleMetrics.centerSpread).toBeLessThanOrEqual(2);
  expect(titleMetrics.textLeft).toBeGreaterThan(titleMetrics.menuRight);
  expect(titleMetrics.leftSpread).toBeGreaterThanOrEqual(-1);
  expect(titleMetrics.wordRows).toBeGreaterThan(1);
});
