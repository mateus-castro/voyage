const app = require('express')();
const http = require('http');
const swagger = require('swagger-ui-express');
const swaggerFile = require('./swagger_output.json');
const bodyParser = require('body-parser');
var fileupload = require("express-fileupload");

// Iniciando server
http.createServer(app).listen('80');
console.log("Server iniciado na porta :80");
console.log("Swagger na porta :80/docs");

// Habilitando leitura do body
//app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());
app.use(fileupload());

// Subindo swagger gerado
app.use('/docs', swagger.serve, swagger.setup(swaggerFile));


// Todos arquivos de rotas devem ser declarados abaixo
// Tambem devem ser declarados no swagger.js para documentacao
require('./rotas/padrao')(app);
