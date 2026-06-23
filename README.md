# La esperanto-kurso laŭ la Zagreba metodo

[![Aliĝu la babililon https://gitter.im/Esperanto/kurso-zagreba-metodo](https://badges.gitter.im/Esperanto/kurso-zagreba-metodo.svg)](https://gitter.im/Esperanto/kurso-zagreba-metodo?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

Tiu deponejo enhavas la Esperanto-kurson laŭ la [Zagreba metodo](https://eo.wikipedia.org/wiki/Zagreba_metodo) en strukturita datumaranĝo. Do, la kompleta enhavo estas konservita per [YAML](https://en.wikipedia.org/wiki/YAML)-dosieroj, facile legeblaj per diversaj komputilaj programlingvoj – kaj ankaŭ por homoj.

Tiel oni facile kaj rapide povos krei eldonaĵojn de la kurso en HTML, EPUB, PDF aŭ ia ajn formo.

## Demonstraĵo

- https://esperanto12.net/

## Kiel krei eligon

Unue kreu virtualan medion kaj instalu la bezonatajn Python- kaj npm-dependecojn:

    make install

La rektaj Python-dependecoj estas listigitaj en `requirements.in`. `requirements.txt` estas la ŝlosita instal-dosiero, generita per:

    make lock

La frontend-bibliotekoj, kiuj aperas publike sub `/vendor/...`, estas ŝlositaj en `package.json` kaj `package-lock.json`. Ili estas instalataj per `npm ci --ignore-scripts` dum `make install` kaj kopiataj al `eligo/retejo/vendor` dum HTML-generado.
Por tio necesas Node.js kun npm; la pinglita Node-versio troviĝas en `.nvmrc` kaj la GitHub Actions-laborfluo uzas tiun saman version.

Por kontroli la anglan Markdown-, HTML- kaj Anki-eligon:

    make check

Tio unue forigas `eligo/retejo`, poste generas `eligo/md/en.md` kaj `eligo/retejo/en`, kaj fine kontrolas kernajn dosierojn kaj la APKG-eksporton.

### HTML

    make html LINGVO=en

Kreas HTML-dosierujon en `eligo/retejo/en`.

Por generi la tutan produktadan HTML-eligon:

    make html-all

Tio ankaŭ kreas PWA-manifeston, ikonojn, registrilon kaj radikan `sw.js`. Tiuj dosieroj estas provizore ne ligitaj el la HTML, do la retejo nuntempe ne proponas instaleblan PWA-on al vizitantoj.

Por kontroli, ke la PWA-manifesto validas kaj ke ĉiu generita dosiero troviĝas en la offline-listo:

    make check-pwa

Por antaŭrigardi jam generitan HTML-on loke:

    make serve

Tio servas `eligo/retejo` ĉe `http://127.0.0.1:8000`.

Por forigi la generitan retejan eligon:

    make clean

La produkta retejo `esperanto12.net` estas disponigata per GitHub Pages el `eligo/retejo`.
PR-oj al `master` rulas la saman kontrolon kaj HTML-kunmeton, sed ne disponigas retejon.

### PDF kaj EPUB

Vi bezonas [Pandoc](https://pandoc.org), minimume versionon 2.

    make md LINGVO=en

Eligas la tutan kurson en Markdown al `STDOUT`, tial per:

    make md LINGVO=en | pandoc --latex-engine=xelatex -o en.pdf
    make md LINGVO=en | pandoc -o en.epub

oni povas krei kaj PDF kaj EPUB dosieron.

#### Limigu enhavon

    venv/bin/python -m fonto.py.generu --lingvo en --eligformo md --printendaj-partoj ekzerco2 solvo2
      --printendaj-lecionoj 1 2 3
    
Eligu nur ekzercon 2 kaj sian solvon, kaj nur de lecionoj 1, 2, 3. Legu plu per `venv/bin/python -m fonto.py.generu --help`.

## Permesiloj

Tiun ĉi kurson oni povas libere uzi, kondiĉe ke oni nomas la [aŭtorojn](AUTHORS.md).

### Esperantaj tekstoj

![permesilo](fonto/bildoj/by-nd.png)

La Esperantaj leciontekstoj en la kurso `enhavo/netradukenda/tekstoj` devas resti neŝanĝitaj. Tial aplikas la [CC BY-ND 4.0](enhavo/netradukenda/tekstoj/PERMESILO.md).

### Aliaj dosieroj

![permesilo](fonto/bildoj/by.png)

Ĉion alian oni povas ŝanĝi. Tial aplikas la [CC BY 4.0](PERMESILO.md).

## Pliaj tradukoj?

Ĉu vi volas traduki la kurson al nova lingvo? Belege! Bonvole [plulegu tie](KONTRIBUADO.md).
