# Specifoj por tradukenda enhavo

Ĉi tiu dosierujo enhavas la stabilajn specifojn por tradukoj de la
Zagreba-metoda kurso. La celo estas konservi la kursan strukturon kaj samtempe
disigi la regulojn tiel, ke malgrandaj enhavaj ŝanĝoj ne koliziu en unu granda
prompta dosiero.

Por laboro pri unu lingvo:

1. Agordu `LINGVO`, ekzemple `LINGVO=de`.
2. Por ordinara lingva tasko, laboru nur en
   `enhavo/tradukenda/${LINGVO}/**`.
3. Legu la koncernajn specifojn en ĉi tiu dosierujo antaŭ redaktado.
4. Redaktu ĉi tiujn specifojn aŭ aliajn komunajn dosierojn nur se la tasko tion
   klare petas.
5. Ne ŝanĝu la netradukendan Esperantan fontenhavon.

Ĝeneralaj reguloj:

- Plibonigu tradukojn sen ŝanĝi la kursan strukturon.
- Korektu gramatikajn, ortografiajn, interpunkciajn kaj stilajn erarojn en la
  cela lingvo.
- Faru la videblan tekston natura, klara kaj lernanto-amika, sed restu fidele
  proksima al la Esperanta enhavo.
- Se kampo estas intence lernhelpa, ekzemple `rektatraduko`, sekvu ĝian apartan
  specifon.
- Konservu la ekzistantan tonon kaj rektan alparolon al lernantoj.
- Konservu validan YAML-on kaj Markdown-on.
- Ne ŝanĝu dosiernomojn, ŝlosilojn, dosierujan strukturon aŭ generatoran kodon,
  krom se aparta tasko eksplicite petas tion.
- Se YAML-valoro povus esti interpretata speciale, metu ĝin inter citilojn
  (ekz. `on`, `off`, `yes`, valoroj kun apostrofoj aŭ dupunktoj).
- Konservu UTF-8 kaj la Esperantajn diakritajn signojn.

Simpla lingvo por lernantoj:

- Klarigoj por lernantoj estu kiel eble plej simplaj.
- Uzu mallongajn frazojn.
- Uzu oftajn vortojn.
- Klarigu unu ideon post alia.
- Evitu nenecesajn fakvortojn. Se fakvorto estas bezonata, klarigu ĝin tuj.
- Disigu longajn frazojn en du aŭ pli da frazoj aŭ en liston.
- Preferu klaran ekzemplon al longa abstrakta klarigo.
- Ne metu tro multe da nova informo en unu loko.

Labormaniero:

1. Ekde aktuala `master` kreu novan branĉon; neniam enmetu rekte al `master`.
2. Legu la dosierojn de la lingvo antaŭ ol redakti.
3. Post YAML-redaktoj rulu la normaligilon laŭ la repo-instrukcioj.
4. Post gramatikaj ŝanĝoj komparu la lecionon kun la koncerna temlisto en
   `gramatiko/NN.yml`.
5. Por lingvospecifa laboro, uzu lingvolimitajn kontrolojn kiam eblas, ekzemple
   `make check-yaml LINGVO=${LINGVO}`,
   `make check-yaml-normalized LINGVO=${LINGVO}` kaj
   `make check-md-normalized LINGVO=${LINGVO}`. Se vi generis aŭ kontrolas
   PWA-eligon por unu lingvo, uzu ankaŭ `make check-pwa LINGVO=${LINGVO}`.
6. `make check` devas sukcesi antaŭ ĉiu enmeto, krom se la tasko estas klare
   limigita al lingvospecifaj kontroloj kaj la PR priskribas tion.
7. Puŝu kaj kreu PR per `gh`, kun titolo kaj priskribo en Esperanto.
