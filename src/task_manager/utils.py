class UniqueQueue:
    """Очередь, которая хранит только уникальные элементы"""

    def __init__(self):
        self._items = []
        self._set = set()

    def add(self, item):
        """Добавляет элемент, если его ещё нет в очереди"""
        if item not in self._set:
            self._items.append(item)
            self._set.add(item)

    def pop(self):
        """Удаляет и возвращает последний элемент (LIFO)"""
        if not self._items:
            return None
        item = self._items.pop()
        self._set.remove(item)
        return item

    def last(self):
        """Возвращает последний добавленный элемент"""
        if not self._items:
            return None
        return self._items[-1]

    def __len__(self):
        """Возвращает длину очереди"""
        return len(self._items)

    def __contains__(self, item):
        """Проверяет, есть ли элемент в очереди"""
        return item in self._set