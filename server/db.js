const Database = require('better-sqlite3');
const path = require('path');

const db = new Database(path.join(__dirname, 'leaderboard.db'));

db.exec(`
    CREATE TABLE IF NOT EXISTS scores (
        uuid       TEXT     PRIMARY KEY,
        pseudo     TEXT     NOT NULL,
        money      INTEGER  NOT NULL DEFAULT 0,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
`);

function upsertScore(uuid, pseudo, money) {
    db.prepare(`
        INSERT INTO scores (uuid, pseudo, money, updated_at)
        VALUES (?, ?, ?, CURRENT_TIMESTAMP)
        ON CONFLICT(uuid) DO UPDATE SET
            pseudo     = excluded.pseudo,
            money      = MAX(money, excluded.money),
            updated_at = CURRENT_TIMESTAMP
    `).run(uuid, pseudo, parseInt(money));
}

function getLeaderboard(limit = 10) {
    return db.prepare(`
        SELECT pseudo, money,
               ROW_NUMBER() OVER (ORDER BY money DESC) AS rank
        FROM scores
        ORDER BY money DESC
        LIMIT ?
    `).all(limit);
}

module.exports = { upsertScore, getLeaderboard };
