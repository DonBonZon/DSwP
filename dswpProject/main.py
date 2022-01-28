import db_migrator
import db_context
import db_connection
import statistics
import charts
import logger

connection = db_connection.connect_to_db()

migrator = db_migrator.DbMigrator(connection)
context = db_context.DbContext(connection)
stats = statistics.Statistics(context)
charts = charts.Charts(context)

# migrator.clear_db()
# migrator.migrate_countries()
# migrator.migrate_days()

# print("Basic info for Poland")
# stats.getBasicInfo("PL")
# print("Mean of deaths at 11.2021 in Poland")
# stats.getMeanOfDeathsInMonth("PL",2021,11)
# print("Test for notmal distribution for Poland")
# stats.testNormalDistribution("PL")
# print("Test for variance equality for Poland")
# stats.testWarianceEquality("PL","New_cases","New_deaths")
# stats.testMulipleMeans("PL")

# charts.plot_confirmed_cases('PL')
# stats.makeRegresion('PL')
# charts.plot_new_deaths('CH')
charts.plot_new_cases('IT')
