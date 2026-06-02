import os
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, classification_report
import joblib


def load_data():
    paths = [
        'output/combined_prices.csv',
        'sample_prices.csv'
    ]
    for p in paths:
        if os.path.exists(p):
            return pd.read_csv(p)
    raise FileNotFoundError('No data file found')


def prepare_features(df: pd.DataFrame):
    df = df.copy()
    if 'extraction_date' in df.columns:
        df['extraction_date'] = pd.to_datetime(df['extraction_date'])
    else:
        df['extraction_date'] = pd.to_datetime('today')
    df = df.sort_values(['product_name','extraction_date'])
    # create lag features per product
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    df['lag_1'] = df.groupby('product_name')['price'].shift(1)
    df['lag_2'] = df.groupby('product_name')['price'].shift(2)
    df['lag_3'] = df.groupby('product_name')['price'].shift(3)
    df['next_price'] = df.groupby('product_name')['price'].shift(-1)
    # keep rows that have price and next_price; fill missing lags with current price
    df = df.dropna(subset=['price','next_price'])
    df['lag_1'] = df['lag_1'].fillna(df['price'])
    df['lag_2'] = df['lag_2'].fillna(df['price'])
    df['lag_3'] = df['lag_3'].fillna(df['price'])
    # target trend: up/down/stable
    def trend(row):
        if row['next_price'] > row['price'] * 1.01:
            return 1
        elif row['next_price'] < row['price'] * 0.99:
            return -1
        else:
            return 0
    df['trend'] = df.apply(trend, axis=1)
    features = df[['price','lag_1','lag_2','lag_3']].fillna(0)
    return features, df['next_price'], df['trend']


def train_and_save():
    df = load_data()
    X, y_reg, y_clf = prepare_features(df)
    if X.empty:
        print('No training data after preprocessing.')
        return
    n = len(X)
    # If very small dataset, train on all and skip holdout evaluation
    if n < 3:
        print('Very small training set (n=%d). Training on all data, skipping holdout evaluation.' % n)
        reg = RandomForestRegressor(n_estimators=50, random_state=42)
        reg.fit(X, y_reg)
        clf = RandomForestClassifier(n_estimators=50, random_state=42)
        clf.fit(X, y_clf)
    else:
        X_train, X_test, yreg_train, yreg_test, yclf_train, yclf_test = train_test_split(
            X, y_reg, y_clf, test_size=0.2, random_state=42
        )
        # Regressor
        reg = RandomForestRegressor(n_estimators=50, random_state=42)
        reg.fit(X_train, yreg_train)
        preds = reg.predict(X_test)
        mae = mean_absolute_error(yreg_test, preds)
        print(f'Regressor MAE: {mae:.4f}')
        # Classifier
        clf = RandomForestClassifier(n_estimators=50, random_state=42)
        clf.fit(X_train, yclf_train)
        preds_clf = clf.predict(X_test)
        print('Classifier report:')
        print(classification_report(yclf_test, preds_clf))
    os.makedirs('models', exist_ok=True)
    joblib.dump(reg, 'models/price_regressor.pkl')
    joblib.dump(clf, 'models/price_classifier.pkl')
    print('Saved models to models/')


if __name__ == '__main__':
    train_and_save()
