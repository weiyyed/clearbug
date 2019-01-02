/*动态改变模块信息*/
function show_module(module_info, id) {
    module_info = module_info.split('replaceFlag');
    var a = $(id);
    a.empty();
    for (var i = 0; i < module_info.length; i++) {
        if (module_info[i] !== "") {
            var value = module_info[i].split('^=');
            a.prepend("<option value='" + value[0] + "' >" + value[1] + "</option>")
        }
    }
    a.prepend("<option value='请选择' selected>请选择</option>");

}

function show_case(case_info, id) {
    case_info = case_info.split('replaceFlag');
    var a = $(id);
    a.empty();
    for (var i = 0; i < case_info.length; i++) {
        if (case_info[i] !== "") {
            var value = case_info[i].split('^=');
            a.prepend("<option value='" + value[0] + "' >" + value[1] + "</option>")
        }
    }
    a.prepend("<option value='请选择' selected>请选择</option>");

}

/*表单信息异步传输*/
function info_ajax(id, url) {
    var data = $(id).serializeJSON();
    if (id === '#add_task') {
        var include = [];
        var i = 0;
        $("ul#pre_case li a").each(function () {
            include[i++] = [$(this).attr('id'), $(this).text()];
        });
        data['module'] = include;
    }

    $.ajax({
        type: 'post',
        url: url,
        data: JSON.stringify(data),
        contentType: "application/json",
        success: function (data) {
            if (data !== 'ok') {
                if (data.indexOf('/api/') !== -1) {
                    window.location.href = data;
                } else {
                    myAlert(data);
                }
            }
            else {
                window.location.reload();
            }
        }
        ,
        error: function () {
            myAlert('Sorry，服务器可能开小差啦, 请重试!');
        }
    });

}

function auto_load(id, url, target, type) {
    var data = $(id).serializeJSON();
    if (id === '#form_message' || id === '#belong_message' || id === '#pro_filter') {
        data = {
            "test": {
                "name": data,
                "type": type
            }
        }
    } else if (id === '#form_config') {
        data = {
            "config": {
                "name": data,
                "type": type
            }
        }
    } else {
        data = {
            "task": {
                "name": data,
                "type": type
            }
        }
    }
    $.ajax({
        type: 'post',
        url: url,
        data: JSON.stringify(data),
        contentType: "application/json",
        success: function (data) {
            if (type === 'module') {
                show_module(data, target)
            } else {
                show_case(data, target)
            }
        }
        ,
        error: function () {
            myAlert('Sorry，服务器可能开小差啦, 请重试!');
        }
    });

}

function update_data_ajax(id, url) {
    var data = $(id).serializeJSON();
    $.ajax({
        type: 'post',
        url: url,
        data: JSON.stringify(data),
        contentType: "application/json",
        success: function (data) {
            if (data !== 'ok') {
                myAlert(data);
            }
            else {
                window.location.reload();
            }
        },
        error: function () {
            myAlert('Sorry，服务器可能开小差啦, 请重试!');
        }
    });
}

function del_data_ajax(id, url) {
    var data = {
        "id": id,
        'mode': 'del'
    };
    $.ajax({
        type: 'post',
        url: url,
        data: JSON.stringify(data),
        contentType: "application/json",
        success: function (data) {
            if (data !== 'ok') {
                myAlert(data);
            }
            else {
                window.location.reload();
            }
        },
        error: function () {
            myAlert('Sorry，服务器可能开小差啦, 请重试!');
        }
    });
}

function copy_data_ajax(id, url) {
    var data = {
        "data": $(id).serializeJSON(),
        'mode': 'copy'
    };
    $.ajax({
        type: 'post',
        url: url,
        data: JSON.stringify(data),
        contentType: "application/json",
        success: function (data) {
            if (data !== 'ok') {
                myAlert(data);
            }
            else {
                window.location.reload();
            }
        },
        error: function () {
            myAlert('Sorry，服务器可能开小差啦, 请重试!');
        }
    });
}

function case_ajax(type, editor) {
    var url = $("#url").serializeJSON();
    var method = $("#method").serializeJSON();
    var dataType = $("#DataType").serializeJSON();
    var caseInfo = $("#form_message").serializeJSON();
    var variables = $("#form_variables").serializeJSON();
    var request_data = null;
    if (dataType.DataType === 'json') {
        try {
            request_data = eval('(' + editor.session.getValue() + ')');
        }
        catch (err) {
            myAlert('Json格式输入有误！');
            return
        }
    } else {
        request_data = $("#form_request_data").serializeJSON();
    }
    var headers = $("#form_request_headers").serializeJSON();
    var extract = $("#form_extract").serializeJSON();
    var validate = $("#form_validate").serializeJSON();
    var parameters = $('#form_params').serializeJSON();
    var hooks = $('#form_hooks').serializeJSON();
    var include = [];
    var i = 0;
    $("ul#pre_case li a").each(function () {
        include[i++] = [$(this).attr('id'), $(this).text()];
    });
    caseInfo['include'] = include;
    const test = {
        "test": {
            "name": caseInfo,
            "parameters": parameters,
            "variables": variables,
            "request": {
                "url": url.url,
                "method": method.method,
                "headers": headers,
                "type": dataType.DataType,
                "request_data": request_data
            },
            "extract": extract,
            "validate": validate,
            "hooks": hooks,
        }
    };
    if (type === 'edit') {
        url = '/api/edit_case/';
    } else {
        url = '/api/add_case/';
    }
    $.ajax({
        type: 'post',
        url: url,
        data: JSON.stringify(test),
        contentType: "application/json",
        success: function (data) {
            if (data === 'session invalid') {
                window.location.href = "/api/login/";
            } else {
                if (data.indexOf('/api/') != -1) {
                    window.location.href = data;
                } else {
                    myAlert(data);
                }
            }
        },
        error: function () {
            myAlert('Sorry，服务器可能开小差啦, 请重试!');
        }
    });
}

function config_ajax(type) {
    var dataType = $("#config_data_type").serializeJSON();
    var caseInfo = $("#form_config").serializeJSON();
    var variables = $("#config_variables").serializeJSON();
    var parameters = $('#config_params').serializeJSON();
    var hooks = $('#config_hooks').serializeJSON();
    var request_data = null;
    if (dataType.DataType === 'json') {
        try {
            request_data = eval('(' + editor.session.getValue() + ')');
        }
        catch (err) {
            myAlert('Json格式输入有误！');
            return
        }
    } else {
        request_data = $("#config_request_data").serializeJSON();
    }
    var headers = $("#config_request_headers").serializeJSON();

    const config = {
        "config": {
            "name": caseInfo,
            "variables": variables,
            "parameters": parameters,
            "request": {
                "headers": headers,
                "type": dataType.DataType,
                "request_data": request_data
            },
            "hooks": hooks,

        }
    };
    if (type === 'edit') {
        url = '/api/edit_config/';
    } else {
        url = '/api/add_config/';
    }
    $.ajax({
        type: 'post',
        url: url,
        data: JSON.stringify(config),
        contentType: "application/json",
        success: function (data) {
            if (data === 'session invalid') {
                window.location.href = "/api/login/";
            } else {
                if (data.indexOf('/api/') != -1) {
                    window.location.href = data;
                } else {
                    myAlert(data);
                }
            }
        },
        error: function () {
            myAlert('Sorry，服务器可能开小差啦, 请重试!');
        }
    });
}

/*提示 弹出*/
function myAlert(data) {
    $('#my-alert_print').text(data);
    $('#my-alert').modal({
        relatedTarget: this
    });
}

function post(url, params) {
    var temp = document.createElement("form");
    temp.action = url;
    temp.method = "post";
    temp.style.display = "none";
    for (var x in params) {
        var opt = document.createElement("input");
        opt.name = x;
        opt.value = params[x];
        temp.appendChild(opt);
    }
    document.body.appendChild(temp);
    temp.submit();
    return temp;
}

function del_row(id) {
    var attribute = id;
    var chkObj = document.getElementsByName(attribute);
    var tabObj = document.getElementById(id);
    for (var k = 0; k < chkObj.length; k++) {
        if (chkObj[k].checked) {
            tabObj.deleteRow(k + 1);
            k = -1;
            //表单数量
            var totalform = $('#id_casestep_set-TOTAL_FORMS');
            var newval = Number(totalform.val()) - 1;
            totalform.val(newval);
        }
    }
}

//添加行
function add_row(id) {
    var content = $("table#" + id + ' tbody').children('tr').last().html();
    var last_no = $("table#" + id + ' tbody tr').length - 2;
    var new_no = last_no + 1
    var exp = RegExp('-' + last_no + '-', 'g')
    var new_content = content.replace(exp, '-' + new_no + '-') //替换行数
    new_content = new_content.replace(/"\s(value=.*?)\s/g, '" ')
    new_content = new_content.replace(/selected/g, '')
    $("table#" + id + ' tbody').children('tr').last().after("<tr>" + new_content + "</tr>")
    //表单数量
    var totalform = $('#id_casestep_set-TOTAL_FORMS');
    var newval = Number(totalform.val()) + 1;
    totalform.val(newval);
}

//元素选择变更
function change_element(id) {
    var page = $('#' + id);
    var page_data = page.val();
    var url = '/haptest/page_element/' + page_data;
    $.get(url, function (data) {
        page.parent().next().children().html(data);
    });
};


function init_acs(language, theme, editor) {
    editor.setTheme("ace/theme/" + theme);
    editor.session.setMode("ace/mode/" + language);

    editor.setFontSize(17);

    editor.setReadOnly(false);

    editor.setOption("wrap", "free");

    ace.require("ace/ext/language_tools");
    editor.setOptions({
        enableBasicAutocompletion: true,
        enableSnippets: true,
        enableLiveAutocompletion: true,
        autoScrollEditorIntoView: true
    });


}


