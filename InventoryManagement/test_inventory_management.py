import unittest
from inventory_management import WareHouse, Order, OrderManager


class WareHouseTests(unittest.TestCase):
    def setUp(self):
        self.wareHouseCalifornia = WareHouse('California')
        self.wareHouseCalifornia.increment('APP', 500)
        self.wareHouseCalifornia.increment('ORG', 200)

    def test_name(self):
        """
        Test stored name
        """
        assert self.wareHouseCalifornia.name == 'California'

    def test_increment(self):
        """
        Test increment method
        """
        assert self.wareHouseCalifornia.inventory['APP'] == 500
        self.assertTrue(self.wareHouseCalifornia.increment('APP', 100))
        assert self.wareHouseCalifornia.inventory['APP'] == 600

    def test_decrement(self):
        """
        Test decrement method
        """
        assert self.wareHouseCalifornia.inventory['APP'] == 500
        self.assertTrue(self.wareHouseCalifornia.decrement('APP', 100))
        assert self.wareHouseCalifornia.inventory['APP'] == 400
        self.assertFalse(self.wareHouseCalifornia.decrement('APP', 500))
        assert self.wareHouseCalifornia.inventory['APP'] == 400
        self.assertFalse(self.wareHouseCalifornia.decrement('AAA', 100))


if __name__ == '__main__':
    unittest.main(exit=False)

