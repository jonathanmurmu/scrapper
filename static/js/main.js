$(document).ready(function() {
    // searching products in dashboard page
    // var json_result;
    // var search_item;
     
    $('#dashboard_search_form').submit(function() { // catch the form's submit event
        $.ajax({ // create an AJAX call...
            data: $(this).serialize(), // get the form data
            type: $(this).attr('method'), // GET or POST
            url: $(this).attr('action'), // the file to call
            beforeSend: function(){
                // storing the search_item in order to ues it on click of filters.
                // search_item = $('#id_search').val();
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
    
    $('.filter-click').click(function(){
        // initailizng low to high or high to low in price_sort
        var price_sort = $('input[name=price_sort]:checked').val();

        // // both flipkart and amazon in checked
        // if ($('#checkbox_flipkart').prop("checked") == true && $('#checkbox_amazon').prop("checked") == true){
        //     site_choice = ''
        // }
        // // when only amazon is checked
        // else if ($('#checkbox_amazon').prop("checked") == true){
        //     site_choice = 'amazon'
        // }
        // // when only flipkart is checked
        // else if ($('#checkbox_flipkart').prop("checked") == true){
        //     site_choice = 'flipkart'
        // }    
        // // when nothing is checked
        // else{
        //     site_choice = ''
        // }
        $.ajax({
            // data: {
            //     'price_sort': price_sort, //'site_choice': site_choice
            //     'amazon': $('#checkbox_amazon').prop("checked"),
            //     'flipkart': $('#checkbox_flipkart').prop("checked")

            // }, // get the form data
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
                // json_result = json_data.product;
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
});