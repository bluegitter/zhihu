import pandas as pd
import matplotlib.pyplot as plt

import os
os.chdir(r'F:\城市数据团\数据解析核心')

import warnings
warnings.filterwarnings('ignore')

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

file1 = '知乎数据_201701.csv'
file2 = '六普常住人口数.csv'

# 筛选出所有省份
df2 = pd.read_csv(file2, engine='python')
urbon_population = df2.groupby(['省']).sum().drop(['总计'])
index = urbon_population.index.tolist()
# print(index)

# 对省份名称进行统一规范处理
urbon_population_index = []
for index in index:
    if index == '内蒙古自治区' or index == '黑龙江省':
        index = index[:3]
    else:
        index = index[:2]
    # print(index)
    urbon_population_index.append(index)
# print(urbon_population_index)
urbon_population.index = urbon_population_index
# print(urbon_population.index.tolist())


df1 = pd.read_csv(file1, engine='python')


def clear_nan(df):
    '''
    数据清洗,去除空值
    '''
    df = df.fillna('缺失数据', inplace=False)
    return df


df1 = clear_nan(df1)

# 针对省份计算出对应数量以及密度
data1 = df1.groupby(['居住地']).count()[['_id']]
data1 = data1.loc[urbon_population_index]
data1.rename(columns={'_id':'quantity'}, inplace=True)
data1['density'] = data1['quantity'] / urbon_population['常住人口']
# print(data1)


def std(df):
    '''
    对数量和密度进行标准化处理
    '''
    df[df.columns.tolist()] = (df[df.columns.tolist()] - df[df.columns.tolist()].min()) / (df[df.columns.tolist()].max() - df[df.columns.tolist()].min())*100
    # print(df)
    return df


data1 = std(data1)

# 按照数量以及密度分别进行排序
quantity = data1.sort_values(by='quantity', ascending=False, inplace=False)
density = data1.sort_values(by='density', ascending=False, inplace=False)
# print(quantity)
# print(density)
# 选取前20名
quantity = quantity.iloc[:20]
density = density.iloc[:20]
# print(quantity)
# print(density)

fig = plt.figure(figsize=(15, 8))
ax1 = fig.add_subplot(2, 1, 1)
ax2 = fig.add_subplot(2, 1, 2)

ax1.bar(quantity.index, quantity['quantity'], color='green')
ax1.set_title('知友数量Top20')
ax1.grid(axis='y', ls='--')
for a, b in zip(quantity.index, quantity['quantity']):
    ax1.text(a, 5, '%.1f'%b, ha='center')
ax2.bar(density.index, density['density'], color='blue')
ax2.set_title('知友密度Top20')
ax2.grid(axis='y', ls='--')
for a, b in zip(density.index, density['density']):
    ax2.text(a, 5, '%.1f'%b, ha='center')
plt.savefig('address.png', dpi=400)
# plt.show()

# 提取相关字段
data2 = df1[['_id', '教育经历', '关注者', '关注']]
# print(data2.head())

# 分组统计对应总数量
data2 = data2.groupby(['教育经历']).sum()[['关注者', '关注']]

# 对别名进行汇总
data2.loc['清华大学'] = data2.loc['清华大学'] + data2.loc['五道口男子职业技术学院']
data2.loc['重庆文理学院'] = data2.loc['重庆文理学院'] + data2.loc['重庆第一工程尸培养基地']

# 对比较长的index进行重命名
data2.rename(index={'四川烹饪高专':'四川旅游学院', '哈尔滨工业大学（HIT）':'哈尔滨工业大学', '圣母大学 (University of Notre Dame)':'圣母大学', '东京大学OIST':'东京大学'}, inplace=True)

# 按照粉丝数进行排名
school = data2.sort_values(by='关注者', ascending=False, inplace=False)

# 删除无意义的行
school.drop(school.index[[0, 4, 8, 9, 10, 11, 13, 18, 21, 22, 26, 27, 28, 29, 35, 37]], inplace=True)

# 提取前20名
school = school.iloc[:20]
print(school)

# 计算关注人数和粉丝数的平均值
fans_mean = school[['关注者']].mean().values
subscribers_mean = school[['关注']].mean().values
# print(fans_mean)
# print(subscribers_mean)

fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(school[['关注']], school[['关注者']], s=school[['关注者']]/1000, marker='.',label='学校')
# 辅助线
ax.axvline(subscribers_mean, color='red', ls='--', label='平均关注人数:{}人'.format(int(subscribers_mean[0])))
ax.axhline(fans_mean, color='blue', ls='--', label='平均粉丝人数:{}人'.format(int(fans_mean[0])))
# 文本
for a, b, c in zip(school['关注'], school['关注者'], school.index):
    ax.text(a, b, c, fontsize=8)
ax.legend()
ax.grid(ls='--')
plt.savefig('school.png', dpi=400)
# plt.show()

print('finished!')