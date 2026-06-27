const { expect, test } = require('@playwright/test');

test('ĉefpaĝo elektas retumilan lingvon', async ({ browser }) => {
  const context = await browser.newContext({ locale: 'fr-FR' });
  const page = await context.newPage();

  await page.goto('/');

  await expect(page.getByRole('heading', { name: "Apprendre l'espéranto" })).toBeVisible();
  await expect(page.getByText('Le cours le plus rapide pour apprendre les bases')).toBeVisible();

  const primaryLanguage = page.locator('#cxefpagxo-cxefa-lingvo');
  await expect(primaryLanguage).toHaveText('Français');
  await expect(primaryLanguage).toHaveAttribute('href', 'fr/');

  const languageButton = page.locator('#cxefpagxo-lingvoj-butono');
  await expect(languageButton).toContainText('🌐');
  await expect(languageButton).toHaveClass(/btn-light/);
  await page.locator('#cxefpagxo-lingvoj-butono').click();

  const languageMenu = page.locator('#cxefpagxo-lingvoj');
  await expect(languageMenu.getByRole('link', { name: 'English' })).toBeVisible();
  await expect(languageMenu.getByRole('link', { name: 'Français' })).toHaveCount(0);
  await expect(page.locator('.cxefpagxo-pri-esperanto a')).toHaveAttribute('href', 'https://esperanto.net/');
  await expect(page.getByText('Subtenita de la')).toBeVisible();
  await expect(page.getByRole('link', { name: 'Universala Esperanto Asocio' })).toBeVisible();

  await context.close();
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

test('poŝtelefone vortaro restas inter logo kaj cxiamaj butonoj en unu linio', async ({ page }) => {
  for (const width of [320, 360, 390]) {
    await page.setViewportSize({ width, height: 720 });
    await page.goto('/en/01/');

    const dictionary = page.locator('#vortaro');
    await expect(dictionary).toBeVisible();
    await expect(page.getByRole('button', { name: 'Toggle navigation' })).toHaveCount(0);

    const logoBox = await page.locator('.navbar-brand').boundingBox();
    const dictionaryBox = await dictionary.boundingBox();
    const appendixBox = await page.getByRole('button', { name: 'Appendix' }).boundingBox();
    const languageBox = await page.getByRole('button', { name: 'Elekti alian lingvon' }).boundingBox();
    const navbarBox = await page.locator('.navbar').boundingBox();

    expect(dictionaryBox.x).toBeGreaterThan(logoBox.x + logoBox.width - 1);
    expect(dictionaryBox.x + dictionaryBox.width).toBeLessThan(appendixBox.x + 1);
    expect(appendixBox.x + appendixBox.width).toBeLessThan(languageBox.x + languageBox.width + 1);
    expect(languageBox.x + languageBox.width).toBeLessThanOrEqual(width);
    expect(Math.abs((dictionaryBox.y + dictionaryBox.height / 2) - (logoBox.y + logoBox.height / 2))).toBeLessThan(3);
    expect(Math.abs((dictionaryBox.y + dictionaryBox.height / 2) - (appendixBox.y + appendixBox.height / 2))).toBeLessThan(3);
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

test('piedo montras grizajn tri kolumnojn kun permesilaj ligiloj', async ({ page }) => {
  await page.goto('/en/01/');

  const footer = page.locator('.footer');
  await expect(footer).toHaveCSS('background-color', 'rgb(136, 136, 136)');
  await expect(footer.locator('img[src="/assets/img/cc-by.svg"]')).toBeVisible();
  await expect(footer.getByRole('link', { name: 'Krea komunaĵo' })).toHaveAttribute(
    'href',
    'https://github.com/Esperanto/kurso-zagreba-metodo/blob/master/PERMESILO.md',
  );
  await expect(footer.getByText('Surbaze de la')).toBeVisible();
  await expect(footer.getByRole('link', { name: 'Zagreba metodo' })).toHaveAttribute(
    'href',
    'https://eo.wikipedia.org/wiki/Zagreba_metodo',
  );
  await expect(footer.getByRole('link', { name: 'Kontribuantoj' })).toHaveAttribute(
    'href',
    /auxtoroj\/$/,
  );
  await expect(footer.getByRole('link', { name: 'Kontribuu' })).toHaveAttribute(
    'href',
    'https://github.com/Esperanto/kurso-zagreba-metodo/tree/master/KONTRIBUADO.md',
  );
  await expect(footer.getByText(/⏱︎ Versio: [0-9a-f]{7}/)).toBeVisible();

  const footerBox = await footer.boundingBox();
  const viewport = page.viewportSize();
  expect(Math.round(footerBox.x)).toBe(0);
  expect(Math.abs(footerBox.width - viewport.width)).toBeLessThan(1);
});

test('ŝvebi super tekstaj vortoj montras tradukajn ŝprucfenestrojn', async ({ page }) => {
  await page.goto('/en/01/');

  await page.locator('.leciona-titolo-teksto > a', { hasText: 'Amiko' }).first().hover();

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

test('aldona kaj lingva menuoj restas cxiam atingeblaj', async ({ page }) => {
  await page.setViewportSize({ width: 580, height: 720 });
  await page.goto('/en/01/');

  await page.getByRole('button', { name: 'Appendix' }).click();

  const appendixMenu = page.locator('.dropdown-menu.show').filter({
    hasText: 'Correlatives',
  });
  await expect(appendixMenu).toBeVisible();

  await page.getByRole('button', { name: 'Appendix' }).click();
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

test('malsupra pagxilo uzas sagojn kun tradukitaj konsiletoj', async ({ page }) => {
  await page.goto('/en/02/');

  const pager = page.locator('ul.pager');
  await expect(pager.getByRole('link', { name: 'Back' })).toHaveText('◀︎');
  await expect(pager.getByRole('link', { name: 'Back' })).toHaveAttribute('title', 'back');
  await expect(pager.getByRole('link', { name: 'Forward' })).toHaveText('▶︎');
  await expect(pager.getByRole('link', { name: 'Forward' })).toHaveAttribute('title', 'forward');
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
