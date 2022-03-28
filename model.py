# imports
from keras import layers
from keras.models import Sequential
from matplotlib import pyplot as plt
import tensorflow as tf


# some variables for the images
batch_size = 32
img_height = 180
img_width = 180

data_dir = 'dataset/Set1'
test_dir = 'dataset/Set2'


# generating dataset train and val with 80/20 split between training and testing
try:
    train_ = tf.keras.utils.image_dataset_from_directory(
        data_dir,
        validation_split=0.2,
        subset="training",
        seed=123,
        image_size=(img_height, img_width),
        batch_size=batch_size)

    val_ = tf.keras.utils.image_dataset_from_directory(
        data_dir,
        validation_split=0.2,
        subset="validation",
        seed=123,
        image_size=(img_height, img_width),
        batch_size=batch_size)

except Exception as e:
    print("Error: ", e)
    exit()

# printing the class names of the dataset
class_names = train_.class_names
print(class_names)


# normalizing and standarding the dataset to eliminate any bias
normalization_layer = layers.Rescaling(1. / 255)
normalized_ds = train_.map(lambda x, y: (normalization_layer(x), y))


# data augmentation - flipping horizontal, vertical, roation and zoom
data_augmentation = tf.keras.Sequential(
    [
        layers.RandomFlip("horizontal",
                          input_shape=(img_height,
                                       img_width,
                                       3)),
        layers.RandomFlip("vertical",
                          input_shape=(img_height,
                                       img_width,
                                       3)),
        layers.RandomRotation(0.2),
        layers.RandomZoom(0.3),
    ]
)

# assigning the classes length for dense layer
num_classes = len(class_names)


# the cnn model which takes image with size 180 x 180 x 3
model = Sequential([
    layers.Rescaling(1. / 255, input_shape=(img_height, img_width, 3)),
    layers.Conv2D(16, 3, padding='same', activation='relu'),
    layers.MaxPooling2D(),
    layers.Conv2D(32, 3, padding='same', activation='relu'),
    layers.MaxPooling2D(),
    layers.Conv2D(64, 3, padding='same', activation='relu'),
    layers.MaxPooling2D(),
    layers.Dropout(0.5),
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dense(num_classes)
])

# using adam optimizer to compile the model
model.compile(optimizer='adam', loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True), metrics=['accuracy'])

# prints the model information in the console
model.summary()


# fitting the model with the train and test data and running it for 10 ephochs
epochs = 10
history = model.fit(train_, validation_data=val_, epochs=epochs)


# history plot based
acc = history.history['accuracy']
val_acc = history.history['val_accuracy']

loss = history.history['loss']
val_loss = history.history['val_loss']

epochs_range = range(epochs)

plt.figure(figsize=(8, 8))
plt.subplot(1, 2, 1)
plt.plot(epochs_range, acc, label='Training Accuracy')
plt.plot(epochs_range, val_acc, label='Validation Accuracy')
plt.legend(loc='lower right')
plt.title('Training and Validation Accuracy')

plt.subplot(1, 2, 2)
plt.plot(epochs_range, loss, label='Training Loss')
plt.plot(epochs_range, val_loss, label='Validation Loss')
plt.legend(loc='upper right')
plt.title('Training and Validation Loss')
plt.show()