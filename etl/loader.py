"""CSV loader module for banking transactions."""

import csv
import logging
from pathlib import Path
from typing import Any

# Configure logging
logger = logging.getLogger(__name__)


# Custom Exceptions
class CSVFileNotFoundError(Exception):
    """Raised when CSV file is not found."""
    pass


class CSVEmptyRowError(Exception):
    """Raised when empty rows are detected."""
    pass


class CSVColumnMismatchError(Exception):
    """Raised when CSV has wrong number of columns."""
    pass


class CSVMissingMandatoryFieldError(Exception):
    """Raised when mandatory columns are missing."""
    pass


def load_csv(path: str) -> list:
    """
    Load CSV file and convert to list of dictionaries.
    
    Args:
        path: Path to CSV file
        
    Returns:
        List of dictionaries containing CSV data
        
    Raises:
        CSVFileNotFoundError: If file doesn't exist
        CSVMissingMandatoryFieldError: If mandatory columns are missing
        CSVColumnMismatchError: If row has wrong column count
        CSVEmptyRowError: If empty rows are detected
    """
    mandatory_columns = {
        'transaction_id',
        'transaction_date',
        'customer_id',
        'account_id',
        'amount',
        'currency'
    }
    
    # Check if file exists
    file_path = Path(path)
    if not file_path.exists():
        logger.error(f"CSV file not found: {path}")
        raise CSVFileNotFoundError(f"File not found: {path}")
    
    logger.info(f"Loading CSV from: {path}")
    
    rows = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            
            # Check if headers exist
            if reader.fieldnames is None:
                logger.error("CSV file has no headers")
                raise CSVMissingMandatoryFieldError("CSV file has no headers")
            
            # Check mandatory columns
            headers_set = set(reader.fieldnames)
            missing_columns = mandatory_columns - headers_set
            
            if missing_columns:
                logger.error(f"Missing mandatory columns: {missing_columns}")
                raise CSVMissingMandatoryFieldError(
                    f"Missing mandatory columns: {missing_columns}"
                )
            
            logger.info(f"CSV headers verified. Found columns: {reader.fieldnames}")
            
            # Read rows
            for row_num, row in enumerate(reader, start=2):  # start=2 because row 1 is header
                # Check for empty rows
                if not any(row.values()):
                    logger.warning(f"Empty row detected at line {row_num}")
                    raise CSVEmptyRowError(f"Empty row detected at line {row_num}")
                
                # Check column count
                if len(row) != len(reader.fieldnames):
                    logger.error(
                        f"Row {row_num} has {len(row)} columns, "
                        f"expected {len(reader.fieldnames)}"
                    )
                    raise CSVColumnMismatchError(
                        f"Row {row_num} has wrong column count"
                    )
                
                rows.append(row)
            
            logger.info(f"Successfully loaded {len(rows)} rows from CSV")
            return rows
    
    except (CSVFileNotFoundError, CSVEmptyRowError, CSVColumnMismatchError, 
            CSVMissingMandatoryFieldError):
        raise
    except Exception as e:
        logger.error(f"Unexpected error reading CSV: {e}")
        raise
