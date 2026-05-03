import pandas as pd
from sklearn.linear_model import LinearRegression
import pickle

data = pd.read_csv("data.csv")

X = data[['price_sold', 'demand']]
y = data['units_sold']

model = LinearRegression()
model.fit(X, y)

pickle.dump(model, open("model.pkl", "wb"))

print("Model ready!")