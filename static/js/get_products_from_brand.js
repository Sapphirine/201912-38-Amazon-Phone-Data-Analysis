function generateProducts(){
    var brand = $("#brand_box").val()
    console.log(brand)

    $.ajax({
        type: 'POST',
        url: "/get_products",
        data: JSON.stringify({'brand': brand}),
        contentType: 'application/json;charset=UTF-8',
        success: function(response){
            $("#product_box").empty();
            var product_list = response['result']['product_list'];
//
            console.log(product_list);
            $.each(product_list, function(key, value){
                console.log("this is the value")
                console.log(value)
                var product_title = `
                    <option value = ${value}>${value}</option>
                `
                $("#product_box").append(product_title)
            });
        }
    })
//    console.log("sjdflsjkdflsd")
}