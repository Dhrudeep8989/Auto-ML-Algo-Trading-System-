# # src/ml_model.py

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
import config

class MLPredictor:
    """ML model using Random Forest"""

    def __init__(self):
        self.model = None
        self.accuracy = None
        self.scaler = None

    def train_model(self, stock_data_dict):
        print("🤖 Training Random Forest Model...")
        all_features = []
        all_targets = []

        for symbol, data in stock_data_dict.items():
            if data is not None:
                required_cols = ['RSI', 'MACD', 'Volume_Ratio', 'MA_20', 'MA_50', 'Next_Day_Up']
                if not all(col in data.columns for col in required_cols):
                    continue

                features = data[['RSI', 'MACD', 'Volume_Ratio', 'MA_20', 'MA_50']].copy()
                targets = data['Next_Day_Up'].copy()

                # Advanced feature engineering
                features['MA_diff'] = features['MA_20'] - features['MA_50']
                features['RSI_MA'] = features['RSI'] / (features['MA_50'] + 1)
                features['MACD_Squared'] = features['MACD'] ** 2
                features['Volatility'] = (features['MA_20'] - features['MA_50']).abs() / (features['MA_50'] + 1)

                combined = pd.concat([features, targets], axis=1).dropna()
                if not combined.empty:
                    all_features.append(combined.iloc[:, :-1])
                    all_targets.append(combined.iloc[:, -1])

        if not all_features:
            print("❌ No training data available")
            return None

        # Concatenate data
        X = pd.concat(all_features, ignore_index=True)
        y = pd.concat(all_targets, ignore_index=True)

        # Normalize with StandardScaler
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X)

        # Train/test split
        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y, test_size=config.ML_TEST_SIZE, random_state=config.ML_RANDOM_STATE
        )

        # Optimized RandomForest with grid tuning
        param_grid = {
            'n_estimators': [100, 150],
            'max_depth': [5, 10, None],
            'min_samples_split': [2, 4],
            'max_features': ['sqrt', 'log2']
        }

        grid = GridSearchCV(RandomForestClassifier(random_state=config.ML_RANDOM_STATE),
                            param_grid, cv=3, n_jobs=-1)
        grid.fit(X_train, y_train)
        self.model = grid.best_estimator_

        y_pred = self.model.predict(X_test)
        self.accuracy = accuracy_score(y_test, y_pred)
        print(f"✅ Optimized RF Accuracy: {self.accuracy:.1%}")
        return self.model

    def predict(self, features):
        if self.model is None or self.scaler is None:
            return None

        try:
            # Reconstruct all engineered features
            RSI, MACD, Volume_Ratio, MA_20, MA_50 = features
            MA_diff = MA_20 - MA_50
            RSI_MA = RSI / (MA_50 + 1)
            MACD_Squared = MACD ** 2
            Volatility = abs(MA_20 - MA_50) / (MA_50 + 1)

            full_features = [RSI, MACD, Volume_Ratio, MA_20, MA_50,
                             MA_diff, RSI_MA, MACD_Squared, Volatility]
            scaled = self.scaler.transform([full_features])

            prediction = self.model.predict(scaled)[0]
            proba = self.model.predict_proba(scaled)[0]
            return {
                'prediction': 'UP' if prediction == 1 else 'DOWN',
                'confidence': max(proba)
            }
        except Exception as e:
            print(f"❌ Prediction error: {e}")
            return None
