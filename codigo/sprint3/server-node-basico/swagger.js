const swaggerAutogen = require('swagger-autogen')();

// Arquivo que sera usado para documentacao. Usado no index.js
const outputFile = './swagger_output.json';

// Declaracao de todos os arquivos de rotas
const endpointsFiles = ['./rotas/padrao.js'];

swaggerAutogen(outputFile, endpointsFiles);