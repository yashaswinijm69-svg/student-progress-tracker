# Student Progress Tracker

A personal tool to track academic progress, habits, and goals.

## Phase 1: Project Scaffold & Database Foundation
- Project structure set up.
- SQLAlchemy models for Categories, Tasks, Completions, and Settings.
- SQLite database initialization.
- Basic Streamlit landing page.

## Tech Stack
- **Language:** Python
- **Framework:** Streamlit
- **Database:** SQLite
- **ORM:** SQLAlchemy

## Project Structure
- `app.py`: Main Streamlit application entry point.
- `db.py`: Database models and initialization logic.
- `requirements.txt`: Project dependencies.
- `tracker.db`: SQLite database file (generated after first run).

## Installation

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   streamlit run app.py
   ```
