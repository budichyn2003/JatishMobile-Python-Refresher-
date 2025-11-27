# 🏗️ Architecture Documentation

Dokumentasi lengkap tentang arsitektur Banking ETL Assessment Project.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Banking ETL Assessment                   │
└─────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
    ┌─────────┐       ┌─────────┐       ┌────────────┐
    │   Data  │       │   ETL   │       │  Utilities │
    │ Loading │       │Pipeline │       │   (Async)  │
    └─────────┘       └─────────┘       └────────────┘
        │                   │                   │
        │              ┌────┴────┐              │
        │              │          │              │
    ┌───▼────┐    ┌────▼──┐  ┌───▼──┐    ┌─────▼─────┐
    │ Loader │    │Validat│  │Clean │    │ Async API │
    │        │    │ e     │  │er    │    │ Utilities │
    └────────┘    └───────┘  └──────┘    └───────────┘
        │              │         │           │
        │              ▼         ▼           ▼
        │         ┌────────────────────┐
        │         │  Transformer       │
        │         │  (Feature Engineer)│
        │         └────────────────────┘
        │              │
        └──────────────┼──────────────┘
                       ▼
          ┌─────────────────────────┐
          │  Processed Data Output  │
          │  (Ready for Analytics)  │
          └─────────────────────────┘
```

## Data Flow

### 1. Data Ingestion (Loading)

```
CSV File (banking_transactions.csv)
    │
    ▼
┌─────────────────────────┐
│ load_csv()              │
├─────────────────────────┤
│ • Read CSV file         │
│ • Validate file exists  │
│ • Check mandatory cols  │
│ • Detect empty rows     │
│ • Verify column count   │
└─────────────────────────┘
    │
    ▼
List[dict[str, Any]]
(Raw transaction data)
```

**Error Handling:**
- CSVFileNotFoundError: File tidak ditemukan
- CSVMissingMandatoryFieldError: Kolom wajib hilang
- CSVEmptyRowError: Ada baris kosong
- CSVColumnMismatchError: Jumlah kolom tidak sesuai

### 2. Validation (Quality Assurance)

```
Raw Transaction Dict
    │
    ▼
┌──────────────────────────────┐
│ validate_transaction()       │
├──────────────────────────────┤
│ • Check transaction_id       │
│ • Validate date format       │
│ • Validate amount (positive) │
│ • Check currency (IDR/USD)   │
│ • Check account_type         │
│ • Flag amount anomalies      │
└──────────────────────────────┘
    │
    ├─ VALID ─────┐
    │             ▼
    │    Dict (validated)
    │
    └─ INVALID ──→ Raise Exception
```

**Validation Rules:**
1. **transaction_id**: Pattern `TXNxxxxxxx` (regex: `^TXN\d{7}$`)
2. **transaction_date**: Format `YYYY-MM-DD` atau `DD/MM/YYYY`
3. **amount**: Non-negative, float-convertible
4. **currency**: Whitelist (IDR, USD, SGD only)
5. **direction**: DEBIT atau CREDIT
6. **account_type**: SAVINGS, CURRENT, CREDIT_CARD, LOAN
7. **Anomaly Check**: Flag jika amount > 10,000,000

### 3. Cleaning (Data Quality)

```
Validated Transaction
    │
    ▼
┌────────────────────────────────┐
│ clean_transaction()            │
├────────────────────────────────┤
│ • Trim whitespace              │
│ • Normalize date format        │
│ • Normalize currency (uppercase)
│ • Clean numeric values         │
│ • Impute merchant_category     │
└────────────────────────────────┘
    │
    ▼
Cleaned Transaction Dict
(All values standardized)
```

**Cleaning Operations:**
1. **Whitespace Trimming**: Hapus leading/trailing spaces
2. **Date Normalization**: Konversi ke `YYYY-MM-DD`
3. **Currency Normalization**: Konversi ke uppercase
4. **Numeric Cleaning**: Handle None, empty strings, invalid values
5. **Category Imputation**: Default "Unknown" untuk kategori kosong

### 4. Transformation (Feature Engineering)

```
Cleaned Transaction
    │
    ▼
┌───────────────────────────────────┐
│ transform_transaction()           │
├───────────────────────────────────┤
│ Type Conversions:                 │
│ • transaction_date → date object  │
│ • amount → float                  │
│ • risk_score → float or None      │
│                                   │
│ Derived Features:                 │
│ • is_large_transaction (bool)     │
│ • is_crossborder (bool)           │
│ • transaction_day (str)           │
│ • amount_log (float)              │
└───────────────────────────────────┘
    │
    ▼
Enriched Transaction Dict
(Ready for analytics)
```

**Transformations:**

| Feature | Input | Output | Logic |
|---------|-------|--------|-------|
| `is_large_transaction` | amount | bool | amount > 5,000,000 |
| `is_crossborder` | currency | bool | currency != 'IDR' |
| `transaction_day` | date | str | Hari (Monday-Sunday) |
| `amount_log` | amount | float | log(amount) if amount > 0 |

### 5. Async Utilities (External Data)

```
External API Call
    │
    ▼
┌──────────────────────────────────┐
│ fetch_quote(symbol)              │
├──────────────────────────────────┤
│ • Make HTTP request              │
│ • Handle timeout (10s)           │
│ • Retry on failure (3 attempts)  │
│ • Parse response                 │
└──────────────────────────────────┘
    │
    ├─ SUCCESS ────→ Return quote dict
    │
    └─ FAILURE ───→ Log & Return None
               (filtered in concurrent)
```

**Retry Strategy:**
- Max Retries: 3 attempts
- Timeout: 10 seconds per attempt
- Backoff: 1 second delay between retries
- Error Types: TimeoutError, ClientError, generic exceptions

## Module Design

### `etl/loader.py`
**Responsibility**: Data ingestion dari CSV file

**Key Functions:**
- `load_csv(path: str) -> list`: Main entry point
- Internal validation functions

**Dependencies:** csv, logging, pathlib, typing

**Exception Hierarchy:**
```
Exception
├── CSVFileNotFoundError
├── CSVEmptyRowError
├── CSVColumnMismatchError
└── CSVMissingMandatoryFieldError
```

### `etl/validator.py`
**Responsibility**: Business rule validation

**Key Functions:**
- `validate_transaction(dict) -> dict`: Main orchestrator
- `validate_transaction_id(str) -> bool`
- `validate_date(str) -> bool`
- `validate_amount(Any) -> bool`
- `validate_currency(str) -> bool`
- `check_amount_anomaly(float) -> bool`

**Dependencies:** logging, re, datetime, typing

**Exception Hierarchy:**
```
Exception
├── InvalidTransactionIDError
├── InvalidDateFormatError
├── InvalidCurrencyError
└── InvalidAmountError
```

### `etl/cleaner.py`
**Responsibility**: Data normalization dan quality improvement

**Key Functions:**
- `clean_transaction(dict) -> dict`: Main orchestrator
- `trim_whitespace(str) -> str`
- `normalize_date(str) -> str`
- `normalize_currency(str) -> str|None`
- `clean_numeric(Any) -> float|None`
- `clean_merchant_category(str) -> str`

**Dependencies:** logging, datetime, typing

### `etl/transformer.py`
**Responsibility**: Type conversion dan feature engineering

**Key Functions:**
- `transform_transaction(dict) -> dict`: Main orchestrator
- `convert_date_to_date_object(str) -> date`
- `convert_amount_to_float(Any) -> float`
- `convert_risk_score_to_float(Any) -> float|None`
- `is_large_transaction(float) -> bool`
- `is_crossborder_transaction(str) -> bool`
- `get_transaction_day(date) -> str`
- `calculate_amount_log(float) -> float|None`

**Dependencies:** logging, math, datetime, typing

### `utils/async_api.py`
**Responsibility**: Async HTTP operations dengan retry logic

**Key Functions:**
- `@retry_on_failure(max_retries=3, timeout=10)`: Decorator
- `async fetch_quote(symbol: str) -> dict`: Fetch single quote
- `async fetch_multiple_quotes(symbols: list) -> list`: Concurrent fetch

**Dependencies:** asyncio, logging, functools, typing, aiohttp

### `tests/`
**Responsibility**: Unit tests untuk semua modul

**Structure:**
- `conftest.py`: Pytest fixtures
- `test_loader.py`: Loader tests (6 tests)
- `test_validator.py`: Validator tests (26 tests)
- `test_cleaner.py`: Cleaner tests (28 tests)
- `test_transformer.py`: Transformer tests (27 tests)
- `test_utils.py`: Async API tests (4 tests)

**Total**: 102 tests, 100% passing

## Design Patterns

### 1. Pipeline Pattern
```
Load → Validate → Clean → Transform
  ↓        ↓         ↓        ↓
Input   Quality   Normalize  Output
```

Each stage:
- Takes input from previous stage
- Applies specific transformation
- Validates output
- Passes to next stage
- Or raises exception

### 2. Decorator Pattern
```python
@retry_on_failure(max_retries=3, timeout=10)
async def fetch_quote():
    # Original function
    pass

# Decorator adds:
# • Retry logic
# • Timeout handling
# • Error logging
# • Automatic backoff
```

### 3. Custom Exception Hierarchy
```python
# Base exceptions inherit from Exception
class CSVFileNotFoundError(Exception):
    pass

# Enables specific error handling
try:
    transactions = load_csv('file.csv')
except CSVFileNotFoundError:
    # Handle specific error
    pass
except Exception:
    # Fallback for other errors
    pass
```

### 4. Fixture Pattern (Testing)
```python
@pytest.fixture
def valid_transaction():
    return {
        'transaction_id': 'TXN1234567',
        'transaction_date': '2024-01-01',
        'amount': '1000.00',
        'currency': 'IDR',
        # ... other fields
    }

# Use in tests
def test_validator(valid_transaction):
    assert validate_transaction(valid_transaction)
```

### 5. Single Responsibility Principle (SRP)
```
loader.py      → Only handles CSV loading
validator.py   → Only validates business rules
cleaner.py     → Only normalizes data
transformer.py → Only converts types & engineers features
async_api.py   → Only handles async HTTP operations
```

Each function does ONE thing:
- `trim_whitespace()`: Only trim spaces
- `validate_date()`: Only validate date format
- `is_large_transaction()`: Only check if large

## Code Organization

### Type Hints
```python
def validate_transaction(transaction: dict[str, Any]) -> dict[str, Any]:
    """
    Full type hints for clarity:
    - Input: dict with string keys and Any values
    - Output: dict with string keys and Any values
    """
    pass
```

### Logging Strategy
```python
import logging
logger = logging.getLogger(__name__)

logger.info("Loading CSV file: banking_transactions.csv")
logger.debug("Row 1 validation passed")
logger.warning("Amount anomaly detected: 15,000,000 > 10,000,000")
logger.error("Invalid date format: 2024-13-01")
```

### Error Handling
```python
# Explicit error handling
try:
    validate_date(date_str)
except InvalidDateFormatError as e:
    logger.error(f"Date validation failed: {e}")
    raise  # Re-raise for caller to handle
```

## Performance Considerations

### 1. CSV Loading
- **Time**: O(n) where n = number of rows
- **Memory**: O(n) for list of dicts
- **Optimization**: Use generators for large files

### 2. Validation
- **Time**: O(n × v) where v = validation rules
- **Current**: 7 validation rules per transaction
- **Optimization**: Early exit on first failure

### 3. Transformation
- **Time**: O(n × f) where f = feature count
- **Current**: 7 features per transaction (4 engineered)
- **Optimization**: Vectorize with pandas if needed

### 4. Async Operations
- **Concurrency**: asyncio.gather() for parallel requests
- **Speed**: 3 requests in ~10s (vs ~30s sequential)
- **Scalability**: Semaphore for rate limiting

## Testing Strategy

### Unit Tests (102 total)
```
test_loader.py      → 6 tests
test_validator.py   → 26 tests
test_cleaner.py     → 28 tests
test_transformer.py → 27 tests
test_utils.py       → 15 tests
```

### Test Categories
1. **Normal Cases**: Valid input, expected behavior
2. **Edge Cases**: Empty strings, None values, boundary values
3. **Error Cases**: Invalid input, exceptions raised
4. **Integration**: Full pipeline execution

### Coverage Areas
- ✅ CSV validation (file exists, columns correct, rows valid)
- ✅ Data validation (ID pattern, dates, amounts, currencies)
- ✅ Data cleaning (whitespace, date format, category imputation)
- ✅ Type conversion (string→float, string→date)
- ✅ Feature engineering (large transaction, crossborder, day, log)
- ✅ Async operations (single fetch, multiple concurrent, error handling)

## Scalability

### Current Limitations
- Loads entire CSV into memory
- No database persistence
- Single-threaded processing
- Synchronous main pipeline

### Improvements for Scale
1. **Streaming**: Use generators instead of loading entire CSV
2. **Database**: Add PostgreSQL/MongoDB for persistence
3. **Parallelization**: Process batches concurrently
4. **Async Processing**: Make entire pipeline async
5. **Caching**: Add Redis for memoization
6. **Messaging**: Use Kafka/RabbitMQ for event streaming

### Example: Streaming CSV
```python
def load_csv_streaming(path: str):
    """Generator instead of loading all into memory"""
    with open(path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield row

# Use
for transaction in load_csv_streaming('data.csv'):
    validated = validate_transaction(transaction)
    cleaned = clean_transaction(validated)
    transformed = transform_transaction(cleaned)
```

## Deployment Considerations

### Environment Variables
```python
import os

CSV_PATH = os.getenv('CSV_PATH', 'data/banking_transactions.csv')
API_TIMEOUT = int(os.getenv('API_TIMEOUT', '10'))
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
```

### Configuration Management
```python
# config.py
class Config:
    CSV_PATH = 'data/banking_transactions.csv'
    BATCH_SIZE = 1000
    API_TIMEOUT = 10
    MAX_RETRIES = 3
    
class ProdConfig(Config):
    CSV_PATH = '/data/production.csv'
    BATCH_SIZE = 5000
```

### Monitoring & Logging
```python
import logging.config

LOGGING_CONFIG = {
    'version': 1,
    'handlers': {
        'console': {'class': 'logging.StreamHandler'},
        'file': {'class': 'logging.FileHandler', 'filename': 'app.log'}
    },
    'root': {'handlers': ['console', 'file'], 'level': 'INFO'}
}

logging.config.dictConfig(LOGGING_CONFIG)
```

## Security Considerations

### Data Validation
✅ Input validation for all fields
✅ Type checking in all functions
✅ Whitelist-based currency validation

### Error Messages
✅ No sensitive data in error messages
✅ Generic errors for external APIs
✅ Detailed logging for debugging

### Dependencies
✅ All dependencies pinned in requirements.txt
✅ Minimal, well-maintained packages
✅ No dangerous eval() or exec()

## Future Enhancements

### Short Term
1. Add database integration
2. Implement streaming CSV processing
3. Add API endpoint for processing
4. Create Docker image

### Long Term
1. Machine learning fraud detection
2. Real-time streaming with Kafka
3. GraphQL API
4. Admin dashboard
5. Data warehouse integration

## References

- [Python Async IO](https://docs.python.org/3/library/asyncio.html)
- [pytest Documentation](https://docs.pytest.org/)
- [PEP 8 Style Guide](https://pep8.org/)
- [aiohttp Documentation](https://docs.aiohttp.org/)

---

**Last Updated**: 2024
**Version**: 1.0
**Architecture Pattern**: Pipeline + Decorator Pattern
