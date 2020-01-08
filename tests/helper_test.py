import unittest
import database_operations


class TestSum(unittest.TestCase):
    def test_add_to_list(self):
        item = {"item": 'Test Item 2', "status": database_operations.NOT_STARTED}
        res_data = database_operations.add_to_list(item["item"])

        self.assertEqual(res_data, item)


if __name__ == '__main__':
    unittest.main()
