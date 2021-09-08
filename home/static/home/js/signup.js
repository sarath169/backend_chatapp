var UserSignup = {
    
    init: function(){

        $("#signup-submit-btn").click(function(e){
            e.preventDefault();
            var values = {};
            $.each($("#user-signup-form").serializeArray(), function(i, field){
                values[field.name] = field.value;
            });

            $.ajax({
                url: UserSignup.create_user_api_url,
                type: "POST",
                data: values,
                success: function(response) {
                    console.log(response);
                    location.href = UserSignup.login_view_url;
                },
                error: function(xhr, errmsg, err){
                    error_responses = xhr.responseJSON
                    console.log(error_responses)
                    error_msg = "";
                    $.each(error_responses, function(key, errmsg){
                        error_msg += key +": "+errmsg + "\n"
                    })
                    alert(error_msg)
                }
            })
        })
    }


}