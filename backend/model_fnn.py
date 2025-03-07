import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, RobustScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from scipy import stats
import joblib
import datetime
import warnings
warnings.filterwarnings('ignore')

# Function to load and preprocess the data
def load_and_preprocess(file_path, target_col='cortisol'):
    # Load the data
    print(f"Loading data from {file_path}...")
    df = pd.read_csv(file_path)
    
    # Display basic information
    print("\nDataset Overview:")
    print(f"Shape: {df.shape}")
    print("\nFirst 5 rows:")
    print(df.head())
    
    # Check for missing values
    print("\nMissing values:")
    print(df.isnull().sum())
    
    # Basic statistics
    print("\nBasic statistics:")
    print(df.describe())
    
    # Handle missing values if any
    if df.isnull().sum().sum() > 0:
        print("\nHandling missing values...")
        # For numerical columns, fill with median
        for col in df.columns:
            if df[col].dtype in ['int64', 'float64']:
                df[col] = df[col].fillna(df[col].median())
    
    # Check for outliers using IQR
    print("\nChecking for outliers...")
    Q1 = df.quantile(0.25)
    Q3 = df.quantile(0.75)
    IQR = Q3 - Q1
    outliers = ((df < (Q1 - 1.5 * IQR)) | (df > (Q3 + 1.5 * IQR))).sum()
    print(f"Number of potential outliers per column:\n{outliers}")
    
    # Split features and target
    X = df.drop(target_col, axis=1)
    y = df[target_col]
    
    return X, y, df

# Feature engineering function
def engineer_features(X, y=None):
    print("\nEngineering features...")
    X_new = X.copy()
    
    # Ratio features
    X_new['ir_to_red_ratio'] = X['ir'] / X['red'].replace(0, 0.001)  # Avoid division by zero
    
    # Log transforms for skewed features
    for col in X.columns:
        # Only check skewness if y is provided (during training)
        if y is not None:
            skewness = stats.skew(X[col])
            if skewness > 0.5:
                X_new[f'{col}_log'] = np.log1p(X[col] - X[col].min() + 1 if X[col].min() <= 0 else X[col])
        else:
            # During prediction, add log features for all columns to match training
            X_new[f'{col}_log'] = np.log1p(X[col] - X[col].min() + 1 if X[col].min() <= 0 else X[col])
    
    # Interaction features
    X_new['ir_heart_rate'] = X['ir'] * X['heart_rate']
    X_new['red_heart_rate'] = X['red'] * X['heart_rate']
    X_new['gsr_heart_rate'] = X['gsr'] * X['heart_rate']
    
    # Polynomial features for key relationships
    X_new['heart_rate_squared'] = X['heart_rate'] ** 2
    X_new['gsr_squared'] = X['gsr'] ** 2
    
    if y is not None:
        print(f"Added {X_new.shape[1] - X.shape[1]} new features. New shape: {X_new.shape}")
    
    return X_new

# Function to explore correlations and feature importance
def explore_relationships(X, y, df):
    print("\nExploring feature relationships...")
    
    # Correlation matrix
    correlation = df.corr()
    
    # Display target correlations sorted
    target_corr = correlation[y.name].drop(y.name).sort_values(ascending=False)
    print(f"\nCorrelations with {y.name}:")
    print(target_corr)
    
    # Train a quick Random Forest to get feature importances
    rf = RandomForestRegressor(n_estimators=100, random_state=42)
    rf.fit(X, y)
    
    # Get feature importances
    importances = pd.DataFrame({
        'Feature': X.columns,
        'Importance': rf.feature_importances_
    }).sort_values('Importance', ascending=False)
    
    print("\nFeature importances from Random Forest:")
    print(importances)
    
    return target_corr, importances

# Function to find the best performing model without optimization
def find_best_model(X, y):
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Scale the features
    scaler = RobustScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    print("\nTraining multiple models to find the best one...")
    
    # Define base models
    models = {
        'XGBoost': XGBRegressor(random_state=42, objective='reg:squarederror'),
        'LightGBM': LGBMRegressor(random_state=42),
        'Neural Network': MLPRegressor(random_state=42, max_iter=2000),
        'SVR': SVR(),
        'Random Forest': RandomForestRegressor(random_state=42)
    }
    
    # Dictionary to store results
    results = {}
    
    # Train and evaluate each model
    for name, model in models.items():
        print(f"\nTraining {name}...")
        model.fit(X_train_scaled, y_train)
        
        # Predict on test set
        y_pred = model.predict(X_test_scaled)
        
        # Calculate metrics
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)
        
        # Calculate custom accuracy metric for regression
        y_range = y_test.max() - y_test.min()
        accuracy = 1 - (rmse / y_range)
        accuracy_percentage = accuracy * 100
        
        # Store results
        results[name] = {
            'MSE': mse,
            'RMSE': rmse,
            'R2': r2,
            'MAE': mae,
            'Accuracy': accuracy_percentage,
            'Model': model
        }
        
        print(f"  {name} Results:")
        print(f"  - MSE: {mse:.4f}")
        print(f"  - RMSE: {rmse:.4f}")
        print(f"  - R2 Score: {r2:.4f}")
        print(f"  - Accuracy: {accuracy_percentage:.2f}%")
    
    # Find the best model
    best_model_name = max(results, key=lambda k: results[k]['Accuracy'])
    best_model = results[best_model_name]['Model']
    best_accuracy = results[best_model_name]['Accuracy']
    
    print(f"\nBest Model: {best_model_name} with accuracy {best_accuracy:.2f}%")
    
    return best_model, scaler, X_engineered.columns.tolist(), best_model_name, best_accuracy

# Save the trained model and scaler
def save_model(model, scaler, feature_names=None, file_prefix="physiological_data"):
    # Create timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save model and scaler
    model_filename = f"{file_prefix}_model_{timestamp}.joblib"
    scaler_filename = f"{file_prefix}_scaler_{timestamp}.joblib"
    
    print(f"\nSaving model to {model_filename}")
    joblib.dump(model, model_filename)
    
    print(f"Saving scaler to {scaler_filename}")
    joblib.dump(scaler, scaler_filename)
    
    # If feature names are provided, save them too
    if feature_names is not None:
        features_filename = f"{file_prefix}_features_{timestamp}.joblib"
        print(f"Saving feature names to {features_filename}")
        joblib.dump(feature_names, features_filename)
        return model_filename, scaler_filename, features_filename
    
    return model_filename, scaler_filename

# Function to make predictions with the trained model
def predict_with_model(model, scaler, data, engineered_features=None):
    """
    Makes predictions using the trained model
    
    Parameters:
    -----------
    model : trained model
        The trained ML model
    scaler : fitted scaler
        The scaler used to scale the training data
    data : pandas DataFrame
        Data to predict on, must have same columns as training data
    engineered_features : list, optional
        List of feature names after engineering
        
    Returns:
    --------
    predictions : numpy array
        Model predictions
    """
    # Check if data has the required columns
    original_features = ['ir', 'red', 'heart_rate', 'gsr']
    missing_cols = [col for col in original_features if col not in data.columns]
    
    if missing_cols:
        raise ValueError(f"Data is missing required columns: {missing_cols}")
    
    # Engineer features
    data_eng = engineer_features(data)
    
    # If engineered_features is provided, ensure we have the same columns in the same order
    if engineered_features is not None:
        # Add missing columns with zeros
        for col in engineered_features:
            if col not in data_eng.columns:
                data_eng[col] = 0
                
        # Select only needed columns in the right order
        data_eng = data_eng[engineered_features]
    
    # Scale the data
    data_scaled = scaler.transform(data_eng)
    
    # Make predictions
    predictions = model.predict(data_scaled)
    
    return predictions

# Function to run the simplified pipeline
def run_simple_ml_pipeline(file_path, target_col='cortisol', save=True):
    print("Starting Simple ML Pipeline for Physiological Data\n" + "="*50)
    
    # Load and preprocess data
    X, y, df = load_and_preprocess(file_path, target_col)
    
    # Explore relationships
    target_corr, importances = explore_relationships(X, y, df)
    
    # Engineer features
    global X_engineered
    X_engineered = engineer_features(X, y)
    
    # Find the best model without optimization
    best_model, scaler, features, model_name, accuracy = find_best_model(X_engineered, y)
    
    print("\n" + "="*50)
    print(f"Best Model: {model_name}")
    print(f"Accuracy: {accuracy:.2f}%")
    print("="*50)
    
    # Save the model if requested
    if save:
        saved_files = save_model(best_model, scaler, features)
        print(f"\nModel and related files saved successfully.")
        
    # Return the artifacts
    return {
        'model': best_model,
        'scaler': scaler,
        'feature_importance': importances,
        'accuracy': accuracy,
        'model_name': model_name,
        'engineered_features': features
    }

# Main execution
if __name__ == "__main__":
    # Example usage:
    file_path = "cleaned_gsr_dataset.csv"  # Replace with your file path
    
    # Run the pipeline
    artifacts = run_simple_ml_pipeline(file_path, target_col='cortisol', save=True)
    
    # Print final results
    print(f"\nFinal Results:")
    print(f"Best model: {artifacts['model_name']}")
    print(f"Accuracy: {artifacts['accuracy']:.2f}%")
    
    # Example of how to use the model for predictions
    """
    # Load new data for predictions
    new_data = pd.read_csv("new_samples.csv")
    
    # Make predictions
    predictions = predict_with_model(
        artifacts['model'], 
        artifacts['scaler'], 
        new_data, 
        artifacts['engineered_features']
    )
    
    print("Predictions for new data:")
    print(predictions)
    """