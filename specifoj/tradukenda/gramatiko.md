# Gramatikaj klarigoj

Koncernas `gramatiko/01.md` … `gramatiko/12.md`.

Konservu la celon de la leciono kaj la kursan strukturon. Vi rajtas reordigi
sekciojn, aldoni klarigojn kaj ŝanĝi ekzemplojn, kiam tio helpas kovri la
temojn aŭ evitas antaŭdoni ekzerco-respondojn.

- Dispecigu densajn tekstblokojn en skaneblan strukturon: subtitoloj, mallongaj
  alineoj kaj listeroj.
- Gramatikaj klarigoj estas lernanto-videblaj klarigoj. Tial apliku la
  ĝeneralan regulon pri simpla lingvo.
- Eksplicitigu la regulecon de Esperanto, ekzemple `-as` egala por ĉiuj
  personoj, posedaj pronomoj = pronomo + `-a`, la vokala sistemo `-o`/`-a`/`-e`,
  kaj la tempaj vokaloj `i`–`a`–`o`.
- Klarigu el la perspektivo de parolantoj de la cela lingvo. Se Esperanta
  strukturo mankas en la cellingvo, funkcias alimaniere aŭ facile instigas
  eraron, donu apartan klarigon kun kontrasto kaj mallonga ekzemplo.
- Aldonu memorhelpilojn kaj avertojn pri stumbliloj, kiujn parolantoj de la cela
  lingvo emas fari.
- Por Esperantaj ekzemploj kaj vortelekto sekvu `uzataj-vortoj.md`.
- Ne antaŭdonu respondojn de la samlecionaj ekzercoj: en gramatika klarigo ne
  kopiu ekzaktajn traduk-taskajn vortojn kun iliaj tradukoj kiel ekzemplojn.
  Elektu oftan, jam konatan aŭ analogan ekzemplon por instrui la saman ŝablonon.

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
- Por vortfaradaj ekzemploj, skribu la bazan vorton, poste sagon al la nova
  vorto: `*skribi* (traduko) → *skribilo* (traduko)`.
- Por frazaj ekzemploj, skribu simplan Esperantan frazon kaj poste la tradukon.
- Krucreferencojn faru ligiloj: `[<leciono> 6](/${LINGVO}/06/gramatiko/)`.
- La tabelon de korelativoj ligu al `[<korelativoj>](/${LINGVO}/tabelvortoj/)`.
- Ne skribu nudan «(leciono 5)».
- Riparu fuŝan markadon, ekz. `*libr_ego_*` al `*libr__eg__o*`.
- Tabeloj ne rendiĝas en gramatiko; ne uzu inline-Markdown-tabelon, sed ligu al
  `/${LINGVO}/tabelvortoj/`.

La atendataj temoj por ĉiu leciono troviĝas en `gramatiko/01.yml` …
`gramatiko/12.yml`. Ĉiu dosiero estas homlegebla listo de gramatikaj
minimumoj, ne maŝinlegebla kontrolilo. Ĉiu ero havas `temo`, `subtemoj` kaj
`ekzemploj`. Tiuj temoj estas minimuma postulo: estas tute en ordo, se leciono
enhavas pliajn klarigojn, ekzemplojn aŭ helpajn rimarkojn.

La gramatiko devas doni al lernantoj la ilaron por solvi la ekzercojn de la
sama leciono. Tial la temlistoj inkluzivas ne nur klasikajn gramatikajn
titolojn, sed ankaŭ vortfaradajn ŝablonojn, frue bezonatajn tabelvortojn kaj
ekzerco-rilatajn uzotipojn. Kiam speca ekzemplo devenas el ekzerco, ne
transprenu ĝin kiel solvon en lernanto-videblan klarigon de la sama leciono;
elektu oftan aŭ jam konatan analogan ekzemplon, kiu instruas la saman ŝablonon.

Kiam vi redaktas gramatikan lecionon, komparu ĝian Markdown-dosieron kun la
koncerna temlisto kaj kun la ekzercoj de la sama leciono. Certigu, ke ĉiuj
temoj kaj subtemoj estas enhave kovritaj. Temo povas aperi kiel propra titolo,
subtitolo aŭ klara klariga sekcio; la vortumo ne devas esti identa al la
temnomo. La listigitaj ekzemploj montras atendatan specon de uzado, ne
devigajn frazojn. Se temo ŝajnas manki aŭ troviĝi en alia leciono, kontrolu
tion aktive antaŭ PR kaj menciu la decidon en la PR-priskribo.
