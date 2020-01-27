from __future__ import division
from __future__ import print_function

import plotly.graph_objs as go
from  plotly  import  tools
import plotly.plotly as py

import os
from plotly.offline import plot
import pandas as pd
from configuration import CONFIG_FILE, DATA_HDD_CDD_PLOTS_FOLDER, DATA_RAW_BUILDING_IPCC_SCENARIOS_FILE, DATA_RAW_BUILDING_TODAY_HDD_FOLDER



def calc_graph(data_frame, output_path,  colors_hdd, colors_cdd, cities, scenarios):

    fig = tools.make_subplots(rows=1, cols=len(cities), shared_yaxes=True, shared_xaxes=True,
                              subplot_titles=cities,)

    for i, city in enumerate(cities):
        data = data_frame[data_frame["City"] == city]
        scenario_change_50_100 = []
        scenario_change_0_50 = []
        scenario_change_50_100_h = []
        scenario_change_0_50_h = []
        for j, scenario in enumerate(scenarios):
            data2 = data[data["SCENARIO_CLASS"] == scenario]
            x = data2.index

            y = data2["CDD_18_5_C"]
            trace = go.Scatter(x=x, y=y, name="CDD for scenario" + scenario, marker=dict(color=colors_hdd[j]),
                               )
            fig.append_trace(trace, 1, i+1)
            scenario_change_50_100.append((data2.loc["2100", "CDD_18_5_C"] - data2.loc["2050", "CDD_18_5_C"])/5)
            scenario_change_0_50.append((data2.loc["2050", "CDD_18_5_C"] - data2.loc["2010", "CDD_18_5_C"])/4)

            y = data2["HDD_18_5_C"]
            trace = go.Scatter(x=x, y=y, name="HDD for scenario " + scenario, marker=dict(color=colors_cdd[j]), yaxis = 'y2')
            fig.append_trace(trace, 1, i+1)

            scenario_change_50_100_h.append((data2.loc["2100", "HDD_18_5_C"] - data2.loc["2050", "HDD_18_5_C"])/5)
            scenario_change_0_50_h.append((data2.loc["2050", "HDD_18_5_C"] - data2.loc["2010", "HDD_18_5_C"])/4)


        print(" %change per decade cooling ", city, round(sum(scenario_change_0_50)/3,0), round(sum(scenario_change_50_100)/3,0))
        print(" %change per decade heating ", city, round(sum(scenario_change_0_50_h)/3,0), round(sum(scenario_change_50_100_h)/3,0))

    for i in fig['layout']['annotations']:
        i['font'] = dict(family='Helvetica, monospace', size=20)


    fig['layout'].update(yaxis=dict(domain=[0, 1.0]), yaxis2=dict(domain=[0, 1]), plot_bgcolor= "rgb(236,243,247)",
                         font=dict(family='Helvetica, monospace', size=18)
                         )
    plot(fig, auto_open=False, filename=output_path + '//' + "lines" + ".html")


    return fig

def main(years_to_map, output_path, future_hdd_cdd_file,  colors_hdd, colors_cdd, cities, scenarios):
    # get data from every city and transform into data per scenario
    data_final = pd.DataFrame()
    for i, city in enumerate(cities):

        data_future_HDD_CDD = future_hdd_cdd_file[future_hdd_cdd_file['City'] == city]
        HDD_baseline = data_future_HDD_CDD.loc[data_future_HDD_CDD["Scenario"]=="1990_2010"]["HDD_18_5_C"].values[0]
        CDD_baseline = data_future_HDD_CDD.loc[data_future_HDD_CDD["Scenario"]=="1990_2010"]["CDD_18_5_C"].values[0]

        # heating case
        data_future_HDD_CDD["YEAR"] = [x.split("_", 1)[1] for x in data_future_HDD_CDD["Scenario"].values]
        data_future_HDD_CDD["TODAY_HDD_18_5_C"] = HDD_baseline
        data_future_HDD_CDD["TODAY_CDD_18_5_C"] =  CDD_baseline
        data_future_HDD_CDD.set_index("YEAR", inplace=True)
        data_future_HDD_CDD["SCENARIO_CLASS"] = [x.split("_", 1)[0] for x in data_future_HDD_CDD["Scenario"].values]
        df = data_future_HDD_CDD[["TODAY_HDD_18_5_C", "TODAY_CDD_18_5_C", "HDD_18_5_C", "CDD_18_5_C", "SCENARIO_CLASS", "City"]]

        data_final = pd.concat([data_final, df])

    data_final["HDD_18_5_C"] = (data_final["HDD_18_5_C"]- data_final["TODAY_HDD_18_5_C"])/data_final["TODAY_HDD_18_5_C"]*100
    data_final["CDD_18_5_C"] = (data_final["CDD_18_5_C"]- data_final["TODAY_CDD_18_5_C"])/data_final["TODAY_CDD_18_5_C"]*100


    calc_graph(data_final, output_path,  colors_hdd, colors_cdd, cities, scenarios)


if __name__ == "__main__":
    data_path = os.path.join(os.path.dirname(os.getcwd()), 'IPCC_scenarios', 'data')
    cities = pd.read_excel(CONFIG_FILE, sheet_name='test_cities')['City'].values[5:]
    output_path = DATA_HDD_CDD_PLOTS_FOLDER
    future_hdd_cdd_file = pd.read_csv(DATA_RAW_BUILDING_IPCC_SCENARIOS_FILE)
    scenarios = ["B1", "A1B", "A2"]
    colors_cdd = ["rgb(239,154,154)", "rgb(239,83,80)","rgb(183,28,28)"]
    colors_hdd = ["rgb(144,202,249)", "rgb(66,165,245)", "rgb(13,71,161)"]
    years_to_map = [2020, 2030, 2040, 2050, 2060, 2070, 2080, 2090, 2100]

    main(years_to_map, output_path, future_hdd_cdd_file, colors_hdd, colors_cdd, cities, scenarios)