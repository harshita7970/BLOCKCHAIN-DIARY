import streamlit as st
from blockchain_diary import Blockchain, Block
from time import time
import uuid
from datetime import datetime

# Initialize blockchain
if "diary_chain" not in st.session_state:
    st.session_state.diary_chain = Blockchain()

if "users" not in st.session_state:
    st.session_state.users = {}

st.title("📝 Blockchain Digital Diary - Expandable Block View")

# 1️⃣ User registration
st.subheader("👤 Register / Select User")
user_name = st.text_input("Enter your name:")

if user_name:
    if user_name not in st.session_state.users:
        diary_id = str(uuid.uuid4())[:8]  # generate short unique diary ID
        st.session_state.users[user_name] = diary_id
        st.success(f"Welcome, {user_name}! Your diary ID: {diary_id}")
    else:
        diary_id = st.session_state.users[user_name]
        st.info(f"Welcome back, {user_name}! Your diary ID: {diary_id}")
else:
    st.warning("Please enter your name to continue.")

# 2️⃣ Add diary entry
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
            mining_info = st.session_state.diary_chain.add_block(new_block)
            st.success("Entry added successfully! ✅")
            st.info(f"Mined Hash: {mining_info['hash']} 🔒")

# 3️⃣ Display blockchain calculations (start from Block 1)
st.header("🔗 Blockchain Calculation (Click to Expand)")
for block in st.session_state.diary_chain.chain[1:]:  # skip Genesis block
    ts = datetime.fromtimestamp(block.timestamp)
    date_str = ts.strftime("%d-%m-%Y (%A)")

    user = block.data.get("user_name")
    diary_id = block.data.get("diary_id")
    entry_text = block.data.get("entry")

    with st.expander(f"Block {block.index}"):
        st.write(f"**Previous Hash:** {block.previous_hash}")
        st.write(f"**Hash:** {block.hash}")
        st.write(f"**User:** {user}")
        st.write(f"**Diary ID:** {diary_id}")
        st.write(f"**Date:** {date_str}")
        st.write(f"**Entry:** {entry_text}")

# 4️⃣ Blockchain integrity check
if st.button("Check Blockchain Integrity"):
    if st.session_state.diary_chain.is_chain_valid():
        st.success("Blockchain is valid! 🔒 No tampering detected.")
    else:
        st.error("Warning! Blockchain has been tampered with!")

