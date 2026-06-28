import re
import unicodedata


def fari_ankron(teksto):
    teksto = unicodedata.normalize('NFKD', teksto)
    signoj = []
    previous_separator = False

    for signo in teksto.lower():
        if signo.isalnum():
            signoj.append(signo)
            previous_separator = False
        elif not previous_separator:
            signoj.append('-')
            previous_separator = True

    ankro = ''.join(signoj).strip('-')
    return ankro or 'sekcio'


def unika_ankro(teksto, uzitaj):
    ankro = fari_ankron(teksto)
    if ankro not in uzitaj:
        uzitaj[ankro] = 1
        return ankro

    uzitaj[ankro] += 1
    return ankro + '-' + str(uzitaj[ankro])


def forigu_html(teksto):
    return re.sub(r'<[^>]+>', '', teksto)
