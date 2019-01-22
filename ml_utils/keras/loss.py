import tensorflow as tf
from keras import backend as K


# Root Mean Squared Loss Function
def rmse(y_true, y_pred):
    return K.sqrt(K.mean(K.square(y_pred - y_true)))


# IoU metric
def mean_iou(y_true, y_pred):
    prec = []
    for t in np.arange(0.5, 1.0, 0.05):
        y_pred_ = tf.to_int32(y_pred > t)
        score, up_opt = tf.metrics.mean_iou(y_true, y_pred_, 2)
        K.get_session().run(tf.local_variables_initializer())
        with tf.control_dependencies([up_opt]):
            score = tf.identity(score)
        prec.append(score)
    return K.mean(K.stack(prec), axis=0)


def iou_loss(target, output):
    """Compute IoU between an output tensor (prediction) and a target tensor.
    # Arguments
        target: The label/ground truth tensor with the same shape as `output`.
        output: The prediction/logits tensor.
    # Returns
        A tensor.
    """

    #print("target: ", target.shape)
    #print("output: ", output.shape)

    #assert target.shape == output.shape
    pred = tf.reshape(output, [-1])
    gt_labels = tf.reshape(target, [-1])

    mul_x_y = tf.multiply(pred, gt_labels)
    inter = tf.reduce_sum(mul_x_y)

    union = tf.reduce_sum(tf.subtract(tf.add(pred, gt_labels), mul_x_y))

    iou = tf.divide(inter, union)
    return tf.subtract(tf.constant(1.0, dtype=tf.float32), iou)
