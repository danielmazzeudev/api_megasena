const express = require('express');
const cors = require('cors');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = 4000;
const currentVersion = "24.0.0";

app.use(cors());

app.get('/', (req, res) => {
    const filePath = path.join(__dirname, 'python/megasena.json');

    fs.readFile(filePath, 'utf8', (err, data) => {
        if (err) {
            return res.status(500).json({ error: "File not found." });
        }
        try {
            res.json(JSON.parse(data));
        } catch (parseErr) {
            res.status(500).json({ error: "Error on JSON file format." });
        }
    });
});

app.get('/version', (req, res) => {
    res.json({ version: currentVersion });
});

app.listen(PORT, () => {
    console.log(`Server is running on port:${PORT}`);
    console.log(`Current version: ${currentVersion}`);
});