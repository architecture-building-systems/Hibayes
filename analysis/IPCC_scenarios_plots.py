import os

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import scatter_matrix, parallel_coordinates


def main(data_path, data_path_current, output_path, cities, cooling_heating, temperature):

    # get data from every city and transform into data per scenario
    data = pd.read_csv(os.path.join(data_path, "future_degree_days.csv"))
    scenarios = data["Scenario"].unique()
    data_table = pd.DataFrame()
    for city in cities:
        data_current = pd.read_csv(os.path.join(data_path_current, city+".csv"))
        data_new = data [data['City']== city]
        data_new2 = data_new.set_index("Scenario")


        # HEATING CASE
        today_value = data_new2.loc["A1B_2020", "HDD_18_5_C"]
        data_new["YEAR"] = [x.split("_",1)[1] for x in data_new["Scenario"].values]
        data_new.set_index("YEAR", inplace=True)
        data_new["CHANGE"] = ((data_new["HDD_18_5_C"] - today_value)/today_value)*100
        data_new["SCENARIO_CLASS"] = [x.split("_",1)[0] for x in  data_new["Scenario"].values]
        data_final = pd.DataFrame()
        for scenario in scenarios:
            scenario_type = scenario.split("_", 1)[1]
            df = data_new[data_new.index == scenario_type]
            # df[scenario_type] =
            data_final[scenario_type] = pd.DataFrame({scenario_type:df["HDD_18_5_C"].values})

        fig, ax = plt.subplots()
        data_final[['2020','2030', '2040', '2050']].plot.box(title=city, figsize=(4,4),ax=ax)

        # COOLING CASE
        today_value = data_new2.loc["A1B_2020", "CDD_18_5_C"]
        data_new["YEAR"] = [x.split("_",1)[1] for x in data_new["Scenario"].values]
        data_new.set_index("YEAR", inplace=True)
        data_new["CHANGE"] = ((data_new["CDD_18_5_C"] - today_value)/today_value)*100
        data_new["SCENARIO_CLASS"] = [x.split("_",1)[0] for x in  data_new["Scenario"].values]
        data_final = pd.DataFrame()
        for scenario in scenarios:
            scenario_type = scenario.split("_", 1)[1]
            df = data_new[data_new.index == scenario_type]
            # df[scenario_type] =
            data_final[scenario_type] = pd.DataFrame({scenario_type:df["CDD_18_5_C"].values})

        data_final[['2020','2030', '2040', '2050']].plot.box(title=city, figsize=(4,4),ax=ax)
        plt.ylim((0, 3500))
        plt.savefig(os.path.join(output_path, cooling_heating, city + cooling_heating+".png"))
    #
    #     data_final['scenario'] = df["SCENARIO_CLASS"].values
    #     data_final['city'] = city
    #
    #     data_table = data_table.append(data_final)
    # data_table.to_csv(os.path.join(output_path, cooling_heating, cooling_heating+".csv"))

if __name__ == "__main__":
    name_model = "log_neural_net_wide_deep_4L_453%_3%"
    cooling_heating = "HDD" #HDD
    temperature = "HDD_18_5_C" #HDD_18_5_C
    data_path = os.path.join(os.path.dirname(os.getcwd()), 'IPCC_scenarios', 'data')
    data_path_current = os.path.join(os.path.dirname(os.getcwd()), 'today_heating_degree_days', 'data')
    output_path = os.path.join(os.path.dirname(os.getcwd()), 'IPCC_scenarios', 'plots')
    cities = pd.read_excel(os.path.join(os.path.dirname(os.getcwd()), "cities.xlsx"), sheet_name='test_cities')['City']

    main(data_path, data_path_current, output_path, cities, cooling_heating, temperature)


