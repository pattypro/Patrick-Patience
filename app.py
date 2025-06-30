
import streamlit as st
import pandas as pd
from datetime import datetime

# --- AUTH ---
USERS = {"patrick@example.com": "yourpassword", "patience@example.com": "herpassword"}

def login():
    with st.sidebar:
        st.title("Login")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if USERS.get(email) == password:
                st.session_state["user"] = email
            else:
                st.error("Invalid credentials")

if "user" not in st.session_state:
    login()
    st.stop()

# --- TITLE ---
st.title("💖 Patrick & Patience Journal")
st.markdown("Welcome, **Patrick & Patience**! This is your private space to share memories, goals, and thoughts.")

# --- MENU ---
menu = st.sidebar.radio("Menu", ["📸 Memories", "🎯 Weekly Goals", "💭 Freewriting"])

# --- Helper functions ---
def load_data(file):
    try:
        return pd.read_csv(file)
    except:
        return pd.DataFrame()

def save_data(file, df):
    df.to_csv(file, index=False)

# --- Memories ---
if menu == "📸 Memories":
    st.header("📸 Share a Memory")
    memory = st.text_area("What do you want to remember today?")
    if st.button("Save Memory"):
        df = load_data("memories.csv")
        new_entry = {"Date": datetime.now().strftime("%Y-%m-%d %H:%M"), "Memory": memory}
        df = df.append(new_entry, ignore_index=True)
        save_data("memories.csv", df)
        st.success("Memory saved!")

    st.subheader("🗂 All Memories")
    df = load_data("memories.csv")
    if not df.empty:
        st.dataframe(df[::-1])

# --- Goals ---
elif menu == "🎯 Weekly Goals":
    st.header("🎯 Add a Weekly Goal")
    goal = st.text_input("Your goal this week?")
    if st.button("Add Goal"):
        df = load_data("goals.csv")
        new_entry = {"Date": datetime.now().strftime("%Y-%m-%d"), "Goal": goal, "Done": False}
        df = df.append(new_entry, ignore_index=True)
        save_data("goals.csv", df)
        st.success("Goal added!")

    st.subheader("📅 This Week's Goals")
    df = load_data("goals.csv")
    if not df.empty:
        for i in df.index:
            checked = st.checkbox(df["Goal"][i], value=df["Done"][i])
            df.at[i, "Done"] = checked
        save_data("goals.csv", df)

# --- Freewriting ---
elif menu == "💭 Freewriting":
    st.header("💭 Write Your Thoughts")
    thoughts = st.text_area("Write anything you feel...")
    if st.button("Save Thought"):
        df = load_data("thoughts.csv")
        new_entry = {"Date": datetime.now().strftime("%Y-%m-%d %H:%M"), "Thought": thoughts}
        df = df.append(new_entry, ignore_index=True)
        save_data("thoughts.csv", df)
        st.success("Thought saved!")

    st.subheader("📓 Thought Journal")
    df = load_data("thoughts.csv")
    if not df.empty:
        st.dataframe(df[::-1])
