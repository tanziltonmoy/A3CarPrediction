# Import packages

from dash import Dash, html, callback, Output, Input, State, dcc
import dash_bootstrap_components as dbc
import pickle
import numpy as np
from sklearn.preprocessing import StandardScaler

#Load Model
model_path = "model/model.model"
model = pickle.load(open(model_path, 'rb'))

# load the scaling parameters
scaler_path = "model/scaler.pkl"
loaded_scaler_params = pickle.load(open(scaler_path, 'rb'))

# Create scaler with the loaded parameters
loaded_scaler = StandardScaler()
loaded_scaler.mean_ = loaded_scaler_params['mean']
loaded_scaler.scale_ = loaded_scaler_params['scale']

app = Dash(__name__, external_stylesheets=[dbc.themes.CERULEAN])

# App layout with enhanced design
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H2("Car Selling Price Prediction"), width={'size': 6, 'offset': 3})
    ]),

    dbc.Row([
        dbc.Col(html.Div([
            html.H4("Instructions:"),
            html.Ul([
                html.Li("To predict the selling price of a car, please provide the required inputs: Year, km driven, Engine size, Max power, Type of fuel, and Transmission."),
                html.Li("Blank input will be automatically filled using an imputation technique."),
                html.Li("Click the 'Predict' button. The app will then use the selected model to predict the selling price based on the provided inputs.")
            ])
        ]), width={'size': 6, 'offset': 3}, className="mb-4")
    ]),
    
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H4("Enter Car Details", className="card-title"),
                dbc.Row([
                    dbc.Col(dbc.Label("Year of Car Made (e.g., 2020):"), width=6),
                    dbc.Col(dbc.Input(id="year", type="number", placeholder="Enter the Car Model Year"), width=6),
                    dbc.Tooltip("Enter the manufacturing year of the car", target="year"),
                ]),
                dbc.Row([
                    dbc.Col(dbc.Label("Number of km Driven (e.g., 450000 km):"), width=6),
                    dbc.Col(dbc.Input(id="km_driven", type="number", placeholder="Enter KM driven"), width=6),
                    dbc.Tooltip("Enter the total kilometers driven by the car", target="km_driven"),
                ]),
                dbc.Row([
                    dbc.Col(dbc.Label("Engine Size (e.g., 1248 CC):"), width=6),
                    dbc.Col(dbc.Input(id="engine_size", type="number", placeholder="Enter Engine size (in CC)"), width=6),
                    dbc.Tooltip("Enter the engine capacity in CC", target="engine_size"),
                ]),
                dbc.Row([
                    dbc.Col(dbc.Label("Max Power of Car (e.g., 74 kW):"), width=6),
                    dbc.Col(dbc.Input(id="max_power", type="number", placeholder="Enter Max Power"), width=6),
                    dbc.Tooltip("Enter the maximum power output of the car in kW", target="max_power"),
                ]),
                dbc.Row([
                    dbc.Col(dbc.Label("Type of Fuel:"), width=6),
                    dbc.Col(dcc.Dropdown(['Petrol', 'Diesel'], id='fuel_dropdown'), width=6),
                    dbc.Tooltip("Select the type of fuel used by the car", target="fuel_dropdown"),
                ]),
                dbc.Row([
                    dbc.Col(dbc.Label("Type of Transmission:"), width=6),
                    dbc.Col(dcc.Dropdown(['Manual', 'Automatic'], id='transmission_dropdown'), width=6),
                    dbc.Tooltip("Select the transmission type of the car", target="transmission_dropdown"),
                ]),
                dbc.Button("Predict", id="submit", color="primary", className="mr-2", style={"marginTop": "20px"})
            ])
        ]), width=6)
    ], justify="center"),
    dbc.Row([
        dbc.Col(html.Div([
            html.H4("Prediction Result"),
            html.Div(id="output_monitor", className="alert alert-success")
        ]), width={'size': 6, 'offset': 3})
    ]),

    dbc.Row([
        dbc.Col(html.Div([
            html.P("Developed by Tanzil Al Sabah", className="text-muted"),
            html.P("ID: 123845", className="text-muted")
        ]), width={'size': 6, 'offset': 3}, className="mt-5")
    ])
], fluid=True)

@callback(
    Output(component_id="output_monitor", component_property="children"),
    State(component_id="year", component_property="value"),
    State(component_id="km_driven", component_property="value"),
    State(component_id="engine_size", component_property="value"),
    State(component_id="max_power", component_property="value"),  
    State( component_id="fuel_dropdown", component_property="value"),
    State( component_id="transmission_dropdown", component_property="value"),
    Input(component_id="submit", component_property='n_clicks'),
    prevent_initial_call=True
)
def Predict_Life_Expectancy(year, km_driven, engine_size, max_power, fuel, transmission, submit):
    print(year, km_driven, engine_size, max_power, fuel, transmission)
    if year is None:
        age = 7.137924897668625 #initialized by mean of age
    else:
        age = abs(2023+1 - year)  #calculating age as the same way was done in training  ( age_of_car = [ max_year_of_data_set + 1 - year_of_car_model ] )
    if km_driven is None:
        km_driven = 70029.87346502936 #initialized by mean of km_driven
    if engine_size is None:
        engine_size = 1463.855626715462 #initialized by mean of engine_size
    if max_power is None:
        max_power = 91.819726 #initialized by mean of max_power
    if fuel is None or fuel == "Diesel":
        fuel = 0 #initialized by Diesel type if no input
    else:
        fuel = 1
    if transmission is None  or transmission == "Manual": 
        transmission = 1            #initialized by Manual type if no input
    else:
        transmission = 0

    #type casting of value in float64
    age = np.float64(age)
    km_driven = np.float64(km_driven)
    engine_size = np.float64(engine_size)
    max_power = np.float64(max_power)
    fuel = np.float64(fuel)
    transmission = np.float64(transmission)

    
    # Make prediction using the model
    input_feature = np.array([[km_driven, age, engine_size, max_power, fuel, transmission]])
    # Transform the first 4 features
    input_feature[:, :4] = loaded_scaler.transform(input_feature[:, :4]) 
    print(input_feature.shape)
    prediction = model.predict(input_feature)[0]
    prediction = np.exp(prediction)
    predictedText = f"Predicted Selling Price: {prediction:.2f}"
    return predictedText
# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)
