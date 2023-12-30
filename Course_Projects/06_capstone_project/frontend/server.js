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

const express = require('express');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 8080;

// Serve static files from the 'src' and 'components' directories
app.use(express.static(path.join(__dirname, 'src')));
app.use(express.static(path.join(__dirname, 'components')));
app.use(express.static(path.join(__dirname, 'stylesheets')));

// Start the server
app.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
});
