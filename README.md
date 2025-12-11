# 第一部分：雨课堂智能题库抓取工具 (Yuketang Interactive Spider)

这是一个基于 **Selenium** 和 **Pandas** 开发的交互式 Python 爬虫工具。它可以辅助用户在雨课堂 Web 端进行练习时，自动抓取题目、选项及正确答案，并将其整理保存为 Excel 题库文件，方便后续复习。

## ✨ 功能特点

- **🤖 自动化驱动**：自动调用 Chrome 浏览器，利用 `webdriver_manager` 自动管理驱动版本。
- **🔄 交互式抓取**：无需复杂的逆向 API，采用“手动答题/交卷 -> 程序抓取”的半自动模式，安全且稳定。
- **📝 智能解析**：
  - 支持单选题和多选题。
  - 自动识别并清洗选项（A-G）。
  - 自动提取正确答案（支持多选组合，如 "AB"）。
- **💾 增量保存**：每次抓取自动追加并保存到 Excel，具备去重功能，防止题目重复记录。

## 🛠️ 环境要求

- **Python**: 3.8+
- **Browser**: Google Chrome

### 依赖库安装

在使用前，请确保安装了以下 Python 库：

```bash
pip install pandas selenium webdriver-manager openpyxl
````

> 注意：`openpyxl` 是 Pandas 写入 Excel (.xlsx) 文件所必需的依赖。

## ⚙️ 配置说明

在运行代码之前，请打开脚本文件，根据你的电脑环境修改 **配置区域**：

```python
# ================= 配置区域 =================
# 目标网址 (通常不需要修改)
URL = "[https://www.yuketang.cn/v2/web/index]" 

# 📢 重要：请修改为你自己的保存路径！
SAVE_PATH = "/Users/AndyRONG/Downloads/雨课堂题库_智能版.xlsx"
# Windows 示例: r"D:\学习资料\雨课堂题库.xlsx"
# Mac 示例: "/Users/your_name/Downloads/雨课堂题库.xlsx"

# ===========================================
```

## 🚀 使用指南 (保姆级教程)

1.  **运行脚本**：
    在终端或 IDE 中运行 Python 脚本：

    ```bash
    python spider.py
    ```

2.  **登录与进入课程**：

      - 脚本会自动打开一个 Chrome 浏览器窗口。
      - 请在浏览器中选择要登录的雨课堂（OUC默认选择长江雨课堂），然后微信扫码登录账号。
      - 点击进入你要刷题的课程章节。

3.  **操作流程**：
    此爬虫采用“交互模式”，请遵循控制台打印的指引：

    1.  点击 **【开始答题】**。
    2.  直接点击 **【交卷】** -\> **【确认交卷】**（不需要真的做题，目的是为了看答案）。
    3.  点击 **【查看试卷】**，直到页面加载出带有**正确答案**的详情页。
    4.  回到运行脚本的控制台（Terminal），按下 **【回车键 (Enter)】**。

4.  **查看结果**：

      - 程序会自动抓取当前页面的所有题目。
      - 控制台会提示：`✅ 抓取成功！本轮新增: X 题`。
      - Excel 文件会自动更新。

5.  **循环操作**：

      - 在浏览器点击 **【返回】** -\> **【再次作答】** -\> **【交卷】** -\> **【查看试卷】**。
      - 再次按 **【回车】** 抓取新的一批题目。
      - 输入 `q` 并回车可退出程序。

## 📂 输出文件示例

生成的 Excel 文件将包含以下列：

| 题目 | 答案 | A | B | C | D | ... |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 下列关于Python说法正确的是？ | ABC | 简单易学 | 开源免费 | 跨平台 | 只能在Windows运行 | ... |

## ⚠️ 免责声明 (Disclaimer)

1.  **仅供学习交流**：本项目仅用于个人学习代码编写、自动化测试技术研究以及个人复习资料整理。
2.  **请勿用于作弊**：严禁将本工具用于任何形式的考试作弊或商业用途。
3.  **数据安全**：本工具运行在本地，不会上传用户的账号密码，但请妥善保管生成的题库文件。
4.  使用本工具所产生的任何后果由使用者自行承担。

-----

# 第二部分：题库 Excel 转 PDF 生成器 (Excel to PDF Quiz Generator)

这是一个基于 Python 的实用工具，用于将 Excel 格式的题库自动转换为排版精美的 PDF 文件。

该工具专为整理“雨课堂”等平台的题库设计，能够一键生成两个版本的 PDF：
1.  **解析版**：每道题下方紧跟正确答案，适合背诵和复习。
2.  **练习版**：题目中不含答案，并在文档末尾附带答案速查表（方阵格式），适合模拟自测。

## ✨ 功能特点

* **双模式输出**：同时生成“解析版”和“练习版”两个 PDF 文件。
* **智能排版**：
    * 自动识别单选题和多选题，并分章节排版。
    * 题目与选项智能防跨页截断（KeepTogether），阅读体验极佳。
    * 练习版末尾自动生成矩阵式的答案速查表。
* **跨平台字体支持**：自动检测 macOS 和 Windows 系统下的常用中文字体（如 SimHei, PingFang, Songti 等），无需繁琐配置。
* **PDF 安全保护**：支持设置 PDF 权限（如禁止修改、禁止复制等）。
* **macOS 兼容性修复**：内置针对 macOS OpenSSL 环境的 `hashlib` 补丁，解决 ReportLab 在特定环境下的报错问题。

## 🛠 环境依赖

本项目依赖 Python 3.x 及以下第三方库：

* `pandas` (数据处理)
* `openpyxl` (读取 Excel 引擎)
* `reportlab` (PDF 生成核心)

### 安装依赖

```bash
pip install pandas openpyxl reportlab
````

## 📂 数据格式要求

请准备一个 `.xlsx` Excel 文件，数据表头（第一行）需包含以下列名：

| 列名 | 说明 |
| :--- | :--- |
| **题目** | 题干内容 |
| **答案** | 正确选项（如 "A", "ABC"） |
| **A** | 选项 A 的内容 |
| **B** | 选项 B 的内容 |
| **...** | 更多选项 (C, D, E...) |

> **注意**：程序会自动过滤掉内容为空的选项列。

## 🚀 快速开始

1.  克隆本项目到本地：

    ```bash
    git clone [https://github.com/AndyRong921/Excel-to-PDF-Quiz-Generator.git](https://github.com/AndyRong921/Excel-to-PDF-Quiz-Generator.git)
    cd Excel-to-PDF-Quiz-Generator
    ```

2.  将你的题库 Excel 文件放入项目目录（例如命名为 `question_bank.xlsx`）。

3.  修改脚本 `paiban.py` 顶部的配置区域：

    ```python
    # ================= 配置区域 =================
    INPUT_EXCEL_NAME = "question_bank.xlsx"  # 你的输入文件名
    OUTPUT_PREFIX = "自定义姓名"        # 输出文件名前缀
    HEADER_TEXT = "适用学期：2025年秋季学期"   # PDF 页眉文字
    # ===========================================
    ```

4.  运行脚本：

    ```bash
    python paiban.py
    ```

5.  运行成功后，你将在同目录下看到生成的两个 PDF 文件（解析版 & 练习版）。

## ⚙️ 高级配置

### PDF 加密与权限

在 `paiban.py` 代码中，你可以修改 `StandardEncryption` 的参数来调整 PDF 权限：

```python
encrypt_config = StandardEncryption(
    userPassword="",                 # 打开密码（留空则直接打开）
    ownerPassword="YourSecretPassword", # 权限密码
    canPrint=1,                      # 允许打印
    canModify=0,                     # 禁止修改
    canCopy=1                        # 允许复制文本
)
```

## 📝 License

[MIT License](https://www.google.com/search?q=LICENSE)

-----
如果觉得好用，欢迎点个 Star ⭐️！
**Author**: [AndyRong921](https://www.google.com/search?q=https://github.com/AndyRong921)

```


```


