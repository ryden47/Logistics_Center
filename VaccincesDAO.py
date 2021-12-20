from Vaccine import Vaccine


class _VaccinesDAO:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, vaccine):
        self._conn.execute("""
                        INSERT INTO vaccines (id, date, supplier, quantity)
                        VALUES (?, ?, ?, ?)
                        """, [vaccine.id_v, vaccine.date, vaccine.supplier, vaccine.quantity])

    def next_available_id(self):
        c = self._conn.cursor()
        m = c.execute("""
                        SELECT MAX(id) AS Maximum
                        FROM vaccines
                        """).fetchone()
        if m[0] is None:
            return 1
        return m[0] + 1

    def last_added_vaccine(self):
        c = self._conn.cursor()
        record = c.execute("""
                                SELECT * FROM vaccines
                                ORDER BY date limit 1
                                """).fetchone()
        return Vaccine(*record)

    def pull_out_of_inventory(self, amount):
        while amount != 0:
            oldest_vaccine = self.last_added_vaccine()
            new_quantity = oldest_vaccine.quantity - amount
            if new_quantity <= 0:  # delete row
                amount -= oldest_vaccine.quantity
                self._conn.execute("""
                            DELETE FROM vaccines WHERE id = ?
                            """, [oldest_vaccine.id_v])
            else:
                amount = 0
                self._conn.execute("""
                            UPDATE vaccines SET quantity = ?
                            WHERE id = ?
                            """, [new_quantity, oldest_vaccine.id_v])


vaccines_DAO = _VaccinesDAO(None)
