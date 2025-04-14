# Step 1: Clone the repository
git clone https://github.com/V1k1ng04/cashtrack.git
cd cashtrack

# Step 2: Create and activate a virtual environment

# For Windows:
python -m venv venv
venv\Scripts\activate

# For Mac/Linux:
python3 -m venv venv
source venv/bin/activate

# Step 3: Install the required dependencies
pip install -r requirements.txt

# Step 4: Set up the database
python init_db.py

# Step 5: Run the application
python app.py

# The app will be available at http://127.0.0.1:5000/
# Open this URL in your web browser to access the application
