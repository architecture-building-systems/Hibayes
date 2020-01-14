import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas.plotting import scatter_matrix
from sklearn import linear_model
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split

from configuration import CONFIG_FILE, DATA_ALLDATA_FILE
from sklearn.cluster import KMeans, DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import make_blobs
from sklearn import mixture


def calc_MAPE(y_true, y_pred, n):
    delta = (y_pred - y_true)
    error = np.sum((np.abs(delta / y_true))) * 100 / n
    return error


def calc_accurracy(y_prediction, y_target):
    MAPE_single_building = calc_MAPE(y_true=y_target, y_pred=y_prediction, n=len(y_target)).round(2)
    MAPE_city_scale = calc_MAPE(y_true=np.mean(y_target), y_pred=np.mean(y_prediction), n=1).round(2)
    r2 = r2_score(y_true=y_target, y_pred=y_prediction).round(2)

    return MAPE_single_building, MAPE_city_scale, r2

random_state = 170
np.random.RandomState(random_state)
data_path = DATA_ALLDATA_FILE
cities_path = CONFIG_FILE
cities = pd.read_excel(cities_path, sheet_name='test_cities')['City'].values

df2 = pd.read_csv(data_path)
df2['RATIO'] = df2['LOG_SITE_ENERGY_kWh_yr']/df2['LOG_THERMAL_ENERGY_kWh_yr']
# df2 = df2[df2['CLIMATE_ZONE'] == 'Hot-humid']
df2 = df2[df2["CITY"] == "Los Angeles, CA"]
df2 = df2[df2["BUILDING_CLASS"] == "Commercial"]
n_components = 3

#
cities = df2.CITY.unique()
building_classes = df2.BUILDING_CLASS.unique()
df = pd.DataFrame()
for city in cities:
    for classes in building_classes:
        df3 = df2[df2["CITY"] == city]
        df3 = df3[df3["BUILDING_CLASS"] == classes]
        if df3.empty:
            x=1
        else:
            X_cluster = df3[["LOG_THERMAL_ENERGY_kWh_yr", "LOG_SITE_ENERGY_kWh_yr"]].values
            cv_type = 'tied'
            gmm = mixture.GaussianMixture(n_components=n_components, covariance_type=cv_type)
            gmm.fit(X_cluster)
            cluster_labels = gmm.predict(X_cluster)
            df3['CLUSTERS'] = cluster_labels
            df = pd.concat([df, df3], ignore_index=True)


#RATIO
X = df[["LOG_THERMAL_ENERGY_kWh_yr", "RATIO"]].values
Y = df[["LOG_SITE_ENERGY_kWh_yr"]].values
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=random_state)
regr = linear_model.LinearRegression()
regr.fit(X_train, y_train)
y_pred = regr.predict(X_test)

#get clusters
X_cluster = [[x[0],y[0]] for x,y in zip(X_test, y_test)]
cv_type='tied'
gmm = mixture.GaussianMixture(n_components=n_components,   covariance_type=cv_type)
gmm.fit(X_cluster)
cluster_labels = gmm.predict(X_cluster)
plt.scatter([[x[0]] for x in X_test], y_test, c=cluster_labels.reshape(-1,1))
plt.plot([[x[0]] for x in X_test], y_pred, color='blue', linewidth=3)
plt.show()

#COEFFICIENTS
y_test = np.exp(y_test)
y_pred = np.exp(y_pred)
MAPE, PE, r2_test = calc_accurracy(y_pred, y_test)
# The coefficients
print('Coefficients: \n', regr.coef_, regr.intercept_)
# The mean squared error
print('MAPE error: %.2f'
      % MAPE)
# The mean squared error
print('PE error: %.2f'
      % PE)
# The coefficient of determination: 1 is perfect prediction
print('Coefficient of determination: %.2f'
      % r2_test)

#CLUSTERS
X = df[["LOG_THERMAL_ENERGY_kWh_yr", "RATIO", "CLUSTERS"]].values
Y = df[["LOG_SITE_ENERGY_kWh_yr"]].values
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=random_state)
regr = linear_model.LinearRegression()
regr.fit(X_train, y_train)
y_pred = regr.predict(X_test)

#get clusters
X_cluster = [[x[0],y[0]] for x,y in zip(X_test, y_test)]
cv_type='tied'
gmm = mixture.GaussianMixture(n_components=n_components,   covariance_type=cv_type)
gmm.fit(X_cluster)
cluster_labels = gmm.predict(X_cluster)
plt.scatter([[x[0]] for x in X_test], y_test, c=cluster_labels.reshape(-1,1))
plt.plot([[x[0]] for x in X_test], y_pred, color='blue', linewidth=3)
plt.show()

#COEFFICIENTS
y_test = np.exp(y_test)
y_pred = np.exp(y_pred)
MAPE, PE, r2_test = calc_accurracy(y_pred, y_test)
# The coefficients
print('Coefficients: \n', regr.coef_, regr.intercept_)
# The mean squared error
print('MAPE error: %.2f'
      % MAPE)
# The mean squared error
print('PE error: %.2f'
      % PE)
# The coefficient of determination: 1 is perfect prediction
print('Coefficient of determination: %.2f'
      % r2_test)

#RATIO
X = df[["LOG_THERMAL_ENERGY_kWh_yr"]].values
Y = df[["LOG_SITE_ENERGY_kWh_yr"]].values
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=random_state)
regr = linear_model.LinearRegression()
regr.fit(X_train, y_train)
y_pred = regr.predict(X_test)

#get clusters
X_cluster = [[x[0],y[0]] for x,y in zip(X_test, y_test)]
cv_type='tied'
gmm = mixture.GaussianMixture(n_components=n_components,   covariance_type=cv_type)
gmm.fit(X_cluster)
cluster_labels = gmm.predict(X_cluster)
plt.scatter([[x[0]] for x in X_test], y_test, c=cluster_labels.reshape(-1,1))
plt.plot([[x[0]] for x in X_test], y_pred, color='blue', linewidth=3)
plt.show()

#COEFFICIENTS
y_test = np.exp(y_test)
y_pred = np.exp(y_pred)
MAPE, PE, r2_test = calc_accurracy(y_pred, y_test)
# The coefficients
print('Coefficients: \n', regr.coef_, regr.intercept_)
# The mean squared error
print('MAPE error: %.2f'
      % MAPE)
# The mean squared error
print('PE error: %.2f'
      % PE)
# The coefficient of determination: 1 is perfect prediction
print('Coefficient of determination: %.2f'
      % r2_test)

# X = [[x[0],y[0]] for x,y in zip(X_test2,y_test2)]
# # y_pred = KMeans(n_clusters=3, random_state=random_state).fit_predict(X)
# cv_type='tied'
# gmm = mixture.GaussianMixture(n_components=3,   covariance_type=cv_type)
# gmm.fit(X)
# y_pred = gmm.predict(X)


# fields = ["LOG_SITE_ENERGY_kWh_yr", "LOG_THERMAL_ENERGY_kWh_yr", 'RATIO']  # , "ok"]
# scatter_matrix(df[fields], alpha=0.2, marker='o', figsize=(10, 10), diagonal='hist', hist_kwds={'bins': 224})
# plt.show()


# sns.pairplot(df, size=4, aspect=1,
#                          hue="BUILDING_CLASS",
#                          #diag_kind='none',
#                          markers="+", plot_kws = dict(s=50, edgecolor="b", linewidth=1), diag_kws = dict(bins=224),
#                          palette="PuBuGn_d")

# df = df[df["CITY"] == "Seattle, WA"] #"Seattle, WA"
#
# import matplotlib as mpl
# mpl.rcParams['mathtext.fontset'] = 'cm'
# fig, axes = plt.subplots(1, 3, figsize=(12,6));
# plt.subplots_adjust(wspace=0.4, bottom=0.25 , top=0.7);
# commercial = (63/255,192/255,194/255)
# residential = (126/255,127/255,132/255)
# xaxis_1 = r'$\log(y_{i,j})$'
# xaxis_2 = r'$\log(x_{1_{i,j}})$'
# xaxis_3 = r'$\log(x_{2_{i,j}})$'
# yaxis_2 = r'$\log(y_{i,j})$'
# yaxis_3 = r'$\log(y_{i,j})$'
# # "rgb(255,209,29)","rgb(126,199,143)","rgb(245,131,69)","rgb(240,75,91)"
# # df["LOG_SITE_ENERGY_MWh_yr"].plot(ax=axes[0,0], kind='hist', bins=200, color=color); axes[0,0].set_title('(a)');
# df[df["BUILDING_CLASS"] == "Residential"]["LOG_SITE_ENERGY_MWh_yr"].plot(ax=axes[0], kind='hist', bins=200, color=residential,)
# df[df["BUILDING_CLASS"] == "Commercial"]["LOG_SITE_ENERGY_MWh_yr"].plot(ax=axes[0], kind='hist', bins=200, color=commercial)
#
#
# # df.plot.scatter(ax=axes[1,0], x="LOG_HDD_FLOOR_18_5_C_m2", y ="LOG_SITE_ENERGY_MWh_yr", color=color); axes[1,0].set_title('(d)')
# df[df["BUILDING_CLASS"] == "Commercial"].plot.scatter(ax=axes[1], x="LOG_HDD_FLOOR_18_5_C_m2", y ="LOG_CDD_FLOOR_18_5_C_m2", color=commercial)
# df[df["BUILDING_CLASS"] == "Residential"].plot.scatter(ax=axes[1], x="LOG_HDD_FLOOR_18_5_C_m2", y ="LOG_CDD_FLOOR_18_5_C_m2", color=residential)
#
# df[df["BUILDING_CLASS"] == "Commercial"].plot.scatter(ax=axes[2], x="LOG_CDD_FLOOR_18_5_C_m2", y ="LOG_SITE_ENERGY_MWh_yr", color=commercial)
# df[df["BUILDING_CLASS"] == "Residential"].plot.scatter(ax=axes[2], x="LOG_CDD_FLOOR_18_5_C_m2", y ="LOG_SITE_ENERGY_MWh_yr", color=residential)
#
# axes[0].set_xlabel(xaxis_1, fontsize=14)
# axes[0].legend(["Residential", "Commercial"])
# axes[1].set_xlabel(xaxis_2, fontsize=14)
# axes[2].set_xlabel(xaxis_3, fontsize=14)
# axes[1].set_ylabel(yaxis_2, fontsize=14)
# axes[2].set_ylabel(yaxis_3, fontsize=14)
#
# axes[1].set_title('All 96 cities', fontsize=18, y=1.08)
#
# plt.show()


# for city in cities[:2]:
#     city_data = df[df.CITY == city]
#     sns.distplot(a = city_data["LOG_SITE_ENERGY_MWh_yr"])

# sns.violinplot(x="CITY", y="LOG_SITE_ENERGY_MWh_yr", hue="BUILDING_CLASS", data=df,
#                split=True, palette="Set3");

# sns.violinplot(x="LOG_SITE_ENERGY_MWh_yr", hue="BUILDING_CLASS", data=df,
#                split=True, palette="Set3");

# f, ax = plt.subplots(figsize=(10, 8))
# corr = df[fields].corr()
# sns.heatmap(corr, mask=np.zeros_like(corr, dtype=np.bool), cmap=sns.diverging_palette(220, 10, as_cmap=True),
#             square=True, ax=ax)


# fields = ["LOG_SITE_EUI_kWh_m2yr", "LOG_GROSS_FLOOR_AREA_m2", "HDD_18_5_C", "CDD_18_5_C"]
# df_commercial = df[df.BUILDING_CLASS == "Commercial"]
# scatter_matrix(df_commercial[fields], alpha=0.2, figsize=(10, 10), diagonal='hist', hist_kwds={'bins': 160})
# print(len(df_commercial.index))
# plt.show()
#
# fields = ["LOG_SITE_EUI_kWh_m2yr", "LOG_GROSS_FLOOR_AREA_m2", "HDD_18_5_C", "CDD_18_5_C"]
# df_residential = df[df.BUILDING_CLASS == "Residential"]
# scatter_matrix(df_residential[fields], alpha=0.2, figsize=(10, 10), diagonal='hist', hist_kwds={'bins': 160})
# print(len(df_residential.index))
