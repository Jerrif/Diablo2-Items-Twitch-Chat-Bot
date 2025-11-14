# Diablo II Items Twitch Chat Bot

Have you ever been watching a Diablo 2 speedrun, and seen that familiar, oh-so-beautiful gold colored item text on the ground? Your excitement builds only for the streamer to move on without even acknowledging its existence?
<img alt="The rondel is Heart Carver, it gives +4 find item" src="https://diablo2.diablowiki.net/images/4/41/World-event16.jpg"/>

"Unique rondel, poggers! That's Wizspike! Wait, no - that's a bone knife... so what's that rondel then?"

A Python-based Twitch chat bot I wrote for Diablo 2 speedrunning streams. It provides instant access to Diablo II item statistics, including unique and set item data. Users can query the bot for detailed item information using simple chat commands.

## Features

- **Web Scraping**: Automatically extracts item data from [diablo.gamepedia.com](https://diablo.gamepedia.com) (although I realised too late that I should have used [The Arreat Summit](https://classic.battle.net/diablo2exp/))
- **SQLite Database**: Stores 100+ unique and set items with their complete statistics
- **Twitch Integration**: Real-time chat bot that responds to user queries in Twitch chat
- **Smart Search**: Find items by name or type (e.g., `!unique coldkill` or `!unique sword`)
- **Text Formatting**: Automatically formats item stats for readability in chat messages

## Tech Stack

- **Language**: Python 3
- **Database**: SQLite3
- **APIs**: Twitch IRC
- **Web Scraping**: urllib, regex
- **Key Libraries**: socket, sqlite3, re, time

## Usage

Once the bot is running in your Twitch chat, users can query items:

### Unique Items
```
!unique coldkill         # Search by item name
!unique sword            # Search by item type
!unique thestoneofjordan # Search for a specific unique ring
```

### Set Items
```
!set sigonsguard         # Search by set name
!set towershield         # Search by item type
```

The bot responds with formatted item statistics including:
- Damage/Defense values
- Requirement levels
- Special attributes and bonuses
- Class-specific bonuses

## Getting Started

### Prerequisites

- Python 3.6+
- Twitch account with bot permissions
- OAuth token from Twitch

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Diablo2-Items-Twitch-Chat-Bot.git
cd Diablo2-Items-Twitch-Chat-Bot
```

2. Configure credentials in `bot_init.py`:
```python
PASS = "oauth:YOUR_OAUTH_TOKEN_HERE"
CHANNEL = "your_twitch_channel"
```

3. (Optional) Initialize the database by running the scraper (or just use the included d2items.db):
```bash
python items.py
```

4. Start the bot:
```bash
python bot_run.py
```

## How It Works

### Data Collection (items.py)
- Scrapes all unique items and set items from a D2 wiki
- Parses HTML tables using regex to extract item names and statistics
- Handles website inconsistencies and data formatting issues
- Stores data in a SQLite database

### Bot Operations (bot_run.py)
- Connects to Twitch IRC and monitors chat for commands
- Queries the database for matching items
- Formats item stats for readability & *brevity* (twitch's ambiguous ~<500 char limit)
- Implements cooldown functionality to prevent spam

## Example Output

```
User: !unique stormshield
Bot: [Stormshield][Monarch][Defense: 136 - 519][Indestructible][Req lvl: 73][+3-371 Defense (+3.75 per Character Level)][25% Increased Chance of Blocking][35% Faster Block Rate][Damage Reduced by 35%][Cold Resist +60%][Lightning Resist +25%][+30 to Strength][Attacker Takes Lightning Damage of 10]
```

## Project Structure

```
├── items.py           # Web scraper and database creation
├── bot_init.py        # Twitch IRC connection setup
├── bot_run.py         # Main chat bot logic and command handler
└── d2items.db         # SQLite database (created with items.py)
```

## Development Notes

### Database Schema

**uniques table:**
- `search_string` - Item type for searching (e.g., "sword", "armor")
- `item_name` - Unique item name (normalized, no spaces)
- `item_text` - Formatted item statistics

**sets table:**
- `search_string` - Item type for searching
- `item_name` - Set item name (normalized)
- `set_name` - Name of the set group
- `item_text` - Formatted item statistics

### Known Limitations

- Web scraper currently targets diablo.gamepedia.com; breaks if site structure changes
- Some wiki pages have HTML formatting inconsistencies (manually corrected in code)
- Chat message length limits affect very long item descriptions

## Resources

- [Diablo Gamepedia](https://diablo.gamepedia.com) - Data source
- [Twitch IRC Documentation](https://dev.twitch.tv/docs/irc) - Bot protocol
- [Python sqlite3 Documentation](https://docs.python.org/3/library/sqlite3.html)
