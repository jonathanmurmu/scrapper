$(document).ready(function() {
    $('#dashboard_search_form').submit(function() { // catch the form's submit event
        $.ajax({ // create an AJAX call...
            data: $(this).serialize(), // get the form data
            type: $(this).attr('method'), // GET or POST
            url: $(this).attr('action'), // the file to call
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
            	$('#result_area').html(json_data.result)
            },
            error: function() { // on error..
            	alert("none")
            }
        });
        return false;
    });
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