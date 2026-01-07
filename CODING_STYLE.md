# Coding Style Guide

This document outlines the coding style standards used throughout the project to ensure consistency and maintainability.

## Session Key Naming Convention

All session keys use **snake_case** (lowercase with underscores):

### Standard Session Keys
- `logged_in` - User login status (boolean)
- `user_id` - User ID
- `user_email` - User email address
- `session_id` - Session identifier
- `saved_token` - Saved payment token
- `exp_month` - Card expiration month
- `exp_year` - Card expiration year
- `reference_id` - Payer authentication reference ID
- `ship_to_address` - Shipping address

### Examples
✅ **Correct:**
```python
session['logged_in'] = True
session['user_id'] = user_id
session['saved_token'] = token
session['reference_id'] = ref_id
```

❌ **Incorrect:**
```python
session['loggedin'] = True  # Should be 'logged_in'
session['userid'] = user_id  # Should be 'user_id'
session['savedtoken'] = token  # Should be 'saved_token'
session['referenceId'] = ref_id  # Should be 'reference_id'
session['shipToAddress'] = address  # Should be 'ship_to_address'
```

## Variable Naming

- Use **snake_case** for all variables and functions
- Use **UPPER_CASE** for constants
- Use descriptive names that indicate purpose

### Examples
```python
# Variables
saved_token = session.get('saved_token')
exp_month = request.form.get('exp_month')
reference_number = generate_reference_number()

# Functions
def get_session_value(key: str) -> Any:
def handle_payer_auth_enroll(...):
def extract_form_data() -> Dict[str, Any]:
```

## Error Handling

### Try-Except Blocks
- Always use try-except blocks for routes that interact with external services
- Provide user-friendly error messages
- Log errors appropriately (avoid print statements in production)

### Examples
```python
@views.route("/example", methods=["GET", "POST"])
def example():
    try:
        # Route logic here
        return render_template("example.html")
    except Exception as e:
        flash(f"Error: {str(e)}", category="error")
        return redirect(url_for('views.login'))
```

## Authentication

### Login Required Decorator
Use the `@login_required` decorator for protected routes:

```python
from views.cybersource_soap import login_required

@views.route("/protected")
@login_required
def protected_route():
    # Route logic here
    pass
```

### Manual Login Checks
If manual checking is needed, use consistent pattern:

```python
if not session.get('logged_in'):
    flash("Please log in first!", category="error")
    return redirect(url_for('views.login'))
```

## Type Hints

Use type hints for function parameters and return types:

```python
from typing import Optional, Dict, Any, Tuple

def process_payment(
    amount: str,
    currency: str,
    card_number: str
) -> Dict[str, Any]:
    """Process payment transaction."""
    pass
```

## Documentation

### Docstrings
All functions should have docstrings describing:
- Purpose of the function
- Parameters (Args)
- Return values (Returns)
- Exceptions (Raises) if applicable

### Examples
```python
def mask_card(card_number: str) -> str:
    """
    Mask credit card number for display/storage.
    Shows first 6 and last 4 digits, masks the rest.
    
    Args:
        card_number: Credit card number to mask
        
    Returns:
        Masked card number string (e.g., "123456xxxxxx7890")
    """
    pass
```

## Code Organization

### Imports
Order imports as follows:
1. Standard library imports
2. Third-party imports
3. Local application imports

```python
# Standard library
import datetime
from typing import Optional, Dict, Any
from functools import wraps

# Third-party
from flask import render_template, request, redirect, url_for, flash, session

# Local
from . import views
import config
import constants
from repository import TokenRepository, TransactionRepository
from utils import mask_card
```

### Function Organization
- Keep functions focused on a single responsibility
- Break down large functions into smaller, reusable functions
- Group related functions together

## Security Best Practices

### Sensitive Data
- Never log or print sensitive data (card numbers, passwords, tokens)
- Always mask card numbers before storage/display
- Use environment variables for secrets

### Examples
```python
# ✅ Correct - Mask card number
masked_card = mask_card(card_number)
print(f"Card: {masked_card}")  # Output: "123456xxxxxx7890"

# ❌ Incorrect - Don't log full card number
print(f"Card: {card_number}")  # Security risk!
```

## Database Access

### Repository Pattern
Always use repository classes instead of direct database access:

```python
# ✅ Correct
tokens = TokenRepository.get_tokens_by_user_id(user_id)
TransactionRepository.create_transaction(...)

# ❌ Incorrect - Direct SQL
cursor.execute("SELECT * FROM tokens WHERE user_id = %s", (user_id,))
```

## Consistency Checklist

When adding or modifying code, ensure:

- [ ] Session keys use snake_case
- [ ] Variables use snake_case
- [ ] Functions have type hints
- [ ] Functions have docstrings
- [ ] Error handling is in place
- [ ] Sensitive data is masked
- [ ] Repository pattern is used for database access
- [ ] Imports are properly organized
- [ ] No debug print statements in production code

## Migration Notes

If you encounter legacy code with old naming conventions:

1. **Session Keys**: Update to snake_case
   - `loggedin` → `logged_in`
   - `userid` → `user_id`
   - `sessionId` → `session_id`
   - `savedtoken` → `saved_token`
   - `expMonth` → `exp_month`
   - `expYear` → `exp_year`
   - `referenceId` → `reference_id`
   - `shipToAddress` → `ship_to_address`

2. **Use `get_session_value()` helper** for backward compatibility:
   ```python
   from views.cybersource_soap import get_session_value
   
   user_id = get_session_value('user_id')  # Handles both 'user_id' and 'userid'
   ```
