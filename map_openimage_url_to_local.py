#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Map Open Images URLs (single-turn or multi-turn) to local Open Images images.

Supports two input formats:
  1. Single-turn (e.g., preference.jsonl):
     {"open_image_input_url": "https://farm6.staticflickr.com/..._o.jpg", ...}

  2. Multi-turn (e.g., multi_turn.jsonl):
     {"files": [{"id": "original_input_image", "url": "https://farm6.staticflickr.com/..._o.jpg"}, ...]}
"""

import os
import csv
import json
from tqdm import tqdm

is_multi_turn = False  # <-- Set to True for multi-turn format
metadata_csv = "openimages/train-images-boxable-with-rotation.csv"
jsonl_in = "openimages/sft.jsonl"  # or preference.jsonl or multi-turn.jsonl;change to your actual file path
jsonl_out = "openimages/sft_with_local_source_image_path.jsonl" # change to your actual desired file path
image_root = "openimages/openimage_source_images"  # parent folder containing train_*/ folders; change to your actual file path


print("📘 Loading metadata mapping (URL → ImageID)...")
url_to_id = {}
with open(metadata_csv, "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        url = row["OriginalURL"].strip()
        img_id = row["ImageID"].strip()
        url_to_id[url] = img_id
print(f"✅ Loaded {len(url_to_id):,} entries from metadata CSV")


print(f"📂 Indexing local .jpg images under {image_root}...")
local_id_to_path = {}
for root, _, files in tqdm(os.walk(image_root), desc="Scanning subfolders"):
    for file in files:
        if file.lower().endswith(".jpg"):
            image_id = os.path.splitext(file)[0]
            local_id_to_path[image_id] = os.path.join(root, file)
print(f"✅ Indexed {len(local_id_to_path):,} local image files")


count_matched = 0
count_url_not_found = 0
count_file_missing = 0

print("🔗 Mapping input URLs to local files...")
with open(jsonl_in, "r") as fin, open(jsonl_out, "w") as fout:
    for line in tqdm(fin, desc="Processing JSONL"):
        if not line.strip():
            continue
        data = json.loads(line)

        # --- SINGLE TURN FORMAT ---
        if not is_multi_turn:
            url = data.get("open_image_input_url")
        # --- MULTI TURN FORMAT ---
        else:
            url = None
            files = data.get("files", [])
            for f in files:
                if f.get("id") == "original_input_image":
                    url = f.get("url")
                    break

        if not url:
            data["local_input_image"] = None
            count_url_not_found += 1
            fout.write(json.dumps(data) + "\n")
            continue

        image_id = url_to_id.get(url)
        if not image_id:
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

print("\n Mapping complete.")
print(f"  Matched successfully: {count_matched:,}")
print(f"  URL not found in metadata: {count_url_not_found:,}")
print(f"  ImageID found but file missing locally: {count_file_missing:,}")
print(f"\nOutput saved to: {jsonl_out}")
