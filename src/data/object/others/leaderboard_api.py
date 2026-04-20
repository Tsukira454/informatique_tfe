# Elvin Mouyart
# UTF-8
import threading
import requests
from object.others.logger import logger

API_BASE = "https://nexus.astry.be"
API_KEY  = "nexus_change_me"   # doit correspondre à API_KEY dans server/.env
TIMEOUT  = 5


def get_leaderboard():
    """Retourne la liste [{rank, pseudo, money}, ...] ou None si erreur."""
    try:
        r = requests.get(f"{API_BASE}/leaderboard", timeout=TIMEOUT)
        r.raise_for_status()
        return r.json()
    except Exception:
        logger.warning("Leaderboard inaccessible", exc_info=False)
        return None


def submit_score(account_uuid, pseudo, money):
    """Envoie le score en arrière-plan (non bloquant). Retourne True si OK."""
    result = {"ok": False}

    def _send():
        try:
            r = requests.post(
                f"{API_BASE}/score",
                json={"uuid": account_uuid, "pseudo": pseudo, "money": int(money)},
                headers={"x-api-key": API_KEY},
                timeout=TIMEOUT,
            )
            result["ok"] = r.status_code == 200
        except Exception:
            logger.warning("Impossible d'envoyer le score au serveur", exc_info=False)

    t = threading.Thread(target=_send, daemon=True)
    t.start()
    return t  # l'appelant peut join() pour attendre si besoin
