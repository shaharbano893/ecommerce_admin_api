import os
import sys

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.insert_sample_data import insert_sample_data

if __name__ == "__main__":
    print("📦 Inserting sample data...")
    insert_sample_data()
    print("🚀 Done! You can now run the app using:")
    print("👉 fastapi dev")
