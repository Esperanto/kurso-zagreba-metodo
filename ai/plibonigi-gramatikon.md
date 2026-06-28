# Prompto: plibonigi la gramatikajn klarigojn de lingvo

Ĉi tiu dokumento estas reuzebla prompto. Ĝi priskribas ĉiujn lingvajn kaj
redaktajn plibonigojn, kiujn ni jam aplikis al la gramatikaj lecionoj de la
germana (`enhavo/tradukenda/de/gramatiko/`) kaj la angla
(`enhavo/tradukenda/en/gramatiko/`). Uzu ĝin por apliki la samajn plibonigojn
al alia lingvo.

---

## Via tasko

Vi plibonigas la gramatikajn klarigojn de la lingvo **[LINGVO-KODO]** en
`enhavo/tradukenda/[LINGVO-KODO]/gramatiko/01.md` … `12.md`. Plibonigu la
**prezenton** laŭ bonaj pedagogiaj normoj, **sen ŝanĝi la instruatan enhavon**.
Ĉiu leciono plu transdonu ekzakte la samajn temojn kaj la samajn
Esperanto-ekzemplojn kiel antaŭe — nur la klarigoj, la strukturo kaj la
prezento pliboniĝu.

## Kio NE rajtas ŝanĝiĝi

- Ne aldonu, ne forigu kaj ne movu gramatikajn temojn inter la lecionoj.
- Konservu ĉiujn Esperanto-ekzemplojn (la ekzemplajn vortojn kaj frazojn).
- Konservu la ekzistantajn tradukojn de la ekzemploj.
- Ne ŝanĝu la ĝentilecan alparolon (ci/vi k.s.) sen neceso.
- Konservu la sekcian strukturon de la traktata lingvo. La lingvoj **ne** havas
  identan strukturon (ekz. la angla havas plenan sekcion «Alphabet»;
  la germana havas aliajn sekciojn). Sekvu la strukturon de la traktata lingvo.

## Principoj de plibonigo

1. **Dispecigu densajn tekstblokojn** en skaneblan strukturon: subtitoloj,
   mallongaj alineoj, listeroj.
2. **Eksplicitigu la regulecon de Esperanto** — tio estas la ĉefa pedagogia
   forto. Ekzemploj: la finaĵo `-as` estas egala por ĉiuj personoj; posedaj
   pronomoj = pronomo + `-a`; la vokala sistemo `-o`/`-a`/`-e`; la tempaj
   vokaloj `i`–`a`–`o` (`-is`/`-as`/`-os`); la kompleta aro de verbaj finaĵoj.
3. **Kontrastu kun la denaska lingvo de la lernanto.** Montru la helpajn
   paralelojn kaj avertu pri la diferencoj (vidu la lingvo-specifajn notojn
   sube).
4. **Aldonu memorhelpilojn** — komencu ilin prefere per la Esperanto-vorto.
5. **Aldonu avertojn pri stumbliloj** — mallongajn notojn pri eraroj, kiujn
   parolantoj de tiu lingvo emas fari.

## Formataj konvencioj

- **Ĉio Esperanta estas kursiva**: `*vorto*` (ankaŭ unuopaj literoj kaj finaĵoj).
- **Novajn morfemojn marku grase** per `__morfemo__` (rendiĝas grase). Ĉe la
  enkonduko de nova finaĵo/afikso (en titolo aŭ teksto) kombinu kursivon+grason:
  `*__-o__*`. Ene de ekzempla vorto la morfemo estas grasa: `patr__in__o`.
- **Avertaj kaj memorhelpaj kestoj kun ikonoj.** La ikono estas ĉiam la sama por
  la sama tipo; la etikedan tekston traduku en la cellingvon:
  - `**⚠️ <averto>:**` — por avertoj/stumbliloj (ekz. angle «Watch out»,
    germane «Achtung»).
  - `**💡 <memorhelpilo>:**` — por memorhelpiloj kaj konsiletoj (ekz. angle
    «Memory aid» / «Tip», germane «Merke» / «Eselsbrücke» / «Tipp»).
- **Neniu ikono en titoloj.** Tio rompus la enhav-kontrolon
  `fonto/py/kontrolu_eligon.py`, kiu atendas ekzakte ekz. `<h3>Alphabet</h3>`.
- **Ekzemplojn metu kiel listerojn.** Kiam kesto enkondukas ekzemplo(j)n per
  dupunkto, metu ĉiun ekzemplon en apartan listeron — ne inline. Ekzemple:

  ```markdown
  **💡 <memorhelpilo>:** *-ec* respondas al ...:

  - *bela* (traduko) → *beleco* (traduko)
  ```

- **Formato de ekzemplo**: komencu per la Esperanto-vorto, traduko en krampoj,
  poste sago al la rezulto: `*skribi* (traduko) → *skribilo* (traduko)`.
  Evitu la malan ordon, ekz. «per kio oni skribas (*skribi*) → *skribilo*».
- **Krucreferencojn faru ligiloj.** Referencante alian lecionon, ligu ĝin:
  `[<leciono> 6](/[LINGVO-KODO]/06/gramatiko/)`. Referencu la tabelon de
  korelativoj per ligilo al la apendico:
  `[<korelativoj>](/[LINGVO-KODO]/tabelvortoj/)`. Ne skribu nudan «(leciono 5)».

## Teknikaj reguloj

- Dosieroj: `enhavo/tradukenda/[LINGVO-KODO]/gramatiko/01.md` … `12.md`.
- Markdown-rendado: `*x*` → kursiva; `__x__` → grasa (propra morfema emfazo);
  `**x**` → grasa.
- **Tabeloj ne rendiĝas** (mankas tabela kromaĵo en mistune). Por la korelativoj
  ne uzu inline-Markdown-tabelon — ligu al `/[LINGVO-KODO]/tabelvortoj/` (aŭ
  sekvu la ekzistantan aliron de la lingvo).
- Lecion-URL: `/[LINGVO-KODO]/0N/gramatiko/` (du-cifere). Apendico de
  korelativoj: `/[LINGVO-KODO]/tabelvortoj/`.
- Riparu fuŝan markadon, ekz. `*libr_ego_*` (unuopaj substrekoj → kursiva «ego»)
  al `*libr__eg__o*` (ĝusta grasa morfemo).
- Rulu `make check` antaŭ ĉiu commit. Por vide kontroli unu lingvon:
  `make html LINGVO=[LINGVO-KODO]`, poste rigardu
  `eligo/retejo/[LINGVO-KODO]/0N/gramatiko/`.

## Lingvo-specifaj kontrastoj

Trovu por la nova lingvo la analogajn paralelojn kaj stumblilojn. Utilaj
demandoj: ĉu la lingvo havas artikolojn? kazojn (kaj kiom)? gramatikan genron?
fiksan aŭ liberan akcenton? duoblan negacion? Kiuj literoj/sonoj de la lingvo
respondas al la Esperantaj?

**La germana (de)** — jam farita:

- Prononco: *eŭ* ≠ germana «eu/oj»; *v* = w; *c* = z; *z* = voĉa s.
- *-in* kiel germana «-in» (Lehrerin); akcento sur la antaŭlasta silabo «kiel en
  la itala».
- Mankas nedifina artikolo; *ne* staras antaŭ la verbo.

**La angla (en)** — jam farita:

- Prononco: *c* = ts, *j* = y, *g* ĉiam malmola; puraj vokaloj (ne diftongigu).
- Pluralo *-j*, ne *-s*; neniu 3-persona *-s* (*li sidas*); *-in* ≈ «-ine»
  (hero → heroine); *-ist* kiel «-ist»; *mal-* kiel «malfunction».
- *da*, ne *de*; neniu duobla negacio.

**Ekzemplo por estonta lingvo — la rusa (ru):**

- Sonoj: *c*/*ĉ*/*ŝ*/*ĵ*/*ĥ* respondas al ц/ч/ш/ж/х (granda avantaĝo).
- *si* ↔ себя, *sia* ↔ свой; moviĝa akuzativo *en domon* ↔ «в дом».
- Nur 2 kazoj anstataŭ 6; fiksa akcento (la rusa havas liberan) — malstreĉigo.
- **Averto:** la rusa havas duoblan negacion, kiun Esperanto **ne** havas.

## Labormaniero

1. Ekde aktuala `master` kreu novan branĉon (neniam committu rekte al `master`).
2. Legu ĉiujn 12 dosierojn de la lingvo por kompreni ĝian strukturon **antaŭ** ol
   redakti.
3. Apliku la principojn supre, konservante la enhavon.
4. `make check` devas sukcesi.
5. Pushu kaj kreu PR per `gh`, kun titolo kaj priskribo en Esperanto.

## Referencoj

Rigardu kiel finitajn ekzemplojn:

- `enhavo/tradukenda/de/gramatiko/` (la germana)
- `enhavo/tradukenda/en/gramatiko/` (la angla)
