$(document).ready(function(){
  $('[data-toggle="tooltip"]').tooltip(); 
  $('[data-toggle="popover"]').popover({
    placement: 'bottom',
    trigger: 'hover',
    html: true 
  }); 
  $('.container table').addClass('table'); 
});

function esperantigu(s) {
  
    s = s.replace('cx', 'ĉ')
    s = s.replace('gx', 'ĝ')
    s = s.replace('jx', 'ĵ')
    s = s.replace('hx', 'ĥ')
    s = s.replace('sx', 'ŝ')
    s = s.replace('Cx', 'Ĉ')
    s = s.replace('Gx', 'Ĝ')
    s = s.replace('Jx', 'Ĵ')
    s = s.replace('Hx', 'Ĥ')
    s = s.replace('Sx', 'Ŝ')
    s = s.replace('ux', 'ŭ')
    s = s.replace('Ux', 'Ŭ')

    return s;
}

function normalize(s) {

  s = esperantigu(s);
  s = s.toLowerCase(s);
  return s;
}

function selectNextTabbableOrFocusable(selector){
	var selectables = $(selector);
	var current = $(':focus');
	var nextIndex = 0;
	if(current.length === 1){
		var currentIndex = selectables.index(current);
		if(currentIndex + 1 < selectables.length){
			nextIndex = currentIndex + 1;
		}
	}

	selectables.eq(nextIndex).focus();
}


$('input[data-solvo]').on('input', function() {
  var id = $(this).attr('id');
  var form_group = $('#form-group-' + id);
  var glyphicon = $('#glyphicon-' + id);

  // Get input and normalize.
  var input = $(this).val();
  input = normalize(input);

  // Split data-solvo to find solutions and normalize.
  var solutions = $(this).attr('data-solvo').split(/\s*\|\s*/);
  solutions = jQuery.map(solutions, normalize);

  if (jQuery.inArray(input, solutions) !== -1) {
    form_group.removeClass('has-error').addClass('has-success');
    glyphicon.removeClass('glyphicon-remove').addClass('glyphicon-ok');
		// Set focus on the current
		// to not confuse it during the following step. 
		$(this).focus();
		// Jump to the next input.
		selectNextTabbableOrFocusable(':tabbable');
  } else {
    form_group.removeClass('has-success').addClass('has-error');
    glyphicon.removeClass('glyphicon-ok').addClass('glyphicon-remove');
  }
});

$('.solvu').click(function() {
  var form_id = $(this).attr('data-form-id');
  var inputs  = $('#form-' + form_id + ' input[data-solvo] ');
  inputs.each(function() {
    var solvo = $(this).attr('data-solvo');
    $(this).val(solvo);
    $(this).trigger('input');
  });
});

$('.forigu').click(function() {
  var form_id = $(this).attr('data-form-id');
  var inputs  = $('#form-' + form_id + ' input[data-solvo] ');
  inputs.each(function() {
    $(this).val('');
    $(this).trigger('input');
  });
});


var currentLangCode = $('#lingvoelektilo').val();

$('#lingvoelektilo').change(function(e) {

	// currentLangCode comes from global.
	var newLanguangeCode = $(this).val()

	var url = window.location.href;
  url = url.replace(
		'/' + currentLangCode + '/',  	
	  '/' + newLanguangeCode + '/'
	);
	window.location.href = url;

	// var previousLangCode = $('#lingvoelektilo').val());
	// var before_change = $(this).data('pre');
	// console.log(before_change);
	//var langCode = console.log($(this).val())
});
