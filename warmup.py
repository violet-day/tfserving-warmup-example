import os
import tensorflow as tf
from tensorflow import saved_model
from tensorflow_serving.apis import model_pb2
from tensorflow_serving.apis import predict_pb2
from tensorflow_serving.apis import prediction_log_pb2


def make_assets_dir(export_dir):
  """
  create assets dir
  :param export_dir:
  :return:
  """
  assets_dir = os.path.join(export_dir, 'assets.extra')
  if tf.gfile.IsDirectory(assets_dir):
    tf.gfile.DeleteRecursively(assets_dir)

  tf.gfile.MakeDirs(assets_dir)
  tf.logging.info('mk dir %s done' % assets_dir)
  return assets_dir


def placeholder_to_random_tensor(placeholder_tensor, magic_dim=6):
  """
  convert placeholder tensor to random tensor
  :param placeholder_tensor:
  :param magic_dim:
  :return:
  """
  shape = placeholder_tensor.get_shape().as_list()
  shape = [magic_dim if s is None else s for s in shape]
  return tf.random_normal(shape=shape, dtype=placeholder_tensor.dtype)


def load_saved_model(sess, export_dir):
  """
  load saved_model from export dir
  :param sess:
  :param export_dir:
  :return:
  """
  graph_def = saved_model.loader.load(sess=sess, export_dir=export_dir,
                                      tags=[saved_model.tag_constants.SERVING])
  signature_def = graph_def.signature_def[saved_model.signature_constants.DEFAULT_SERVING_SIGNATURE_DEF_KEY]
  input_tensors = {
    k: tf.saved_model.utils.get_tensor_from_tensor_info(signature_def.inputs[k])
    for k, v in signature_def.inputs.items()
  }
  random_tensors = {k: placeholder_to_random_tensor(v, tf.flags.FLAGS.magic_dim) for k, v in input_tensors.items()}
  return random_tensors


def main(_):
  assets_dir = make_assets_dir(tf.flags.FLAGS.export_dir)
  with tf.Session() as session:
    random_tensors = load_saved_model(session, tf.flags.FLAGS.export_dir)
    with tf.python_io.TFRecordWriter(os.path.join(assets_dir, 'tf_serving_warmup_requests')) as writer:
      for _ in range(tf.flags.FLAGS.batch_size):
        request = predict_pb2.PredictRequest(
          model_spec=model_pb2.ModelSpec(name=tf.flags.FLAGS.name),
          inputs={k: tf.make_tensor_proto(v) for k, v in session.run(random_tensors).items()}
        )
        log = prediction_log_pb2.PredictionLog(
          predict_log=prediction_log_pb2.PredictLog(request=request))
        writer.write(log.SerializeToString())


if __name__ == "__main__":
  tf.flags.DEFINE_string('export_dir', None, 'model export dir')
  tf.flags.DEFINE_string('name', None, 'mode name in model.config')
  tf.flags.DEFINE_integer('batch_size', 256, 'how many records')
  tf.flags.DEFINE_integer('magic_dim', 6, 'dim use to replace None')

  tf.flags.mark_flag_as_required('export_dir')
  tf.flags.mark_flag_as_required('name')

  tf.app.run()
