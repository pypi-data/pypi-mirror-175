import pandas as pd
import numpy as np
import warnings
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

warnings.filterwarnings('ignore')

class RFI:
    def __init__(self)-> None:
        pass
    def seleccion_modelo_regresion(df):

        X = df.drop('target', axis=1)
        y = df['target']

        X_train, _, y_train, _ = train_test_split(X, y, test_size=0.2, random_state=1)
        rf = RandomForestRegressor().fit(X_train, y_train)
        imp = rf.feature_importances_
        importances = pd.DataFrame({'feature': X_train.columns, 'importance': np.round(imp, 3)}).sort_values('importance', ascending=False)
        percentil_75 = importances['importance'].quantile(0.75)
        columnas_buenas = importances[importances["importance"] >= percentil_75]["feature"].values
        df = pd.concat([df[columnas_buenas], df["target"]], axis=1)

        # if it not dataframe
        if not isinstance(df, pd.DataFrame):
            raise ValueError('Tiene que ser un pandas DataFrame')


        if not all(df.dtypes == 'int32') and not all(df.dtypes == 'float64'):
            raise TypeError("El DataFrame debe contener solo columnas numéricas")

        if "target" not in df.columns:
            raise KeyError("El DataFrame debe contener una columna llamada 'target' (variable a predecir) ")
        
        if df.isnull().sum().sum() > 0:
            raise ValueError("El DataFrame no debe contener valores nulos")
        
        if len(df.columns) < 2:
            raise ValueError("El DataFrame debe contener al menos dos columnas")
        

        if df["target"].isnull().sum() > 0:
            raise ValueError("La columna 'target' no debe contener valores nulos")

        return df
