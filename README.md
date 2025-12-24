# Aiogram 3.x Telegram Bot Template

A production-ready Telegram bot template using **aiogram 3.x** with modern Python practices.

## Features

- **aiogram 3.x** - Modern async Telegram Bot framework
- **Structured logging** - Using structlog with JSON/console output
- **Configuration** - TOML config with Pydantic validation
- **Localization** - Fluent-based i18n support
- **Rate limiting** - Built-in throttling middleware
- **Type hints** - Full type annotations throughout
- **Docker support** - Ready for containerized deployment
- **Database templates** - Abstract repository pattern with SQLite example

## Project Structure

```
├── bot.py              # Entry point
├── config_reader.py    # Configuration handling
├── config.toml         # Configuration file
├── fluent_loader.py    # Localization loader
├── logs.py             # Logging configuration
├── filters/            # Custom filters
│   ├── chat_type.py
│   ├── find_usernames.py
│   ├── is_admin.py
│   ├── is_owner.py
│   └── member_can_restrict.py
├── handlers/           # Message handlers
│   ├── admin_actions.py
│   ├── group_events.py
│   └── personal_actions.py
├── keyboards/          # Inline keyboards
│   ├── confirm.py
│   └── pagination.py
├── middlewares/        # Middlewares
│   ├── localization.py
│   ├── throttling.py
│   └── weekend.py
├── db/                 # Database layer
│   ├── base.py
│   ├── memory.py
│   └── sqlite.py
└── l10n/               # Translations
    ├── en.ftl
    └── ru.ftl
```

## Quick Start

### 1. Clone and install dependencies

```bash
git clone <repository>
cd tgbotbase

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or: venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure the bot

Edit `config.toml`:

```toml
[bot]
token = "YOUR_BOT_TOKEN"
owners = [123456789]  # Your Telegram user ID
```

Or use environment variables:

```bash
cp .env.example .env
# Edit .env with your values
```

### 3. Run the bot

```bash
python bot.py
```

## Docker Deployment

```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `BOT_TOKEN` | Telegram bot token | Required |
| `BOT_OWNERS` | Comma-separated owner IDs | `[]` |
| `CONFIG_FILE_PATH` | Path to config file | `config.toml` |

### Config File (`config.toml`)

```toml
[bot]
token = ""
owners = []

[logs]
show_datetime = true
datetime_format = "%Y-%m-%d %H:%M:%S"
show_debug_logs = true
renderer = "console"  # or "json"

[localization]
default_locale = "en"
fallback_locale = "en"
```

## Adding New Features

### New Handler

```python
# handlers/my_feature.py
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router(name="my_feature")

@router.message(Command("mycommand"))
async def my_handler(message: Message) -> None:
    await message.answer("Hello!")
```

Register in `handlers/__init__.py`:

```python
from . import my_feature

def register_all_handlers(dp: Dispatcher) -> None:
    # ... existing routers ...
    dp.include_router(my_feature.router)
```

### New Filter

```python
# filters/my_filter.py
from aiogram.filters import BaseFilter
from aiogram.types import Message

class MyFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return True  # Your logic here
```

### New Middleware

```python
# middlewares/my_middleware.py
from aiogram import BaseMiddleware

class MyMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        # Before handler
        result = await handler(event, data)
        # After handler
        return result
```

## Localization

Add translations in `l10n/` directory using Fluent format:

```ftl
# l10n/en.ftl
greeting = Hello, { $name }!
```

Use in handlers:

```python
@router.message(Command("greet"))
async def greet(message: Message, l10n: FluentLocalization) -> None:
    text = l10n.format_value("greeting", {"name": message.from_user.first_name})
    await message.answer(text)
```

## Credits

- [aiogram](https://github.com/aiogram/aiogram) - Telegram Bot framework
- [@MasterGroosha](https://github.com/MasterGroosha) - Aiogram 3 tutorials

## License

MIT License (hell yeah!)
