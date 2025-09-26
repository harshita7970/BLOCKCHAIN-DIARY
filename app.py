import streamlit as st
from blockchain_diary import Blockchain, Block
from time import time
import pandas as pd
import uuid
from datetime import datetime

# Initialize blockchain
if "diary_chain" not in st.session_state:
    st.session_state.diary_chain = Blockchain()

if "users" not in st.session_state:
    st.session_state.users = {}  # Stores username -> diary_id

st.title("📝 Blockchain Digital Diary with Mining")
st.write("Each diary entry is mined into the blockchain. Tamper-proof!")

# User registration
st.subheader("👤 Register / Select User")
user_name = st.text_input("Enter your name:")

if user_name:
    if user_name not in st.session_state.users:
        diary_id = str(uuid.uuid4())[:8]  # short unique ID
        st.session_state.users[user_name] = diary_id
        st.success(f"Welcome, {user_name}! Your diary ID: {diary_id}")
    else:
        diary_id = st.session_state.users[user_name]
        st.info(f"Welcome back, {user_name}! Your diary ID: {diary_id}")
else:
    st.warning("Please enter your name to continue.")

# Add diary entry
if user_name:
    entry = st.text_area("Write your diary entry here:")
    if st.button("Add Entry"):
        if entry.strip() == "":
            st.warning("Diary entry cannot be empty!")
        else:
            timestamp = time()
            new_block = Block(
                index=len(st.session_state.diary_chain.chain),
                timestamp=timestamp,
                data={
                    "user_name": user_name,
                    "diary_id": diary_id,
                    "entry": entry
                },
                previous_hash=""
            )
            mined_hash = st.session_state.diary_chain.add_block(new_block)
            st.success("Entry added successfully! ✅")
            st.info(f"Block mined with hash: {mined_hash} 🔒")

# Display diary table
st.header("📊 Diary Details")
diary_data = []

for block in st.session_state.diary_chain.chain[1:]:  # skip genesis
    block_data = block.data
    if isinstance(block_data, dict):
        ts = datetime.fromtimestamp(block.timestamp)
        date_str = ts.strftime("%d-%m-%Y (%A)")
        diary_data.append({
            "User Name": block_data["user_name"],
            "Diary ID": block_data["diary_id"],
            "Date": date_str,
            "Entry": block_data["entry"],
            "Block Hash": block.hash
        })

if diary_data:
    df = pd.DataFrame(diary_data)
    st.table(df)
else:
    st.info("No diary entries yet.")

# Check blockchain integrity
if st.button("Check Blockchain Integrity"):
    if st.session_state.diary_chain.is_chain_valid():
        st.success("Blockchain is valid! 🔒 No tampering detected.")
    else:
        st.error("Warning! Blockchain has been tampered with!")

