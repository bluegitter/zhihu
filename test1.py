import matplotlib.pyplot as plt
import pandas as pd

# 1) 使用pandas库分别读取两个文件到数据框df1和df2。
df1 = pd.read_csv('知乎数据_201701.csv')
df2 = pd.read_csv('六普常住人口数.csv')

# 2) 找出第1职业为“金融“的所有记录，并将其赋值给df1。
df1 = df1[df1['职业1'] == '金融']

# 3）将df1中“关注者“列中为空的值用0填充。
df1['关注者'] = df1['关注者'].fillna(0)

# 4）删除df1中的存在缺失值的行。
df1 = df1.dropna()

# 5) 将df1中按“所在行业”分组，计算每组关注者的数量之和，并将结果保存为df3。
df3 = df1.groupby('所在行业')['关注者'].sum().reset_index()

# 6) 将df2中“地区"列中每个值去掉最后一个字符，如第一行的地区为”安徽省"，变更为“安徽"。
df2['地区'] = df2['地区'].str[:-1]

# 7) 使用df3中数据，绘制所在行业中关注者数量的桂状图，柱状图颜色为绿色(green)x轴标签为”所在行业"，轴标签为“关注者数量”，标题为“不同行业关注者数量柱状图 ”.

# 设置 Matplotlib 字体为支持中文的字体
plt.rcParams['font.sans-serif'] = ['Songti SC']  # 设置默认字体为黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号 '-' 显示为方块的问题

plt.figure(figsize=(10, 6))
plt.bar(df3['所在行业'], df3['关注者'], color='green')
plt.xlabel('所在行业')
plt.ylabel('关注者数量')
plt.title('不同行业关注者数量柱状图')
plt.xticks(rotation=45)
# plt.tight_layout()
plt.show()
