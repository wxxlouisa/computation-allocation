import numpy as np
import lightgbm as lgb


class lgbm:
    def __init__(self, model_file='/home/wangxuanxuan/computation-allocation/score_estimation/gbm_model.txt', feature_encoder_file='/home/wangxuanxuan/computation-allocation/score_estimation/feature_encoding.npy'):
        self.model = lgb.Booster(model_file=model_file)
        self.feature_encoders = np.load(feature_encoder_file, allow_pickle=True)
        self.label_encoder = self.feature_encoders[0]
        self.target_encoder = self.feature_encoders[1]
        pass

    def preprocess(self, feature):
        one_hot_columns = ['column_5', 'column_4', 'column_7']
        num_class = [4, 4, 7]
        target_encoding_columns = ['column_1', 'column_3', 'column_6', 'column_8', 'column_10']
        target_features = []
        for col in target_encoding_columns:
            target_features.append(
                self.target_encoder[col][feature[col]] if feature[col] in self.target_encoder[col] else
                self.target_encoder['mean_socre'])
        target_features = np.array(target_features)
        one_hot_features = []
        for i, col in enumerate(one_hot_columns):
            label = self.label_encoder[col][feature[col]]
            one_hot_vector = np.zeros(num_class[i])
            one_hot_vector[label] = 1
            one_hot_features.append(one_hot_vector)
        one_hot_features = np.concatenate(one_hot_features)
        return np.concatenate([target_features, one_hot_features])


    def predict(self, feature):
        feature = self.preprocess(feature)
        feature = feature.reshape((1, -1))
        return self.model.predict(feature, num_iteration=self.model.best_iteration)
