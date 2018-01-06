var csrftoken = $.cookie('csrftoken');
function csrfSafeMethod(method) {
// these HTTP methods do not require CSRF protection
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
$('#userul').addClass("menu-open");
$('#jump-group').addClass("active");
$('#userli').addClass("active");
});
$(document).ready(function() {
$('#example').dataTable();
} );
$('#optgroup').multiSelect({
  selectableHeader: "<div class='text-center'>可选主机</div><input type='text' style='width: 100%' class='custom-header' autocomplete='off' placeholder='搜索机器'>",
  selectionHeader: "<div class='text-center'>已选主机</div><input type='text' style='width: 100%' class='search-input' autocomplete='off' placeholder='搜索机器'>",
  afterInit: function(ms){
    var that = this,
        $selectableSearch = that.$selectableUl.prev(),
        $selectionSearch = that.$selectionUl.prev(),
        selectableSearchString = '#'+that.$container.attr('id')+' .ms-elem-selectable:not(.ms-selected)',
        selectionSearchString = '#'+that.$container.attr('id')+' .ms-elem-selection.ms-selected';

    that.qs1 = $selectableSearch.quicksearch(selectableSearchString)
    .on('keydown', function(e){
      if (e.which === 40){
        that.$selectableUl.focus();
        return false;
      }
    });

    that.qs2 = $selectionSearch.quicksearch(selectionSearchString)
    .on('keydown', function(e){
      if (e.which == 40){
        that.$selectionUl.focus();
        return false;
      }
    });
  },
  afterSelect: function(){
    this.qs1.cache();
    this.qs2.cache();
  },
  afterDeselect: function(){
    this.qs1.cache();
    this.qs2.cache();
  }
});
function r_select() {
    $('#e_optgroup').multiSelect({
  selectableHeader: "<div class='text-center'>可选主机</div><input type='text' style='width: 100%' class='custom-header' autocomplete='off' placeholder='搜索机器'>",
  selectionHeader: "<div class='text-center'>已选主机</div><input type='text' style='width: 100%' class='search-input' autocomplete='off' placeholder='搜索机器'>",
  afterInit: function(ms){
    var that = this,
        $selectableSearch = that.$selectableUl.prev(),
        $selectionSearch = that.$selectionUl.prev(),
        selectableSearchString = '#'+that.$container.attr('id')+' .ms-elem-selectable:not(.ms-selected)',
        selectionSearchString = '#'+that.$container.attr('id')+' .ms-elem-selection.ms-selected';

    that.qs1 = $selectableSearch.quicksearch(selectableSearchString)
    .on('keydown', function(e){
      if (e.which === 40){
        that.$selectableUl.focus();
        return false;
      }
    });

    that.qs2 = $selectionSearch.quicksearch(selectionSearchString)
    .on('keydown', function(e){
      if (e.which == 40){
        that.$selectionUl.focus();
        return false;
      }
    });
  },
  afterSelect: function(){
    this.qs1.cache();
    this.qs2.cache();
  },
  afterDeselect: function(){
    this.qs1.cache();
    this.qs2.cache();
  }
});
}

$(document).ready(function(){
$('#tijiao2').click(function(){
    $("#retune").text('正在处理....');
     $.ajax({
        type:'POST',
        url:'/jump/group/',
        data:$("#createuser").serialize(),
        cache:false,
        dataType:'json',
        success:function(data){
            if (data[0])
              {
                $("#retune").css('color','green');
                $("#retune").text(data[1]+'，2秒后刷新页面。');
                setTimeout(function(){
                window.location.reload();
                },2000);
              }
            else
              {
              $("#retune").css('color','red');
                $("#retune").text(data[1]);
              }

        },
         error:function(){
            $("#retune").css('color','red');
            $("#retune").text('数据请求失败，请刷新页面尝试!');
        }
    });
});
});
function del_group(doc,id) {
    if(confirm("确认要删除此组，删除后无法恢复哦？")){
    $.ajax({
    url:'/jump/delgroup/',
    type:'POST',
    data:{modify:id},
    success:function (arg) {
        window.location.reload();
        var obj = jQuery.parseJSON(arg);
        var this_id = $(doc).attr('id');
    },
    error:function () {
        console.log('failed');
    }
});
}
};
function edit_group(id) {
		$("#groupid").attr("value",id);
		$("#e_groupname").attr("value",$("#groupname"+id).text());
		$("#description"+$("#description"+id).text()).attr('selected','selected');
		var devlist = $("#dev"+id).text().split(',');
		$.each(devlist,function(i,item){
		    console.log(item)
        $("#dev"+item.replace(/\./g,'')).attr('selected','selected');
　　    });
		r_select();
        $('#myModaledit').modal({show:true});
        $('#myModaledit').on('hide.bs.modal',
          function() {
//             $("#description"+$("#description"+id).text()).removeAttr('selected');
//             $.each(devlist,function(i,item){
//         $("#dev"+item.replace(/\./g,'')).removeAttr('selected');
// 　　    });
           window.location.reload();
          }
        );
}
$(document).ready(function(){
$('#e_tijiao').click(function(){
    $("#retune").text('正在处理....');
     $.ajax({
        type:'POST',
        url:'/jump/edit_group/',
        data:$("#editgroup").serialize(),
        cache:false,
        dataType:'json',
        success:function(data){
            if (data[0])
              {
                $("#e_retune").css('color','green');
                $("#e_retune").text(data[1]+'，2秒后刷新页面。');
                setTimeout(function(){
                window.location.reload();
                },2000);
              }
            else
              {
              $("#e_retune").css('color','red');
                $("#e_retune").text(data[1]);
              }

        },
         error:function(){
            $("#e_retune").css('color','red');
            $("#e_retune").text('数据请求失败，请刷新页面尝试!');
        }
    });
});
});
$(document).ready(function() {
  $('#createuser')
      .bootstrapValidator({
          feedbackIcons: {
              valid: 'glyphicon glyphicon-ok',
              invalid: 'glyphicon glyphicon-remove',
              validating: 'glyphicon glyphicon-refresh'
          },
          fields: {
              groupname: {
                  validators: {
                      notEmpty: {
                      message: '组名不得为空！'
                      },
                      stringLength:{
                      min:0,
                      max:15,
                      message:'组名应小于15个字符.'
                  }
                  }
              }
          }
      });
});