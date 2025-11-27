"""Tests for transaction transformer module."""

import pytest
import math
from datetime import date, datetime

from etl.transformer import (
    convert_date_to_date_object,
    convert_amount_to_float,
    convert_risk_score_to_float,
    is_large_transaction,
    is_crossborder_transaction,
    get_transaction_day,
    calculate_amount_log,
    transform_transaction
)


class TestConvertDateToDateObject:
    """Test cases for date conversion."""
    
    def test_convert_valid_date(self):
        """Test converting valid date."""
        result = convert_date_to_date_object('2024-02-21')
        assert isinstance(result, date)
        assert result == date(2024, 2, 21)
    
    def test_convert_invalid_date(self):
        """Test converting invalid date."""
        result = convert_date_to_date_object('invalid')
        assert result is None
    
    def test_convert_empty_date(self):
        """Test converting empty date."""
        result = convert_date_to_date_object('')
        assert result is None


class TestConvertAmountToFloat:
    """Test cases for amount conversion."""
    
    def test_convert_valid_amount_string(self):
        """Test converting valid amount string."""
        result = convert_amount_to_float('5000.50')
        assert isinstance(result, float)
        assert result == 5000.50
    
    def test_convert_numeric_amount(self):
        """Test converting numeric amount."""
        result = convert_amount_to_float(5000)
        assert result == 5000.0
    
    def test_convert_invalid_amount(self):
        """Test converting invalid amount."""
        result = convert_amount_to_float('abc')
        assert result is None
    
    def test_convert_none_amount(self):
        """Test converting None amount."""
        result = convert_amount_to_float(None)
        assert result is None


class TestConvertRiskScoreToFloat:
    """Test cases for risk score conversion."""
    
    def test_convert_valid_risk_score(self):
        """Test converting valid risk score."""
        result = convert_risk_score_to_float('0.5')
        assert isinstance(result, float)
        assert result == 0.5
    
    def test_convert_numeric_risk_score(self):
        """Test converting numeric risk score."""
        result = convert_risk_score_to_float(0.5)
        assert result == 0.5
    
    def test_convert_invalid_risk_score(self):
        """Test converting invalid risk score."""
        result = convert_risk_score_to_float('abc')
        assert result is None
    
    def test_convert_empty_risk_score(self):
        """Test converting empty risk score."""
        result = convert_risk_score_to_float('')
        assert result is None


class TestIsLargeTransaction:
    """Test cases for large transaction detection."""
    
    def test_large_transaction_above_threshold(self):
        """Test transaction above threshold."""
        assert is_large_transaction(6_000_000) is True
    
    def test_large_transaction_equal_threshold(self):
        """Test transaction equal to threshold."""
        assert is_large_transaction(5_000_000) is False
    
    def test_large_transaction_below_threshold(self):
        """Test transaction below threshold."""
        assert is_large_transaction(4_999_999) is False
    
    def test_large_transaction_none(self):
        """Test None amount."""
        assert is_large_transaction(None) is False


class TestIsCrossborderTransaction:
    """Test cases for crossborder detection."""
    
    def test_crossborder_usd(self):
        """Test USD transaction is crossborder."""
        assert is_crossborder_transaction('USD') is True
    
    def test_crossborder_sgd(self):
        """Test SGD transaction is crossborder."""
        assert is_crossborder_transaction('SGD') is True
    
    def test_not_crossborder_idr(self):
        """Test IDR transaction is not crossborder."""
        assert is_crossborder_transaction('IDR') is False
    
    def test_crossborder_lowercase(self):
        """Test lowercase currency handling."""
        assert is_crossborder_transaction('usd') is True
    
    def test_crossborder_empty(self):
        """Test empty currency."""
        assert is_crossborder_transaction('') is False


class TestGetTransactionDay:
    """Test cases for transaction day extraction."""
    
    def test_get_transaction_day_wednesday(self):
        """Test getting day for Wednesday."""
        d = date(2024, 2, 21)  # Wednesday
        assert get_transaction_day(d) == 'Wednesday'
    
    def test_get_transaction_day_monday(self):
        """Test getting day for Monday."""
        d = date(2024, 2, 19)  # Monday
        assert get_transaction_day(d) == 'Monday'
    
    def test_get_transaction_day_sunday(self):
        """Test getting day for Sunday."""
        d = date(2024, 2, 25)  # Sunday
        assert get_transaction_day(d) == 'Sunday'
    
    def test_get_transaction_day_none(self):
        """Test None date."""
        assert get_transaction_day(None) is None


class TestCalculateAmountLog:
    """Test cases for amount log calculation."""
    
    def test_calculate_log_positive_amount(self):
        """Test calculating log of positive amount."""
        result = calculate_amount_log(100)
        expected = math.log(100)
        assert abs(result - expected) < 0.0001
    
    def test_calculate_log_one(self):
        """Test calculating log of 1."""
        result = calculate_amount_log(1)
        assert result == 0.0
    
    def test_calculate_log_zero(self):
        """Test calculating log of 0."""
        result = calculate_amount_log(0)
        assert result is None
    
    def test_calculate_log_negative(self):
        """Test calculating log of negative number."""
        result = calculate_amount_log(-100)
        assert result is None
    
    def test_calculate_log_none(self):
        """Test calculating log of None."""
        result = calculate_amount_log(None)
        assert result is None


class TestTransformTransaction:
    """Test cases for full transaction transformation."""
    
    def test_transform_valid_transaction(self, valid_transaction):
        """Test transforming valid transaction."""
        transformed = transform_transaction(valid_transaction)
        
        assert isinstance(transformed['transaction_date'], date)
        assert isinstance(transformed['amount'], float)
        assert isinstance(transformed['is_large_transaction'], bool)
        assert isinstance(transformed['is_crossborder'], bool)
        assert isinstance(transformed['transaction_day'], str)
    
    def test_transform_date_conversion(self, valid_transaction):
        """Test date type conversion."""
        transformed = transform_transaction(valid_transaction)
        
        assert transformed['transaction_date'] == date(2024, 2, 21)
    
    def test_transform_amount_conversion(self, valid_transaction):
        """Test amount type conversion."""
        transformed = transform_transaction(valid_transaction)
        
        assert transformed['amount'] == 5000.50
    
    def test_transform_large_transaction_flag(self, large_amount_transaction):
        """Test large transaction flag."""
        transformed = transform_transaction(large_amount_transaction)
        
        assert transformed['is_large_transaction'] is True
    
    def test_transform_crossborder_flag_idr(self, valid_transaction):
        """Test crossborder flag for IDR."""
        transformed = transform_transaction(valid_transaction)
        
        assert transformed['is_crossborder'] is False
    
    def test_transform_crossborder_flag_usd(self):
        """Test crossborder flag for USD."""
        transaction = {
            'transaction_date': '2024-02-21',
            'amount': '5000.50',
            'currency': 'USD'
        }
        transformed = transform_transaction(transaction)
        
        assert transformed['is_crossborder'] is True
    
    def test_transform_amount_log(self, valid_transaction):
        """Test amount log calculation."""
        transformed = transform_transaction(valid_transaction)
        
        assert isinstance(transformed['amount_log'], float)
        assert transformed['amount_log'] > 0
    
    def test_transform_transaction_day(self, valid_transaction):
        """Test transaction day extraction."""
        transformed = transform_transaction(valid_transaction)
        
        assert transformed['transaction_day'] == 'Wednesday'
