import sys
sys.path.append('/home/wangxuanxuan/computation-allocation/')
import numpy as np
import pandas as pd


class DecisionModuleOnline:
    def __init__(self, param_file_name='params.npy'):
        try:
            self.params = np.load(param_file_name, allow_pickle=True).item()
            print(self.params)
        except FileNotFoundError as e:
            print("Error when loading parameter file", e)

    def decide(self, score, drop_ratio):
        try:
            return score < self.params[drop_ratio] # true: drop
        except KeyError as e:
            print("Error when looking for the parameter of given drop_ratio: ", e)


class DecisionModuleOffline:
    def __init__(self, data_file_name, train_data_ratio, drop_ratios):
        # load data and shuffle it
        data = pd.read_csv(data_file_name)
        N = len(data)
        shuffle_ids = np.random.permutation(N)
        self.data = data.iloc[shuffle_ids]
        train_data_size = int(N * train_data_ratio)
        self.train_data = self.data.iloc[:train_data_size]
        self.test_data = self.data.iloc[train_data_size:]
        self.drop_ratios = drop_ratios
        self.quantiles = []
        pass

    def train(self):
        for q in self.drop_ratios:
            self.quantiles.append(self.train_data['score'].quantile(q))

    def test(self, sample_size):
        # generate sampled data
        test_inds = np.random.randint(low=0, high=len(self.test_data), size=sample_size)
        test_data_sample = self.test_data.iloc[test_inds]
        test_score_sample = test_data_sample['score'].values
        S = np.sum(test_score_sample)

        # calculate the droped score ratio based on the quantiles
        drop_scores = []
        drop_ratios_alg = []
        for thd in self.quantiles:
            drop_scores.append(np.sum(test_score_sample[test_score_sample < thd]) / S)
            drop_ratios_alg.append(len(test_score_sample[test_score_sample < thd]) / sample_size)

        # calculate the best droped score ratio
        best_drop_scores = []
        test_score_sample.sort()
        for q in self.drop_ratios:
            best_drop_scores.append(np.sum(test_score_sample[: int(q * len(test_score_sample))]) / S)

        # calculate the drop score ration of random dropping strategy
        random_drop_scores = []
        for q in self.drop_ratios:
            np.random.shuffle(test_score_sample)
            random_drop_scores.append(np.sum(test_score_sample[: int(q * len(test_score_sample))]) / S)
        return drop_scores, best_drop_scores, random_drop_scores, drop_ratios_alg
