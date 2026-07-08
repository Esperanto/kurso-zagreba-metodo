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
- Antaŭ ol ŝanĝi radikajn tradukojn, konsultu
  `enhavo/netradukenda/radikaj_finajxoj.yml`: ĝi montras la bazan finaĵon /
  vortospecon de la radiko (`-o`, `-a`, `-i`, `-e` ktp.). Elektu tradukon, kiu
  kongruas kun tiu finaĵo; ekz. adjektiva radiko (`jun: a`) bezonas adjektivan
  tradukon, ne substantivan.
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

## Ekzerco 2 (`ekzercoj/traduku-kaj-respondu/*.yml`)

- Plibonigu la kampojn `demando` tiel, ke ili sonu nature en la cellingvo.
- Por `rektatraduko`, tamen konservu ĝin kiel **vort-post-vorta lernhelpa
  mapo**, ne kiel natura frazo. La lernanto devas laŭ la cellingva vorto povi
  rekoni, al kiu Esperanta vorto ĝi respondas.
- Ne kunfandu apartajn Esperantajn vortojn en unu natura cellingva esprimo se
  tio malklarigus la mapon. Ekz. traduku `Kiom` kaj `ofte` aparte anstataŭ
  kunigi ilin al natura esprimo kiel "kiom ofte".
- Ĉe prepozicioj elektu tradukon kiu montras la Esperantan funkcion, eĉ se la
  natura frazo uzus alian prepozicion. Ekz. en hispana `rektatraduko` por `per`
  taŭgas `por medio de`, ne la idioma prepozicio `en` el natura frazo.

## Fasado kaj lingva startpaĝo (`fasado/cxefpagxo.yml`)

La lingva startpaĝo (`/${LINGVO}/`) uzas tekstojn el `fasado/cxefpagxo.yml`.
Necesaj ŝlosiloj — ĉiuj devas ĉeesti kaj NE esti malplenaj:

- `Ek` (start-butono)
- `Lerni Esperanton` (la SEO-serĉfrazo "lerni Esperanton")
- `Lerni Esperanton en 12 lecionoj` (ĉeftitolo / h1)
- `Esperanto en 12 lecionoj` (titolo ankaŭ de aliaj paĝoj)
- `La plej rapida kurso por la bazoj` (subtitolo)
- `{{lingvo_nombro}} lingvoj` (lingvo-nombrilo)
- `Trovu Esperanto-parolantojn`

Reguloj:

- **Kompleteco:** ĉiu lingvo havu ĉiujn ĉi ŝlosilojn kun ne-malplena valoro.
  Plenigu mankantajn/malplenajn (plej ofte mankas `Lerni Esperanton`).
- **Ĝusta lingvo:** atentu loktenilojn kopiitajn el ALIA lingvo (ekz. franca en
  ne-franca dosiero, rusa en belarusa, angla en ne-tradukita, persa en kurda).
  Anstataŭigu per la cela lingvo. Se vi ne povas fidinde traduki la lingvon,
  **marku ĝin por kontrolo de denaskulo** anstataŭ diveni.
- **Titolo kun verbo (SEO):** `Lerni Esperanton en 12 lecionoj` enhavu la lernan
  verbon kaj tenu la serĉfrazon "lerni Esperanton" (= la valoro de
  `Lerni Esperanton`) kune. Konstruu ĝin el `Lerni Esperanton` + la
  "en N lecionoj"-parto (el `Esperanto en 12 lecionoj`). Ekz. de:
  `Esperanto lernen in 12 Lektionen`; es: `Aprender esperanto en 12 lecciones`.
  Por SOV-/CJK-lingvoj aranĝu la vortordon nature, sed tenu la serĉfrazon kune.
- **Placeholder-oj** (ekz. `{{lingvo_nombro}}`) restu netuŝitaj; ŝanĝu nur la
  ĉirkaŭan tekston/ordon laŭbezone.

## Enkonduko (`enkonduko.md`)

La enkonduka teksto de la startpaĝo venas el `enkonduko.md`. Prilaboru ĝin laŭ la
modelo de `enhavo/tradukenda/en/enkonduko.md` — samaj kernaj punktoj (kiom da
vortoj, senpaga / sen registriĝo, ligilo al la fiŝkartaro, kaj la fina alvoko
kiel "Provu ĝin!"). Konservu la Markdown-formaton kaj la placeholder-ojn
(`{{ url.kartaro }}`, `{{ url.anki }}`).

**Sed se iu lingvo jam havas pluan, netipan enhavon** (ekz. priskribon de la
kursostrukturo aŭ mencion pri mobil-optimumigo, kiel en `de/`), **lasu ĝin** —
nur korektu ĝin lingve kaj akordigu la kernon kun la angla.

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
