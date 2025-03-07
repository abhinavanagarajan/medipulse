import joblib
import numpy as np
import os

def load_saved_model(model_file, scaler_file, features_file):
    """Load the saved model and associated files with debug info."""
    try:
        # Check if files exist
        for file in [model_file, scaler_file, features_file]:
            if not os.path.exists(file):
                print(f"File not found: {file}")
                return None, None, None

        # Load files with debug info
        print(f"Loading model from {model_file}")
        model = joblib.load(model_file)
        print(f"Model type: {type(model)}")

        print(f"Loading scaler from {scaler_file}")
        scaler = joblib.load(scaler_file)
        print(f"Scaler type: {type(scaler)}")

        print(f"Loading features from {features_file}")
        features = joblib.load(features_file)
        print(f"Features type: {type(features)}")
        print(f"Features shape/length: {len(features) if isinstance(features, list) else features.shape}")

        return model, scaler, features

    except Exception as e:
        print(f"Error loading model files: {str(e)}")
        return None, None, None

def predict_with_model(model, scaler, input_data, features):
    """Make predictions with extensive error checking and debugging."""
    try:
        # Input validation
        if None in [model, scaler, features]:
            print("Model components not properly loaded")
            return 10.0

        if input_data is None or len(input_data) != 4:
            print(f"Invalid input data. Expected 4 features, got: {input_data}")
            return 10.0

        # Convert input to float array
        input_array = np.array(input_data, dtype=np.float32).reshape(1, -1)
        print(f"Input array shape: {input_array.shape}")
        print(f"Input array dtype: {input_array.dtype}")
        print(f"Input values: {input_array}")

        # Scale input
        try:
            scaled_input = scaler.transform(input_array)
            print(f"Scaled input shape: {scaled_input.shape}")
            print(f"Scaled input dtype: {scaled_input.dtype}")
        except Exception as e:
            print(f"Scaling error: {str(e)}")
            return 10.0

        # Make prediction
        try:
            prediction = model.predict(scaled_input)
            print(f"Prediction value: {prediction[0]}")
            return float(prediction[0])
        except Exception as e:
            print(f"Prediction error: {str(e)}")
            return 10.0

    except Exception as e:
        print(f"General prediction error: {str(e)}")
        return 10.0
