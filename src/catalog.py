from src.exceptions import DuplicateIDError, NotFoundObjectError


class AircraftCatalog:
    def __init__(self):
        self._items = []
        self._items_by_id = {}

    def add(self, item):
        if item.id in self._items_by_id:
            raise DuplicateIDError("Дубликат ID")
        self._items.append(item)
        self._items_by_id[item.id] = item

    def get(self, item_id):
        if item_id not in self._items_by_id:
            raise NotFoundObjectError("ID нет в каталоге")
        return self._items_by_id[item_id]

    def remove(self, item_id):
        if item_id not in self._items_by_id:
            raise NotFoundObjectError("ID нет в каталоге")
        item = self._items_by_id[item_id]
        self._items.remove(item)
        self._items_by_id.pop(item_id)

    def find_by_category(self, category):
        result = []
        for item in self._items:
            if category == item.category:
                result.append(item)
        return result

    def find_by_name(self, query):
        result = []
        for item in self._items:
            if query.lower() in item.name.lower():
                result.append(item)
        return result

    def __len__(self):
        return len(self._items)

    def __iter__(self):
        return iter(self._items)

    def __contains__(self, item_id):
        return item_id in self._items_by_id
