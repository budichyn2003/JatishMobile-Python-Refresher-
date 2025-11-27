"""Cleaner module for banking transactions."""

import logging
from datetime import datetime
from typing import Any, Optional

# Configure logging
logger = logging.getLogger(__name__)


def trim_whitespace(value: Any) -> Any:
    """
    Trim whitespace from string values.
    
    Args:
        value: Value to trim
        
    Returns:
        Trimmed string or original value
    """
    if isinstance(value, str):
        return value.strip()
    return value


def normalize_date(date_str: str) -> Optional[str]:
    """
    Normalize date to YYYY-MM-DD format.
    
    Args:
        date_str: Date string in YYYY-MM-DD or DD/MM/YYYY format
        
    Returns:
        Normalized date string or None if invalid
    """
    if not date_str:
        return None
    
    date_str = str(date_str).strip()
    
    # Try YYYY-MM-DD format
    try:
        dt = datetime.strptime(date_str, '%Y-%m-%d')
        return dt.strftime('%Y-%m-%d')
    except ValueError:
        pass
    
    # Try DD/MM/YYYY format
    try:
        dt = datetime.strptime(date_str, '%d/%m/%Y')
        return dt.strftime('%Y-%m-%d')
    except ValueError:
        pass
    
    logger.warning(f"Could not normalize date: {date_str}")
    return None


def normalize_currency(currency: str) -> Optional[str]:
    """
    Normalize and validate currency.
    
    Args:
        currency: Currency code
        
    Returns:
        Normalized currency code or None if invalid
    """
    if not currency:
        return None
    
    valid_currencies = {'IDR', 'USD', 'SGD'}
    currency_clean = str(currency).strip().upper()
    
    if currency_clean not in valid_currencies:
        logger.warning(f"Invalid currency, setting to None: {currency}")
        return None
    
    return currency_clean


def clean_numeric(value: Any) -> Optional[float]:
    """
    Clean numeric values.
    
    Args:
        value: Value to clean
        
    Returns:
        Float value or None if invalid
    """
    if value is None or (isinstance(value, str) and not value.strip()):
        return None
    
    try:
        return float(value)
    except (ValueError, TypeError):
        logger.warning(f"Could not convert to numeric: {value}")
        return None


def clean_merchant_category(merchant_category: str) -> str:
    """
    Clean merchant category with simple imputation.
    
    Args:
        merchant_category: Merchant category value
        
    Returns:
        Cleaned merchant category (defaults to 'Unknown' if empty)
    """
    if not merchant_category or not str(merchant_category).strip():
        return "Unknown"
    
    return str(merchant_category).strip()


def clean_transaction(transaction: dict[str, Any]) -> dict[str, Any]:
    """
    Clean transaction data.
    
    Args:
        transaction: Raw transaction dictionary
        
    Returns:
        Cleaned transaction dictionary
    """
    logger.debug(f"Cleaning transaction: {transaction.get('transaction_id')}")
    
    cleaned = {}
    
    # Copy all fields and apply cleaning rules
    for key, value in transaction.items():
        if key in ['transaction_id', 'customer_id', 'account_id', 'channel', 
                   'region', 'txn_type']:
            # Trim whitespace for ID and text fields
            cleaned[key] = trim_whitespace(value)
        
        elif key in ['transaction_date', 'value_date']:
            # Normalize dates
            cleaned[key] = normalize_date(value)
        
        elif key == 'currency':
            # Normalize currency
            cleaned[key] = normalize_currency(value)
        
        elif key in ['amount', 'risk_score']:
            # Clean numeric values
            cleaned[key] = clean_numeric(value)
        
        elif key == 'merchant_category':
            # Impute missing merchant category
            cleaned[key] = clean_merchant_category(value)
        
        elif key in ['account_type', 'direction']:
            # Normalize to uppercase and trim
            if value:
                cleaned[key] = trim_whitespace(value).upper()
            else:
                cleaned[key] = value
        
        else:
            # Keep as is, but trim if string
            cleaned[key] = trim_whitespace(value) if isinstance(value, str) else value
    
    logger.debug(f"Cleaning complete for {transaction.get('transaction_id')}")
    
    return cleaned
