import subprocess
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nba_analytics_project.settings')
django.setup()

# Run the Streamlit app
if __name__ == "__main__":
    subprocess.run(["streamlit", "run", "streamlit_app/app.py"]) 