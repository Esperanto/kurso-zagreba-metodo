# Specifoj por tradukenda enhavo

Ĉi tiu dosierujo enhavas la stabilajn specifojn por tradukoj de la
Zagreba-metoda kurso. La celo estas konservi la kursan strukturon kaj samtempe
disigi la regulojn tiel, ke malgrandaj enhavaj ŝanĝoj ne koliziu en unu granda
prompta dosiero.

Por laboro pri unu lingvo:

1. Agordu `LINGVO`, ekzemple `LINGVO=de`.
2. Laboru nur en `enhavo/tradukenda/${LINGVO}/**`.
3. Legu la koncernajn specifojn en ĉi tiu dosierujo antaŭ redaktado.
4. Ne ŝanĝu la netradukendan Esperantan fontenhavon.

Ĝeneralaj reguloj:

- Plibonigu tradukojn sen ŝanĝi la kursan strukturon.
- Korektu gramatikajn, ortografiajn, interpunkciajn kaj stilajn erarojn en la
  cela lingvo.
- Faru la tradukitan tekston natura, klara kaj lernanto-amika, sed restu fidele
  proksima al la Esperanta enhavo.
- Konservu la ekzistantan tonon kaj rektan alparolon al lernantoj.
- Konservu validan YAML-on kaj Markdown-on.
- Ne ŝanĝu dosiernomojn, ŝlosilojn, dosierujan strukturon aŭ generatoran kodon,
  krom se aparta tasko eksplicite petas tion.
- Se YAML-valoro povus esti interpretata speciale, metu ĝin inter citilojn
  (ekz. `on`, `off`, `yes`, valoroj kun apostrofoj aŭ dupunktoj).
- Konservu UTF-8 kaj la Esperantajn diakritajn signojn.

Labormaniero:

1. Ekde aktuala `master` kreu novan branĉon; neniam enmetu rekte al `master`.
2. Legu la dosierojn de la lingvo antaŭ ol redakti.
3. Post YAML-redaktoj rulu la normaligilon laŭ la repo-instrukcioj.
4. Post gramatikaj ŝanĝoj komparu la lecionon kun la koncerna temlisto en
   `gramatiko/NN.yml`.
5. `make check` devas sukcesi antaŭ ĉiu enmeto.
6. Puŝu kaj kreu PR per `gh`, kun titolo kaj priskribo en Esperanto.
