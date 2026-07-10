$(document).ready(function(){
  var popoverAllowList = $.extend(
    true,
    {},
    bootstrap.Tooltip.Default.allowList,
    { table: [], tbody: [], tr: [], td: [] }
  );

  $('[data-bs-toggle="tooltip"]').each(function() {
    new bootstrap.Tooltip(this);
  });
  $('[data-bs-toggle="popover"]').each(function() {
    new bootstrap.Popover(this, {
      placement: 'bottom',
      trigger: 'hover',
      html: true,
      allowList: popoverAllowList
    });
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

  s = s.trim();
  s = esperantigu(s);
  s = s.toLowerCase(s);
  return s;
}

// Trovas la videblajn tabeblajn elementojn per jQuery-kerno (sen jQuery-UI,
// kiu antaŭe provizis la «:tabbable»-elektilon).
function selectNextTabbable(){
	var selectables = $(
		'a[href], button:not([disabled]), input:not([disabled]), '
		+ 'select:not([disabled]), textarea:not([disabled]), [tabindex]'
	).filter(function(){
		return this.tabIndex >= 0 && $(this).is(':visible');
	});
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

var gxustaSono = null;

function gxustaSonoElemento() {
	if (gxustaSono !== null) {
		return gxustaSono;
	}

	gxustaSono = document.createElement('audio');
	gxustaSono.preload = 'auto';

	var ogg = document.createElement('source');
	ogg.src = '/assets/ogg/gxuste.ogg';
	ogg.type = 'audio/ogg';
	gxustaSono.appendChild(ogg);

	var mp3 = document.createElement('source');
	mp3.src = '/assets/mp3/gxuste.mp3';
	mp3.type = 'audio/mpeg';
	gxustaSono.appendChild(mp3);

	return gxustaSono;
}

function luduGxustanSonon() {
	var sono = gxustaSonoElemento();

	try {
		sono.currentTime = 0;
	} catch (e) {
	}

	try {
		var ludado = sono.play();
		if (ludado && typeof ludado.catch === 'function') {
			ludado.catch(function() {});
		}
	} catch (e) {
	}
}

function estasUzantaEnigo(evento) {
	return evento && evento.originalEvent && evento.originalEvent.isTrusted;
}


$('input[data-solvo]').on('input', function(evento) {
  // Get input and normalize.
  var input = $(this).val();
  input = normalize(input);
	var jam_gxusta = $(this).hasClass('is-valid');

  // Split data-solvo to find solutions and normalize.
  var solutions = $(this).attr('data-solvo').split(/\s*\|\s*/);
  solutions = jQuery.map(solutions, normalize);

	var correct = 
	  // Input it part of solutions	
		(jQuery.inArray(input, solutions) !== -1)
	  ||
		(input == normalize($(this).attr('data-solvo')));

  if (correct) {
    $(this).removeClass('is-invalid').addClass('is-valid');
		if (!jam_gxusta && estasUzantaEnigo(evento)) {
			luduGxustanSonon();
		}
		// Set focus on the current
		// to not confuse it during the following step. 
		$(this).focus();
		// Jump to the next input.
		selectNextTabbable();
  } else {
    $(this).removeClass('is-valid').addClass('is-invalid');
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


var currentLangCode = $('.lingvoelektilo-ligilo[aria-current="true"]').data('lingvo');

$('.lingvoelektilo-ligilo').click(function(e) {
  if (!currentLangCode) {
    return;
  }

  e.preventDefault();
  var newLanguageCode = $(this).data('lingvo');

  var url = window.location.href;
  url = url.replace(
    '/' + currentLangCode + '/',
    '/' + newLanguageCode + '/'
  );
  window.location.href = url;
});
