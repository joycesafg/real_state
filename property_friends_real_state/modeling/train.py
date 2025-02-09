import pandas as pd
import joblib
from category_encoders import TargetEncoder
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from pathlib import Path
import typer
from loguru import logger

# App initialization
app = typer.Typer()

# Paths (set default or use parameters)
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_TRAIN_PATH = PROJECT_ROOT / "data/processed/train.csv"
DEFAULT_TEST_PATH = PROJECT_ROOT / "data/processed/test.csv"
DEFAULT_MODEL_PATH = PROJECT_ROOT / "property_friends_real_state/app"

def load_data(train_path: str, test_path: str):
    """
    Loads the train and test datasets into pandas DataFrames.
    """
    try:
        train = pd.read_csv(train_path)
        test = pd.read_csv(test_path)
        logger.info(f"Successfully loaded data from {train_path} and {test_path}")
        return train, test
    except Exception as e:
        logger.error(f"Error loading data: {e}")
        raise

def build_preprocessor():
    """
    Builds the column transformer with target encoding for categorical features.
    """
    categorical_cols = ["type", "sector"]
    categorical_transformer = TargetEncoder()
    
    preprocessor = ColumnTransformer(
        transformers=[('categorical', categorical_transformer, categorical_cols)]
    )
    
    return preprocessor

def build_model():
    """
    Build and return the GradientBoostingRegressor model.
    """
    return GradientBoostingRegressor(
        random_state=42, 
        learning_rate=0.01,
        n_estimators=300,
        max_depth=5,
        loss="absolute_error"
    )

def save_model(pipeline, model_path):
    """
    Saves the trained pipeline model to the specified path.
    """
    model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, model_path / "model.pkl")
    logger.success(f"Model saved to {model_path}/model.pkl")

@app.command()
def main(
    train_path: Path = DEFAULT_TRAIN_PATH,
    test_path: Path = DEFAULT_TEST_PATH,
    model_path: Path = DEFAULT_MODEL_PATH,
):
    """
    Main function to train and save the modelo.
    """
    logger.info(f"Using paths - Train: {train_path}, Test: {test_path}, Model: {model_path}")
    
    # Load data
    train, test = load_data(train_path, test_path)
    
    train_cols = [col for col in train.columns if col not in ['id', 'target']]
    target = "price"
    
    # Build preprocessing and model pipeline
    preprocessor = build_preprocessor()
    model = build_model()
    
    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('model', model)
    ])
    
    # Fit the model
    logger.info("Training model...")
    pipeline.fit(train[train_cols], train[target])
    
    # Save the model
    save_model(pipeline, model_path)
    logger.success("Model training complete!")

if __name__ == "__main__":
    app()
