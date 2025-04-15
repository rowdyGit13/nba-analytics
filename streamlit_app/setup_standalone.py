import os
import shutil
import sys
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def setup_standalone_environment():
    """
    Prepare the environment for running Streamlit in standalone mode by:
    1. Ensuring data directories exist
    2. Moving any CSV files to the correct location
    """
    # Current script directory
    current_dir = Path(__file__).resolve().parent
    
    # Create the processed data directory if it doesn't exist
    data_dir = current_dir / "data"
    processed_dir = data_dir / "processed"
    
    data_dir.mkdir(exist_ok=True)
    processed_dir.mkdir(exist_ok=True)
    
    logger.info(f"Created data directories: {data_dir}, {processed_dir}")
    
    # Check if there are CSV files in the data directory that need to be moved to processed
    csv_files_in_data = list(data_dir.glob("*.csv"))
    if csv_files_in_data:
        logger.info(f"Found {len(csv_files_in_data)} CSV files in data directory")
        
        # Copy these files to the processed directory if they don't exist there
        for csv_file in csv_files_in_data:
            target_file = processed_dir / csv_file.name
            if not target_file.exists():
                shutil.copy2(csv_file, target_file)
                logger.info(f"Copied {csv_file.name} to processed directory")
    
    # Check that we have all the required CSV files in the processed directory
    required_files = ["players.csv", "teams.csv", "games.csv", 
                      "team_metrics.csv", "team_rankings.csv"]
    
    missing_files = []
    for required_file in required_files:
        if not (processed_dir / required_file).exists():
            missing_files.append(required_file)
    
    if missing_files:
        logger.warning(f"Missing required CSV files in processed directory: {', '.join(missing_files)}")
        logger.warning("The app might not function correctly without these files.")
    else:
        logger.info("All required CSV files found in the processed directory")
    
    return True

if __name__ == "__main__":
    logger.info("Setting up standalone environment for NBA Analytics Dashboard")
    if setup_standalone_environment():
        logger.info("✅ Setup completed successfully")
        
        # Provide instructions for running the app
        logger.info("\nTo run the Streamlit app in standalone mode, use:")
        logger.info("    streamlit run streamlit_app/app.py")
        
        # Check if streamlit is installed
        try:
            import streamlit
            logger.info("✅ Streamlit is installed")
        except ImportError:
            logger.warning("⚠️ Streamlit is not installed. Install it with:")
            logger.warning("    pip install -r streamlit_app/requirements.txt")
    else:
        logger.error("❌ Setup failed")
        sys.exit(1) 