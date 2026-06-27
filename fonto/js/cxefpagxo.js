(function () {
  const dataElement = document.getElementById('cxefpagxo-lingvodatenoj');
  if (!dataElement) {
    return;
  }

  let lingvoj;
  try {
    lingvoj = JSON.parse(dataElement.textContent);
  } catch (error) {
    return;
  }
  if (!Array.isArray(lingvoj) || lingvoj.length === 0) {
    return;
  }

  const lingvojLauxKodo = new Map(lingvoj.map((lingvo) => [lingvo.kodo.toLowerCase(), lingvo]));

  function normaliguKodon(kodo) {
    return String(kodo || '').trim().toLowerCase().replace('_', '-');
  }

  function kandidatoj() {
    const retumilajLingvoj = navigator.languages && navigator.languages.length
      ? navigator.languages
      : [navigator.language || 'en'];
    const rezulto = [];

    for (const retumilaLingvo of retumilajLingvoj) {
      const kodo = normaliguKodon(retumilaLingvo);
      if (!kodo) {
        continue;
      }
      rezulto.push(kodo);

      if (kodo.startsWith('zh-hant')) {
        rezulto.push('zh-tw');
      }
      if (kodo.startsWith('zh-hans')) {
        rezulto.push('zh');
      }

      const bazaKodo = kodo.split('-')[0];
      if (bazaKodo && bazaKodo !== kodo) {
        rezulto.push(bazaKodo);
      }
    }

    rezulto.push('en');
    return rezulto;
  }

  function elektuLingvon() {
    for (const kodo of kandidatoj()) {
      if (lingvojLauxKodo.has(kodo)) {
        return lingvojLauxKodo.get(kodo);
      }
    }
    return lingvoj[0];
  }

  function agorduElementon(elemento, lingvo) {
    elemento.lang = lingvo.kodo;
    elemento.dir = lingvo.tekstodirekto || 'ltr';
  }

  function aldonuDropdownEron(menuo, lingvo) {
    const ero = document.createElement('li');
    const ligilo = document.createElement('a');
    ligilo.className = 'dropdown-item';
    ligilo.href = lingvo.kodo + '/';
    ligilo.textContent = lingvo.nomo;
    ligilo.title = lingvo.esperanta_nomo;
    agorduElementon(ligilo, lingvo);
    ero.append(ligilo);
    menuo.append(ero);
  }

  const elektitaLingvo = elektuLingvon();
  const teksto = document.getElementById('cxefpagxo-teksto');
  const titolo = document.getElementById('cxefpagxo-titolo');
  const subtitolo = document.getElementById('cxefpagxo-subtitolo');
  const cxefaLingvo = document.getElementById('cxefpagxo-cxefa-lingvo');
  const menuo = document.getElementById('cxefpagxo-lingvoj');

  document.documentElement.lang = elektitaLingvo.kodo;
  document.title = elektitaLingvo.titolo + ' | ' + elektitaLingvo.subtitolo;
  titolo.textContent = elektitaLingvo.titolo;
  subtitolo.textContent = elektitaLingvo.subtitolo;
  agorduElementon(teksto, elektitaLingvo);

  cxefaLingvo.href = elektitaLingvo.kodo + '/';
  cxefaLingvo.textContent = elektitaLingvo.nomo;
  cxefaLingvo.title = elektitaLingvo.nomo;
  agorduElementon(cxefaLingvo, elektitaLingvo);

  menuo.textContent = '';
  for (const lingvo of lingvoj) {
    if (lingvo.kodo !== elektitaLingvo.kodo) {
      aldonuDropdownEron(menuo, lingvo);
    }
  }
}());
