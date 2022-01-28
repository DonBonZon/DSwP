import matplotlib.pyplot as plt
import seaborn as sns

class Charts:
    def __init__(self, context):
        self.context = context

    def maximum(self, vec):
        m = 0
        index = 0
        i = 0
        while i < len(vec):
            if vec[i] > m:
                m = vec[i]
                index = i
            i += 1
        return m, index

    def plot_confirmed_cases(self, iso2):
        days = self.context.get_days(iso2)
        
        dates = [x[1] for x in days] 
        confirmed_cases = [x[5] for x in days]
       
        plt.plot(dates, confirmed_cases, 'gray')

        plt.title(f'Confirmed cases of COVID-19 plot ({iso2})')
        plt.xlabel('Date')
        plt.ylabel('Number of confirmed cases')
        plt.legend(['confirmed cases'], loc='upper left')
        plt.grid(True, axis = 'y')
        plt.xticks(dates[::140])  

        plt.show()

    def plot_new_cases(self, iso2):
        days = self.context.get_days(iso2)
        
        dates = [x[1] for x in days] 
        new_cases = [x[5] for x in days]

        globalMax = self.maximum(new_cases)
       
        plt.plot(dates, new_cases, 'gray')
        plt.plot(dates[globalMax[1]], new_cases[globalMax[1]], 'ro') # global maximum

        plt.title(f'New cases of COVID-19 plot ({iso2})')
        plt.xlabel('Date')
        plt.ylabel('Number of new cases')
        plt.legend(['new cases', f'global max = {new_cases[globalMax[1]]}'], loc='upper left')
        plt.grid(True, axis = 'y')
        plt.xticks(dates[::140])  

        plt.show()

    def plot_new_deaths(self, iso2):
        days = self.context.get_days(iso2)
        
        dates = [x[1] for x in days] 
        new_deaths = [x[6] for x in days]

        globalMax = self.maximum(new_deaths)
       
        plt.plot(dates, new_deaths, 'gray')
        plt.plot(dates[globalMax[1]], new_deaths[globalMax[1]], 'ro') # global maximum

        plt.title(f'New deaths caused by COVID-19 plot ({iso2})')
        plt.xlabel('Date')
        plt.ylabel('Number of new deaths')
        plt.legend(['new deaths', f'global max = {new_deaths[globalMax[1]]}'], loc='upper left')
        plt.grid(True, axis = 'y')
        plt.xticks(dates[::140])  

        plt.show()

    def plot_regression(self,df,x,y):
        sns.regplot(x=x, y=y, data=df)
        plt.show()