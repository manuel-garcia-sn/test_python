import unittest
from database.Items import crud
from database.models import Item


class TestDatabaseOperations(unittest.TestCase):
    base_item_name = 'Test Item '

    @classmethod
    def setUpClass(cls) -> None:
        crud.init()

        for x in range(100):
            crud.add_to_list(cls.base_item_name + str(x))

    # @classmethod
    # def tearDownClass(cls) -> None:
    #     database_operations.truncate_items()

    def test_insert(self):
        i = Item('Pepe1')
        result = crud.add_to_list(i.name)

        self.assertEqual(i.name, result.name)

    def test_search_in_list(self):
        item_to_search = self.base_item_name + str(10)
        res_data = crud.search_in_list(item_to_search)

        self.assertEqual(res_data.name, item_to_search)

    def test_delete_item(self):
        item_to_delete = self.base_item_name + str(50)

        crud.delete_item_list(item_to_delete)
        res_data = crud.search_in_list(item_to_delete)

        i = Item('Pepe 99')
        result = crud.add_to_list(i.name)

        self.assertEqual(res_data, None)

    def test_get_all_items(self):
        items = crud.get_all_items()

        self.assertEqual(items['count'], 100)

if __name__ == '__main__':
    unittest.main()
