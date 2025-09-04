# Image Search Engine with OpenCV and Python

A complete Content-Based Image Retrieval (CBIR) system that allows you to search through image collections using visual similarity rather than text-based metadata. This project implements a "search by example" image search engine using color histograms in the HSV color space.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technical Architecture](#technical-architecture)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [Configuration](#configuration)
- [Examples](#examples)
- [Limitations](#limitations)
- [Future Improvements](#future-improvements)
- [Contributing](#contributing)
- [License](#license)

## Overview

This image search engine utilizes computer vision techniques to create a visual search system. Instead of relying on text tags or metadata, it analyzes the actual visual content of images to find similar ones. The system is particularly effective for vacation photos, stock images, and any collection where visual similarity is more important than textual descriptions.

### Key Capabilities

- **Visual Search**: Submit a query image and find visually similar images
- **Color-Based Matching**: Uses HSV color histograms for robust color analysis
- **Region-Based Analysis**: Divides images into 5 regions for spatial color distribution
- **Scale Invariant**: Works with images of different sizes
- **Fast Retrieval**: Efficient similarity computation using chi-squared distance

## Features

- ✅ Content-Based Image Retrieval (CBIR) system
- ✅ HSV color space analysis for better human perception alignment
- ✅ Region-based color histograms for spatial awareness
- ✅ Chi-squared distance metric for similarity comparison
- ✅ Configurable histogram bins for different dataset sizes
- ✅ CSV-based indexing for fast search operations
- ✅ Command-line interface for easy integration
- ✅ Extensible architecture for additional descriptors

## Technical Architecture

### Core Components

1. **ColorDescriptor**: Extracts 3D HSV color histograms from images
2. **Indexer**: Processes dataset and creates searchable feature database
3. **Searcher**: Compares query images against indexed features
4. **Search Interface**: Command-line tool for performing searches

### Algorithm Pipeline

```
Input Image → HSV Conversion → Region Segmentation → Histogram Extraction → Feature Vector → Similarity Comparison → Ranked Results
```

## Installation

### Prerequisites

- Python 3.6+
- OpenCV 3.0+ or 4.0+
- NumPy
- imutils

### Setup

1. Clone the repository:
```bash
git clone https://github.com/Shuv13/image-search-engine.git
cd image-search-engine
```

2. Install required dependencies:
```bash
pip install opencv-python numpy imutils
```

3. Verify OpenCV installation:
```python
import cv2
print(cv2.__version__)
```

## Usage

### 1. Prepare Your Dataset

Organize your images in a single directory:
```
dataset/
├── image1.png
├── image2.png
├── image3.png
└── ...
```

### 2. Index Your Dataset

Create a searchable index of your image collection:

```bash
python index.py --dataset path/to/dataset --index index.csv
```

**Parameters:**
- `--dataset`: Path to directory containing images to index
- `--index`: Output path for the generated index file

### 3. Perform Searches

Search for similar images using a query image:

```bash
python search.py --index index.csv --query path/to/query.png --result-path path/to/dataset
```

**Parameters:**
- `--index`: Path to the generated index file
- `--query`: Path to the query image
- `--result-path`: Path to the dataset directory for displaying results

### 4. View Results

The system will display:
1. Your query image
2. Similar images ranked by relevance (press any key to cycle through results)

## Project Structure

```
image-search-engine/
├── pyimagesearch/
│   ├── __init__.py
│   ├── colordescriptor.py    # Color histogram extraction
│   └── searcher.py           # Search and similarity functions
├── dataset/                  # Your image collection
├── queries/                  # Sample query images
├── index.py                  # Dataset indexing script
├── search.py                 # Search interface script
├── index.csv                 # Generated feature index
└── README.md
```

## How It Works

### 1. Color Descriptor (colordescriptor.py)

The `ColorDescriptor` class implements the core feature extraction:

- **HSV Color Space**: Converts RGB images to HSV for better human perception alignment
- **Region-Based Analysis**: Divides each image into 5 regions:
  - Top-left corner
  - Top-right corner  
  - Bottom-left corner
  - Bottom-right corner
  - Center elliptical region
- **3D Histogram**: Creates histograms with configurable bins (default: 8×12×3 = 288 features per region)
- **Feature Vector**: Generates 1,440-dimensional feature vector (5 regions × 288 features)

### 2. Image Indexing (index.py)

The indexing process:

1. Loads each image from the dataset
2. Extracts features using ColorDescriptor
3. Stores image filename and feature vector in CSV format
4. Creates searchable index for fast retrieval

### 3. Search Engine (searcher.py)

The search process:

1. Loads the pre-computed index
2. Compares query features with indexed features
3. Uses chi-squared distance for similarity measurement
4. Returns ranked results (most similar first)

### 4. Chi-Squared Distance

The similarity metric formula:
```
d = 0.5 * Σ[(a - b)² / (a + b + ε)]
```

Where:
- `a`, `b`: corresponding histogram bins
- `ε`: small value to prevent division by zero
- Lower values indicate higher similarity

## Configuration

### Histogram Bins

Adjust the number of bins in `ColorDescriptor((H, S, V))`:

```python
# Default configuration
cd = ColorDescriptor((8, 12, 3))  # 288 features per region

# For smaller datasets (fewer bins)
cd = ColorDescriptor((4, 6, 2))   # 48 features per region

# For larger datasets (more bins)
cd = ColorDescriptor((16, 16, 4)) # 1024 features per region
```

### Search Results Limit

Modify the search limit in `searcher.py`:

```python
results = searcher.search(features, limit=20)  # Return top 20 results
```

## Examples

### Beach Photos Search

Query image: Beach scene with blue sky and sand
```bash
python search.py --index index.csv --query queries/beach.png --result-path dataset
```

Expected results: Images with blue sky (upper region) and sandy/brown colors (lower region)

### Sunset Photos Search

Query image: Sunset with orange/red sky
```bash
python search.py --index index.csv --query queries/sunset.png --result-path dataset
```

Expected results: Images with warm colors and similar color distribution

### Architecture Photos Search

Query image: Building or monument
```bash
python search.py --index index.csv --query queries/pyramids.png --result-path dataset
```

Expected results: Architectural images with similar color patterns

## Limitations

### Current Limitations

1. **Color-Only Analysis**: Only considers color distribution, not shapes or objects
2. **Spatial Resolution**: Limited to 5 regions for spatial information
3. **Lighting Sensitivity**: May be affected by different lighting conditions
4. **Content Agnostic**: Cannot distinguish between semantically different objects with similar colors

### Performance Considerations

- **Dataset Size**: Performance degrades with very large datasets (>10,000 images)
- **Memory Usage**: Entire index is loaded into memory during search
- **Indexing Time**: O(n) time complexity for dataset indexing

## Future Improvements

### Planned Enhancements

1. **Web Interface**: Flask/Django web application for easier interaction
2. **Advanced Descriptors**: 
   - Texture features (LBP, Gabor filters)
   - Shape features (Hu moments)
   - SIFT/SURF keypoint descriptors
3. **Machine Learning Integration**:
   - Deep learning features (CNN embeddings)
   - Learned similarity metrics
4. **Performance Optimizations**:
   - Database integration (PostgreSQL, MongoDB)
   - Approximate nearest neighbor search (FAISS, Annoy)
   - Batch processing capabilities
5. **Advanced Features**:
   - Multi-modal search (text + image)
   - Face detection and recognition
   - Object detection integration

### Possible Extensions

```python
# Example: Adding texture features
class TextureDescriptor:
    def describe(self, image):
        # Local Binary Pattern implementation
        # Gabor filter responses
        # etc.
        pass

# Example: Combining multiple descriptors
class CombinedDescriptor:
    def __init__(self):
        self.color_desc = ColorDescriptor((8, 12, 3))
        self.texture_desc = TextureDescriptor()
    
    def describe(self, image):
        color_features = self.color_desc.describe(image)
        texture_features = self.texture_desc.describe(image)
        return color_features + texture_features
```

## Contributing

We welcome contributions! 

**Note**: This is a educational/research project demonstrating CBIR concepts. For production use, consider additional optimizations and error handling.
