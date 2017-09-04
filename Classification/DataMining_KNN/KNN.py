# -*- coding:utf-8 -*-

# @Author zpf 


class KNN:
    # 训练测试txt数据的路径
    train_data_path = ""
    test_data_path = ""
    # 训练测试数据
    train_data_list = []
    test_data_list = []

    def __init__(self, train_path, test_path):
        self.train_data_path = train_path
        self.test_data_path = test_path
        self.read_data(self.train_data_path, self.test_data_path)

    # 读取文件数据
    def read_data(self, train_path, test_path):
        for line in open(train_path):
            line = line.split()
            self.train_data_list.append(line)
        for line in open(test_path):
            line = line.split()
            self.test_data_list.append(line)

    # 计算样本之间的欧几里得距离
    def Euclidean_distance(self):
        for sample in self.test_data_list:
            for element in self.train_data_list:
                # 欧几里得距离及其list
                distance = 0
                all_distance = []
                i = 0
                while i < len(sample):
                    distance += (sample[i] - element[i+1])**2
                    i += 1
                all_distance.append(distance)


if __name__ == "__main__":
    train_data = "./train.txt"
    test_data = "./test.txt"
    KNN_N = KNN(train_data, test_data)
