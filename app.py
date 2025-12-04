# app.py
import streamlit as st
import pandas as pd
import os
from datetime import datetime

# -------------------------------
# Page Config & Styling
# -------------------------------
st.set_page_config(
    page_title="Health Record Management System",
    page_icon="hospital",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main {background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);}
    .css-1d391kg {background: #007bff;}
    h1 {color: #007bff; font-weight: 700; text-align: center; padding: 1rem 0;}
    .stButton>button {
        background-color: #00bcd4; color: white; border-radius: 8px; border: none; padding: 0.5rem 1rem;
    }
    .stButton>button:hover {background-color: #0097a7;}
    .metric-card {
        background: white; padding: 1.5rem; border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1); text-align: center;
    }
    .metric-value {font-size: 2.2rem; font-weight: bold; color: #007bff;}
    .metric-label {color: #6c757d; font-size: 1rem;}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# Data Functions
# -------------------------------
DATA_FILE = "health_records.csv"

def load_data() -> pd.DataFrame:
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=[
            "ID", "Name", "Age", "Gender", "Blood Type",
            "Phone", "Address", "Medical History", "Date Added"
        ])

def save_data(df: pd.DataFrame):
    df.to_csv(DATA_FILE, index=False)

# -------------------------------
# Initialize Session State (replaces global variables)
# -------------------------------
if "df" not in st.session_state:
    st.session_state.df = load_data()

if "next_id" not in st.session_state:
    if st.session_state.df.empty:
        st.session_state.next_id = 1
    else:
        st.session_state.next_id = int(st.session_state.df["ID"].max()) + 1

df = st.session_state.df          # shortcut for readability
next_id = st.session_state.next_id

# -------------------------------
# Sidebar Navigation
# -------------------------------
st.sidebar.image("https://img.icons8.com/fluency/100/000000/hospital.png", use_column_width=True)
st.sidebar.title("Health RMS")
page = st.sidebar.radio("Navigation", [
    "Dashboard",
    "View & Search",
    "Add Patient",
    "Edit Records (Full CRUD)",
    "Delete Record"
])

# -------------------------------
# Dashboard
# -------------------------------
if page == "Dashboard":
    st.title("Health Record Management System")
    st.markdown("### Dashboard Overview")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{len(df)}</div><div class="metric-label">Total Patients</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{df["Gender"].value_counts().get("Male",0)}</div><div class="metric-label">Male</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{df["Gender"].value_counts().get("Female",0)}</div><div class="metric-label">Female</div></div>', unsafe_allow_html=True)
    with c4:
        avg = round(df["Age"].mean(), 1) if not df.empty else 0
        st.markdown(f'<div class="metric-card"><div class="metric-value">{avg}</div><div class="metric-label">Avg Age</div></div>', unsafe_allow_html=True)

# -------------------------------
# View & Search
# -------------------------------
elif page == "View & Search":
    st.title("View Patient Records")
    if df.empty:
        st.info("No records yet.")
    else:
        search = st.text_input("Search by Name / ID / Phone")
        disp = df
        if search:
            disp = df[
                df["Name"].str.contains(search, case=False, na=False) |
                df["Phone"].str.contains(search, na=False) |
                df["ID"].astype(str).str.contains(search)
            ]
        st.dataframe(disp, use_container_width=True)
        st.caption(f"Showing {len(disp)} of {len(df)} records")

# -------------------------------
# Add Patient
# -------------------------------
elif page == "Add Patient":
    st.title("Add New Patient")
    with st.form("add_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name *")
            age = st.number_input("Age *", min_value=0, max_value=120)
            gender = st.selectbox("Gender *", ["", "Male", "Female", "Other"])
        with col2:
            blood = st.selectbox("Blood Type", ["", "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
            phone = st.text_input("Phone")
            address = st.text_area("Address")

        history = st.text_area("Medical History")

        if st.form_submit_button("Add Patient"):
            if not name or not age or gender == "":
                st.error("Name, Age and Gender are required!")
            else:
                new_row = pd.DataFrame([{
                    "ID": st.session_state.next_id,
                    "Name": name.strip(),
                    "Age": int(age),
                    "Gender": gender,
                    "Blood Type": blood or "Not specified",
                    "Phone": phone or "N/A",
                    "Address": address or "N/A",
                    "Medical History": history or "None",
                    "Date Added": datetime.now().strftime("%Y-%m-%d %H:%M")
                }])

                st.session_state.df = pd.concat([st.session_state.df, new_row], ignore_index=True)
                st.session_state.next_id += 1
                save_data(st.session_state.df)

                st.success(f"Patient {name} added! ID: {st.session_state.next_id-1}")
                st.balloons()

# -------------------------------
# Full CRUD Editor (Best Experience)
# -------------------------------
elif page == "Edit Records (Full CRUD)":
    st.title("Edit Records – Full CRUD")
    st.markdown("Edit inline • Add rows • Delete rows → Click **Save** when done")

    if df.empty:
        st.info("No data yet.")
    else:
        edited = st.data_editor(
            df,
            num_rows="dynamic",
            use_container_width=True,
            column_config={
                "ID": st.column_config.NumberColumn("ID", disabled=True),
                "Name": st.column_config.TextColumn("Name", required=True),
                "Age": st.column_config.NumberColumn("Age", min_value=0, max_value=120),
                "Gender": st.column_config.SelectboxColumn("Gender", options=["Male", "Female", "Other"]),
                "Blood Type": st.column_config.SelectboxColumn("Blood Type", options=["A+","A-","B+","B-","AB+","AB-","O+","O-"]),
            }
        )

        if st.button("Save All Changes", type="primary"):
            # Auto-fill ID for newly added rows
            if edited["ID"].isna().any():
                max_id = df["ID"].max() if not df["ID"].isna().all() else 0
                edited.loc[edited["ID"].isna(), "ID"] = range(max_id + 1, max_id + 1 + edited["ID"].isna().sum())

            st.session_state.df = edited.copy()
            save_data(st.session_state.df)
            st.success("All changes saved successfully!")
            st.rerun()

# -------------------------------
# Delete Record
# -------------------------------
elif page == "Delete Record":
    st.title("Delete Patient")
    st.warning("This action is permanent!")

    if df.empty:
        st.info("No records to delete.")
    else:
        pid = st.number_input("Patient ID", min_value=1, step=1)
        if st.button("Delete Patient", type="secondary"):
            if pid in df["ID"].values:
                name = df[df["ID"] == pid]["Name"].iloc[0]
                st.session_state.df = df[df["ID"] != pid]
                save_data(st.session_state.df)
                st.error(f"Deleted: {name} (ID {pid})")
            else:
                st.error("ID not found!")

# -------------------------------
# Footer
# -------------------------------
st.sidebar.markdown("---")
st.sidebar.caption("© 2025 Health Record Management System | Built with Streamlit")