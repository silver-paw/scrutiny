from dataclasses import dataclass
import time

class PollingTimeout(Exception):
    """This exception is raised when the configured timeout is reached"""
    pass

@dataclass
class Context:
    start_time : float
    timeout : float
    current_attempt : int = 0
    max_attempts : int = None
    interval : int = None

    def step(self) -> None:
        self.current_attempt += 1

    def timed_out(self) -> bool:
        return time.time() - self.start_time > self.timeout

    def maxed_attempts(self) -> bool:
        """Return False when there is no maximum attempt configured, or when the current attempt number is greater or equal to the configured target"""
        if self.max_attempts is None:
            return False
        return self.current_attempt >= self.max_attempts

    def should_continue_iterate(self) -> bool:
        return not self.timed_out() and not self.maxed_attempts()


class Polling:
    def __init__(self, timeout=60, max_attempts=None, interval=None) -> None:
        self._timeout = timeout
        self._max_attempts = max_attempts
        self._interval = interval

    def execute(self) -> None:
        context = Context(start_time=time.time(), timeout=self._timeout, max_attempts=self._max_attempts, interval=self._interval)
        while context.should_continue_iterate():
            context.step()
            yield context
            
            if not context.should_continue_iterate():
                break

            if self._interval:
                time.sleep(self._interval)

        if context.timed_out():
            raise PollingTimeout()
