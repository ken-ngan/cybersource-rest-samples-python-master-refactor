# URL Switcher Guide

This project includes a convenient switcher to toggle between localhost and ngrok URLs.

## Quick Switch

### Method 1: Environment Variable (Recommended)

Set the `URL_MODE` environment variable in your `.env` file:

**For localhost:**
```bash
URL_MODE=localhost
```

**For ngrok:**
```bash
URL_MODE=ngrok
```

### Method 2: Direct BASE_URL Override

You can also set `BASE_URL` directly to override the switcher:

```bash
BASE_URL=https://your-custom-url.com
```

## Default Behavior

- If `URL_MODE` is not set, defaults to `localhost`
- If `BASE_URL` is explicitly set, it takes precedence over `URL_MODE`

## URLs

- **Localhost**: `https://127.0.0.1:3000` (uses `LOCAL_HOST` and `PORT` from environment)
- **Ngrok**: `https://swampier-melida-unsqueamishly.ngrok-free.dev`

## Example .env Configuration

```bash
# Switch to ngrok
URL_MODE=ngrok

# Or switch to localhost
URL_MODE=localhost

# Or use custom URL
BASE_URL=https://my-custom-domain.com
```

## Updating Ngrok URL

If your ngrok URL changes, update it in:
- `config.py` - `NGROK_URL` constant
- `config_loader.py` - `ngrok_url` variable

## Usage in Code

Both `config.py` and `config_loader.py` support the switcher:

```python
# In config.py
import config
print(config.BASE_URL)  # Uses URL_MODE or BASE_URL from environment

# In config_loader.py
from config_loader import SecureConfig
config = SecureConfig()
print(config.BASE_URL)  # Uses URL_MODE or BASE_URL from environment
```
