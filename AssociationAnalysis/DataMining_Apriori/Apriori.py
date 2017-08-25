# -*- coding:utf-8 -*-

# @Author zpf
import itertools


class FrequentItem:
    # 频繁项集的集合ID
    idArray = []
    # 频繁项集的支持度计数
    count = 0
    # 频繁项集的长度，1项集或是2项集，亦或是3项集
    length = 0

    def __init__(self, id_array, item_count):
        self.idArray = id_array
        self.count = item_count
        self.length = len(id_array)

    def get_id_array(self):
        return self.idArray

    def set_id_array(self, id_array):
        self.idArray = id_array

    def get_count(self):
        return self.count

    def set_count(self, item_count):
        self.count = item_count

    def get_length(self):
        return self.length

    def set_length(self, array_length):
        self.length = array_length


class AprioriTool:
    # 最小支持度计数
    min_support_count = 0
    # 文件地址
    file_path = ''
    # 每个事务中的商品ID
    total_goods_ids = []
    # 过程中计算出来的所有频繁项集列表
    result_item = []
    # 过程中计算出来频繁项集的ID集合
    result_item_id = []
    # 剪枝后的新频繁项集
    new_item = []

    def __init__(self, path, support_count):
        self.path = path
        self.min_support_count = support_count
        self.read_data_file(file_path)

    # 从文件中读取数据
    def read_data_file(self, path):
        data_array = []

        file = open(path)
        for line in file:
            if line != '':
                temp_array = line.split()
                data_array.append(temp_array)
        file.close()

        for array in data_array:
            temp = array[1:].copy()
            # 将事务ID加入列表
            self.total_goods_ids.append(temp)

    # 项集连接步
    def compute_link(self):
        # 当前已经进行连接运算到几项集,开始时就是1项集
        current_num = 1
        # 初始化列表
        init_list = []
        temp_item = {}
        # 商品id的种类
        id_type = []
        for array in self.total_goods_ids:
            for goods_id in array:
                if goods_id in id_type:
                    temp_value = temp_item[goods_id]
                    temp_item[goods_id] = temp_value + 1
                else:
                    id_type.append(goods_id)
                    temp_item[goods_id] = 1
        # 得到初始频繁项集，并将初始频繁项集存入result_item， result_item_id中
        id_type.sort()
        for goods_id in id_type:
            temp_id_array = []
            temp_id_array.append(goods_id)
            temp_node = FrequentItem(temp_id_array, temp_item[goods_id])
            # 根据最小支持度，判断初始项集是否频繁
            if temp_node.get_count() >= self.min_support_count:
                init_list.append(temp_node)
                self.result_item.append(temp_node)
                self.result_item_id.append(temp_id_array)

        # 连接计算的终止数，k项集必须算到k-1子项集为止
        end_num = len(init_list) - 1
        while current_num < end_num:
            result_container = []
            i = 0
            while i < len(init_list) - 1:
                array1 = init_list[i].get_id_array()
                j = i + 1
                while j < len(init_list):
                    array2 = init_list[j].get_id_array()

                    temp_ids = []
                    # 连接两个array，比较对应位置值是否相等
                    k = 0
                    while k < len(array1):
                        if array1[k] == array2[k]:
                            temp_ids.append(array1[k])
                        else:
                            temp_ids.append(array1[k])
                            temp_ids.append(array2[k])
                        k += 1

                    is_contain = False
                    if len(temp_ids) == len(array1) + 1:
                        is_contain = self.is_id_array_contains(
                            result_container, temp_ids)
                        if not is_contain:
                            result_container.append(temp_ids)
                    j += 1
                i += 1
            init_list = self.pruning(result_container)

            # 将每步连接得到的频繁项集存入result_item, result_item_id
            for item in init_list:
                self.result_item.append(item)
                self.result_item_id.append(item.get_id_array())

            current_num += 1

        # 输出频繁项集
        l = 1
        while l <= current_num:
            print("频繁" + str(l) + "项集：{")
            for frequent_set in self.result_item:
                if frequent_set.get_length() == l:
                    print(str(frequent_set.get_id_array()) + ", ")
            print("}")
            l += 1

    # 判断列表结果中是否已经包含此数组
    @staticmethod
    def is_id_array_contains(container, array):
        is_contain = True
        if len(container) == 0:
            is_contain = False
            return is_contain

        for element in container:
            if len(element) != len(array):
                continue

            is_contain = True
            i = 0
            while i < len(element):
                if element[i] not in array:
                    is_contain = False
                    break
                i += 1
            # 如果判断出包含，直接退出
            if is_contain:
                break

        return is_contain

    # 对频繁项集做剪枝步骤，必须保证新的频繁项集的子项集也必须是频繁项集
    def pruning(self, middle_result_ids):
        # 剪枝后的新频繁项集
        self.new_item = []
        # 需要删除的不符合要求的项集id
        delete_id_array = []
        # 判断子项集是否是频繁项集
        is_contain = True
        for array in middle_result_ids:
            i_index = 0
            while i_index < len(array):
                is_contain = True
                temp = []
                j = 0
                while j < len(array):
                    if j != i_index:
                        temp.append(array[j])
                    j += 1

                if not self.is_id_array_contains(self.result_item_id, temp):
                    is_contain = False
                    break
                i_index += 1

                if not is_contain:
                    delete_id_array.append(array)

        # 移除子项集不是频繁项集的id组合
        for array in delete_id_array:
            del middle_result_ids[middle_result_ids.index(array)]

        # 移除不满足最小支持度的id组合
        for array1 in middle_result_ids:
            temp_num = 0
            for array2 in self.total_goods_ids:
                if self.is_str_array_contain(array2, array1):
                    temp_num += 1
            # 将支持度 >= 最小支持度的频繁项集加入result_item, result_item_id
            if temp_num >= self.min_support_count:
                temp_item = FrequentItem(array1, temp_num)
                self.new_item.append(temp_item)

        return self.new_item

    # 数组array2是否包含于array1中，不需要完全一样
    @staticmethod
    def is_str_array_contain(array1, array2):
        is_contain = True
        for element in array2:
            if element not in array1:
                is_contain = False
        return is_contain

    # 根据产生的频繁项集输出关联规则
    # @param min_conf
    #        最小置信度阈值
    def print_attach_rule(self, min_conf):
        self.compute_link()
        # 计算得到的频繁项集id_array的最大长度
        max_length = len(self.result_item_id[-1])
        for item in self.result_item:
            item_array = item.get_id_array()
            if len(item_array) == max_length:
                l = max_length - 1
                # 最长频繁项集的子集
                sub_set = []
                while l > 0:
                    for sub_item in itertools.combinations(item_array, l):
                        sub_set.append(list(sub_item))
                    l -= 1
                # A->B, conf(A->B) = P(B|A) = P(AB)/P(A)
                for sub_a in sub_set:
                    pos_ab = self.result_item_id.index(item_array)
                    pos_a = self.result_item_id.index(sub_a)
                    sub_ab_item = self.result_item[pos_ab]
                    sub_a_item = self.result_item[pos_a]
                    conf_ab = sub_ab_item.get_count() / sub_a_item.get_count()
                    sub_b = list(set(item_array).difference(set(sub_a)))
                    if conf_ab > min_conf:
                        print("Event(A)->Event(B) = "
                              + str(sub_a) + "->" + str(sub_b)
                              + "\t" + "是强规则")
                    else:
                        # print("Event(A)->Event(B) = "
                        #       + str(sub_a) + "->" + str(sub_b)
                        #       + "\t" + "不是强规则")
                        pass


if __name__ == '__main__':
    file_path = './input.txt'
    tool = AprioriTool(file_path, 2)
    tool.print_attach_rule(0.7)
