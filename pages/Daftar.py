import streamlit as st

if 'nama' not in st.session_state:
    nama = st.text_input("Masukkan Nama: ")
    email = st.text_input("Masukkan Email: ")

    if st.button("Daftar"):
        st.session_state.nama = nama
        st.rerun()
else:
    st.write("KAMU SUDAH TERDAFTAR!")