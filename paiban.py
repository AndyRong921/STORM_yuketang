import hashlib

# ==========================================
# 🔧 修复: 解决 macOS/Python 环境下的 'usedforsecurity' 报错
# ==========================================
try:
    _original_md5 = hashlib.md5
    def _patched_md5(*args, **kwargs):
        kwargs.pop('usedforsecurity', None)
        return _original_md5(*args, **kwargs)
    hashlib.md5 = _patched_md5
except Exception:
    pass
# ==========================================

import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, KeepTogether, Flowable, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.pdfencrypt import StandardEncryption
import os

# ================= 配置区域 =================
# 1. Excel 文件路径 (确保文件名正确)
EXCEL_PATH = "/Users/xxxxxx/xxxxxx.xlsx"

# 2. 输出路径前缀
PDF_BASE_PATH = "/Users/xxxxxx/xxxxxxx/xxxxxx.文件名字"

# 3. 页眉内容
HEADER_TEXT = "xxxxxxxx"

# ===========================================

class HorizontalLine(Flowable):
    """自定义分割线组件"""
    def __init__(self, width=440):
        Flowable.__init__(self)
        self.width = width

    def draw(self):
        self.canv.setStrokeColor(colors.lightgrey)
        self.canv.setLineWidth(0.5)
        self.canv.line(0, 0, self.width, 0)

def get_system_font_path():
    candidate_fonts = [
        "SimHei.ttf",                                
        "/Users/rongzhijin/Downloads/SimHei.ttf",    
        "/System/Library/Fonts/PingFang.ttc",                
        "/System/Library/Fonts/Supplemental/Songti.ttc",     
        "/System/Library/Fonts/STHeiti Medium.ttc",  
        "/System/Library/Fonts/STHeiti Light.ttc",   
        "/Library/Fonts/Songti.ttc",
        "/Library/Fonts/Arial Unicode.ttf",
        "C:\\Windows\\Fonts\\simhei.ttf",            
        "C:\\Windows\\Fonts\\msyh.ttf"               
    ]
    for font_path in candidate_fonts:
        if os.path.exists(font_path):
            print(f"✅ 已自动找到可用字体: {font_path}")
            return font_path
    return None

def draw_header(canvas, doc):
    canvas.saveState()
    try:
        canvas.setFont('ChineseFont', 9)
    except:
        canvas.setFont('Helvetica', 9)
    
    page_width, page_height = A4
    x_pos = page_width - 2*cm
    y_pos = page_height - 1.0*cm 
    
    canvas.drawRightString(x_pos, y_pos, HEADER_TEXT)
    canvas.setLineWidth(0.5)
    canvas.setStrokeColor(colors.grey)
    canvas.line(2*cm, y_pos - 0.2*cm, page_width - 2*cm, y_pos - 0.2*cm)
    canvas.restoreState()

# 【修改点 1】: 函数参数增加 judgment_choice
def create_pdf_file(filename, single_choice, multi_choice, judgment_choice, font_name, mode='inline'):
    """
    :param judgment_choice: 判断题列表
    """
    content_width = A4[0] - 4*cm
    
    encrypt_config = StandardEncryption(
        userPassword="", 
        ownerPassword="AndyRONG921", 
        canPrint=1, canModify=0, canCopy=1, canAnnotate=0
    )

    doc = SimpleDocTemplate(
        filename, pagesize=A4,
        rightMargin=2*cm, leftMargin=2*cm,
        topMargin=2*cm, bottomMargin=2*cm,
        encrypt=encrypt_config
    )
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(name='ExamTitle', parent=styles['Heading1'], fontName=font_name, fontSize=20, alignment=1, spaceAfter=20, textColor=colors.black)
    section_style = ParagraphStyle(name='SectionHeader', parent=styles['Heading2'], fontName=font_name, fontSize=15, spaceBefore=15, spaceAfter=10, textColor=colors.HexColor("#2c3e50"), borderPadding=5)
    question_style = ParagraphStyle(name='QuestionText', parent=styles['Normal'], fontName=font_name, fontSize=11, leading=18, spaceAfter=8, textColor=colors.black)
    option_style = ParagraphStyle(name='OptionText', parent=styles['Normal'], fontName=font_name, fontSize=10.5, leftIndent=15, leading=16, textColor=colors.HexColor("#34495e"))
    answer_style = ParagraphStyle(name='AnswerText', parent=styles['Normal'], fontName=font_name, fontSize=10, textColor=colors.HexColor("#1e8449"), leftIndent=15, spaceBefore=5, spaceAfter=5, backColor=colors.HexColor("#e8f8f5"), borderPadding=3)

    story = []
    story.append(Paragraph("《xxxxxxxxxxxxxxxx》题库", title_style))
    story.append(Spacer(1, 0.5*cm))

    # 答案收集器
    single_answers = []
    multi_answers = []
    judgment_answers = []

    # ================= 1. 单选题 =================
    if single_choice:
        story.append(Paragraph(f"一、单选题 (共 {len(single_choice)} 题)", section_style))
        story.append(HorizontalLine())
        story.append(Spacer(1, 0.3*cm))
        
        for i, q in enumerate(single_choice):
            idx = i + 1
            q_elements = []
            q_elements.append(Paragraph(f"<b>{idx}.</b> {q['title']}", question_style))
            for opt in q['options']:
                q_elements.append(Paragraph(opt, option_style))
            
            if mode == 'inline':
                q_elements.append(Paragraph(f"<b>【正确答案】 {q['answer']}</b>", answer_style))
            else:
                single_answers.append(f"{idx}.{q['answer']}")
            
            q_elements.append(Spacer(1, 0.4*cm))
            q_elements.append(HorizontalLine())
            q_elements.append(Spacer(1, 0.4*cm))
            story.append(KeepTogether(q_elements))

    # ================= 2. 多选题 =================
    if multi_choice:
        if single_choice: story.append(PageBreak())
        story.append(Paragraph(f"二、多选题 (共 {len(multi_choice)} 题)", section_style))
        story.append(HorizontalLine())
        story.append(Spacer(1, 0.3*cm))
        
        for i, q in enumerate(multi_choice):
            idx = i + 1
            q_elements = []
            q_elements.append(Paragraph(f"<b>{idx}.</b> {q['title']}", question_style))
            for opt in q['options']:
                q_elements.append(Paragraph(opt, option_style))
            
            if mode == 'inline':
                q_elements.append(Paragraph(f"<b>【正确答案】 {q['answer']}</b>", answer_style))
            else:
                multi_answers.append(f"{idx}.{q['answer']}")
            
            q_elements.append(Spacer(1, 0.4*cm))
            q_elements.append(HorizontalLine())
            q_elements.append(Spacer(1, 0.4*cm))
            story.append(KeepTogether(q_elements))

    # ================= 3. 判断题 (新增板块) =================
    if judgment_choice:
        # 如果前面有题，换页
        if single_choice or multi_choice: story.append(PageBreak())
        
        story.append(Paragraph(f"三、判断题 (共 {len(judgment_choice)} 题)", section_style))
        story.append(HorizontalLine())
        story.append(Spacer(1, 0.3*cm))
        
        for i, q in enumerate(judgment_choice):
            idx = i + 1
            q_elements = []
            # 判断题通常没有选项显示，只有题干
            q_elements.append(Paragraph(f"<b>{idx}.</b> {q['title']}", question_style))
            
            # 如果 Excel 里确实有选项（比如 A.正确 B.错误），也可以显示
            # 但之前的代码清空了选项列，所以这里通常为空
            for opt in q['options']:
                q_elements.append(Paragraph(opt, option_style))
            
            if mode == 'inline':
                # 直接显示 正确 或 错误
                q_elements.append(Paragraph(f"<b>【答案】 {q['answer']}</b>", answer_style))
            else:
                judgment_answers.append(f"{idx}.{q['answer']}")
            
            q_elements.append(Spacer(1, 0.3*cm))
            q_elements.append(HorizontalLine())
            q_elements.append(Spacer(1, 0.3*cm))
            story.append(KeepTogether(q_elements))

    # ================= 练习版答案汇总 =================
    if mode == 'end':
        story.append(PageBreak())
        story.append(Paragraph("参考答案", title_style))
        story.append(HorizontalLine())
        story.append(Spacer(1, 0.5*cm))
        
        matrix_style = TableStyle([
            ('FONTNAME', (0,0), (-1,-1), font_name),
            ('FONTSIZE', (0,0), (-1,-1), 11),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('TOPPADDING', (0,0), (-1,-1), 6),
        ])

        # 辅助函数：生成表格
        def make_answer_table(data_list, cols_count):
            table_data = []
            row = []
            for item in data_list:
                row.append(item)
                if len(row) == cols_count:
                    table_data.append(row)
                    row = []
            if row:
                while len(row) < cols_count: row.append("")
                table_data.append(row)
            col_width = content_width / cols_count
            t = Table(table_data, colWidths=[col_width] * cols_count)
            t.setStyle(matrix_style)
            return t

        if single_answers:
            story.append(Paragraph(f"<b>一、单选题答案</b>", section_style))
            story.append(make_answer_table(single_answers, 8)) # 8列
            story.append(Spacer(1, 0.5*cm))

        if multi_answers:
            story.append(Paragraph(f"<b>二、多选题答案</b>", section_style))
            story.append(make_answer_table(multi_answers, 5)) # 5列(因为多选答案长)
            story.append(Spacer(1, 0.5*cm))

        # 【新增】判断题答案表格
        if judgment_answers:
            story.append(Paragraph(f"<b>三、判断题答案</b>", section_style))
            # 判断题答案可能是中文“正确/错误”，建议用6列或8列
            story.append(make_answer_table(judgment_answers, 6)) 
            story.append(Spacer(1, 0.5*cm))

    try:
        print(f"📄 正在写入 PDF 文件: {filename} ...")
        doc.build(story, onFirstPage=draw_header, onLaterPages=draw_header)
        print(f"✅ 成功! 文件已生成: {filename}")
    except Exception as e:
        print(f"❌ 生成文件失败: {e}")

def generate_exam_pdf():
    print("🚀 开始 PDF 生成程序...")
    
    if not os.path.exists(EXCEL_PATH):
        print(f"❌ 错误: 找不到 Excel 文件! {EXCEL_PATH}")
        return

    print("🔍 正在查找中文字体...")
    font_path = get_system_font_path()
    if not font_path:
        print("❌ 未找到中文字体，无法生成 PDF。")
        return

    try:
        pdfmetrics.registerFont(TTFont('ChineseFont', font_path))
    except Exception as e:
        try:
             pdfmetrics.registerFont(TTFont('ChineseFont', font_path, subfontIndex=0))
        except:
             print(f"❌ 字体注册失败: {e}")
             return

    print(f"📊 读取 Excel: {EXCEL_PATH} ...")
    try:
        df = pd.read_excel(EXCEL_PATH).fillna("")
    except Exception as e:
        print(f"❌ 读取 Excel 失败: {e}")
        return

    single_choice_list = []
    multi_choice_list = []
    judgment_list = [] # 【新增】判断题列表

    for index, row in df.iterrows():
        try:
            ans = str(row['答案']).strip()
            # 清洗答案以便后续处理
            clean_ans = ans.replace(" ", "").replace(",", "")
            
            question_data = {
                "title": str(row['题目']),
                "options": [],
                "answer": ans
            }
            
            # 只有当非判断题时，我们才去提取A-G列
            # 但是为了兼容，我们还是都提取一下，如果为空也没关系
            for label in ['A', 'B', 'C', 'D', 'E', 'F', 'G']:
                if label in row and str(row[label]).strip() != "":
                    question_data['options'].append(f"{label}. {row[label]}")
            
            # 【修改点 2】: 核心分类逻辑
            # 如果答案包含 中文"正确/错误" 或 "对/错"，归为判断题
            if any(k in clean_ans for k in ["正确", "错误", "对", "错"]):
                judgment_list.append(question_data)
            # 如果答案长度 > 1 (如 "ABC")，归为多选题
            elif len(clean_ans) > 1:
                multi_choice_list.append(question_data)
            # 剩下的归为单选题 (A, B, C, D)
            else:
                single_choice_list.append(question_data)

        except Exception as row_e:
            continue

    print(f"📚 题目统计：单选 {len(single_choice_list)} | 多选 {len(multi_choice_list)} | 判断 {len(judgment_list)}")

    if not (single_choice_list or multi_choice_list or judgment_list):
        print("❌ 错误: Excel 中没有解析出任何题目。")
        return

    # 生成两个版本 (传入三个列表)
    file_path_inline = f"{PDF_BASE_PATH}_背诵版.pdf"
    create_pdf_file(file_path_inline, single_choice_list, multi_choice_list, judgment_list, 'ChineseFont', mode='inline')

    file_path_end = f"{PDF_BASE_PATH}_练习版.pdf"
    create_pdf_file(file_path_end, single_choice_list, multi_choice_list, judgment_list, 'ChineseFont', mode='end')
    
    try:
        os.system(f"open {os.path.dirname(PDF_BASE_PATH)}")
    except:
        pass

    print("🎉 所有任务已完成!")

if __name__ == "__main__":
    generate_exam_pdf()
