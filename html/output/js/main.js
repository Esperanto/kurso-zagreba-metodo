$(document).ready(function(){
  $('[data-toggle="tooltip"]').tooltip(); 
});

$('input[data-expected]').keyup(function() {
  var formGroup = $(this).closest('.form-group');
  var glyphicon = $(this).next('span.glyphicon');
  if ( $(this).val() == $(this).attr('data-expected') ) {
    formGroup.removeClass('has-error').addClass('has-success');
    glyphicon.removeClass('glyphicon-remove').addClass('glyphicon-ok');
  } else {
    formGroup.removeClass('has-success').addClass('has-error');
    glyphicon.removeClass('glyphicon-ok').addClass('glyphicon-remove');
  }
});



