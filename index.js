const express = require('express');
const cors = require('cors');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = 4000;

app.use(cors());

app.get('/', (req, res) => {
    const filePath = path.join(__dirname, 'megasena.json');

    fs.readFile(filePath, 'utf8', (err, data) => {
        if (err) {
            return res.status(500).json({ error: "Arquivo não encontrado." });
        }
        try {
            res.json(JSON.parse(data));
        } catch (parseErr) {
            res.status(500).json({ error: "Erro no formato do JSON." });
        }
    });
});

app.listen(PORT, () => {
    console.log(`✅ Servidor de dados rodando em:${PORT}`);
});