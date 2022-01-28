import db_connection
import logger

class DbContext:
    def __init__(self, cnn):
        self.logger = logger.Logger()
        self.cnn = cnn
        self.cursor = cnn.cursor()

    def get_max_id(self, table):
        self.cursor.execute(f"SELECT MAX(ID) FROM {table}")
        max_id = self.cursor.fetchone()
        if max_id[0] is None:
            return 0
        return max_id[0]

    def get_max_date_for_country(self, iso2):
        self.cursor.execute(
            f"SELECT MAX(DAY_DATE) FROM DAYS WHERE COUNTRY_ISO2 = '{iso2.upper()}'"
        )
        max_date = self.cursor.fetchone()
        if max_date[0] is None:
            return "2020-01-01"
        return max_date[0]

    def get_countries(self):
        countries = []
        self.cursor.execute("SELECT * FROM COUNTRIES")
        while True:
            row = self.cursor.fetchone()
            if row is None:
                break
            else:
                countries.append(row)
        return countries

    def get_country(self, iso2):
        self.cursor.execute(f"SELECT * FROM COUNTRIES WHERE ISO2 = '{iso2.upper()}'")
        result = self.cursor.fetchone()
        return result

    def get_days(self, iso2):
        days = []

        self.cursor.execute(
            f"SELECT * FROM DAYS WHERE COUNTRY_ISO2 = '{iso2.upper()}' ORDER BY DAY_DATE"
        )

        while True:
            row = self.cursor.fetchone()
            if row is None:
                break
            else:
                days.append(row)

        return days

    def get_days_by_month(self, iso2, year, month):
        days = []
        
        self.cursor.execute(
            f"SELECT * FROM DAYS WHERE COUNTRY_ISO2 = '{iso2.upper()}' AND EXTRACT(YEAR FROM DAY_DATE) = {year} AND EXTRACT(MONTH FROM DAY_DATE) = {month} ORDER BY DAY_DATE"
        )

        while True:
            row = self.cursor.fetchone()
            if row is None:
                break
            else:
                days.append(row)

        return days

    def add_death_mean(self, iso2, year, month, mean):
        self.logger.message("Adding death mean...")
        month = month if month < 10 else f"0{month}"
        try:
            self.cursor.execute(f"INSERT INTO DEATHS_MEANS VALUES ('{iso2}:{year}-{month}', {mean}, '{iso2}')")
            self.cnn.commit()
            self.logger.success(f"Rows added: {self.cursor.rowcount}")
        except BaseException as ex:
            self.logger.error(str(ex))