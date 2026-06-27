#!/usr/bin/env python3
"""
Exemples d'utilisation du bot de billeterie
"""

from bot import TicketBot, SiteList, QueueModule, Ticket
import logging

# Configurer le logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def example_1_psg_queue_it():
    """Exemple 1: Acheter des billets PSG avec Queue-it"""
    logger.info("=" * 50)
    logger.info("Exemple 1: PSG + Queue-it")
    logger.info("=" * 50)
    
    bot = TicketBot(
        site=SiteList.PSG,
        queue_module=QueueModule.QUEUE_IT
    )
    
    tickets = [
        Ticket(
            event_id="psg_match_2024",
            ticket_type="VIP",
            quantity=2,
            price=150.0
        ),
        Ticket(
            event_id="psg_match_2024",
            ticket_type="Standard",
            quantity=1,
            price=50.0
        )
    ]
    
    success = bot.run(tickets)
    return success


def example_2_lens_secutix():
    """Exemple 2: Acheter des billets Lens avec Secutix"""
    logger.info("=" * 50)
    logger.info("Exemple 2: Lens + Secutix")
    logger.info("=" * 50)
    
    bot = TicketBot(
        site=SiteList.LENS,
        queue_module=QueueModule.SECUTIX,
        timeout=60
    )
    
    tickets = [
        Ticket(
            event_id="lens_match_2024",
            ticket_type="Carré Or",
            quantity=3,
            price=200.0
        )
    ]
    
    success = bot.run(tickets)
    return success


def example_3_auteuil_wetix():
    """Exemple 3: Acheter des billets Auteuil avec Wetix"""
    logger.info("=" * 50)
    logger.info("Exemple 3: Auteuil + Wetix")
    logger.info("=" * 50)
    
    bot = TicketBot(
        site=SiteList.AUTEUIL,
        queue_module=QueueModule.WETIX
    )
    
    tickets = [
        Ticket(
            event_id="auteuil_2024",
            ticket_type="Tribune",
            quantity=4,
            price=80.0
        )
    ]
    
    success = bot.run(tickets)
    return success


def example_4_stade_de_france_paylogic():
    """Exemple 4: Acheter des billets Stade de France avec Paylogic"""
    logger.info("=" * 50)
    logger.info("Exemple 4: Stade de France + Paylogic")
    logger.info("=" * 50)
    
    bot = TicketBot(
        site=SiteList.STADE_DE_FRANCE,
        queue_module=QueueModule.PAYLOGIC
    )
    
    tickets = [
        Ticket(
            event_id="sdf_match_2024",
            ticket_type="Premium",
            quantity=2,
            price=175.0
        )
    ]
    
    success = bot.run(tickets)
    return success


def example_5_multiple_tickets():
    """Exemple 5: Acheter plusieurs types de billets"""
    logger.info("=" * 50)
    logger.info("Exemple 5: Tickets multiples")
    logger.info("=" * 50)
    
    bot = TicketBot(
        site=SiteList.TICKETMASTER_FR,
        queue_module=QueueModule.QUEUE_IT
    )
    
    tickets = [
        Ticket(event_id="evt_001", ticket_type="VIP", quantity=2, price=200.0),
        Ticket(event_id="evt_001", ticket_type="Premium", quantity=3, price=150.0),
        Ticket(event_id="evt_001", ticket_type="Standard", quantity=5, price=75.0),
        Ticket(event_id="evt_001", ticket_type="Economy", quantity=10, price=40.0),
    ]
    
    success = bot.run(tickets)
    return success


def main():
    """Fonction principale"""
    logger.info("🎫 Démarrage du Bot de Billeterie")
    
    # Décommenter l'exemple à tester
    
    # try:
    #     example_1_psg_queue_it()
    # except Exception as e:
    #     logger.error(f"Erreur Exemple 1: {e}")
    
    # try:
    #     example_2_lens_secutix()
    # except Exception as e:
    #     logger.error(f"Erreur Exemple 2: {e}")
    
    # try:
    #     example_3_auteuil_wetix()
    # except Exception as e:
    #     logger.error(f"Erreur Exemple 3: {e}")
    
    # try:
    #     example_4_stade_de_france_paylogic()
    # except Exception as e:
    #     logger.error(f"Erreur Exemple 4: {e}")
    
    # try:
    #     example_5_multiple_tickets()
    # except Exception as e:
    #     logger.error(f"Erreur Exemple 5: {e}")
    
    logger.info("✅ Exemples disponibles - Décommenter pour tester")


if __name__ == "__main__":
    main()
