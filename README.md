# CNN kullanarak otomatik dudak okuma
Bu, aslında 10 kelime ve 10 kelime öbeği konuşan insanları sınıflandıran küçük bir projedir. Giriş bir videodur ve makine kelimeyi / ifadeyi video karelerindeki yüz ve dudak hareketlerine göre 20 nesneden sınıflandıracaktır.

# Başlarken
Pekala, proje hakkında fikir verecek, video girdiğimiz, çerçeveler aldığımız, birleştirdiğimiz, yeniden boyutlandırdığımız, modele beslediğimiz, sınıflandırdığımız bir GUI (Uygulama.py) var. Bütün bunlar aşağıda açıklanmıştır.

İçindekiler
=================
<!--ts-->
   * [CNN kullanarak Otomatik Dudak okuma](#cnn-kullanarak-otomatik-dudak-okuma)
   * [Başlarken](#başlarken)
   * [İçindekiler](#içindekiler)
   * [Kitaplıklar](#kitaplıklar)
   * [Veri Kümesi](#veri-kümesi)
   * [Model](#model)
   * [Sonuç ve Analiz](#sonuç-ve-analiz)
   * [Genel Uygulama](#genel-uygulama)
   * [Sonuç](#sonuç)
   * [Gelecek Kapsam](#gelecek-kapsam)
<!--te-->

# Kitaplıklar
Bu projede birçok Python kütüphanesi kullanıldı. Bunları şu şekilde kurmanızı tavsiye ederim:
```
CV'yi açın: pip install opencv-python
Tkinter: apt-get install python-tk
Pillow: pip Install Pillow
Numpy: pip install numpy
Tensorflow: pip install tensorflow-gpu
```
Sürümlerde belirsizlik olabileceğinden kitaplıkları yüklerken hatalar meydana gelebilir. Bu yüzden sürümü değiştirmeyi kontrol edin. Ayrıca modeli google colab'da eğitmek için tensorflow-gpu kullandım. Yani bir kolab kullanılabilir, oldukça iyidir.

# Veri Kümesi
Herhangi bir makine öğrenimi problemi için en önemli şey veridir. Verileri 15 kişiden(7 Erkek 8 Kadın) oluşturduk. Veri Kümesi, her nesnede 10 kez 15 konuşmacı tarafından söylenen 10 kelime ve 10 ifadeden oluşur.
Veriler, görüntü dizisi biçimindeydi. Zor olan kısım, bu veri setini model için gerekli olan doğru forma dönüştürmekti.
Veri setini tek bir görüntü girişi olarak dönüştürdük. Bu, aşağıdaki şekilde gösterilebilir:
<br/>
Yukarıdaki şekilde olduğu gibi, veri seti sol taraftaki görüntü dizisini içerir. Tüm konuşmacıların yüz kısımlarını görüntü sırasına göre bölümlere ayırdık. Sol tarafta görüldüğü gibi özellikleri çıkarmak zor, bu yüzden görüntülerden yüzü çıkardık. Bu, veri kümesindeki her görüntü ile yapılır.

Her bir görüntüden yüzleri çıkardıktan sonra, görüntü dizilerini tek bir görüntüde birleştirdik. Bu bir çeşit matris gibi görünebilir. Bu adım, basit CNN kullandığımız ve LSTM ve RNN gibi gelişmiş konuları kullandığımız için yapılmıştır. Yastık kullanarak bunu kolayca yapabiliriz. Söylenen her kelime / kelime öbeği için, bu tür birleştirilmiş görüntüler oluşturduk.
Ayrıca sabit bir boyuta yeniden boyutlandırdık, yani burada 224 * 224 olarak yeniden boyutlandırdık.
<br/>
Bundan sonra tek bir kelime / ifade için 150 resim içeren veri setini alıyoruz, ancak her nesneye kendi 20 tane daha ekledik, yani iki konuşmacımız 10 kelime ve 10 kelime öbeği söyledi ve bu veri setine eklendi.
<br/>
Yani genel olarak 3400 resmimiz var (her biri 10 kez 20 nesne söyleyen 17 konuşmacı) ve tren testini 80-20 olarak ayırdık.

# Model
Veri kümesini doğru biçimde aldıktan sonra, sonraki adım Uygulama Modeli'dir.
<br/>
Modelin tamamı ve uygulaması, modeli oluşturduğumuz [final.ipynb](final.ipynb) dosyasındadır. Dosyada Görüntü veri üreteci, çeşitli CNN katmanları, analiz bölümü bulunmaktadır.
<br/>
Model şu şekildedir:
```
model = Sequential()

# 1 - Convolution
model.add(Conv2D(64,(3,3), padding='same', input_shape=(224, 224,1)))
model.add(BatchNormalization())
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

# 2nd Convolution layer
model.add(Conv2D(128,(5,5), padding='same'))
model.add(BatchNormalization())
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

# 3rd Convolution layer
model.add(Conv2D(512,(3,3), padding='same'))
model.add(BatchNormalization())
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

# 4th Convolution layer
model.add(Conv2D(512,(3,3), padding='same'))
model.add(BatchNormalization())
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

# Flattening
model.add(Flatten())

# Fully connected layer 1st layer
model.add(Dense(256))
model.add(BatchNormalization())
model.add(Activation('relu'))
model.add(Dropout(0.25))

# Fully connected layer 2nd layer
model.add(Dense(512))
model.add(BatchNormalization())
model.add(Activation('relu'))
model.add(Dropout(0.25))

model.add(Dense(nb_classes, activation='softmax'))

opt = Adam(lr=0.0001)
model.compile(optimizer=opt, loss='categorical_crossentropy', metrics=['accuracy'])
```
   4 Conv 2D katman (Normalizasyon, MaxPooling, Dropout ve Activation ile birlikte) ve 2 tamamen bağlı katman vardır. Model, Adam optimizer ile 0.0001 lr ve
kayıp = 'categorical_crossentropy' ile derlenmiştir.
```
epochs = 50

import ModelCheckpoint from keras.callbacks

checkpoint = ModelCheckpoint ("my_model.h5", monitor = 'val_acc', verbose = 1, save_best_only = True, mode = 'max')
callbacks_list = [kontrol noktası]

history = model.fit_generator (generator = train_generator,
                                steps_per_epoch = train_generator.n // train_generator.batch_size,
                                epochs = epochs,
                                validation_data = validation_generator,
                                validation_steps = validation_generator.n // validation_generator.batch_size,
                                callbacks = callbacks_list
                                )
```
Model daha sonra yukarıda gösterildiği gibi epochs = 50 ve parti boyutu = 20 ile donatılmıştır. Sonuç ve Analiz aşağıda tartışılmaktadır.
<br/>
# Sonuç ve Analiz
Model iyi bir eğitim doğrulama doğruluğu göstermektedir. Bu en iyi model değil ama oldukça iyi bir model. Karışıklık matrisi aşağıda gösterildiği gibidir:


# Genel Uygulama
Genel uygulama, bir uygulama penceresini açan Uygulama.py dosyasını çalıştırıyor. Dudak okumak istediğimiz videoyu seçebiliriz. Bu video sesli olabilir veya gürültülü bir ortamdan olabilir.
Sistem, kareleri videodan çıkarır, yani aslında görüntü dizisini alır. Bu, onu tek bir görüntü halinde birleştirecek ve 224 * 224 olarak yeniden boyutlandıracaktır. Daha sonra kaydedilen modele aktarılır ve sonuç, GUI'nin kendisindeki metin tahminidir.

# Sonuç
Yani bu giriş seviyesi için oldukça iyi bir proje. Ayrıca belirsizlik, sınırlı veri kümesi nedeniyle yeni yüzler algılandığında yaşanan sorunlar gibi bazı sorunlar ortaya çıkmaktadır. Ayrıca bilinen yüzlerle uyumludur. Bu yüzden çalışmak için oldukça iyi bir proje.

# Gelecek Kapsam
Bu proje gerçek zamanlı dudak okuma uygulanarak genişletilebilir, bu veri setine daha fazla yüz eklenerek sağlanabilir. Türkçe dilindeki birbirine yakın kelimeler için, bazı NLP ve LSTM / RNN teknikleri eklenerek de ele alınabilir.
