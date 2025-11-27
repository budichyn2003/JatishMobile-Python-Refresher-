"""Tests for transaction cleaner module."""

import pytest
from datetime import date

from etl.cleaner import (
    trim_whitespace,
    normalize_date,
    normalize_currency,
    clean_numeric,
    clean_merchant_category,
    clean_transaction
)


class TestTrimWhitespace:
    """Test cases for whitespace trimming."""
    
    def test_trim_leading_whitespace(self):
        """Test trimming leading whitespace."""
        assert trim_whitespace('  hello') == 'hello'
    
    def test_trim_trailing_whitespace(self):
        """Test trimming trailing whitespace."""
        assert trim_whitespace('hello  ') == 'hello'
    
    def test_trim_both_sides(self):
        """Test trimming both sides."""
        assert trim_whitespace('  hello  ') == 'hello'
    
    def test_no_whitespace(self):
        """Test string without whitespace."""
        assert trim_whitespace('hello') == 'hello'
    
    def test_trim_non_string(self):
        """Test trimming non-string values."""
        assert trim_whitespace(123) == 123
        assert trim_whitespace(None) is None


class TestNormalizeDate:
    """Test cases for date normalization."""
    
    def test_normalize_iso_format(self):
        """Test normalizing YYYY-MM-DD format."""
        assert normalize_date('2024-02-21') == '2024-02-21'
    
    def test_normalize_ddmmyyyy_format(self):
        """Test normalizing DD/MM/YYYY format."""
        assert normalize_date('21/02/2024') == '2024-02-21'
    
    def test_normalize_empty_date(self):
        """Test normalizing empty date."""
        assert normalize_date('') is None
        assert normalize_date(None) is None
    
    def test_normalize_invalid_date(self):
        """Test normalizing invalid date."""
        assert normalize_date('invalid') is None


class TestNormalizeCurrency:
    """Test cases for currency normalization."""
    
    def test_normalize_uppercase(self):
        """Test normalizing uppercase currency."""
        assert normalize_currency('IDR') == 'IDR'
    
    def test_normalize_lowercase(self):
        """Test normalizing lowercase currency."""
        assert normalize_currency('idr') == 'IDR'
    
    def test_normalize_mixed_case(self):
        """Test normalizing mixed case currency."""
        assert normalize_currency('IdR') == 'IDR'
    
    def test_invalid_currency_returns_none(self):
        """Test invalid currency returns None."""
        assert normalize_currency('EUR') is None
    
    def test_empty_currency_returns_none(self):
        """Test empty currency returns None."""
        assert normalize_currency('') is None


class TestCleanNumeric:
    """Test cases for numeric value cleaning."""
    
    def test_clean_valid_numeric_string(self):
        """Test cleaning valid numeric string."""
        assert clean_numeric('5000.50') == 5000.50
    
    def test_clean_numeric_value(self):
        """Test cleaning numeric value."""
        assert clean_numeric(5000) == 5000.0
    
    def test_clean_empty_numeric(self):
        """Test cleaning empty numeric."""
        assert clean_numeric('') is None
        assert clean_numeric(None) is None
    
    def test_clean_invalid_numeric(self):
        """Test cleaning invalid numeric."""
        assert clean_numeric('abc') is None


class TestCleanMerchantCategory:
    """Test cases for merchant category cleaning."""
    
    def test_clean_valid_category(self):
        """Test cleaning valid category."""
        assert clean_merchant_category('GROCERY') == 'GROCERY'
    
    def test_clean_empty_category(self):
        """Test cleaning empty category defaults to Unknown."""
        assert clean_merchant_category('') == 'Unknown'
        assert clean_merchant_category(None) == 'Unknown'
    
    def test_clean_whitespace_category(self):
        """Test cleaning whitespace-only category."""
        assert clean_merchant_category('   ') == 'Unknown'
    
    def test_clean_category_with_whitespace(self):
        """Test cleaning category with surrounding whitespace."""
        assert clean_merchant_category('  GROCERY  ') == 'GROCERY'


class TestCleanTransaction:
    """Test cases for full transaction cleaning."""
    
    def test_clean_valid_transaction(self, valid_transaction):
        """Test cleaning valid transaction."""
        cleaned = clean_transaction(valid_transaction)
        
        assert isinstance(cleaned, dict)
        assert cleaned['transaction_id'] == 'TXN0000001'
        assert cleaned['currency'] == 'IDR'
        assert cleaned['direction'] == 'DEBIT'
    
    def test_clean_whitespace_in_fields(self):
        """Test cleaning whitespace in fields."""
        transaction = {
            'transaction_id': '  TXN0000001  ',
            'customer_id': '  CUST00001  ',
            'merchant_category': '  GROCERY  '
        }
        
        cleaned = clean_transaction(transaction)
        
        assert cleaned['transaction_id'] == 'TXN0000001'
        assert cleaned['customer_id'] == 'CUST00001'
        assert cleaned['merchant_category'] == 'GROCERY'
    
    def test_clean_date_normalization(self):
        """Test date normalization in cleaning."""
        transaction = {
            'transaction_date': '21/02/2024'
        }
        
        cleaned = clean_transaction(transaction)
        
        assert cleaned['transaction_date'] == '2024-02-21'
    
    def test_clean_missing_merchant_category(self):
        """Test cleaning transaction with missing merchant category."""
        transaction = {
            'merchant_category': ''
        }
        
        cleaned = clean_transaction(transaction)
        
        assert cleaned['merchant_category'] == 'Unknown'
    
    def test_clean_currency_normalization(self):
        """Test currency normalization."""
        transaction = {
            'currency': 'idr'
        }
        
        cleaned = clean_transaction(transaction)
        
        assert cleaned['currency'] == 'IDR'
    
    def test_clean_invalid_currency_to_none(self):
        """Test invalid currency becomes None."""
        transaction = {
            'currency': 'EUR'
        }
        
        cleaned = clean_transaction(transaction)
        
        assert cleaned['currency'] is None
