import argparse
import re
import sys
from pathlib import Path
from typing import Optional

SKRIPT_DOSIERUJO = Path(__file__).resolve().parent
sys.path = [
    vojo for vojo in sys.path if Path(vojo or ".").resolve() != SKRIPT_DOSIERUJO
]

import html
import yaml
from lxml import etree as ET


DTD_ENTOJ = {}

EO_ALFABETO = "aàábcĉdeèéſfgeĝhĥijĵklmnoprsŝtuŭvxyz"
EO_ORDO = {dok: i for i, dok in enumerate(EO_ALFABETO)}
ENTO_STRIKTO = re.compile(r"&[a-zA-Z0-9_#-]+;")


def eo_sort_klavo(teksto: str):
    return [EO_ORDO.get(c, ord(c)) for c in teksto.lower()]


def sargi_ciujn_dtd_entojn(baz_dosierujoj: list[Path]):
    global DTD_ENTOJ

    dtd_dosieroj = []
    for baz_dosierujo in baz_dosierujoj:
        if baz_dosierujo.exists():
            dtd_dosieroj.extend(baz_dosierujo.glob("**/*.dtd"))

    if not dtd_dosieroj:
        print(
            "[Averto] Neniu .dtd-dosiero trovita. Entoj estos tradukitaj nur per norma HTML."
        )
        return

    ent_strikto = re.compile(r'<!ENTITY\s+([a-zA-Z0-9_-]+)\s+["\']([^"\']+)["\']\s*>')
    krudaj_entoj = {}

    for dtd_dosiero in dtd_dosieroj:
        try:
            enhavo = dtd_dosiero.read_text(encoding="utf-8", errors="ignore")
            for nomo, valoro in ent_strikto.findall(enhavo):
                krudaj_entoj[f"&{nomo};"] = valoro
        except OSError as err:
            print(f"[Averto] Ne eblis legi DTD-dosieron {dtd_dosiero.name}: {err}")

    sangita = True
    iteracioj = 0
    while sangita and iteracioj < 10:
        sangita = False
        iteracioj += 1
        for nomo, valoro in list(krudaj_entoj.items()):
            nova_valoro = valoro
            for sub_nomo, sub_valoro in krudaj_entoj.items():
                if sub_nomo in nova_valoro:
                    nova_valoro = nova_valoro.replace(sub_nomo, sub_valoro)
                    sangita = True

            malkodita_valoro = html.unescape(nova_valoro)
            if malkodita_valoro != valoro:
                sangita = True

            krudaj_entoj[nomo] = malkodita_valoro

    DTD_ENTOJ = krudaj_entoj
    print(
        f"-> Ŝargis {len(DTD_ENTOJ)} DTD-entojn el {len(dtd_dosieroj)} DTD-dosiero(j)."
    )


def anstataui_enton(trafo: re.Match) -> str:
    ento = trafo.group(0)
    if ento in DTD_ENTOJ:
        return DTD_ENTOJ[ento]

    malkodita = html.unescape(ento)
    if malkodita != ento:
        return malkodita

    if ento.startswith("&") and ento.endswith(";") and len(ento) > 3:
        interna = ento[1:-1]
        if interna[0].isupper():
            return ""

    return ento


def malkodigi_revo_tekston(kruda_teksto: str) -> str:
    if not kruda_teksto:
        return ""
    teksto = ENTO_STRIKTO.sub(anstataui_enton, kruda_teksto)
    return " ".join(teksto.split())


def kunmeti_eo_vorton(radiko: str, elemento: ET.Element) -> str:
    vort_partoj = []
    if elemento.text:
        vort_partoj.append(elemento.text)

    for infano in elemento:
        if infano.tag == "rad":
            if infano.text:
                vort_partoj.append(infano.text)
        elif infano.tag == "tld":
            vort_partoj.append(radiko)

        if infano.tail:
            vort_partoj.append(infano.tail)

    kruda_vorto = "".join(vort_partoj)
    pura_vorto = re.sub(r"[/]", "", kruda_vorto)
    return malkodigi_revo_tekston(pura_vorto)


def eltrahi_cxefajn_tradukojn(
    elemento: ET.Element, cel_lingvo: Optional[str] = None
) -> list[tuple[str, str]]:
    tradukoj = []
    for infano in elemento:
        if infano.tag == "ekz":
            continue

        if infano.tag == "trd":
            lng = infano.get("lng")
            if lng and (cel_lingvo is None or lng == cel_lingvo):
                teksto = malkodigi_revo_tekston("".join(infano.itertext()))
                if teksto:
                    tradukoj.append((lng, teksto))

        elif infano.tag == "trdgrp":
            lng = infano.get("lng")
            if lng and (cel_lingvo is None or lng == cel_lingvo):
                for trd in infano.findall("trd"):
                    teksto = malkodigi_revo_tekston("".join(trd.itertext()))
                    if teksto:
                        tradukoj.append((lng, teksto))

        elif infano.tag in ("snc", "subart", "dif", "rim"):
            tradukoj.extend(eltrahi_cxefajn_tradukojn(infano, cel_lingvo))

    return tradukoj


def prilabori_ekzemplajn_tradukojn(
    patra_elemento: ET.Element,
    radiko: str,
    mult_lingva_dikt: dict,
    cel_lingvo: Optional[str] = None,
):
    for ekz in patra_elemento.findall(".//ekz"):
        ind = ekz.find("ind")
        if ind is None:
            continue

        eo_vorto = kunmeti_eo_vorton(radiko, ind)
        if not eo_vorto:
            continue

        for infano in ekz:
            if infano.tag == "trd":
                lng = infano.get("lng")
                if lng and (cel_lingvo is None or lng == cel_lingvo):
                    traduko = malkodigi_revo_tekston("".join(infano.itertext()))
                    if traduko:
                        aldoni_tradukon(mult_lingva_dikt, lng, eo_vorto, traduko)
            elif infano.tag == "trdgrp":
                lng = infano.get("lng")
                if lng and (cel_lingvo is None or lng == cel_lingvo):
                    for trd in infano.findall("trd"):
                        traduko = malkodigi_revo_tekston("".join(trd.itertext()))
                        if traduko:
                            aldoni_tradukon(mult_lingva_dikt, lng, eo_vorto, traduko)


def aldoni_tradukon(mult_dikt: dict, lng: str, eo_vorto: str, traduko: str):
    if lng not in mult_dikt:
        mult_dikt[lng] = {}
    if eo_vorto not in mult_dikt[lng]:
        mult_dikt[lng][eo_vorto] = []
    if traduko not in mult_dikt[lng][eo_vorto]:
        mult_dikt[lng][eo_vorto].append(traduko)


def analizi_xml_dosieron(
    dosier_vojo: Path, mult_lingva_dikt: dict, cel_lingvo: Optional[str] = None
):
    try:
        xml_enhavo = dosier_vojo.read_text(encoding="utf-8", errors="ignore")
        xml_enhavo = ENTO_STRIKTO.sub(anstataui_enton, xml_enhavo)
        analizilo = ET.XMLParser(recover=True, resolve_entities=False)
        radiko_elem = ET.fromstring(xml_enhavo.encode("utf-8"), analizilo)
    except Exception as err:
        print(f"\n[Averto] Eraro dum analizo de {dosier_vojo.name}: {err}")
        return

    if radiko_elem is None:
        return

    rad_elem = radiko_elem.find(".//rad")
    if rad_elem is None or not rad_elem.text:
        return
    radiko = malkodigi_revo_tekston(rad_elem.text)

    for drv in radiko_elem.findall(".//drv"):
        kap = drv.find("kap")
        if kap is None:
            continue

        eo_vorto = kunmeti_eo_vorton(radiko, kap)
        if not eo_vorto:
            continue

        cxefaj_tradukoj = eltrahi_cxefajn_tradukojn(drv, cel_lingvo)
        for lng, traduko in cxefaj_tradukoj:
            aldoni_tradukon(mult_lingva_dikt, lng, eo_vorto, traduko)

        prilabori_ekzemplajn_tradukojn(drv, radiko, mult_lingva_dikt, cel_lingvo)


def konservi_yaml(lng: str, eo_dikt: dict, eliga_dosierujo: Path):
    eliga_dosiero = eliga_dosierujo / f"{lng}.yml"

    formatita_dikt = {}
    for klavo in sorted(eo_dikt.keys(), key=eo_sort_klavo):
        valoroj = eo_dikt[klavo]
        if len(valoroj) == 1:
            formatita_dikt[klavo] = valoroj[0]
        else:
            formatita_dikt[klavo] = valoroj

    with eliga_dosiero.open("w", encoding="utf-8") as dosiero:
        yaml.dump(
            formatita_dikt,
            dosiero,
            allow_unicode=True,
            sort_keys=False,
            default_flow_style=False,
        )


def analizi_argumentojn():
    analizilo = argparse.ArgumentParser(
        description="Eltrahas vortarajn enigojn el Revo-XML-dosieroj."
    )
    analizilo.add_argument(
        "pozicia_lingvo", nargs="?", help="Volata lingvokodo, ekzemple 'de'."
    )
    analizilo.add_argument(
        "--lingvo", help="Volata lingvokodo. Se mankas, prilaboras ĉiujn lingvojn."
    )
    analizilo.add_argument(
        "--revo-fonto", type=Path, default=Path("submoduloj/revo-fonto")
    )
    analizilo.add_argument(
        "--voko-grundo", type=Path, default=Path("submoduloj/voko-grundo")
    )
    analizilo.add_argument("--eligo-dir", type=Path, default=Path("eligo/revo"))
    return analizilo.parse_args()


def main():
    argumentoj = analizi_argumentojn()
    cel_lingvo = argumentoj.lingvo or argumentoj.pozicia_lingvo
    cel_lingvo = cel_lingvo.lower() if cel_lingvo else None

    eliga_dosierujo = argumentoj.eligo_dir
    eliga_dosierujo.mkdir(parents=True, exist_ok=True)

    sargi_ciujn_dtd_entojn([argumentoj.revo_fonto, argumentoj.voko_grundo])

    font_dosierujo = argumentoj.revo_fonto / "revo"
    if not font_dosierujo.exists():
        print(f"Eraro: Dosierujo '{font_dosierujo}' ne ekzistas.")
        sys.exit(1)

    xml_dosieroj = sorted(font_dosierujo.glob("**/*.xml"))
    total_files = len(xml_dosieroj)

    if cel_lingvo:
        print(
            f"Iras tra {total_files} XML-dosieroj nur por la lingvo: '{cel_lingvo}'...\n"
        )
    else:
        print(f"Iras tra {total_files} XML-dosieroj por ĉiuj lingvoj en unu paŝo...\n")

    mult_lingva_dikt = {}

    for indekso, xml_dosiero in enumerate(xml_dosieroj, start=1):
        if indekso % 500 == 0 or indekso == total_files:
            sys.stdout.write(
                f"\rProgreso: [{indekso}/{total_files}] XML-dosieroj prilaboritaj..."
            )
            sys.stdout.flush()

        analizi_xml_dosieron(xml_dosiero, mult_lingva_dikt, cel_lingvo)

    print(f"\n\nKonservas YAML-dosierojn en '{eliga_dosierujo}/'...")

    if not mult_lingva_dikt:
        print("[Averto] Neniu traduko trovita.")
        return

    for lng, eo_dikt in mult_lingva_dikt.items():
        konservi_yaml(lng, eo_dikt, eliga_dosierujo)
        print(
            f"-> '{eliga_dosierujo / f'{lng}.yml'}' konservita kun {len(eo_dikt)} vortoj."
        )

    print("\n-> Sukceso! Ĉiuj petitaj YAML-dosieroj estas skribitaj.")


if __name__ == "__main__":
    main()
