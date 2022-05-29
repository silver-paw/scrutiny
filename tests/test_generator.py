import time
import unittest

from scrutiny.generator import Polling, PollingTimeout


class TestPolling(unittest.TestCase):
    """Test the Polling object"""

    def test_polling_class_create_instance(self) -> None:
        Polling()
        Polling(3)

    def test_polling_class_execute_returns_not_none(self) -> None:
        poll = Polling()
        val = poll.execute()
        self.assertIsNotNone(val)

    def test_polling_timeout_default(self) -> None:
        poll = Polling()
        start_time = time.time()
        with self.assertRaises(PollingTimeout):
            for attempt in poll.execute():
                pass
        self.assertAlmostEqual(time.time() - start_time, 60, delta=0.1)

    def test_polling_timeout_5s(self) -> None:
        poll = Polling(timeout=5)
        start_time = time.time()
        with self.assertRaises(PollingTimeout):
            for attempt in poll.execute():
                pass
        self.assertAlmostEqual(time.time() - start_time, 5, delta=0.1)

    def test_polling_3_attempts(self) -> None:
        poll = Polling(max_attempts=3)
        count = 0
        for attempt in poll.execute():
            count += 1

        self.assertEqual(count, 3)

    def test_polling_5_attempt(self) -> None:
        poll = Polling(max_attempts=5)
        count = 0
        for attempt in poll.execute():
            count += 1

        self.assertEqual(count, 5)

    def test_polling_interval_3x1s(self) -> None:
        poll = Polling(max_attempts=3, interval=1)
        start_time = time.time()
        for attempt in poll.execute():
            pass
        self.assertGreaterEqual(time.time() - start_time, (3 - 1) * 1)

    def test_polling_interval_default(self) -> None:
        poll = Polling(max_attempts=3)
        start_time = time.time()
        for attempt in poll.execute():
            pass
        self.assertLess(time.time() - start_time, 0.1)

    def test_polling_interval_5x2s(self) -> None:
        poll = Polling(max_attempts=5, interval=2)
        start_time = time.time()
        for attempt in poll.execute():
            pass
        self.assertGreaterEqual(time.time() - start_time, (5 - 1) * 2)

    def test_timeout_10s_with_2s_interval(self):
        poll = Polling(timeout=10, interval=2)
        start_time = time.time()
        count = 0
        with self.assertRaises(PollingTimeout):
            for attempt in poll.execute():
                count += 1

        self.assertAlmostEqual(time.time() - start_time, 10, delta=0.1)
        self.assertEqual(count, 5)
