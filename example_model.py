import tensorflow as tf

example_placeholder = tf.placeholder(shape=[10], dtype=tf.float32, name='example')
anchors_placeholder = tf.placeholder(shape=[None, 10], dtype=tf.float32, name='anchors')

distance = tf.norm(example_placeholder - anchors_placeholder, axis=1) / tf.norm(example_placeholder)
similarity = 1 - distance
similarity = similarity * tf.to_float(similarity >= 0)

sess = tf.Session()

inputs = {
  'example': example_placeholder,
  'anchors': anchors_placeholder
}

outputs = {
  'similarity': similarity
}

tf.saved_model.simple_save(sess, 'models/0', inputs, outputs)
