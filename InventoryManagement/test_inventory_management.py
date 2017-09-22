import unittest
from inventory_management import WareHouse, Order, OrderManager


class OrderManagerTests(unittest.TestCase):
    def setUp(self):
        self.wareHouseCalifornia = WareHouse('California')
        self.wareHouseCalifornia.increment('APP', 500)
        self.wareHouseCalifornia.increment('ORG', 200)

        self.wareHouseNewYork = WareHouse('New York')
        self.wareHouseNewYork.increment('APP', 1200)
        self.wareHouseNewYork.increment('ORG', 700)

        self.orderManager = OrderManager([self.wareHouseCalifornia, self.wareHouseNewYork])

    def test_race_conditions(self):
        """
        Test race conditions
        """
        order1 = Order('ORG', 600)
        order2 = Order('ORG', 500)

        assert self.orderManager.acknowledge_order(order1)
        assert self.orderManager.acknowledge_order(order2)
        assert self.orderManager.ship_order(order1, 'track111')
        # Race condition: order acknowledged, but can not be shipped
        assert not self.orderManager.ship_order(order2, 'track222')

    def test_ship_order_small_amount(self):
        """
        Test small amount, so it can be shipped from first warehouse
        """
        order = Order('ORG', 200)
        self.assertTrue(self.orderManager.ship_order(order, 'track111'))
        assert order.warehouses['California'] == 200
        assert order.shipped
        assert self.wareHouseCalifornia.inventory['ORG'] == 0
        assert self.wareHouseNewYork.inventory['ORG'] == 700

    def test_ship_order_big_for_first_warehouse(self):
        """
        Test too big amount for the first warehouse and enough for second
        """
        order = Order('ORG', 500)
        self.assertTrue(self.orderManager.ship_order(order, 'track111'))
        assert order.warehouses['New York'] == 500
        assert order.shipped
        assert self.wareHouseCalifornia.inventory['ORG'] == 200
        assert self.wareHouseNewYork.inventory['ORG'] == 200

    def test_ship_order_for_both_warehouses(self):
        """
        Test ship from both warehouses
        """
        order = Order('ORG', 800)
        self.assertTrue(self.orderManager.ship_order(order, 'track111'))
        assert order.warehouses['California'] == 200
        assert order.warehouses['New York'] == 600
        assert order.shipped
        assert self.wareHouseCalifornia.inventory['ORG'] == 0
        assert self.wareHouseNewYork.inventory['ORG'] == 100

    def test_ship_order_too_big(self):
        """
        Test ship too big order
        """
        order = Order('ORG', 1000)
        self.assertFalse(self.orderManager.ship_order(order, 'track111'))
        assert order.warehouses == {}
        assert not order.shipped
        assert order.canceled
        assert self.wareHouseCalifornia.inventory['ORG'] == 200
        assert self.wareHouseNewYork.inventory['ORG'] == 700

    def test_acknowledge_order(self):
        """
        Test acknowledge_order method
        """
        order1 = Order('ORG', 200)        # test small amount
        self.assertTrue(self.orderManager.acknowledge_order(order1))

        order2 = Order('ORG', 900)        # test amount for two warehouses
        self.assertTrue(self.orderManager.acknowledge_order(order2))

        order3 = Order('ORG', 1000)       # test too big amount
        self.assertFalse(self.orderManager.acknowledge_order(order3))


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

    def test_get_amount(self):
        """
        Test get_amount method
        """
        self.assertEqual(self.wareHouseCalifornia.get_amount('APP'), 500)
        self.assertEqual(self.wareHouseCalifornia.get_amount('AAA'), 0)

    def test_get_name(self):
        """
        Test get_name method
        """
        self.assertEqual(self.wareHouseCalifornia.get_name(), 'California')

if __name__ == '__main__':
    unittest.main(exit=False)

