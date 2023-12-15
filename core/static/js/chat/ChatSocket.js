document.addEventListener('DOMContentLoaded', function() {
    var chatSocket = new WebSocket("ws://127.0.0.1:8001/ws/path/");

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
        var chatLog = document.querySelector('#chat-log');
        chatLog.value += (data.message + '\n');
    };

    chatSocket.onclose = function(e) {
        console.error('Chat socket closed unexpectedly');
    };
});   