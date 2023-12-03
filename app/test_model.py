import pickle
import numpy as np
from sklearn.preprocessing import StandardScaler
import mlflow
import os
import joblib


loaded_model = pickle.load(open("model3.pkl", 'rb'))



scaler_path = "scaler/scaler.pkl"
loaded_scaler_params = pickle.load(open(scaler_path, 'rb'))

# # Create scaler with the loaded parameters
loaded_scaler = StandardScaler()
loaded_scaler.mean_ = loaded_scaler_params['mean']
loaded_scaler.scale_ = loaded_scaler_params['scale']       



# Test whether the model takes expected input
#initialize the features with user input values
km_driven = np.log(450000)
year = 2020
age = abs(2020+1 - year) #calulatring age of the car model by subtracting from the max year 2020
max_power = 90
engine = 780
fuel_Petrol = 0
transmission_type = 0

data = np.array([[km_driven,age,engine,max_power,fuel_Petrol, transmission_type]])
# Transform the first 4 features
data[:, :4] = loaded_scaler.transform(data[:, :4])

intercept = np.ones((data.shape[0], 1))
input_feature = np.concatenate((intercept, data), axis=1)

def test_input():
        try:
            _ = loaded_model.predict(input_feature)
        except Exception as e:
            assert False, f"Model failed to take expected input: {e}"
    
def test_output_shape():    
    try:
        prediction = loaded_model.predict(input_feature)
        assert prediction.shape == (1,), "Output shape is not as expected"
    except Exception as e:
        assert False, f"Output shape test failed: {e}"

if __name__ == '__main__':
    # If the script is run directly, execute your app or other logic
    test_input()
    test_output_shape()