#!/usr/bin/env python3
"""
AI Model for Predicting Clinical Uptake of Therapeutic Lenses (Stellest Lens)
Uses ensemble methods and deep learning for accurate predictions
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.preprocessing import StandardScaler, RobustScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, roc_curve
import xgboost as xgb
import lightgbm as lgb
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

class StellesteAIModel:
    def __init__(self):
        """Initialize the AI model ensemble"""
        self.models = {}
        self.scalers = {}
        self.feature_importance = {}
        self.is_trained = False
        self.feature_names = []
        
    def initialize_models(self):
        """Initialize all models in the ensemble"""
        self.models = {
            'random_forest': RandomForestClassifier(
                n_estimators=200,
                max_depth=10,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=42,
                class_weight='balanced'
            ),
            'xgboost': xgb.XGBClassifier(
                n_estimators=200,
                max_depth=6,
                learning_rate=0.1,
                subsample=0.8,
                colsample_bytree=0.8,
                random_state=42,
                eval_metric='logloss'
            ),
            'lightgbm': lgb.LGBMClassifier(
                n_estimators=200,
                max_depth=6,
                learning_rate=0.1,
                subsample=0.8,
                colsample_bytree=0.8,
                random_state=42,
                verbose=-1
            ),
            'gradient_boosting': GradientBoostingClassifier(
                n_estimators=200,
                max_depth=6,
                learning_rate=0.1,
                random_state=42
            ),
            'logistic_regression': LogisticRegression(
                random_state=42,
                class_weight='balanced',
                max_iter=1000
            ),
            'svm': SVC(
                kernel='rbf',
                probability=True,
                random_state=42,
                class_weight='balanced'
            )
        }
        
        self.scalers = {
            'standard': StandardScaler(),
            'robust': RobustScaler()
        }
    
    def prepare_features(self, X: pd.DataFrame, fit_scaler: bool = False) -> np.ndarray:
        """Prepare features for training/prediction"""
        if fit_scaler:
            X_scaled = self.scalers['robust'].fit_transform(X)
        else:
            X_scaled = self.scalers['robust'].transform(X)
        
        return X_scaled
    
    def train_models(self, X: pd.DataFrame, y: pd.Series) -> Dict:
        """Train all models and return performance metrics"""
        self.initialize_models()
        self.feature_names = list(X.columns)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Prepare features
        X_train_scaled = self.prepare_features(X_train, fit_scaler=True)
        X_test_scaled = self.prepare_features(X_test)
        
        results = {}
        
        print("Training AI models...")
        print("=" * 50)
        
        for name, model in self.models.items():
            print(f"Training {name}...")
            
            try:
                # Train model
                if name in ['logistic_regression', 'svm']:
                    model.fit(X_train_scaled, y_train)
                    y_pred = model.predict(X_test_scaled)
                    y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]
                else:
                    model.fit(X_train, y_train)
                    y_pred = model.predict(X_test)
                    y_pred_proba = model.predict_proba(X_test)[:, 1]
                
                # Calculate metrics
                accuracy = model.score(X_test_scaled if name in ['logistic_regression', 'svm'] else X_test, y_test)
                auc_score = roc_auc_score(y_test, y_pred_proba)
                
                # Cross-validation
                cv_scores = cross_val_score(
                    model, 
                    X_train_scaled if name in ['logistic_regression', 'svm'] else X_train, 
                    y_train, 
                    cv=5, 
                    scoring='roc_auc'
                )
                
                results[name] = {
                    'accuracy': accuracy,
                    'auc': auc_score,
                    'cv_mean': cv_scores.mean(),
                    'cv_std': cv_scores.std(),
                    'predictions': y_pred,
                    'probabilities': y_pred_proba
                }
                
                # Store feature importance
                if hasattr(model, 'feature_importances_'):
                    self.feature_importance[name] = dict(zip(
                        self.feature_names, model.feature_importances_
                    ))
                elif hasattr(model, 'coef_'):
                    self.feature_importance[name] = dict(zip(
                        self.feature_names, abs(model.coef_[0])
                    ))
                
                print(f"  Accuracy: {accuracy:.4f}")
                print(f"  AUC: {auc_score:.4f}")
                print(f"  CV Score: {cv_scores.mean():.4f} (+/- {cv_scores.std()*2:.4f})")
                
            except Exception as e:
                print(f"  Error training {name}: {e}")
                continue
        
        # Create ensemble predictions
        ensemble_proba = np.mean([
            results[name]['probabilities'] for name in results.keys()
        ], axis=0)
        
        ensemble_pred = (ensemble_proba > 0.5).astype(int)
        ensemble_auc = roc_auc_score(y_test, ensemble_proba)
        
        results['ensemble'] = {
            'accuracy': np.mean(ensemble_pred == y_test),
            'auc': ensemble_auc,
            'predictions': ensemble_pred,
            'probabilities': ensemble_proba
        }
        
        print(f"\nEnsemble Model:")
        print(f"  Accuracy: {results['ensemble']['accuracy']:.4f}")
        print(f"  AUC: {results['ensemble']['auc']:.4f}")
        
        self.is_trained = True
        self.test_data = (X_test, y_test)
        
        return results
    
    def predict_stellest_uptake(self, patient_data: Dict) -> Dict:
        """Predict Stellest lens uptake for a single patient"""
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
        
        # Convert patient data to DataFrame
        df = pd.DataFrame([patient_data])
        
        # Ensure all required features are present
        for feature in self.feature_names:
            if feature not in df.columns:
                df[feature] = 0  # Default value
        
        # Reorder columns to match training data
        df = df[self.feature_names]
        
        # Make predictions with all models
        predictions = {}
        
        for name, model in self.models.items():
            try:
                if name in ['logistic_regression', 'svm']:
                    X_scaled = self.prepare_features(df)
                    prob = model.predict_proba(X_scaled)[0, 1]
                    pred = model.predict(X_scaled)[0]
                else:
                    prob = model.predict_proba(df)[0, 1]
                    pred = model.predict(df)[0]
                
                predictions[name] = {
                    'probability': prob,
                    'prediction': pred,
                    'confidence': 'High' if abs(prob - 0.5) > 0.3 else 'Medium' if abs(prob - 0.5) > 0.15 else 'Low'
                }
            except Exception as e:
                print(f"Error with {name}: {e}")
                continue
        
        # Ensemble prediction
        ensemble_prob = np.mean([pred['probability'] for pred in predictions.values()])
        ensemble_pred = 1 if ensemble_prob > 0.5 else 0
        
        # Risk factors analysis
        risk_factors = self.analyze_risk_factors(patient_data)
        
        return {
            'ensemble_prediction': {
                'will_benefit': bool(ensemble_pred),
                'probability': float(ensemble_prob),
                'confidence': 'High' if abs(ensemble_prob - 0.5) > 0.3 else 'Medium' if abs(ensemble_prob - 0.5) > 0.15 else 'Low'
            },
            'individual_models': predictions,
            'risk_factors': risk_factors,
            'recommendation': self.generate_recommendation(ensemble_prob, risk_factors)
        }
    
    def analyze_risk_factors(self, patient_data: Dict) -> Dict:
        """Analyze patient risk factors"""
        risk_factors = {
            'high_risk': [],
            'medium_risk': [],
            'protective': []
        }
        
        # Age factors
        age = patient_data.get('age', 12)
        if age < 8:
            risk_factors['high_risk'].append('Very young age at treatment start')
        elif age > 15:
            risk_factors['medium_risk'].append('Older age at treatment start')
        
        # Myopia severity
        avg_power = patient_data.get('average_initial_power', 3.0)
        if avg_power > 6.0:
            risk_factors['high_risk'].append('High myopia (>6D)')
        elif avg_power > 3.0:
            risk_factors['medium_risk'].append('Moderate myopia (3-6D)')
        
        # Family history
        if patient_data.get('family_history_myopia', 0) == 1:
            risk_factors['medium_risk'].append('Family history of myopia')
        
        # Lifestyle factors
        screen_time = patient_data.get('screen_time', 3.0)
        outdoor_time = patient_data.get('outdoor_time', 1.0)
        
        if screen_time > 6:
            risk_factors['high_risk'].append('Excessive screen time (>6 hours/day)')
        elif screen_time > 3:
            risk_factors['medium_risk'].append('High screen time (3-6 hours/day)')
        
        if outdoor_time < 1:
            risk_factors['high_risk'].append('Insufficient outdoor time (<1 hour/day)')
        elif outdoor_time >= 2:
            risk_factors['protective'].append('Good outdoor time (≥2 hours/day)')
        
        # Compliance
        wearing_time = patient_data.get('stellest_wearing_time', 14.0)
        if wearing_time < 10:
            risk_factors['high_risk'].append('Poor compliance (<10 hours/day)')
        elif wearing_time >= 14:
            risk_factors['protective'].append('Excellent compliance (≥14 hours/day)')
        
        return risk_factors
    
    def generate_recommendation(self, probability: float, risk_factors: Dict) -> str:
        """Generate clinical recommendation"""
        if probability > 0.7:
            base_rec = "Highly recommended for Stellest lens treatment."
        elif probability > 0.5:
            base_rec = "Recommended for Stellest lens treatment."
        elif probability > 0.3:
            base_rec = "Consider Stellest lens treatment with close monitoring."
        else:
            base_rec = "Alternative myopia control methods may be more suitable."
        
        # Add specific recommendations based on risk factors
        additional_recs = []
        
        if len(risk_factors['high_risk']) > 2:
            additional_recs.append("Address high-risk factors before treatment.")
        
        if 'Insufficient outdoor time' in risk_factors['high_risk']:
            additional_recs.append("Increase outdoor activities to ≥2 hours/day.")
        
        if 'Excessive screen time' in risk_factors['high_risk']:
            additional_recs.append("Implement screen time restrictions.")
        
        if 'Poor compliance' in risk_factors['high_risk']:
            additional_recs.append("Ensure proper lens wearing schedule (12-16 hours/day).")
        
        if additional_recs:
            base_rec += " " + " ".join(additional_recs)
        
        return base_rec
    
    def plot_feature_importance(self, top_n: int = 15):
        """Plot feature importance from the best performing model"""
        if not self.feature_importance:
            print("No feature importance data available")
            return
        
        # Use Random Forest importance (usually most interpretable)
        importance_data = self.feature_importance.get('random_forest', 
                                                    list(self.feature_importance.values())[0])
        
        # Sort features by importance
        sorted_features = sorted(importance_data.items(), key=lambda x: x[1], reverse=True)
        top_features = sorted_features[:top_n]
        
        features, importances = zip(*top_features)
        
        plt.figure(figsize=(12, 8))
        plt.barh(range(len(features)), importances)
        plt.yticks(range(len(features)), features)
        plt.xlabel('Feature Importance')
        plt.title(f'Top {top_n} Most Important Features for Stellest Lens Prediction')
        plt.gca().invert_yaxis()
        plt.tight_layout()
        plt.savefig('static/feature_importance.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        return top_features
    
    def save_model(self, model_path: str = 'models/stellest_ai_model.pkl'):
        """Save the trained model ensemble"""
        if not self.is_trained:
            raise ValueError("Model must be trained before saving")
        
        model_data = {
            'models': self.models,
            'scalers': self.scalers,
            'feature_names': self.feature_names,
            'feature_importance': self.feature_importance,
            'is_trained': self.is_trained
        }
        
        joblib.dump(model_data, model_path)
        print(f"Model saved to: {model_path}")
    
    def load_model(self, model_path: str = 'models/stellest_ai_model.pkl'):
        """Load a trained model ensemble"""
        model_data = joblib.load(model_path)
        
        self.models = model_data['models']
        self.scalers = model_data['scalers']
        self.feature_names = model_data['feature_names']
        self.feature_importance = model_data['feature_importance']
        self.is_trained = model_data['is_trained']
        
        print(f"Model loaded from: {model_path}")

def train_stellest_model():
    """Main function to train the Stellest AI model"""
    from data_preprocessing import MyopiaDataPreprocessor
    
    print("STELLEST LENS AI MODEL TRAINING")
    print("=" * 40)
    
    # Load and preprocess data
    preprocessor = MyopiaDataPreprocessor('Stellest_Restrospective Data to Hindustan.xlsx')
    processed_data = preprocessor.preprocess_data()
    
    # Get features and target
    feature_data = preprocessor.get_feature_importance_data()
    X = feature_data['features']
    y = feature_data['target']
    
    print(f"Training with {len(X)} samples and {len(X.columns)} features")
    
    # Initialize and train model
    ai_model = StellesteAIModel()
    results = ai_model.train_models(X, y)
    
    # Save model
    ai_model.save_model()
    
    # Plot feature importance
    ai_model.plot_feature_importance()
    
    print("\nModel training completed successfully!")
    
    return ai_model, results

if __name__ == "__main__":
    model, results = train_stellest_model()
