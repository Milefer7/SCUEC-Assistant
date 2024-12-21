import pandas as pd
import os


def split_csv(input_csv_file, output_dir, max_lines=2000):
    # 读取输入的 CSV 文件，跳过错误行并显示警告
    df = pd.read_csv(input_csv_file, on_bad_lines='warn')

    # 创建输出目录（如果不存在）
    os.makedirs(output_dir, exist_ok=True)

    # 获取 CSV 文件的总行数
    total_rows = len(df)
    print(f"Total rows in the CSV: {total_rows}")

    # 计算需要多少个文件
    num_files = (total_rows // max_lines) + 1
    print(f"Splitting into {num_files} files.")

    for i in range(num_files):
        # 计算每个文件的起始和结束行
        start_row = i * max_lines
        end_row = min((i + 1) * max_lines, total_rows)

        # 获取当前分块的数据
        chunk = df.iloc[start_row:end_row]

        # 生成新文件名
        output_file = os.path.join(output_dir, f"output_{i + 1}.csv")

        # 保存当前块数据到新的 CSV 文件
        chunk.to_csv(output_file, index=False)
        print(f"Saved: {output_file}")


# 主程序
input_csv_file = '../output/table/all_tables.csv'  # 输入的 CSV 文件
output_dir = '../output/table/split'  # 输出目录，保存分割后的 CSV 文件

# 执行切分操作
split_csv(input_csv_file, output_dir)

print("CSV splitting complete.")
