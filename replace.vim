:set ignorecase

" Preserve some words
:%s/\(kaj\|de\|Marko\|Ana\|ne\|tie\|Tie\|kie\|kio\|la\|la\|la\)/XXX\0XXX/g

" Make paragraphs.
:%s/^\(.*\)\n\n/- \1\r/g

" Make words.
:%s/^-/-\r  /g
:%s/\s*\([a-zA-ZĉĝĥĵŝŭĈĜĤĴŜŬ]\+\)\s*/  -\r  - \1\r/g
:%s/\(\.\)/  - \1\r/g
:%s/\(,\|?\|!\)/  - '\1'\r/g

" Make morphemes.
:%s/^  -/  -\r    -/g
:%s/ojn$/o\r    - j\r    - n/g
:%s/ajn$/a\r    - j\r    - n/g
:%s/aj$/a\r    - j/g
:%s/oj$/o\r    - j/g
:%s/on$/o\r    - n/g
:%s/an$/a\r    - n/g

:%s/o$/\r    - o/g
" Todo: exclude "la"
:%s/a$/\r    - a/g
:%s/e$/\r    - e/g

:%s/\(in\)$/\r    - \1/g
:%s/\(ist\)$/\r    - \1/g
:%s/\(ej\)$/\r    - \1/g
:%s/\(et\)$/\r    - \1/g
:%s/\(eg\)$/\r    - \1/g
:%s/\(as\|is\|os\|us\)$/\r    - \1/g
:%s/\(at\|it\|ot\|ut\)$/\r    - \1/g
:%s/\(ant\|int\|ont\|unt\)$/\r    - \1/g

:%s/\(mal\|al\|ge\)$/\r    - \1/g

" Remove lists of empty words.
:%s/^    -\n//g

" Indent.
:%s/^/  /


:%s/XXX\(.*\)XXX/\1/g
