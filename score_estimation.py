import tensorflow as tf
import json
from utils import MAP_PATH, CNT_PATH, MODEL_PATH
from score_model import Model
import random


class ScoreEstimation(object):
    def __init__(self):
        tf.reset_default_graph()
        self.sess = tf.Session()

        with open(MAP_PATH, 'r') as json_file:
            self.map_dict = json.load(json_file)

        with open(CNT_PATH, 'r') as json_file:
            self.cnt_dict = json.load(json_file)

        self.model = Model(self.cnt_dict)

        saver = tf.train.Saver()
        saver.restore(self.sess, MODEL_PATH)

    def predict(self, features):
        """
        given the features of a request, return its estimated score value.
        :param features: dict type, e.g. {feature1: xxx, ..., feature10:xxx}
        :return: the score value, float type
        """
        self.transform_features(features)
        print(features)
        score = self.model.predict(self.sess, features)[0]

        if score > 1:
            return 1
        elif score < 0:
            return 0
        else:
            return score

    def transform_features(self, features):
        for k, v in features.items():
            if k != 'req_id':
                if k == 'score':
                    features[k] = [v]
                else:
                    # 如果遇到之前不存在的特征，就直接取随机
                    features[k] = [self.map_dict[k]['m'].get(v, random.randint(0, self.cnt_dict[k]))]

if __name__ == '__main__':
    score_estimator = ScoreEstimation()
    uij = {'req_id':'GHFYUVFyugqwwfuwqbfqwfnqw',
           'column_1': '065b6e528c7e45b506ba44f383e5b70e',
           'column_2': '0000de66b99ca7079dbb185feb62cada',
           'column_3': '0a323bb716b22836ccfd46261d9189ec',
           'column_4': 'c8a67ca09751dcd119f352c9c289a96b',
           'column_5': '857d012e28fb1e16b9ab5b0362cefd94',
           'column_6': '045d262d25ddfed7dc3caa5f3a0afef9',
           'column_7': '8c57d6f8316b24c0754f96f5f5ad2a84',
           'column_8': 'ee63caa6a4f918f33d022fbbe2ad3e4c',
           'column_9': '0377d8cd178e15c7becf3157f71ab77b',
           'column_10': '0f51d1f88f4aa678cacb0e97d0e12a64',
           'score': 0.2555449903011322}
    score = score_estimator.predict(uij)
    print(score)