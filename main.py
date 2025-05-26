import pandas as pd
from ucimlrepo import fetch_ucirepo
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# 对所有特征列做编码
def encode_features(df):
    for col in df.columns:
        if df[col].dtype == 'object':
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col])
    return df

mushroom = fetch_ucirepo(id=73)
# ? 定义朴素贝叶斯分类器
class bayes_model():
    def __init__(self):
        pass

    # ? 加载数据
    def load_data(self):
        # fetch dataset
        # data (as pandas dataframes)
        X = mushroom.data.features.copy()
        y = mushroom.data.targets.copy()
        X = encode_features(X)
        y = y.values.ravel()  # 保证y为一维
        train_x, test_x, train_y, test_y = train_test_split(X, y, test_size=0.3, random_state=123)
        return train_x, test_x, train_y, test_y

    # ? 训练高斯朴素贝叶斯模型
    def train_model(self, train_x, train_y):
        clf = GaussianNB()
        clf.fit(train_x, train_y)
        return clf

    # ? 处理预测的数据
    def proba_data(self, clf, test_x, test_y):
        y_predict = clf.predict(test_x)  # 返回待预测样本的预测结果(所属类别)
        y_proba = clf.predict_proba(test_x)  # 返回预测样本属于各标签的概率
        accuracy = accuracy_score(test_y, y_predict) * 100  # 计算predict预测的准确率

        return y_predict, y_proba, accuracy

    # ? 训练数据
    def exc_p(self):
        train_x, test_x, train_y, test_y = self.load_data()  # 加载数据
        clf = self.train_model(train_x, train_y)  # 训练 高斯朴素贝叶斯 模型clf
        y_predict, y_proba, accuracy = self.proba_data(clf, test_x, test_y)  # 利用训练好的模型clf对测试集test_x进行结果预测分析

        return train_x, test_x, train_y, test_y, y_predict, y_proba, accuracy


if __name__ == '__main__':
    train_x, test_x, train_y, test_y, y_predict, y_proba, accuracy = bayes_model().exc_p()
    featurenames = list(mushroom.data.features.columns)
    print()
    print("=============================================朴素贝叶斯分类器==============================================")
    # 训练集与其标签 df1
    df1_1 = pd.DataFrame(train_x).reset_index(drop=True)
    df1_2 = pd.DataFrame(train_y)
    df1 = pd.merge(df1_1, df1_2, left_index=True, right_index=True)
    df1.columns = featurenames + ['train classify']
    print("=============================================训练集==============================================")
    print(f'The train dataSet is:\n{df1}\n')
    # 测试集与其标签 df2
    df2_1 = pd.DataFrame(test_x).reset_index(drop=True)
    df2_2 = pd.DataFrame(test_y)
    df2 = pd.merge(df2_1, df2_2, left_index=True, right_index=True)
    df2.columns = featurenames + ['test classify']
    print("=============================================测试集==============================================")
    print(f'The test dataSet is:\n{df2}\n')
    # 预测结果
    # 预测结果
    tot1 = pd.DataFrame([test_y, y_predict]).T
    tot2 = pd.DataFrame(y_proba).apply(lambda col: col.map(lambda x: '%.2f' % x))
    tot = pd.merge(tot1, tot2, left_index=True, right_index=True)
    proba_cols = [f'predict_{i}' for i in range(tot2.shape[1])]
    tot.columns = ['y_true', 'y_predict'] + proba_cols
    print("============================================预测结果==============================================")
    print('The result of predict is: \n', tot)
    print("=============================================准确率==============================================")
    print(f'The accuracy of Testset is: {accuracy:.2f}%')
