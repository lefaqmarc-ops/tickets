#!/usr/bin/env python3
"""
Bot pour l'ajout au panier de billets de billeterie
Support des sites: Auteuil, PSG, Lens, TicketMaster FR, Wetix FCFS, Stade De France
Support des modules queue: Queue-it, Wetix, Secutix, Paylogic
"""

import requests
import time
from enum import Enum
from typing import Optional, Dict, List
from dataclasses import dataclass
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SiteList(Enum):
    """Sites de billeterie supportés"""
    AUTEUIL = "auteuil"
    PSG = "psg"
    LENS = "lens"
    TICKETMASTER_FR = "ticketmaster_fr"
    WETIX_FCFS = "wetix_fcfs"
    STADE_DE_FRANCE = "stade_de_france"


class QueueModule(Enum):
    """Modules de queue supportés"""
    QUEUE_IT = "queue_it"
    WETIX = "wetix"
    SECUTIX = "secutix"
    PAYLOGIC = "paylogic"


@dataclass
class Ticket:
    """Classe représentant un billet"""
    event_id: str
    ticket_type: str
    quantity: int
    price: Optional[float] = None


@dataclass
class Cart:
    """Classe représentant un panier"""
    session_id: str
    tickets: List[Ticket]
    total_price: float = 0.0


class TicketBotBase:
    """Classe de base pour le bot de billeterie"""
    
    def __init__(self, site: SiteList, queue_module: QueueModule, timeout: int = 30):
        self.site = site
        self.queue_module = queue_module
        self.timeout = timeout
        self.session = requests.Session()
        self.cart: Optional[Cart] = None
        self.queue_token: Optional[str] = None
        
    def get_site_url(self) -> str:
        """Retourne l'URL de base du site"""
        urls = {
            SiteList.AUTEUIL: "https://www.auteuil.com",
            SiteList.PSG: "https://www.psg.fr",
            SiteList.LENS: "https://www.lensfc.fr",
            SiteList.TICKETMASTER_FR: "https://www.ticketmaster.fr",
            SiteList.WETIX_FCFS: "https://www.wetix.fr",
            SiteList.STADE_DE_FRANCE: "https://www.stadedefrance.com"
        }
        return urls[self.site]
    
    def initialize_queue(self) -> bool:
        """Initialise la queue selon le module utilisé"""
        logger.info(f"Initialisation de la queue: {self.queue_module.value}")
        try:
            if self.queue_module == QueueModule.QUEUE_IT:
                return self._init_queue_it()
            elif self.queue_module == QueueModule.WETIX:
                return self._init_wetix()
            elif self.queue_module == QueueModule.SECUTIX:
                return self._init_secutix()
            elif self.queue_module == QueueModule.PAYLOGIC:
                return self._init_paylogic()
        except Exception as e:
            logger.error(f"Erreur lors de l'initialisation de la queue: {e}")
            return False
    
    def _init_queue_it(self) -> bool:
        """Initialise Queue-it"""
        logger.info("Initialisation Queue-it")
        try:
            # Intégration Queue-it
            headers = {
                'User-Agent': 'TicketBot/1.0'
            }
            response = self.session.get(
                f"{self.get_site_url()}/queue",
                headers=headers,
                timeout=self.timeout
            )
            if response.status_code == 200:
                # Extraction du token Queue-it
                self.queue_token = response.headers.get('QueueITToken')
                logger.info("Queue-it initialisée avec succès")
                return True
        except Exception as e:
            logger.error(f"Erreur Queue-it: {e}")
        return False
    
    def _init_wetix(self) -> bool:
        """Initialise Wetix"""
        logger.info("Initialisation Wetix")
        try:
            response = self.session.post(
                f"{self.get_site_url()}/api/wetix/init",
                json={"site": self.site.value},
                timeout=self.timeout
            )
            if response.status_code == 200:
                self.queue_token = response.json().get('token')
                logger.info("Wetix initialisée avec succès")
                return True
        except Exception as e:
            logger.error(f"Erreur Wetix: {e}")
        return False
    
    def _init_secutix(self) -> bool:
        """Initialise Secutix"""
        logger.info("Initialisation Secutix")
        try:
            response = self.session.post(
                f"{self.get_site_url()}/api/secutix/init",
                json={"site": self.site.value},
                timeout=self.timeout
            )
            if response.status_code == 200:
                self.queue_token = response.json().get('session_id')
                logger.info("Secutix initialisée avec succès")
                return True
        except Exception as e:
            logger.error(f"Erreur Secutix: {e}")
        return False
    
    def _init_paylogic(self) -> bool:
        """Initialise Paylogic"""
        logger.info("Initialisation Paylogic")
        try:
            response = self.session.post(
                f"{self.get_site_url()}/api/paylogic/init",
                json={"site": self.site.value},
                timeout=self.timeout
            )
            if response.status_code == 200:
                self.queue_token = response.json().get('session_token')
                logger.info("Paylogic initialisée avec succès")
                return True
        except Exception as e:
            logger.error(f"Erreur Paylogic: {e}")
        return False
    
    def create_cart(self) -> bool:
        """Crée un nouveau panier"""
        logger.info("Création d'un nouveau panier")
        try:
            response = self.session.post(
                f"{self.get_site_url()}/api/cart/create",
                headers=self._get_headers(),
                timeout=self.timeout
            )
            if response.status_code == 201:
                session_id = response.json().get('session_id')
                self.cart = Cart(session_id=session_id, tickets=[])
                logger.info(f"Panier créé: {session_id}")
                return True
        except Exception as e:
            logger.error(f"Erreur lors de la création du panier: {e}")
        return False
    
    def add_to_cart(self, ticket: Ticket) -> bool:
        """Ajoute un billet au panier"""
        if not self.cart:
            logger.error("Aucun panier n'a été créé")
            return False
        
        logger.info(f"Ajout au panier: {ticket.quantity}x {ticket.ticket_type}")
        try:
            response = self.session.post(
                f"{self.get_site_url()}/api/cart/{self.cart.session_id}/add",
                json={
                    "event_id": ticket.event_id,
                    "ticket_type": ticket.ticket_type,
                    "quantity": ticket.quantity
                },
                headers=self._get_headers(),
                timeout=self.timeout
            )
            if response.status_code == 200:
                self.cart.tickets.append(ticket)
                logger.info(f"Billet ajouté au panier avec succès")
                return True
        except Exception as e:
            logger.error(f"Erreur lors de l'ajout au panier: {e}")
        return False
    
    def remove_from_cart(self, ticket_id: str) -> bool:
        """Supprime un billet du panier"""
        if not self.cart:
            logger.error("Aucun panier n'a été créé")
            return False
        
        logger.info(f"Suppression du billet: {ticket_id}")
        try:
            response = self.session.post(
                f"{self.get_site_url()}/api/cart/{self.cart.session_id}/remove",
                json={"ticket_id": ticket_id},
                headers=self._get_headers(),
                timeout=self.timeout
            )
            if response.status_code == 200:
                logger.info("Billet supprimé du panier")
                return True
        except Exception as e:
            logger.error(f"Erreur lors de la suppression du billet: {e}")
        return False
    
    def get_cart(self) -> Optional[Dict]:
        """Récupère le contenu du panier"""
        if not self.cart:
            logger.error("Aucun panier n'a été créé")
            return None
        
        try:
            response = self.session.get(
                f"{self.get_site_url()}/api/cart/{self.cart.session_id}",
                headers=self._get_headers(),
                timeout=self.timeout
            )
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            logger.error(f"Erreur lors de la récupération du panier: {e}")
        return None
    
    def checkout(self) -> bool:
        """Procède à la validation du panier"""
        if not self.cart:
            logger.error("Aucun panier n'a été créé")
            return False
        
        logger.info("Validation du panier (checkout)")
        try:
            response = self.session.post(
                f"{self.get_site_url()}/api/cart/{self.cart.session_id}/checkout",
                headers=self._get_headers(),
                timeout=self.timeout
            )
            if response.status_code == 200:
                logger.info("Panier validé avec succès")
                return True
        except Exception as e:
            logger.error(f"Erreur lors de la validation du panier: {e}")
        return False
    
    def _get_headers(self) -> Dict[str, str]:
        """Retourne les headers HTTP avec le token de queue"""
        headers = {
            'User-Agent': 'TicketBot/1.0',
            'Content-Type': 'application/json'
        }
        if self.queue_token:
            headers['Authorization'] = f'Bearer {self.queue_token}'
        return headers


class TicketBot(TicketBotBase):
    """Bot principal pour l'achat de billets"""
    
    def run(self, tickets_to_buy: List[Ticket]) -> bool:
        """Exécute la séquence complète d'achat"""
        logger.info(f"Démarrage du bot pour {self.site.value}")
        
        # Étape 1: Initialiser la queue
        if not self.initialize_queue():
            logger.error("Impossible d'initialiser la queue")
            return False
        
        time.sleep(1)
        
        # Étape 2: Créer un panier
        if not self.create_cart():
            logger.error("Impossible de créer un panier")
            return False
        
        time.sleep(1)
        
        # Étape 3: Ajouter les billets au panier
        for ticket in tickets_to_buy:
            if not self.add_to_cart(ticket):
                logger.error(f"Impossible d'ajouter le billet: {ticket}")
                return False
            time.sleep(0.5)
        
        # Étape 4: Afficher le panier
        cart_content = self.get_cart()
        if cart_content:
            logger.info(f"Contenu du panier: {cart_content}")
        
        # Étape 5: Valider le panier
        if not self.checkout():
            logger.error("Impossible de valider le panier")
            return False
        
        logger.info("Achat complété avec succès!")
        return True


def main():
    """Fonction principale pour tester le bot"""
    
    # Exemple d'utilisation
    bot = TicketBot(
        site=SiteList.PSG,
        queue_module=QueueModule.QUEUE_IT
    )
    
    # Créer des billets à acheter
    tickets = [
        Ticket(
            event_id="evt_123456",
            ticket_type="VIP",
            quantity=2,
            price=150.0
        ),
        Ticket(
            event_id="evt_123456",
            ticket_type="Standard",
            quantity=1,
            price=50.0
        )
    ]
    
    # Lancer l'achat
    bot.run(tickets)


if __name__ == "__main__":
    main()
