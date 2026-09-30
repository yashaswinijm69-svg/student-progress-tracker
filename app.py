import streamlit as st
from db import init_db, add_category, get_all_categories, update_category, delete_category

def category_management():
    st.header("📂 Category Management")
    
    # Form to add a new category
    with st.expander("➕ Add New Category"):
        with st.form("add_category_form", clear_on_submit=True):
            name = st.text_input("Category Name")
            target = st.number_input("Weekly Target (hours)", min_value=0.0, step=0.5, format="%.1f")
            submit_button = st.form_submit_button("Add Category")
            
            if submit_button:
                if not name.strip():
                    st.error("Category name cannot be empty.")
                elif target <= 0:
                    st.error("Weekly target hours must be greater than 0.")
                else:
                    success, message = add_category(name.strip(), target)
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(f"Error: {message}")

    # Display existing categories
    st.subheader("Existing Categories")
    categories = get_all_categories()
    
    if not categories:
        st.info("No categories created yet. Add one above!")
    else:
        for cat in categories:
            with st.container(border=True):
                col1, col2, col3, col4 = st.columns([3, 2, 1, 1])
                col1.write(f"**{cat.name}**")
                col2.write(f"{cat.weekly_target_hours} hrs/week")
                
                if col3.button("Edit", key=f"edit_{cat.id}"):
                    st.session_state[f"editing_{cat.id}"] = True
                
                if col4.button("Delete", key=f"delete_{cat.id}"):
                    st.session_state[f"deleting_{cat.id}"] = True

                # Edit Mode
                if st.session_state.get(f"editing_{cat.id}", False):
                    with st.form(f"edit_form_{cat.id}"):
                        new_name = st.text_input("New Name", value=cat.name)
                        new_target = st.number_input("New Weekly Target", value=cat.weekly_target_hours, min_value=0.1, step=0.5)
                        col_e1, col_e2 = st.columns(2)
                        if col_e1.form_submit_button("Save"):
                            if not new_name.strip():
                                st.error("Name cannot be empty.")
                            else:
                                success, message = update_category(cat.id, new_name.strip(), new_target)
                                if success:
                                    st.session_state[f"editing_{cat.id}"] = False
                                    st.success(message)
                                    st.rerun()
                                else:
                                    st.error(message)
                        if col_e2.form_submit_button("Cancel"):
                            st.session_state[f"editing_{cat.id}"] = False
                            st.rerun()

                # Delete Confirmation
                if st.session_state.get(f"deleting_{cat.id}", False):
                    st.warning(f"Are you sure you want to delete '{cat.name}'?")
                    col_d1, col_d2 = st.columns(2)
                    if col_d1.button("Confirm Delete", key=f"conf_del_{cat.id}"):
                        success, message = delete_category(cat.id)
                        if success:
                            st.session_state[f"deleting_{cat.id}"] = False
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)
                    if col_d2.button("Cancel", key=f"canc_del_{cat.id}"):
                        st.session_state[f"deleting_{cat.id}"] = False
                        st.rerun()

def main():
    st.set_page_config(page_title="Student Progress Tracker", page_icon="🎓")
    
    # Initialize the database
    init_db()
    
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Dashboard", "Category Management"])
    
    if page == "Dashboard":
        st.title("🎓 Student Progress Tracker")
        st.info("Welcome to your dashboard! Use the sidebar to manage categories.")
        
        # Summary of categories
        categories = get_all_categories()
        if categories:
            st.subheader("Your Categories")
            for cat in categories:
                st.write(f"- **{cat.name}**: {cat.weekly_target_hours} hrs/week")
        else:
            st.info("No categories found. Please go to Category Management to add some.")

    elif page == "Category Management":
        category_management()

if __name__ == "__main__":
    main()
