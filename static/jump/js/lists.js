var csrftoken = $.cookie('csrftoken');
function csrfSafeMethod(method) {
return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
beforeSend: function(xhr, settings) {
    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
}
});
$(document).ready(function(){
$('#early').addClass("active");
});
$(document).ready(function() {
$('#example').dataTable();
} );

function link_prem(ip) {
    window.open('http://'+window.location.host+'/xterm/?'+'&hostname='+$("#username"+ip).text()+'&prem='+$("#group"+ip).text(), "_blank")
}