import tensorflow as tf
import pandas as pd
import numpy as np

df = pd.read_pickle('new_squares.pickle')
x = df.iloc[:, 0]
y = df.iloc[:, 1]

l0 = tf.keras.layers.Flatten(input_shape=(50, 50))
l1 = tf.keras.layers.Dense(300, activation=tf.nn.relu)
l2 = tf.keras.layers.Dense(300, activation=tf.nn.relu)
l3 = tf.keras.layers.Dense(10, activation=tf.nn.softmax)
model = tf.keras.Sequential([l0, l1, l2, l3])
model.compile(optimizer=tf.optimizers.Adam(),
              loss='sparse_categorical_crossentropy')
model.fit(np.array([el for el in x]), np.array(y), epochs=500)

model.save('num_recognition.h5')
