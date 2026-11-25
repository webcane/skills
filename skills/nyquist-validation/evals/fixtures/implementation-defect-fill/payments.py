class Payments:
    def __init__(self):
        self.rows = []

    def post(self, key, amount):
        operation = {"id": len(self.rows) + 1, "key": key, "amount": amount}
        self.rows.append(operation)
        return 200, operation["id"]
