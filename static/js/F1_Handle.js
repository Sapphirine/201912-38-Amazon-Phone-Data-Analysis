function sendBrand(){
    var brand = $("#brand_box").val()
    console.log(brand)

    $.ajax({
        type: 'POST',
        url: "/phone_recommend",
        data: JSON.stringify(brand),
        contentType: 'application/json;charset=UTF-8',
        success: function(response){
            $("#my_div").empty();
            var phone_list = response['result'];
            console.log(phone_list);
            $.each(phone_list, function(index, value){
                $("#my_div").append(index + ":" + value + '<br>')
            });
        }
    })
//    console.log("sjdflsjkdflsd")
}

