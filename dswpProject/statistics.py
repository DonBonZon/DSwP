import numpy as np
import pandas as pd
from scipy.stats import shapiro, levene, f_oneway
from statsmodels.api import OLS,add_constant

import charts
import db_context
import db_connection
connection = db_connection.connect_to_db()
context = db_context.DbContext(connection)

class Statistics:

    def __init__(self, context):
        self.context = context
        self.charts = charts.Charts(context)

    def covertToDf(self,target):
        return  pd.DataFrame(
            target,
            columns=["DAY_ID", "Date", "Confirmed_cases", "Active_cases", "Deaths", "New_cases", "New_deaths", "ISO2"],
        )

    def getBasicInfo(self,ISO2):
        data = self.context.get_days(ISO2)
        df = self.covertToDf(data)
        print("Dataframe data:")
        print(df)
        print("Basic stats:")
        print(df.describe())

    def getMeanOfDeathsInMonth(self,ISO2,year,month):
        data = self.context.get_days_by_month(ISO2,year,month)
        df = self.covertToDf(data)
        print(df)
        mean = df['New_deaths'].mean()
        print(mean)
        self.context.add_death_mean(ISO2, year, month, mean)
    
    def testNormalDistribution(self,ISO2):
        data = self.context.get_days(ISO2)
        df = self.covertToDf(data)
        targets = ["Confirmed_cases","Active_cases","Deaths","New_cases","New_deaths"]
        for target in targets:
            stat, p = shapiro(df[target])
            print(f"{target}:   stat={stat} p={p}")

    def testWarianceEquality(self,ISO2,col1,col2):
        data = self.context.get_days(ISO2)
        df = self.covertToDf(data)
        stat, p = levene(df[col1],df[col2])
        print(f"For {col1} and {col2}: stat={stat} p={p}")

    def testMulipleMeans(self,ISO2):
        data = self.context.get_days(ISO2)
        df = self.covertToDf(data)
        targets = ["Active_cases","DAY_ID","Deaths"]
        stat, p = f_oneway(df[targets[0]],df[targets[1]],df[targets[2]])
        print(f"ANOVA")
        print(f"stat={stat} p={p}")

    def makeRegresion(self,ISO2):
        data = self.context.get_days(ISO2)
        df = self.covertToDf(data)
        X = df['Date']
        test_list = [int(i) for i in range(len(X))]
        Y = df['Deaths']
        X = add_constant(X)
        model = OLS(Y, test_list).fit()
        prediction = model.predict(test_list)
        print(model.summary())
        print(prediction)

        self.charts.plot_regression(df,test_list,'Deaths')
