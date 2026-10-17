# 🛰️ AI Disaster Response: YOLO Training Pipeline

This folder contains everything needed to train the building damage assessment model on Google Colab.

## 🚀 Quick Start Guide

1. **Prepare Data**:
   - Zip the `data/processed/multi_hazards` folder.
   - Upload `multi_hazards.zip` and `ai/datasets/dataset.yaml` to your Google Drive.

2. **Run Notebook**:
   - Open `train_yolo.ipynb` in Google Colab.
   - Change the runtime to **GPU** (T4, A100, or L4).
   - Follow the cells in order.

3. **Key Steps in Notebook**:
   - **Cell 1**: Mount Google Drive.
   - **Cell 2**: Install dependencies using `requirements.txt`.
   - **Cell 3**: Unzip the dataset to the Colab local disk for faster I/O.
   - **Cell 4**: Initialize YOLO11-seg (or YOLOv8-seg) and start training.
   - **Cell 5**: Evaluate on the test set.
   - **Cell 6**: Export `best.pt` back to Google Drive.

## 📊 Training Parameters
We use the configurations in `ai/training/configs/hyperparameters.yaml`. 
- **Epochs**: 100
- **Image Size**: 640x640
- **Model**: YOLO11n-seg (Nano) for speed and efficiency in a hackathon context.
