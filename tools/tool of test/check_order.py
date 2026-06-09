import os

# 主目录
base_dir = r'c:\Users\25708\Desktop\真题'
target_dir = os.path.join(base_dir, 'sorted_images')

# 检查同一年份的图片顺序
def check_order():
    math_types = ['数学一', '数学二', '数学三']
    years = list(range(2025, 2008, -1))  # 2025-2009
    
    for math_type in math_types:
        math_dir = os.path.join(target_dir, math_type)
        print(f'\n检查 {math_type} 的图片顺序:')
        
        for year in years:
            year_dir = os.path.join(math_dir, f'{year}年')
            if os.path.exists(year_dir):
                # 获取目录中的所有png文件
                files = [f for f in os.listdir(year_dir) if f.endswith('.png')]
                # 按照文件名排序
                files.sort()
                
                print(f'  {year}年:')
                for i, file in enumerate(files):
                    print(f'    {i+1}. {file}')
            else:
                print(f'  {year}年: 目录不存在')

if __name__ == '__main__':
    print('开始检查图片顺序...')
    check_order()
    print('图片顺序检查完成！')
