NProgress.start();
$(document).ready(function(){
    NProgress.done();
});
function myEvent(obj,ev,fn){
if(obj.attachEvent){
obj.attachEvent('on'+ev,fn);
}else{
obj.addEventListener(ev,fn,false);
}
}
myEvent(window,'load',function(){
var oRTT=document.getElementById('scroll-top');
var pH=document.documentElement.clientHeight;
var timer=null;
var scrollTop;
window.onscroll=function(){
scrollTop=document.documentElement.scrollTop||document.body.scrollTop;
if(scrollTop>=pH){
oRTT.style.display='block';
}else{
oRTT.style.display='none';
}
return scrollTop;
};
oRTT.onclick=function(){
clearInterval(timer);
timer=setInterval(function(){
var now=scrollTop;
var speed=(0-now)/10;
speed=speed>0?Math.ceil(speed):Math.floor(speed);
if(scrollTop==0){
    clearInterval(timer);
}
document.documentElement.scrollTop=scrollTop+speed;
document.body.scrollTop=scrollTop+speed;
}, 30);
}
});
function get_Notice()
{
var tbody=window.document.getElementById("tbody-result");
var str = "";
$.ajax({
url:'/jump/get_notice_list/',
type:'GET',
success:function (arg) {
var obj = jQuery.parseJSON(arg);
for (i in obj) {
    str += "<tr>" +
    "<td class='text-center'>" + obj[i].fields.create_date + "</td>" +
    "<td class='text-center'>" + obj[i].fields.name + "</td>" +
    "</tr>";
}
tbody.innerHTML = str;
$('#notices').modal({show:true});
}
});
}
function showLogin()
{
$.ajax({
    url:'/jump/get_notice_num/',
    type:'GET',
    success:function (arg) {
        if(isNaN(arg)){
        return false;
        }
        if (arg !=='0'){
            $("#notice").html(arg);
        } else {
           $("#notice").html('');
        }
    }
});
}
$(function () { $('#notices').on('hide.bs.modal', function () {
      $.ajax({
    url:'/jump/get_notice_list/',
    type:'POST',
    data:{modify:1},
    success:function (arg) {
        $("#notice").html('');
    }
});
    });
})
setInterval("showLogin()","10000");
(function(){showLogin();}())