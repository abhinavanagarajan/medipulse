import pandas as pd
import joblib
import numpy as np

def load_saved_model(model_file, scaler_file, features_file=None):
    """
    Load a saved model and its associated files
    
    Parameters:
    -----------
    model_file : str
        Path to the saved model file
    scaler_file : str
        Path to the saved scaler file
    features_file : str, optional
        Path to the saved features file
        
    Returns:
    --------
    model : trained model
        The loaded ML model
    scaler : fitted scaler
        The loaded scaler
    features : list, optional
        List of feature names if features_file is provided
    """
    print(f"Loading model from {model_file}")
    model = joblib.load(model_file)
    
    print(f"Loading scaler from {scaler_file}")
    scaler = joblib.load(scaler_file)
    
    features = None
    if features_file:
        print(f"Loading feature names from {features_file}")
        features = joblib.load(features_file)
    
    return model, scaler, features

def engineer_features(X):
    """
    Apply the same feature engineering that was used during training
    
    Parameters:
    -----------
    X : pandas DataFrame
        Input data with original features
        
    Returns:
    --------
    X_new : pandas DataFrame
        Data with engineered features
    """
    print("Engineering features for prediction...")
    X_new = X.copy()
    
    # Ratio features
    X_new['ir_to_red_ratio'] = X['ir'] / X['red'].replace(0, 0.001)  # Avoid division by zero
    
    # Log transforms for all columns
    for col in X.columns:
        X_new[f'{col}_log'] = np.log1p(X[col] - X[col].min() + 1 if X[col].min() <= 0 else X[col])
    
    # Interaction features
    X_new['ir_heart_rate'] = X['ir'] * X['heart_rate']
    X_new['red_heart_rate'] = X['red'] * X['heart_rate']
    X_new['gsr_heart_rate'] = X['gsr'] * X['heart_rate']
    
    # Polynomial features for key relationships
    X_new['heart_rate_squared'] = X['heart_rate'] ** 2
    X_new['gsr_squared'] = X['gsr'] ** 2
    
    return X_new

def predict_with_model(model, scaler, data, engineered_features=None):
    """
    Makes predictions using the trained model
    
    Parameters:
    -----------
    model : trained model
        The trained ML model
    scaler : fitted scaler
        The scaler used to scale the training data
    data : pandas DataFrame or list
        Data to predict on, must have same columns as training data
    engineered_features : list, optional
        List of feature names after engineering
        
    Returns:
    --------
    predictions : numpy array
        Model predictions
    """
    # Check if data is in the correct format
    if isinstance(data, list):
        data = pd.DataFrame([data], columns=['ir', 'red', 'heart_rate', 'gsr'])
    
    # Check if data has the required columns
    missing_cols = [col for col in ['ir', 'red', 'heart_rate', 'gsr'] if col not in data.columns]
    
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
    print(predictions[0]
    )
    return predictions[0]

# Example usage
if __name__ == "__main__":
    # Replace these with your actual saved model filenames
    model_file = "physiological_data_model_20250306_163919.joblib"
    scaler_file = "physiological_data_scaler_20250306_163919.joblib"
    features_file = "physiological_data_features_20250306_163919.joblib"
    
    # Load the saved model and associated files
    model, scaler, features = load_saved_model(model_file, scaler_file, features_file)
    
    # Define new data for predictions (replace with actual values)
    # Example: a list of values for ['ir', 'red', 'heart_rate', 'gsr']
    new_data = [2230,1312,88,1453]
    
    # Make predictions
    predictions = predict_with_model(model, scaler, new_data, features)
    
    # Display predictions
    print("\nPredictions for new data:")
    print(predictions)
    
    # Optionally, you can save predictions to a file
    result_df = pd.DataFrame([new_data], columns=['ir', 'red', 'heart_rate', 'gsr'])
    result_df['predicted_cortisol'] = predictions
    result_df.to_csv("prediction_results.csv", index=False)
    print("\nPredictions saved to 'prediction_results.csv'")
