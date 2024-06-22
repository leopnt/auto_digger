from glob import glob
from tqdm import tqdm

from tensorflow.keras.models import load_model
import tensorflow.keras.backend as K
import tensorflow as tf

from generate_training_data import Track

class GlobalL2Pooling1D(tf.keras.layers.Layer):
    def call(self, inputs):
        return tf.sqrt(tf.reduce_sum(tf.square(inputs), axis=1))

def euclidean_distance(embeddings):
    x, y = embeddings
    sum_square = K.sum(K.square(x - y), axis=1, keepdims=True)
    return K.sqrt(K.maximum(sum_square, K.epsilon()))

def eucl_dist_output_shape(shapes):
    shape1, _ = shapes
    return (shape1[0], 1)

def contrastive_loss(y_true, y_pred):
    margin = 1.0
    square_pred = K.square(y_pred)
    margin_square = K.square(K.maximum(margin - y_pred, 0))
    return (y_true * square_pred + (1 - y_true) * margin_square)

# Custom objects for loading the model
custom_objects = {
    'GlobalL2Pooling1D': GlobalL2Pooling1D,
    'euclidean_distance': euclidean_distance,
    'eucl_dist_output_shape': eucl_dist_output_shape,
    'contrastive_loss': contrastive_loss
}

def distance(left_path: str, right_path: str, model, from_sec: int = 40, to_sec: int = 43):
    spec_left = Track(left_path).spectrogram(from_sec, to_sec)
    spec_right = Track(right_path).spectrogram(from_sec, to_sec)

    input_shape = model.input_shape[0][1:]
    spec_left_reshaped = spec_left.T.reshape(1, input_shape[0], input_shape[1])
    spec_right_reshaped = spec_right.T.reshape(1, input_shape[0], input_shape[1])

    pred = model.predict([spec_left_reshaped, spec_right_reshaped], verbose=False)
    
    return pred.ravel()[0]

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "query_path",
        help="track path to run query from"
    )
    parser.add_argument(
        "database_path",
        help="database of candidate tracks"
    )
    args = parser.parse_args()

    print("Load model...")
    model = load_model('siamese_model_n2.h5', custom_objects=custom_objects)

    print("Compare query to database...")
    scores = {'path': [], 'score': []}
    for track_path in tqdm(glob(f"{args.database_path}/*")):
        average_score = 0.0
        count = 0.0
        for offsets in range(60, 90, 3): # multiple spectrograms of length 3s on this timeframe
            similarity_score = distance(args.query_path, track_path, model, offsets, offsets+3)
            average_score += similarity_score
            count += 1.0

        scores[track_path] = average_score / count
    
    d_view = [(v,k) for k,v in scores.items()]
    d_view.sort(reverse=True)
    for v, k in d_view:
        print(f"{k}: {v}")
