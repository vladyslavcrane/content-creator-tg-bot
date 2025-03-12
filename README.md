# Daily Movies Bot

A Telegram bot that posts daily movie recommendations to a specified channel or chat.

## Overview

Daily Movies Bot uses OpenAI's GPT models to generate engaging movie recommendations with details like plot summaries, interesting facts, and reasons to watch. The bot can be scheduled to post daily recommendations or can post on demand via commands.

## Features

- 🎬 Posts random movie recommendations
- 🤖 Uses OpenAI's API for content generation
- ⏰ Scheduled posting with customizable timing
- 🔐 Command access restricted to bot owner
- 📊 Logs responses for future reference

## Architecture

The project follows a modular architecture:

- **Main Module** (`main.py`): Entry point that initializes the bot, MongoDB, and scheduler
- **API Module** (`app/api.py`): Handles communication with OpenAI API
- **Handlers Module** (`app/handlers.py`): Contains Telegram command handlers
- **Config Module** (`app/config.py`): Manages application configuration
- **Scheduler Module** (`app/scheduler.py`): Sets up scheduled tasks

## Installation

### Prerequisites

- Python 3.9+
- Telegram Bot Token (from [@BotFather](https://t.me/BotFather))
- OpenAI API Key

### Setup

