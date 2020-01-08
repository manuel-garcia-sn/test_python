import unittest

import database_operations


class TestDatabaseOperations(unittest.TestCase):
    item = {"item": 'Test Item 1000', "status": database_operations.NOT_STARTED}
    base_item_name = 'Test Item '

    @classmethod
    def setUpClass(cls) -> None:
        database_operations.truncate_items()

        for x in range(100):
            database_operations.add_to_list(cls.base_item_name + str(x))

    # @classmethod
    # def tearDownClass(cls) -> None:
    #     database_operations.truncate_items()

    def test_add_to_list(self):
        res_data = database_operations.add_to_list(self.item["item"])

        self.assertEqual(res_data, self.item)

    def test_search_in_list(self):
        item_to_search = self.base_item_name + str(10)
        res_data = database_operations.search_in_list(item_to_search)

        self.assertEqual(res_data["item"], item_to_search)

    def test_delete_item(self):
        item_to_delete = self.base_item_name + str(50)

        database_operations.delete_item_list(item_to_delete)
        res_data = database_operations.search_in_list(item_to_delete)

        self.assertEqual(res_data, None)

    def test_get_all_items(self):
        items = database_operations.get_all_items()

        self.assertEqual(items['count'], 100)


if __name__ == '__main__':
    unittest.main()
