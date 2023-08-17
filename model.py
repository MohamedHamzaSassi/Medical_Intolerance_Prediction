import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.ensemble import AdaBoostRegressor
from sklearn.metrics import classification_report
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import GridSearchCV
from imblearn.over_sampling import SMOTE

def predict_intolerance():

    # Load the Excel sheet into a pandas dataframe
    df = pd.read_excel(r'C:/Users/moham/OneDrive/Desktop/PFE/new_clean1.xlsx')

    # Replace '?' values with NaN
    df = df.replace('?', -1)

    # Split the dataframe into features (X) and target (y)
    X = df.drop('Intolerance_M', axis=1)
    y = df['Intolerance_M']

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Apply SMOTE to the 'Intolerance_M' column only
    smote = SMOTE(sampling_strategy="minority")
    X_train_res, y_train_res = smote.fit_resample(X_train, y_train)

    # Train an AdaBoost regressor with a decision tree as the base estimator on the training data
    X_train=X_train_res
    y_train=y_train_res
    ada = AdaBoostRegressor(estimator=DecisionTreeRegressor(max_depth=2), n_estimators=100, random_state=42)
    params = {
        "n_estimators": [50, 100, 200],
        "learning_rate": [0.1, 0.5, 1],
    }

    # GridSearch with 5-fold cross-validation
    model = GridSearchCV(ada, param_grid=params, cv=5)

    # Fitter les données d'entraînement
    model.fit(X_train, y_train)
    # Use the model to make predictions on the test data
    y_pred = model.predict(X_test)
    y_pred = to_categorical(y_pred, 2)
    y_pred2=[]
    for i in range(len(y_pred)):
        y_pred2.append(int(y_pred[i][1]))
    # Evaluate the performance of the model using mean squared error (MSE) and R-squared (R2) metrics
    #mse = mean_squared_error(y_test, y_pred2)
    #r2 = r2_score(y_test, y_pred2)
    #res=classification_report(y_test, y_pred2)
    #print("Mean Squared Error (MSE): {:.2f}".format(mse))
    #print("R-squared (R2): {:.2f}".format(r2))

    # Load the excel file
    df = pd.read_excel('form_data.xlsx')

    # Get the last row of the dataframe
    new_data = df.iloc[[-1]]

    # Replace '?' with -1
    new_data = new_data.replace('?', -1)

    # Rename the columns in new_data to match X_train
    new_data = new_data.rename(columns={'PRÉCIS_ATOP_2': 'PRÉCIS_ATOP_?', 'tranche_dage_2': 'tranche_dage_?'})

    # Use the model to make predictions on new data
    predicted_intolerance = model.predict(new_data)
    return predicted_intolerance

#predict_intolerance()
