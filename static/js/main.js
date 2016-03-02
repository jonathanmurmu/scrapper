$(document).ready(function() {
    $('#dashboard_search_form').submit(function() { // catch the form's submit event
        $.ajax({ // create an AJAX call...
            data: $(this).serialize(), // get the form data
            type: $(this).attr('method'), // GET or POST
            url: $(this).attr('action'), // the file to call

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