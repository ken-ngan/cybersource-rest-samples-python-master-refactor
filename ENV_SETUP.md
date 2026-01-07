# Environment Variables Setup Guide

This project uses environment variables for all sensitive configuration. This ensures that secrets are never committed to version control.

## Quick Start

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and fill in your actual credentials.

3. The `.env` file is already in `.gitignore` and will not be committed.

## Required Environment Variables

### Flask Configuration

- `FLASK_SECRET_KEY`: Secret key for Flask sessions (generate a strong random string)
- `FLASK_DEBUG`: Set to `False` in production, `True` for development
- `FLASK_PORT`: Port number (default: 3000)
- `FLASK_HOST`: Host address (default: 127.0.0.1)
- `BASE_URL`: Base URL for your application (optional, see URL switcher below)
- `URL_MODE`: Convenient switcher - set to `"localhost"` or `"ngrok"` (default: `"localhost"`)

### URL Switcher

For easy switching between localhost and ngrok:

**Option 1: Use URL_MODE (Recommended)**
```bash
# For localhost
URL_MODE=localhost

# For ngrok
URL_MODE=ngrok
```

**Option 2: Set BASE_URL directly**
```bash
BASE_URL=https://127.0.0.1:3000
# or
BASE_URL=https://swampier-melida-unsqueamishly.ngrok-free.dev
```

If `BASE_URL` is set, it takes precedence over `URL_MODE`. See `URL_SWITCHER.md` for more details.

### CyberSource Configuration

- `MERCHANT_ID`: Your CyberSource merchant ID
- `ENVIRONMENT`: Either `PROD` or `CAS` (sandbox)

### Merchant-Specific Configuration

For each merchant ID and environment combination, you need to set variables in the format:
`{MERCHANT_ID}_{ENVIRONMENT}_{CONFIG_KEY}`

Example for merchant `gphktoken` in `PROD`:
- `gphktoken_PROD_MERCHANT_KEY_ID`
- `gphktoken_PROD_MERCHANT_SECRET_KEY`
- `gphktoken_PROD_SA_PROFILE_ID`
- `gphktoken_PROD_SA_ACCESS_KEY`
- `gphktoken_PROD_SA_SECRET_KEY`
- `gphktoken_PROD_SOP_PROFILE_ID`
- `gphktoken_PROD_SOP_ACCESS_KEY`
- `gphktoken_PROD_SOP_SECRET_KEY`
- `gphktoken_PROD_SOAP_P12_FILE`
- `gphktoken_PROD_SOAP_P12_PASSWORD`

### Supabase Configuration

- `SUPABASE_URL`: Your Supabase project URL
- `SUPABASE_KEY`: Your Supabase service role key

### MPGS Configuration (Optional)

- `MPGS_MERCHANT_ID`
- `MPGS_API_PASSWORD`
- `MPGS_BASE_URL`
- `MPGS_API_VERSION`

### AFS SOAP Configuration (Optional)

- `AFS_SOAP_USERNAME`
- `AFS_SOAP_P12_FILE`
- `AFS_SOAP_P12_PASSWORD`
- `AFS_SOAP_WSDL`

## Generating a Secure Flask Secret Key

You can generate a secure secret key using Python:

```python
import secrets
print(secrets.token_hex(32))
```

Or using OpenSSL:

```bash
openssl rand -hex 32
```

## Security Best Practices

1. **Never commit `.env` files** - They are already in `.gitignore`
2. **Use different credentials for development and production**
3. **Rotate secrets regularly**
4. **Use environment-specific `.env` files** (e.g., `.env.development`, `.env.production`)
5. **Restrict access to production environment variables**
6. **Use secret management services** (AWS Secrets Manager, HashiCorp Vault, etc.) in production

## Migration from Hardcoded Values

If you're migrating from the old hardcoded configuration:

1. Extract all hardcoded values from `config.py` (if any remain)
2. Add them to your `.env` file using the naming convention above
3. Restart your application
4. Verify that all functionality works correctly

## Troubleshooting

If you see configuration errors:

1. Check that all required environment variables are set
2. Verify the variable names match the expected format
3. Ensure there are no typos in variable names
4. Check that `.env` file is in the project root directory
5. Restart your application after changing `.env` file
