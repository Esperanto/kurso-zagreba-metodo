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

Instalu Python-dependecojn per:

```sh
pip install -r requirements.txt
```

Generu HTML por lingvo, ekzemple la angla:

```sh
python generate.py --lingvo en --eligformo html
```

Tio skribas al `html_generiloj/output/en`.

Generu Markdown:

```sh
python generate.py --lingvo en --eligformo md
```

La Markdown-eligo estas skribata al stdout. Generado de PDF kaj EPUB bezonas Pandoc, kiel priskribite en `README.md`.

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
python generate.py --lingvo en --eligformo html
```

Por ŝanĝoj al Markdown-eligo, rulu ankaŭ:

```sh
python generate.py --lingvo en --eligformo md >/tmp/leo-en.md
```

Se ŝanĝo influas specifan lingvon, rulu la generilon ankaŭ por tiu lingvo.
