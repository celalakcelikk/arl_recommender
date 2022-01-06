import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from itertools import chain
pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)

############################################
# Veri Ön İşleme İşlemlerini Gerçekleştiriniz
############################################
#: Önemli not!
##: 2010-2011 verilerilerini seçiniz ve tüm veriyi ön işlemeden geçiriniz. Germany seçimi sonraki basamakta olacaktır.

df_ = pd.read_excel("datasets/online_retail_II.xlsx", sheet_name="Year 2010-2011")
df = df_.copy()

def check_df(dataframe, head=5, tail=5):
    print("##################### Shape #####################")
    print(dataframe.shape)

    print("##################### Types #####################")
    print(dataframe.dtypes)

    print("##################### Head #####################")
    print(dataframe.head(head))

    print("##################### Tail #####################")
    print(dataframe.tail(tail))

    print("##################### NA #####################")
    print(dataframe.isnull().sum())

    print("##################### Quantiles #####################")
    print(dataframe.quantile([0, 0.05, 0.50, 0.95, 0.99, 1]).T)

    print("##################### Describe #####################")
    print(dataframe.describe().T)

    print("##################### Info #####################")
    print(dataframe.info())


def outlier_thresholds(dataframe, variable):
    quartile1 = dataframe[variable].quantile(0.01)
    quartile3 = dataframe[variable].quantile(0.99)
    interquantile_range = quartile3 - quartile1
    up_limit = quartile3 + 1.5 * interquantile_range
    low_limit = quartile1 - 1.5 * interquantile_range
    return low_limit, up_limit


def replace_with_thresholds(dataframe, variable):
    low_limit, up_limit = outlier_thresholds(dataframe, variable)
    dataframe.loc[(dataframe[variable] < low_limit), variable] = low_limit
    dataframe.loc[(dataframe[variable] > up_limit), variable] = up_limit


def retail_data_prep(dataframe):
    dataframe.drop(dataframe[dataframe["StockCode"] == "POST"].index, inplace=True)
    dataframe.dropna(inplace=True)
    dataframe = dataframe[~dataframe["Invoice"].str.contains("C", na=False)]
    dataframe = dataframe[dataframe["Quantity"] > 0]
    dataframe = dataframe[dataframe["Price"] > 0]
    replace_with_thresholds(dataframe, "Quantity")
    replace_with_thresholds(dataframe, "Price")
    return dataframe


df = retail_data_prep(df)
df[df['StockCode'] == "POST"]["Description"].unique()
check_df(df)

############################################
# Germany Müşterileri Üzerinden Birliktelik Kuralları Üretiniz
############################################

def create_invoice_product_df(dataframe, id=False):
    if id:
        return dataframe.groupby(['Invoice', "StockCode"])['Quantity'].sum().unstack().fillna(0). \
            applymap(lambda x: 1 if x > 0 else 0)
    else:
        return dataframe.groupby(['Invoice', 'Description'])['Quantity'].sum().unstack().fillna(0). \
            applymap(lambda x: 1 if x > 0 else 0)


def check_id(dataframe, stock_code):
    product_name = dataframe[dataframe["StockCode"] == stock_code][["Description"]].values[0].tolist()
    print(f"{stock_code}: {product_name}")


def create_rules(dataframe, id=True, country="France"):
    dataframe = dataframe[dataframe['Country'] == country]
    dataframe = create_invoice_product_df(dataframe, id)
    frequent_itemsets = apriori(dataframe, min_support=0.01, use_colnames=True)
    rules = association_rules(frequent_itemsets, metric="support", min_threshold=0.01)
    return rules


rules = create_rules(df, country="Germany")

rules.head()

############################################
# ID'leri verilen ürünlerin isimleri nelerdir?
############################################
#: Kullanıcı 1 ürün id'si: 21987
#: Kullanıcı 2 ürün id'si: 23235
#: Kullanıcı 3 ürün id'si: 22747

user_id = [21987, 23235, 22747]
for i in user_id:
    check_id(df, i)

############################################
# Sepetteki Kullanıcılar için Ürün Önerisi Yapınız
############################################


def uniq_chain(*args, **kwargs):
    seen = set()
    for x in chain(*args, **kwargs):
        if x in seen:
            continue
        seen.add(x)
        yield x


def arl_recommender(rules_df, product_id, rec_count=1):
    sorted_rules = rules_df.sort_values("lift", ascending=False)
    recommendation_list = []
    for i, product in sorted_rules["antecedents"].items():
        for j in list(product):
            if j == product_id:
                recommendation_list.append(list(sorted_rules.iloc[i]["consequents"]))
    recommendation_list = list(set(chain(*recommendation_list)))

    return recommendation_list[:rec_count]


for i in user_id:
    result = arl_recommender(rules, i, 1000).copy()
    print(f"{i} => İlk 10: {result[:10]} <-> Toplam Boyut: {len(result)}")

############################################
# Önerilen Ürünlerin İsimleri Nelerdir?
############################################

for i in user_id:
    check_id(df, arl_recommender(rules, i, 1)[0])
