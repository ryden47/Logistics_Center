import sys

from _PersistenceLayer import psl


def insert_from_config(config_file):
    with open(config_file, 'r') as config:
        lines = config.readlines()
        first_line = (lines[0].split(","))
        first_line = [int(first_line) for first_line in first_line]
        line = iter(lines[1:])
        insert_vac, insert_sup, insert_clc, insert_log = [], [], [], []
        for t in range(first_line[0]):
            insert_vac.append(next(line))
        for t in range(first_line[1]):
            insert_sup.append(next(line))
        for t in range(first_line[2]):
            insert_clc.append(next(line))
        for t in range(first_line[3]):
            insert_log.append(next(line))
        for i in range(0, len(insert_log), 1):
            psl.insert_logistic(insert_log[i])
        for i in range(0, len(insert_clc), 1):
            psl.insert_clinic(insert_clc[i])
        for i in range(0, len(insert_sup), 1):
            psl.insert_supplier(insert_sup[i])
        for i in range(0, len(insert_vac), 1):
            psl.insert_vaccine(insert_vac[i])
        print("All insertions has been accomplished.")


def execute_orders(orders_file):
    with open(orders_file, 'r') as orders:
        orders = orders.readlines()
        for order in orders:
            order = order.split(",")
            if len(order) == 3:
                psl.receive_shipment(order)
            elif len(order) == 2:
                psl.send_shipment(order)
    print("Executed all orders successfully.")


def print_summary(output_txt):
    with open(output_txt, 'w') as output:
        output.write(psl.print_summary())
    print("output.txt file has been created.")


def main(args):
    psl.create_tables()
    insert_from_config(args[1])
    execute_orders(args[2])
    print_summary(args[3])


if __name__ == '__main__':
    main(sys.argv)
