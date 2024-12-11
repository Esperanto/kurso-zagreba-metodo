# Kiel helpi

Saluton! Unue, dankon pro via emo helpi kun ĉi tiu kurso! Jen kiel fari tion:

## Kreu konton ĉe GitHub

1. Bonvolu iri al https://github.com/join kaj krei (senpagan) personan konton.
2. Sendu vian uzantnomon al georg@jaehnig.org kaj skribu ankaŭ:
   - al kiu lingvo vi volas traduki,
   - kiun ekzistantan similan lingvon vi volas uzi kiel ĝermon (normale oni elektas la anglan, sed ekzemple, se vi volas traduki al la indonezia, indus elekti la similan malajan).
3. Atendu mian respondon. :)

## Akceptu la inviton al la teamo

Kiam mi ricevos vian mesaĝon, mi invitos vin al la Esperanta teamo ĉe GitHub. Mi informos vin kiam mi faros tion. Por akcepti la inviton:

1. Iru al https://github.com/Esperanto kaj alklaku "View invitation".
2. En la sekva paĝo, alklaku "Join Esperanto".

## Kontrolu, ĉu traduko al via lingvo jam ekzistas

La [Zagreba Metodo](https://eo.wikipedia.org/wiki/Zagreba_metodo) jam estas tradukita al multaj lingvoj. Plej bone estas, ke vi ne mem traduku al via lingvo, sed trovu tradukaĵon al tiu lingvo.  

La tradukaĵoj ĝis nun estas eldonitaj nur en libra formo. Kelkaj skanaĵoj ekzistas:

- [angla](http://esperantofre.com/zagreb/zagreba.htm)
- [bulgara, finna, hispana, itala, korea, kroata, makedona (nekompleta), pola, rumana, slovaka, svahila, vjetnama kaj aliaj](https://mega.nz/folder/kchTHKwD#4EtlaUyMuPqEbx5No-qgAw)

(Se vi havas pli da skanaĵoj, bonvolu aldoni ilin aŭ [informu min](mailto:georg@jaehnig.org)!)

## Tradukado

Nun ek al la tradukado!

### Ĝenerale: kiel redakti

1. Bonvolu iri al la dosierujo, kiun mi kreis por la nova lingvo. (Mi sendis la ligilon en mia retpoŝto al vi.)
2. Eniru la dosierujon kaj malfermu la dosieron, kiun vi volas traduki (simple alklaku ĝin).
3. Redaktu la dosierojn: alklaku la redaktu-butonon:

![Redaktu](redaktu.png)

### Ekzercoj

Estas plej bone komenci per la ekzercoj:

#### Ekzerco 1 

1. Iru al `/ekzercoj/traduku` kaj malfermu `01.yml`. Nun vi vidas la fontdosieron de la [unua ekzerco](https://esperanto12.net/en/01/ekzerco1/).
2. Traduku la Esperantajn vortojn al la nova lingvo:
   - Forigu la anglajn vortojn.
   - En ilian lokon, entajpu la vortojn de la nova lingvo.

Se via nova lingvo havas nur unu tradukaĵon, skribu unu linion, ekzemple:

    - enskribi: to register

Se via nova lingvo havas pli ol unu tradukaĵon, skribu pli da linioj, ekzemple:

    - enskribi: 
      - to register
      - to inscribe

Finfine, alklaku "Commit changes" sube por konservi viajn ŝanĝojn.

Same, traduku la aliajn dosierojn en `/ekzercoj/traduku`. Plej bone estas, se vi ĉiam skribas multajn eblajn tradukaĵojn por ĉiu vorto. Tiel ĉiuj eblaj respondoj de la estontaj lernantoj estos ĝustaj.

#### Vortaro 

Simile, traduku ĉiujn dosierojn en `/vortaro`.

#### Ekzerco 3

En `/ekzercoj/traduku-kaj-respondu`, ni tradukas la [trian ekzercon](https://esperanto12.net/en/01/ekzerco3/). Por ĉiu traduko, vi vidas du liniojn:

    demando:
    rektatraduko:

En la linio `demando:`, skribu bonsonan frazon en via lingvo, ekzemple:

    demando: Does friendship make you more happy than love does?

En la linio `rektatraduko:`, skribu laŭvortan tradukon en via lingvo. Ĝi ne devas esti bonsona aŭ eĉ gramatike ĝusta. Ĝi nur celas informi la lernanton, kiujn Esperantajn vortojn li aŭ ŝi uzu. Ekzemple:

    rektatraduko: 
      - Ĉu: Whether
      - amikeco: friendship
      - pli: more
      - feliĉigas: makes happy
      - vin: you
      - ol: than
      - la: the
      - amo: love
      - '?'

Estas tre utile uzi la samajn vortojn kiel en viaj tradukoj en `/vortaro`. Sed rimarku, ke tie oni bezonas **nur unu** tradukaĵon por ĉiu vorto.

Se via lingvo tute ne havas laŭvortan tradukon por kelkaj Esperantaj vortoj, skribu ian klarigon. Ekzemple, se la angla ne havus la vorton "the", oni povus skribi:

      - la: (definite article)

Denove: La celo estas, ke la lernanto sciu, kion li aŭ ŝi skribu.

#### Se iu traduko ne aperas

Foje vi devas uzi citilojn, ekzemple:

    vorto: "on"

Ĉar `on` estas angla vorto, la dosierformato interpretas ĝin kiel bulea valoro (boolean) kaj pensas, ke ĝi signifas `TRUE`. Tial vi devas uzi citilojn: `"on"`.

Alia ekzemplo:

    vorto: "apostrophe's translation"

Se vi uzas apostrofon en la tradukaĵo, uzu citilojn ĉirkaŭ ĝi.

### Gramatiko

La gramatikaj klarigoj estas en la dosierujo `/gramatiko`. Ili estas skribitaj en [Markdown](https://en.wikipedia.org/wiki/Markdown).

Ĉi tie vi havas plenan liberecon pri la enhavo: vi povas aldoni ekzemplojn kaj klarigojn laŭbezone. Eble la parolantoj de via lingvo bezonos aliajn klarigojn ol tiuj, kiuj jam ekzistas en la ĝerma lingvo. Adaptu ilin laŭ via gusto.

- Por ĉiu leciono, kreu dosieron kun la leciona indekso. Ekzemple:
  - `01.md` - Klarigo pri leciono 1
  - `02.md` - Klarigo pri leciono 2
  - ktp.
- Skribu ĉion en Esperanto uzante `*`, ekzemple:
  - `*bona lingvo*`
- Disigu Esperanton kaj la tradukon per `–` (paŭzostreko), ne per `-`. Ekzemple:
  - `*bona lingvo* – good language`
- Vortojn aŭ literojn, kiujn vi klarigas, emfazigu per `__`. Ekzemple:
  - `The morpheme *-ej* denotes a place, for example *lern__ej__o* – school`
- Se vi dubas, rigardu la [germanan version](de/).

Ne zorgu, se GitHub foje malĝuste prezentas partojn de Markdown (ekz. kombinadojn kiel `*lern__ej__o*`) montrante la Markdown-dosierojn en sia retejo. Tio estas nur problemo de GitHub; nia kreanta skripto tamen ĝuste interpretos ilin.
