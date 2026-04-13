const express = require('express');
const cors = require('cors');
const fs = require('fs/promises');
const path = require('path');

const app = express();
const PORT = Number(process.env.PORT) || 4000;
const currentVersion = process.env.APP_VERSION || '39.0.0';
const dataFilePath = path.join(__dirname, 'python', 'megasena.json');

app.use(cors());

function setNoStore(res) {
    res.set({
        'Cache-Control': 'no-store, no-cache, must-revalidate, proxy-revalidate',
        Pragma: 'no-cache',
        Expires: '0',
        'Surrogate-Control': 'no-store',
    });
}

function normalizeDraw(draw) {
    return {
        draw_number: Number(draw?.draw_number) || 0,
        draw_date: String(draw?.draw_date || ''),
        numbers: Array.isArray(draw?.numbers)
            ? draw.numbers.map((number) => String(number).padStart(2, '0'))
            : [],
        winners_4_numbers: Number(draw?.winners_4_numbers) || 0,
        winners_5_numbers: Number(draw?.winners_5_numbers) || 0,
        winners_6_numbers: Number(draw?.winners_6_numbers) || 0,
        prize_value_4_numbers: Number(draw?.prize_value_4_numbers) || 0,
        prize_value_5_numbers: Number(draw?.prize_value_5_numbers) || 0,
        prize_value_6_numbers: Number(draw?.prize_value_6_numbers) || 0,
        accumulated_prize: Number(draw?.accumulated_prize) || 0,
        is_accumulated: Boolean(draw?.is_accumulated),
        estimated_next_prize: Number(draw?.estimated_next_prize) || 0,
    };
}

app.get('/', async (req, res) => {
    setNoStore(res);

    try {
        const rawData = await fs.readFile(dataFilePath, 'utf8');
        const parsedData = JSON.parse(rawData);

        if (!Array.isArray(parsedData)) {
            return res.status(500).json({ error: 'Unexpected JSON structure.' });
        }

        const normalizedData = parsedData
            .map(normalizeDraw)
            .filter((draw) => draw.draw_number > 0)
            .sort((a, b) => a.draw_number - b.draw_number);

        return res.json(normalizedData);
    } catch (error) {
        if (error.code === 'ENOENT') {
            return res.status(500).json({ error: 'File not found.' });
        }

        if (error instanceof SyntaxError) {
            return res.status(500).json({ error: 'Error on JSON file format.' });
        }

        return res.status(500).json({ error: 'Unexpected server error.' });
    }
});

app.get('/version', (req, res) => {
    setNoStore(res);
    res.json({ version: currentVersion });
});

app.listen(PORT, () => {
    console.log(`Server is running on port:${PORT}`);
    console.log(`Current version: ${currentVersion}`);
});
