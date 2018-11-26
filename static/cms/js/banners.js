$(function () {
 $("#save_image_btn").click(function (event) {
        event.preventDefault()/*阻止默认事件*/
     var dialog=$("#myModal");
     var self=$(this)
     var name_input=$("input[name='name']")
     var imageurl_input=$("input[name='image_url']")
     var link_url_input=$("input[name='link_url']")
     var weight_url_input=$("input[name='weight_url']")
     var name=name_input.val()
     var  image_url=imageurl_input.val()
     var  link_url=link_url_input.val()
     var  weight_url=weight_url_input.val()
     var submit_btn=self.attr('data-type')
     var banner_id=self.attr('data-id')
     if (!name ||! image_url||!link_url||!weight_url){
         xtalert.alertInfoToast("请输入完整信息")
         return
     }
     var url=''
     if (submit_btn=='update')
     {
         url='/cms/edit_banners/'
     }else {
          url='/cms/abanner/'
     }
     ajaxhelper.post({
         'url': url,
            'data': {
                'name': name,
                'image_url':image_url,
                'link_url':link_url,
                'weight_url':weight_url,
                'banner_id':banner_id
            },
            'success': function (data) {
                dialog.modal("hide")
                if(data['code'] == 200){
                    window.location.reload()
                //    重新加载当前界面
                }else{
                    xtalert.alertInfo(data['message']);
                }
            },
            'fail': function (error) {
                xtalert.alertNetworkError();
            }
     })


 })

})
$(function () {
    $(".edit_banner_btn").click(function (event) {
        var self=$(this)
        var dialog=$("#myModal")
        dialog.modal("show")
        var tr=self.parent().parent()
    //    .parent()是td  在parent()就是trs
        //为了方便，我们给tr.设置一些属性，并赋值
        var name=tr.attr('data-name')
        var image_url = tr.attr("data-image");
        var link_url = tr.attr("data-link");
        var priority = tr.attr("data-weight");
       var nameInput = dialog.find("input[name='name']");
        var imageInput = dialog.find("input[name='image_url']");
        var linkInput = dialog.find("input[name='link_url']");
        var priorityInput = dialog.find("input[name='weight_url']");
        var saveBtn = dialog.find("#save_image_btn");
        nameInput.val(name);
        imageInput.val(image_url);
        linkInput.val(link_url);
        priorityInput.val(priority);
        //为了区分是新上传，还是编辑保存
        saveBtn.attr("data-type",'update');
        saveBtn.attr('data-id',tr.attr('data-id'));
    })
})
$(function () {
    $(".del_banner_btn").click( function () {
        var  self=$(this)
        var tr=self.parent().parent()
        var banner_id=tr.attr("data-id")
        xtalert.alertConfirm({
            'msg':"您确定要删除当前信息",
            'confirmCallback':function () {
                ajaxhelper.post({
                    'url':'/cms/del_banner/',
                    'data':{
                        'banner_id':banner_id
                    },
                    'success':function (data) {
                        if(data['code'] == 200){
                            window.location.reload();
                        }else{
                            xtalert.alertInfo(data['message']);
                        }
                    }
                })
            }
        })
    })
})
