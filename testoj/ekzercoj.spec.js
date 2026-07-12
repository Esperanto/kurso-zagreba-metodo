const { expect, test } = require('@playwright/test');

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

    await expect(sizeOffsets.every((offset) => offset === 1)).toBe(true);
  }
});

test('ekzerco 2 uzas Bootstrap-validigon ene de enigogrupoj', async ({ page }) => {
  await page.goto('/en/01/ekzerco2/');

  await expect(page.locator('.ekzerco2-tasko input[type="button"].ekz2-fiksa-vorto')).toHaveCount(0);
  await expect(page.locator('.ekzerco2-tasko input[type="text"].ekz2-fiksa-vorto')).toHaveCount(0);
  await expect(page.locator('.ekzerco2-tasko .input-group:not(:has(input.form-control)) > .input-group-text').first()).toBeVisible();

  const inputGroup = page.locator('.ekzerco2-tasko .input-group:has(input.form-control)').first();
  await expect(inputGroup.locator('.feedback-icon')).toHaveCount(0);
  await expect(inputGroup.locator('input.form-control')).toHaveClass(/is-invalid/);

  const groupEdges = await inputGroup.evaluate((group) => {
    const parts = [...group.children].map((part) => part.getBoundingClientRect());
    return parts.slice(1).every((part, index) => {
      const previous = parts[index];
      return Math.abs(previous.right - part.left) <= 1;
    });
  });

  await expect(groupEdges).toBe(true);

  const heightSpread = await page.locator('.ekzerco2-tasko .input-group, .ekzerco2-tasko .form-group')
    .evaluateAll((items) => {
      const heights = items.slice(0, 8).map((item) => Math.round(item.getBoundingClientRect().height));
      return Math.max(...heights) - Math.min(...heights);
    });
  await expect(heightSpread).toBeLessThanOrEqual(2);

  const punctuationGap = await page.locator('.ekzerco2-tasko .ekz2-interpunkcio').first()
    .evaluate((punctuation) => {
      const previous = punctuation.previousElementSibling;
      return Math.round(punctuation.getBoundingClientRect().left - previous.getBoundingClientRect().right);
    });
  await expect(punctuationGap).toBeGreaterThanOrEqual(4);
});

test('ekzercaj respondaj kampoj montras validigan retrosignon', async ({ page }) => {
  for (const path of ['/en/06/ekzerco1/', '/en/06/ekzerco3/']) {
    await page.goto(path);

    const inputs = page.locator('.form-horizontal input[data-solvo]');
    // Komence ĉiu kampo estas markita kiel nevalida (Bootstrap-5-validigo).
    await expect(inputs.first()).toHaveClass(/is-invalid/);

    // «Solvu» plenigas ĉiun kampon per ĝia solvo → is-valid.
    const solveButtons = page.locator('.solvu');
    const buttonCount = await solveButtons.count();
    for (let i = 0; i < buttonCount; i += 1) {
      await solveButtons.nth(i).click();
    }

    const inputCount = await inputs.count();
    for (let i = 0; i < inputCount; i += 1) {
      await expect(inputs.nth(i)).toHaveClass(/is-valid/);
    }
  }
});

test('gxuste-sono ludas unufoje kiam respondo farigxas gxusta per tajpado', async ({ page }) => {
  await page.addInitScript(() => {
    window.__gxustePlayCalls = [];
    HTMLMediaElement.prototype.play = function() {
      window.__gxustePlayCalls.push({
        sources: Array.from(this.querySelectorAll('source')).map((source) => ({
          src: source.getAttribute('src'),
          type: source.getAttribute('type'),
        })),
      });
      return Promise.resolve();
    };
  });

  await page.goto('/en/06/ekzerco1/');

  const input = page.locator('.form-horizontal input[data-solvo]').first();
  const solvo = await input.getAttribute('data-solvo');
  const unuaSolvo = solvo.split(/\s*\|\s*/)[0];

  await input.focus();
  await page.keyboard.type(unuaSolvo);

  await expect(input).toHaveClass(/is-valid/);
  await expect.poll(
    () => page.evaluate(() => window.__gxustePlayCalls),
  ).toEqual([
    {
      sources: [
        { src: '/assets/ogg/gxuste.ogg', type: 'audio/ogg' },
        { src: '/assets/mp3/gxuste.mp3', type: 'audio/mpeg' },
      ],
    },
  ]);

  await page.locator('.solvu').click();
  await expect.poll(
    () => page.evaluate(() => window.__gxustePlayCalls.length),
  ).toBe(1);
});

test('ekzercaj titoloj montras nur la celan lingvon', async ({ page }) => {
  await page.goto('/en/01/ekzerco1/');
  await expect(page.getByRole('heading', { level: 3, name: 'Translate' })).toBeVisible();
  await expect(page.getByRole('heading', { level: 3, name: /Translate \// })).toHaveCount(0);

  await page.goto('/en/01/ekzerco2/');
  await expect(page.getByRole('heading', { level: 3, name: 'Complete the sentences' })).toBeVisible();
  await expect(page.getByRole('heading', { level: 3, name: /Complete the sentences \// })).toHaveCount(0);

  await page.goto('/en/01/ekzerco3/');
  await expect(page.getByRole('heading', { level: 3, name: 'Translate and answer' })).toBeVisible();
  await expect(page.getByRole('heading', { level: 3, name: /Translate and answer \// })).toHaveCount(0);
});
