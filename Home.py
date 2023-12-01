import streamlit as st
import pandas as pd
from datetime import timedelta
import plotly.express as px
from PIL import Image


if 'nama' in st.session_state:
    st.title(f'Hai, {st.session_state.nama}, Selamat Datang.')
    st.markdown('#') 

    
    if 'data' not in st.session_state:
        st.session_state.data = pd.DataFrame(columns=['Date', 'Category', 'Amount', 'Type'])

    
    image = Image.open('logocakep.jpg')
    st.image(image, width=140)
    st.title('C a k e p .')
    st.write('Selamat datang di Cakep, Kendalikan pengeluaran dengan mencatat keuangan hanya dengan Cakep')

    
    date = st.date_input('Date')
    type = st.radio('Type', ['Revenue', 'Expense'])

    if type == 'Revenue':
        category_options = ['Produk dan Jasa', 'Investasi', 'Iklan dan Langganan', 'Pelayanan dan Pengelolaan']
    elif type == 'Expense':
        category_options = ['Operasional', 'Pajak', 'Hutang', 'Darurat']

    category = st.selectbox('Category', category_options)
    amount = st.number_input('Amount')

    
    if st.button('Tambahkan Data'):
        new_data = pd.DataFrame({'Date': [date], 'Category': [category], 'Amount': [amount], 'Type': [type]})
        st.session_state.data = pd.concat([st.session_state.data, new_data], ignore_index=True)
        st.write('Data berhasil ditambahkan!')

    
    st.write('Data Revenue dan Expense:')
    delete_rows = st.dataframe(st.session_state.data, height=200)
    rows_to_delete = st.multiselect('Pilih Baris untuk Dihapus', st.session_state.data.index)
    if st.button('Hapus Baris yang Dipilih'):
        st.session_state.data = st.session_state.data.drop(index=rows_to_delete)
        st.write('Data Berhasil Dihapus!')

    
    total_expense = st.session_state.data[st.session_state.data['Type'] == 'Expense']['Amount'].sum()
    total_revenue = st.session_state.data[st.session_state.data['Type'] == 'Revenue']['Amount'].sum()

    
    st.write(f'Total Expense: {total_expense}')
    st.write(f'Total Revenue: {total_revenue}')

    
    current_balance = total_revenue - total_expense
    st.write(f'Saldo Saat Ini: {current_balance}')

    
    st.subheader('Period Tracking')
    period = st.selectbox('Select Period', ['Daily', 'Weekly', 'Monthly'])
    if period == 'Daily':
        start_date = date
        end_date = date
    elif period == 'Weekly':
        start_date = date - timedelta(days=date.weekday())
        end_date = start_date + timedelta(days=6)
    elif period == 'Monthly':
        start_date = date.replace(day=1)
        end_date = start_date.replace(day=pd.Period(start_date, 'M').days_in_month)

    filtered_data = st.session_state.data[(st.session_state.data['Date'] >= start_date) & (st.session_state.data['Date'] <= end_date)]
    period_total_spending = filtered_data[filtered_data['Type'] == 'Expense']['Amount'].sum()
    period_total_income = filtered_data[filtered_data['Type'] == 'Revenue']['Amount'].sum()

    st.write(f'Total Expense ({period}): {period_total_spending}')
    st.write(f'Total Revenue ({period}): {period_total_income}')

    
    def calculate_financial_metrics(revenue, Operasional, Pajak, Hutang, Darurat):
        laba_kotor = revenue
        laba_bersih = revenue - (Operasional + Pajak + Hutang + Darurat)
        corporate_income_tax = 0.17
        if laba_kotor > 50000000000:  # Rp50 Miliar
            corporate_income_tax *= 0.5
        pph = laba_kotor * corporate_income_tax
        return laba_kotor, laba_bersih, pph

    
    revenue = total_revenue
    Operasional = total_expense
    Pajak = 0
    Hutang = 0
    Darurat = 0
    laba_kotor, laba_bersih, pph = calculate_financial_metrics(revenue, Operasional, Pajak, Hutang, Darurat)

    
    st.write(f'Laba Kotor: {laba_kotor}')
    st.write(f'Laba Bersih: {laba_bersih}')
    st.write(f'Income Tax: {pph}')

    if st.button('Simpan ke Excel'):
        st.session_state.data.to_excel("datacakep.xlsx", index=False)
        st.write('Data Berhasil Disimpan ke Excel!')

    st.subheader('Visualisasi Data')
    fig = px.line(filtered_data, x='Date', y=['Amount'], color='Type', labels={'Amount': 'Jumlah (Rupiah)'}, title='Line Chart: Revenue, Expense, Laba Bersih, dan Laba Kotor')
    st.plotly_chart(fig)
else:
    st.write('ANDA BELUM TERDAFTAR DI SISTEM KAMI, SILAHKAN DAFTAR')
