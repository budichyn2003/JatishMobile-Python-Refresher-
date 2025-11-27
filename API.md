# 📡 Async API Documentation

Dokumentasi lengkap untuk modul async API utilities dalam Banking ETL Assessment.

## Overview

Modul `utils/async_api.py` menyediakan:
- Async HTTP client untuk fetch data dari external API
- Retry decorator dengan exponential backoff
- Concurrent fetching untuk multiple requests
- Error handling dan timeout management

## Instalasi Dependencies

```bash
pip install aiohttp asyncio
```

## Quick Start

### Fetch Single Quote

```python
import asyncio
from utils.async_api import fetch_quote

async def main():
    # Fetch random quote
    result = await fetch_quote('AAPL')
    print(result)
    # Output: {'symbol': 'AAPL', 'quote': '...', 'author': '...'}

# Run async function
asyncio.run(main())
```

### Fetch Multiple Quotes

```python
import asyncio
from utils.async_api import fetch_multiple_quotes

async def main():
    symbols = ['AAPL', 'GOOGL', 'MSFT']
    results = await fetch_multiple_quotes(symbols)
    
    for quote in results:
        print(f"{quote['symbol']}: {quote['quote']}")

asyncio.run(main())
```

## API Reference

### `fetch_quote(symbol: str) -> dict[str, Any]`

Fetch random quote data for a given symbol.

**Parameters:**
- `symbol` (str): Stock/crypto symbol (e.g., 'AAPL', 'BTC')

**Returns:**
- `dict` with keys:
  - `symbol`: Input symbol
  - `quote`: Quote text
  - `author`: Author of quote

**Raises:**
- `ValueError`: If symbol is empty or invalid
- `asyncio.TimeoutError`: If request exceeds timeout (10 seconds)
- `aiohttp.ClientError`: If network request fails

**Example:**
```python
import asyncio
from utils.async_api import fetch_quote

async def main():
    try:
        result = await fetch_quote('AAPL')
        print(f"Quote from {result['author']}: {result['quote']}")
    except ValueError as e:
        print(f"Invalid symbol: {e}")
    except asyncio.TimeoutError:
        print("Request timed out")

asyncio.run(main())
```

### `fetch_multiple_quotes(symbols: list[str]) -> list[dict[str, Any]]`

Fetch quotes for multiple symbols concurrently.

**Parameters:**
- `symbols` (list[str]): List of symbols to fetch

**Returns:**
- `list` of dicts with same structure as `fetch_quote`
- Filters out failed requests automatically

**Example:**
```python
import asyncio
from utils.async_api import fetch_multiple_quotes

async def main():
    symbols = ['AAPL', 'GOOGL', 'MSFT', 'TSLA']
    results = await fetch_multiple_quotes(symbols)
    
    print(f"Successfully fetched {len(results)} quotes")
    for quote in results:
        print(f"- {quote['symbol']}: {quote['author']}")

asyncio.run(main())
```

### `@retry_on_failure(max_retries=3, timeout=10)`

Decorator untuk menambahkan retry logic ke async functions.

**Parameters:**
- `max_retries` (int): Maximum retry attempts (default: 3)
- `timeout` (float): Timeout per attempt in seconds (default: 10)

**Features:**
- Exponential backoff: 1 second delay between retries
- Timeout handling via asyncio.wait_for()
- Automatic logging of retries and failures
- Works with any async function

**Example:**
```python
import asyncio
from utils.async_api import retry_on_failure

@retry_on_failure(max_retries=5, timeout=20)
async def fetch_data_with_retry(url: str):
    # Your async code here
    pass

# Use like normal async function
result = await fetch_data_with_retry('https://api.example.com/data')
```

## Retry Logic Explanation

### How Retry Works

```
Attempt 1: Try operation
  ├─ Success? → Return result
  └─ Failure? → Wait 1s, go to Attempt 2

Attempt 2: Try operation
  ├─ Success? → Return result
  └─ Failure? → Wait 1s, go to Attempt 3

Attempt 3: Try operation
  ├─ Success? → Return result
  └─ Failure? → Raise exception
```

### Timeout Behavior

- Each attempt has 10-second timeout
- If exceeds timeout, retry triggered
- After max retries, TimeoutError raised
- Network errors logged but don't count as failures for retry

### Logging

Retry operations are logged:
```
INFO: Fetching quote for symbol AAPL
DEBUG: Attempt 1 of 3 for fetch_quote
INFO: Successfully fetched quote (attempt 1)
```

## Error Handling

### Common Errors

**ValueError: Empty or invalid symbol**
```python
try:
    result = await fetch_quote('')
except ValueError as e:
    print(f"Error: {e}")  # Error: Symbol cannot be empty
```

**asyncio.TimeoutError**
```python
try:
    result = await fetch_quote('AAPL')
except asyncio.TimeoutError:
    print("Request took too long (>10 seconds)")
```

**aiohttp.ClientError**
```python
try:
    result = await fetch_quote('AAPL')
except aiohttp.ClientError as e:
    print(f"Network error: {e}")
```

### Best Practices

1. **Always use try-except blocks**
   ```python
   try:
       result = await fetch_quote(symbol)
   except Exception as e:
       logger.error(f"Failed to fetch quote: {e}")
   ```

2. **Handle concurrent failures gracefully**
   ```python
   results = await fetch_multiple_quotes(symbols)
   if len(results) < len(symbols):
       logger.warning(f"Only {len(results)}/{len(symbols)} quotes fetched")
   ```

3. **Set appropriate timeouts**
   ```python
   # For quick operations
   @retry_on_failure(timeout=5)
   
   # For slow operations
   @retry_on_failure(timeout=30)
   ```

## Integration with ETL Pipeline

### Using Async API in ETL

```python
import asyncio
from etl import load_csv, transform_transaction
from utils.async_api import fetch_multiple_quotes

async def enrich_transactions_with_quotes():
    # Load transactions
    transactions = load_csv('data/banking_transactions.csv')
    
    # Extract unique merchants (or symbols)
    symbols = list(set(t.get('merchant_category', 'UNKNOWN') 
                       for t in transactions[:10]))
    
    # Fetch quotes
    quotes = await fetch_multiple_quotes(symbols)
    
    # Create lookup
    quote_lookup = {q['symbol']: q['quote'] for q in quotes}
    
    # Enrich transactions
    enriched = []
    for txn in transactions[:5]:
        transformed = transform_transaction(txn)
        transformed['enriched_quote'] = quote_lookup.get(
            txn.get('merchant_category', 'UNKNOWN'),
            'No quote available'
        )
        enriched.append(transformed)
    
    return enriched

# Run
results = asyncio.run(enrich_transactions_with_quotes())
```

## Performance Optimization

### Concurrent Requests

Multiple requests run in parallel:
```python
# These 3 requests run simultaneously, not sequentially
results = await fetch_multiple_quotes(['AAPL', 'GOOGL', 'MSFT'])
```

**Performance**: ~10 seconds for 3 requests (vs ~30 seconds sequential)

### Batch Processing

```python
async def fetch_in_batches(symbols, batch_size=10):
    results = []
    
    for i in range(0, len(symbols), batch_size):
        batch = symbols[i:i+batch_size]
        batch_results = await fetch_multiple_quotes(batch)
        results.extend(batch_results)
    
    return results

# Process 1000 symbols in batches of 10
all_results = asyncio.run(fetch_in_batches(large_symbol_list))
```

## Testing

### Unit Tests

Tests are in `tests/test_utils.py`:

```bash
pytest tests/test_utils.py -v
```

### Test Coverage

- ✅ Valid fetch_quote
- ✅ Invalid symbol handling
- ✅ Concurrent fetching
- ✅ Error filtering in concurrent fetches
- ✅ Timeout handling
- ✅ Retry logic

### Manual Testing

```python
import asyncio
from utils.async_api import fetch_quote, fetch_multiple_quotes

# Test single fetch
print("Testing single fetch...")
result = asyncio.run(fetch_quote('AAPL'))
print(f"✓ Fetched: {result['symbol']}")

# Test multiple fetch
print("\nTesting multiple fetch...")
results = asyncio.run(fetch_multiple_quotes(['AAPL', 'GOOGL', 'MSFT']))
print(f"✓ Fetched {len(results)} quotes")
```

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'aiohttp'"

**Solution:**
```bash
pip install aiohttp
```

### Issue: "SSL error with aiohttp"

**Solution**: Use SSL context:
```python
import aiohttp
import ssl

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

async with aiohttp.ClientSession() as session:
    # Your code
    pass
```

### Issue: "TimeoutError every time"

**Solution**: Increase timeout:
```python
@retry_on_failure(timeout=30)  # Increase from 10 to 30 seconds
async def slow_operation():
    pass
```

### Issue: "Too many concurrent requests"

**Solution**: Reduce concurrency with semaphore:
```python
async def fetch_limited(symbols, max_concurrent=3):
    semaphore = asyncio.Semaphore(max_concurrent)
    
    async def limited_fetch(symbol):
        async with semaphore:
            return await fetch_quote(symbol)
    
    tasks = [limited_fetch(s) for s in symbols]
    return await asyncio.gather(*tasks, return_exceptions=True)
```

## Advanced Usage

### Custom Retry Decorator

```python
from functools import wraps
import asyncio

def custom_retry(max_retries=3, backoff=2):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            for attempt in range(1, max_retries + 1):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries:
                        raise
                    wait_time = backoff ** attempt
                    await asyncio.sleep(wait_time)
        return wrapper
    return decorator

@custom_retry(max_retries=5, backoff=2)
async def my_operation():
    pass
```

### Context Manager for Session

```python
from contextlib import asynccontextmanager
import aiohttp

@asynccontextmanager
async def managed_session():
    async with aiohttp.ClientSession() as session:
        yield session

async def main():
    async with managed_session() as session:
        # Use session
        pass

asyncio.run(main())
```

## API Endpoint Details

**Current Implementation**: Uses dummyjson.com/quotes/random

```
GET https://dummyjson.com/quotes/random

Response:
{
  "id": 1,
  "quote": "Life isn't about finding yourself...",
  "author": "George Bernard Shaw"
}
```

**Note**: Current implementation returns random quotes. For production, replace with your own API endpoint.

## Contributing

To contribute improvements to async_api.py:

1. Keep decorator reusable and generic
2. Add logging at DEBUG level for diagnostics
3. Update tests in test_utils.py
4. Document new parameters in docstrings
5. Test with concurrent operations

## References

- [asyncio documentation](https://docs.python.org/3/library/asyncio.html)
- [aiohttp documentation](https://docs.aiohttp.org/)
- [Python async/await guide](https://realpython.com/async-io-python/)

---

**Last Updated**: 2024
**Version**: 1.0
