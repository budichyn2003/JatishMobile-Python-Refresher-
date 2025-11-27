"""
Example script demonstrating the Banking ETL Pipeline.

This script shows how to use the ETL modules to process banking transactions.
"""

import logging
from etl.loader import load_csv
from etl.validator import validate_transaction
from etl.cleaner import clean_transaction
from etl.transformer import transform_transaction

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def process_banking_transactions(csv_path: str, max_records: int = 10) -> None:
    """
    Process banking transactions through the ETL pipeline.
    
    Args:
        csv_path: Path to CSV file
        max_records: Maximum number of records to process (for demo)
    """
    logger.info("=" * 80)
    logger.info("BANKING ETL PIPELINE DEMO")
    logger.info("=" * 80)
    
    # Step 1: Load CSV
    logger.info("\n[1] LOADING CSV FILE...")
    try:
        transactions = load_csv(csv_path)
        logger.info(f"✓ Loaded {len(transactions)} transactions")
    except Exception as e:
        logger.error(f"✗ Failed to load CSV: {e}")
        return
    
    # Process first few transactions
    limit = min(max_records, len(transactions))
    logger.info(f"\n[2] PROCESSING {limit} TRANSACTIONS...")
    
    successful = 0
    failed = 0
    
    for idx, raw_txn in enumerate(transactions[:limit], 1):
        try:
            # Step 2: Validate
            validated = validate_transaction(raw_txn)
            
            # Step 3: Clean
            cleaned = clean_transaction(validated)
            
            # Step 4: Transform
            transformed = transform_transaction(cleaned)
            
            logger.info(f"\n✓ Transaction {idx}: {transformed['transaction_id']}")
            logger.info(f"  - Date: {transformed['transaction_date']} "
                       f"({transformed['transaction_day']})")
            logger.info(f"  - Amount: {transformed['amount']} {transformed['currency']}")
            logger.info(f"  - Large Transaction: {transformed['is_large_transaction']}")
            logger.info(f"  - Cross-border: {transformed['is_crossborder']}")
            logger.info(f"  - Risk Score: {transformed['risk_score']}")
            logger.info(f"  - Amount Log: {transformed['amount_log']:.2f}" 
                       if transformed['amount_log'] else f"  - Amount Log: N/A")
            
            successful += 1
        
        except Exception as e:
            logger.error(f"\n✗ Transaction {idx}: {type(e).__name__}: {e}")
            failed += 1
    
    # Summary
    logger.info("\n" + "=" * 80)
    logger.info("PROCESSING SUMMARY")
    logger.info("=" * 80)
    logger.info(f"Total Processed: {successful + failed}")
    logger.info(f"Successful: {successful}")
    logger.info(f"Failed: {failed}")
    logger.info(f"Success Rate: {(successful / (successful + failed) * 100):.1f}%")
    logger.info("=" * 80)


def demonstrate_async_api() -> None:
    """Demonstrate the async API functionality."""
    import asyncio
    from utils.async_api import fetch_quote, fetch_multiple_quotes
    
    async def demo():
        logger.info("\n" + "=" * 80)
        logger.info("ASYNC API DEMONSTRATION")
        logger.info("=" * 80)
        
        symbols = ['AAPL', 'GOOGL', 'MSFT']
        
        logger.info(f"\nFetching quotes for: {', '.join(symbols)}")
        logger.info("(Note: This will call dummyjson.com/quotes/random)")
        
        try:
            quotes = await fetch_multiple_quotes(symbols)
            
            logger.info(f"\n✓ Successfully fetched {len(quotes)} quotes:\n")
            for quote in quotes:
                logger.info(f"Symbol: {quote['symbol']}")
                logger.info(f"Quote: \"{quote['quote']}\"")
                logger.info(f"Author: {quote['author']}\n")
        
        except Exception as e:
            logger.warning(f"Could not fetch quotes (network may be unavailable): {e}")
        
        logger.info("=" * 80)
    
    try:
        asyncio.run(demo())
    except Exception as e:
        logger.warning(f"Async demo failed: {e}")


if __name__ == "__main__":
    # Process transactions
    process_banking_transactions('data/banking_transactions.csv', max_records=5)
    
    # Demonstrate async API
    demonstrate_async_api()
    
    logger.info("\n✓ Demo completed successfully!")
