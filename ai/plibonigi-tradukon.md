# Prompto: plibonigi la tradukon de la Zagreba-metoda kurso

Reuzebla prompto por plibonigi la tradukon de unu lingvo de la kurso —
gramatikaj klarigoj, vortaro kaj ekzercoj. Agordu la cellingvon kaj laboru nur
ene de ĝia dosierujo:

```
LINGVO=de
```

Laboru nur en `enhavo/tradukenda/${LINGVO}/**`.

## Celo

Plibonigi la tradukon de la Zagreba-metoda kurso **sen ŝanĝi la kursan
strukturon**.

## Taskoj

- Korektu gramatikajn, ortografiajn, interpunkciajn kaj stilajn erarojn en la
  cela lingvo.
- Faru la tradukitan tekston natura, klara kaj lernanto-amika, sed restu fidele
  proksima al la Esperanta enhavo.
- Konservu la ekzistantan tonon kaj rektan alparolon al lernantoj.
- En gramatikaj klarigoj, se vi aldonas aŭ ŝanĝas Esperantajn ekzemplojn, uzu
  nur bazan/fundamentan Esperanton.
- Ne ŝanĝu la netradukendan Esperantan fontenhavon.

## Gramatikaj klarigoj (`gramatiko/01.md` … `12.md`)

Konservu la temojn, la sekcian strukturon kaj la Esperanto-ekzemplojn de la
lingvo; plibonigu nur la **prezenton**:

- Dispecigu densajn tekstblokojn en skaneblan strukturon (subtitoloj, mallongaj
  alineoj, listeroj).
- Eksplicitigu la regulecon de Esperanto (ekz. `-as` egala por ĉiuj personoj;
  posedaj pronomoj = pronomo + `-a`; la vokala sistemo `-o`/`-a`/`-e`; la tempaj
  vokaloj `i`–`a`–`o`).
- Kontrastu kun la denaska lingvo de la lernanto; aldonu memorhelpilojn (komencu
  ilin prefere per la Esperanto-vorto) kaj avertojn pri stumbliloj (eraroj kiujn
  parolantoj de tiu lingvo emas fari).

Formataj konvencioj:

- **Ĉio Esperanta estas kursiva**: `*vorto*` (ankaŭ unuopaj literoj kaj finaĵoj).
- **Novajn morfemojn marku grase** per `__morfemo__`; ĉe enkonduko de nova
  finaĵo/afikso kombinu kursivon+grason `*__-o__*`; ene de ekzempla vorto la
  morfemo estas grasa: `patr__in__o`.
- **Avertaj kaj memorhelpaj kestoj kun konstanta ikono**, etikedo en la
  cellingvo:
  - `**⚠️ <averto>:**` — por avertoj/stumbliloj
  - `**💡 <memorhelpilo>:**` — por memorhelpiloj kaj konsiletoj
- **Neniu ikono en titoloj** (tio rompus la enhav-kontrolon
  `fonto/py/kontrolu_eligon.py`, kiu atendas ekz. `<h3>Alphabet</h3>`).
- **Ekzemplojn post dupunkto** metu kiel apartajn listerojn, ne inline:

  ```markdown
  **💡 <memorhelpilo>:** *-ec* respondas al ...:

  - *bela* (traduko) → *beleco* (traduko)
  ```

- **Ekzemplo-formato**: Esperanto-vorto unue, traduko en krampoj, sago al la
  rezulto: `*skribi* (traduko) → *skribilo* (traduko)`.
- **Krucreferencojn faru ligiloj**: `[<leciono> 6](/${LINGVO}/06/gramatiko/)`;
  la tabelon de korelativoj ligu al `[<korelativoj>](/${LINGVO}/tabelvortoj/)`.
  Ne skribu nudan «(leciono 5)».
- **Riparu fuŝan markadon**, ekz. `*libr_ego_*` (unuopaj substrekoj → kursiva
  «ego») al `*libr__eg__o*`.
- **Tabeloj ne rendiĝas** (mankas tabela kromaĵo en mistune) — ne uzu
  inline-Markdown-tabelon; ligu al `/${LINGVO}/tabelvortoj/`.

## Vortaro (`vortaro/*.yml`)

- Plibonigu kaj kompletigu tradukojn.
- Aldonu pli da akcepteblaj tradukoj kie utile.
- Uzu maksimume 3 tradukojn por unu Esperanta ero; uzu 4 nur se vere necesas.
- Preferu oftajn, naturajn tradukojn anstataŭ maloftajn aŭ tro vastajn
  sinonimojn.
- Ne forigu ĝustan ekzistantan tradukon krom se ĝi estas klare malĝusta aŭ
  misgvida.

## Ekzerco 1 (`ekzercoj/traduku/*.yml`)

- Plibonigu kaj kompletigu akcepteblajn respondojn.
- Aldonu oftajn variantojn, kiujn lernantoj verŝajne tajpus.
- Aldonu nur vere akcepteblajn variantojn.
- Ne aldonu tro vastajn sinonimojn, kiuj ŝanĝus la signifon.

## Fasado (`fasado/*.yml`)

- Plibonigu ankaŭ la tekstojn de la lingva startpaĝo en
  `fasado/cxefpagxo.yml`.
- Traduku ĉiujn videblajn fasadotekstojn, inkluzive de butonoj kaj mallongaj
  alvokoj kiel `{{lingvo_nombro}} lingvoj` kaj
  `Trovu Esperanto-parolantojn`.
- Konservu placeholder-ojn ekzakte, ekzemple `{{lingvo_nombro}}`; traduku nur
  la ĉirkaŭan tekston.
- Se la cellingvo bezonas alian vortordon ĉirkaŭ placeholder, ŝanĝu la ordon
  nature sed lasu la placeholder-on netuŝita.

## Formato kaj limigoj

- Konservu validan YAML-on kaj Markdown-on.
- Ne ŝanĝu dosiernomojn, ŝlosilojn, dosierujan strukturon aŭ generatoran kodon.
- Ne tuŝu dosierojn ekster `enhavo/tradukenda/${LINGVO}/**`.
- Se YAML-valoro povus esti interpretata speciale, metu ĝin inter citilojn (ekz.
  `on`, `off`, `yes`, valoroj kun apostrofoj aŭ dupunktoj).
- Konservu UTF-8 kaj la Esperantajn diakritajn signojn.

## Labormaniero

1. Ekde aktuala `master` kreu novan branĉon (neniam enmetu rekte al `master`).
2. Legu la dosierojn de la lingvo antaŭ ol redakti.
3. `make check` devas sukcesi antaŭ ĉiu enmeto.
4. Puŝu kaj kreu PR per `gh`, kun titolo kaj priskribo en Esperanto.
