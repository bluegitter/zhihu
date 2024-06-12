import matplotlib.pyplot as plt
import pandas as pd

# 1) 使用pandas库分别读取两个文件到数据框df1和df2。
df1 = pd.read_csv('知乎数据_201701.csv')
df2 = pd.read_csv('六普常住人口数.csv')

# 2) 在df1中帅选出所在行业为“银行”的记录，保存在数据框df1中。
df1 = df1[df1['所在行业'] == '银行']

# 3）将 _id列设置为df1的行索引。
df1.set_index('_id', inplace=True)

# 4）在df1中将教育经历为缺失值的记录删除。
df1 = df1.dropna(subset=['教育经历'])

# 5) 计算df1中教育经历相同的”关注“数量的和，将结果保持在df3。
df3 = df1.groupby('教育经历')['关注'].sum().reset_index()

# 6) 将df2中按“常住人口”的值升序排序，要求改 数据框df2。
df2 = df2.sort_values(by='常住人口', ascending=True)

# 7) 将df3中关注数量之和最多的5所学校以关注数量从高到底以折线图的形式输出。
top5_schools = df3.nlargest(5, '关注')

# 设置 Matplotlib 字体为支持中文的字体
plt.rcParams['font.sans-serif'] = ['Songti SC']  # 设置默认字体为黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号 '-' 显示为方块的问题

plt.figure(figsize=(10, 6))
plt.plot(top5_schools['教育经历'], top5_schools['关注'], marker='o')
plt.title('关注数量之Top5高校')
plt.xlabel('高校')
plt.ylabel('关注数量之和')

# 显示图表
plt.tight_layout()
plt.show()
