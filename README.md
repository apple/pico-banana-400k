# 🍌 Pico-Banana-400K: A Large-Scale Dataset for Text-Guided Image Editing

<font size=7><div align='center' > [[📖 Paper](https://www.arxiv.org/pdf/2510.19808)]  </div></font>

**Pico-Banana-400K** is a large-scale dataset of **~400K text–image–edit triplets** designed to advance research in **text-guided image editing**.  
Each example contains:
- an **original image** (from [Open Images](https://storage.googleapis.com/openimages/web/factsfigures.html)),  
- a **human-like edit instruction**, and  
- the **edited result** generated and verified by the *Nano-Banana* model.

The dataset spans **35 edit operations** across **8 semantic categories**, covering diverse transformations—from low-level color adjustments to high-level object, scene, and stylistic edits.

---



## 🧩 Key Features

| Feature | Description |
|----------|-------------|
| **Total Samples** | ~257K single-turn text–image–edit triplets for SFT, ~56K single-turn text-image(positive) - image(negative)-edit for preference learning, and ~72K multi-turn texts-images-edits for multi-turn applications|
| **Source** | [Open Images](https://storage.googleapis.com/openimages/web/factsfigures.html) |
| **Edit Operations** | 35 across 8 semantic categories |
| **Categories** | Pixel & Photometric, Object-Level, Scene Composition, Stylistic, Text & Symbol, Human-Centric, Scale & Perspective, Spatial/Layout |
| **Image Resolution** | 512–1024 px |
| **Prompt Generator** | [Gemini-2.5-Flash](https://deepmind.google/discover/blog/gemini-2-5/) |
| **Editing Model** | Nano-Banana |
| **Self-Evaluation** | Automated judging pipeline using Gemini-2.5-Pro for edit quality |

---

## 🏗️ Dataset Construction

Pico-Banana-400K is built using a **two-stage multimodal generation pipeline**:

1. **Instruction Generation**  
   Each Open Images sample is passed to *Gemini-2.5-Flash*, which writes concise, natural-language editing instructions grounded in visible content. We also provide short instructions summarized by Qwen-2.5-Instruct-7B. 
   Example:  
   ```json
   {
     "instruction": "Change the red car to blue."
   }
   

2. **Editing + Self-Evaluation**
   The Nano-Banana model performs the edit, then automatically evaluates the result using a structured quality prompt that measures:
   Instruction Compliance (40%)
   Editing Realism (25%)
   Preservation Balance (20%)
   Technical Quality (15%)
   Only edits scoring above a strict threshold (~0.7) are labeled as successful, forming the main dataset; the remaining ~56K are retained as failure cases for robustness and preference learning.

## 📊 Dataset Statistics

**Nano-Banana-400K** contains **~400K image editing data**, covering a wide visual and semantic range drawn from real-world imagery.

---

### 🧭 Category Distribution

| Category | Description | Percentage |
|:----------|:-------------|:------------:|
| **Object-Level Semantic** | Add, remove, replace, or relocate objects | **35%** |
| **Scene Composition & Multi-Subject** | Contextual and environmental transformations | **20%** |
| **Human-Centric** | Edits involving clothing, expression, or appearance | **18%** |
| **Stylistic** | Domain and artistic style transfer | **10%** |
| **Text & Symbol** | Edits involving visible text, signs, or symbols | **8%** |
| **Pixel & Photometric** | Brightness, contrast, and tonal adjustments | **5%** |
| **Scale & Perspective** | Zoom, viewpoint, or framing changes | **2%** |
| **Spatial / Layout** | Outpainting, composition, or canvas extension | **2%** |

---

### 📂 Data Composition

- **Single-Turn SFT samples (successful edits):** ~257K  
- **Single-Turn Preference samples (failure cases):** ~56K
- **Multi-Turn SFT samples (successful cases):** ~72K  
- **Gemini-generated instructions:** concise, natural, and image-aware
- **Edit coverage:** 35 edit types across 8 semantic categories  
- **Image diversity:** includes humans, objects, text-rich scenes, etc from Open Images  

---

### 🖼️ Visualization

Below are representative examples from different categories:

| Category | Example |
|:----------|:---------|
| Object-Level | “Replace the red apple with a green one.” |
| Scene Composition | “Add sunlight streaming through the window.” |
| Human-Centric | “Change the person’s expression to smiling.” |
| Text & Symbol | “Uppercase the text on the billboard.” |
| Stylistic | “Convert the image to a Van Gogh painting style.” |

---

Pico-Banana-400K provides both **breadth** (diverse edit operations) and **depth** (quality-controlled multimodal supervision), making it a strong foundation for training and evaluating text-guided image editing models.

## 🧠 Applications

**Pico-Banana-400K** serves as a versatile resource for advancing controllable and instruction-aware image editing.  
Beyond single-step editing, the dataset enables **multi-turn, conversational editing** and **reward-based training paradigms**.



## 📦 Dataset Download Guide

The **Pico-Banana-400K** dataset is hosted on Apple’s public CDN.  
You can download each component (single-turn, multi-turn, and preference data) using the provided manifest files.  

---

### 🖼️ 1. Single-Turn Edited Images 
Manifest files: [sft link](https://ml-site.cdn-apple.com/datasets/pico-banana-300k/nb/manifest/sft_manifest.txt) and [preference link](https://ml-site.cdn-apple.com/datasets/pico-banana-300k/nb/manifest/preference_manifest.txt)


### 🖼️ 2. Multi-Turn Edited Images 
Manifest file: [multi-turn link](https://ml-site.cdn-apple.com/datasets/pico-banana-300k/nb/manifest/multi_turn_manifest.txt)

### 🖼️ 3. Source Images 
Urls to download source images are provided along with edit instructions in [sft link](https://ml-site.cdn-apple.com/datasets/pico-banana-300k/nb/jsonl/sft.jsonl), [preference link](https://ml-site.cdn-apple.com/datasets/pico-banana-300k/nb/jsonl/preference.jsonl), and [multi-turn link](https://ml-site.cdn-apple.com/datasets/pico-banana-300k/nb/jsonl/multi-turn.jsonl). If you hit rate limit with Flickr when downloading images, you can either request higher rate limit with Flickr or follow steps below.
 
Another way to download the source images is to download packed files train_0.tar.gz and train_1.tar.gz from [Open Images](https://github.com/cvdfoundation/open-images-dataset#download-images-with-bounding-boxes-annotations), then map with the urls we provide. We also provide a sample mapping code [here](map_openimage_url_to_local.py). Due to legal requirements, we cannot provide the source image files directly.
```bash
# install awscli(https://aws.amazon.com/cli/)
# Download Open Images packed files 
aws s3 --no-sign-request --endpoint-url https://s3.amazonaws.com cp s3://open-images-dataset/tar/train_0.tar.gz . 
aws s3 --no-sign-request --endpoint-url https://s3.amazonaws.com cp s3://open-images-dataset/tar/train_1.tar.gz . 

# Create folder for extracted images 
mkdir openimage_source_images

# Extract the tar files 
tar -xvzf train_0.tar.gz -C openimage_source_images
tar -xvzf train_1.tar.gz -C openimage_source_images

# Download metadata CSV (ImageID ↔ OriginalURL mapping)  
wget https://storage.googleapis.com/openimages/2018_04/train/train-images-boxable-with-rotation.csv

# Map urls to local paths
python map_openimage_url_to_local.py #please modify variable is_multi_turn and file paths as needed
```

## 🧩 License
Pico-Banana-400K is released under the Creative Commons Attribution–NonCommercial–NoDerivatives (CC BY-NC-ND 4.0) license.
✅ Free for research and non-commercial use
❌ Commercial use and derivative redistribution are not permitted
🖼️ Source images follow the Open Images (CC BY 2.0) license
By using this dataset, you agree to comply with the terms of both licenses.


## 📘 Citation

If you use **🍌 Pico-Banana-400K** in your research, please cite it as follows:

```bibtex
@inproceedings{Qian2025PicoBanana400KAL,
  title={Pico-Banana-400K: A Large-Scale Dataset for Text-Guided Image Editing},
  author={Yusu Qian and Eli Bocek-Rivele and Liangchen Song and Jialing Tong and Yinfei Yang and Jiasen Lu and Wenze Hu and Zhe Gan},
  year={2025},
  url={https://api.semanticscholar.org/CorpusID:282272484}
}


