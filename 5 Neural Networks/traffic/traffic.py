import cv2
import numpy as np

import os
# According to https://stackoverflow.com/questions/35911252/disable-tensorflow-debugging-information:
# 0 = all messages are logged (default behavior)
# 1 = INFO messages are not printed
# 2 = INFO and WARNING messages are not printed
# 3 = INFO, WARNING, and ERROR messages are not printed
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import sys
import tensorflow as tf

from sklearn.model_selection import train_test_split

EPOCHS = 10
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43
TEST_SIZE = 0.4




def main():

    # Check command-line arguments
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: python traffic.py data_directory [model.h5]")

    # Get image arrays and labels for all image files
    images, labels = load_data(sys.argv[1])

    # Split data into training and testing sets
    labels = tf.keras.utils.to_categorical(labels)
    x_train, x_test, y_train, y_test = train_test_split(
        np.array(images), np.array(labels), test_size=TEST_SIZE
    )

    # Get a compiled neural network
    model = get_model()

    # Fit model on training data
    model.fit(x_train, y_train, epochs=EPOCHS)

    # Evaluate neural network performance
    model.evaluate(x_test,  y_test, verbose=2)

    # Save model to file
    if len(sys.argv) == 3:
        filename = sys.argv[2]
        model.save(filename)
        print(f"Model saved to {filename}.")


def load_data(data_dir):
    """
    Load image data from directory `data_dir`.

    Assume `data_dir` has one directory named after each category, numbered
    0 through NUM_CATEGORIES - 1. Inside each category directory will be some
    number of image files.

    Return tuple `(images, labels)`. `images` should be a list of all
    of the images in the data directory, where each image is formatted as a
    numpy ndarray with dimensions IMG_WIDTH x IMG_HEIGHT x 3. `labels` should
    be a list of integer labels, representing the categories for each of the
    corresponding `images`.
    """
    images = list()
    labels = list()

    for root, dirs, files in os.walk(data_dir, topdown=False):
        # print(f'\n{root=}')
        # print(f'{dirs=}')

        try: label = int(os.path.split(root)[1])        ;print(f'{label=}')
        except ValueError: pass

        for name in files:
            if name.endswith('.ppm'):
                # print(f'{name=}')
                # print(os.path.join(root, name))

                img = cv2.imread(os.path.join(root, name))   
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)   
                img = cv2.resize(img, (IMG_WIDTH, IMG_HEIGHT))
                # print(f'{img=}')
                # cv2.imshow('image',img)
                # k = cv2.waitKey(0)

                images.append(img)
                labels.append(label)

    return (images, labels)


def get_model():
    """
    Returns a compiled convolutional neural network model. Assume that the
    `input_shape` of the first layer is `(IMG_WIDTH, IMG_HEIGHT, 3)`.
    The output layer should have `NUM_CATEGORIES` units, one for each category.
    """

    model = tf.keras.models.Sequential([

        # Recommended by https://www.pyimagesearch.com/2018/12/31/keras-conv2d-and-convolutional-layers/:
        #   - number of filters: 32, 64, or 128 for conv layer closest to input, 
        #     but start with smaller and only increase if necessary. After playing around with the rest of the steps,
        #     64 seems to bring me from 0.95 closer to 0.
        #   - filter size: only go above (3,3) if input image larger than 128x128
        #   - activation: seems fairly common to use relu
        tf.keras.layers.Conv2D(
            32, (3, 3), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)   
        ),

        # Max-pooling with a 2x2 pool size seems to be common
        tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),

        # Flatten units
        tf.keras.layers.Flatten(),

        # According to https://stats.stackexchange.com/questions/181/how-to-choose-the-number-of-hidden-layers-and-nodes-in-a-feedforward-neural-netw
        #   one hidden layer is usually enough for most problems 
        #   and although the previous source says the number of nodes should be the mean between the number of input and out neurons,
        #   according to http://www.faqs.org/faqs/ai-faq/neural-nets/part3/section-10.html
        #   the number of nodes depends on various factors and recommend to simply try with different numbers
        #   in this case it seems like the higher it is, the better?
        #   Reducing the dropout seems to have the largest effect, but it risks overfitting (and it feels like cheating) 
        tf.keras.layers.Dense(128*3, activation="relu"),
        tf.keras.layers.Dropout(0.25),

        # According to https://stats.stackexchange.com/questions/181/how-to-choose-the-number-of-hidden-layers-and-nodes-in-a-feedforward-neural-netw
        #   a classifer NN typically has in its output layer one node for each label if the activation is softmax
        tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax")
    ])

    model.compile(
        optimizer="adam",
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )

    return model

if __name__ == "__main__":
    main()
