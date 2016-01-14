$(document).ready(function(){
  $('[data-toggle="tooltip"]').tooltip(); 
});

$('input[data-expected]').on('input', function() {
  var id = $(this).attr('id');
  var form_group = $('#form-group-' + id);
  var glyphicon = $('#glyphicon-' + id);
  if ( $(this).val() == $(this).attr('data-expected') ) {
    form_group.removeClass('has-error').addClass('has-success');
    glyphicon.removeClass('glyphicon-remove').addClass('glyphicon-ok');
  } else {
    form_group.removeClass('has-success').addClass('has-error');
    glyphicon.removeClass('glyphicon-ok').addClass('glyphicon-remove');
  }
});

$('.solvu').click(function() {
  var ekzerco_id = $(this).attr('data-form-id');
  var inputs  = $('#form-' + ekzerco_id + ' input[data-expected] ');
  inputs.each(function() {
    var solvo = $(this).attr('data-expected');
    $(this).val(solvo);
    $(this).trigger('input');
  });
});

$('.forigu').click(function() {
  var ekzerco_id = $(this).attr('data-form-id');
  var inputs  = $('#form-' + ekzerco_id + ' input[data-expected] ');
  inputs.each(function() {
    $(this).val('');
    $(this).trigger('input');
  });
});

