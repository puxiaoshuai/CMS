$(function () {
    $("#add-board-btn").click(function (event) {
        event.preventDefault()
        xtalert.alertOneInput({
            'text':"请输入版块名称",
            'placeholder':"版本名称",
            'confirmCallback':function (inputvalue) {
                ajaxhelper.post({
                    'url':'/cms/aboards/',
                    'data':{
                        'name':inputvalue
                    },
                    'success':function (data) {
                        if (data['code']==200)
                        {
                            window.location.reload()
                        }else {
                            xtalert.alertInfo(data["message"])
                        }
                    }
                })
            }
        })
    })
})
$(function () {
    $(".edit_board_btn").click(function () {
        var self = $(this);
        var tr = self.parent().parent();
        var name = tr.attr('data-name');
        var board_id = tr.attr("data-id");

        xtalert.alertOneInput({
            'text': '请输入新的板块名称！',
            'placeholder': name,
            'confirmCallback': function (inputValue) {
                ajaxhelper.post({
                    'url': '/cms/uboards/',
                    'data': {
                        'board_id': board_id,
                        'name': inputValue
                    },
                    'success': function (data) {
                        if(data['code'] == 200){
                            window.location.reload();
                        }else{
                            xtalert.alertInfo(data['message']);
                        }
                    }
                });
            }
        });
    });
});
$(function () {
    $(".del_board_btn").click( function () {
        var  self=$(this)
        var tr=self.parent().parent()
        var banner_id=tr.attr("data-id")
        xtalert.alertConfirm({
            'msg':"您确定要删除当前信息",
            'confirmCallback':function () {
                ajaxhelper.post({
                    'url':'/cms/del_boards/',
                    'data':{
                        'board_id':banner_id
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