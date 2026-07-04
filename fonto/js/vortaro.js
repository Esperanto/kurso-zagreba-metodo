function eskapiHtml(s) {
  return String(s).replace(/[&<>"']/g, function(c) {
    return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
  });
}

var substringMatcher = function(vortlisto) {
  return function findMatches(q, cb) {
    var matches, substringRegex;

    // an array that will be populated with substring matches
    matches = [];

		q = esperantigu(q);

    // Traktu la enigon laŭvorte: eskapu regex-signojn (evitu ReDoS kaj rompon ĉe «(» ktp.).
    var eskapita = q.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    var substrRegex = new RegExp('^' + eskapita, 'i');

    // iterate through the pool of strings and for any string that
    // contains the substring `q`, add it to the `matches` array
		var match = function(i, str) {
      if (substrRegex.test(str)) {
        matches.push({
					esperante: vortlisto['esperante'][i], 
					fontlingve: vortlisto['fontlingve'][i]
				});
      }
    }
    $.each(vortlisto['esperante'], match);
    $.each(vortlisto['fontlingve'], match);

		//matches = [{value: 'sdfsdf', year: 333}];
    cb(matches);
  };
};

$('.typeahead').typeahead({
  hint: true,
  highlight: true,
  minLength: 1
}, {
  name: 'states',
  source: substringMatcher(vortlisto),
	display: 'table',
	templates: {
		suggestion: function(data) {
			return '<p><em>' + eskapiHtml(data.esperante) + '</em> – ' + eskapiHtml(data.fontlingve) + '</p>';
		}
	}
});

