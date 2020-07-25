import tensorflow as tf
import pandas as pd
import numpy as np

df = pd.read_pickle('marked_img.pickle')
x = df.iloc[:, 0]
y = df.iloc[:, 1]

l0 = tf.keras.layers.Flatten(input_shape=(500, 500))
l1 = tf.keras.layers.Dense(150, activation=tf.nn.relu)
l2 = tf.keras.layers.Dense(2, activation=tf.nn.softmax)
model = tf.keras.Sequential([l0, l1, l2])
model.compile(optimizer=tf.optimizers.Adam(),
              loss='sparse_categorical_crossentropy')
model.fit(np.array([el for el in x]), np.array(y), epochs=5)

model.save('sudoku_recognition.h5')
