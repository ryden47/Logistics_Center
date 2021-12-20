class _Summary:

    def __init__(self):
        self.total_inventory = 0
        self.total_demand = 0
        self.total_received = 0
        self.total_sent = 0
        self.output_file = []

    def add_to_report(self):
        add = "{},{},{},{}".format(self.total_inventory, self.total_demand, self.total_received, self.total_sent)
        self.output_file.append(add)

    def update_receive(self, amount):
        self.total_received += amount
        self.add_to_report()

    def update_send(self, amount):
        self.total_inventory -= amount
        self.total_demand -= amount
        self.total_sent += amount
        self.add_to_report()

    def show_report(self):
        output = '\n'.join(self.output_file)
        output += "\n"
        return output


summary = _Summary()
