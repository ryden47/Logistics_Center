from Supplier import Supplier


class _SuppliersDAO:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, supplier):
        self._conn.execute("""
                        INSERT INTO suppliers (id, name, logistic)
                        VALUES (?, ?, ?)
                        """, [supplier.id_s, supplier.name, supplier.logistic])

    def find(self, name_s):
        c = self._conn.cursor()
        c.execute("""
                SELECT * FROM suppliers WHERE name = ?
            """, [name_s])
        return Supplier(*c.fetchone())


suppliers_DAO = _SuppliersDAO(None)
