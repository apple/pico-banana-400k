#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Map 'open_image_input_url' in a JSONL file to local Open Images images by searching all subfolders.

Steps:
1. Read Open Images metadata CSV (ImageID ↔ OriginalURL)
2. Recursively index all local image files under image_root
3. Match each JSONL entry’s URL → ImageID → local file
4. Write a new JSONL with 'local_input_image' field
"""

import os
import csv
import json
from tqdm import tqdm


metadata_csv = "/openimages/train-images-boxable-with-rotation.csv"
jsonl_in = "/openimages/sft.jsonl"
jsonl_out = "/openimages/sft_with_local_source_images.jsonl"
image_root = "/openimages/openimage_source_images"  # parent folder containing train_0/, train_1/, etc.


url_to_id = {}
with open(metadata_csv, "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        url = row["OriginalURL"].strip()
        img_id = row["ImageID"].strip()
        url_to_id[url] = img_id

print(f"📘 Loaded {len(url_to_id):,} metadata entries (URL → ImageID)")


print(f"📂 Scanning local images under: {image_root}")
local_id_to_path = {}

for root, _, files in tqdm(os.walk(image_root), desc="Indexing local images"):
    for file in files:
        if file.lower().endswith(".jpg"):
            image_id = os.path.splitext(file)[0]
            full_path = os.path.join(root, file)
            local_id_to_path[image_id] = full_path

print(f"📦 Indexed {len(local_id_to_path):,} local images")

# ==== STEP 3: Process JSONL ====
count_matched = 0
count_url_not_found = 0
count_file_missing = 0

with open(jsonl_in, "r") as fin, open(jsonl_out, "w") as fout:
    for line in tqdm(fin, desc="Mapping URLs"):
        if not line.strip():
            continue
        data = json.loads(line)
        url = data.get("open_image_input_url")

        if not url:
            data["local_input_image"] = None
            count_url_not_found += 1
            fout.write(json.dumps(data) + "\n")
            continue

        image_id = url_to_id.get(url)
        if not image_id:
            # URL not found in metadata mapping
            data["local_input_image"] = None
            count_url_not_found += 1
        else:
            local_path = local_id_to_path.get(image_id)
            if local_path and os.path.exists(local_path):
                data["local_input_image"] = local_path
                count_matched += 1
            else:
                data["local_input_image"] = None
                count_file_missing += 1

        fout.write(json.dumps(data) + "\n")


print("\n✅ Mapping completed.")
print(f"  🟢 Matched successfully: {count_matched:,}")
print(f"  🟡 URL not found in metadata: {count_url_not_found:,}")
print(f"  🔴 ImageID found but file missing locally: {count_file_missing:,}")
print(f"\nOutput saved to: {jsonl_out}")
