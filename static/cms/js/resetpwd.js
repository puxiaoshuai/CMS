
$(document).ready(function () {
    $("#submit").click(function (event) {
        //event.preventDefault();阻止表单的默认提交的事件
        event.preventDefault();
        //获取元素
        var old_pwdE = $("input[name=old_pwd]")
        var new_pwdE = $("input[name=new_pwd]")
        var sure_pwdE = $("input[name=sure_pwd]")
        //获取值
        var oldpwd=old_pwdE.val()
        var newpwd=new_pwdE.val()
        var surepwd=sure_pwdE.val()
        //ajax
        //1.要在模板中渲染一个csrf_token
        //2.在ajax请求的头部设置x-csrftoken,已封装
        ajaxhelper.post({
            'url':'/cms/resetpwd/',
            'data':{
                'old_pwd':oldpwd,
                'new_pwd':newpwd,
                'sure_pwd':surepwd
            },
            //获取到views中返回的jsonty
            'success':function (data) {
                console.log("成功啦啦啦啦啦=============")
               if(data['code'] == 200){
                    xtalert.alertSuccessToast("恭喜！密码修改成功！");
                    old_pwdE.val("");
                    new_pwdE.val("");
                    sure_pwdE.val("");
                }else{
                    var message = data['message'];
                    xtalert.alertInfo(message);
                }

            },
            'fail':function (data) {

                xtalert.alertNetworkError()
            }
        })
    })
})

