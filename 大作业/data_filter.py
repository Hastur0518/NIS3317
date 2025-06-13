import pandas as pd
def read_data(file_path,file_name):
    """
    读取数据文件
    :param file_path: 数据文件路径
    :return: DataFrame
    """
    df = pd.read_csv(file_path)
    #为内部所有数据增加一列district
    df['district'] = file_name
    return df

def filter_data(df):
    """
    过滤数据，保留特定列和满足条件的行
    :param df: 原始DataFrame
    :return: 过滤后的DataFrame
    """
    #修改build_in列的值，只保留年前的数据
    df['build_in'] = df['build_in'].apply(lambda x: x.split('年')[0] if isinstance(x, str) else x)
    #house_info拆为室，厅，卫
    df['室'] = df['house_info'].apply(lambda x: x.split('室')[0] if isinstance(x, str) else x)
    df['厅'] = df['house_info'].apply(lambda x: x.split('厅')[0].split('室')[-1] if isinstance(x, str) else x)
    df['卫'] = df['house_info'].apply(lambda x: x.split('卫')[0].split('厅')[-1] if isinstance(x, str) else x)
    df['高低']= df['house_type'].apply(lambda x: x.split('层')[0] if isinstance(x, str) else x)
    df['总楼层'] = df['house_type'].apply(lambda x: x.split('共')[-1].split('层')[0] if isinstance(x, str) else x)
    df['price'] = df['price'].apply(lambda x: float(x.replace('万', '')) if isinstance(x, str) else x)
    #判断近地铁三个字是否在specials列中
    df['近地铁'] = df['specials'].apply(lambda x: '近地铁' in x if isinstance(x, str) else False)
    #把已经处理过的列drop
    df = df.drop(columns=['house_info', 'house_type', 'specials'])
    #保留特定列
    df = df[['title', 'price', 'avg_price', 'address', 'area', 'towards', 'build_in', 'district', '室', '厅', '卫', '高低', '总楼层', '近地铁']]
    #去除重复数据
    df = df.drop_duplicates(subset=['title', 'district'], keep='first')
    #去除空值
    df = df.dropna(subset=['title', 'price', 'avg_price', 'address', 'area', 'towards', 'build_in', 'district'])
    return df

if __name__ == "__main__":
    # 示例文件路径和名称
    districts = ["minhang", "songjiang", "baoshan", "jiading", "xuhui","qingpu","jingan","putuo","pudong"]
    file_path = "data/"
    total_df = pd.DataFrame()
    for district in districts:
        file_name = f"NIS3317.{district}.csv"
        df = read_data(file_path + file_name, district)
        filtered_df = filter_data(df)
        total_df = pd.concat([total_df, filtered_df], ignore_index=True)
    # 保存处理后的数据
    total_df.to_csv(file_path + "filtered_data.csv", index=False, encoding='utf-8-sig')

