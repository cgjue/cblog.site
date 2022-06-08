
function deleteObject(obj, val, htmlid) {
    let con = confirm('Are you sure?');
    if (con) {
        $.post(val, null, function (data, status) {
            if (typeof (data.status) != "undefined" && data.status != 0) {
                alert(data.msg)
                return;
            }
            $(obj).parents('tr').remove();
            $(htmlid).text(parseInt($(htmlid).text()) - 1);

        })
    }
}