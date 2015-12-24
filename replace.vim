" Make paragraphs.
:%s/^\(.*\)\n\n/- \1\r/g

" Make words.
:%s/^-/-\r  /g
:%s/\s*\([a-zA-ZĉĝĥĵŝŭĈĜĤĴŜŬ]\+\|\.\|,\|?\)\s*/  - \1\r/g

" Make morphemes.
":%s/\(ojn\)$/\ro\rj\nn/g
":%s/\(oj\)$/\r\1/g
":%s/\(on\)$/\r\1/g
":%s/\(o\)$/\r\1/g
":%s/\(e\)$/\r\1/g
":%s/\(a\)$/\r\1/g
