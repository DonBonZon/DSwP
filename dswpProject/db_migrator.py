import db_connection
import db_context
import logger
import covid_api
import json
from time import sleep
from datetime import datetime


class DbMigrator:
    def __init__(self, cnn):
        self.logger = logger.Logger()
        self.cnn = cnn
        self.cursor = cnn.cursor()
        self.context = db_context.DbContext(cnn)

    def clear_db(self):
        self.logger.message("Clearing database...")
        deletedRows = 0
        
        try:
            self.cursor.execute("DELETE FROM DAYS")
            deletedRows = deletedRows + int(self.cursor.rowcount)
            self.cursor.execute("DELETE FROM DEATHS_MEANS")
            deletedRows = deletedRows + int(self.cursor.rowcount)
            self.cursor.execute("DELETE FROM COUNTRIES")
            deletedRows = deletedRows + int(self.cursor.rowcount)
            self.cnn.commit()
        except BaseException as ex:
            self.logger.error(str(ex))

        self.logger.success(f"Rows deleted: {deletedRows}")

    def migrate_countries(self):
        self.logger.message("Migrating countries...")
        
        countries = json.loads(covid_api.get_countries().content)
        x = countries[0]

        data = []
        for country in countries:
            data.append((country["Country"], country["ISO2"]))

        try:
            self.cursor.executemany("INSERT INTO Countries VALUES (:1, :2)", data)
            self.cnn.commit()
        except BaseException as ex:
            self.logger.error(str(ex))

        self.logger.success(f"Countries added: {self.cursor.rowcount}")

    def migrate_days(self):
        self.logger.message("Migrating days...")

        # wyciagamy kraje z bazy
        countries = self.context.get_countries()

        # sprawdzamy czy cos jest w tabeli countries
        if len(countries) < 1:
            self.logger.error("No countries in database")
            return

        data = []
        max_id = self.context.get_max_id("DAYS")
        current_id = max_id

        # foreach country in coutries
        for country in countries:
            if country[1] == "US":
                continue

            self.logger.message(f"Getting days for {country[0]} ({country[1]})...")
            days = json.loads(covid_api.get_days(country[1]).content)
            sleep(0.4)

            if len(days) < 1:
                self.logger.warning(f"No data for {country[0]} ({country[1]})")
                continue

            # tylko dni z data wieksza od maksymalnej w bazie
            max_date = datetime.strptime(
                self.context.get_max_date_for_country(country[1]), "%Y-%M-%d"
            )
            filtered_days = filter(
                lambda day: datetime.strptime(day["Date"][0:10], "%Y-%M-%d") > max_date,
                days,
            )

            for day in filtered_days:
                data.append(
                    (
                        0,
                        day["Date"][0:10],
                        day["Confirmed"],
                        day["Active"],
                        day["Deaths"],
                        0,
                        0,
                        day["CountryCode"],
                    )
                )

        self.logger.message("Preparing data...")

        countryDict = {}
        for d in data:
            if d[7] not in countryDict.keys():
                countryDict[d[7]] = {}
            if d[1] not in (countryDict[d[7]]).keys():
                countryDict[d[7]][d[1]] = []
            countryDict[d[7]][d[1]].append(d)

        for key in countryDict.keys():
            for date in countryDict[key]:
                current_id = current_id + 1
                arr = countryDict[key][date]
                countryDict[key][date] = (
                    current_id,
                    date,
                    sum(x[2] for x in arr),
                    sum(x[3] for x in arr),
                    sum(x[4] for x in arr),
                    0,
                    0,
                    key,
                )

        # print(countryDict)
        prepared_data = []
        for key in countryDict.keys():
            for i in range(len(countryDict[key])):
                date = list(countryDict[key].keys())[i]
                # print(countryDict[key][date])
                if i != 0:
                    prev_date = list(countryDict[key].keys())[i-1]
                    new_cases = countryDict[key][date][2] - countryDict[key][prev_date][2]
                    new_deaths = countryDict[key][date][4] - countryDict[key][prev_date][4]
                else:
                    new_cases = countryDict[key][date][2]
                    new_deaths = countryDict[key][date][4]

                prepared_data.append(
                    (
                        countryDict[key][date][0], # id
                        countryDict[key][date][1], # data
                        countryDict[key][date][2], # confirmed
                        countryDict[key][date][3], # active
                        countryDict[key][date][4], # deaths
                        new_cases,
                        new_deaths,
                        countryDict[key][date][7], # iso
                    )
                )

        self.logger.message("Data prepared")

        # print(len(prepared_data))
        # for d in prepared_data:
        #     print(d)
        try:
            self.cursor.executemany(
                "INSERT INTO DAYS VALUES(:1, TO_DATE(:2,'YYYY-MM-DD'), :3, :4, :5, :6, :7, :8)",
                prepared_data,
            )
            self.cnn.commit()
        except BaseException as ex:
            self.logger.error(str(ex))

        self.logger.success(f"Rows added: {self.cursor.rowcount}")
