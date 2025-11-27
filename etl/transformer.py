"""Transformer module for banking transactions."""

import logging
import math
from datetime import datetime, date
from typing import Any, Optional

# Configure logging
logger = logging.getLogger(__name__)


def convert_date_to_date_object(date_str: str) -> Optional[date]:
    """
    Convert date string to datetime.date object.
    
    Args:
        date_str: Date string in YYYY-MM-DD format
        
    Returns:
        datetime.date object or None if invalid
    """
    if not date_str:
        return None
    
    try:
        return datetime.strptime(str(date_str).strip(), '%Y-%m-%d').date()
    except (ValueError, TypeError):
        logger.warning(f"Could not convert to date object: {date_str}")
        return None


def convert_amount_to_float(amount: Any) -> Optional[float]:
    """
    Convert amount to float.
    
    Args:
        amount: Amount value
        
    Returns:
        Float value or None if invalid
    """
    if amount is None:
        return None
    
    try:
        return float(amount)
    except (ValueError, TypeError):
        logger.warning(f"Could not convert amount to float: {amount}")
        return None


def convert_risk_score_to_float(risk_score: Any) -> Optional[float]:
    """
    Convert risk score to float.
    
    Args:
        risk_score: Risk score value
        
    Returns:
        Float value or None if invalid
    """
    if risk_score is None or (isinstance(risk_score, str) and not risk_score.strip()):
        return None
    
    try:
        return float(risk_score)
    except (ValueError, TypeError):
        logger.warning(f"Could not convert risk score to float: {risk_score}")
        return None


def is_large_transaction(amount: Optional[float]) -> bool:
    """
    Check if transaction amount is large (> 5,000,000).
    
    Args:
        amount: Transaction amount
        
    Returns:
        True if amount > 5,000,000
    """
    if amount is None:
        return False
    
    return amount > 5_000_000


def is_crossborder_transaction(currency: str) -> bool:
    """
    Check if transaction is cross-border (currency != IDR).
    
    Args:
        currency: Currency code
        
    Returns:
        True if currency is not IDR
    """
    if not currency:
        return False
    
    return str(currency).strip().upper() != 'IDR'


def get_transaction_day(date_obj: Optional[date]) -> Optional[str]:
    """
    Get day name from date object.
    
    Args:
        date_obj: datetime.date object
        
    Returns:
        Day name (Monday, Tuesday, etc.) or None
    """
    if not date_obj:
        return None
    
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    return days[date_obj.weekday()]


def calculate_amount_log(amount: Optional[float]) -> Optional[float]:
    """
    Calculate natural log of amount (only if amount > 0).
    
    Args:
        amount: Transaction amount
        
    Returns:
        log(amount) or None if amount <= 0
    """
    if amount is None or amount <= 0:
        return None
    
    try:
        return math.log(amount)
    except (ValueError, TypeError):
        logger.warning(f"Could not calculate log for amount: {amount}")
        return None


def transform_transaction(transaction: dict[str, Any]) -> dict[str, Any]:
    """
    Transform transaction data with type conversions and derived features.
    
    Args:
        transaction: Cleaned transaction dictionary
        
    Returns:
        Transformed transaction dictionary with new features
    """
    logger.debug(f"Transforming transaction: {transaction.get('transaction_id')}")
    
    transformed = transaction.copy()
    
    # Type conversions
    transaction_date = transformed.get('transaction_date')
    transformed['transaction_date'] = convert_date_to_date_object(transaction_date)
    
    amount = transformed.get('amount')
    transformed['amount'] = convert_amount_to_float(amount)
    
    risk_score = transformed.get('risk_score')
    transformed['risk_score'] = convert_risk_score_to_float(risk_score)
    
    # Derived features
    transformed['is_large_transaction'] = is_large_transaction(transformed['amount'])
    transformed['is_crossborder'] = is_crossborder_transaction(
        transformed.get('currency', '')
    )
    transformed['transaction_day'] = get_transaction_day(transformed['transaction_date'])
    transformed['amount_log'] = calculate_amount_log(transformed['amount'])
    
    logger.debug(
        f"Transformation complete for {transaction.get('transaction_id')} - "
        f"Features: large={transformed['is_large_transaction']}, "
        f"crossborder={transformed['is_crossborder']}, "
        f"day={transformed['transaction_day']}"
    )
    
    return transformed
