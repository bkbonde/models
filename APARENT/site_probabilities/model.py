from kipoi.model import BaseModel
from keras.models import load_model
import numpy as np


class APARENTModel(BaseModel):

    def __init__(self, weights):
        self.weights = weights
        self.model = load_model(weights)

    def _predict(self, inputs):
        batch_size = inputs.shape[0]

        input_1 = np.expand_dims(inputs, -1)
        input_2 = np.zeros([batch_size, 13])
        input_3 = np.ones([batch_size, 1])

        _, pred = self.model.predict_on_batch([input_1, input_2, input_3])

        site_probs = pred[:, 1:]
        polya_prob = pred[:, 0]
        return site_probs, polya_prob

    def predict_on_batch(self, inputs):
        site_probs, polya_prob = self._predict(inputs)

        return {
            "logit_polya_prob": polya_prob,
            "logit_site_probs": site_probs,
        }
