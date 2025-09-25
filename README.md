# Arabic OCR (كلمتي) - Arabic Handwritten Text Recognition

A deep learning-based system for recognizing handwritten Arabic text using Convolutional Neural Networks (CNN), Bidirectional LSTM, attention mechanisms, and CTC loss. This project provides both a trained model and a user-friendly PyQt6 interface for real-time Arabic handwriting recognition.

## 🎯 Project Overview

This project was developed as part of the Deep Learning course at École d'Ingénierie Digitale et d'Intelligence Artificielle (EIDIA), Euro Mediterranean University of Fez. The system achieves **96.32% character accuracy** and **79.98% word accuracy** on the IFN/ENIT dataset.

### Key Features
- Arabic handwritten text recognition
- Real-time inference with GUI application
- Multiple decoding methods (Greedy and Beam Search)
- Pre-trained model ready for deployment
- Comprehensive preprocessing pipeline

## 🏗️ Architecture

The model combines several state-of-the-art techniques:

1. **Feature Extraction**: Pre-trained ResNet50 (ImageNet) for visual feature extraction
2. **Sequential Processing**: Bidirectional LSTM layers for temporal dependencies
3. **Attention Mechanism**: Self-attention for enhanced context modeling
4. **Output Alignment**: CTC loss for sequence alignment without explicit character-level annotation

### Model Pipeline
```
Input Image (100x300) → ResNet50 → BiLSTM → Attention → CTC → Arabic Text
```

## 📊 Dataset

**IFN/ENIT Database**: A specialized dataset for Arabic handwritten text recognition
- **Size**: 26,000+ handwritten words from 411 different authors
- **Content**: Tunisian city names in Arabic
- **Splits**: 
  - Training: Sets A, B, C (23,301 images after augmentation)
  - Validation: Subset of training data (1,044 images)
  - Testing: Set D
- **Augmentation**: Applied geometric transformations, brightness/contrast adjustments, and noise addition

## 🚀 Getting Started

### Prerequisites
**Option 1: Using pip (Recommended)**
```bash
pip install -r requirements.txt
```

**Option 2: Using conda**
```bash
conda env create -f environment.yml
conda activate arabic-ocr
```

### Quick Start

1. **Clone the repository**
```bash
git clone <repository-url>
cd ARABIC_OCR_INTERFACE
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the GUI Application**
```bash
python main.py
```

3. **Using the Interface**
   - Click "تحميل صورة" (Upload Image) to select an Arabic handwritten image
   - View results from both Greedy and Beam Search decoding methods
   - Click "الرجوع إلى الشاشة الرئيسية" (Return to Main Screen) to try another image

### Programmatic Usage

```python
from inference import infer_image
from inference_bm import infer_image2

# Greedy decoding
result_greedy = infer_image('path/to/your/image.jpg')
print(f"Greedy result: {result_greedy}")

# Beam search decoding
result_beam = infer_image2('path/to/your/image.jpg', method='beam', beam_width=30)
print(f"Beam search result: {result_beam}")
```

## 📁 Project Structure

```
ARABIC_OCR_INTERFACE/
├── main.py                    # Main application entry point
├── first_screen.py           # Home screen GUI component
├── second_screen.py          # Results display GUI component
├── inference.py              # Greedy decoding inference
├── inference_bm.py           # Beam search decoding inference
├── ocr_model.keras          # Pre-trained model (96MB)
├── char_code_files/         # Character encoding mappings
│   ├── chars_to_codes.json  # Character to code mapping
│   └── codes_to_chars.json  # Code to character mapping
├── set_a_images/            # Sample training images
├── set_d_images/            # Sample test images
├── OCR_PROJECT_NOTEBOOK.ipynb  # Complete training notebook
```

## 🔧 Technical Details

### Model Specifications
- **Input Size**: 100×300 grayscale images
- **Architecture**: ResNet50 + 2×BiLSTM(512,256) + Attention + CTC
- **Output Classes**: 120 (Arabic characters + blank token)
- **Training**: 34 epochs with adaptive learning rate
- **Loss Function**: CTC (Connectionist Temporal Classification)

### Preprocessing Pipeline
1. Grayscale conversion
2. Resize to 100×300 pixels
3. Binary thresholding
4. Color inversion (text appears white on black background)
5. Normalization to [0,1] range

### Character Encoding
The system uses a specialized encoding for Arabic characters considering their contextual forms:
- **Position-aware encoding**: Characters encoded based on position (beginning, middle, end, isolated)
- **120 unique tokens**: Covering all Arabic character variations plus blank token
- **Example**: `kaB` → `قـ` (Arabic letter Qaf at beginning of word)

### Decoding Methods

1. **Greedy Decoding**: Selects most probable character at each time step
2. **Beam Search**: Explores multiple hypotheses with configurable beam width (default: 30)

## 📈 Performance Metrics

| Metric | Greedy Decoding | Beam Search (width=20) |
|--------|----------------|------------------------|
| **Character Accuracy Rate (CAR)** | 96.46% | 96.33% |
| **Word Accuracy Rate (WAR)** | 79.31% | 79.98% |

### Training Curves
The model was trained in multiple phases:
- **Phase 1**: Full model training (epochs 1-16)
- **Phase 2**: Fine-tuning last 30 layers (epochs 17-26)
- **Phase 3**: Fine-tuning last 50 layers (epochs 27-34)

## 🎨 GUI Features

- **Modern Arabic Interface**: RTL support with Arabic text
- **Dual Decoding Display**: Shows results from both decoding methods
- **Image Preview**: Displays uploaded image with proper scaling
- **Intuitive Navigation**: Simple two-screen interface

## 🧪 Evaluation

### Test Environment
- **Hardware**: Google Colab (A100 GPU) and RTX 4070 Laptop GPU
- **Training Time**: ~5 hours for complete training
- **Inference Speed**: Real-time processing for single images

### Dataset Split
- **Training**: Sets A, B, C (90% for training, 10% for validation)
- **Testing**: Set D (independent evaluation)
- **Data Cleaning**: Removed samples with annotation errors (e.g., chadda issues, transcription errors)

## 🔄 Data Augmentation

Applied to increase robustness and dataset size (10,435 → 25,887 images):
- **Geometric**: Rotation (±3°), shearing
- **Photometric**: Brightness/contrast adjustment
- **Noise**: Gaussian noise, motion blur
- **Random Application**: 0-3 augmentations per image

## 📚 References

This project builds upon:
- ResNet architecture for feature extraction
- CTC loss for sequence alignment
- Bidirectional LSTM for sequence modeling
- Attention mechanisms for enhanced context

## 👥 Contributors

**Students:**
- Wiame Adnane
- Abderrahmane Najib
- Manar Kaddouri  
- Zakaria Andour

**Supervisor:** Prof. AMMOUR Alae

## 📄 License

This project was developed as part of academic coursework at UEMF-EIDIA.

## 🔮 Future Improvements

- **Dataset Expansion**: Include more diverse handwriting styles and text types
- **Character-level Attention**: Implement character-level attention visualization
- **Mobile Deployment**: Optimize model for mobile inference
- **Multi-language Support**: Extend to other Arabic dialects and languages
- **Real-time Video OCR**: Process video streams for continuous text recognition

