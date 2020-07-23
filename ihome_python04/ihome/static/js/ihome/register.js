function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");//通过正则表达式获取 cookie
    return r ? r[1] : undefined;//三目运算符
}//js读取cookie的方法

var imageCodeId = "";//保存图片验证码编号为全局变量

function generateUUID() {
    var d = new Date().getTime();
    if (window.performance && typeof window.performance.now === "function") {
        d += performance.now(); //use high-precision timer if available
    }
    var uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
        var r = (d + Math.random() * 16) % 16 | 0;
        d = Math.floor(d / 16);
        return (c == 'x' ? r : (r & 0x3 | 0x8)).toString(16);
    });
    return uuid;
}

// var imageCodeId = ''

function generateImageCode() {
    // 形成图片验证码的图片地址 设置到页面中 让浏览器请求验证码图片
    // 生成图片验证码编号
    // 1.时间戳（存在问题 两人同时点击）
    // 2.uuid（全局唯一标识符）
    imageCodeId = generateUUID();
    //设置图片的url
    var url = '/api/v1.0/image_codes/' + imageCodeId
    $(".image-code img").attr('src', url);
}

function sendSMSCode() {
    //点击发送短信验证码之后被执行的代码
    $(".phonecode-a").removeAttr("onclick");//一旦点击之后就获取短信验证码的onclick事件移除
    var mobile = $("#mobile").val();//获取手机号
    if (!mobile) {
        $("#mobile-err span").html("请填写正确的手机号！");
        $("#mobile-err").show();
        $(".phonecode-a").attr("onclick", "sendSMSCode();");//恢复点击事件
        return;//阻断函数的执行
    }
    var imageCode = $("#imagecode").val();
    if (!imageCode) {//验证图片验证码是否填写
        $("#image-code-err span").html("请填写验证码！");
        $("#image-code-err").show();
        $(".phonecode-a").attr("onclick", "sendSMSCode();");
        return;
    }

    var req_data = {
        image_code: imageCode,//图片验证码的值
        image_code_id: imageCodeId//图片验证码的编号（全局变量）
    }
    $.get('/api/v1.0/sms_codes/' + mobile, req_data, function (resp) {
        //resp是后端返回的响应值 后端返回的是json字符串 ajax将其转化为js对象
        if (resp.errno == '0') {
            var num = 60;
            //表示发送成功
            // 进行60秒倒数计时
            var timer = setInterva(function () {
                //修改倒计时文本
                if (num > 1) {
                    $('.phonecode-a').html(num + '秒');
                    num -= 1;
                } else {
                    $('.phonecode-a').html('获取验证码');
                    $(".phonecode-a").attr("onclick", "sendSMSCode();");
                    // 销毁定时器
                    clearInterval(timer);
                }


            }, 1000, 60)
        } else {
            alert(resp.errmsg);
            $(".phonecode-a").attr("onclick", "sendSMSCode();");
        }
    })
}

$(document).ready(function () {
    generateImageCode();
    $("#mobile").focus(function () {
        $("#mobile-err").hide();
    });
    $("#imagecode").focus(function () {
        $("#image-code-err").hide();
    });
    $("#phonecode").focus(function () {
        $("#phone-code-err").hide();
    });
    $("#password").focus(function () {
        $("#password-err").hide();
        $("#password2-err").hide();
    });
    $("#password2").focus(function () {
        $("#password2-err").hide();
    });
    //为表单提交补充自定义的函数行为（提交事件）
    $(".form-register").submit(function (e) {
        //阻止浏览器的对于表单的默认提交行为
        e.preventDefault();

        var mobile = $("#mobile").val();
        var phoneCode = $("#phonecode").val();
        var passwd = $("#password").val();
        var passwd2 = $("#password2").val();
        if (!mobile) {
            $("#mobile-err span").html("请填写正确的手机号！");
            $("#mobile-err").show();
            return;
        }
        if (!phoneCode) {
            $("#phone-code-err span").html("请填写短信验证码！");
            $("#phone-code-err").show();
            return;
        }
        if (!passwd) {
            $("#password-err span").html("请填写密码!");
            $("#password-err").show();
            return;
        }
        if (passwd != passwd2) {
            $("#password2-err span").html("两次密码不一致!");
            $("#password2-err").show();
            return;
        }
        //调用ajax向后端发送请求
        var req_data = {
            "mobile": mobile,
            "sms_code": phoneCode,
            "password": passwd,
            "password2": passwd2
        };
        var req_json = JSON.stringify(req_data);
        $.ajax({
            url: "/api/v1.0/users",
            type: "post",
            data: req_json,
            contentType: "application/json",
            dataType: 'json',
            headers: {
                "X-CSRFToken": getCookie("csrf_token")
            },//设置请求头中 将csrf_token值放到请求中 方便后端进行csrf进行验证
            success: function (resp) {
                if (resp.errno == 0) {
                    //注册成功  跳转到主页
                    location.href = "/index.html";
                } else {
                    alert(resp.errmsg);
                }
            }
        })
    });
})