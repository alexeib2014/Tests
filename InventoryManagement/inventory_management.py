class WareHouse(object):
    def __init__(self, name):
        self.name = name   # the name of the warehouse
        self.inventory = {}  # dictionary that maps SKU to Quantity

    def increment(self, sku, amount=1):
        """
        This increments the inventory for the given SKU in this 
        warehouse.
        :param sku: The SKU to increment from.
        :param amount: The amount to increment.
        """

        if sku not in self.inventory:
            self.inventory[sku] = 0

        self.inventory[sku] += amount
        return True

    def decrement(self, sku, amount=1):
        """
        This decrement the inventory for the given SKU in this 
        warehouse.
        :param sku: The SKU to decrement from.
        :param amount: The amount to decrement.
        """
        if sku not in self.inventory: 
            # self.inventory[sku] = 0 # we should not add new inventory on decrement procedure
            return False

        if self.inventory[sku] < amount:
            return False  # can decrement below zero. This is an error.

        self.inventory[sku] -= amount
        return True


class Order(object):
    def __init__(self, sku, amount):
        """
        Create order to be fulfilled and shipped
        :param sku: SKU to be ordered (todo: list of SKU to one order)
        :param amount: amount of SKU
        """
        self.acknowledged = False  
        self.canceled = False
        self.shipped = False
        self.rejected = False
        self.tracking_number = ""
        self.sku = ''
        self.amount = 0
        self.warehouses = {}


class OrderManager(object):
    def __init__(self, warehouses):
        # dictionary that maps warehouse name to warehouse object
        self.warehouses = warehouses

    def acknowledge_order(self, order):
        """
        :param order: the order to acknowledge
        :return: True if Acknowledged False otherwise.

        At this point, the seller has acknowledged that they will 
        ship the order. However, the we do not know which warehouse 
        it will be shipped from.

        We only acknowledge if we have enough inventory. Fix the 
        code below to only acknowledge when inventory is available 
        in any warehouse. Perform any inventory management you need
        to do.
        """
        if True:
            order.acknowledged = True
            return True
        else:
            order.rejected = True
            return False

    def pack_order(self, order):
        """
        Pack the order on warehouse(s)
        :param order:
        :return:
        """
        return True

    def ship_order(self, order, tracking_number, warehouse_name):
        """
        At this point, the order has been shipped and seller has 
                determined which warehouse they will be shipping from.
        :param order: the order to ship
        :param tracking_number: Tracking Number of the shipment
        :param warehouse_name: Name of WareHouse it was Shipped From.
        :return: True if Shipped False otherwise.

        Perform any inventory management you need to do here.
        """
        order.shipped = True
        order.tracking_number = tracking_number
        return order.shipped
        
    def cancel_order(self, order):
        """
        Sometimes, seller cancels after he/she has acknowledged 
        the order.
        :param order: Order to Cancel
        :return: True if canceled False otherwise.

        Perform any inventory management you need to do here.
        """
        order.canceled = True
        return order.canceled


if __name__ == '__main__':
    wareHouseCalifornia = WareHouse('California')
    wareHouseCalifornia.increment('APP', 500)
    wareHouseCalifornia.increment('ORG', 200)

    wareHouseNewYork = WareHouse('NewYork')
    wareHouseNewYork.increment('APP', 1200)
    wareHouseNewYork.increment('ORG', 700)

    orderManager = OrderManager([wareHouseCalifornia, wareHouseNewYork])
    pass
