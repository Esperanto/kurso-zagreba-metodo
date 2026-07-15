# Gramatikaj klarigoj

Koncernas `gramatiko/01.md` … `gramatiko/12.md`.

Konservu la temojn, la sekcian strukturon kaj la Esperanto-ekzemplojn de la
lingvo; plibonigu nur la prezenton.

- Dispecigu densajn tekstblokojn en skaneblan strukturon: subtitoloj, mallongaj
  alineoj kaj listeroj.
- Eksplicitigu la regulecon de Esperanto, ekzemple `-as` egala por ĉiuj
  personoj, posedaj pronomoj = pronomo + `-a`, la vokala sistemo `-o`/`-a`/`-e`,
  kaj la tempaj vokaloj `i`–`a`–`o`.
- Kontrastu kun la denaska lingvo de la lernanto.
- Aldonu memorhelpilojn kaj avertojn pri stumbliloj, kiujn parolantoj de la cela
  lingvo emas fari.
- Se vi aldonas aŭ ŝanĝas Esperantajn ekzemplojn, uzu nur bazan/fundamentan
  Esperanton.

Formataj konvencioj:

- Ĉio Esperanta estas kursiva: `*vorto*`, ankaŭ unuopaj literoj kaj finaĵoj.
- Novajn morfemojn marku grase per `__morfemo__`; ĉe enkonduko de nova
  finaĵo/afikso kombinu kursivon kaj grason: `*__-o__*`.
- Ene de ekzempla vorto la morfemo estas grasa: `patr__in__o`.
- Avertaj kaj memorhelpaj kestoj uzas konstantan ikonon kaj etikedon en la
  cellingvo:
  - `**⚠️ <averto>:**` por avertoj/stumbliloj
  - `**💡 <memorhelpilo>:**` por memorhelpiloj kaj konsiletoj
- Neniu ikono en titoloj; tio rompus la enhav-kontrolon
  `fonto/py/kontrolu_eligon.py`.
- Ekzemplojn post dupunkto metu kiel apartajn listerojn, ne inline.
- Ekzemplo-formato: Esperanto-vorto unue, traduko en krampoj, sago al la
  rezulto: `*skribi* (traduko) → *skribilo* (traduko)`.
- Krucreferencojn faru ligiloj: `[<leciono> 6](/${LINGVO}/06/gramatiko/)`.
- La tabelon de korelativoj ligu al `[<korelativoj>](/${LINGVO}/tabelvortoj/)`.
- Ne skribu nudan «(leciono 5)».
- Riparu fuŝan markadon, ekz. `*libr_ego_*` al `*libr__eg__o*`.
- Tabeloj ne rendiĝas en gramatiko; ne uzu inline-Markdown-tabelon, sed ligu al
  `/${LINGVO}/tabelvortoj/`.

La atendataj temoj por ĉiu leciono troviĝas en `gramatiko/01.yml` …
`gramatiko/12.yml`. Ĉiu dosiero estas simpla listo de Esperantaj temnomoj, ne
maŝinlegebla kontrolilo. Tiuj temoj estas minimuma postulo: estas tute en ordo,
se leciono enhavas pliajn klarigojn, ekzemplojn aŭ helpajn rimarkojn.

Kiam vi redaktas gramatikan lecionon, komparu ĝian Markdown-dosieron kun la
koncerna temlisto kaj certigu, ke ĉiuj temoj estas enhave kovritaj. Temo povas
aperi kiel propra titolo, subtitolo aŭ klara klariga sekcio; la vortumo ne devas
esti identa al la temnomo. Se temo ŝajnas manki aŭ troviĝi en alia leciono,
kontrolu tion aktive antaŭ PR kaj menciu la decidon en la PR-priskribo.
