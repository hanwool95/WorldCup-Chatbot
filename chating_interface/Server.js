
const fetch = require('node-fetch');

const express = require("express");
const http = require('http');
require('dotenv').config({ path: '../.env' });
const {TranslationServiceClient} = require('@google-cloud/translate');
const translationClient = new TranslationServiceClient();

const projectId = 'propane-primacy-353119';
const location = 'global';

async function translateKoToEng(text) {
    const request = {
        parent: `projects/${projectId}/locations/${location}`,
        contents: [text],
        mimeType: 'text/plain', // mime types: text/plain, text/html
        sourceLanguageCode: 'ko',
        targetLanguageCode: 'en',
    };

    const [response] = await translationClient.translateText(request);
    return response.translations[0].translatedText
}

async function translateEngToKo(text) {
    const request = {
        parent: `projects/${projectId}/locations/${location}`,
        contents: [text],
        mimeType: 'text/plain', // mime types: text/plain, text/html
        sourceLanguageCode: 'en',
        targetLanguageCode: 'ko',
    };

    const [response] = await translationClient.translateText(request);
    return response.translations[0].translatedText
}

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
        translateKoToEng(value)
            .then(
                (result) => fetch("http://127.0.0.1:8000/",
                    {
                        method: "POST",
                        headers: { "Content-Type": "application/json",},
                        body: JSON.stringify({
                            query: result,
                        }
                        ),
                    }
                    )
                    .then(
                        (response) => response.json()
                    )
                    .then(
                        (data) =>
                            translateEngToKo(JSON.stringify(data['result'])).then(
                                (translated_result) =>
                                    socket.sockets
                                        .emit('clientReceiver',
                                            {clientID: 'chatbot', message: translated_result})
                            )

                    )
            )

    });
});
