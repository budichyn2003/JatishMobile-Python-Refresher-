"""Pytest configuration file for test fixtures."""

import pytest
import tempfile
import csv
from pathlib import Path


@pytest.fixture
def temp_csv_file():
    """Create a temporary CSV file for testing."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, newline='') as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                'transaction_id', 'transaction_date', 'value_date', 'customer_id',
                'account_id', 'account_type', 'txn_type', 'channel', 'direction',
                'amount', 'currency', 'merchant_category', 'region', 'risk_score',
                'is_fraud_suspected'
            ]
        )
        writer.writeheader()
        writer.writerow({
            'transaction_id': 'TXN0000001',
            'transaction_date': '2024-02-21',
            'value_date': '2024-02-22',
            'customer_id': 'CUST00001',
            'account_id': 'ACC00001',
            'account_type': 'SAVINGS',
            'txn_type': 'WITHDRAWAL',
            'channel': 'ATM',
            'direction': 'DEBIT',
            'amount': '5000.50',
            'currency': 'IDR',
            'merchant_category': 'ATM',
            'region': 'JKT',
            'risk_score': '0.1',
            'is_fraud_suspected': '0'
        })
        temp_path = f.name
    
    yield temp_path
    
    # Cleanup
    Path(temp_path).unlink(missing_ok=True)


@pytest.fixture
def valid_transaction():
    """Create a valid transaction for testing."""
    return {
        'transaction_id': 'TXN0000001',
        'transaction_date': '2024-02-21',
        'customer_id': 'CUST00001',
        'account_id': 'ACC00001',
        'amount': '5000.50',
        'currency': 'IDR',
        'direction': 'DEBIT',
        'account_type': 'SAVINGS'
    }


@pytest.fixture
def invalid_transaction_id():
    """Create a transaction with invalid ID."""
    return {
        'transaction_id': 'INVALID123',
        'transaction_date': '2024-02-21',
        'customer_id': 'CUST00001',
        'account_id': 'ACC00001',
        'amount': '5000.50',
        'currency': 'IDR'
    }


@pytest.fixture
def invalid_currency_transaction():
    """Create a transaction with invalid currency."""
    return {
        'transaction_id': 'TXN0000001',
        'transaction_date': '2024-02-21',
        'customer_id': 'CUST00001',
        'account_id': 'ACC00001',
        'amount': '5000.50',
        'currency': 'EUR'  # Invalid currency
    }


@pytest.fixture
def negative_amount_transaction():
    """Create a transaction with negative amount."""
    return {
        'transaction_id': 'TXN0000001',
        'transaction_date': '2024-02-21',
        'customer_id': 'CUST00001',
        'account_id': 'ACC00001',
        'amount': '-5000.50',  # Negative
        'currency': 'IDR'
    }


@pytest.fixture
def large_amount_transaction():
    """Create a transaction with large amount (anomaly)."""
    return {
        'transaction_id': 'TXN0000001',
        'transaction_date': '2024-02-21',
        'customer_id': 'CUST00001',
        'account_id': 'ACC00001',
        'amount': '15000000.00',  # > 10,000,000
        'currency': 'IDR'
    }
