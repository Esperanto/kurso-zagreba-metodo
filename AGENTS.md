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
- `html_generiloj/`: HTML-genera kodo, ŝablonoj kaj generita eligo.
- `leo_markdown/`: Markdown-genera kodo kaj ŝablonoj.
- `genanki/`: inkluzivita aŭ vendorigita projekto rilata al Anki; evitu tuŝi ĝin krom se la tasko specife temas pri tiu subarbo.

## Agordo Kaj Komandoj

Kreu virtualan medion kaj instalu Python-dependecojn per:

```sh
make install
```

La kanonika taska tavolo por agentoj estas `make`, simile al `npm run ...` en JavaScript-projektoj:

```sh
make install
make check
make html LINGVO=en
make html-all
make md LINGVO=en
make serve
```

`make check` instalas nenion. Se `venv/bin/python` aŭ dependecoj mankas, rulu `make install`. La virtuala medio estas `venv` defaŭlte; oni povas uzi alian per `VENV=.venv make install`.

Generu HTML por lingvo, ekzemple la angla:

```sh
make html LINGVO=en
```

Tio skribas al `html_generiloj/output/en`.

Por antaŭrigardi jam generitan HTML-on loke, rulu:

```sh
make serve
```

Tio nur servas la ekzistantan enhavon de `html_generiloj/output`; ĝi ne regeneras dosierojn.

Generu Markdown:

```sh
make md LINGVO=en
```

La Markdown-eligo estas skribata al stdout. Generado de PDF kaj EPUB bezonas Pandoc, kiel priskribite en `README.md`.

La prova retejo `stg.esperanto12.net` estas konstruata per GitHub Pages el `html_generiloj/output` uzante `make html-all`. Ne revivigu `maintenance/gxisdatigu-eligon.sh` por produktadaj deplojoj; ĝi restas nur hereda servila rezervo dum la transiro.

## Redaktado De Enhavo

- Gardu YAML-on valida kaj preferu ekzistantan proksiman strukturon anstataŭ enkonduki novajn formatojn.
- Metu inter citilojn YAML-valorojn, kiuj povus esti interpretataj kiel buleaj aŭ specialaj skalaroj, ekzemple `on`, `off`, `yes`, aŭ valorojn enhavantajn apostrofojn.
- Por gramatika Markdown, sekvu la konvenciojn en `KONTRIBUADO.md`: Esperantaj ekzemploj uzas `*...*`, tradukoj estas apartigitaj per `–`, kaj emfazitaj morfemoj uzas `__...__`.
- Kiam vi aldonas aŭ ĝisdatigas lingvon, spegulu la ekzistantan dosierujan strukturon sub `enhavo/tradukenda/`.
- Ne modifu `enhavo/netradukenda/tekstoj/` krom se la uzanto eksplicite konfirmas licencokonscian ŝanĝon.

## Kodstilaj Notoj

- Ĉi tio estas malgranda Python-projekto, kiu uzas simplajn modulojn kaj ŝablonojn laŭ Jinja/Chevron-stilo. Preferu rektajn ŝanĝojn al novaj abstraktaĵoj.
- Konservu UTF-8-tekston kaj Esperantajn supersignojn.
- `generate.py` estas la ĉefa enirpunkto kaj atendas esti rulata el la deponeja radiko.
- Evitu enmeti generitajn kaŝmemorojn kiel `__pycache__/` aŭ `.pyc`-dosierojn en versikontrolon.

## Validigo

Ne estas dokumentita aŭtomata testaro ĉe la deponeja radiko. Por ŝanĝoj al generiloj aŭ ŝablonoj, rulu almenaŭ:

```sh
make check
```

Se ŝanĝo influas specifan lingvon, rulu la generilon ankaŭ por tiu lingvo.

Por malpli oftaj opcioj de la generilo, uzu rekte:

```sh
venv/bin/python generate.py --help
```
