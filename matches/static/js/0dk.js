/**
 * Created by deekras on 12/21/15.
 */
//$(function() {
//    var dialog;
//    var contact = "{{single.created_by.first_name}} {{single.created_by.last_name}}";
//    function v() {}
//
//    dialog = $( "#dialog-form" ).dialog({
//      autoOpen: false,
//      height: 200,
//      width: 250,
//      modal: true,
//      buttons: {
//          Close: function() {
//          dialog.dialog( "close" );
//        }
//      },
//      });
//
//
//    $( ".contact" ).button().on( "click", function() {
//      dialog.dialog( "open" );
//    });
//      $( ".contact" ).button().on( "mouseout", function() {
//      dialog.dialog( "close" );
//    });
//  });

$(document).ready(function(){
    $(".contact").click(function(contact_info){
        var b = '{{single.created_by.last_name}}';
        var c = $(this).value;
        //var contact_info = "{{single.created_by.first_name}}";
        alert(c);
    });
});