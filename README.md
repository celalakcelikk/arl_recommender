# Association Rule Learning Recommender System (Birliktelik Kuralları Öğrenimli Tavsiye Sistemi)

## İş Problemi
Sepet aşamasındaki kullanıcılara ürün önerisinde bulunmak.

## Veri Seti Hikayesi
* **Online Retail** II isimli veri seti İngiltere merkezli online bir satış mağazasının 01/12/2009 - 09/12/2011 tarihleri arasındaki satışlarını içeriyor.
* Bu şirketin ürün kataloğunda hediyelik eşyalar yer alıyor. Promosyon ürünleri olarak da düşünülebilir.
* Çoğu müşterisinin toptancı olduğu bilgisi de mevcut.

## Veri Seti Değişkenleri
* **Invoice:** Fatura Numarası. Eğer bu kod C ile başlıyorsa işlemin iptal edildiğini ifade eder.
* **StockCode:** Ürün kodu. Her bir ürün için eşsiz numara.
* **Description:** Ürün ismi 
* **Quantity:** Ürün adedi. Faturalardaki ürünlerden kaçar tane satıldığını ifade etmektedir.
* **InvoiceDate:** Fatura tarihi 
* **UnitPrice:** Fatura fiyatı (Sterlin)
* **CustomerID:** Eşsiz müşteri numarası 
* **Country:** Ülke ismi

## Not
Aşağıda 3 farklı kullanıcının sepet bilgileri verilmiştir. Bu sepet bilgilerine en uygun ürün önerisini yapınız. 

**Not:** Ürün önerileri 1 tane ya da 1'den fazla olabilir. 

**Önemli not:** Karar kurallarını 2010-2011 Germany müşterileri üzerinden türetiniz.

* Kullanıcı 1 ürün id'si: 21987 
* Kullanıcı 2 ürün id'si: 23235 
* Kullanıcı 3 ürün id'si: 22747
