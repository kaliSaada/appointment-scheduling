var data = new Date();
var dia     = data.getDate();
var mes     = data.getMonth();
var ano4    = data.getFullYear();
var str_data = ano4 + '-' + (mes+1) + '-' +dia;
if (dia < 10) {
    var str_data = ano4 + '-' + (mes+1) + '-0' +dia;
}else{
    var str_data = ano4 + '-' + (mes+1) + '-' +dia;
}

$(document).ready(function() {

    $.getJSON( "consulta", function( data ) {
      var items = [];
      $.each( data, function( key, val ) {
        items.push( "<div class=\"custom-control custom-checkbox\"><input type=\"checkbox\" class=\"custom-control-label\" id=\"" + val.codigo + "\" name=\"consultas\"><label class=\"list-group-item\" data-color=\"info\" id-user=\"" + val.user_codigo + "\" >" + val.date +" - " + val.hora + "</label></div>" );
      });

      $( "<div/>", {
        'class': '',
        html: items.join( "" )
      }).appendTo( "t-body" );
    });

    $('#calendar').fullCalendar({
    header: {
    left: 'prev,next today',
    center: 'title',
    right: 'month'
    },
    defaultDate: str_data,
    editable: false,
    navLinks: true, // can click day/week names to navigate views
    eventLimit: true, // allow "more" link when too many events
    events: {
        url: '/agenda',
        error: function() {
        $('#script-warning').show();
        }
    },
    loading: function(bool) {
        $('#loading').toggle(bool);
    }
    });
});

function deletar_consulta(){
  var pacote = document.getElementsByName('consultas');
    for (var i = 0; i < pacote.length; i++){
        if ( pacote[i].checked ) {
            console.log(pacote[i])
            if(pacote[i].id !== null){
                var settings = {
                  "async": true,
                  "crossDomain": true,
                  "url": "/consulta/deletar",
                  "method": "POST",
                  "headers": {
                    "content-type": "application/x-www-form-urlencoded",
                  },
                  "data": {
                    "codigo_consulta": pacote[i].id,
                  }
                }
                $.ajax(settings).done(function (response) {
                    window.location.reload()
                });
            }
        }
    }

}

function alterar_consulta(){
  var pacote = document.getElementsByName('consultas');
  var data = document.getElementsByName('data_alterar');
  var time = document.getElementsByName('time_alterar');
  var comentario = document.getElementsByName('comentario_alterar');
  console.log(data, time, comentario)
    for (var i = 0; i < pacote.length; i++){
        if ( pacote[i].checked ) {
            console.log(pacote[i])
            if(pacote[i].id !== null){
                var settings = {
                  "async": true,
                  "crossDomain": true,
                  "url": "/consulta/alterar",
                  "method": "POST",
                  "headers": {
                    "content-type": "application/x-www-form-urlencoded",
                  },
                  "data": {
                    "codigo_consulta": pacote[i].id,
                    "data": data[0].value,
                    "time": time[0].value,
                    "comentario": comentario[0].value,
                  }
                }
                $.ajax(settings).done(function (response) {
                    window.location.reload()
                });
            }
        }
    }

}

