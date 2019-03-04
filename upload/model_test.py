# -*- coding:utf-8 -*-
'''
    WSDetector v1.0
    Author: Frank
    Email: fr4nk404@gmail.com
'''

import sys
#import numpy as np
import tflearn
from tflearn.data_utils import to_categorical, pad_sequences

import hashlib
import os

max_sequences_len=100   # ? 最长序列长度，max_seq_len是指一个切好词的句子最多包含多少个词
max_sys_call=0   # 最大的系统序列调用长度，每个函数对应1个

# 字节bytes转化kb\m\g
def format_size(bytes):
    try:
        bytes = float(bytes)
        kb = bytes / 1024
    except:
        print("传入的字节格式不对")
        return "Error"

    if kb >= 1024:
        M = kb / 1024
        if M >= 1024:
            G = M / 1024
            return "%fG" % (G)
        else:
            return "%fM" % (M)
    else:
        return "%fkb" % (kb)

def get_md5(file_path):
  md5 = None
  if os.path.isfile(file_path):
    f = open(file_path,'rb')
    md5_obj = hashlib.md5()
    md5_obj.update(f.read())
    hash_code = md5_obj.hexdigest()
    f.close()
    md5 = str(hash_code).lower()
  return md5

def load_one_flle(filename):
    '''
    逐行读取文件，并记录系统调用序号的最大值，系统调用序号使用整数记录。
    v 是每一个系统调用函数对应的数字，x 是该段序列的整体的列表，比如：[54, 175, 120, 175, 175, 3, ...]
    '''

    global max_sys_call
    x=[]
    with open(filename) as f:
        line=f.readline()
        line=line.strip('\n')
        line=line.split(' ')
        for v in line:
            if len(v) > 0:
                x.append(int(v))
                if int(v) > max_sys_call:
                    max_sys_call=int(v)
    return x

def predict_rnn(testX):
    global max_sequences_len
    global max_sys_call

    # 构造RNN，使用LSTM算法
    # 建模，输入N*100行，每行为100列，刚才padding成了100
    net = tflearn.input_data([None, max_sequences_len])
    # 这里用embedding层，没有外部的word2vec，输入维是最长调用序列+1，嵌入到128的向量空间(输出的维度)
    net = tflearn.embedding(net, input_dim=max_sys_call+1, output_dim=128)
    # 把词向量再输出给LSTM,隐层也是128层，就是词向量的长度
    net = tflearn.lstm(net, 128, dropout=0.8)
    # 全连接层，分成2层输出
    net = tflearn.fully_connected(net, 2, activation='softmax')
    # 设置优化函数，学习率，损失函数
    # 这里对应的categorical_交叉熵损失函数
    net = tflearn.regression(net, optimizer='adam', learning_rate=0.001,
                             loss='categorical_crossentropy')

    # 实例化RNN，默认序列长度为100，不足时使用0补齐。
    # 因为使用到pad_sequences()函数，所以需要将一维list转换为二维list
    testX =[testX]
    testX = pad_sequences(testX, maxlen=max_sequences_len, value=0.)
    model = tflearn.DNN(net, tensorboard_verbose=3, tensorboard_dir="/log/")
	# 加载训练好的模型
    print("test")
    model.load('/home/frank/Documents/Desktop/1/model.tflearn',weights_only=True)
    y_predict_list = model.predict(testX)
    # print y_predict_list
    #np.set_printoptions(suppress=True)
    for i in y_predict_list:
        #print("[%.9f %.9f]"%(i[0],i[1]))
        print(i)
        if i[0] > 0.5:
            #print("This is a normal behavior.")
            print("Normal")
            str="Normal"
        else:
            #print("This is an attack behavior!")
            print("Webshell")
            str="Webshell"
    return str
#if __name__ == '__main__':

    #x_test1 = load_one_flle("/home/frank/Documents/Desktop/1book-master/data/ADFA-LD/Attack_Data_Master/Adduser_10/UAD-Adduser-10-1371.txt")
    #x_test2 = load_one_flle("/home/frank/Documents/Desktop/1book-master/data/ADFA-LD/Attack_Data_Master/Web_Shell_3/UAD-WS3-2311.txt")
    #x_test3 = load_one_flle("/home/frank/Documents/Desktop/1book-master/data/ADFA-LD/Training_Data_Master/UTD-0012.txt")

    #predict_rnn(x_test2)
	# 将命令行输入的第二个参数作为输入的文件的位置
	# 例如：python model_test.py /home/frank/Documents/Desktop/1book-master/data/ADFA-LD/Attack_Data_Master/Web_Shell_3/UAD-WS3-2311.txt
    #file_dir = sys.argv[1]
    #print(file_dir)
    #predict_rnn(load_one_flle(file_dir))
