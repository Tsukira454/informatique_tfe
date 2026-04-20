const express = require('express');
const https   = require('https');
const http    = require('http');
const fs      = require('fs');
const db      = require('./db');

const app = express();
app.use(express.json());

const PORT    = process.env.PORT    || 3321;
const API_KEY = process.env.API_KEY || 'nexus_change_me';

function requireApiKey(req, res, next) {
    if (req.headers['x-api-key'] !== API_KEY) {
        return res.status(401).json({ error: 'Unauthorized' });
    }
    next();
}

// GET /leaderboard  —  public, retourne le top 10
app.get('/leaderboard', (req, res) => {
    try {
        res.json(db.getLeaderboard(10));
    } catch (e) {
        res.status(500).json({ error: e.message });
    }
});

// POST /score  —  protégé par API key, enregistre / met à jour un score
app.post('/score', requireApiKey, (req, res) => {
    try {
        const { uuid, pseudo, money } = req.body;
        if (!uuid || !pseudo || money === undefined) {
            return res.status(400).json({ error: 'uuid, pseudo et money requis' });
        }
        db.upsertScore(uuid, pseudo, parseInt(money));
        res.json({ ok: true });
    } catch (e) {
        res.status(500).json({ error: e.message });
    }
});

// Démarrage : HTTPS si les certs sont présents, HTTP sinon
const certPath = './certs/cert.pem';
const keyPath  = './certs/key.pem';

if (fs.existsSync(certPath) && fs.existsSync(keyPath)) {
    const creds = {
        key:  fs.readFileSync(keyPath),
        cert: fs.readFileSync(certPath),
    };
    https.createServer(creds, app).listen(PORT, () => {
        console.log(`[Nexus] Leaderboard HTTPS sur le port ${PORT}`);
    });
} else {
    http.createServer(app).listen(PORT, () => {
        console.log(`[Nexus] Leaderboard HTTP sur le port ${PORT} (pas de certs trouvés dans ./certs/)`);
    });
}
