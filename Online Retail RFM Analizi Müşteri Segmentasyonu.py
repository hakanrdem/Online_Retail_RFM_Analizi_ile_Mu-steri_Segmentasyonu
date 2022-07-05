###############################################################
# RFM ile Müşteri Segmentasyonu (Customer Segmentation with RFM)
###############################################################

# 1. İş Problemi (Business Problem)
# 2. Veriyi Anlama (Data Understanding)
# 3. Veri Hazırlama (Data Preparation)
# 4. RFM Metriklerinin Hesaplanması (Calculating RFM Metrics)
# 5. RFM Skorlarının Hesaplanması (Calculating RFM Scores)
# 6. RFM Segmentlerinin Oluşturulması ve Analiz Edilmesi (Creating & Analysing RFM Segments)
# 7. Tüm Sürecin Fonksiyonlaştırılması

###############################################################
# 1. İş Problemi (Business Problem)
###############################################################

# İngiltere merkezli perakende şirketi e-ticaret şirketi müşterilerini segmentlere ayırıp bu segmentlere göre
# pazarlama stratejileri belirlemek istiyor.

# Ortak davranışlar sergileyen müşteri segmentleri özelinde pazarlama çalışmaları yapmanın gelir artışı sağlayacağını düşünmektedir.
# Segmentlere ayırmak için RFM analizi kullanılacaktır.

# Veri Seti Hikayesi
# https://archive.ics.uci.edu/ml/datasets/Online+Retail+II

# Online Retail II isimli veri seti İngiltere merkezli online bir satış mağazasının
# 01/12/2009 - 09/12/2011 tarihleri arasındaki satışlarını içeriyor.

# Değişkenler
#
# InvoiceNo: Fatura numarası. Her işleme yani faturaya ait eşsiz numara. C ile başlıyorsa iptal edilen işlem.
# StockCode: Ürün kodu. Her bir ürün için eşsiz numara.
# Description: Ürün ismi
# Quantity: Ürün adedi. Faturalardaki ürünlerden kaçar tane satıldığını ifade etmektedir.
# InvoiceDate: Fatura tarihi ve zamanı.
# UnitPrice: Ürün fiyatı (Sterlin cinsinden)
# CustomerID: Eşsiz müşteri numarası
# Country: Ülke ismi. Müşterinin yaşadığı ülke.

# Görev 1
# Veriyi Anlama ve Hazırlama

# Adım 1
# Online Retail II excelindeki 2010-2011 verisini okuyunuz. Oluşturduğunuz dataframe’in kopyasını oluşturunuz.

import datetime as dt
import pandas as pd
pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)
pd.set_option('display.width', 500)
pd.set_option('display.float_format', lambda x: '%.3f' % x)

df_ = pd.read_excel("/Users/hakanerdem/PycharmProjects/pythonProject/dsmlbc_9_abdulkadir/Homeworks/hakan_erdem/2_CRM_Analitigi/online_retail_II.xlsx", sheet_name="Year 2010-2011")
df = df_.copy()
df.head()

# Adım 2:
# Veri setinin betimsel istatistiklerini inceleyiniz.

def check_df(dataframe, head=10):
    print("##################### Shape #####################")
    print(dataframe.shape)
    print("##################### Types #####################")
    print(dataframe.dtypes)
    print("##################### Head #####################")
    print(dataframe.head(head))
    print("##################### Tail #####################")
    print(dataframe.tail(head))
    print("##################### NA #####################")
    print(dataframe.isnull().sum())
    print("##################### Quantiles #####################")
    print(dataframe.describe([0, 0.05, 0.50, 0.95, 0.99, 1]).T)

check_df(df)

# Adım 3
# Veri setinde eksik gözlem var mı? Varsa hangi değişkende kaç tane eksik gözlem vardır?

df.isnull().sum()
"""
##################### NA #####################
Invoice             0
StockCode           0
Description      1454  >> Eksik Gözlem
Quantity            0
InvoiceDate         0
Price               0
Customer ID    135080  >> Eksik Gözlem
Country             0
dtype: int64

"""
# Adım 4
# Eksik gözlemleri veri setinden çıkartınız. Çıkarma işleminde ‘inplace=True’ parametresini kullanınız.

df.dropna(inplace=True)
df.shape

# Adım 5
# Eşsiz ürün sayısı kaçtır?

df.head()
df["Description"].nunique()

# Adım 6
# Hangi üründen kaçar tane vardır

df["Description"].value_counts().head()

# Adım 7
# En çok sipariş edilen 5 ürünü çoktan aza doğru sıralayınız

df.groupby("Description").agg({"Quantity": "sum"}).sort_values(by=["Quantity"], ascending=False).head()

# Adım 8
# Faturalardaki ‘C’ iptal edilen işlemleri göstermektedir. İptal edilen işlemleri veri setinden çıkartınız.

df.head()
df["Invoice"].nunique()
df = df[~df["Invoice"].str.contains("C", na=False)]
df.describe().T

# Adım 9
# Fatura başına elde edilen toplam kazancı ifade eden ‘TotalPrice’ adında bir değişken oluşturunuz

df["TotalPrice"] = df["Quantity"] * df["Price"]
df.head()

df.groupby("Invoice").agg({"TotalPrice": "sum"}).head()

# Görev 2
# RFM Metriklerinin Hesaplanması

# Adım 1
# Recency, Frequency ve Monetary tanımlarını yapınız.

# RFM = Recency, Frequency, Monetary RFM metrikleridir.
# Bu metrikler kullanılarak belirli skorlar elde edilir ve bu skorlara göre müşteriler segmentlere ayırılır.
# Recency(yenilik) : Müşterinin en son ne zaman alışveriş yaptığını durumunu belirtmektedir.
# Hesaplanırken analizin yapıldığı tarihten müşterinin son yaptığı alışveriş tarihi çıkarılır.
# Frequency(Sıklık) : Müşterinin yaptığı alışveriş sayısıdır.İşlem sayısı sıklığıdır.
# Monetary(Parasal Değer)  : Müşterilerin bıraktığı parasal değerdir.

# Recency, Frequency, Monetary

# Adım 2
# Müşteri özelinde Recency, Frequency ve Monetary metriklerini groupby, agg ve lambda ile hesaplayınız.

# recency değeri için analiz tarihi ile müşterinin en son ne zaman alışveriş yaptığı tarih farkı alacağız.

df["InvoiceDate"].max() > Timestamp('2011-12-09 12:50:00')

today_date = dt.datetime(2011, 12, 11)
type(today_date)
df.head()

df.groupby("Customer ID").agg({"InvoiceDate": lambda InvoiceDate : (today_date - InvoiceDate.max()).days,
                                "Invoice": lambda Invoice : Invoice.nunique(),
                                "TotalPrice": lambda TotalPrice : TotalPrice.sum()})

# Adım 3
# Hesapladığınız metrikleri rfm isimli bir değişkene atayınız.

rfm = df.groupby("Customer ID").agg({"InvoiceDate": lambda InvoiceDate : (today_date - InvoiceDate.max()).days,
                                "Invoice": lambda Invoice : Invoice.nunique(),
                                "TotalPrice": lambda TotalPrice : TotalPrice.sum()})

# Adım 4
# Oluşturduğunuz metriklerin isimlerini recency, frequency ve monetary olarak değiştiriniz.

rfm.columns = ["recency", "frequency", "monetary"]

# recency değeri için bugünün tarihini (2011, 12, 11) olarak kabul ediniz
# rfm dataframe’ini oluşturduktan sonra veri setini "monetary>0" olacak şekilde filtreleyiniz.
rfm.describe().T
rfm = rfm[rfm["monetary"] > 0]

# Görev 3
# RFM Skorlarının Oluşturulması ve Tek bir Değişkene Çevrilmesi

# Adım 1
# Recency, Frequency ve Monetary metriklerini qcut yardımı ile 1-5 arasında skorlara çeviriniz.
# Adım 2
# Bu skorları recency_score, frequency_score ve monetary_score olarak kaydediniz.

rfm["recency_score"] = pd.qcut(rfm["recency"], 5, labels=[5, 4, 3, 2, 1])

rfm["frequency_score"] = pd.qcut(rfm["frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])

rfm["monetary_score"] = pd.qcut(rfm["monetary"], 5, labels=[1, 2, 3, 4, 5])

# Adım 3
# recency_score ve frequency_score’u tek bir değişken olarak ifade ediniz ve RF_SCORE olarak kaydediniz.

rfm["RF_SCORE"] =rfm["recency_score"].astype(str) + rfm["frequency_score"].astype(str)

rfm.head()

# Görev 4
# RF Skorunun Segment Olarak Tanımlanması

# Adım 1
# Oluşturulan RF skorları için segment tanımlamaları yapınız.

# RFM isimlendirmesi
seg_map = {
    r'[1-2][1-2]': 'hibernating',
    r'[1-2][3-4]': 'at_Risk',
    r'[1-2]5': 'cant_loose',
    r'3[1-2]': 'about_to_sleep',
    r'33': 'need_attention',
    r'[3-4][4-5]': 'loyal_customers',
    r'41': 'promising',
    r'51': 'new_customers',
    r'[4-5][2-3]': 'potential_loyalists',
    r'5[4-5]': 'champions'
}

# Adım 2
# Aşağıdaki seg_map yardımı ile skorları segmentlere çeviriniz.

rfm["segment"] = rfm["RF_SCORE"].replace(seg_map, regex=True)

# Görev 5
# Aksiyon Zamanı !

# Adım 1
# Önemli gördüğünü 3 segmenti seçiniz.
# Bu üç segmenti hem aksiyon kararları açısından hemde segmentlerin yapısı açısından(ortalama RFM değerleri) yorumlayınız.

rfm[["segment", "recency", "frequency", "monetary"]].groupby("segment").agg(["mean", "count"])

# Adım 2
# "Loyal Customers" sınıfına ait customer ID'leri seçerek excel çıktısını alınız.

new_df = pd.DataFrame()
new_df["loyal_customer_id"] = rfm[rfm["segment"] == "loyal_customers"].index
new_df.to_csv("loyal_customer_id.xlsx")