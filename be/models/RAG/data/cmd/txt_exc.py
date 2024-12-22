def split_txt_file(input_file, output_dir, lines_per_file=5000):
    import os

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(input_file, 'r', encoding='utf-8') as file:
        file_number = 1
        lines = []
        for line in file:
            lines.append(line)
            if len(lines) == lines_per_file:
                output_file = os.path.join(output_dir, f'output_{file_number}.txt')
                with open(output_file, 'w', encoding='utf-8') as output:
                    output.writelines(lines)
                lines = []
                file_number += 1

        # Write remaining lines to the last file
        if lines:
            output_file = os.path.join(output_dir, f'output_{file_number}.txt')
            with open(output_file, 'w', encoding='utf-8') as output:
                output.writelines(lines)


# Example usage
input_file = '../output/txt/SCUEC学生手册2024版V1.1.txt'
output_dir = '../output/txt/split_files'
split_txt_file(input_file, output_dir)
