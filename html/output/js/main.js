$(document).ready(function(){
  $('[data-toggle="tooltip"]').tooltip(); 
});

$('input[data-solvo]').on('input', function() {
  var id = $(this).attr('id');
  var form_group = $('#form-group-' + id);
  var glyphicon = $('#glyphicon-' + id);
  if ( $(this).val() == $(this).attr('data-solvo') ) {
    form_group.removeClass('has-error').addClass('has-success');
    glyphicon.removeClass('glyphicon-remove').addClass('glyphicon-ok');
  } else {
    form_group.removeClass('has-success').addClass('has-error');
    glyphicon.removeClass('glyphicon-ok').addClass('glyphicon-remove');
  }
});

$('.solvu').click(function() {
  var ekzerco_id = $(this).attr('data-form-id');
  var inputs  = $('#form-' + ekzerco_id + ' input[data-solvo] ');
  inputs.each(function() {
    var solvo = $(this).attr('data-solvo');
    $(this).val(solvo);
    $(this).trigger('input');
  });
});

$('.forigu').click(function() {
  var ekzerco_id = $(this).attr('data-form-id');
  var inputs  = $('#form-' + ekzerco_id + ' input[data-solvo] ');
  inputs.each(function() {
    $(this).val('');
    $(this).trigger('input');
  });
});

