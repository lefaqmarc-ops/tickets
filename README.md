# 🎫 Ticket Bot - Bot d'achat de billets automatisé

Bot Python pour automatiser l'ajout au panier de billets de billeterie.

## 📋 Fonctionnalités

### Sites supportés
- ✅ Auteuil
- ✅ PSG
- ✅ Lens
- ✅ TicketMaster FR
- ✅ Wetix FCFS
- ✅ Stade De France

### Modules Queue
- ✅ Queue-it
- ✅ Wetix
- ✅ Secutix
- ✅ Paylogic

### Opérations
- Initialisation automatique de la queue
- Création et gestion du panier
- Ajout/suppression de billets
- Consultation du panier
- Validation (checkout) du panier

## 🚀 Installation

### Prérequis
- Python 3.8+
- pip

### Setup

1. **Cloner le repo**
```bash
git clone https://github.com/lefaqmarc-ops/tickets.git
cd tickets
```

2. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

3. **Configurer l'environnement**
```bash
cp .env.example .env
# Éditer .env avec vos configurations
```

## 💻 Utilisation

### Exemple basique

```python
from bot import TicketBot, SiteList, QueueModule, Ticket

# Créer une instance du bot
bot = TicketBot(
    site=SiteList.PSG,
    queue_module=QueueModule.QUEUE_IT
)

# Définir les billets à acheter
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
success = bot.run(tickets)
if success:
    print("✅ Achat réussi!")
else:
    print("❌ Erreur lors de l'achat")
```

### Exemple avec Auteuil et Secutix

```python
from bot import TicketBot, SiteList, QueueModule, Ticket

bot = TicketBot(
    site=SiteList.AUTEUIL,
    queue_module=QueueModule.SECUTIX,
    timeout=60
)

tickets = [
    Ticket(
        event_id="evt_789012",
        ticket_type="Carré Or",
        quantity=3,
        price=200.0
    )
]

bot.run(tickets)
```

## ⚙️ Configuration

### Variables d'environnement (.env)

```env
# URLs des sites (modifiez si nécessaire)
AUTEUIL_URL=https://www.auteuil.com
PSG_URL=https://www.psg.fr
LENS_URL=https://www.lensfc.fr
TICKETMASTER_FR_URL=https://www.ticketmaster.fr
WETIX_FCFS_URL=https://www.wetix.fr
STADE_DE_FRANCE_URL=https://www.stadedefrance.com

# Authentification
API_KEY=votre_api_key
SESSION_TOKEN=votre_session_token

# Timeout des requêtes
REQUEST_TIMEOUT=30
```

## 📖 Structure du code

### Classes principales

#### `Ticket`
Représente un billet à acheter.
```python
Ticket(
    event_id: str,        # ID de l'événement
    ticket_type: str,     # Type de billet (VIP, Standard, etc.)
    quantity: int,        # Quantité
    price: float = None   # Prix (optionnel)
)
```

#### `Cart`
Représente le panier.
```python
Cart(
    session_id: str,      # ID de session
    tickets: List[Ticket] # Liste des billets
)
```

#### `TicketBot`
Bot principal pour l'achat de billets.

**Méthodes principales :**
- `run(tickets: List[Ticket]) -> bool` - Exécute la séquence complète d'achat
- `initialize_queue() -> bool` - Initialise la queue
- `create_cart() -> bool` - Crée un panier
- `add_to_cart(ticket: Ticket) -> bool` - Ajoute un billet
- `remove_from_cart(ticket_id: str) -> bool` - Supprime un billet
- `get_cart() -> Dict` - Récupère le panier
- `checkout() -> bool` - Valide le panier

## 📝 Logging

Le bot utilise le module `logging` de Python. Tous les événements importants sont loggés.

```
INFO - Initialisation de la queue: queue_it
INFO - Initialisation Queue-it
INFO - Création d'un nouveau panier
INFO - Panier créé: 123abc456def
INFO - Ajout au panier: 2x VIP
```

## 🔧 Personnalisation

### Ajouter un nouveau site

1. Ajouter l'énumération dans `SiteList`
2. Ajouter l'URL dans `config.py`
3. Ajouter le mapping dans `get_site_url()`

### Ajouter un nouveau module queue

1. Ajouter l'énumération dans `QueueModule`
2. Implémenter la méthode `_init_<module_name>()`
3. Ajouter l'appel dans `initialize_queue()`

## ⚠️ Important

**À adapter selon les APIs réelles :**

1. Les endpoints API dans `config.py`
2. Les headers d'authentification
3. Les formats de requêtes/réponses
4. Les tokens et sessions

## 🐛 Troubleshooting

### Erreur : "Module not found"
```bash
pip install -r requirements.txt
```

### Erreur : "Connection refused"
- Vérifier les URLs dans `.env`
- Vérifier la connectivité réseau

### Erreur d'authentification
- Vérifier `API_KEY` et `SESSION_TOKEN` dans `.env`
- Vérifier les headers d'authentification

## 📌 À faire

- [ ] Adapter les endpoints réels des APIs
- [ ] Ajouter les headers d'authentification spécifiques
- [ ] Implémenter les retry logic
- [ ] Ajouter les tests unitaires
- [ ] Ajouter la gestion des exceptions spécifiques
- [ ] Documenter les APIs de chaque site

## 📞 Support

Pour toute question, consultez les logs ou ouvrez une issue.

## 📄 Licence

MIT
