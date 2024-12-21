import pandas as pd
import pdfplumber
import camelot
import os

# 提取PDF中的文本和表格
def extract_text_and_tables(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        tables = []

        # 遍历每一页
        for page_num, page in enumerate(pdf.pages):
            # 提取文本
            text += page.extract_text()

            # 提取表格
            table = page.extract_table()
            if table:
                # 清理并格式化表格，直接将表格数据附加到文本后面
                cleaned_table = clean_table_data(table)
                # 使用 f"Page {page_num + 1}" 保留页码信息
                tables.append((f"Page {page_num + 1}", cleaned_table))  # 保存页码与表格

        return text, tables


# 使用Camelot来提高表格提取质量
def extract_tables_with_camelot(pdf_path):
    tables = camelot.read_pdf(pdf_path, pages='all', flavor='stream')  # 使用stream模式获取更多信息
    cleaned_tables = []
    for table in tables:
        df = table.df
        df.dropna(inplace=True)  # 去掉空值
        df.drop_duplicates(inplace=True)  # 去掉重复行
        cleaned_tables.append(df)
    return cleaned_tables


# 清理表格数据
def clean_table_data(table):
    df = pd.DataFrame(table[1:], columns=table[0])  # 第一行是列名
    df.dropna(inplace=True)  # 去掉空值
    df.drop_duplicates(inplace=True)  # 去掉重复行
    return df


# 将所有表格内容保存到一个 CSV 文件
def save_all_tables_to_csv(tables_data, output_csv_file):
    with open(output_csv_file, 'w', newline='', encoding='utf-8') as f:
        first_table = True
        for i, (table_info, table) in enumerate(tables_data):
            page_num = table_info.split(" ")[-1]  # 获取页面编号，格式为 'Page 1'，取 1 作为页码

            # 在表格内容前加入表格编号和页码信息
            if first_table:
                # 写入表头（表头只写一次）
                table.to_csv(f, index=False, header=True)
                first_table = False
            else:
                # 后续表格仅写入数据，不重复写表头
                table.to_csv(f, index=False, header=False)

            print(f"Table {i + 1} (Page {page_num}) saved to CSV.")

    print(f"All tables have been saved to {output_csv_file}")


# 主程序
pdf_path = "../resource/SCUEC学生手册2024版.pdf"
text, tables = extract_text_and_tables(pdf_path)

# 尝试使用Camelot提取更多的表格
camelot_tables = extract_tables_with_camelot(pdf_path)

# 合并pdfplumber提取的表格和Camelot提取的表格
tables.extend([(f"Camelot - {i + 1}", table) for i, table in enumerate(camelot_tables)])

# 设置输出文件路径
output_csv_file = "../output/table/all_tables.csv"  # 所有表格保存为一个 CSV 文件

# 保存所有表格到一个 CSV 文件
save_all_tables_to_csv(tables, output_csv_file)

print(f"Text and tables extracted and saved to {output_csv_file}")
