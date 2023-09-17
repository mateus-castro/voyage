const swaggerAutogen = require('swagger-autogen')();
var serverConfig = require('./appSettings.json')

// Arquivo que sera usado para documentacao. Usado no index.js
const outputFile = './swagger_output.json';

// Declaracao de todos os arquivos de rotas
const endpointsFiles = ['./rotas/padrao.js'];

// Configuracoes adicionais para o swagger
const doc = {
    info: {
      title: serverConfig.nomeProjeto,
      description: serverConfig.descProjeto,
    },
    host: `${serverConfig.url}:${serverConfig.porta}`,
    schemes: [serverConfig.schema],
  };

swaggerAutogen(outputFile, endpointsFiles, doc);