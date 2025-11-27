# Banking ETL Assessment Project

A complete Python ETL (Extract, Transform, Load) mini project for processing banking transactions data with comprehensive validation, cleaning, and transformation pipelines.

## 📋 Project Overview

This project implements a full ETL pipeline for banking transactions with the following key components:

- **Data Loading**: Read and validate CSV files with error handling
- **Validation**: Comprehensive transaction validation with custom exceptions
- **Cleaning**: Data normalization and quality improvements
- **Transformation**: Type conversions and derived feature engineering
- **Async API**: Async HTTP client with retry logic
- **Unit Tests**: Comprehensive pytest coverage

## 📁 Folder Structure

```
banking_etl_assessment/
│
├── README.md                          # Project documentation
├── requirements.txt                   # Python dependencies
│
├── data/
│   └── banking_transactions.csv       # Source data file
│
├── etl/
│   ├── __init__.py                    # ETL module init
│   ├── loader.py                      # CSV loader with error handling
│   ├── validator.py                   # Transaction validation rules
│   ├── cleaner.py                     # Data cleaning functions
│   └── transformer.py                 # Type conversions & feature engineering
│
├── utils/
│   ├── __init__.py                    # Utils module init
│   └── async_api.py                   # Async API client with retry logic
│
└── tests/
    ├── conftest.py                    # Pytest fixtures
    ├── test_loader.py                 # CSV loader tests
    ├── test_validator.py              # Validator tests
    ├── test_cleaner.py                # Cleaner tests
    ├── test_transformer.py            # Transformer tests
    └── test_utils.py                  # Async API tests
```

## 🔄 ETL Flow Explanation

### 1. **Load Phase** (`etl/loader.py`)
- Read CSV file using Python's `csv` module
- Convert to list of dictionaries
- Validate mandatory columns presence
- Detect empty rows and column mismatches

**Custom Exceptions:**
- `CSVFileNotFoundError` - File doesn't exist
- `CSVMissingMandatoryFieldError` - Missing required columns
- `CSVColumnMismatchError` - Wrong column count in rows
- `CSVEmptyRowError` - Empty rows detected

### 2. **Validate Phase** (`etl/validator.py`)
- Check transaction ID format: `TXNxxxxxxx` (TXN + 7 digits)
- Validate date format: `YYYY-MM-DD` or `DD/MM/YYYY`
- Verify amount is non-negative and not empty
- Check currency is in valid set: `IDR`, `USD`, `SGD`
- Optional: Validate direction (`DEBIT`, `CREDIT`) and account type
- Flag anomalies for large amounts (> 10,000,000)

**Custom Exceptions:**
- `InvalidTransactionIDError` - Invalid ID format
- `InvalidDateFormatError` - Invalid date format
- `InvalidCurrencyError` - Invalid currency code
- `InvalidAmountError` - Invalid or negative amount

### 3. **Clean Phase** (`etl/cleaner.py`)
- Trim whitespace from all string fields
- Normalize dates to `YYYY-MM-DD` format
- Normalize currency to uppercase
- Handle missing numeric values → set to `None`
- Impute missing merchant category → `"Unknown"`

### 4. **Transform Phase** (`etl/transformer.py`)
- Convert transaction date to `datetime.date` object
- Convert amount to `float`
- Convert risk_score to `float` or `None`
- **Derived Features:**
  - `is_large_transaction`: `amount > 5,000,000` (boolean)
  - `is_crossborder`: `currency != "IDR"` (boolean)
  - `transaction_day`: Day name (Monday-Sunday)
  - `amount_log`: `log(amount)` if amount > 0

## ✅ Validation Rules

### Mandatory Fields
All transactions must have:
- `transaction_id`
- `transaction_date`
- `customer_id`
- `account_id`
- `amount`
- `currency`

### Validation Rules

| Field | Rules |
|-------|-------|
| `transaction_id` | Pattern: `TXNxxxxxxx` (TXN + 7 digits) |
| `transaction_date` | Format: `YYYY-MM-DD` or `DD/MM/YYYY` |
| `amount` | Cannot be negative, cannot be empty |
| `currency` | Must be: `IDR`, `USD`, `SGD` |
| `direction` | Must be: `DEBIT`, `CREDIT` (optional) |
| `account_type` | Must be: `SAVINGS`, `CURRENT`, `CREDIT_CARD`, `LOAN` (optional) |
| `amount_anomaly` | Flagged when amount > 10,000,000 |

## 🚀 Cara Menjalankan Project

### 1. Setup Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run ETL Pipeline (Example)

```python
from etl.loader import load_csv
from etl.validator import validate_transaction
from etl.cleaner import clean_transaction
from etl.transformer import transform_transaction
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Load data
transactions = load_csv('data/banking_transactions.csv')
print(f"Loaded {len(transactions)} transactions")

# Process first transaction as example
if transactions:
    raw_txn = transactions[0]
    
    # Validate
    validated = validate_transaction(raw_txn)
    
    # Clean
    cleaned = clean_transaction(validated)
    
    # Transform
    transformed = transform_transaction(cleaned)
    
    print("Processed transaction:")
    print(f"  ID: {transformed.get('transaction_id')}")
    print(f"  Date: {transformed.get('transaction_date')}")
    print(f"  Amount: {transformed.get('amount')}")
    print(f"  Large Transaction: {transformed.get('is_large_transaction')}")
    print(f"  Crossborder: {transformed.get('is_crossborder')}")
    print(f"  Day: {transformed.get('transaction_day')}")
    print(f"  Log Amount: {transformed.get('amount_log')}")
```

## 🧪 Cara Menjalankan Unit Test

### Run All Tests

```bash
pytest
```

### Run Tests with Coverage

```bash
pytest --cov=etl --cov=utils --cov-report=html
```

### Run Specific Test File

```bash
# Test loader
pytest tests/test_loader.py -v

# Test validator
pytest tests/test_validator.py -v

# Test cleaner
pytest tests/test_cleaner.py -v

# Test transformer
pytest tests/test_transformer.py -v

# Test async API
pytest tests/test_utils.py -v
```

### Run Specific Test Class

```bash
pytest tests/test_validator.py::TestValidateTransactionID -v
```

### Run Specific Test Function

```bash
pytest tests/test_validator.py::TestValidateTransactionID::test_valid_transaction_id -v
```

## 📊 Contoh Output

### Sample Loaded Transaction
```json
{
  "transaction_id": "TXN0000001",
  "transaction_date": "2024-02-21",
  "value_date": "2024-02-22",
  "customer_id": "CUST00375",
  "account_id": "ACC00000496",
  "account_type": "CREDIT_CARD",
  "txn_type": "WITHDRAWAL",
  "channel": "POS",
  "direction": "DEBIT",
  "amount": "5239.52",
  "currency": "SGD",
  "merchant_category": "RENT",
  "region": "MDN",
  "risk_score": "0.104",
  "is_fraud_suspected": "0"
}
```

### Sample Transformed Transaction
```python
{
  "transaction_id": "TXN0000001",
  "transaction_date": <date(2024, 2, 21)>,          # datetime.date object
  "value_date": <date(2024, 2, 22)>,
  "customer_id": "CUST00375",
  "account_id": "ACC00000496",
  "account_type": "CREDIT_CARD",
  "amount": 5239.52,                                # float
  "currency": "SGD",
  "merchant_category": "RENT",
  "risk_score": 0.104,                              # float
  "is_large_transaction": False,                    # amount <= 5,000,000
  "is_crossborder": True,                           # currency != 'IDR'
  "transaction_day": "Wednesday",                   # datetime weekday
  "amount_log": 8.564,                              # log(5239.52)
  "amount_anomaly": False                           # amount <= 10,000,000
}
```

## 🔮 Potential Improvements

1. **Database Integration**
   - Store processed data in PostgreSQL/MongoDB
   - Add ORM (SQLAlchemy) for database operations

2. **Enhanced Error Handling**
   - Add error recovery mechanisms
   - Implement transaction rollback for failed batches
   - Create error logs for debugging

3. **Performance Optimization**
   - Implement batch processing for large datasets
   - Use pandas for faster CSV processing
   - Add caching mechanisms for repeated validations

4. **Advanced Features**
   - Machine learning for fraud detection
   - Real-time streaming pipeline (Kafka)
   - Data quality metrics and monitoring
   - Automated report generation

5. **Code Quality**
   - Add pre-commit hooks for linting
   - Implement CI/CD pipeline (GitHub Actions)
   - Add type checking with mypy
   - Code coverage targets (>90%)

6. **Documentation**
   - API documentation with Sphinx
   - Architecture diagrams
   - Performance benchmarks
   - Troubleshooting guide

## 📦 Code Quality Standards

This project follows:
- **PEP 8** - Python code style guide
- **Type Hints** - Full type annotations for better IDE support
- **Logging** - Proper logging at INFO, WARNING, ERROR levels
- **SRP** - Single Responsibility Principle
- **DRY** - Don't Repeat Yourself principle
- **SOLID** - Object-oriented design principles

## 🔐 GitHub Deployment

### Prerequisites
- GitHub account
- Git installed locally

### Steps

1. **Initialize Local Repository**
   ```bash
   cd banking_etl_assessment
   git init
   ```

2. **Add All Files**
   ```bash
   git add .
   ```

3. **Create Initial Commit**
   ```bash
   git commit -m "Initial ETL project"
   ```

4. **Rename Branch to main**
   ```bash
   git branch -M main
   ```

5. **Add Remote Repository**
   ```bash
   git remote add origin https://github.com/USERNAME/banking_etl_assessment.git
   ```
   
   *Replace `USERNAME` with your GitHub username*

6. **Push to GitHub**
   ```bash
   git push -u origin main
   ```

### Optional: Add .gitignore

Create `.gitignore` file:
```
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST
.pytest_cache/
htmlcov/
.coverage
.venv
.DS_Store
```

Then commit:
```bash
git add .gitignore
git commit -m "Add .gitignore"
git push
```

## 📚 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `aiohttp` | >=3.8.0 | Async HTTP client |
| `pytest` | >=7.0.0 | Testing framework |
| `pytest-asyncio` | >=0.21.0 | Async test support |
| `python-dateutil` | >=2.8.0 | Date parsing utilities |

## 📝 License

This project is open source and available under the MIT License.

## ✍️ Author

Created as an ETL Assessment Project

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

**Last Updated**: November 2024
