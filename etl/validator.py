"""Validator module for banking transactions."""

import logging
import re
from datetime import datetime
from typing import Any

# Configure logging
logger = logging.getLogger(__name__)


# Custom Exceptions
class InvalidTransactionIDError(Exception):
    """Raised when transaction ID is invalid."""
    pass


class InvalidDateFormatError(Exception):
    """Raised when date format is invalid."""
    pass


class InvalidCurrencyError(Exception):
    """Raised when currency is invalid."""
    pass


class InvalidAmountError(Exception):
    """Raised when amount is invalid."""
    pass


VALID_CURRENCIES = {'IDR', 'USD', 'SGD'}
VALID_DIRECTIONS = {'DEBIT', 'CREDIT'}
VALID_ACCOUNT_TYPES = {'SAVINGS', 'CURRENT', 'CREDIT_CARD', 'LOAN'}
TRANSACTION_ID_PATTERN = r'^TXN\d{7}$'
ANOMALY_THRESHOLD = 10_000_000


def validate_transaction_id(transaction_id: str) -> bool:
    """
    Validate transaction ID format: TXN + 7 digits.
    
    Args:
        transaction_id: Transaction ID to validate
        
    Returns:
        True if valid
        
    Raises:
        InvalidTransactionIDError: If format is invalid
    """
    if not transaction_id or not isinstance(transaction_id, str):
        logger.error(f"Invalid transaction ID type: {type(transaction_id)}")
        raise InvalidTransactionIDError(
            f"Transaction ID must be string, got {type(transaction_id)}"
        )
    
    if not re.match(TRANSACTION_ID_PATTERN, transaction_id.strip()):
        logger.error(f"Transaction ID does not match pattern: {transaction_id}")
        raise InvalidTransactionIDError(
            f"Transaction ID must match pattern TXNxxxxxxx, got {transaction_id}"
        )
    
    return True


def validate_date(date_str: str) -> bool:
    """
    Validate date format: YYYY-MM-DD or DD/MM/YYYY.
    
    Args:
        date_str: Date string to validate
        
    Returns:
        True if valid
        
    Raises:
        InvalidDateFormatError: If format is invalid
    """
    if not date_str or not isinstance(date_str, str):
        logger.error(f"Invalid date type: {type(date_str)}")
        raise InvalidDateFormatError(
            f"Date must be string, got {type(date_str)}"
        )
    
    date_str = date_str.strip()
    
    # Try YYYY-MM-DD format
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        pass
    
    # Try DD/MM/YYYY format
    try:
        datetime.strptime(date_str, '%d/%m/%Y')
        return True
    except ValueError:
        pass
    
    logger.error(f"Invalid date format: {date_str}")
    raise InvalidDateFormatError(
        f"Date must be YYYY-MM-DD or DD/MM/YYYY, got {date_str}"
    )


def validate_amount(amount: Any) -> bool:
    """
    Validate amount.
    
    Args:
        amount: Amount to validate
        
    Returns:
        True if valid
        
    Raises:
        InvalidAmountError: If amount is invalid
    """
    if amount is None or (isinstance(amount, str) and not amount.strip()):
        logger.error("Amount cannot be empty")
        raise InvalidAmountError("Amount cannot be empty")
    
    try:
        amount_float = float(amount)
    except (ValueError, TypeError) as e:
        logger.error(f"Amount cannot be converted to float: {amount}")
        raise InvalidAmountError(f"Amount must be numeric, got {amount}") from e
    
    if amount_float < 0:
        logger.error(f"Amount cannot be negative: {amount_float}")
        raise InvalidAmountError(f"Amount cannot be negative: {amount_float}")
    
    return True


def validate_currency(currency: str) -> bool:
    """
    Validate currency.
    
    Args:
        currency: Currency code to validate
        
    Returns:
        True if valid
        
    Raises:
        InvalidCurrencyError: If currency is invalid
    """
    if not currency or not isinstance(currency, str):
        logger.error(f"Invalid currency type: {type(currency)}")
        raise InvalidCurrencyError(
            f"Currency must be string, got {type(currency)}"
        )
    
    currency_clean = currency.strip().upper()
    
    if currency_clean not in VALID_CURRENCIES:
        logger.error(f"Invalid currency code: {currency}")
        raise InvalidCurrencyError(
            f"Currency must be one of {VALID_CURRENCIES}, got {currency}"
        )
    
    return True


def validate_direction(direction: str) -> bool:
    """
    Validate transaction direction.
    
    Args:
        direction: Direction (DEBIT or CREDIT)
        
    Returns:
        True if valid
    """
    if direction and isinstance(direction, str):
        if direction.strip().upper() not in VALID_DIRECTIONS:
            logger.warning(f"Invalid direction: {direction}")
            return False
    return True


def validate_account_type(account_type: str) -> bool:
    """
    Validate account type.
    
    Args:
        account_type: Account type to validate
        
    Returns:
        True if valid
    """
    if account_type and isinstance(account_type, str):
        if account_type.strip().upper() not in VALID_ACCOUNT_TYPES:
            logger.warning(f"Invalid account type: {account_type}")
            return False
    return True


def check_amount_anomaly(amount: float) -> bool:
    """
    Check if amount is anomalously large.
    
    Args:
        amount: Amount to check
        
    Returns:
        True if amount exceeds threshold
    """
    return float(amount) > ANOMALY_THRESHOLD


def validate_transaction(transaction: dict[str, Any]) -> dict[str, Any]:
    """
    Validate transaction data.
    
    Args:
        transaction: Transaction dictionary to validate
        
    Returns:
        Updated transaction dict with validation flags
        
    Raises:
        InvalidTransactionIDError: If transaction ID is invalid
        InvalidDateFormatError: If date format is invalid
        InvalidAmountError: If amount is invalid
        InvalidCurrencyError: If currency is invalid
    """
    logger.debug(f"Validating transaction: {transaction.get('transaction_id')}")
    
    # Mandatory validations (raise exceptions)
    validate_transaction_id(transaction.get('transaction_id', ''))
    validate_date(transaction.get('transaction_date', ''))
    validate_amount(transaction.get('amount'))
    validate_currency(transaction.get('currency', ''))
    
    # Optional validations (log warnings)
    validate_direction(transaction.get('direction', ''))
    validate_account_type(transaction.get('account_type', ''))
    
    # Add validation flags
    transaction['amount_anomaly'] = check_amount_anomaly(
        transaction.get('amount', 0)
    )
    
    logger.debug(
        f"Transaction {transaction.get('transaction_id')} validation successful"
    )
    
    return transaction
