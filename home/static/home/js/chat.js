var Chat = {

    messages_list: [],
    
    init: function(){

        $("#logout-submit-btn").click(function(e){
            e.preventDefault();
            sessionStorage.clear();
            location.href = Chat.login_view_url;
        });


        // $("#send-msg").click(function(e){
        //     e.preventDefault();
        //     Chat.send_message();
        // });
    },

    send_message: function(){
        msg = $("input[name='message-text']").val();
        console.log(msg)
        Chat.messages_list.push(msg)
        // clear the input box
        $("input[name='message-text']").val('')

        if (Chat.messages_list){
            $(".chat-messages").append("<p>" + msg + "</p>")
        }

    },

}


