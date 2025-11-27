"""Async API utilities for banking ETL project."""

import asyncio
import logging
from functools import wraps
from typing import Callable, Any, Coroutine

import aiohttp

# Configure logging
logger = logging.getLogger(__name__)

MAX_RETRIES = 3
TIMEOUT_SECONDS = 10
API_ENDPOINT = "https://dummyjson.com/quotes/random"


def retry_on_failure(max_retries: int = MAX_RETRIES, timeout: int = TIMEOUT_SECONDS) -> Callable:
    """
    Decorator for retrying async functions on failure.
    
    Args:
        max_retries: Maximum number of retry attempts
        timeout: Timeout in seconds for each attempt
        
    Returns:
        Decorated function
    """
    def decorator(func: Callable[..., Coroutine]) -> Callable:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_exception = None
            
            for attempt in range(1, max_retries + 1):
                try:
                    logger.debug(
                        f"Attempting {func.__name__} (attempt {attempt}/{max_retries})"
                    )
                    result = await asyncio.wait_for(
                        func(*args, **kwargs),
                        timeout=timeout
                    )
                    logger.info(f"{func.__name__} succeeded on attempt {attempt}")
                    return result
                
                except asyncio.TimeoutError as e:
                    last_exception = e
                    logger.warning(
                        f"{func.__name__} timeout on attempt {attempt}/{max_retries}"
                    )
                    if attempt < max_retries:
                        await asyncio.sleep(1)  # Wait before retry
                
                except aiohttp.ClientError as e:
                    last_exception = e
                    logger.warning(
                        f"{func.__name__} client error on attempt {attempt}/{max_retries}: {e}"
                    )
                    if attempt < max_retries:
                        await asyncio.sleep(1)  # Wait before retry
                
                except Exception as e:
                    last_exception = e
                    logger.error(
                        f"{func.__name__} unexpected error on attempt {attempt}/{max_retries}: {e}"
                    )
                    if attempt < max_retries:
                        await asyncio.sleep(1)  # Wait before retry
            
            logger.error(
                f"{func.__name__} failed after {max_retries} attempts. "
                f"Last error: {last_exception}"
            )
            raise last_exception or Exception(
                f"{func.__name__} failed after {max_retries} attempts"
            )
        
        return wrapper
    return decorator


@retry_on_failure(max_retries=MAX_RETRIES, timeout=TIMEOUT_SECONDS)
async def fetch_quote(symbol: str) -> dict[str, Any]:
    """
    Fetch random quote from API with retry logic and timeout handling.
    
    Args:
        symbol: Symbol for the quote (used in response)
        
    Returns:
        Dictionary with symbol, quote, and author
        
    Raises:
        aiohttp.ClientError: If API request fails
        asyncio.TimeoutError: If request times out
    """
    if not symbol or not isinstance(symbol, str):
        raise ValueError(f"Invalid symbol: {symbol}")
    
    logger.info(f"Fetching quote for symbol: {symbol}")
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(API_ENDPOINT, ssl=False) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    result = {
                        "symbol": symbol,
                        "quote": data.get("quote", ""),
                        "author": data.get("author", "Unknown")
                    }
                    
                    logger.debug(f"Successfully fetched quote for {symbol}")
                    return result
                
                else:
                    error_msg = f"API returned status {response.status}"
                    logger.error(error_msg)
                    raise aiohttp.ClientError(error_msg)
        
        except aiohttp.ClientSSLError as e:
            logger.error(f"SSL error: {e}")
            raise
        except asyncio.TimeoutError as e:
            logger.error(f"Request timeout: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error fetching quote: {e}")
            raise


async def fetch_multiple_quotes(symbols: list[str]) -> list[dict[str, Any]]:
    """
    Fetch multiple quotes concurrently.
    
    Args:
        symbols: List of symbols to fetch quotes for
        
    Returns:
        List of quote dictionaries
    """
    logger.info(f"Fetching {len(symbols)} quotes concurrently")
    
    tasks = [fetch_quote(symbol) for symbol in symbols]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Filter out exceptions
    quotes = []
    for result in results:
        if isinstance(result, dict):
            quotes.append(result)
        else:
            logger.warning(f"Error fetching quote: {result}")
    
    logger.info(f"Successfully fetched {len(quotes)} quotes")
    return quotes
