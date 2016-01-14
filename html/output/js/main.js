$(document).ready(function(){
  $('[data-toggle="tooltip"]').tooltip(); 
});

$('input[data-expected]').keyup(function() {
  var id = $(this).attr('id');
  var formGroup = $('#form-group-' + id);
  var glyphicon = $('#glyphicon-' + id);
  if ( $(this).val() == $(this).attr('data-expected') ) {
    formGroup.removeClass('has-error').addClass('has-success');
    glyphicon.removeClass('glyphicon-remove').addClass('glyphicon-ok');
  } else {
    formGroup.removeClass('has-success').addClass('has-error');
    glyphicon.removeClass('glyphicon-ok').addClass('glyphicon-remove');
  }
});



