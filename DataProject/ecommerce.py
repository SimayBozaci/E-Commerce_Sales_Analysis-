import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

file_path = "/Users/simaybozaci/Downloads/OnlineRetail.csv"

try:
    df = pd.read_csv(file_path, encoding='ISO-8859-1')

    print("Veri Önizleme:\n", df.head())
    print("\nEksik Değer Sayısı:\n", df.isnull().sum())

    df.dropna(inplace=True)
    df.drop(['InvoiceNo', 'CustomerID', 'Country'], axis=1, inplace=True)

    print("\nGüncellenmiş Veri Bilgisi:\n", df.info())

    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'], errors='coerce')
    df['TotalPrice'] = df['Quantity'] * df['UnitPrice']

    print("\nSayısal Veriler için Temel İstatistikler:\n", df.describe())

    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)
    sns.histplot(df['Quantity'], bins=30, kde=True, color='blue')
    plt.title("Ürün Miktarı Dağılımı")

    plt.subplot(1, 2, 2)
    sns.histplot(df['TotalPrice'], bins=30, kde=True, color='green')
    plt.title("Toplam Satış Fiyatı Dağılımı")

    plt.show()

    top_products = df.groupby('Description')['Quantity'].sum().sort_values(ascending=False).head(10)
    print("\nEn Çok Satın Alınan İlk 10 Ürün:\n", top_products)

    plt.figure(figsize=(10, 6))
    top_products.plot(kind='bar', color='red')
    plt.title("En Çok Satın Alınan Ürünler")
    plt.xlabel("Ürün")
    plt.ylabel("Satış Miktarı")
    plt.xticks(rotation=45)
    plt.show()

    df['Month'] = df['InvoiceDate'].dt.to_period('M')
    monthly_sales = df.groupby('Month')['TotalPrice'].sum()

    plt.figure(figsize=(14, 6))
    monthly_sales.plot(kind='line', marker='o', color='orange', label='Aylık Satış')
    plt.title("Aylık Toplam Satış")
    plt.xlabel("Ay")
    plt.ylabel("Satış Tutarı")
    plt.legend()
    plt.show()



    popular_items = top_products.index[:3]
    plt.figure(figsize=(10, 6))
    for item in popular_items:
        item_sales = df[df['Description'] == item].groupby('Month')['Quantity'].sum()
        item_sales.index = item_sales.index.to_timestamp()
        plt.plot(item_sales, marker='o', label=item)

    plt.title("Popüler Ürünlerin Aylık Satış Miktarı")
    plt.xlabel("Ay")
    plt.ylabel("Satış Miktarı")
    plt.legend()
    plt.xticks(rotation=45)
    plt.show()

    plt.figure(figsize=(10, 6))
    sns.boxplot(data=df, x='Quantity')
    plt.title("Ürün Miktarının Aşırı Değer Analizi")
    plt.show()

    plt.figure(figsize=(10, 6))
    sns.boxplot(data=df, x='TotalPrice')
    plt.title("Toplam Satış Fiyatının Aşırı Değer Analizi")

    plt.show()

except FileNotFoundError:
    print(f"Dosya '{file_path}' bulunamadı. Lütfen dosya yolunu kontrol edin.")

