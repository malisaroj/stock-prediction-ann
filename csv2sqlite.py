import sqlite3
import csv


class Database:
    def __init__(self, **kwargs):
        self.filename = kwargs.get('filename', 'data.db')
        self.tablename = kwargs.get('tablename')
        self.CreateTable()


# conn = sqlite3.connect("data.db")
# c = conn.cursor()

    def CreateTable(self):

        if self.tablename == 'data_table':
            cmd = """CREATE TABLE IF NOT EXISTS data_table ('Date' NUMERIC PRIMARY KEY, 'Total Transactions' INT, 'Traded Shares' REAL, 'TotalTraded Amount' REAL, 'Maximum Price' REAL, 'Minimum Price' REAL, 'Closing Price' REAL)"""
        self.db.execute(cmd)

        self.db.commit()

    def GetTable(self):
        self.CreateTable()
        return self.db.execute('SELECT * FROM {}'.format(self.tablename))

    def __iter__(self):
        cursor = self.db.execute('SELECT * FROM {}'.format(self.tableName))
        for row in cursor:
            yield dict(row)

    @property
    def filename(self): return self._filename

    @filename.setter
    def filename(self, fn):
        self._filename = fn
        self.db = sqlite3.connect(fn)
        self.db.row_factory = sqlite3.Row

    @filename.deleter
    def filename(self):
        self.db.close()

# c.execute("""CREATE TABLE IF NOT EXISTS data_table ('Date' NUMERIC PRIMARY KEY, 'Total Transactions' INT, 'Traded Shares' REAL, 'TotalTraded Amount' REAL, 'Maximum Price' REAL, 'Minimum Price' REAL, 'Closing Price' REAL)""")
    def insert(self, **kwargs):
        if self.tablename == 'data_table':
            with open('ADBL.csv', 'r') as data_table:
                dr = csv.DictReader(data_table, delimiter=',')
                to_db = [(i['Date'], i['Total Transactions'], i['Traded Shares'], i['TotalTraded Amount'], i['Maximum Price'], i['Minimum Price'], i['Closing Price']) for i in dr]
            self.db.executemany("INSERT INTO data_table VALUES (?,?,?,?,?,?,?);", to_db)

        self.db.commit()


def main():
    ser = Database(filename='data.db', tablename='data_table')
    ser.insert(tablename='data_table')
    print('ok')


if __name__ == '__main__':
    main()
# with open('ADBL.csv', 'r') as data_table:
#     dr = csv.DictReader(data_table, delimiter=',')
#     to_db = [(i['Date'], i['Total Transactions'], i['Traded Shares'], i['TotalTraded Amount'], i['Maximum Price'], i['Minimum Price'], i['Closing Price']) for i in dr]

# c.executemany("INSERT INTO data_table VALUES (?,?,?,?,?,?,?);", to_db)
# conn.commit()
# conn.close()

# Select statment to query the db
# cursor = c.execute("Select * from person order by lastName")
# for row in cursor:
#     print("ID = ", row[0])
#     print("Last Name = ", row[1])
#     print("First Name = ", row[2])
#     print("Phone Number = ", row[7], "\n")
