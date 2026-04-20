const express = require('express');
const mysql = require('mysql2/promise');
require('dotenv').config();

const app = express();
app.use(express.json());

// === Connexion DB ===
const db = mysql.createPool({
    host: process.env.DB_HOST,
    user: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
    database: process.env.DB_NAME
});

// === CREATE PLAYER ===
app.post('/player', async (req, res) => {
    try {
        const { player_name, player_money, player_energy, player_skin } = req.body;

        if (!player_name) {
            return res.status(400).json({ error: 'player_name est requis' });
        }

        const [result] = await db.execute(
            'INSERT INTO leaderboard (player_name, player_money, player_energy, player_skin) VALUES (?, ?, ?, ?)',
            [player_name, player_money || 0, player_energy || 0, player_skin || 'null']
        );

        res.status(201).json({
            message: 'Joueur créé',
            id: result.insertId
        });
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

// === UPDATE PLAYER ===
app.put('/player/:id', async (req, res) => {
    try {
        const { id } = req.params;
        const { player_name, player_money, player_energy, player_skin } = req.body;

        const [result] = await db.execute(
            'UPDATE leaderboard SET player_name=?, player_money=?, player_energy=?, player_skin=? WHERE idleaderboard=?',
            [player_name, player_money, player_energy, player_skin, id]
        );

        if (result.affectedRows === 0) {
            return res.status(404).json({ error: 'Joueur introuvable' });
        }

        res.json({ message: 'Joueur mis à jour' });
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

// === GET LEADERBOARD ===
app.get('/leaderboard', async (req, res) => {
    try {
        const limit = parseInt(req.query.limit) || 10;

        const [rows] = await db.execute(
            'SELECT * FROM leaderboard ORDER BY player_money DESC LIMIT ?',
            [limit]
        );

        res.json(rows);
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

// === LANCEMENT ===
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Serveur lancé sur http://localhost:${PORT}`);
});