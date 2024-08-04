import multiprocessing


class WarehouseManager:
    def __init__(self):
        self.data = multiprocessing.Manager().dict()

    def process_request(self, request):
        product, action, amount = request
        if product in self.data:
            if action == 'receipt':
                self.data[product] += amount
            elif action == 'shipment':
                if amount < self.data[product]:
                    self.data[product] -= amount
        else:
            self.data[product] = amount

    def run(self, requests):
        processes = []
        for request in requests:
            processes.append(multiprocessing.Process(target=self.process_request, args=(request,)))
        for i in processes:
            i.start()
        for i in processes:
            i.join()


if __name__ == '__main__':
    manager = WarehouseManager()

    requests1 = [
        ("product1", "receipt", 100),
        ("product2", "receipt", 150),
        ("product1", "shipment", 30),
        ("product3", "receipt", 200),
        ("product2", "shipment", 50)
    ]
    manager.run(requests1)
    print(manager.data)
