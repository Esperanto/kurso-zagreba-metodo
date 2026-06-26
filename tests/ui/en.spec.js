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

test('poŝtelefona aldona menuo restas malhela', async ({ page }) => {
  await page.setViewportSize({ width: 580, height: 720 });
  await page.goto('/en/01/');

  await page.getByRole('button', { name: 'Toggle navigation' }).click();
  await page.getByRole('button', { name: 'Appendix' }).click();

  const menu = page.locator('.dropdown-menu.show').filter({
    hasText: 'Correlatives',
  });
  await expect(menu).toBeVisible();
  await expect(menu).toHaveCSS('background-color', 'rgb(34, 34, 34)');
});

test('lecionaj langetoj montras ikonojn kun etikedoj sur labortablo', async ({ page }) => {
  await page.goto('/en/01/');

  const tabs = page.locator('.nav-tabs');

  await expect(tabs.getByRole('link', { name: 'Text' })).toContainText('📖');
  await expect(tabs.getByRole('link', { name: 'New words' })).toContainText('🗂️');
  await expect(tabs.getByRole('link', { name: 'Grammar' })).toContainText('🧩');
  await expect(tabs.getByRole('link', { name: 'Exercise 1' })).toContainText('1️⃣');
  await expect(tabs.getByRole('link', { name: 'Exercise 2' })).toContainText('2️⃣');
  await expect(tabs.getByRole('link', { name: 'Exercise 3' })).toContainText('3️⃣');
});

test('poŝtelefone nur aktiva leciona langeto montras etikedon', async ({ page }) => {
  await page.setViewportSize({ width: 580, height: 720 });
  await page.goto('/en/01/gramatiko/');

  const textTab = page.getByRole('link', { name: 'Text' });
  const grammarTab = page.getByRole('link', { name: 'Grammar' });

  await expect(textTab.locator('.tab-icon')).toBeVisible();
  await expect(textTab.locator('.tab-label')).toBeHidden();
  await expect(grammarTab.locator('.tab-icon')).toBeVisible();
  await expect(grammarTab.locator('.tab-label')).toBeVisible();
  await expect(grammarTab).toContainText('🧩');
  await expect(grammarTab).toContainText('Grammar');
});

test('aktiva leciona langeto havas kampecan fonon', async ({ page }) => {
  await page.goto('/en/01/ekzerco3/');

  await expect(page.getByRole('link', { name: 'Exercise 3' })).toHaveCSS(
    'background-color',
    'rgb(240, 240, 240)',
  );
});

test('poŝtelefonaj lecionaj langetoj restas en unu vico kaj alteco', async ({ page }) => {
  await page.setViewportSize({ width: 360, height: 720 });

  const activeTabs = [
    '/en/01/vortoj/',
    '/en/01/ekzerco1/',
    '/en/01/ekzerco2/',
    '/en/01/ekzerco3/',
  ];

  for (const path of activeTabs) {
    await page.goto(path);

    const rowCount = await page.locator('.nav-tabs .nav-item').evaluateAll((items) => {
      const tops = items.map((item) => Math.round(item.getBoundingClientRect().top));
      return new Set(tops).size;
    });

    await expect(rowCount).toBe(1);

    const centerSpread = await page.locator('.nav-tabs .nav-link').evaluateAll((links) => {
      const centers = links.map((link) => {
        const box = link.getBoundingClientRect();
        return Math.round(box.top + box.height / 2);
      });
      return Math.max(...centers) - Math.min(...centers);
    });

    await expect(centerSpread).toBeLessThanOrEqual(1);
  }
});

test('ekzercaj dupunktoj vicigxas dekstre', async ({ page }) => {
  await page.setViewportSize({ width: 580, height: 720 });

  for (const path of ['/en/06/ekzerco1/', '/en/06/ekzerco3/']) {
    await page.goto(path);

    const labelEdgeSpread = await page.locator('.form-horizontal .form-group.has-feedback .control-label')
      .evaluateAll((labels) => {
        const rights = labels.map((label) => Math.round(label.getBoundingClientRect().right));
        return Math.max(...rights) - Math.min(...rights);
      });

    await expect(labelEdgeSpread).toBeLessThanOrEqual(1);
  }
});

test('ekzercaj tekstkampoj sekvas la size-valoron', async ({ page }) => {
  for (const path of ['/en/06/ekzerco1/', '/en/06/ekzerco3/']) {
    await page.goto(path);

    const sizeOffsets = await page.locator('.form-horizontal input[type="text"]')
      .evaluateAll((inputs) => inputs.map((input) => {
        const firstAnswer = input.dataset.solvo.split(' | ')[0];
        return Number(input.getAttribute('size')) - firstAnswer.length;
      }));

    await expect(sizeOffsets.every((offset) => offset === 2)).toBe(true);
  }
});

test('ekzercaj respondaj ikonoj restas en la kampoj', async ({ page }) => {
  for (const path of ['/en/06/ekzerco1/', '/en/06/ekzerco3/']) {
    await page.goto(path);

    const iconPositions = await page.locator('.form-horizontal .col-sm-10')
      .evaluateAll((cells) => cells.map((cell) => {
        const input = cell.querySelector('input[type="text"]');
        const icon = cell.querySelector('.feedback-icon');
        const inputBox = input.getBoundingClientRect();
        const iconBox = icon.getBoundingClientRect();

        return {
          insideInput: iconBox.left >= inputBox.left && iconBox.right <= inputBox.right,
          rightGap: Math.round(inputBox.right - iconBox.right),
        };
      }));

    await expect(iconPositions.every(({ insideInput }) => insideInput)).toBe(true);
    await expect(iconPositions.every(({ rightGap }) => rightGap >= 5 && rightGap <= 25)).toBe(true);
  }
});
