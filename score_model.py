import tensorflow as tf
from scipy.stats import spearmanr

class Model(object):
    def __init__(self, cnt_dict):
        # id类特征
        self.column_1 = tf.placeholder(tf.int32, [None, ], name='column_1')
        self.column_2 = tf.placeholder(tf.int32, [None, ], name='column_2')
        self.column_3 = tf.placeholder(tf.int32, [None, ], name='column_3')
        self.column_4 = tf.placeholder(tf.int32, [None, ], name='column_4')
        self.column_5 = tf.placeholder(tf.int32, [None, ], name='column_5')
        self.column_6 = tf.placeholder(tf.int32, [None, ], name='column_6')
        self.column_7 = tf.placeholder(tf.int32, [None, ], name='column_7')
        self.column_8 = tf.placeholder(tf.int32, [None, ], name='column_8')
        self.column_9 = tf.placeholder(tf.int32, [None, ], name='column_9')
        self.column_10 = tf.placeholder(tf.int32, [None, ], name='column_10')
        # 标签y
        self.y = tf.placeholder(tf.float32, [None, ], name='label')
        # embedding的lookup table
        column_1_emb_w = tf.get_variable("column_1_emb_w", [cnt_dict['column_1'], 8])
        column_2_emb_w = tf.get_variable("column_2_emb_w", [cnt_dict['column_2'], 16])
        column_3_emb_w = tf.get_variable("column_3_emb_w", [cnt_dict['column_3'], 8])
        column_4_emb_w = tf.get_variable("column_4_emb_w", [cnt_dict['column_4'], 4])
        column_5_emb_w = tf.get_variable("column_5_emb_w", [cnt_dict['column_5'], 4])
        column_6_emb_w = tf.get_variable("column_6_emb_w", [cnt_dict['column_6'], 8])
        column_7_emb_w = tf.get_variable("column_7_emb_w", [cnt_dict['column_7'], 4])
        column_8_emb_w = tf.get_variable("column_8_emb_w", [cnt_dict['column_8'], 4])
        column_9_emb_w = tf.get_variable("column_9_emb_w", [cnt_dict['column_9'], 8])
        column_10_emb_w = tf.get_variable("column_10_emb_w", [cnt_dict['column_10'], 8])
        # 每个user自己的偏置
        # column_2_b = tf.get_variable("column_2_b_", [cnt_dict['column_2']], initializer=tf.constant_initializer(0.0))

        column_1_emb = tf.nn.embedding_lookup(column_1_emb_w, self.column_1)
        column_2_emb = tf.nn.embedding_lookup(column_2_emb_w, self.column_2)
        column_3_emb = tf.nn.embedding_lookup(column_3_emb_w, self.column_3)
        column_4_emb = tf.nn.embedding_lookup(column_4_emb_w, self.column_4)
        column_5_emb = tf.nn.embedding_lookup(column_5_emb_w, self.column_5)
        column_6_emb = tf.nn.embedding_lookup(column_6_emb_w, self.column_6)
        column_7_emb = tf.nn.embedding_lookup(column_7_emb_w, self.column_7)
        column_8_emb = tf.nn.embedding_lookup(column_8_emb_w, self.column_8)
        column_9_emb = tf.nn.embedding_lookup(column_9_emb_w, self.column_9)
        column_10_emb = tf.nn.embedding_lookup(column_10_emb_w, self.column_10)

        # emb_features = [column_1_emb, column_2_emb, column_3_emb, column_4_emb, column_5_emb,
        #                 column_6_emb, column_7_emb, column_8_emb, column_9_emb, column_10_emb]

        emb_features = [column_1_emb, column_2_emb, column_3_emb, column_4_emb, column_5_emb,
                        column_6_emb, column_7_emb, column_8_emb, column_9_emb, column_10_emb]

        emb = tf.concat(values=emb_features, axis=1)

        layer_1 = tf.layers.dense(emb, 64, activation=tf.nn.relu, name='f1')
        layer_2 = tf.layers.dense(layer_1, 32, activation=tf.nn.relu, name='f2')
        layer_3 = tf.layers.dense(layer_2, 16, activation=tf.nn.relu, name='f3')
        layer_4 = tf.layers.dense(layer_3, 1, activation=None, name='f4')
        layer_4 = tf.reshape(layer_4, [-1])

        # emb_b = tf.gather(column_2_b, self.column_2)

        self.output = layer_4

        # Step variable
        self.global_step = tf.Variable(0, trainable=False, name='global_step')
        self.global_epoch_step = tf.Variable(0, trainable=False, name='global_epoch_step')
        self.global_epoch_step_op = tf.assign(self.global_epoch_step, self.global_epoch_step + 1)

        #         self.loss = tf.sqrt(tf.reduce_mean(tf.square(tf.subtract(self.y, self.output))))
        self.loss = tf.reduce_mean(tf.square(tf.subtract(self.y, self.output)))

        trainable_params = tf.trainable_variables()
        self.train_op = tf.train.GradientDescentOptimizer(learning_rate=0.1).minimize(self.loss)

        self.spear = self.get_spearman_rankcor(self.y, self.output)

    def train(self, sess, uij):
        loss, _, spear = sess.run([self.loss, self.train_op, self.spear], feed_dict=self.generate_feeddict(uij))
        return loss, spear

    def evaluate(self, sess, uij):
        loss, output, spear = sess.run([self.loss, self.output, self.spear], feed_dict=self.generate_feeddict(uij))
        return loss, output, spear

    def predict(self, sess, uij):
        output = sess.run([self.output], feed_dict=self.generate_feeddict(uij))
        return output

    def generate_feeddict(self, uij):
        feed_dict = {self.column_1: uij['column_1'], self.column_2: uij['column_2'], self.column_3: uij['column_3'],
                     self.column_4: uij['column_4'], self.column_5: uij['column_5'], self.column_6: uij['column_6'],
                     self.column_7: uij['column_7'], self.column_8: uij['column_8'], self.column_9: uij['column_9'],
                     self.column_10: uij['column_10'], self.y: uij['score']}
        return feed_dict

    def get_spearman_rankcor(self, y_true, y_pred):
        return (tf.py_function(spearmanr, [tf.cast(y_pred, tf.float32),
                                           tf.cast(y_true, tf.float32)], Tout=tf.float32))

class DataInput:
    def __init__(self, data, batch_size, column_name_list):

        self.batch_size = batch_size
        self.column_name_list = column_name_list
        self.data = data
        self.epoch_size = len(self.data) // self.batch_size
        if self.epoch_size * self.batch_size < len(self.data):
            self.epoch_size += 1
        self.i = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.i == self.epoch_size:
            raise StopIteration

        batch = self.data.iloc[self.i * self.batch_size: min((self.i + 1) * self.batch_size, len(self.data))]
        self.i += 1

        uij = {}
        for feature in self.column_name_list:
            uij[feature] = list(batch[feature].values)
        uij['score'] = list(batch['score'].values)

        return self.i, uij


class DataEvalInput:
    def __init__(self, data, column_name_list):
        self.data = data
        self.column_name_list = column_name_list

    def generate_eval_data(self):
        uij = {}
        for feature in self.column_name_list:
            uij[feature] = list(self.data[feature].values)
        uij['score'] = list(self.data['score'].values)

        return uij