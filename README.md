#  Crop Doctor Kenya

A deep learning tool that diagnoses crop diseases from leaf images and provides treatment recommendations in English and Swahili, built specifically for Kenyan smallholder farmers growing maize, potato, and tomato.

## The Problem

Kenya loses an estimated 30-40% of crop yields annually to plant diseases. Smallholder farmers, who produce over 75% of Kenya's food, often lack access to agricultural extension officers and cannot identify diseases early enough to prevent crop loss. A farmer who can photograph a sick leaf and get an instant diagnosis and treatment plan in their language can act before a single sick plant becomes a field-wide outbreak.

## Live Demo

[Add deployed URL once available]

## What It Does

Upload a photo of a crop leaf and get:
- Instant disease diagnosis with confidence score
- Severity classification (Critical, High, Medium, Healthy)
- Step-by-step treatment recommendations
- Prevention advice
- Disease name in Swahili
- Urgency rating from "monitor regularly" to "act within 24 hours"
- Contact details for KALRO and agricultural extension services

## Supported Crops and Diseases

### Maize (Mahindi) 4 classes
- Gray Leaf Spot (Ugonjwa wa Madoa ya Kijivu)
- Common Rust (Kutu ya Mahindi)
- Northern Leaf Blight (Ugonjwa wa Majani ya Mahindi)
- Healthy (Mahindi Yenye Afya)

### Potato (Viazi) 3 classes
- Early Blight (Ugonjwa wa Mapema wa Viazi)
- Late Blight (Ugonjwa wa Marehemu wa Viazi) Critical
- Healthy (Viazi Vyenye Afya)

### Tomato (Nyanya) 10 classes
- Bacterial Spot (Madoa ya Bakteria ya Nyanya)
- Early Blight (Ugonjwa wa Mapema wa Nyanya)
- Late Blight (Ugonjwa wa Marehemu wa Nyanya) Critical
- Leaf Mold (Ukungu wa Majani ya Nyanya)
- Septoria Leaf Spot (Madoa ya Majani ya Nyanya)
- Spider Mites (Utitiri wa Nyanya)
- Target Spot (Madoa ya Lengo ya Nyanya)
- Yellow Leaf Curl Virus (Virusi vya Manjano ya Nyanya) Critical
- Mosaic Virus (Virusi vya Mosaic ya Nyanya)
- Healthy (Nyanya Yenye Afya)

## Model Performance

| Metric | Value |
|---|---|
| Architecture | MobileNetV2 (transfer learning, ImageNet weights) |
| Training images | 5,100 (300 per class) |
| Validation accuracy | 87.18% |
| Classes | 17 (14 diseases + 3 healthy) |
| Input size | 224 x 224 RGB |
| Confidence threshold | 60% below this the model flags uncertainty |

Training was performed on Google Colab (T4 GPU) using transfer learning with the base MobileNetV2 frozen and a custom classification head trained for 10 epochs.

## Dataset

[PlantVillage Dataset](https://www.kaggle.com/datasets/vipoooool/new-plant-diseases-dataset) containing 87,900 labeled crop leaf images across 38 classes. This project uses a Kenya-relevant subset of 17 classes covering maize, potato, and tomato, the three most important staple crops for Kenyan smallholder farmers.

## Kenya-Specific Features

- Disease names translated to Swahili for all 17 classes
- Treatment recommendations reference locally available fungicides and Kenya-specific organizations (KALRO, county agriculture offices)
- Severity classification with urgency ratings aligned to real agricultural extension guidance
- Contact information for KALRO helpline (+254 20 4183301) and free Safaricom SMS service (0800 720 710)
- Confidence threshold warning: if the model is less than 60% confident, it explicitly recommends consulting a professional rather than guessing

## Honest Limitations

- Trained on laboratory-quality images, accuracy may be lower on blurry or poorly lit field photos
- 300 training images per class is a relatively small dataset; performance on rare disease presentations may be weaker
- Does not cover all crops grown in Kenya. Wheat, beans, cassava, and other crops are not supported
- This is a portfolio demonstration tool, not a certified agricultural diagnostic instrument
- For Critical severity diseases (Late Blight, Yellow Leaf Curl Virus), always consult an agricultural extension officer to confirm diagnosis before destroying crops

## Tech Stack

- Model training: TensorFlow, Keras, MobileNetV2, Google Colab T4 GPU
- Data: PlantVillage dataset via Kaggle
- App: Streamlit, Python 3.11
- Image processing: Pillow, NumPy

## Project Structure
