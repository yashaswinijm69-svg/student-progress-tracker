import streamlit as st
from db import init_db

def main():
    st.set_page_config(page_title="Student Progress Tracker", page_icon="🎓")
    
    st.title("🎓 Student Progress Tracker")
    
    # Initialize the database
    try:
        init_db()
        st.success("Database initialized successfully! ✅")
        st.info("Phase 1: Project scaffold and database foundation is complete.")
        
        st.markdown("""
        ### Next Steps:
        - Add Category Management (Phase 2)
        - Implement Task & Habit tracking (Phase 2)
        - Build Analytics Dashboard (Phase 3)
        """)
        
    except Exception as e:
        st.error(f"Error initializing database: {e}")

if __name__ == "__main__":
    main()
