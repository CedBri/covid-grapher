import json, requests
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import datetime as dt

class CovidProvData:
    def __init__(self, daily_data):
        self.active_cases = int(daily_data["active_cases"])
        self.daily_cases = int(daily_data["cases"])
        self.cumul_avax = int(daily_data["cumulative_avaccine"])
        self.cumul_cases = int(daily_data["cumulative_cases"])
        self.cumul_deaths = int(daily_data["cumulative_deaths"])
        self.date = daily_data["date"]
        self.province = daily_data["province"]

def fetch_data(province, before="2099-12-31", after="2020-01-01"):
    data_list = []

    url = f'https://api.opencovid.ca/summary?loc={province}'
    before = f'&before={before}' # Get data before date. YYYY-MM-DD.
    after = f'&after={after}' # Get data after date. YYYY-MM-DD.
    req = requests.get(url + before + after)
    # Gotta correct all the 'NULL' values to 0
    raw_data = json.loads(req.text)
    raw_data  = json.dumps(raw_data).replace('NULL', '0')
    raw_data = json.loads(raw_data)
    for item in raw_data["summary"]:
        data_list.append(CovidProvData(item))
    return data_list

def graph_data(data_list, act_cas_opt = False, daily_cases_opt = False, cumul_avax_opt = False,
        cumul_cases_opt = True, deaths_opt = True):
    
    # Def lists
    actives_cases_list = []
    daily_cases_list = []
    cumul_avax_list = []
    cumul_cases_list = []
    cumul_deaths_list = []
    dates_list = []

    # Triage data
    for item in data_list:
        actives_cases_list.append(item.active_cases)
        daily_cases_list.append(item.daily_cases)
        cumul_avax_list.append(item.cumul_avax)
        cumul_cases_list.append(item.cumul_cases)
        cumul_deaths_list.append(item.cumul_deaths)
        dates_list.append(item.date)
    
    # Format date
    
    dates_list = [dt.datetime.strptime(d, '%d-%m-%Y').date() for d in dates_list]

    # Gen plot
    fig, (ax_1, ax_2) = plt.subplots(nrows=2, ncols=1)
    ax_1.plot(dates_list, cumul_cases_list, label="Cumul of cases")
    ax_2.plot(dates_list, cumul_avax_list, label="Cumul of vaccines")
   # if act_cas_opt:
        # plt.plot(dates_list, actives_cases_list, label="Number of active cases" )
    # if daily_cases_opt:
        # plt.plot(dates_list, daily_cases_list, label="Number of daily cases")
    # if cumul_avax_opt:
        # plt.plot(dates_list, cumul_avax_list, label="Cumulative number of vaccines given")
    # if cumul_cases_opt:
        # plt.plot(dates_list, cumul_cases_list, label="Cumulative number of cases")
    # if deaths_opt:
        # plt.plot(dates_list, cumul_deaths_list, label="Cumulative number of deaths")


    ax_1.legend(loc=0)
    ax_2.legend(loc=0)
    plt.show() 
def main():
    graph_data(fetch_data("QC")) 


if __name__=='__main__':
    main()
