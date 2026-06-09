"""
自动下载答案解析图片 (1700-2000)
保存到 answer 文件夹
无需按回车，自动开始
"""
from download_answers import download_batch_answers
import sys

if __name__ == "__main__":
    print("\n" + "="*70)
    print("自动下载答案解析图片 (1700-2000)")
    print("="*70)
    print("\n配置:")
    print("  范围: 1700 - 2000")
    print("  保存目录: answer")
    print("  共计: 301 个答案")
    print("\n按 Ctrl+C 可随时中断，进度会自动保存")
    print("="*70)
    print("\n开始下载...\n")
    
    try:
        success, exists, not_found, error = download_batch_answers(1700, 2000, "answer")
        
        print("\n" + "="*70)
        print("✅ 全部完成！")
        print("="*70)
        print(f"\n下载范围: 1700-2000")
        print(f"保存位置: answer 文件夹")
        
    except KeyboardInterrupt:
        print("\n\n⚠️ 已中断，进度已保存")
        print("下次运行会自动继续")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
