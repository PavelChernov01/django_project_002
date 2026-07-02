import unittest
from task_manager.utils import UniqueQueue


class TestUniqueQueue(unittest.TestCase):

    def setUp(self):
        self.queue = UniqueQueue()

    def test_add_unique(self):
        self.queue.add(1)
        self.assertEqual(len(self.queue), 1)

    def test_add_duplicate(self):
        self.queue.add(1)
        self.queue.add(1)
        self.assertEqual(len(self.queue), 1)

    def test_add_multiple_unique(self):
        self.queue.add(1)
        self.queue.add(2)
        self.queue.add(3)
        self.assertEqual(len(self.queue), 3)

    def test_last(self):
        self.queue.add(1)
        self.queue.add(2)
        self.assertEqual(self.queue.last(), 2)

    def test_last_empty(self):
        self.assertIsNone(self.queue.last())

    def test_len_empty(self):
        self.assertEqual(len(self.queue), 0)

    def test_lifo_order(self):
        self.queue.add(1)
        self.queue.add(2)
        self.queue.add(3)
        self.assertEqual(self.queue.pop(), 3)
        self.assertEqual(self.queue.pop(), 2)
        self.assertEqual(self.queue.pop(), 1)

    def test_pop_empty(self):
        self.assertIsNone(self.queue.pop())

    def test_contains(self):
        self.queue.add(1)
        self.assertTrue(1 in self.queue)
        self.assertFalse(2 in self.queue)