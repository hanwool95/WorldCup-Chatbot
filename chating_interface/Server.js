
const fetch = require('node-fetch');

const express = require("express");
const http = require('http');



const PORT = 3737;

var clientID = "사용자";

const app = express();
app.set('views', __dirname + '/views')
app.set("view engine", 'ejs')
app.use(express.static(__dirname + '/'));

app.get('/', (req, res) =>{
    res.render('interface')
})


let server = http.createServer(app);
server.listen(PORT, () => {
    console.log(`listening at http://127.0.0.1:${PORT}...`);
});

let socket = require('socket.io')(server);



socket.sockets.on('connection', function(client){

    console.log('Connection: '+ clientID);

    client.on('serverReceiver', function(value){
        socket.sockets.emit('clientReceiver', {clientID: clientID, message: value});
        fetch("http://127.0.0.1:8000/", {
            method: "POST",
            headers: { "Content-Type": "application/json",},
            body: JSON.stringify({
                query: value,
            }),
        }).then((response) => response.json()).then((data) =>
            socket.sockets.emit('clientReceiver', {clientID: 'chatbot', message: JSON.stringify(data['result'])}));
    });
});
