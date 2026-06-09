"""
下载试题答案解析图片
使用前请确保：
1. 你有权限访问这些资源
2. 遵守网站服务条款
3. 仅用于个人学习目的
"""
import requests
import os
import time
from PIL import Image
from io import BytesIO
import json

def load_progress():
    """加载下载进度"""
    if os.path.exists('answers_progress.json'):
        with open('answers_progress.json', 'r') as f:
            return json.load(f)
    return {'completed': []}

def save_progress(completed):
    """保存下载进度"""
    with open('answers_progress.json', 'w') as f:
        json.dump({'completed': completed}, f)

def download_answer(session, answer_id, save_dir):
    """下载单个答案图片"""
    url = f"https://zhentiqiang.com/static/photos/analysis_images/{answer_id}.png"
    save_path = os.path.join(save_dir, f"{answer_id}.png")
    
    # 如果已存在，跳过
    if os.path.exists(save_path):
        return 'exists'
    
    try:
        response = session.get(url, timeout=30)
        if response.status_code == 404:
            return 'not_found'
        response.raise_for_status()
        
        # 验证是否为有效图片
        img = Image.open(BytesIO(response.content))
        
        # 保存图片
        os.makedirs(save_dir, exist_ok=True)
        with open(save_path, 'wb') as f:
            f.write(response.content)
        
        return 'success'
    except requests.exceptions.Timeout:
        return 'timeout'
    except requests.exceptions.RequestException as e:
        return f'error: {str(e)}'
    except Exception as e:
        return f'error: {str(e)}'

def download_single_answer(answer_id, save_dir="answer"):
    """下载单个指定的答案"""
    print(f"\n下载答案解析图片: {answer_id}")
    print("="*50)
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': 'https://zhentiqiang.com/'
    })
    
    result = download_answer(session, answer_id, save_dir)
    
    if result == 'success':
        print(f"✓ 下载成功: {answer_id}.png")
        print(f"保存位置: {os.path.abspath(os.path.join(save_dir, f'{answer_id}.png'))}")
        return True
    elif result == 'exists':
        print(f"○ 文件已存在: {answer_id}.png")
        print(f"位置: {os.path.abspath(os.path.join(save_dir, f'{answer_id}.png'))}")
        return True
    elif result == 'not_found':
        print(f"✗ 未找到答案: {answer_id}")
        return False
    else:
        print(f"✗ 下载失败: {result}")
        return False

def download_batch_answers(start_id, end_id, save_dir="answer"):
    """批量下载答案"""
    print(f"\n批量下载答案解析图片: {start_id} - {end_id}")
    print("="*70)
    
    # 加载进度
    progress = load_progress()
    completed = set(progress['completed'])
    
    if completed:
        print(f"已完成: {len(completed)} 个答案")
        print("将跳过已下载的答案\n")
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': 'https://zhentiqiang.com/'
    })
    
    success_count = 0
    exists_count = 0
    not_found_count = 0
    error_count = 0
    timeout_count = 0
    
    # 创建保存目录
    os.makedirs(save_dir, exist_ok=True)
    
    for answer_id in range(start_id, end_id + 1):
        # 跳过已完成的
        if answer_id in completed:
            exists_count += 1
            if answer_id % 50 == 0:  # 每50个显示一次
                print(f"  {answer_id:4d}: ○ 已完成", flush=True)
            continue
        
        print(f"  {answer_id:4d}: ", end='', flush=True)
        result = download_answer(session, answer_id, save_dir)
        
        if result == 'success':
            print("✓ 成功")
            success_count += 1
            completed.add(answer_id)
            # 每10个成功下载保存一次进度
            if success_count % 10 == 0:
                save_progress(list(completed))
        elif result == 'exists':
            print("○ 已存在")
            exists_count += 1
            completed.add(answer_id)
        elif result == 'not_found':
            print("✗ 不存在")
            not_found_count += 1
        elif result == 'timeout':
            print("⏱ 超时")
            timeout_count += 1
        else:
            print(f"✗ 失败")
            error_count += 1
        
        # 延迟，避免请求过快
        time.sleep(0.3)
        
        # 每100个显示一次进度统计
        if (answer_id - start_id + 1) % 100 == 0:
            current = answer_id - start_id + 1
            total = end_id - start_id + 1
            print(f"\n  --- 进度: {current}/{total} ({current*100//total}%) | 成功:{success_count} 已存在:{exists_count} 不存在:{not_found_count} ---\n")
    
    # 最后保存一次进度
    save_progress(list(completed))
    
    print("\n" + "="*70)
    print("下载完成!")
    print("="*70)
    print(f"✓ 成功下载: {success_count}")
    print(f"○ 已存在: {exists_count}")
    print(f"✗ 不存在: {not_found_count}")
    print(f"⏱ 超时: {timeout_count}")
    print(f"✗ 其他失败: {error_count}")
    print(f"总计: {success_count + exists_count}/{end_id - start_id + 1}")
    print(f"保存位置: {os.path.abspath(save_dir)}")
    
    return success_count, exists_count, not_found_count, error_count

def main():
    print("\n" + "="*70)
    print("试题答案解析图片下载工具")
    print("="*70)
    print("\n默认配置:")
    print("  起始ID: 640")
    print("  结束ID: 1700")
    print("  保存目录: answer")
    print("\n请选择:")
    print("1. 使用默认配置开始下载 (640-1700)")
    print("2. 自定义下载范围")
    print("3. 下载单个答案")
    
    choice = input("\n请选择 (1/2/3，直接回车使用默认): ").strip()
    
    if choice == '' or choice == '1':
        # 默认配置：640-1700，保存到answer文件夹
        print("\n开始下载 640-1700 到 answer 文件夹...")
        download_batch_answers(640, 1700, "answer")
    
    elif choice == '2':
        range_input = input("请输入范围 (例如: 1-1000): ").strip()
        save_dir = input("保存目录 (直接回车使用 'answer'): ").strip() or "answer"
        try:
            start_id, end_id = map(int, range_input.split('-'))
            if start_id > end_id:
                print("✗ 起始ID不能大于结束ID")
                return
            download_batch_answers(start_id, end_id, save_dir)
        except ValueError:
            print("✗ 无效的范围格式")
    
    elif choice == '3':
        answer_id = input("请输入答案ID: ").strip()
        save_dir = input("保存目录 (直接回车使用 'answer'): ").strip() or "answer"
        try:
            answer_id = int(answer_id)
            download_single_answer(answer_id, save_dir)
        except ValueError:
            print("✗ 无效的答案ID")
    
    else:
        print("✗ 无效的选择")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n已中断，进度已保存")
    except Exception as e:
        print(f"\n错误: {e}")
        import traceback
        traceback.print_exc()
