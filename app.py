from flask import Flask, render_template, url_for, request
import tensorflow as tf
import gensim
from keras_preprocessing.sequence import pad_sequences
import re

# 加载模型和word2vec预训练模型
model = tf.keras.models.load_model('./model/')
w2v_model = gensim.models.Word2Vec.load('./model/')


def convert_data_to_index(string_data, wv):
    index_data = []
    for word in string_data:
        if word in wv:
            index_data.append(wv.vocab[word].index)
    return index_data


def convert_sequences_to_index(list_of_sequences, wv):
    ll = []  #
    for i in range(len(list_of_sequences)):
        ll.append(convert_data_to_index(list_of_sequences[i], wv))
    return ll


def seq2ngram(seqs, k, s, wv):
    f = open(seqs)
    lines = f.readlines()
    f.close()
    list22 = []
    print('need to n-gram %d lines' % len(lines))

    for num, line in enumerate(lines):
        if num < 200000:
            line = line[:-1]  # remove '\n' and lower ACGT
            l = len(line)  # length of line
            list2 = []  # 所有序列的k-mer构成的列表
            for i in range(0, l, s):
                if i + k >= l + 1:
                    break
                list2.append(line[i:i + k])  #

            list22.append(convert_data_to_index(list2, wv))  # 把索引和list2中的k-mer对应起来加入一个新的列表list22

    return list22


# 实例flask
app = Flask(__name__)


@app.route('/')
def index():
    return render_template("home.html")


@app.route('/home')
def home():
    return render_template("home.html")


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/predict')
def predict():
    return render_template('predict.html')


@app.route('/result', methods=['POST'])
def predict_result():
    patten = re.compile(r"[a-zBD-FH-SU-Z0-9!@#$%^&*()+_={}\[\]|\\:\"<>?/’~·.,，。、；：‘”【】？《》\s*\u4e00-\u9fa5]")
    if request.method == 'POST':
        # 从表单获取信息
        message = request.form['message']

        if message == "":
            error_msg = "数据为空,请重新输入"
            return render_template('error.html', error_msg=error_msg)
        elif len(message) < 20:
            error_msg = "序列长度小于20nt,请重新输入"
            return render_template('error.html', error_msg=error_msg)

        # 统计seq的数量
        seq_num = message.count('>')
        # 划分序列的 name 和seq
        data = message.strip().split('\n')

        seq_dict = {}  # 序列大字典
        seq_data = []  # 纯序列数据

        num = 0  # seq_dict的key

        for i, line in enumerate(data):

            # 判断data是否是fasta格式
            if seq_num > 0:
                # line为seq
                if not line.startswith('>'):
                    seq['seq'] += line.replace('\r', '')  # 把seq连接起来
                    # 如果line还没碰到> 并且 下标i没到data的长度-1
                    if patten.findall(seq['seq']) != []:
                        error_msg = "数据含有非法字符,请重新输入"
                        return render_template('error.html', error_msg=error_msg)
                    else:
                        if i != len(data) - 1:
                            if not data[i + 1].startswith('>'):
                                continue
                            else:
                                seq_dict[num] = seq
                                seq_data.append(seq['seq'])
                                num += 1
                        else:
                            seq_dict[num] = seq
                            seq_data.append(seq['seq'])
                            num += 1
                # line为name
                else:
                    seq = {}
                    seq['name'] = line.replace('\r', '')
                    seq['seq'] = ''
                    seq['num'] = num + 1
                    continue
            else:
                # 不是fasta格式
                seq = {}
                seq['name'] = 'None'
                seq['seq'] = line.replace('\r', '')
                if patten.findall(seq['seq']) == []:
                    seq['num'] = i + 1
                    seq_dict[i] = seq
                    seq_data.append(line)
                else:
                    error_msg = "数据含有非法字符,请重新输入"
                    return render_template('error.html', error_msg=error_msg)

        # 转换成索引序列
        index_data = convert_sequences_to_index(seq_data, w2v_model.wv)

        # 控制序列长度
        for item in index_data:
            if len(item) > 600:
                item = item[:600]
        X = pad_sequences(index_data, maxlen=600, padding='post')

        # 预测标签值
        y_pred_list = (model.predict(X) > 0.5).astype('int32')
        # 预测概率值
        y_prob_list = model.predict(X)

        # 二维列表变一维列表
        y_pred = [i for item in y_pred_list for i in item]
        y_prob = [i for item in y_prob_list for i in item]

        for i in range(len(y_pred)):
            seq_dict[i]['y_prob'] = y_prob[i]
            if y_pred[i] == 1:
                seq_dict[i]['y_pred'] = 'paRNA'
            else:
                seq_dict[i]['y_pred'] = '--'

    return render_template('result.html', seq_dict=seq_dict)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
