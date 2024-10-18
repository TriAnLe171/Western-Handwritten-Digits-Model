import tensorflow as tf
import numpy as np
import tensorflow_datasets as tfds
import matplotlib.pyplot as plt

# Load MNIST dataset
(train_images, train_labels), (test_images, test_labels) = tf.keras.datasets.mnist.load_data()

# Convert images and labels to tensors
train_images = tf.convert_to_tensor(train_images, dtype=tf.float32)
train_labels = tf.convert_to_tensor(train_labels, dtype=tf.int32)
test_images = tf.convert_to_tensor(test_images, dtype=tf.float32)
test_labels = tf.convert_to_tensor(test_labels, dtype=tf.int32)


# Create a TensorFlow dataset from the data
train_dataset = tf.data.Dataset.from_tensor_slices((train_images, train_labels))
test_dataset = tf.data.Dataset.from_tensor_slices((test_images, test_labels))

# Shuffle and batch the training dataset
batch_size = 64
train_dataset = train_dataset.shuffle(buffer_size=len(train_images)).batch(batch_size)

# Choose CPU or GPU to execute the code
devices = tf.config.list_physical_devices("GPU")
if len(devices) > 0:
    device = "GPU"
else:
    device = "CPU"

print(f"Using {device} device")

# Neural network 
# Don't need to do the low-level details, keras can do it
model = tf.keras.Sequential()
# model.add(tf.keras.layers.Conv2D(filters=32,kernel_size=(3,3),activation='relu', input_shape= (28,28,1)))
# model.add(tf.keras.layers.MaxPooling2D((2, 2)))
# model.add(tf.keras.layers.Conv2D(64, (3, 3), activation='relu'))
# model.add(tf.keras.layers.MaxPooling2D((2, 2)))
# model.add(tf.keras.layers.Conv2D(64, (3, 3), activation='relu'))
model.add(tf.keras.layers.Flatten())
model.add(tf.keras.layers.Dense(512, activation='relu'))
model.add(tf.keras.layers.Dense(256, activation='relu'))
model.add(tf.keras.layers.Dense(10))
# model.summary()

num_epochs=3
# Choose the optimizer algorithm, loss function, and evaluation metrics
model.compile(
    optimizer=tf.keras.optimizers.Adam(0.001),
    loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
    metrics=[tf.keras.metrics.SparseCategoricalAccuracy()], #the model will compute the accuracy using SparseCategoricalAccuracy()
)

# Training (and maybe testing) process

model.fit(
    train_dataset,
    epochs=num_epochs,
    batch_size=batch_size,
)
    
test_dataset_batched = test_dataset.batch(batch_size)
test_loss, test_accuracy = model.evaluate(test_dataset_batched)
print(f"Test Loss: {test_loss}")
print(f"Test Accuracy: {test_accuracy}")

# Perform prediciton on i-th image
i=np.random.randint(0,len(test_images))

img=test_images[i]
img = tf.expand_dims(img, axis=0)

# Perform prediction on the digit image
prediction = model.predict(img)
predicted_label = np.argmax(prediction)
confidence = np.max(prediction)

print(confidence)
print(predicted_label)

image = test_images[i]

# Display the image
plt.imshow(image, cmap='gray')
plt.axis('off')  # Remove axis labels
plt.show()