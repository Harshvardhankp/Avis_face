from keras import __version__
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
import os


def generatedata(sourcepath,targetpath,prefix,mf):
	datagen = ImageDataGenerator(
        	rotation_range=0,
        	width_shift_range=0.2,
        	height_shift_range=0.2,
        	shear_range=0.2,
        	zoom_range=0.2,
        	horizontal_flip=True,
        	fill_mode='nearest')
	imagePaths=[os.path.join(sourcepath,f) for f in os.listdir(sourcepath)]
	cnt=0
	fact=int(mf)
	for imagePath in imagePaths:
		if os.path.isfile(imagePath) :
			print (imagePath)
			img = load_img(imagePath)  # this is a PIL image
			x = img_to_array(img)  # this is a Numpy array with shape (3, 150, 150)
			x = x.reshape((1,) + x.shape)  # this is a Numpy array with shape (1, 3, 150, 150)
	
			# the .flow() command below generates batches of randomly transformed images
			# and saves the results to the `preview/` directory
			i = 1
			for batch in datagen.flow(x, batch_size=16,save_to_dir=targetpath, save_prefix=prefix, save_format='jpeg'):
	    			i += 1
	    			if i >= fact:
	        			break  # otherwise the generator would loop indefinitely



#generatedata("./Data/train/gotu","./Data_final/gotu/","gotu" )  # generatedata(sourcepath,targetpath,prefix)


