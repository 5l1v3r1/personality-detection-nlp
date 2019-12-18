# -*- coding: utf-8 -*-
"""naive_bayes.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1n4QXNgU5EoGG74zmtjnMP5MRumcForXy

<span style="font-size:1.1em;">Colab'a Google drive'ı entegre ediyoruz. Kullanılacak olan veriseti Google Drive'da bulunmaktadır</span>
"""

from google.colab import drive
drive.mount('/content/gdrive')

import pandas as pd

"""<span style="font-size:1.1em;">Google Drive'ımızın root pathi</span> ```gdrive/My Drive``` <span style="font-size:1.1em;">oluyor. Proje için gerekli verisetini **mbti** adında bir klasör oluşturup içerisine yüklüyoruz. İlgili verisetinin pathi</span> ```gdrive/My Drive/mbti/all_users.csv``` <span style="font-size:1.1em;">oluyor.</span>"""

df = pd.read_csv("gdrive/My Drive/mbti/all_users_v2.csv", sep = ';', header = 0)

df

import matplotlib.pyplot as plt

"""<span style="font-size:1.1em;">Verisetinin **class** tiplerine göre dağılım</span>"""

fig = plt.figure(figsize=(8,6))

df.groupby('typeClass').type.count().plot.bar(ylim=0)
plt.savefig('dataset_distribution_typeClass.png')
plt.show()

"""<span style="font-size:1.1em;">Verisetindeki **I/E** dağılımını göstermektedir. I olanlar x ekseninde 0 olarak E olanlar ise 1 olarak gösterilmektedir</span>"""

fig = plt.figure(figsize=(8,6))

df.groupby('I/E').type.count().plot.bar(ylim=0)
plt.savefig('gdrive/My Drive/mbti/dataset_distribution_I-E.png')
plt.show()

"""<span style="font-size:1.1em;">Verisetindeki **S/N** dağılımını göstermektedir. N olanlar x ekseninde 0 olarak S olanlar ise 1 olarak gösterilmektedir</span>"""

fig = plt.figure(figsize=(8,6))

df.groupby('S/N').type.count().plot.bar(ylim=0)
plt.savefig('gdrive/My Drive/mbtidataset_distribution_S-N.png')
plt.show()

"""<span style="font-size:1.1em;">Verisetindeki **T/F** dağılımını göstermektedir. F olanlar x ekseninde 0 olarak T olanlar ise 1 olarak gösterilmektedir</span>"""

fig = plt.figure(figsize=(8,6))

df.groupby('T/F').type.count().plot.bar(ylim=0)
plt.savefig('gdrive/My Drive/mbti/dataset_distribution_T-F.png')
plt.show()

"""<span style="font-size:1.1em;">Verisetindeki **J/P** dağılımını göstermektedir. P olanlar x ekseninde 0 olarak J olanlar ise 1 olarak gösterilmektedir</span>"""

fig = plt.figure(figsize=(8,6))

df.groupby('J/P').type.count().plot.bar(ylim=0)
plt.savefig('gdrive/My Drive/mbti/dataset_distribution_J-P.png')
plt.show()

"""Aşağıda ise verisetinin 16 farklı MBTI kişilik tiplerine göre dağılımı gösterilmektedir."""

fig = plt.figure(figsize=(8,4))

df.groupby('type').type.count().plot.bar(ylim=0)
plt.savefig('gdrive/My Drive/mbti/dataset_distribution_type.png')
plt.show()

"""Stop words, drive'da /mbti altındaki stop_words_tr.txt okunarak alınır

---
"""

file = open("gdrive/My Drive/mbti/stop_words_tr.txt")
stop_word_list = file.read().split('\n')
file.close()

stop_word_list

"""# Pre-Processing

Entrylere ön işleme adımları uygulanır. Bu adımlar:


1.   Bütün harflerin küçük harf haline getirilmesi

2.   '**bkz**', '**--- spoiler ---**', '**spoiler**', '**#12341324**' (gibi böyle rakamların devam ettiği) entrylerin verisetinden çıkarılması gerekmektedir.

3. Entrylerden stop words'ler silinmelidir.

4. Web sitelerinin temizlenmesi

5. Noktalama işaretlerinin temizlenmesi

6. Rakamların temizlenmesi

7. Stemming kullanılması

Temizlenme işlemlerinde empty string yerine space (' ') ile replace edilerek yapılmalıdır. Arından da fazla boşluklar vs trim edilmelidir.

```[+-]?([0-9]*)([.][0-9])?``` regex olarak kullanılacak hem rakamların silinmesinde hem de ondaklı sayıların silinmesinde --> buna gerek kalmadı

Entrylerdeki harfler küçük harf haline getirilir
"""

df['entry'] = df['entry'].str.lower()
df['entry']

"""Dataframe içerisindeki bütün entrylere '**bkz**', '**spoiler**', '**#**' içerip içermediğine bakar ve bunun sonucu index numarasıyla birlikte döner. ```15 True``` gibi bu demek oluyor ki 15 numaralı index bizim yazmış olduğumuz koşulu sağlamaktadır."""

indexes_contains_unwanted_words = df['entry'].str.contains('|'.join(['bkz', 'spoiler', r'#\d*']))

"""Dataframe'den ilgili entryler çıkartılır"""

df = df[~indexes_contains_unwanted_words]

df['entry']

"""Entrylerden stop words silinir.   --> Bu kısım gerekmeyebilir"""

df['entry'] = df['entry'].apply(lambda x: ' '.join([word for word in x.split() if word not in (stop_word_list)]))
df['entry']

"""Entrylerden web site linkleri silinir."""

df['entry'] = df['entry'].str.replace(r'http\S+', ' ', regex=True)
df['entry'] = df['entry'].str.replace(r'www\S+', '', regex=True)
df['entry']

"""Entrylerden noktalama işaretleri temizlenir."""

import string

df['entry'] = df['entry'].apply(lambda x: x.translate(str.maketrans(string.punctuation, ' '*len(string.punctuation))))
df['entry']

"""Entrylerden rakamlar silinir."""

df['entry'] = df['entry'].str.replace('\d+', ' ')
df['entry']

"""Verisetinin stemmera sokmadan önceki ön işlemeden geçirilmiş hali kaydedilir. Buradaki amaç stemmerdan geçirilmiş ve geçirilmemiş halinin başarı açısından karşılaştırılmasının yapılabilmesi."""

df.to_csv("gdrive/My Drive/mbti/preprocessed_dataset_no_stemming.csv", sep=';', encoding='utf-8')

"""SnowballStemmer içerisinde Türkçe dili için kullanabileceğimiz TurkishStemmer import edilir. Stemmer ile kelimelerin köklerine ulaşılır. Lemmatization işlemiyle kök bulunduğu zaman elde edilen kökler biçimsel açıdan da doğru olurken (yani mantıksal açıdan da) stemmer ile elde edilen köklerde böyle bir durum söz konusu değildir. Dolayısıyla stemming edilmis hallerine bakıldıgında mantıksal açıdan düzgün sonuclar vermeyebilir.

Google Colab'a snowballstemmer ile ilgil package'i indirmek için aşağıdaki komutu çalıştırıyoruz.
"""

!pip install snowballstemmer

from snowballstemmer import TurkishStemmer

stemmer = TurkishStemmer()
df['entry']

indexes = df.index

for i in range(len(indexes)):
    index = indexes[i]
    entry = df['entry'][index]
    entry_kokler = stemmer.stemWords(entry.split(" "))
    df['entry'][index] = " ".join(entry_kokler)

df['entry']

"""Stemmera sokulmuş hali kaydedilir."""

df.to_csv("gdrive/My Drive/mbti/preprocessed_dataset_with_stemming.csv", sep=';', encoding='utf-8')

"""TF-IDF özellik vektörünün çıkartılmasında kullanılacak değişken aşağıda belirlenmiş olan parametrelerle oluşturulur."""

from sklearn.feature_extraction.text import TfidfVectorizer

tfidf_vectorizer = TfidfVectorizer(sublinear_tf=True, norm='l2', encoding='utf-8', ngram_range=(1, 2), stop_words = stop_word_list, max_features=5000, analyzer = 'word', token_pattern=r'\w{1,}')

"""**Feature Extraction** 

Burada tf-idf vektörlerinin çıkartılmasında kullanılacak olan vocabulary oluşturulur.
"""

tfidf_vectorizer.fit(df['entry'])

"""Veriseti train ve test olmak üzere ikiye ayrılır. Test %20 ve train %80'ini oluşturacak şekilde tüm veriseti bölünür. random_state parametresi ile tekrardan bölündüğünde bir öncekiyle aynı train ve test veri setlerinin oluşturulması sağlanır."""

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(df['entry'], df['typeClass'], random_state = 42, test_size = 0.20)

"""Train ve test datasetlerinden tf-idf vektörleri çıkartılır"""

X_train_tfidf = tfidf_vectorizer.transform(X_train)
X_test_tfidf = tfidf_vectorizer.transform(X_test)

"""Multinominal Naive Bayes modeli oluşturulur. Oluşturulan bu model verisetinde "type" olarak belirtilen "analysts", "diplomats", "sentimenls", "explorers" sınıflarından hangilerine ait olduğunu tahmin etmek için kullanılır"""

from sklearn.naive_bayes import MultinomialNB

clf = MultinomialNB().fit(X_train_tfidf, y_train)
test_typeClass = y_test.values

predictions = clf.predict(X_test_tfidf)

predictions

"""<span style="font-size:1.1em">Yapılacak tahminlerle ilgili istatistiksel verileri tutmak için</span> ```predictions_result```<span style="font-size:1.1em"> adında bir değişken oluşturulur.</span>

<span style="font-size:1.1em">Bu değişkenin yapısı aşağıdaki gibidir.</span>

```json
{
    "predicted": {
        "analysts":  { "actual": {"analysts": 0, "diplomats": 0, "explorers": 0, "sentinels": 0} }
        "diplomats": { "actual": {"analysts": 0, "diplomats": 0, "explorers": 0, "sentinels": 0} }
        "explorers": { "actual": {"analysts": 0, "diplomats": 0, "explorers": 0, "sentinels": 0} }
        "sentinels": { "actual": {"analysts": 0, "diplomats": 0, "explorers": 0, "sentinels": 0} }
    }
}
```

* <span style="font-size:1.1em;">Yapılan tahminlerle ilgili verilere ulaşabilmek için</span>

    ```predictions_results['predicted']```


* <span style="font-size:1.1em;">Yapılan tahminin analyst ise:</span>

    ```predictions_results['predicted']['analysts']``` 


* <span style="font-size:1.1em;">Yapılan analyst tahmininin gerçek değerlerine erişmek için:</span>     

    ```predictions_results['predicted']['analysts']['actual']```  


* <span style="font-size:1.1em;">Test verisi, model tarafından analysts olarak tahmin edilmiştir ve bu verinin gerçek değeri de analysts'tir.</span>

    ```predictions_results['predicted']['analysts']['actual']['analysts']```
"""

prediction_results = {'predicted': {}}  ## prediction_result['analysts'] means prediction is 'analysts'

prediction_results['predicted']['analysts']  = {'actual': {'analysts': 0, 'diplomats': 0, 'explorers': 0, 'sentinels': 0}}
prediction_results['predicted']['diplomats'] = {'actual': {'analysts': 0, 'diplomats': 0, 'explorers': 0, 'sentinels': 0}}
prediction_results['predicted']['explorers'] = {'actual': {'analysts': 0, 'diplomats': 0, 'explorers': 0, 'sentinels': 0}}
prediction_results['predicted']['sentinels'] = {'actual': {'analysts': 0, 'diplomats': 0, 'explorers': 0, 'sentinels': 0}}

## prediction_result['analysts']['diplomats'] means prediction is analysts but actual value is diplomats

"""```prediction_results```<span style="font-size:1.1em"> içerisinde tutulan sayaçların değerleri arttırılır.</span>"""

for i in range(len(predictions)):
  predicted_value = predictions[i]
  actual_value = test_typeClass[i]
  prediction_results['predicted'][predicted_value]['actual'][actual_value] += 1

"""<span style="font-size:1.1em">JSON formatına çevrilir </span>```dict``` <span style="font-size:1.1em">tipi. Bu sayede daha okunaklı bir şekilde print edilmiş olur. </span>"""

import json

print(json.dumps(prediction_results, indent = 2))

"""<span style="font-size:1.1em;">İlgili field extract edilir</span> ```dict``` <span style="font-size:1.1em;">yapısından.</span>"""

results = prediction_results['predicted']

"""<span style="font-size:1.1em;">Başarı oranı hesaplanır</span>"""

accuracy = (results['analysts']['actual']['analysts'] + results['diplomats']['actual']['diplomats'] + results['explorers']['actual']['explorers'] + results['sentinels']['actual']['sentinels']) / len(predictions)
accuracy

"""<span style="font-size:1.1em;">**E/I** boyutu tahmin edilir</span>"""

X_train, X_test, y_train, y_test = train_test_split(df['entry'], df['I/E'], random_state = 42)  ## Geri kalanlar S, T, J

X_train_tfidf = tfidf_vectorizer.transform(X_train)
X_test_tfidf = tfidf_vectorizer.transform(X_test)

clf = MultinomialNB().fit(X_train_tfidf, y_train)
test_typeClass = y_test.values

predictions = clf.predict(X_test_tfidf)

predictions

predicted = {}
predicted['I'] = {'actual': {'I': 0, 'E': 0}}
predicted['E'] = {'actual': {'I': 0, 'E': 0}}
predicted

for i in range(len(predictions)):
  predicted[predictions[i]]['actual'][test_typeClass[i]] += 1

predicted

accuracy = (predicted['E']['actual']['E'] + predicted['I']['actual']['I']) / len(predictions)

accuracy

"""<span style="font-size:1.1em">**S/N** boyutu tahmin edilir.</span>"""

X_train, X_test, y_train, y_test = train_test_split(df['entry'], df['S/N'], random_state = 42)  ## Geri kalan boyutlar: T, J

X_train_tfidf = tfidf_vectorizer.transform(X_train)
X_test_tfidf = tfidf_vectorizer.transform(X_test)

clf = MultinomialNB().fit(X_train_tfidf, y_train)
test_typeClass = y_test.values

predictions = clf.predict(X_test_tfidf)

predicted['N'] = {'actual': {'N': 0, 'S': 0}}
predicted['S'] = {'actual': {'N': 0, 'S': 0}}

predicted

for i in range(len(predictions)):
  predicted[predictions[i]]['actual'][test_typeClass[i]] += 1

predicted

accuracy = (predicted['N']['actual']['N'] + predicted['S']['actual']['S']) / len(predictions)

accuracy

"""<span style="font-size:1.1em">**T/F** boyutu tahmin edilir.</span>"""

X_train, X_test, y_train, y_test = train_test_split(df['entry'], df['T/F'], random_state = 42)  ##  J

X_train_tfidf = tfidf_vectorizer.transform(X_train)
X_test_tfidf = tfidf_vectorizer.transform(X_test)

clf = MultinomialNB().fit(X_train_tfidf, y_train)
test_typeClass = y_test.values

predictions = clf.predict(X_test_tfidf)

predicted['T'] = {'actual': {'T': 0, 'F': 0}}
predicted['F'] = {'actual': {'T': 0, 'F': 0}}

predicted

for i in range(len(predictions)):
  predicted[predictions[i]]['actual'][test_typeClass[i]] += 1

predicted

accuracy = (predicted['F']['actual']['F'] + predicted['T']['actual']['T']) / len(predictions)

accuracy

"""<span style="font-size:1.1em">**J/P** boyutu tahmin edilir.</span>"""

X_train, X_test, y_train, y_test = train_test_split(df['entry'], df['J/P'], random_state = 42) 

X_train_tfidf = tfidf_vectorizer.transform(X_train)
X_test_tfidf = tfidf_vectorizer.transform(X_test)

clf = MultinomialNB().fit(X_train_tfidf, y_train)
test_typeClass = y_test.values

predictions = clf.predict(X_test_tfidf)

predicted['J'] = {'actual': {'J': 0, 'P': 0}}
predicted['P'] = {'actual': {'J': 0, 'P': 0}}

predicted

for i in range(len(predictions)):
  predicted[predictions[i]]['actual'][test_typeClass[i]] += 1

predicted

accuracy = (predicted['P']['actual']['P'] + predicted['J']['actual']['J']) / len(predictions)

accuracy

prediction_results['predicted'].update(predicted) 

prediction_results