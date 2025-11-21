import asyncio
from typing import Dict, Any, Callable, Optional
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class BackgroundWorker:
    def __init__(self, max_retries: int = 3, initial_delay: float = 1.0, max_delay: float = 60.0):
        self.tasks = set()
        self.max_retries = max_retries
        self.initial_delay = initial_delay
        self.max_delay = max_delay

    async def _execute_with_retry(self, task_func: Callable, *args, **kwargs) -> Any:
        """Execute a task with exponential backoff retry logic."""
        delay = self.initial_delay
        last_exception = None
        
        for attempt in range(self.max_retries + 1):
            try:
                return await task_func(*args, **kwargs)
            except Exception as e:
                last_exception = e
                if attempt < self.max_retries:
                    # Calculate next delay with exponential backoff and jitter
                    delay = min(self.initial_delay * (2 ** attempt), self.max_delay)
                    jitter = delay * 0.1  # 10% jitter
                    delay_with_jitter = delay + (jitter * (2 * (0.5 - 0.5)))
                    
                    logger.warning(
                        f"Attempt {attempt + 1} failed. Retrying in {delay_with_jitter:.2f} seconds. Error: {str(e)}"
                    )
                    await asyncio.sleep(delay_with_jitter)
                else:
                    logger.error(
                        f"Task failed after {self.max_retries} attempts. Error: {str(e)}"
                    )
                    raise last_exception

    async def add_task(self, task_func: Callable, *args, **kwargs) -> None:
        """Add a task to be executed in the background."""
        task = asyncio.create_task(
            self._execute_with_retry(task_func, *args, **kwargs)
        )
        self.tasks.add(task)
        task.add_done_callback(self.tasks.discard)

    async def shutdown(self, timeout: float = 30.0) -> None:
        """Gracefully shutdown the worker, waiting for pending tasks to complete."""
        if not self.tasks:
            return
            
        logger.info(f"Waiting for {len(self.tasks)} background tasks to complete...")
        done, pending = await asyncio.wait(
            self.tasks,
            timeout=timeout,
            return_when=asyncio.ALL_COMPLETED
        )
        
        if pending:
            logger.warning(f"Cancelling {len(pending)} pending tasks...")
            for task in pending:
                task.cancel()
            
            try:
                await asyncio.wait(pending, timeout=5.0)
            except asyncio.TimeoutError:
                logger.error("Timed out waiting for pending tasks to complete")

# Global worker instance
worker = BackgroundWorker()
