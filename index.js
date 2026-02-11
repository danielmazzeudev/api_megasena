const express = require('express');
const cors = require('cors');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = 3000;

app.use(cors());

app.get('/', (req, res) => {
    const filePath = path.join(__dirname, 'megasena.json');

    fs.readFile(filePath, 'utf8', (err, data) => {
        if (err) {
            console.error("Error reading file:", err);
            return res.status(500).json({ error: "Error reading database." });
        }

        try {
            const jsonData = JSON.parse(data);
            res.json(jsonData);
        } catch (parseErr) {
            res.status(500).json({ error: "Invalid JSON format." });
        }
    });
});

app.listen(PORT, () => {
    console.log(`Server running on port:${PORT}`);
});