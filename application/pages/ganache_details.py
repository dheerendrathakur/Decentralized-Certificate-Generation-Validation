import streamlit as st
from web3 import Web3
from connection import w3
import datetime

def ganache_details():
    st.title('Ganache Account Details')
    current_account = w3.eth.accounts[0]  # 
    st.subheader('Current Account')
    st.write(current_account)

    # Fetch balance for the current account
    st.subheader('Balance')
    balance = w3.eth.get_balance(current_account)
    st.write(f'{current_account}: {w3.fromWei(balance, "ether")} Ether')

    # Fetch transactions in the latest block
    st.subheader('Transactions')
    block = w3.eth.get_block('latest', full_transactions=True)
    for transaction in block.transactions:
        if transaction["from"] == current_account or transaction["to"] == current_account:
            timestamp = datetime.datetime.fromtimestamp(block["timestamp"])
            st.write(f'Timestamp: {timestamp}')
            st.write(f'From: {transaction["from"]}')
            st.write(f'To: {transaction["to"]}')
            st.write(f'Value: {w3.fromWei(transaction["value"], "ether")} Ether')

    # If the "Show More" button is clicked, fetch transactions in all blocks
    if st.button('Show More'):
        if 'show_more' not in st.session_state or not st.session_state.show_more:
            st.session_state.show_more = True
            for i in range(w3.eth.block_number, 0, -1):
                block = w3.eth.get_block(i, full_transactions=True)
                for transaction in block.transactions:
                    if transaction["from"] == current_account or transaction["to"] == current_account:
                        timestamp = datetime.datetime.fromtimestamp(block["timestamp"])
                        st.write(f'Timestamp: {timestamp}')
                        st.write(f'From: {transaction["from"]}')
                        st.write(f'To: {transaction["to"]}')
                        st.write(f'Value: {w3.fromWei(transaction["value"], "ether")} Ether')
        else:
            st.session_state.show_more = False
            st.experimental_rerun()