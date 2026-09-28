# High-Frequency Reconstruction Project

## Setup Instructions
1. **Clone the repository:**
   `git clone <your-repo-link>`
2. **Create a virtual environment:**
   `python3 -m venv venv`
3. **Activate the environment:**
   - Windows: `venv\Scripts\activate`
   - Linux/macOS: `source venv/bin/activate`
4. **Install dependencies:**
   `pip install -r requirements.txt`

## How to Run
Execute the main pipeline using:
`python src/main.py --input data/raw/sample.wav`
To run the Live Demo System:
`streamlit run ui/app.py`