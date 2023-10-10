module.exports = (app) => {
    const path = require('path');
    const request = require('request');
    const serverConfig = require('../appSettings.json');
    const fs = require("fs");

    // Formula padrao para endpoints
    app.get('/health-check', (req, res) => {
        res.status(200).send("Server rodando!");
    });

    app.post('/processar-img', (req, res) => {
        // #swagger.tags = ['Processamento de imagens']
        // #swagger.description = 'Endpoint para processamento da imagem no modelo da Voyager.'
        /*
            #swagger.parameters['imagem'] = {
                type: 'file',
                required: 'true',
                description: 'Imagem a ser processada.',
            } 
        */
        const url = serverConfig.urlBackend + "/processar_img/";
        console.log("URL Backend: " + url);

        console.log("Salvando imagem...");

        // Apos isso, usar o fs pra ler de volta e jogar no corpo
        req.files.imagem.mv('./rotas/arquivos/temp/images/upload.jpg', function (err) {
            if (err) {
                console.log("Erro ao salvar imagem!");
                return res.status(500).send(err);
            }
            
            console.log("Sucesso ao salvar imagem!");
            console.log("Chamando Backend...");
            request.post({
                url,
                formData: {
                    "imagem": fs.createReadStream('./rotas/arquivos/temp/images/upload.jpg')
                }
            },
                (err, responseBack, body) => {
                    if (err) {
                        console.log("Erro ao chamar Backend!");
                    }

                    if (responseBack && responseBack.statusCode === 200) {
                        console.log("Sucesso ao chamar Backend!");
                    }

                    res.status(responseBack.statusCode).send(body);
                });
        });
    });

    app.get('/dados-modelo', (req, res) => {
        // #swagger.tags = ['Processamento de imagens']
        // #swagger.description = 'Endpoint para verificar acuracidade atual do modelo usado pelo projeto.'
        const url = serverConfig.urlBackend + "/main_model";
        console.log("Chamando URL: " + url);
        const options = {}

        request.get(
            url,
            options,
            (err, response, body) => {
                if (err) {
                    console.log("Erro!");
                }

                if (response.statusCode === 200) {
                    console.log("Sucesso!");
                }

                console.log("Body:");
                console.log(body);
                res.status(response.statusCode).send(body);
            });
    });

    app.get('/', (req, res) => {
        res.status(200)
            .sendFile(path.join(__dirname, '/paginas/home.html'));
    });

}