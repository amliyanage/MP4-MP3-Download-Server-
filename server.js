const express = require('express');
const ytdl = require('ytdl-core');
const cors = require('cors');

const app = express();
const port = 3001;

app.use(cors());

app.get('/video-options/:videoId', async (req, res) => {
    const { videoId } = req.params;

    try {
        const info = await ytdl.getInfo(`https://www.youtube.com/watch?v=${videoId}`);
        const formats = info.formats;

        const filteredFormats = formats.filter(format => format.hasVideo || format.hasAudio);

        res.json({
            formats: filteredFormats,
            bestQuality: filteredFormats.find(format => format.qualityLabel === '1440p') // Example for best quality
        });
    } catch (error) {
        console.error('Error fetching video info:', error);
        res.status(500).send('Error fetching video details');
    }
});

app.listen(port, () => {
    console.log(`Server running on http://localhost:${port}`);
});
