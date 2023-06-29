module.exports = (app) => {

    // Formula padrao para endpoints
    app.get('/', (req, res) => {
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


        res.status(200).send(`Processando img pipipi popopo...`);
    });

}