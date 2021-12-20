class _LogisticsDAO:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, logistic):
        self._conn.execute("""
                        INSERT INTO logistics (id, name, count_sent, count_received)
                        VALUES (?, ?, ?, ?)
                        """, [logistic.id_l, logistic.name, logistic.count_sent, logistic.count_received])

    def update_receive(self, amount, id_s):
        self._conn.execute("""
                        UPDATE logistics SET count_received = count_received + ?
                        WHERE id = ?
                        """, [amount, id_s])

    def update_send(self, amount, id_l):
        self._conn.execute("""
                        UPDATE logistics SET count_sent = count_sent + ?
                        WHERE id = ?
                        """, [amount, id_l])


logistics_DAO = _LogisticsDAO(None)
