$(document).ready(function () {
    $("#platform_id").change(function () {
    	var params = $("#platform_id option:selected").val();
        $.ajax({
            url:root+"/getPlatformFee.action",
            type:'POST',
            data:{
            	'platform_id':params
            },
            dataType:'json',
            success:function (data) {
                $("#fee_rate").val(data.result);
            }
        });
    });


});