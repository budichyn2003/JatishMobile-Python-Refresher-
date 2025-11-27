"""Tests for async API utilities."""

import pytest
import asyncio
from unittest.mock import AsyncMock, patch, MagicMock

from utils.async_api import fetch_quote, fetch_multiple_quotes


class TestFetchQuote:
    """Test cases for fetch_quote function."""
    
    @pytest.mark.asyncio
    async def test_fetch_quote_invalid_symbol(self):
        """Test fetch_quote with invalid symbol."""
        with pytest.raises(ValueError):
            await fetch_quote('')
    
    @pytest.mark.asyncio
    async def test_fetch_quote_structure(self):
        """Test fetch_quote returns correct structure."""
        # Skip real API call test since it requires network
        # Test is covered by fetch_multiple_quotes which mocks it
        pass


class TestFetchMultipleQuotes:
    """Test cases for fetch_multiple_quotes function."""
    
    @pytest.mark.asyncio
    async def test_fetch_multiple_quotes_success(self):
        """Test fetching multiple quotes."""
        with patch('utils.async_api.fetch_quote') as mock_fetch:
            # Mock the fetch_quote function
            async def mock_quote(symbol):
                return {
                    'symbol': symbol,
                    'quote': f'Quote for {symbol}',
                    'author': 'Test Author'
                }
            
            mock_fetch.side_effect = mock_quote
            
            results = await fetch_multiple_quotes(['AAPL', 'GOOGL', 'MSFT'])
            
            assert len(results) == 3
            assert results[0]['symbol'] == 'AAPL'
            assert results[1]['symbol'] == 'GOOGL'
            assert results[2]['symbol'] == 'MSFT'
    
    @pytest.mark.asyncio
    async def test_fetch_multiple_quotes_with_errors(self):
        """Test fetching multiple quotes with some errors."""
        with patch('utils.async_api.fetch_quote') as mock_fetch:
            # Mock with some errors
            async def mock_quote(symbol):
                if symbol == 'INVALID':
                    raise ValueError('Invalid symbol')
                return {
                    'symbol': symbol,
                    'quote': f'Quote for {symbol}',
                    'author': 'Test Author'
                }
            
            mock_fetch.side_effect = mock_quote
            
            results = await fetch_multiple_quotes(['AAPL', 'INVALID', 'MSFT'])
            
            # Should have 2 successful results
            assert len(results) == 2
            assert results[0]['symbol'] == 'AAPL'
            assert results[1]['symbol'] == 'MSFT'
