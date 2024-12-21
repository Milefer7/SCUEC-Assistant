import json

input_file = 'merged_data_in_use.jsonl'
output_file = 'modified_data.jsonl'

with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
    for line in infile:
        data = json.loads(line.strip())
        data['instruction'] = data.pop('input')
        data['input'] = ""
        json.dump(data, outfile, ensure_ascii=False)
        outfile.write('\n')