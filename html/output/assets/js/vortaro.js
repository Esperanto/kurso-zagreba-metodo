var substringMatcher = function(vortlisto) {
  return function findMatches(q, cb) {
    var matches, substringRegex;

    // an array that will be populated with substring matches
    matches = [];

    // Search for strings that begin with the query.
    substrRegex = new RegExp('^' + q, 'i');

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
			return '<p><em>' + data.esperante + '</em> – ' + data.fontlingve + '</p>';
		}
	}
});

