import sqlite3
import atexit

from Clinic import Clinic
from Logistic import Logistic
from Supplier import Supplier
from Vaccine import Vaccine
from _Summary import summary

from VaccincesDAO import vaccines_DAO
from SuppliersDAO import suppliers_DAO
from ClinicsDAO import clinics_DAO
from LogisticsDAO import logistics_DAO


class _PersistenceLayer:

    def __init__(self):
        self._conn = sqlite3.connect('database.db')
        vaccines_DAO._conn = self._conn
        suppliers_DAO._conn = self._conn
        clinics_DAO._conn = self._conn
        logistics_DAO._conn = self._conn

    def _close(self):
        self._conn.commit()
        self._conn.close()

    def create_tables(self):
        self._conn.executescript("""
                    CREATE TABLE IF NOT EXISTS logistics ( 
                        id INTEGER PRIMARY KEY, 
                        name STRING NOT NULL, 
                        count_sent INTEGER NOT NULL, 
                        count_received INTEGER NOT NULL 
                    );
                    CREATE TABLE IF NOT EXISTS clinics ( 
                        id INTEGER PRIMARY KEY, 
                        location STRING NOT NULL, 
                        demand INTEGER NOT NULL, 
                        logistic INTEGER REFERENCES logistics(id) 
                    );
                    CREATE TABLE IF NOT EXISTS suppliers ( 
                        id INTEGER PRIMARY KEY, 
                        name STRING NOT NULL, 
                        logistic INTEGER REFERENCES logistics(id) 
                    );
                    CREATE TABLE IF NOT EXISTS vaccines ( 
                        id INTEGER PRIMARY KEY, 
                        date DATE NOT NULL, 
                        supplier INTEGER REFERENCES suppliers(id), 
                        quantity INTEGER NOT NULL 
                    );
        """)
        print("Tables has been created.")

    def _create_vaccine_DTO(self, line):
        line = line.split(",")
        v_id = int(line[0])
        date = line[1]
        supplier = int(line[2])
        quantity = int(line[3])
        return Vaccine(v_id, date, supplier, quantity)

    def _create_supplier_DTO(self, line):
        line = line.split(",")
        id_s = int(line[0])
        name = line[1]
        logistics = int(line[2])
        return Supplier(id_s, name, logistics)

    def _create_clinic_DTO(self, line):
        line = line.split(",")
        id_c = int(line[0])
        location = line[1]
        demand = int(line[2])
        logistics = int(line[3])
        return Clinic(id_c, location, demand, logistics)

    def _create_logistic_DTO(self, line):
        line = line.split(",")
        id_l = int(line[0])
        name = line[1]
        count_sent = int(line[2])
        count_received = int(line[3])
        return Logistic(id_l, name, count_sent, count_received)

    def insert_vaccine(self, line):
        vaccine = self._create_vaccine_DTO(line)
        vaccines_DAO.insert(vaccine)
        summary.total_inventory += vaccine.quantity

    def insert_supplier(self, line):
        supplier = self._create_supplier_DTO(line)
        suppliers_DAO.insert(supplier)

    def insert_clinic(self, line):
        clinic = self._create_clinic_DTO(line)
        clinics_DAO.insert(clinic)
        summary.total_demand += clinic.demand

    def insert_logistic(self, line):
        logistic = self._create_logistic_DTO(line)
        logistics_DAO.insert(logistic)

    def receive_shipment(self, order):
        name, amount, date = order[0], int(order[1]), order[2]
        next_id = vaccines_DAO.next_available_id()
        supplier = suppliers_DAO.find(name)
        vaccine_string = str(next_id) + "," + str(date) + "," + str(supplier.id_s) + "," + str(amount)
        self.insert_vaccine(vaccine_string)
        logistics_DAO.update_receive(amount, supplier.id_s)
        summary.update_receive(amount)

    def send_shipment(self, order):
        location, amount = order[0], int(order[1])
        clinic = clinics_DAO.find(location)
        clinics_DAO.decrease_demand(amount, clinic.id_c)
        logistics_DAO.update_send(amount, clinic.logistic)
        vaccines_DAO.pull_out_of_inventory(amount)
        summary.update_send(amount)

    def print_summary(self):
        return summary.show_report()


psl = _PersistenceLayer()
atexit.register(psl._close)
