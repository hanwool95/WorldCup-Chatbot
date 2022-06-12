

window.onload = function(){
    var socket = io.connect('ws://127.0.0.1:3737');
    var div = document.getElementById('message');
    var txt = document.getElementById('txtChat');
    txt.focus();

    txt.onkeydown = sendMessage.bind(this);
    function sendMessage(event){
        if(event.keyCode == 13){
            var message = event.target.value;
            if(message){
                socket.emit('serverReceiver', message);
                txt.value = '';
            }
        }
    }

    socket.on('clientReceiver', function(data){
        var message = '['+ data.clientID + '님의 말' + '] ' + data.message;
        div.innerText += message + '\r\n';
        div.scrollTop = div.scrollHeight;
    });
};

