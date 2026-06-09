"""
快速下载答案解析图片 (640-1700)
保存到 answer 文件夹
"""
from download_answers import download_batch_answers

if __name__ == "__main__":
    print("\n" + "="*70)
    print("快速下载答案解析图片")
    print("="*70)
    print("\n配置:")
    print("  范围: 640 - 1700")
    print("  保存目录: answer")
    print("\n按 Ctrl+C 可随时中断，进度会自动保存")
    print("="*70)
    
    input("\n按回车键开始下载...")
    
    try:
        download_batch_answers(640, 1700, "answer")
    except KeyboardInterrupt:
        print("\n\n已中断，进度已保存")
        print("下次运行会自动继续")
    except Exception as e:
        print(f"\n错误: {e}")
        import traceback
        traceback.print_exc()
