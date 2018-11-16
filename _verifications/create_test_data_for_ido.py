import os
import pickle
os.environ["THEANO_FLAGS"] = "device=cpu,floatX=float32,force_device=True"
os.environ["MKL_THREADING_LAYER"] = "GNU"
import numpy as np
import pandas as pd
import pymc3 as pm
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from configuration import HIERARCHICAL_MODEL_PERFORMANCE_FOLDER, HIERARCHICAL_MODEL_INFERENCE_FOLDER, DATA_TRAINING_FILE, DATA_TESTING_FILE, CONFIG_FILE


def main(output_trace_path, Xy_training_path, Xy_testing_path, output_path, city_target):
    # loading data
    with open(output_trace_path, 'rb') as buff:
        data = pickle.load(buff)
        hierarchical_model, hierarchical_trace, scaler, degree_index, \
        response_variable, predictor_variables = data['inference'], data['trace'], data['scaler'], \
                                                 data['city_index_df'], data['response_variable'],\
                                                 data['predictor_variables']


    # get data of the traces and get Betas and epsilon for the city
    data = pm.trace_to_dataframe(hierarchical_trace)
    code_city = degree_index["CODE"].loc[degree_index["CITY"]==city_target]
    code = code_city.values[0]
    alpha = data['b1__' + str(code)]
    beta = data['b2__' + str(code)]
    eps = data['eps__' + str(code)]


    # fields to scale
    fields_to_scale = [response_variable] + predictor_variables

    # get training data,do the scaler and select the data for the city
    Xy_training = pd.read_csv(Xy_training_path)
    Xy_testing = pd.read_csv(Xy_testing_path)
    if scaler != None:
        Xy_training[fields_to_scale] = pd.DataFrame(scaler.transform(Xy_training[fields_to_scale]),
                                                columns=Xy_training[fields_to_scale].columns)

        Xy_testing[fields_to_scale] = pd.DataFrame(scaler.transform(Xy_testing[fields_to_scale]),
                                               columns=Xy_testing[fields_to_scale].columns)

    x_training_city = Xy_testing.loc[Xy_testing["CITY"]==city_target]
    x_testing_city = Xy_testing.loc[Xy_testing["CITY"] ==city_target]




if __name__ == "__main__":

    name_model = "log_log_all_2var_standard_5000"
    output_path = os.path.join(HIERARCHICAL_MODEL_PERFORMANCE_FOLDER, name_model + ".csv")
    output_trace_path = os.path.join(HIERARCHICAL_MODEL_INFERENCE_FOLDER, name_model + ".pkl")
    Xy_training_path = DATA_TRAINING_FILE
    Xy_testing_path = DATA_TESTING_FILE
    city_target = "New York, NY"
    main_cities = pd.read_excel(CONFIG_FILE, sheet_name='test_cities')['City'].values

    main(output_trace_path, Xy_training_path, Xy_testing_path, output_path, city_target)
