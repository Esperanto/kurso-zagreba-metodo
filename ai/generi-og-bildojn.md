# Prompto: generi Open Graph-bildojn por lingvaj startpaĝoj

Reuzebla prompto por generi aŭ regeneri la lingvajn Open Graph-bildojn el la
lokaj startpaĝoj de la kurso.

## Celo

Kreu PNG-bildon por ĉiu preta lingva startpaĝo, uzante la videblan enhavon de
`/<lingvo>/` kiel fonton. Kiam tasko eksplicite petas ankaŭ testajn lingvojn,
inkluzivu ankaŭ lingvojn kun `stato: testa`. La bildoj estu konservitaj sub:

```sh
fonto/bildoj/og/<lingvo>.png
```

La radika bildo `fonto/bildoj/og.png` restu la ĝenerala fallback-bildo kaj ne
estu regenerata per ĉi tiu tasko krom se tio estas eksplicite petita.

La publikaj `og:image`-valoroj en la HTML estu absolutaj URL-oj, ekzemple:

```html
<meta property="og:image" content="https://esperanto12.net/assets/img/og/de.png" />
```

Ne anstataŭigu ilin per relativaj vojoj kiel `/assets/img/og/de.png`; multaj
Open Graph-konsumantoj atendas plenan `https://...`-URL-on.

## Lingvoj

Normale uzu nur lingvojn el `agordoj/lingvoj.yml` kun:

```yaml
stato: preta
```

Kiam la tasko eksplicite petas ankaŭ testajn lingvojn, uzu lingvojn kun:

```yaml
stato: preta
```

aŭ:

```yaml
stato: testa
```

Por ĉiu generita bildo:

- Aldonu 100 px blankan randon maldekstre.
- Aldonu 100 px blankan randon dekstre.
- Forigu 2 px ĉe la malsupro de la fina bildo.

Direkto (`tekstodirekto`) influas la paĝan aranĝon mem, sed la fina blanka
rando estas simetria por LTR- kaj RTL-lingvoj.

## Generado

1. Generu la bezonatajn lingvajn retejojn, prefere en unu generatora voko por
   eviti paralelan kopiadon de komunaj statikaj dosieroj:

   ```sh
   venv/bin/python -m fonto.py.generu --lingvoj <lingvokodoj> --eligformo html
   ```

2. Servu la generitan retejon el `eligo/retejo`:

   ```sh
   make serve PORT=8765
   ```

3. Per Playwright malfermu `http://127.0.0.1:8765/<lingvo>/` kun:

   ```js
   viewport: { width: 1200, height: 630 }
   deviceScaleFactor: 2
   ```

4. Antaŭ la ekrankopio kaŝu la sticky navbaron:

   ```js
   await page.addStyleTag({
     content: 'nav.navbar { display: none !important; }'
   });
   ```

5. Faru ekrankopion nur de ĉi tiu elemento:

   ```css
   body > main > div > div > div
   ```

6. Konservu unue kiel provizoran dosieron:

   ```sh
   fonto/bildoj/og/<lingvo>.raw.png
   ```

7. Aldonu blankan randon kaj forigu 2 px ĉe la malsupro per ImageMagick:

   ```sh
   magick fonto/bildoj/og/<lingvo>.raw.png \
     -background white \
     -splice 100x0 \
     -gravity east \
     -splice 100x0 \
     -gravity south \
     -chop 0x2 \
     fonto/bildoj/og/<lingvo>.png
   ```

8. Forigu ĉiujn provizorajn `*.raw.png`-dosierojn.

## Kontroloj

Post generado:

- Kontrolu ke ĉiu bezonata lingvo havas bildon. Por nur pretaj lingvoj:

  ```sh
  venv/bin/python - <<'PY'
  from pathlib import Path
  import yaml

  lingvoj = yaml.safe_load(Path('agordoj/lingvoj.yml').read_text(encoding='utf-8'))
  pretaj = [k for k, v in sorted(lingvoj.items()) if v.get('stato') == 'preta']
  missing = [k for k in pretaj if not Path(f'fonto/bildoj/og/{k}.png').is_file()]
  print('pretaj:', len(pretaj), 'missing:', missing)
  raise SystemExit(bool(missing))
  PY
  ```

  Por pretaj kaj testaj lingvoj:

  ```sh
  venv/bin/python - <<'PY'
  from pathlib import Path
  import yaml

  lingvoj = yaml.safe_load(Path('agordoj/lingvoj.yml').read_text(encoding='utf-8'))
  kodoj = [
      k for k, v in sorted(lingvoj.items())
      if v.get('stato') in {'preta', 'testa'}
  ]
  missing = [k for k in kodoj if not Path(f'fonto/bildoj/og/{k}.png').is_file()]
  print('pretaj+testaj:', len(kodoj), 'missing:', missing)
  raise SystemExit(bool(missing))
  PY
  ```

- Kontrolu ke ne restas provizoraj dosieroj:

  ```sh
  find fonto/bildoj/og -maxdepth 1 -name '*.raw.png' -print
  ```

- Kontrolu dimensiojn kaj grandecon:

  ```sh
  file fonto/bildoj/og/*.png
  ls -lh fonto/bildoj/og/*.png
  ```

- Faru vidan kontrolon de almenaŭ unu LTR-bildo, unu RTL-bildo kaj unu bildo
  kun longa teksto.
- Rulu:

  ```sh
  git diff --check
  ```

## Atentoj

- Ne lanĉu plurajn `make html LINGVO=...` komandojn paralele; ili kopias samajn
  komunajn statikajn dosierojn kaj povas kolizii.
- Ne inkluzivu la navbaron en la bildoj.
- Ne commit-u generitan `eligo/retejo`.
- Commit-u nur fontajn bildojn sub `fonto/bildoj/og/` kaj eventualajn intence
  petitajn generatorajn aŭ ŝablonajn ŝanĝojn.
