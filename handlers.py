# handlers.py
import json
import csv
from presidio_masker import mask_text_presidio

def mask_text(input_file, output_file, log):
    with open(input_file, 'r', encoding='utf-8', errors='replace') as fi, \
         open(output_file, 'w', encoding='utf-8') as fo:
        for line_num, line in enumerate(fi, 1):
            location = f"Line {line_num}"
            masked_line = mask_text_presidio(line.rstrip('\n'), log, location)
            fo.write(masked_line)


def mask_csv(input_file, output_file, active_patterns, sub_map, log):
    with open(input_file, 'r') as fi, open(output_file, 'w', newline='') as fo:
        reader = csv.reader(fi)
        writer = csv.writer(fo)
        for row_num, row in enumerate(reader, 1):
            masked_row = []
            for col_num, cell in enumerate(row, 1):
                location = f"Row {row_num}, Column {col_num}"
                masked_cell = apply_mask(cell, active_patterns, sub_map, log, location)
                masked_row.append(masked_cell)
            writer.writerow(masked_row)


def mask_json(input_file, output_file, active_patterns, sub_map, log):
    # Note: For very large JSON files, this loads the entire file into memory.
    # For streaming large JSON, consider libraries like ijson, but for simplicity, we load fully.
    with open(input_file, 'r') as fi:
        data = json.load(fi)

    def recurse(obj, path):
        if isinstance(obj, str):
            location = '/'.join(path)
            return apply_mask(obj, active_patterns, sub_map, log, location)
        elif isinstance(obj, dict):
            return {k: recurse(v, path + [k]) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [recurse(v, path + [str(i)]) for i, v in enumerate(obj)]
        else:
            return obj

    masked_data = recurse(data, ['root'])
    with open(output_file, 'w') as fo:
        json.dump(masked_data, fo, indent=4)


def mask_hl7(input_file, output_file, active_patterns, sub_map, log):
    with open(input_file, 'r') as fi, open(output_file, 'w') as fo:
        for seg_num, seg in enumerate(fi, 1):
            seg = seg.strip()
            if not seg:
                continue
            fields = seg.split('|')
            masked_fields = []
            for field_num, field in enumerate(fields, 1):
                location = f"Segment {seg_num}, Field {field_num}"
                if '^' in field:
                    subs = field.split('^')
                    masked_subs = []
                    for sub_num, subf in enumerate(subs, 1):
                        sub_loc = f"{location}, Subfield {sub_num}"
                        masked_subs.append(apply_mask(subf, active_patterns, sub_map, log, sub_loc))
                    masked_field = '^'.join(masked_subs)
                else:
                    masked_field = apply_mask(field, active_patterns, sub_map, log, location)
                masked_fields.append(masked_field)
            fo.write('|'.join(masked_fields) + '\n')