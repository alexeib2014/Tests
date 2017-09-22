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

    def get_amount(self,sku):
        if sku not in self.inventory:
            return 0
        return self.inventory[sku]

    def get_name(self):
        return self.name


class Order(object):
    def __init__(self, sku, amount):
        """
        Create order to be fulfilled and shipped
        :param sku: SKU to be ordered (todo: list of SKU in one order)
        :param amount: amount of SKU
        """
        self.acknowledged = False  
        self.canceled = False
        self.shipped = False
        self.rejected = False
        self.tracking_number = ""
        self.sku = sku
        self.amount = amount
        self.warehouses = {}

    def __str__(self):
        tags = []
        if self.acknowledged:
            tags.append('acknowledged')
        if self.canceled:
            tags.append('canceled')
        if self.shipped:
            tags.append('shipped')
        if self.rejected:
            tags.append('rejected')
        return '<Order: %s[%i] %s>' % (self.sku, self.amount, ','.join(tags))


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

        We only acknowledge if we have enough inventory.
        """
        total_amount = 0
        for warehouse in self.warehouses:
            total_amount += warehouse.get_amount(order.sku)
        if total_amount >= order.amount :
            order.acknowledged = True
            return True
        else:
            order.rejected = True
            return False

    def ship_order(self, order, tracking_number):
        """
        At this point, the order has been shipped and seller has 
                determined which warehouse they will be shipping from.
        :param order: the order to ship
        :param tracking_number: Tracking Number of the shipment
        :return: True if Shipped False otherwise.
        """

        # Optimization: find single warehouse with enough amount
        for warehouse in self.warehouses:
            amount = warehouse.get_amount(order.sku)
            if order.amount <= amount:
                break
        if order.amount <= amount:
            warehouse.decrement(order.sku, order.amount)
            order.warehouses[warehouse.get_name()] = order.amount
            order.shipped = True
            order.tracking_number = tracking_number
            return order.shipped

        # Divide order for few warehouses
        order_amount = order.amount
        for warehouse in self.warehouses:
            amount = warehouse.get_amount(order.sku)
            if order_amount <= amount:
                warehouse.decrement(order.sku, order_amount)
                order.warehouses[warehouse.get_name()] = order_amount
                order.shipped = True
                order.tracking_number = tracking_number
                return order.shipped
            else:
                warehouse.decrement(order.sku, amount)
                order.warehouses[warehouse.get_name()] = amount
                order_amount -= amount

        self.cancel_order(order)
        return False
        
    def cancel_order(self, order):
        """
        Sometimes, seller cancels after he/she has acknowledged 
        the order.
        :param order: Order to Cancel
        :return: True if canceled False otherwise.
        """
        for warehouse in self.warehouses:
            warehouse_name = warehouse.get_name()
            if warehouse_name in order.warehouses:
                warehouse.increment(order.sku, order.warehouses[warehouse_name])
                del order.warehouses[warehouse_name]
        order.canceled = True
        return order.canceled


if __name__ == '__main__':
    wareHouseCalifornia = WareHouse('California')
    wareHouseCalifornia.increment('APP', 500)
    wareHouseCalifornia.increment('ORG', 200)

    wareHouseNewYork = WareHouse('New York')
    wareHouseNewYork.increment('APP', 1200)
    wareHouseNewYork.increment('ORG', 700)

    orderManager = OrderManager([wareHouseCalifornia, wareHouseNewYork])

    print('Test race conditions:')
    order1 = Order('ORG', 600)
    order2 = Order('ORG', 500)

    if orderManager.acknowledge_order(order1) and orderManager.acknowledge_order(order2):
        orderManager.ship_order(order1, 'track111')
        # Race condition: order acknowledged, but can not be shipped
        orderManager.ship_order(order2, 'track222')

    print(order1)
    print(order2)
