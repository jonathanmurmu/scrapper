$(document).ready(function() {
    // searching products in dashboard page
    $('#dashboard_search_form').submit(function() { // catch the form's submit event
        $.ajax({ // create an AJAX call...
            data: $(this).serialize(), // get the form data
            type: $(this).attr('method'), // GET or POST
            url: $(this).attr('action'), // the file to call
            beforeSend: function(){
                // clearing the product result area
                $('result_area').html('')  
                
                // clearing all the filters
                $('input[name=price_sort]').prop('checked', false);
                $('input[type=checkbox]').prop('checked', false);

                // displaying the loading image
                $("#load_div").show();

                // disabling the submit button
                $('#dashboard_search_submit').addClass("disabled")
            },
            complete: function(){
                // when the products are listed remove the loading image
                $("#load_div").hide();

                // enable the submit button again
                $('#dashboard_search_submit').removeClass("disabled")
            },
            success: function(json_data) { // on success..
                // json_result = json_data.product;
                $('.filter-panel').show()
                $('#result_area').html(json_data.result)
            },
            error: function() { // on error..
                alert("none")
            }
        });
        
        return false;
    });    
    
    // for filtering the products in the dashboard
    $('.filter-click').click(function(){
        $.ajax({
            data: $('#dashboard_filter_form').serialize(),
            type: $('#dashboard_filter_form').attr('method'), // GET or POST
            url: $('#dashboard_filter_form').attr('action'), // the file to call
            beforeSend: function(){
                // clearing the product result area.
                $('result_area').html('')           

                // displaying the loading image
                $("#load_div").show();

                // disabling the submit button
                $('#dashboard_search_submit').addClass("disabled")
            },
            complete: function(){
                // when the products are listed remove the loading image
                $("#load_div").hide();

                // enable the submit button again
                $('#dashboard_search_submit').removeClass("disabled")
            },
            success: function(json_data) { // on success..
                $('.filter-panel').show()
                $('#result_area').html(json_data.result)
            },
            error: function() { // on error..
                alert("none")
            }
        });
        return true;
    });
    
    // scrapping products in scrap page
    $('#scrap_form').submit(function() { // catch the form's submit event
        $.ajax({ // create an AJAX call...
            data: $(this).serialize(), // get the form data
            type: $(this).attr('method'), // GET or POST
            url: $(this).attr('action'), // the file to call
            beforeSend: function(){
                // clearing the product result area.
                $('#scrap_result_area').html('')                

                // displaying the loading image
                $("#load_div").show();

                // disabling the submit button
                $('#scrap_submit').addClass("disabled")
            },
            complete: function(){
                // when the products are listed remove the loading image
                $("#load_div").hide();

                // enable the submit button again
                $('#scrap_submit').removeClass("disabled")
            },
            success: function(json_data) { // on success..

                $('#scrap_result_area').html(json_data.result)
            },
            error: function() { // on error..
                alert("none")
            }
        });
        return false;
    });

    // ajax for changing the total on changing the quantity
    $("#id_quantity").change(function(){
        $.ajax({ // create an AJAX call...
            data: $("#quantity_form").serialize(), // get the form data
            type: $("#quantity_form").attr('method'), // GET or POST
            url: $("#quantity_form").attr('action'), // the file to call
            success: function(json_data) { // on success..
                if (json_data.success){
                    $('#total_price').html(json_data.total_price)
                    $('#place_order_link').removeClass("disabled")
                }
                else{
                    alert(json_data.message)
                    $('#place_order_link').addClass("disabled")
                }
                
            },
            error: function() { // on error..
                alert("Error")

            }
        });
        return false;
    });
});
