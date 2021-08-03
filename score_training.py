import pandas as pd
import os
import json
import tensorflow as tf
import time
import sys
from score_model import Model, DataInput, DataEvalInput
from utils import MAP_PATH, CNT_PATH, MODEL_PATH, TRANS_ROOT_PATH, DATASET_ORI_PATH, RANDOM_STATE

def create_dir():
    """
    创建所需要的目录
    """
    # 创建数据处理后的data目录
    if not os.path.exists(TRANS_ROOT_PATH):
        print('Create dir: %s' % TRANS_ROOT_PATH)
        os.makedirs(TRANS_ROOT_PATH)

def data_transform():
    df = pd.read_csv(DATASET_ORI_PATH)
    column_name_list = [column_name for column_name in list(df.columns) if "column" in column_name]

    def build_map(df, col_name):
        key = sorted(df[col_name].unique().tolist())
        m = dict(zip(key, range(len(key))))
        m_reverse = dict(zip(range(len(key)), key))
        return m, m_reverse, key

    print("column_name : category_cnt")
    map_dict = {}
    cnt_dict = {}
    for column_name in column_name_list:
        m, m_reverse, key = build_map(df, column_name)
        category_cnt = len(key)
        print("%s : %d"%(column_name, category_cnt))
        map_dict[column_name] = {"m": m, "m_reverse": m_reverse}
        cnt_dict[column_name] = category_cnt
        df[column_name] = df[column_name].map(lambda x: m[x])
    with open(MAP_PATH, 'w') as f:
        json.dump(map_dict, f)
    with open(CNT_PATH, 'w') as f:
        json.dump(cnt_dict, f)

    df_shuffle = df.sample(frac=1.0, random_state=RANDOM_STATE)
    df_train = df_shuffle.iloc[:int(len(df_shuffle) * 0.8), :]
    df_eval = df_shuffle.iloc[int(len(df_shuffle) * 0.8):, :]
    return cnt_dict, df_train, df_eval, column_name_list

def main():
    tf.reset_default_graph()

    with tf.Session() as sess:
        model = Model(cnt_dict)
        sess.run(tf.global_variables_initializer())
        sess.run(tf.local_variables_initializer())

        start_time = time.time()

        for _epoch in range(1):
            for _, uij in DataInput(df_train, 1024, column_name_list):
                loss, spear = model.train(sess, uij)

                _iter = model.global_epoch_step.eval()
                print('\t Epoch %d \t Iter %d \t Cost time: %.2f \t Train_loss: %.4f \t Spearman: %.4f' %
                      (_epoch, _iter, time.time() - start_time, loss, spear))
                sys.stdout.flush()
                model.global_epoch_step_op.eval()

        eval_data_generator = DataEvalInput(df_eval, column_name_list)
        print(df_eval.shape)
        uij = eval_data_generator.generate_eval_data()
        loss, output, spear = model.evaluate(sess, uij)
        print('Eval_loss: %.4f \t Spearman: %.4f' % (loss, spear))
        eval_res_df = pd.DataFrame()
        eval_res_df['predict'] = output
        eval_res_df['label'] = uij['score']
        eval_res_df.to_csv('./trans_data/eval_out.csv')

        for _epoch in range(1):
            for _, uij in DataInput(df_eval, 1024, column_name_list):
                loss, spear = model.train(sess, uij)

                _iter = model.global_epoch_step.eval()
                print('\t Epoch %d \t Iter %d \t Cost time: %.2f \t Train_loss: %.4f \t Spearman: %.4f' %
                      (_epoch, _iter, time.time() - start_time, loss, spear))
                sys.stdout.flush()
                model.global_epoch_step_op.eval()

        saver = tf.train.Saver()
        saver.save(sess, MODEL_PATH)sss
        print("Finish Training!")

if __name__ == "__main__":
    create_dir()
    cnt_dict, df_train, df_eval, column_name_list = data_transform()
    main()