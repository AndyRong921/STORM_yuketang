import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import re
import os

# ================= 配置区域 =================
URL = "https://www.yuketang.cn/v2/web/index" ## 一般不需要修改
# 文件保存路径 (你指定的下载目录)
SAVE_PATH = "/xxxx/xxxx/xxxx/xxxx/雨课堂题库_智能版.xlsx" ## 输入你的电脑保存路径
# ===========================================

def run_interactive_spider():
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    question_db = {} 
    
    print("🚀 浏览器已启动...")
    driver.get(URL)

    print("\n" + "="*60)
    print("📢 【交互模式 - 操作指南】")
    print("1. 请手动登录 -> 进课程 -> 开始答题。")
    print("2. 直接点【交卷】->【交卷】(不用做题)。")
    print("3. 点【查看试卷】，直到看见带有正确答案的详情页。")
    print("4. 回到这里按 【回车 (Enter)】，我开始智能抓取。")
    print("="*60 + "\n")
    
    batch_count = 1
    while True:
        user_input = input(f"waiting... 请操作到【答案页面】后按回车 (输入 q 退出): ")
        if user_input.lower() == 'q': break

        # 切换到最新窗口
        if len(driver.window_handles) > 1:
            driver.switch_to.window(driver.window_handles[-1])

        print(f"   ⚡️ 正在第 {batch_count} 次抓取...")

        try:
            # 获取所有题目块
            blocks = driver.find_elements(By.CLASS_NAME, "result_item")
            
            if not blocks:
                print("   ⚠️ 没找到题目，请确认你在【查看试卷】页面！")
                continue

            new_count = 0
            for block in blocks:
                try:
                    # 1. 提取题目
                    q_text = block.find_element(By.CSS_SELECTOR, ".item-body h4").text.strip()
                    
                    # 2. 智能提取选项 (核心修改)
                    # 同时查找单选(radioText) 和 多选(checkboxText)
                    # 并且过滤掉空文本
                    opt_eles = block.find_elements(By.CSS_SELECTOR, ".radioText, .checkboxText")
                    opts = [o.text.strip() for o in opt_eles if o.text.strip()]
                    
                    # 如果上面没找到，尝试用 ElementUI 的通用类名做保底
                    if not opts:
                        opt_eles = block.find_elements(By.CSS_SELECTOR, ".el-radio__label, .el-checkbox__label")
                        opts = [o.text.strip() for o in opt_eles if o.text.strip()]

                    # 3. 提取答案 (支持多选 ABC)
                    full_text = block.text
                    ans_match = re.search(r"正确答案[：:]\s*([A-Za-z\s,]+)", full_text)
                    if ans_match:
                        # 清洗答案，比如把 "A, B" 变成 "AB"
                        ans = ans_match.group(1).replace(" ", "").replace(",", "").strip()
                    else:
                        ans = "未知"

                    # 4. 存入数据库 (动态填充)
                    if q_text and q_text not in question_db:
                        # 先创建一个基础字典
                        item_data = {
                            "题目": q_text,
                            "答案": ans
                        }
                        
                        # 动态填入选项：Excel表头预设 A-F
                        # 如果只有4个选项，E和F就是空的；如果有6个，就都填进去
                        labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
                        for i, label in enumerate(labels):
                            if i < len(opts):
                                item_data[label] = opts[i] # 有选项就填
                            else:
                                item_data[label] = ""      # 没选项就留空

                        question_db[q_text] = item_data
                        new_count += 1
                        
                except Exception as e:
                    # print(f"错题: {e}") 
                    continue
            
            print(f"   ✅ 抓取成功！本轮新增: {new_count} 题 | 总计: {len(question_db)} 题")
            save_to_excel(question_db)
            
            print("-" * 40)
            print("👉 下一步：手动点【返回】->【再次作答】->【交卷】->【查看试卷】")
            print("-" * 40)
            batch_count += 1

        except Exception as e:
            print(f"   ❌ 出错: {e}")

    print("程序结束。")
    driver.quit()

def save_to_excel(data):
    try:
        df = pd.DataFrame(data.values())
        # 强制按顺序排列列名，看起来更整齐
        cols = ["题目", "答案", "A", "B", "C", "D", "E", "F"]
        # 确保只取存在的列（防止有时候只有A-D报错）
        existing_cols = [c for c in cols if c in df.columns]
        df = df[existing_cols]
        
        df.to_excel(SAVE_PATH, index=False)
        print(f"📁 文件已更新: {SAVE_PATH}")
    except Exception as e:
        print(f"❌ 保存失败: {e}")

if __name__ == "__main__":
    run_interactive_spider()