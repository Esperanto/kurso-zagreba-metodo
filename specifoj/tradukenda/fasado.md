# Fasado kaj lingva startpaĝo

Koncernas `fasado/cxefpagxo.yml`.

La lingva startpaĝo (`/${LINGVO}/`) uzas tekstojn el `fasado/cxefpagxo.yml`.
Necesaj ŝlosiloj — ĉiuj devas ĉeesti kaj ne esti malplenaj:

- `Ek` (start-butono)
- `Lerni Esperanton` (la SEO-serĉfrazo "lerni Esperanton")
- `Lerni Esperanton en 12 lecionoj` (ĉeftitolo / h1)
- `Esperanto en 12 lecionoj` (titolo ankaŭ de aliaj paĝoj)
- `La plej rapida kurso por la bazoj` (subtitolo)
- `{{lingvo_nombro}} lingvoj` (lingvo-nombrilo)
- `Trovu Esperanto-parolantojn`

Reguloj:

- Ĉiu lingvo havu ĉiujn ĉi ŝlosilojn kun ne-malplena valoro.
- Plenigu mankantajn aŭ malplenajn valorojn; plej ofte mankas
  `Lerni Esperanton`.
- Atentu loktenilojn kopiitajn el alia lingvo, ekzemple franca en ne-franca
  dosiero, rusa en belarusa, angla en ne-tradukita aŭ persa en kurda.
- Anstataŭigu alilingvajn restaĵojn per la cela lingvo.
- Se vi ne povas fidinde traduki la lingvon, marku ĝin por kontrolo de denaskulo
  anstataŭ diveni.
- `Lerni Esperanton en 12 lecionoj` enhavu la lernan verbon kaj tenu la
  serĉfrazon "lerni Esperanton" (= la valoro de `Lerni Esperanton`) kune.
- Konstruu la ĉeftitolon el `Lerni Esperanton` + la "en N lecionoj"-parto el
  `Esperanto en 12 lecionoj`.
- Por SOV-/CJK-lingvoj aranĝu la vortordon nature, sed tenu la serĉfrazon kune.
- Placeholder-oj, ekzemple `{{lingvo_nombro}}`, restu netuŝitaj; ŝanĝu nur la
  ĉirkaŭan tekston aŭ ordon laŭbezone.

Ekzemploj por la ĉeftitolo:

- Germana: `Esperanto lernen in 12 Lektionen`
- Hispana: `Aprender esperanto en 12 lecciones`
