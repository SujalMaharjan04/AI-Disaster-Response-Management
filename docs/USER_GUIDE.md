# 📖 User Guide: AI Disaster Response Platform

## Overview
This platform helps emergency responders analyze satellite imagery after a disaster (flood/earthquake) to identify damaged buildings and get actionable recommendations based on official guidelines.

## How to Use the Platform

### 1. Image Analysis
- **Upload**: Drag and drop a satellite image of the disaster area into the **Upload Zone**.
- **Processing**: The system will:
  - Use a YOLO segmentation model to detect building footprints.
  - Classify each building as: *No Damage, Minor Damage, Major Damage,* or *Destroyed*.
  - Consult official response guidelines via the RAG engine.

### 2. Reading the Results
- **Damage Summary**: View the total count of buildings in each damage category.
- **Geospatial View**: The map overlays the analyzed imagery to show the extent of the disaster.
- **Emergency Recommendation**: Read the AI-generated a recommendation. This is based on the specific counts of damaged buildings and the official guidelines stored in the knowledge base.

## For the Demo
1. Upload a known disaster image (e.g., from the xView2 test set).
2. Wait for the "Analysis Completed" status.
3. Show the **Destroyed** count $\rightarrow$ Point to the **Emergency Recommendation** $\rightarrow$ Explain how the AI used guidelines to suggest priority actions.
