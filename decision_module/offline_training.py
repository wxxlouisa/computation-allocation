import sys
sys.path.append('/home/wangxuanxuan/computation-allocation/')
sys.path.append('/home/wangxuanxuan/computation-allocation/score_estimation/')
from decision_module import DecisionModuleOffline, DecisionModuleOnline
from utils import plot, plot_bar
import numpy as np

if __name__ == '__main__':
    drop_ratios = np.arange(1, 100) / 100
    num_drop_ratio = len(drop_ratios)
    decision_offline = DecisionModuleOffline(data_file_name='/home/wangxuanxuan/computation-allocation/data/source.post.csv', train_data_ratio=0.8,
                                             drop_ratios=drop_ratios)

    decision_offline.train()
    np.save('/home/wangxuanxuan/computation-allocation/output/params.npy', dict(zip(drop_ratios, decision_offline.quantiles)))

    for sample_size in [100, 1000, 10000, 100000]:
        num_trial = 10
        drop_scores_avg = np.zeros(num_drop_ratio)
        best_drop_scores_avg = np.zeros(num_drop_ratio)
        drop_ratios_alg_avg = np.zeros(num_drop_ratio)
        for _ in range(num_trial):
            drop_scores, best_drop_scores, _, drop_ratios_alg = decision_offline.test(sample_size)
            drop_scores_avg += np.array(drop_scores)
            best_drop_scores_avg += np.array(best_drop_scores)
            drop_ratios_alg_avg += np.array(drop_ratios_alg)
        drop_scores_avg /= num_trial
        best_drop_scores_avg /= num_trial
        drop_ratios_alg_avg /= num_trial

        plot(drop_ratios, [drop_scores_avg, best_drop_scores_avg], labels=['our algorithm', 'best'],
             xlabel='drop ratio', ylabel='score ratio', title='dropped score ratio under different drop ratios')

        plot(drop_ratios, [drop_ratios_alg_avg, drop_ratios], labels=['our algorithm', 'best'],
             xlabel='drop ratio', ylabel='drop ratio of our algorithm', title='drop ratio of our algorithm')
