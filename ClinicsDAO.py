from Clinic import Clinic


class _ClinicsDAO:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, clinic):
        self._conn.execute("""
                        INSERT INTO clinics (id, location, demand, logistic)
                        VALUES (?, ?, ?, ?)
                        """, [clinic.id_c, clinic.location, clinic.demand, clinic.logistic])

    def find(self, location):
        c = self._conn.cursor()
        c.execute("""
                    SELECT * FROM clinics WHERE location = ?
                    """, [location])
        return Clinic(*c.fetchone())

    def decrease_demand(self, amount, id_c):
        self._conn.execute("""
                        UPDATE clinics SET demand = demand - ?
                        WHERE id = ?
                        """, [amount, id_c])


clinics_DAO = _ClinicsDAO(None)
