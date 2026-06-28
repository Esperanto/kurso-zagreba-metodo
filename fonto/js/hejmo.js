(function () {
  const dataElement = document.getElementById('hejmo-lingvodatenoj');
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

  const elektitaLingvo = elektuLingvon();
  window.location.replace('/' + elektitaLingvo.kodo + '/');
}());
