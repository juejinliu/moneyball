$(document).ready(function () {
    $("#id_platform").change(function () {
    	var params = $("#id_platform option:selected").val();
        $.ajax({
            url:"{% url 'get_platform_fee' %}",
            type:'POST',
            data:{
            	'platform':params
            },
            dataType:'json',
            success:function (data) {
                $("#id_feerate").val(data.result);
            }
        });
    });
});