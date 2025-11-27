# 🔧 Troubleshooting Guide

Panduan lengkap untuk mengatasi masalah umum dalam Banking ETL Assessment Project.

## Installation Issues

### Issue 1: "Python command not found"

**Symptoms:**
```
'python' is not recognized as an internal or external command
```

**Solutions:**

**Windows:**
1. Verify Python installation:
   ```bash
   python --version
   ```
2. If not found, add Python to PATH:
   - Install Python from python.org
   - Check "Add Python to PATH" during installation
   - Restart terminal

**macOS/Linux:**
```bash
python3 --version
# Use python3 instead of python
python3 -m venv venv
```

---

### Issue 2: "Permission denied" on macOS/Linux

**Symptoms:**
```
bash: ./venv/bin/activate: Permission denied
```

**Solution:**
```bash
chmod +x venv/bin/activate
source venv/bin/activate
```

---

### Issue 3: "pip command not found"

**Symptoms:**
```
'pip' is not recognized as an internal or external command
```

**Solution:**
```bash
# Reinstall pip
python -m pip install --upgrade pip

# Or use pip3 on macOS/Linux
pip3 install -r requirements.txt
```

---

### Issue 4: "Virtual environment activation issues"

**Symptoms:**
- Terminal doesn't show `(venv)` prefix
- Packages installed but not available

**Solutions:**

**Windows - Try alternatives:**
```bash
# Option 1: Use python directly
python -m pip install -r requirements.txt

# Option 2: Use PowerShell
.\venv\Scripts\Activate.ps1

# Option 3: Use cmd.exe
venv\Scripts\activate.bat
```

**macOS/Linux:**
```bash
# Source is required
source venv/bin/activate

# Add full path if needed
/path/to/project/venv/bin/activate
```

---

### Issue 5: "Module 'typing' has no attribute 'list'"

**Symptoms:**
```
AttributeError: module 'typing' has no attribute 'list'
ImportError: cannot import name 'list' from 'typing'
```

**Cause:** Python 3.9+ doesn't support `typing.list` (use built-in `list`)

**Solution:**
This is already fixed in current code, but if you see it:
- Ensure you're using Python 3.9+
- Update imports to use built-in types:
  ```python
  # Wrong (Python 3.9+)
  from typing import list, dict
  def func() -> list[dict]:
      pass
  
  # Correct (Python 3.9+)
  def func() -> list:
      pass
  ```

---

## Runtime Issues

### Issue 6: "CSV file not found"

**Symptoms:**
```
ERROR: CSV file not found at data/banking_transactions.csv
CSVFileNotFoundError: File not found: data/banking_transactions.csv
```

**Solutions:**

1. Check file exists:
   ```bash
   # Windows
   dir data\banking_transactions.csv
   
   # macOS/Linux
   ls -la data/banking_transactions.csv
   ```

2. Run from project root:
   ```bash
   cd banking_etl_assessment
   python example.py
   ```

3. Use absolute path:
   ```python
   from etl.loader import load_csv
   
   transactions = load_csv('/full/path/to/banking_transactions.csv')
   ```

---

### Issue 7: "Invalid CSV file format"

**Symptoms:**
```
CSVMissingMandatoryFieldError: Missing mandatory columns
CSVColumnMismatchError: Column count mismatch
```

**Solutions:**

1. Verify CSV structure:
   ```bash
   # See first row
   head -n 2 data/banking_transactions.csv
   ```

2. Required columns:
   - transaction_id
   - transaction_date
   - customer_id
   - account_id
   - amount
   - currency

3. Check column count:
   ```bash
   # Count columns in first row
   head -1 data/banking_transactions.csv | tr ',' '\n' | wc -l
   ```

4. Fix CSV format:
   - Ensure comma-separated values
   - No missing headers
   - No special characters in headers
   - Proper quoting of values with commas

---

### Issue 8: "Validation errors"

**Symptoms:**
```
InvalidTransactionIDError: Invalid transaction ID: ABC123
InvalidDateFormatError: Invalid date format: 2024/01/01
InvalidCurrencyError: Invalid currency: EUR
InvalidAmountError: Invalid amount: -500
```

**Solutions:**

**Transaction ID Error:**
- Required format: `TXNxxxxxxx` (TXN + 7 digits)
- Fix: `TXN1234567` ✓ (not `ABC123` or `TXN123`)

**Date Format Error:**
- Accepted formats: `YYYY-MM-DD` or `DD/MM/YYYY`
- Fix: `2024-01-01` ✓ (not `2024/01/01`)

**Currency Error:**
- Allowed: IDR, USD, SGD only
- Fix: Use one of allowed currencies (not EUR, GBP, etc.)

**Amount Error:**
- Must be non-negative number
- Fix: `1000.00` ✓ (not `-500` or `invalid`)

---

### Issue 9: "Empty rows in CSV"

**Symptoms:**
```
CSVEmptyRowError: Empty row detected at row N
```

**Solution:**
1. Identify empty rows:
   ```bash
   # See row numbers with empty values
   awk -F',' 'NF < 10 {print NR": "$0}' data/banking_transactions.csv
   ```

2. Remove empty rows:
   ```python
   import csv
   
   # Read and filter
   rows = []
   with open('data/banking_transactions.csv') as f:
       reader = csv.DictReader(f)
       rows = [r for r in reader if any(r.values())]
   
   # Write back
   with open('data/banking_transactions_clean.csv', 'w', newline='') as f:
       writer = csv.DictWriter(f, fieldnames=rows[0].keys())
       writer.writeheader()
       writer.writerows(rows)
   ```

---

## Testing Issues

### Issue 10: "Tests not running"

**Symptoms:**
```
error collecting tests
no tests ran
```

**Solutions:**

1. Check pytest installed:
   ```bash
   pytest --version
   ```

2. Install if missing:
   ```bash
   pip install -r requirements.txt
   ```

3. Run from project root:
   ```bash
   cd banking_etl_assessment
   pytest tests/ -v
   ```

4. Check test files exist:
   ```bash
   ls -la tests/
   ```

---

### Issue 11: "Test import errors"

**Symptoms:**
```
ImportError: cannot import name 'X' from 'etl'
ModuleNotFoundError: No module named 'etl'
```

**Solutions:**

1. Activate virtual environment:
   ```bash
   # Windows
   .\venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

2. Check Python path:
   ```bash
   python -c "import sys; print(sys.path)"
   ```

3. Reinstall package in development mode:
   ```bash
   pip install -e .
   ```

4. Check __init__.py files exist:
   ```bash
   # Should exist in:
   # - banking_etl_assessment/__init__.py
   # - etl/__init__.py
   # - utils/__init__.py
   # - tests/__init__.py (optional but good)
   ```

---

### Issue 12: "Test failures"

**Symptoms:**
```
FAILED tests/test_validator.py::TestValidateDate::test_invalid_date
AssertionError: False is not True
```

**Solutions:**

1. See detailed error:
   ```bash
   pytest tests/test_validator.py::TestValidateDate::test_invalid_date -v
   ```

2. Run with full output:
   ```bash
   pytest tests/ -vv -s
   ```

3. Run single test file:
   ```bash
   pytest tests/test_validator.py -v
   ```

4. Check test logic vs implementation:
   - Review test case expectations
   - Verify function behavior
   - Check edge case handling

---

### Issue 13: "pytest-asyncio warnings"

**Symptoms:**
```
WARNING: asyncio.TimeoutError recorded as assertion error
```

**Solution:**
- Upgrade pytest-asyncio:
  ```bash
  pip install --upgrade pytest-asyncio
  ```

- Add to pytest.ini:
  ```ini
  [pytest]
  asyncio_mode = auto
  ```

---

## Async API Issues

### Issue 14: "Async operation errors"

**Symptoms:**
```
asyncio.TimeoutError: Timeout while fetching quote
aiohttp.ClientError: Cannot connect to host
```

**Solutions:**

1. Increase timeout:
   ```python
   from utils.async_api import fetch_quote
   
   # Default is 10 seconds, try longer
   result = await fetch_quote('AAPL')  # with retry decorator
   ```

2. Check network connection:
   ```bash
   ping www.google.com
   ```

3. Check API endpoint:
   ```bash
   curl https://dummyjson.com/quotes/random
   ```

4. Use with error handling:
   ```python
   import asyncio
   from utils.async_api import fetch_quote
   
   try:
       result = await fetch_quote('AAPL')
   except asyncio.TimeoutError:
       print("Request timed out - API server slow")
   except Exception as e:
       print(f"Error: {e}")
   ```

---

### Issue 15: "SSL/TLS certificate errors"

**Symptoms:**
```
aiohttp.ClientSSLError: Cannot connect to host dummyjson.com ssl:True
```

**Solution:**
```python
import ssl
import aiohttp

# Disable SSL verification (NOT for production!)
connector = aiohttp.TCPConnector(ssl=False)
session = aiohttp.ClientSession(connector=connector)

# Better: Use system certificates
import certifi
ssl_context = ssl.create_default_context(cafile=certifi.where())
connector = aiohttp.TCPConnector(ssl=ssl_context)
```

---

### Issue 16: "Too many concurrent requests"

**Symptoms:**
```
aiohttp.ClientError: Too many connections
ConnectionError: Connection refused
```

**Solution:**
```python
from utils.async_api import fetch_multiple_quotes

# Reduce concurrency
async def fetch_with_limit(symbols, max_concurrent=3):
    semaphore = asyncio.Semaphore(max_concurrent)
    
    async def limited_fetch(symbol):
        async with semaphore:
            from utils.async_api import fetch_quote
            return await fetch_quote(symbol)
    
    tasks = [limited_fetch(s) for s in symbols]
    return await asyncio.gather(*tasks, return_exceptions=True)
```

---

## Data Quality Issues

### Issue 17: "Data cleaning not working"

**Symptoms:**
```
Whitespace not trimmed
Currency not normalized
Merchant category still empty
```

**Solutions:**

1. Check input data:
   ```python
   from etl.cleaner import clean_transaction
   
   transaction = {'name': '  John  ', 'currency': 'idr'}
   cleaned = clean_transaction(transaction)
   print(cleaned)  # Check output
   ```

2. Verify cleaning functions:
   ```python
   from etl.cleaner import trim_whitespace, normalize_currency
   
   assert trim_whitespace('  test  ') == 'test'
   assert normalize_currency('idr') == 'IDR'
   ```

3. Check order of operations:
   - Trim whitespace first
   - Then normalize other fields
   - Finally impute missing values

---

### Issue 18: "Feature engineering incorrect"

**Symptoms:**
```
is_large_transaction = False (should be True)
amount_log = None (should be float)
```

**Solutions:**

1. Check threshold values:
   - Large transaction: amount > 5,000,000
   - Crossborder: currency != 'IDR'

2. Verify amount conversion:
   ```python
   from etl.transformer import calculate_amount_log
   import math
   
   amount = 1000
   result = calculate_amount_log(amount)
   assert result == math.log(1000)
   ```

3. Test transformations:
   ```python
   from etl.transformer import transform_transaction
   
   transaction = {
       'transaction_date': '2024-01-01',
       'amount': '10000000',
       'currency': 'USD',
       'risk_score': '0.5'
   }
   
   result = transform_transaction(transaction)
   print(result)  # Verify all fields present
   ```

---

## Performance Issues

### Issue 19: "Slow CSV loading"

**Symptoms:**
```
Taking more than 10 seconds to load CSV
Memory usage very high
```

**Solutions:**

1. Use generator for large files:
   ```python
   def load_csv_streaming(path: str):
       """Memory-efficient CSV loading"""
       with open(path) as f:
           reader = csv.DictReader(f)
           for row in reader:
               yield row
   
   # Use
   for transaction in load_csv_streaming('data.csv'):
       # Process one at a time
       pass
   ```

2. Use pandas for better performance:
   ```bash
   pip install pandas
   ```
   ```python
   import pandas as pd
   
   df = pd.read_csv('data/banking_transactions.csv')
   transactions = df.to_dict('records')
   ```

3. Monitor memory:
   ```bash
   # Windows
   Get-Process python
   
   # macOS/Linux
   ps aux | grep python
   ```

---

### Issue 20: "Slow async operations"

**Symptoms:**
```
fetch_multiple_quotes taking 30+ seconds
```

**Solution:**
```python
import asyncio
from utils.async_api import fetch_multiple_quotes

# Check if running concurrently
symbols = ['AAPL', 'GOOGL', 'MSFT']

# This should be ~10 seconds (parallel)
# Not ~30 seconds (sequential)
results = await fetch_multiple_quotes(symbols)
```

---

## Debugging Techniques

### Enable Debug Logging

```python
import logging

# Set to DEBUG level
logging.basicConfig(level=logging.DEBUG)

# Or for specific module
logger = logging.getLogger('etl')
logger.setLevel(logging.DEBUG)

# Then run your code
from etl.loader import load_csv
transactions = load_csv('data/banking_transactions.csv')
# Will show DEBUG messages
```

### Use Python Debugger

```python
from etl.validator import validate_transaction

transaction = {
    'transaction_id': 'TXN1234567',
    'transaction_date': '2024-01-01',
    'amount': '1000'
}

# Add breakpoint
import pdb; pdb.set_trace()
result = validate_transaction(transaction)

# In debugger:
# (Pdb) print(result)
# (Pdb) next
# (Pdb) continue
```

### Print Debugging

```python
# Add print statements
transaction = {'amount': '1000'}
print(f"Before: {transaction}")

cleaned = clean_transaction(transaction)
print(f"After: {cleaned}")

# Or use logging
import logging
logger = logging.getLogger(__name__)
logger.debug(f"Transaction: {transaction}")
```

### Unit Testing for Debugging

```bash
# Run tests with output
pytest tests/test_validator.py -v -s

# Run specific test
pytest tests/test_validator.py::TestValidateDate::test_valid_date -v

# Show print statements
pytest tests/ -s
```

---

## Getting Help

### Check Documentation
- `README.md` - Project overview
- `SETUP.md` - Installation guide
- `ARCHITECTURE.md` - System design
- `API.md` - Async API documentation
- Code docstrings:
  ```bash
  python -c "from etl.loader import load_csv; help(load_csv)"
  ```

### Check Existing Tests
- `tests/` folder has examples for each module
- Tests show expected behavior
- Great reference for usage

### Common Error Messages

| Error | Cause | Fix |
|-------|-------|-----|
| `CSVFileNotFoundError` | CSV file missing | Verify file path |
| `InvalidTransactionIDError` | Bad ID format | Use TXNxxxxxxx format |
| `InvalidDateFormatError` | Bad date format | Use YYYY-MM-DD |
| `InvalidCurrencyError` | Currency not IDR/USD/SGD | Use valid currency |
| `InvalidAmountError` | Amount is negative/invalid | Use positive number |
| `asyncio.TimeoutError` | API slow | Increase timeout |
| `aiohttp.ClientError` | Network error | Check connection |

---

## System Information Debugging

**Collect this info when reporting issues:**

```bash
# Python version
python --version

# Installed packages
pip list

# OS info
# Windows
systeminfo

# macOS
system_profiler SPHardwareDataType

# Linux
uname -a

# Project structure
find . -name "*.py" -type f

# Recent error log
tail -50 app.log
```

---

## Contact & Support

For persistent issues:
1. Check all documentation above
2. Review test cases for expected behavior
3. Verify data format matches requirements
4. Check error logs for details
5. Try minimal reproducible example

---

**Last Updated**: 2024
**Version**: 1.0
