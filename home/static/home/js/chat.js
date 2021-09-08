var Chat = {
    
    init: function(){

        $("#logout-submit-btn").click(function(e){
            e.preventDefault();
            sessionStorage.clear();
            location.href = Chat.login_view_url;
        })
    }


}