import os
import boto3
import pandas as pd
from pathlib import Path
import typer
from loguru import logger
from typing import Dict

# App initialization
app = typer.Typer()

# AWS Configuration (use environment variables for security)
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
S3_BUCKET = "case-property-friends"

# S3 file paths
S3_FILES = {
    "test": "test.csv",
    "train": "train.csv"
}

# Define project root and local data paths
PROJ_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJ_ROOT / "data/processed"
DATA_DIR.mkdir(parents=True, exist_ok=True)  # Ensure directory exists

logger.info(f"Project root: {PROJ_ROOT}")
logger.info(f"Data directory: {DATA_DIR}")

# Initialize S3 client
s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY
)


def download_data(s3_key: str, local_path: Path) -> None:
    """Download file from S3 only if it does not exist locally."""
    if local_path.exists():
        logger.info(f"File already exists: {local_path}, skipping download.")
        return

    try:
        s3_client.download_file(S3_BUCKET, s3_key, str(local_path))
        logger.info(f"Downloaded {s3_key} to {local_path}")
    except Exception as e:
        logger.error(f"Failed to download {s3_key} from S3: {e}")


def load_data(file_path: Path) -> pd.DataFrame:
    """Load CSV data into a pandas DataFrame."""
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        logger.error(f"Error loading {file_path}: {e}")
        return None


# Main function
@app.command()
def main(
    test_path: Path = DATA_DIR / "test.csv",
    train_path: Path = DATA_DIR / "train.csv",
) -> None:
    """Download and load the train and test datasets."""
    # Download and load datasets
    datasets: Dict[str, pd.DataFrame] = {}
    for name, s3_key in S3_FILES.items():
        local_path = DATA_DIR / s3_key
        download_data(s3_key, local_path)
        datasets[name] = load_data(local_path)

    # Print sample data for the test set
    if datasets.get("test") is not None:
        logger.info("Test Data Loaded Successfully!")
        print(datasets["test"].head())


if __name__ == "__main__":
    app()
