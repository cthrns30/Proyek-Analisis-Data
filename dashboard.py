import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

# Mengatur tampilan halaman utama Streamlit
st.title('Dashboard Analisis Penyewaan Sepeda')
st.subheader('Visualisasi Data Penyewaan Berdasarkan Variabel Cuaca dan Hari Kerja')

# Memuat dataset 'main_data.csv' yang terletak di folder yang sama
df = pd.read_csv("main_data.csv")

# Mengubah kolom 'dteday' menjadi format datetime (sesuaikan dengan kolom tanggal di CSV Anda)
df['dteday'] = pd.to_datetime(df['dteday'])

# Menentukan rentang tanggal untuk memfilter data
min_date = df['dteday'].min()
max_date = df['dteday'].max()

# Sidebar untuk filter berdasarkan rentang tanggal
with st.sidebar:
    st.image("https://raw.githubusercontent.com/cthrns30/assets/main/dataset-card.jpeg")  # Placeholder untuk logo
    st.write('## Filter Data Berdasarkan Tanggal:')
    
    # Menambahkan filter tanggal
    start_date, end_date = st.date_input(
        label='Pilih rentang tanggal', 
        min_value=min_date, 
        max_value=max_date, 
        value=[min_date, max_date]
    )

# Filter data berdasarkan rentang tanggal
filtered_df = df[(df['dteday'] >= pd.to_datetime(start_date)) & (df['dteday'] <= pd.to_datetime(end_date))]

# Menampilkan informasi dasar tentang data terfilter
st.write(f"Data yang ditampilkan berdasarkan rentang waktu dari **{start_date}** hingga **{end_date}**:")
st.dataframe(filtered_df.head())

# Menampilkan statistik deskriptif untuk variabel cuaca dan penyewaan
st.write('Statistik Deskriptif untuk Variabel Cuaca dan Total Penyewaan:')
weather_related_columns = ['temp', 'atemp', 'hum', 'windspeed', 'cnt']
st.write(filtered_df[weather_related_columns].describe())

# Visualisasi Scatter Plot antara variabel cuaca dan total penyewaan
st.subheader('Visualisasi Korelasi antara Variabel Cuaca dan Total Penyewaan')

fig, axes = plt.subplots(2, 2, figsize=(12, 10))

sns.scatterplot(x='temp', y='cnt', data=filtered_df, ax=axes[0, 0], color='blue')
axes[0, 0].set_title('Suhu vs Total Penyewaan')

sns.scatterplot(x='hum', y='cnt', data=filtered_df, ax=axes[0, 1], color='green')
axes[0, 1].set_title('Kelembapan vs Total Penyewaan')

sns.scatterplot(x='windspeed', y='cnt', data=filtered_df, ax=axes[1, 0], color='red')
axes[1, 0].set_title('Kecepatan Angin vs Total Penyewaan')

correlation_matrix = filtered_df[['temp', 'hum', 'windspeed', 'cnt']].corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', ax=axes[1, 1])
axes[1, 1].set_title('Korelasi Heatmap Variabel Cuaca')

st.pyplot(fig)

# Visualisasi Boxplot untuk distribusi penyewaan sepeda pada hari kerja dan hari libur
st.subheader('Distribusi Penyewaan Sepeda pada Hari Kerja dan Hari Libur')

filtered_df['workingday'] = filtered_df['workingday'].replace({0: 'Hari Libur', 1: 'Hari Kerja'})
plt.figure(figsize=(8, 6))
sns.boxplot(x='workingday', y='cnt', hue='workingday', data=filtered_df, palette=['red', 'blue'], dodge=False)
plt.title('Distribusi Penyewaan pada Hari Kerja dan Hari Libur')
plt.xlabel('Tipe Hari')
plt.ylabel('Total Penyewaan')
plt.legend([],[], frameon=False)
st.pyplot(plt)

# Menampilkan informasi tambahan
st.write('Dashboard ini menampilkan analisis data penyewaan sepeda berdasarkan variabel cuaca, serta perbandingan penyewaan pada hari kerja dan hari libur.')

# Footer
st.caption('Copyright © Bike Sharing Dashboard 2024')