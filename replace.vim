" Make paragraphs.
:%s/^\(.*\)\n\n/- \1\r/g

" Make words.
:%s/^-/-\r  /g
:%s/\s*\([a-zA-ZĉĝĥĵŝŭĈĜĤĴŜŬ]\+\|\.\|?\)\s*/  - \1\r/g
:%s/\s*\(,\)\s*/  - '\1'\r/g

" Make morphemes.
:%s/^  -/  -\r    -/g
":%s/ojn$/\r    - o\r    - j\r    - n/g
:%s/oj$/o\r    - j/g
:%s/on$/o\r    - n/g

:%s/o$/\r    - o/g
" Todo: exclude "la"
:%s/a$/\r    - a/g
:%s/e$/\r    - e/g

:%s/\(in\)$/\r    - \1/g
:%s/\(ist\)$/\r    - \1/g
:%s/\(as\|is\|os\|us\)$/\r    - \1/g
:%s/\(at\|it\|ot\|ut\)$/\r    - \1/g
:%s/\(ant\|int\|ont\|unt\)$/\r    - \1/g

" Indent.
:%s/-/    -/
