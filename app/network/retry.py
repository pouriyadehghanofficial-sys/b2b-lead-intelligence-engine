"""Retry strategy and backoff logic"""

import time
import random
from typing import Optional, Callable, Any
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class BackoffStrategy(Enum):
    """Backoff strategies for retries"""
    LINEAR = "linear"
    EXPONENTIAL = "exponential"
    FIBONACCI = "fibonacci"
    RANDOM = "random"


class RetryStrategy:
    """Configurable retry strategy with various backoff algorithms"""
    
    def __init__(
        self,
        max_retries: int = 3,
        initial_delay: float = 1.0,
        backoff_factor: float = 2.0,
        max_delay: float = 60.0,
        strategy: BackoffStrategy = BackoffStrategy.EXPONENTIAL,
        jitter: bool = True,
    ):
        self.max_retries = max_retries
        self.initial_delay = initial_delay
        self.backoff_factor = backoff_factor
        self.max_delay = max_delay
        self.strategy = strategy
        self.jitter = jitter
    
    def calculate_delay(self, attempt: int) -> float:
        """Calculate delay for given attempt number"""
        if self.strategy == BackoffStrategy.LINEAR:
            delay = self.initial_delay * attempt
        elif self.strategy == BackoffStrategy.EXPONENTIAL:
            delay = self.initial_delay * (self.backoff_factor ** (attempt - 1))
        elif self.strategy == BackoffStrategy.FIBONACCI:
            delay = self._fibonacci_delay(attempt)
        elif self.strategy == BackoffStrategy.RANDOM:
            delay = random.uniform(self.initial_delay, self.initial_delay * attempt)
        else:
            delay = self.initial_delay
        
        # Apply jitter
        if self.jitter:
            delay = delay * (0.5 + random.random())
        
        # Cap at max delay
        return min(delay, self.max_delay)
    
    def _fibonacci_delay(self, attempt: int) -> float:
        """Calculate Fibonacci-based delay"""
        if attempt <= 1:
            return self.initial_delay
        a, b = self.initial_delay, self.initial_delay
        for _ in range(attempt - 1):
            a, b = b, a + b
        return a
    
    def execute(
        self,
        func: Callable,
        *args,
        on_retry: Optional[Callable] = None,
        on_failure: Optional[Callable] = None,
        **kwargs
    ) -> Any:
        """Execute function with retry logic"""
        last_exception = None
        
        for attempt in range(1, self.max_retries + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e
                
                if attempt <= self.max_retries:
                    delay = self.calculate_delay(attempt)
                    logger.warning(
                        f"Attempt {attempt} failed: {str(e)}. "
                        f"Retrying in {delay:.2f}s..."
                    )
                    
                    if on_retry:
                        on_retry(attempt, delay, e)
                    
                    time.sleep(delay)
                else:
                    logger.error(f"All {self.max_retries} retries failed: {str(e)}")
                    if on_failure:
                        on_failure(e)
        
        raise last_exception
