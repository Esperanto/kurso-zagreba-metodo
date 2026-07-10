const { expect, test } = require('@playwright/test');

test('hejmpaĝo plusendas al la retumila lingvo', async ({ browser }) => {
  const context = await browser.newContext({ locale: 'de-DE' });
  await context.addInitScript(() => {
    Object.defineProperty(navigator, 'languages', { get: () => ['de-DE', 'en-US'] });
    Object.defineProperty(navigator, 'language', { get: () => 'de-DE' });
  });
  const page = await context.newPage();

  await page.goto('/');
  await expect(page).toHaveURL(/\/de\/$/);

  await context.close();
});

test('hejmpaĝo plusendas nekonatan lingvon al la angla', async ({ browser }) => {
  const context = await browser.newContext({ locale: 'zz-ZZ' });
  await context.addInitScript(() => {
    Object.defineProperty(navigator, 'languages', { get: () => ['zz-ZZ'] });
    Object.defineProperty(navigator, 'language', { get: () => 'zz-ZZ' });
  });
  const page = await context.newPage();

  await page.goto('/');
  await expect(page).toHaveURL(/\/en\/$/);

  await context.close();
});

test('hejmpaĝo signalas la lingvoversiojn al serĉiloj', async ({ page }) => {
  const response = await page.request.get('/');
  const html = await response.text();

  expect(html).toContain('Learn Esperanto');
  // La lingvoversioj estas signalitaj al serĉiloj per hreflang-alternativoj
  // en la kapo (la hejmpaĝo mem estas JS-lingvoelektilo kun plusendo).
  expect(html).toContain('rel="alternate" hreflang="en" href="https://esperanto12.net/en/"');
  expect(html).toContain('rel="alternate" hreflang="de" href="https://esperanto12.net/de/"');
  expect(html).not.toContain('hejmo-subtitolo');
});

test('angla lingva startpaĝo montras kursan enkondukon', async ({ page }) => {
  await page.goto('/en/');

  await expect(page.locator('.lingva-startpagxo-logo')).toHaveAttribute(
    'src',
    '/assets/img/logo/logo-256.png',
  );
  await expect(page.getByRole('heading', { name: 'Learn Esperanto in 12 Lessons' })).toBeVisible();
  await expect(page.getByText('The Fastest Basics Course')).toBeVisible();
  await expect(page.getByText('most important 500 words')).toBeVisible();
  await expect(page.getByText('without registration')).toBeVisible();
  await expect(page.getByRole('link', { name: 'flashcard deck' })).toHaveAttribute(
    'href',
    '/en/eksporto/en.apkg',
  );
  await expect(page.getByRole('link', { name: 'Anki' })).toHaveAttribute(
    'href',
    'https://apps.ankiweb.net/',
  );
  await expect(page.getByRole('link', { name: 'Anki' })).toHaveAttribute('target', '_blank');
  await expect(page.getByRole('link', { name: 'Anki' })).toHaveAttribute('rel', 'noopener');
  await expect(page.getByRole('link', { name: 'Start' })).toHaveAttribute('href', '/en/01');

  const languageButton = page.locator('.lingva-startpagxo-agoj .dropdown-toggle');
  await expect(languageButton).toContainText('🌐');
  await expect(languageButton).toContainText(/languages/);
  await languageButton.click();
  await expect(page.locator('.lingva-startpagxo-lingvoj').getByRole('link', { name: 'English' })).toBeVisible();

  const speakerLink = page.getByRole('link', { name: 'Find Esperanto speakers' });
  await expect(speakerLink).toHaveAttribute(
    'href',
    '/en/post',
  );
  await expect(page.locator('.lingva-startpagxo-parolantoj')).toHaveClass(/text-center/);
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

test('piedo montras grizajn tri kolumnojn kun permesilaj ligiloj', async ({ page }) => {
  await page.goto('/en/01/');

  const footer = page.locator('.footer');
  await expect(footer).toHaveCSS('background-color', 'rgb(136, 136, 136)');
  await expect(footer.locator('img[src="/assets/img/cc-by.svg"]')).toBeVisible();
  await expect(footer.getByRole('link', { name: 'Krea komunaĵo' })).toHaveAttribute(
    'href',
    'https://github.com/Esperanto/kurso-zagreba-metodo/blob/master/PERMESILO.md',
  );
  await expect(footer.getByRole('link', { name: 'Krea komunaĵo' })).toHaveAttribute('target', '_blank');
  await expect(footer.getByRole('link', { name: 'Krea komunaĵo' })).toHaveAttribute('rel', 'noopener');
  await expect(footer.getByText('Surbaze de la')).toBeVisible();
  await expect(footer.getByRole('link', { name: 'Zagreba metodo' })).toHaveAttribute(
    'href',
    'https://eo.wikipedia.org/wiki/Zagreba_metodo',
  );
  await expect(footer.getByRole('link', { name: 'Zagreba metodo' })).toHaveAttribute('target', '_blank');
  await expect(footer.getByRole('link', { name: 'Zagreba metodo' })).toHaveAttribute('rel', 'noopener');
  await expect(footer.getByRole('link', { name: 'Kontribuantoj' })).toHaveAttribute(
    'href',
    /auxtoroj\/$/,
  );
  await expect(footer.getByRole('link', { name: 'Kontribuu' })).toHaveAttribute(
    'href',
    'https://github.com/Esperanto/kurso-zagreba-metodo/tree/master/KONTRIBUADO.md',
  );
  await expect(footer.getByRole('link', { name: 'Kontribuu' })).toHaveAttribute('target', '_blank');
  await expect(footer.getByRole('link', { name: 'Kontribuu' })).toHaveAttribute('rel', 'noopener');
  const versio = footer.locator('.versio');
  const versioDato = versio.locator('.versio-dato');
  await expect(versio).toHaveText(/⏱︎ Versio: [0-9a-f]{7} \d{4}-\d{2}-\d{2} \d{2}:\d{2} Z/);
  await expect(versioDato).toHaveAttribute('datetime', /\d{4}-\d{2}-\d{2}T\d{2}:\d{2}Z/);
  await expect(versioDato).toHaveCSS('white-space', 'nowrap');
  await expect(versioDato).toHaveCSS('text-wrap-mode', 'nowrap');

  const footerBox = await footer.boundingBox();
  const viewport = page.viewportSize();
  expect(Math.round(footerBox.x)).toBe(0);
  expect(Math.abs(footerBox.width - viewport.width)).toBeLessThan(1);
});

test('piedo ligas al redaktado de la aktuala enhavo', async ({ page }) => {
  await page.goto('/en/');
  await expect(page.locator('.footer').getByRole('link', { name: 'Redaktu tiun ĉi enhavon' })).toHaveAttribute(
    'href',
    'https://github.com/Esperanto/kurso-zagreba-metodo/blob/master/enhavo/tradukenda/en/enkonduko.md',
  );
  await expect(page.locator('.footer').getByRole('link', { name: 'Redaktu tiun ĉi enhavon' })).toHaveAttribute('target', '_blank');
  await expect(page.locator('.footer').getByRole('link', { name: 'Redaktu tiun ĉi enhavon' })).toHaveAttribute('rel', 'noopener');

  await page.goto('/en/01/');
  await expect(page.locator('.footer').getByRole('link', { name: 'Redaktu tiun ĉi enhavon' })).toHaveAttribute(
    'href',
    'https://github.com/Esperanto/kurso-zagreba-metodo/tree/master/enhavo/tradukenda/en/vortaro',
  );

  await page.goto('/en/01/gramatiko/');
  await expect(page.locator('.footer').getByRole('link', { name: 'Redaktu tiun ĉi enhavon' })).toHaveAttribute(
    'href',
    'https://github.com/Esperanto/kurso-zagreba-metodo/blob/master/enhavo/tradukenda/en/gramatiko/01.md',
  );

  await page.goto('/en/01/ekzerco1/');
  await expect(page.locator('.footer').getByRole('link', { name: 'Redaktu tiun ĉi enhavon' })).toHaveAttribute(
    'href',
    'https://github.com/Esperanto/kurso-zagreba-metodo/blob/master/enhavo/tradukenda/en/ekzercoj/traduku/01.yml',
  );

  await page.goto('/en/01/ekzerco3/');
  await expect(page.locator('.footer').getByRole('link', { name: 'Redaktu tiun ĉi enhavon' })).toHaveAttribute(
    'href',
    'https://github.com/Esperanto/kurso-zagreba-metodo/blob/master/enhavo/tradukenda/en/ekzercoj/traduku-kaj-respondu/01.yml',
  );
});

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
