from data_preparation import load_data
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error,r2_score
import matplotlib.pyplot as plt

x,y = load_data("data/household_power_consumption.txt")
x_train, x_test, y_train, y_test = train_test_split(x,y,test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(x_train,y_train)
y_pred = model.predict(x_test)


print("Mean Squared Error:", mean_squared_error(y_test,y_pred))
print("R2 Score:", r2_score(y_test,y_pred))


# Visualization
plt.scatter(y_test,y_pred, alpha=0.5)
plt.xlabel("Actual power values")
plt.ylabel("predicted power values ")
plt.title("Actual ve predicted power values")
plt.show()