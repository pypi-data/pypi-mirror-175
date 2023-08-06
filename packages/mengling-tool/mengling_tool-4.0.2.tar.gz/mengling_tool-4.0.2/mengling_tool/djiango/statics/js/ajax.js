//改变元素内容,url仅访问statics的内容 ../statics/temp.html'
function ajaxChange(url, jq, method = 'GET', data = null) {
    var xmlhttp;
    if (window.XMLHttpRequest) {
        //  IE7+, Firefox, Chrome, Opera, Safari 浏览器执行代码
        xmlhttp = new XMLHttpRequest();
    } else {
        // IE6, IE5 浏览器执行代码
        xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
    }
    xmlhttp.onreadystatechange = function () {
        if (xmlhttp.readyState === 4 && xmlhttp.status === 200) {
            // document.getElementById(id).innerHTML = xmlhttp.responseText;//不会执行js
            $(jq).html(xmlhttp.responseText);//转为html对象后加入至目标下
        }
    }
    xmlhttp.open(method, url, true);
    xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xmlhttp.send(data);
}

//表单提交
function formSubmit(form, url, result_success_func, error_func = null, type = "POST", ifasync = false) {
    $.ajax({
        type: type,//方法类型
        url: url,//url
        data: form != null ? form.serialize() : null,
        async: ifasync,
        success: function (result) {
            result_success_func(result);
            return false;//需要加,否则window.location.href跳转无法执行
            // if (result.resultCode == 200)
        },
        error: function () {
            if (error_func) error_func();
        }
    });
}

//表单提交
function getFormSubmit(form_jq, url, type = "POST", ifasync = false) {
    var r = null, status = false;
    $.ajax({
        type: type,//方法类型
        url: url,//url
        data: form_jq != null ? form_jq.serialize() : null,
        //使用异步返回必然为null
        async: ifasync,
        success: function (result) {
            r = result;
            return false;//需要加,否则window.location.href跳转无法执行
            // if (result.resultCode == 200)
        },
        error: function () {
            r = null;
        }
    });
    return r;
}


function ajax(url, data, ret_sucfunc = null, ret_errfunc = null, type = "POST", ifasync = true) {
    $.ajax({
        type: type,//方法类型
        url: url,//url
        data: data,
        //使用异步返回必然为null
        async: ifasync,
        processData: false,
        contentType: false,
        success: function (result) {
            if (ret_sucfunc != null) ret_sucfunc(result);
            return false;
        },
        error: ret_errfunc != null ? ret_errfunc : function (err) {
        }
    });
}

//自动同步
function auto(url, jq, timeout, method = 'GET', data = null) {
    var fn = function () {
        ajaxChange(url, jq, method, data);
        setTimeout(fn, timeout);
    }
    fn();
}


//文件上传
function upload(url, e_or_id, ifasync = false, note = '正在上传...') {
    var formData;
    if (typeof e_or_id == 'string') formData = new FormData(document.getElementById(e_or_id));
    else formData = new FormData(e_or_id);
    var r = null;
    auto_alert(note, t = -1);
    $.ajax({
        url: url,
        type: "post",
        data: formData,
        async: ifasync,
        processData: false,
        contentType: false,
        success: function (res) {
            if (res) {
                close_auto_alert();
                alert(res);
                r = res;
            }
            return false;
        },
        error: function (err) {
            close_auto_alert();
            alert("上传失败!\n" + err);
            r = err;
        }
    })
    return r;
}
