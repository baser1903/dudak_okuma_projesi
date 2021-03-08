from FramesExtraction import extractFrames
from concat import concatFrames
from resize import resize1
from ourmodel import createModel
import os
import cv2
import numpy as np


def prediction(vidcap):
    vidcap = cv2.VideoCapture(vidcap)
    extractFrames(vidcap)
    concatFrames(1)
    path = "./Resimler/"
    for file in os.scandir(path):
        if file.name.endswith(".jpg"):
            os.unlink(file.path)
    pathnew = "./Sonuc/image.jpg"       
    image1 = resize1(pathnew)
    height, width, channels = image1.shape
    pic_size = 224
    """
	# number of images to feed into the NN for every batch
	batch_size = 20
	datagen_train = ImageDataGenerator()
	datagen_validation = ImageDataGenerator()
	train_generator = datagen_train.flow_from_directory(base_path + "train",
		                                                target_size=(pic_size,pic_size),
		                                                color_mode="grayscale",
		                                                batch_size=batch_size,
		                                                class_mode='categorical',
		                                                shuffle=True)
	validation_generator = datagen_validation.flow_from_directory(base_path + "test",
		                                                target_size=(pic_size,pic_size),
		                                                color_mode="grayscale",
		                                                batch_size=batch_size,
		                                                class_mode='categorical',
		                                                shuffle=False)
	"""	                                                
    model = createModel(pic_size, pic_size)
    model.load_weights("./my_newmodel.h5")
    print("Model yüklendi..")
    OBJECT_LIST = ["Dur", "Seç", "Bağ", "Affedersiniz", "Güle güle", "İyi günler",
                     "Merhaba", "Nasılsın", "Üzgünüm", "Bu oyunu seviyorum", "Navigasyon", 
                     "Sonraki", "Tanıştığımıza memnun oldum" ,"Önceki", "Başlat", "Başla", "Navigasyonu durdur",
                     "Teşekkür ederim", "Ağ", "Rica ederim"]
    gray = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray = gray.reshape(224,224,1)
    some = (OBJECT_LIST[model.predict_classes(np.array([gray]))[0]])
    print(some)
    return some