var Login = {
    
    init: function(){

        $("#login-submit-btn").click(function(e){
            e.preventDefault();
            var values = {};
            $.each($("#user-login-form").serializeArray(), function(i, field){
                values[field.name] = field.value;
            });

            $.ajax({
                url: Login.login_api_url,
                type: "POST",
                data: values,
                success: function(response) {
                    console.log(response);
                    sessionStorage.clear();
                    $.each(response, function(key, value) {
                        sessionStorage.setItem(key, value);
                    });
                    location.href = Login.chat_panel_url.replace(
                        '9999', sessionStorage.getItem("user_id"));
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