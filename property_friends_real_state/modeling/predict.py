import pandas as pd
import joblib
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import typer
from loguru import logger
from sklearn.metrics import mean_squared_error, mean_absolute_error, mean_absolute_percentage_error

# App initialization
app = typer.Typer()

def print_metrics(predictions, target):
    """
    Compute and print the performance metrics for model evaluation.
    """
    rmse = np.sqrt(mean_squared_error(predictions, target))
    mape = mean_absolute_percentage_error(predictions, target)
    mae = mean_absolute_error(predictions, target)
    
    # Print metrics
    logger.info(f"RMSE: {rmse}")
    logger.info(f"MAPE: {mape}")
    logger.info(f"MAE: {mae}")

    return rmse, mape, mae


def plot_metrics(rmse, mape, mae):
    """
    Plot the performance metrics (RMSE, MAPE, MAE) in a bar chart.
    """
    metrics = {'RMSE': rmse, 'MAPE': mape, 'MAE': mae}
    plt.figure(figsize=(10, 6))
    plt.bar(metrics.keys(), metrics.values(), color=['blue', 'orange', 'green'])
    plt.title('Model Evaluation Metrics')
    plt.ylabel('Value')
    plt.xlabel('Metric')
    plt.tight_layout()
    plt.savefig('model_metrics.png')
    logger.info("Metrics plot saved as 'model_metrics.png'.")


@app.command()
def main(
    test_path: Path = Path(__file__).resolve().parents[2] / "data/processed/test.csv",
    model_path: Path = Path(__file__).resolve().parents[1] / "app/model.pkl"
):
    """
    Main function to load the model, perform inference, and evaluate performance metrics.
    """
    logger.info("Performing inference for model...")
    target = "price"
    
    # Load the test data
    test = pd.read_csv(test_path)
    
    # Load the trained model pipeline
    pipeline = joblib.load(model_path)
    
    # Get feature names used for inference
    feature_names = pipeline[0].feature_names_in_
    
    # Perform inference
    test_predictions = pipeline.predict(test[feature_names])
    test_target = test[target].values
    
    # Print metrics
    rmse, mape, mae = print_metrics(test_predictions, test_target)
    
    # Plot and save metrics
    plot_metrics(rmse, mape, mae)

    logger.success("Inference complete and metrics saved.")
    

if __name__ == "__main__":
    app()
