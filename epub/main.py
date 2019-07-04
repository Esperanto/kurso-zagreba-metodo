# -*- coding: utf-8 -*-

import os
import shutil
import re
import pypandoc

def write_epub_pdf_file(filename, content, papersize="a4"):
    dirname = os.path.dirname(filename)
    if not os.path.exists(dirname):
        os.makedirs(dirname)

    open(filename + '.md', 'w').write(content)
    pypandoc.convert_text(content, 'epub', format='md', outputfile=filename + '.epub')
    if papersize=="a5":
        pypandoc.convert_text(content, 'pdf', format='md',  outputfile=filename + '.pdf', extra_args=["--latex-engine=xelatex", "-V", "margin-top=1cm", "-V", "margin-bottom=1cm", "-V", "margin-right=1.3cm", "-V", "margin-left=1.3cm", "-V", "papersize:a5"])
    elif papersize=="letterpaper":
        pypandoc.convert_text(content, 'pdf', format='md',  outputfile=filename + '.pdf', extra_args=["--latex-engine=xelatex", "-V", "margin-top=2.54cm", "-V", "margin-bottom=2.54cm", "-V", "margin-right=2.54cm", "-V", "margin-left=2.54cm", "-V", "papersize:letterpaper"])
    else:
        pypandoc.convert_text(content, 'pdf', format='md',  outputfile=filename + '.pdf', extra_args=["--latex-engine=xelatex", "-V", "margin-top=2.54cm", "-V", "margin-bottom=2.54cm", "-V", "margin-right=2.54cm", "-V", "margin-left=2.54cm", "-V", "papersize:a4"])

def generate_lekcio(lekcio, lekcio_numero):
    libro = ""
    libro += "# Lekcio {} - ".format(lekcio_numero+1) + lekcio["teksto"]["titolo_string"] + "\n\n"

    # teksto
    libro += "## {} ".format(enhavo['fasado']['Teksto']) + lekcio["teksto"]["titolo_string"] + "\n\n"
    libro += "</div style=\"line-height: 80px; font-size: 40px;\">\\begin{large}"
    for par in lekcio["teksto"]["paragrafoj"]:
        libro += " ".join(["".join(vorto) for vorto in par if vorto]) + "\n\n"
    libro += "\\end{large}</div>"

    # Novaj Vortoj
    libro += "## {} ".format(enhavo['fasado']['Novaj vortoj']) + lekcio["teksto"]["titolo_string"] + "\n\n"
    for vortoj_de, vortlisto in lekcio["vortoj"].items():
        libro += "\n\n### " + vortoj_de[0].upper() + vortoj_de[1:] + "\n\n"
        vortlisto = [v for v in vortlisto if v[0] not in "ABCDEFGHIJKLMNOPRSTUVZ"]
        vlen = (len(vortlisto)+2)//3
        #libro += "<table width=100%>"
        libro += ("-"*15+" ")*3+"\n"
        for v_ind in range(vlen):
            v1, v2, v3 = [vortlisto[v_ind].lower() if len(vortlisto) > v_ind and vortlisto[v_ind].lower() in enhavo["vortaro"] else "MDT" for i in [v_ind, v_ind+vlen, v_ind+2*vlen]]
            t1, t2, t3 = [enhavo["vortaro"][v]["tradukajxo"] if v != "MDT" else "MDT" for v in [v1, v2, v3]]
            t1 = t1 if type(t1)==type("") or not t1 else ", ".join(t1)
            t2 = t2 if type(t2)==type("") or not t2 else ", ".join(t2)
            t3 = t3 if type(t3)==type("") or not t3 else ", ".join(t3)
            v1 = "{} - {}{}".format(v1, t1, " "*(15-len(t1)) if t1 else ""*15)
            v2 = "{} - {}{}".format(v2, t2, " "*(15-len(t2)) if t2 else ""*15)
            v3 = "{} - {}{}".format(v3, t3, " "*(15-len(t3)) if t3 else ""*15)
            #libro += "<tr><td>{}</td><td>{}</td><td>{}</td></tr>\n".format(v1, v2, v3)
            libro += "{}{}{}\n".format(v1, v2, v3)
        libro += ("-"*15+" ")*3 + "\n\n"
    libro += "\\pagebreak"  + "\n\n"
    # gramatiko
    libro += "## {} ".format(enhavo['fasado']['Gramatiko']) + "\n\n"
    libro += lekcio["gramatiko"]["teksto"] + "\n\n"
    libro += "\\pagebreak"  + "\n\n"

    libro += "## {} ".format(enhavo['fasado']['Ekzercoj']) + "\n\n"

    libro += "## {} ".format(enhavo['fasado']['Traduku']) + "\n\n"
    tradukendaj = [list(t.keys())[0] for t in lekcio["ekzercoj"]["Traduku"]]
    tlen = (len(tradukendaj)+1)//2
    libro += ("-"*33+" ")*2+"\n"
    for t_ind in range(tlen):
        t1 = tradukendaj[t_ind]
        t2 = tradukendaj[t_ind+tlen] if t_ind+tlen < len(tradukendaj) else ""
        v1 = "{} - _______________".format(t1)
        v2 = "{} - _______________".format(t2) if t2 != "" else ""
        libro += "{}{}{}{}\n".format((33-len(v1))*" ", v1, (33-len(v2))*" ", v2)
    libro += ("-"*33+" ")*2 + "\n\n"

    libro += "## {} ".format(enhavo['fasado']['Kompletigu la frazojn']) + "\n\n"
    tradukendaj = []
    for frazo in lekcio["ekzercoj"]["Kompletigu la frazojn"]:
        tradukendaj += [" ".join([ frazero["videbla"] if frazero["videbla"] else 15*"_"
                        for frazero in frazo if "videbla" in frazero])]
    tlen = (len(tradukendaj)+1)//2
    for t in tradukendaj:
        libro += "* {}\n".format(t)
    libro += "\n\n"

    libro += "## {} ".format(enhavo['fasado']['Traduku kaj respondu']) + "\n\n"
    tradukendaj = [t['demando'] for t in lekcio["ekzercoj"]["Traduku kaj respondu"]]
    for t in tradukendaj:
        libro += "* {}".format(t) + " : \n\n" + 50*"_" + "\n\n" + 50*"_" + "\n\n"

    for rep in [".", "!", "?", ","]:
        libro = libro.replace(" " + rep, rep)
    libro = re.sub("(__)((?=[^_ ])[\W\w])+(__)", "**\\2**", libro)
    return libro

def generate_epub(lingvo, enhavo, args):
    output_path = 'epub/output/' + lingvo + "/"
    lekcioj = ""
    # Forigu nunan dosierujon.
    shutil.rmtree(output_path, ignore_errors=True)
    for i, lekcio in enumerate(enhavo["lecionoj"]):
        lekcio_string = generate_lekcio(lekcio, i)
        lekcioj += lekcio_string + "\\pagebreak"  + "\n\n"
        # Kreu novajn dosierojn
        write_epub_pdf_file(output_path+"lekcio"+str(i+1), lekcio_string, args.papersize)
    write_epub_pdf_file(output_path+"cxiuj_lekcioj", lekcioj, args.papersize)
