#!/usr/bin/env node

import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
const Diff2Html = require('diff2html');

const chunks = [];
for await (const chunk of process.stdin) {
  chunks.push(chunk);
}

const diff = Buffer.concat(chunks).toString('utf8');
const html = Diff2Html.html(diff, {
  drawFileList: true,
  matching: 'lines',
  outputFormat: 'side-by-side',
  renderNothingWhenEmpty: false,
});

process.stdout.write(html);
