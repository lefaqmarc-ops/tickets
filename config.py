"""
Configuration centralisée du bot de billeterie
"""
import os
from dotenv import load_dotenv

load_dotenv()

# URLs des sites
SITE_URLS = {
    "auteuil": os.getenv("AUTEUIL_URL", "https://www.auteuil.com"),
    "psg": os.getenv("PSG_URL", "https://www.psg.fr"),
    "lens": os.getenv("LENS_URL", "https://www.lensfc.fr"),
    "ticketmaster_fr": os.getenv("TICKETMASTER_FR_URL", "https://www.ticketmaster.fr"),
    "wetix_fcfs": os.getenv("WETIX_FCFS_URL", "https://www.wetix.fr"),
    "stade_de_france": os.getenv("STADE_DE_FRANCE_URL", "https://www.stadedefrance.com"),
}

# Authentification
API_KEY = os.getenv("API_KEY", "")
SESSION_TOKEN = os.getenv("SESSION_TOKEN", "")

# Timeouts
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "30"))

# User Agent
USER_AGENT = "TicketBot/1.0 (+http://github.com/lefaqmarc-ops/tickets)"

# Endpoints API (à adapter selon les sites réels)
ENDPOINTS = {
    "queue_init": "/api/queue/init",
    "cart_create": "/api/cart/create",
    "cart_add": "/api/cart/{session_id}/add",
    "cart_remove": "/api/cart/{session_id}/remove",
    "cart_get": "/api/cart/{session_id}",
    "cart_checkout": "/api/cart/{session_id}/checkout",
}
