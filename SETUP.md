# 🛠️ Setup Instructions

Panduan lengkap untuk setup dan menjalankan Banking ETL Assessment Project.

## System Requirements

- Python 3.8+
- pip (Python package manager)
- Git (untuk version control)
- Virtual Environment (recommended)

## Installation Steps

### 1. Clone or Download the Project

**Option A: Clone from GitHub**
```bash
git clone https://github.com/USERNAME/banking_etl_assessment.git
cd banking_etl_assessment
```

**Option B: Download as ZIP**
- Download repository from GitHub
- Extract to your desired location
- Open terminal in extracted folder

### 2. Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` prefix in your terminal.

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `aiohttp` - Async HTTP client
- `pytest` - Testing framework
- `pytest-asyncio` - Async test support
- `python-dateutil` - Date utilities

Verify installation:
```bash
pip list
```

### 4. Verify Installation

Run the example script to verify everything works:

```bash
python example.py
```

You should see output showing 5 processed transactions.

## Running Unit Tests

### Run All Tests

```bash
pytest tests/ -v
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

### Run with Coverage Report

```bash
pytest --cov=etl --cov=utils --cov-report=html
```

This creates a coverage report in `htmlcov/index.html`.

## Using the ETL Pipeline

### Basic Usage

```python
from etl.loader import load_csv
from etl.validator import validate_transaction
from etl.cleaner import clean_transaction
from etl.transformer import transform_transaction

# Load CSV
transactions = load_csv('data/banking_transactions.csv')

# Process first transaction
if transactions:
    # Validate
    validated = validate_transaction(transactions[0])
    
    # Clean
    cleaned = clean_transaction(validated)
    
    # Transform
    transformed = transform_transaction(cleaned)
    
    # Output
    print(transformed)
```

### Using in Your Code

```python
# Import the modules
from etl import load_csv, validate_transaction, clean_transaction, transform_transaction

# Process all transactions
transactions = load_csv('your_data.csv')

for txn in transactions:
    try:
        # Full pipeline
        validated = validate_transaction(txn)
        cleaned = clean_transaction(validated)
        transformed = transform_transaction(cleaned)
        
        # Use transformed data
        print(f"Processed: {transformed['transaction_id']}")
    except Exception as e:
        print(f"Error: {e}")
```

## Project Structure

```
banking_etl_assessment/
├── __init__.py
├── README.md
├── GITHUB.md              # GitHub deployment guide
├── SETUP.md              # This file
├── requirements.txt      # Python dependencies
├── example.py           # Example usage script
│
├── data/
│   └── banking_transactions.csv    # Sample data
│
├── etl/
│   ├── __init__.py
│   ├── loader.py         # CSV loading with validation
│   ├── validator.py      # Transaction validation
│   ├── cleaner.py        # Data cleaning
│   └── transformer.py    # Feature transformation
│
├── utils/
│   ├── __init__.py
│   └── async_api.py      # Async API utilities
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py       # pytest configuration
│   ├── test_loader.py
│   ├── test_validator.py
│   ├── test_cleaner.py
│   ├── test_transformer.py
│   └── test_utils.py
│
└── venv/                 # Virtual environment (created locally)
```

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'pytest'"

**Solution**: Install requirements:
```bash
pip install -r requirements.txt
```

### Issue: "Virtual environment not activated"

**Solution**: Activate virtual environment:

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### Issue: "CSV file not found"

**Solution**: Ensure you're running from project root directory:
```bash
cd banking_etl_assessment
python example.py
```

### Issue: "aiohttp SSL error"

**Solution**: This is normal for some async operations. The retry logic will handle it.

## Development Setup

If you want to contribute to the project:

1. **Install development dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install black mypy pylint
   ```

2. **Format code**:
   ```bash
   black etl/ utils/ tests/
   ```

3. **Run type checking**:
   ```bash
   mypy etl/ utils/
   ```

4. **Run linting**:
   ```bash
   pylint etl/ utils/
   ```

## Deactivating Virtual Environment

When you're done:

```bash
deactivate
```

## Next Steps

1. ✅ Setup complete!
2. Run `python example.py` to test
3. Run `pytest tests/ -v` to run tests
4. Check `README.md` for project details
5. Check `GITHUB.md` for GitHub deployment
6. Modify code for your needs

## Getting Help

- Check `README.md` for project documentation
- Review test files in `tests/` for usage examples
- Read docstrings in `etl/` and `utils/` modules
- Check `example.py` for sample usage

---

**Happy coding! 🚀**
