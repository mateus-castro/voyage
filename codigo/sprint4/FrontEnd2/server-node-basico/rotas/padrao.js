module.exports = (app) => {
    const path = require('path');

    // Formula padrao para endpoints
    app.get('/health-check', (req, res) => {
        res.status(200).send("Server rodando!");
    });

    app.post('/processar-img', (req, res) => {
        // #swagger.tags = ['Processamento de imagens']
        // #swagger.description = 'Endpoint para processamento da imagem no modelo da Voyager.'
        /*
            #swagger.parameters['singleFile'] = {
                type: 'file',
                required: 'true',
                description: 'Imagem a ser processada.',
            } 
        */

        // Retorno que virá da API Python
        const retorno = {
            "origem": "Humano",
            "aderencia": "80%",
            "acuracia": "90%",
        };
        res.status(200).send(retorno);
    });

    app.get('/', (req, res) => {
        res.status(200)
            .sendFile(path.join(__dirname, '/paginas/home.html'));
    });

}