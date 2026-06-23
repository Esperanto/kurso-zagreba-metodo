# AGENTS.md

Gvidilo por aŭtomatigitaj kodaj agentoj laborantaj en ĉi tiu deponejo.

## Projekta Superrigardo

Ĉi tiu deponejo enhavas la Esperanto-kurson laŭ la Zagreba metodo. La kursa enhavo estas konservita ĉefe kiel YAML kaj Markdown, poste transformata al HTML, Markdown, PDF, EPUB aŭ rilataj formatoj.

La projekta lingvo kaj la dokumentaro videbla al uzantoj estas plejparte Esperantaj. Konservu ekzistantajn Esperantajn vortumojn kaj dosiernomajn konvenciojn krom se tasko eksplicite petas tradukon aŭ tekstajn ŝanĝojn.

## Gravaj Dosierujoj

- `enhavo/netradukenda/`: netradukenda fontenhavo komuna al ĉiuj lingvoj.
- `enhavo/netradukenda/tekstoj/`: Esperantaj leciontekstoj. Ili estas licencitaj laŭ CC BY-ND kaj ne devas esti ŝanĝitaj.
- `enhavo/tradukenda/<lingvo>/`: lingvospecifaj tradukoj, gramatikaj klarigoj, ekzercoj, vortaroj, enkonduko kaj posta teksto.
- `agordoj/`: agordo de lingvoj kaj aŭtoroj.
- `fonto/py/`: Python-generatoroj. La ĉefa enirpunkto estas `fonto.py.generu`.
- `fonto/html/` kaj `fonto/md/`: ŝablonoj por HTML kaj Markdown.
- `fonto/css/`, `fonto/js/`, `fonto/bildoj/` kaj `fonto/sonoj/`: statikaj fontdosieroj kopiataj al la reteja eligo.
- `eligo/retejo/`: generita HTML-retejo. Ne versikontrolu ĝin.
- `vendor/`: vendorigitaj eksteraj bibliotekoj, inkluzive de `bootstrap`, `jquery` kaj `typeahead`. Evitu tuŝi ilin krom se la tasko specife temas pri tiu subarbo.
- `iloj/`: prizorgaj helpiloj.

## Agordo Kaj Komandoj

Kreu virtualan medion kaj instalu Python-dependecojn per:

```sh
make install
```

La kanonika taska tavolo por agentoj estas `make`, simile al `npm run ...` en JavaScript-projektoj:

```sh
make install
make check
make check-pwa
make html LINGVO=en
make html-all
make md LINGVO=en
make serve
make clean
```

`make check` instalas nenion. Ĝi ĉiam kontrolas la anglan eligon, unue forigas `eligo/retejo`, generas `eligo/md/en.md` kaj `eligo/retejo/en`, kaj kontrolas kernajn HTML-dosierojn kaj la Anki-APKG-on. Se `venv/bin/python` aŭ dependecoj mankas, rulu `make install`. La virtuala medio estas `venv` defaŭlte; oni povas uzi alian per `VENV=.venv make install`.

Python-dependecoj estas mastrumataj per pip kaj pip-tools. Redaktu rektajn dependecojn en `requirements.in`, poste rulu `make lock` por regeneri la ŝlositan `requirements.txt`. Por intence ĝisdatigi ĉiujn ŝlositajn versiojn, rulu `make lock-upgrade`.

Generu HTML por lingvo, ekzemple la angla:

```sh
make html LINGVO=en
```

Tio skribas al `eligo/retejo/en`.

`make html` kaj `make html-all` kreas ankaŭ PWA-dosierojn (`manifest.webmanifest`, `pwa/registru.js`, `pwa/images/` kaj `sw.js`). Tiuj dosieroj estas provizore ne ligitaj el la HTML, do la retejo nuntempe ne proponas instaleblan PWA-on al vizitantoj. Ne redaktu `eligo/retejo/sw.js` permane. Post `make html-all`, rulu `make check-pwa` por kontroli la nepublike proponatan PWA-eligon.

Por antaŭrigardi jam generitan HTML-on loke, rulu:

```sh
make serve
```

Tio nur servas la ekzistantan enhavon de `eligo/retejo`; ĝi ne regeneras dosierojn.

Por forigi generitan retejan eligon, rulu:

```sh
make clean
```

Generu Markdown:

```sh
make md LINGVO=en
```

La Markdown-eligo estas skribata al stdout. Generado de PDF kaj EPUB bezonas Pandoc, kiel priskribite en `README.md`.

La produkta retejo `esperanto12.net` estas disponigata per GitHub Pages el `eligo/retejo` uzante `make html-all` kaj `make check-pwa`. PR-oj al `master` rulas kontrolon kaj HTML-kunmeton, sed ne disponigas retejon. Ne aldonu apartajn disponigajn skriptojn por produktado; la Pages-artefakta laborfluo estas la kanonika disponigo.

## Redaktado De Enhavo

- Gardu YAML-on valida kaj preferu ekzistantan proksiman strukturon anstataŭ enkonduki novajn formatojn.
- Metu inter citilojn YAML-valorojn, kiuj povus esti interpretataj kiel buleaj aŭ specialaj skalaroj, ekzemple `on`, `off`, `yes`, aŭ valorojn enhavantajn apostrofojn.
- Por gramatika Markdown, sekvu la konvenciojn en `KONTRIBUADO.md`: Esperantaj ekzemploj uzas `*...*`, tradukoj estas apartigitaj per `–`, kaj emfazitaj morfemoj uzas `__...__`.
- Kiam vi aldonas aŭ ĝisdatigas lingvon, spegulu la ekzistantan dosierujan strukturon sub `enhavo/tradukenda/`.
- Ne modifu `enhavo/netradukenda/tekstoj/` krom se la uzanto eksplicite konfirmas licencokonscian ŝanĝon.

## Kodstilaj Notoj

- Ĉi tio estas malgranda Python-projekto, kiu uzas simplajn modulojn kaj ŝablonojn laŭ Jinja/Chevron-stilo. Preferu rektajn ŝanĝojn al novaj abstraktaĵoj.
- Konservu UTF-8-tekston kaj Esperantajn supersignojn.
- `fonto.py.generu` estas la ĉefa enirpunkto kaj atendas enhavajn vojojn relative al la deponeja radiko.
- Evitu enmeti generitajn kaŝmemorojn kiel `__pycache__/` aŭ `.pyc`-dosierojn en versikontrolon.

## Validigo

Ne estas dokumentita aŭtomata testaro ĉe la deponeja radiko. Por ŝanĝoj al generiloj aŭ ŝablonoj, rulu almenaŭ:

```sh
make check
```

Se ŝanĝo influas la PWA-on aŭ la produktadan retejan eligon, rulu ankaŭ:

```sh
make html-all
make check-pwa
```

Se ŝanĝo influas specifan lingvon, rulu la generilon ankaŭ por tiu lingvo.

Por malpli oftaj opcioj de la generilo, uzu rekte:

```sh
venv/bin/python -m fonto.py.generu --help
```
