const { expect, test } = require('@playwright/test');

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
