"""
下载 group_9 和 group_10 的所有试卷
"""
import requests
import os
import time
from PIL import Image
from io import BytesIO
import json

def load_progress():
    """加载下载进度"""
    if os.path.exists('group9_10_progress.json'):
        with open('group9_10_progress.json', 'r') as f:
            return json.load(f)
    return {'completed': []}

def save_progress(completed):
    """保存下载进度"""
    with open('group9_10_progress.json', 'w') as f:
        json.dump({'completed': completed}, f)

def download_question(session, group_id, paper_id, q_num, save_dir):
    """下载单个题目"""
    url = f"https://zhentiqiang.com/static/photos/group_{group_id}/paper_{paper_id}/{q_num}.png"
    save_path = os.path.join(save_dir, f"{q_num:02d}.png")
    
    try:
        response = session.get(url, timeout=30)
        if response.status_code == 404:
            return None
        response.raise_for_status()
        
        img = Image.open(BytesIO(response.content))
        os.makedirs(save_dir, exist_ok=True)
        
        with open(save_path, 'wb') as f:
            f.write(response.content)
        
        return True
    except:
        return False

def download_paper(session, group_id, paper_id, completed):
    """下载一套试卷"""
    paper_key = f"g{group_id}_p{paper_id}"
    
    # 检查是否已完成
    if paper_key in completed:
        return 0
    
    save_dir = f"题目图片/group_{group_id}/paper_{paper_id}"
    
    # 检查是否已存在
    if os.path.exists(save_dir):
        existing = len([f for f in os.listdir(save_dir) if f.endswith('.png')])
        if existing > 0:
            print(f"  Paper {paper_id:3d}: ○ 已存在 ({existing}题)")
            completed.add(paper_key)
            return existing
    
    print(f"  Paper {paper_id:3d}: ", end='', flush=True)
    
    count = 0
    for i in range(1, 31):
        result = download_question(session, group_id, paper_id, i, save_dir)
        
        if result is None:
            if i > 5:
                break
        elif result:
            count += 1
            print(".", end='', flush=True)
        
        time.sleep(0.2)
    
    if count > 0:
        print(f" ✓ {count}题")
        completed.add(paper_key)
        return count
    else:
        print(f" ○ 不存在")
        return 0

def download_group(session, group_id, completed):
    """下载一个 group 的所有试卷"""
    print(f"\n{'='*70}")
    print(f"Group {group_id}")
    print(f"{'='*70}")
    
    group_papers = 0
    group_questions = 0
    
    for paper_id in range(1, 101):
        count = download_paper(session, group_id, paper_id, completed)
        if count > 0:
            group_papers += 1
            group_questions += count
            save_progress(list(completed))
        time.sleep(0.3)
    
    print(f"\n✓ Group {group_id} 完成: {group_papers}套试卷, {group_questions}题")
    return group_papers, group_questions

def main():
    print("\n" + "="*70)
    print("下载 Group 9 和 Group 10 (支持断点续传)")
    print("="*70)
    
    # 加载进度
    progress = load_progress()
    completed = set(progress['completed'])
    
    if completed:
        print(f"\n已完成: {len(completed)} 套试卷")
        print("将跳过已下载的试卷\n")
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': 'https://zhentiqiang.com/'
    })
    
    total_papers = 0
    total_questions = 0
    
    # 下载 group_9
    papers, questions = download_group(session, 9, completed)
    total_papers += papers
    total_questions += questions
    time.sleep(2)
    
    # 下载 group_10
    papers, questions = download_group(session, 10, completed)
    total_papers += papers
    total_questions += questions
    
    print("\n" + "="*70)
    print("全部下载完成!")
    print("="*70)
    print(f"本次下载: {total_papers} 套试卷, {total_questions} 题")
    print(f"总计完成: {len(completed)} 套试卷")
    print(f"保存位置: {os.path.abspath('题目图片')}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n已中断，进度已保存")
    except Exception as e:
        print(f"\n错误: {e}")
