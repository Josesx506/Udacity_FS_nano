// var http = require('http');
// var fs = require('fs');

// const PORT = 8080;

// fs.readFile('src/index.html', function(error, html) {
//     if (error) {
//         throw error;
//     }
//     http.createServer(function (request, response) {
//         response.writeHeader(200, {'Content-Tyoe': 'text/html'});
//         response.write(html);
//         response.end();
//     }).listen(PORT)
// }); 


const express = require('express')
const request = require('request');

app = express();
const PORT = 3000;

app.get('/home', function(req, res) {
    request('http://127.0.0.1:5000/', function (error, response, body) {
        console.error('error:', error); // Print the error
        console.log('statusCode:', response && response.statusCode); // Print the response status code if a response was received
        console.log('body:', body); // Print the data received
        res.send(body); //Display the response on the website
      });      
});

app.listen(PORT, function (){ 
    console.log('Listening on Port 3000');
});  
