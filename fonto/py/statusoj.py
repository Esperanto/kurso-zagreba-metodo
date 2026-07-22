# -*- coding: utf-8 -*-

PUBLIKAJ_LINGVO_STATOJ = {'preta', 'beta'}
HTML_LINGVO_STATOJ = PUBLIKAJ_LINGVO_STATOJ | {'testa'}


def estas_publika_lingvo(lingvo):
    return lingvo.get('stato') in PUBLIKAJ_LINGVO_STATOJ


def estas_beta_lingvo(lingvo):
    return lingvo.get('stato') == 'beta'
