"""Tests for transaction validator module."""

import pytest
from datetime import datetime

from etl.validator import (
    validate_transaction_id,
    validate_date,
    validate_amount,
    validate_currency,
    validate_transaction,
    InvalidTransactionIDError,
    InvalidDateFormatError,
    InvalidCurrencyError,
    InvalidAmountError
)


class TestValidateTransactionID:
    """Test cases for transaction ID validation."""
    
    def test_valid_transaction_id(self):
        """Test valid transaction ID format."""
        assert validate_transaction_id('TXN0000001') is True
        assert validate_transaction_id('TXN1234567') is True
    
    def test_invalid_transaction_id_format(self):
        """Test invalid transaction ID format."""
        with pytest.raises(InvalidTransactionIDError):
            validate_transaction_id('INVALID001')
    
    def test_invalid_transaction_id_wrong_prefix(self):
        """Test transaction ID with wrong prefix."""
        with pytest.raises(InvalidTransactionIDError):
            validate_transaction_id('ABC0000001')
    
    def test_invalid_transaction_id_wrong_length(self):
        """Test transaction ID with wrong digit count."""
        with pytest.raises(InvalidTransactionIDError):
            validate_transaction_id('TXN000001')  # Only 6 digits
    
    def test_invalid_transaction_id_type(self):
        """Test transaction ID with wrong type."""
        with pytest.raises(InvalidTransactionIDError):
            validate_transaction_id(123456789)


class TestValidateDate:
    """Test cases for date validation."""
    
    def test_valid_date_iso_format(self):
        """Test valid date in YYYY-MM-DD format."""
        assert validate_date('2024-02-21') is True
        assert validate_date('2024-01-01') is True
    
    def test_valid_date_ddmmyyyy_format(self):
        """Test valid date in DD/MM/YYYY format."""
        assert validate_date('21/02/2024') is True
        assert validate_date('01/01/2024') is True
    
    def test_invalid_date_format(self):
        """Test invalid date format."""
        with pytest.raises(InvalidDateFormatError):
            validate_date('02-21-2024')
    
    def test_invalid_date_nonexistent(self):
        """Test invalid date (non-existent)."""
        with pytest.raises(InvalidDateFormatError):
            validate_date('2024-13-45')
    
    def test_empty_date(self):
        """Test empty date."""
        with pytest.raises(InvalidDateFormatError):
            validate_date('')


class TestValidateAmount:
    """Test cases for amount validation."""
    
    def test_valid_amount(self):
        """Test valid amount."""
        assert validate_amount('5000.50') is True
        assert validate_amount(5000.50) is True
        assert validate_amount('1000') is True
    
    def test_negative_amount(self):
        """Test negative amount."""
        with pytest.raises(InvalidAmountError):
            validate_amount('-5000.50')
    
    def test_zero_amount(self):
        """Test zero amount (should be valid)."""
        assert validate_amount('0') is True
        assert validate_amount(0) is True
    
    def test_empty_amount(self):
        """Test empty amount."""
        with pytest.raises(InvalidAmountError):
            validate_amount('')
        
        with pytest.raises(InvalidAmountError):
            validate_amount(None)
    
    def test_non_numeric_amount(self):
        """Test non-numeric amount."""
        with pytest.raises(InvalidAmountError):
            validate_amount('abc')


class TestValidateCurrency:
    """Test cases for currency validation."""
    
    def test_valid_currency_idr(self):
        """Test valid IDR currency."""
        assert validate_currency('IDR') is True
    
    def test_valid_currency_usd(self):
        """Test valid USD currency."""
        assert validate_currency('USD') is True
    
    def test_valid_currency_sgd(self):
        """Test valid SGD currency."""
        assert validate_currency('SGD') is True
    
    def test_invalid_currency(self):
        """Test invalid currency."""
        with pytest.raises(InvalidCurrencyError):
            validate_currency('EUR')
    
    def test_empty_currency(self):
        """Test empty currency."""
        with pytest.raises(InvalidCurrencyError):
            validate_currency('')
    
    def test_lowercase_currency(self):
        """Test lowercase currency (should be normalized)."""
        assert validate_currency('idr') is True


class TestValidateTransaction:
    """Test cases for full transaction validation."""
    
    def test_validate_valid_transaction(self, valid_transaction):
        """Test validating valid transaction."""
        result = validate_transaction(valid_transaction)
        
        assert result['transaction_id'] == 'TXN0000001'
        assert 'amount_anomaly' in result
        assert result['amount_anomaly'] is False
    
    def test_validate_invalid_transaction_id(self, invalid_transaction_id):
        """Test transaction with invalid ID."""
        with pytest.raises(InvalidTransactionIDError):
            validate_transaction(invalid_transaction_id)
    
    def test_validate_invalid_currency(self, invalid_currency_transaction):
        """Test transaction with invalid currency."""
        with pytest.raises(InvalidCurrencyError):
            validate_transaction(invalid_currency_transaction)
    
    def test_validate_negative_amount(self, negative_amount_transaction):
        """Test transaction with negative amount."""
        with pytest.raises(InvalidAmountError):
            validate_transaction(negative_amount_transaction)
    
    def test_amount_anomaly_flag(self, large_amount_transaction):
        """Test anomaly flag for large amount."""
        result = validate_transaction(large_amount_transaction)
        
        assert result['amount_anomaly'] is True
    
    def test_normal_amount_no_anomaly(self, valid_transaction):
        """Test normal amount has no anomaly flag."""
        result = validate_transaction(valid_transaction)
        
        assert result['amount_anomaly'] is False
