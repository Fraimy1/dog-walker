# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A Telegram bot for logging dog walks with SQLite persistence. Users log walks via keyboard buttons, optionally add parameters (e.g., "Didn't poop", "Long walk") within a 5-minute window, and broadcast notifications to group members.

## Tech Stack

- **Python** with **AIogram** (Telegram bot framework)
- **SQLite** with **SQLAlchemy** ORM
- Docker containerization (handled separately by project owner)

## Project Structure

```
src/bot/       # Bot modules - each file handles specific functionality
data/database  # SQLite database storage
```

## Architecture

The bot uses a modular design where each source file in `src/bot/` is responsible for a single area of functionality. Key flows:

1. **Walk logging**: User presses main button → creates DB record with timestamp → starts 5-minute timer
2. **Parameter selection**: User selects optional parameters via keyboard buttons, or presses "Send", or timer expires → updates DB record
3. **Broadcast**: After parameters are finalized, notify all group members with walk details

## Development Commands

Once dependencies are set up:

```bash
# Install dependencies
uv pip install -r requirements.txt

# Run the bot
python -m src.bot.main  # or appropriate entry point
```

## Key Implementation Notes

- Bot token should be managed via environment variables
- Keyboard buttons use Telegram's ReplyKeyboardMarkup (buttons above keyboard)
- Database should track: username, timestamp, walk parameters, and walk history
