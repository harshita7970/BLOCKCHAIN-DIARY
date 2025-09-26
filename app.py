import streamlit as st
from blockchain_diary import Blockchain, Block
from time import time

# Initialize blockchain
if "diary_chain" not in st.session_state:
    st.session_state.diary_chain = Blockchain()

st.title("📝 Blockchain-Based Digital Diary")
st.write("Add your daily note. Once saved, it cannot be changed!")

# User input
entry = st.text_area("Write your diary entry here:")

if st.button("Add Entry"):
    if entry.strip() == "":
        st.warning("Diary entry cannot be empty!")
    else:
        new_block = Block(
            index=len(st.session_state.diary_chain.chain),
            timestamp=time(),
            data=entry,
            previous_hash=""
        )
        st.session_state.diary_chain.add_block(new_block)
        st.success("Entry added successfully! ✅")

# Display diary entries
st.header("📜 Diary Timeline")
for block in reversed(st.session_state.diary_chain.chain[1:]):  # skip genesis
    st.subheader(f"Day {block.index}")
    st.write(f"Timestamp: {block.timestamp}")
    st.write(f"Entry: {block.data}")
    st.write(f"Block Hash: {block.hash}")
    st.markdown("---")

# Blockchain validity
if st.button("Check Integrity"):
    if st.session_state.diary_chain.is_chain_valid():
        st.success("Blockchain is valid! 🔒 No tampering detected.")
    else:
        st.error("Warning! Blockchain has been tampered with!")
