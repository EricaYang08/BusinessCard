# Business Card Text Extraction and Field Classification

This project implements a full pipeline to extract text from scanned business card images, classify each extracted line into structured fields (such as Name, Phone, Email, Address, Company, etc.), and output organized results.

The system combines **OpenCV**, **Pytesseract OCR**, **PyTorch** classifier, and **rule-based post-processing** to handle real-world noisy business card images, achieving approximately **80% field extraction accuracy**.

---

## Project Structure

- business_card.zip: Example business card images.
- Business_Card_Scanner_Algorithm.ipynb: Jupyter Notebook with all code steps.
- README.md: Project documentation.

---

## Key Features

- **Text Extraction**: OpenCV + Pytesseract OCR to extract raw text from images.
- **Initial Line Classification**: PyTorch model trained on synthetic data.
- **Rule-Based Backup**: Handcrafted rules to supplement model predictions for higher robustness.
- **Post-Processing**:
  - Smart splitting of Phone and Fax numbers from messy lines.
  - Preserving leftover useful text into other category.
  - Safeguarding against information loss.
- **Structured Output**: Fields grouped into Name, Phone, Email, Address, Company, Title, Website, Other.

---

## Technologies Used

- Python 3
- OpenCV
- Pytesseract
- PyTorch
- Faker (for synthetic data generation)
- Regular Expressions (Regex)

---

## Pipeline Overview

1. **Image Preprocessing**:
   - Load and scan business card images
   - Convert to RGB format
2. **OCR Extraction**:
   - Use Pytesseract to detect text lines
3. **Dataset Preparation**:
   - Generate synthetic training data with Faker
   - Build vocabulary for tokenization
4. **Model Training**:
   - Train a small PyTorch model to predict field categories
5. **Prediction and Correction**:
   - Predict using model
   - Apply rule-based corrections
   - Post-process for Phone and Fax splitting
6. **Grouping and Output**:
   - Group lines into structured field

---

## Example Output

      Business Card: /content/business_card_folder/business_card/002.jpg
      Name: MEXICAN GRILL | CHRIS SALCEDO
      Address: 2675 EL CAMINO REAL
      Phone: 650.462.9154
      Other: APPRENTICE | CHIPOTLE MEXICAN GRILL, I! | PALO ALTO, CA 94306
