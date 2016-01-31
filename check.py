import yaml
import jinja2
import markdown
import glob
import re
import mistune

enhavo = {}
enhavo['vortaro'] = {}

def transpose_headlines(markdown, level):
    prefix = ''
    for i in range(level):
        prefix += '#'
    markdown = re.sub(r'^#', '#' + prefix, markdown)
    markdown = re.sub(r'\n#', '\n#' + prefix, markdown)
    return markdown 


def get_markdown_headlines(s):

    headlines = []
    for match in  re.finditer(r'(^|\n)# (.+)\n', s):
        headlines.append(match.group(2).strip())

    return headlines

def load(language):

    enhavo = {}
    enhavo['vortaro'] = {}

    filenames = [
        'enhavo/tradukenda/de/vortaro/radiko.yml',
        'enhavo/tradukenda/de/vortaro/vorto.yml',
    ]
    for filename in filenames:
        vortlisto = yaml.load(file(filename, 'r'))
        enhavo['vortaro'].update(vortlisto)


    enhavo['fasado'] = {}
    filenames = [
        'enhavo/tradukenda/de/vortaro/radiko.yml',
        'enhavo/tradukenda/de/vortaro/vorto.yml',
    ]
    for filename in filenames:
        tradukajxoj = yaml.load(file(filename, 'r'))
        enhavo['fasado'].update(tradukajxoj)

    filename = 'enhavo/tradukenda/' + language + '/enkonduko.md'

    enkonduko = file(filename, 'r').read()
    enkonduko = unicode(enkonduko, 'utf-8')
    #enkonduko = transpose_headlines(enkonduko, 1)

    enhavo['enkonduko'] = enkonduko

    lecionoj = []

    for i in range(1,13):
        leciono = {
            'teksto': None,
            'gramatiko': None,
            'ekzercoj': None,
        }
        i_padded = str(i).zfill(2)
        
        leciono['indekso'] = {
            'cifre': i,
            'cxene': i_padded
        }

        filename = 'enhavo/netradukenda/tekstoj/' + i_padded + '.yml'
        leciono['teksto'] = yaml.load(file(filename, 'r'))

        # Create a string of the lesson titles.
        titolo_string = ''
        for radikoj in leciono['teksto']['titolo']:
            if radikoj:
                titolo_string += ''.join(radikoj)
            else:
                titolo_string += ' '
        
        leciono['teksto']['titolo_string'] = titolo_string

        filename = 'enhavo/tradukenda/' + language + '/gramatiko/' + i_padded + '.md'

        gramatiko_teksto = file(filename, 'r').read()
        gramatiko_teksto = unicode(gramatiko_teksto, 'utf-8')
        gramatiko_titoloj = get_markdown_headlines(gramatiko_teksto)
        gramatiko_teksto = transpose_headlines(gramatiko_teksto, 2)


        gramatiko = {
            'teksto': gramatiko_teksto,
            'titoloj': gramatiko_titoloj,
        }
        leciono['gramatiko'] = gramatiko

        ekzercoj = {}

        filename = 'enhavo/tradukenda/' + language + '/ekzercoj/traduku/' + i_padded + '.yml'
        ekzercoj['Traduku'] = yaml.load(file(filename, 'r'))

        filename = 'enhavo/tradukenda/' + language + '/ekzercoj/traduku-kaj-respondu/' + i_padded + '.yml'
        ekzercoj['Traduku kaj respondu'] = yaml.load(file(filename, 'r'))

        filename = 'enhavo/netradukenda/ekzercoj/kompletigu-la-frazojn/' + i_padded + '.yml'
        ekzercoj['Kompletigu la frazojn'] = yaml.load(file(filename, 'r'))


        # Covert from dict to list.
        leciono['ekzercoj'] = ekzercoj

        lecionoj.append(leciono)

    enhavo['lecionoj'] = lecionoj

    return enhavo

enhavo = load('de')
# TItel mitdurchsuchen
# nur radikoj und vortoj
for i in range(12):
    for vortoj in enhavo['lecionoj'][i]['teksto']['paragrafoj']:
        for vorto in vortoj:
            if vorto:
                if type(vorto) is list:
                    if ''.join(vorto) in enhavo['vortaro']:
                        enhavo['vortaro'].pop(''.join(vorto))
                    if ''.join(vorto).lower() in enhavo['vortaro']:
                        enhavo['vortaro'].pop(''.join(vorto).lower())
                    for radiko in vorto:
                        if radiko in enhavo['vortaro']:
                            enhavo['vortaro'].pop(radiko)
                        if radiko.lower() in enhavo['vortaro']:
                            enhavo['vortaro'].pop(radiko.lower())

for vorto in enhavo['vortaro'].keys():
    print vorto

exit()
