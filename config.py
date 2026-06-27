"""
Configuration centralisée du bot de billeterie
Basée sur les APIs découvertes des sites réels
"""
import os
from dotenv import load_dotenv

load_dotenv()

# URLs des sites
SITE_URLS = {
    "auteuil": os.getenv("AUTEUIL_URL", "https://www.auteuil.com"),
    "psg": os.getenv("PSG_URL", "https://billetterie.psg.fr/fr"),
    "lens": os.getenv("LENS_URL", "https://www.lensfc.fr"),
    "ticketmaster_fr": os.getenv("TICKETMASTER_FR_URL", "https://www.ticketmaster.fr"),
    "wetix_fcfs": os.getenv("WETIX_FCFS_URL", "https://www.wetix.fr"),
    "stade_de_france": os.getenv("STADE_DE_FRANCE_URL", "https://www.stadefrance.com/fr/billetteries/concerts"),
}

# Authentification
API_KEY = os.getenv("API_KEY", "")
SESSION_TOKEN = os.getenv("SESSION_TOKEN", "")
TICKETMASTER_API_KEY = os.getenv("TICKETMASTER_API_KEY", "")

# Timeouts
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "30"))

# User Agent
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

# ========== ENDPOINTS DÉCOUVERTS ==========

# PSG Billetterie - API endpoints
PSG_ENDPOINTS = {
    "events": "/api/v1/events",
    "event_details": "/api/v1/events/{event_id}",
    "event_seats": "/api/v1/events/{event_id}/seats",
    "cart_create": "/api/v1/cart",
    "cart_add": "/api/v1/cart/{session_id}/items",
    "cart_remove": "/api/v1/cart/{session_id}/items/{ticket_id}",
    "cart_get": "/api/v1/cart/{session_id}",
    "cart_update": "/api/v1/cart/{session_id}/update",
    "cart_validate": "/api/v1/cart/{session_id}/validate",
    "checkout": "/api/v1/cart/{session_id}/checkout",
    "order": "/api/v1/order",
}

# Stade de France - Utilise France Billet/Ticketmaster
STADE_DE_FRANCE_ENDPOINTS = {
    "events": "/api/v1/events",
    "event_details": "/api/v1/events/{event_id}",
    "cart_create": "/api/v1/cart",
    "cart_add": "/api/v1/cart/{session_id}/items",
    "cart_get": "/api/v1/cart/{session_id}",
    "checkout": "/api/v1/cart/{session_id}/checkout",
}

# TicketMaster France - API publique
TICKETMASTER_ENDPOINTS = {
    "discovery_base": "https://app.ticketmaster.com/discovery/v2/",
    "events": "events.json",
    "event_details": "events/{event_id}.json",
    "venues": "venues.json",
    "attractions": "attractions.json",
}

# Queue Modules Endpoints
QUEUE_ENDPOINTS = {
    "queue_it": {
        "init": "/api/queue/queue-it/init",
        "status": "/api/queue/queue-it/status",
    },
    "wetix": {
        "init": "/api/queue/wetix/init",
        "status": "/api/queue/wetix/status",
    },
    "secutix": {
        "init": "/api/queue/secutix/init",
        "status": "/api/queue/secutix/status",
    },
    "paylogic": {
        "init": "/api/queue/paylogic/init",
        "status": "/api/queue/paylogic/status",
    },
}

# Headers par défaut
DEFAULT_HEADERS = {
    "User-Agent": USER_AGENT,
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "fr-FR,fr;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Content-Type": "application/json",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
}

# Configuration des retries
RETRY_CONFIG = {
    "total": 3,
    "backoff_factor": 1,
    "status_forcelist": [429, 500, 502, 503, 504],
    "allowed_methods": ["HEAD", "GET", "OPTIONS", "POST", "DELETE"],
}

# Délais entre les requêtes (en secondes)
DELAYS = {
    "queue_init": 1,
    "cart_create": 1,
    "add_ticket": 0.5,
    "checkout": 2,
}

# ========== TOKENS ET SESSIONS ==========
# Ces valeurs doivent être définies dans .env ou obtenues à l'exécution

CSRF_TOKEN = os.getenv("CSRF_TOKEN", "")
SESSION_ID = os.getenv("SESSION_ID", "")
QUEUE_TOKEN = os.getenv("QUEUE_TOKEN", "")

# ========== LOGGING ==========
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", "ticket_bot.log")
