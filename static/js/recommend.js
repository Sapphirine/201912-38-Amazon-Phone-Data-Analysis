function sendBrand(){
    var brand = $("#brand_box").val()
    var price = $("#price_box").val()
    console.log(brand)

    $.ajax({
        type: 'POST',
        url: "/phone_recommend",
        data: JSON.stringify({'brand': brand, 'price': price}),
        contentType: 'application/json;charset=UTF-8',
        success: function(response){
            $("#my_div").empty();
            var phone_list = response['result'];

            console.log(phone_list);
            $.each(phone_list, function(index, value){
                console.log(value)
//                $("#my_div").append(index + ":" + value['rating'] + '<br>')
                var phone_table_html = `
                  <div class="pricing-table">
                      <h3 class="pricing-title">${value['brand']}</h3>
                      <div class="price">$ ${value['price']}</sup></div>
                      <!-- Lista de Caracteristicas / Propiedades -->
                      <div><img src = ${value['image_url']}></div>
                      <div class="table-buy">
                          <p>${value['title']}</p>
                          <a href=${value['link']} class="pricing-action">Details</a>
                      </div>
                  </div>
                `
                $("#my_div").append(phone_table_html)
            });
        }
    })
//    console.log("sjdflsjkdflsd")
}

