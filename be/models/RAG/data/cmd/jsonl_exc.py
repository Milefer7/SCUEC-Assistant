import json

def merge_jsonl_files(input_files, output_file):
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for input_file in input_files:
            with open(input_file, 'r', encoding='utf-8') as infile:
                for line in infile:
                    # Read each line and write it to the output file
                    outfile.write(line)
    print(f"Files merged into {output_file}")

# Example usage:
input_files = ['../output/jsonl/output_1-成功.jsonl', '../output/jsonl/output_2-成功.jsonl', '../output/jsonl/output_3-成功.jsonl', '../output/jsonl/output_4-成功.jsonl']
output_file = '../output/jsonl/success/merged_output.jsonl'
merge_jsonl_files(input_files, output_file)