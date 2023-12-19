document.addEventListener('DOMContentLoaded', function() {
    var chatSocket = new WebSocket('ws://127.0.0.1:8001/ws/chat/' + advertId + '/' + userId + '/');

    document.querySelector('#chat-message-submit').onclick = function(e) {
        var messageInputDom = document.querySelector('#chat-message-input');
        var message = messageInputDom.value;
        chatSocket.send(JSON.stringify({
            'message': message
        }));
        messageInputDom.value = '';
    };

    chatSocket.onmessage = function(e) {
        var data = JSON.parse(e.data);

        console.log("data");

        var messageComponent = createMessageComponent(
            document.getElementById('chat-log'),
            data.sender_id,
            data.username,
            data.message,
            data.profilePicUrl,
            data.time
        );
    };
    

    chatSocket.onclose = function(e) {
        console.error('Chat socket closed unexpectedly');
    };
});   