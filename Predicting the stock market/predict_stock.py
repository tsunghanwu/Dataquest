import pandas as pd
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

df = pd.read_csv("sphist.csv")
df["Date"] = pd.to_datetime(df["Date"])

timeline = df["Date"] > datetime(year=2015, month=4, day=1)

df = df.sort_values("Date", ascending = True)

day5_mean = []
day30_mean = []
day365_mean = []
day_5_stddev = []
day_365_stddev = []

for index, row in df.iterrows():
    rolling_mean_5 = np.mean(df["Close"].iloc[index-5:index])
    rolling_mean_30 = np.mean(df["Close"].iloc[index-30:index])
    rolling_mean_365 = np.mean(df["Close"].iloc[index-365:index])
    rolling_stddev_5 = np.std(df["Close"].iloc[index-5:index])
    rolling_stddev_365 = np.std(df["Close"].iloc[index-365:index])
    
    day5_mean.append(rolling_mean_5)
    day30_mean.append(rolling_mean_30)
    day365_mean.append(rolling_mean_365)
    day_5_stddev.append(rolling_stddev_5)
    day_365_stddev.append(rolling_stddev_365)

df["Day_5"] = pd.Series(day5_mean)
df["Day_30"] = pd.Series(day30_mean)
df["Day_365"] = pd.Series(day365_mean)
df["Day_5/365_ratio"] = df["Day_5"] / df["Day_365"]
df["Day_5_stddev"] = pd.Series(day_5_stddev)
df["Day_365_stddev"] = pd.Series(day_365_stddev)
df["Day_5/365_std_ratio"] = df["Day_5_stddev"] / df["Day_365_stddev"]

df = df[df["Date"] > datetime(1951,1,3)]
df = df.dropna(axis=0)

train = df[df["Date"] < datetime(2013,1,1)]
test = df[df["Date"] >= datetime(2013,1,1)]

features = ["Day_5", "Day_30", "Day_365", "Day_5/365_ratio", "Day_5_stddev", "Day_365_stddev", "Day_5/365_std_ratio"]

lr = LinearRegression()
lr.fit(train[features], train["Close"])
predictions = lr.predict(test[features])
mae = mean_absolute_error(test["Close"], predictions)
coeff = lr.coef_
intercept = lr.intercept_

fig, ax = plt.subplots()
plt.plot(test["Date"], test["Close"], label="Actual")
plt.plot(test["Date"], predictions, label="Predicted")
plt.title("Closing price vs. Date")
plt.xlabel("Date")
plt.ylabel("Closing price")
plt.xticks(rotation=90)
plt.legend()
plt.show()
