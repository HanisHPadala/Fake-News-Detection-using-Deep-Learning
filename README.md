# Fake-News-Detection-using-Deep-Learning

This project is a machine learning model for detecting fake news articles. Using a Long Short-Term Memory (LSTM) neural network trained on labeled datasets of fake and real news, this model can classify manually entered news text as "REAL" or "FAKE."

## Project Structure
- `fake news detection.py`: Script for training the model on labeled news datasets.
- `model loading and prediction.py`: Script for making predictions on manually entered news text.
- `fake_news_detection_model.keras`: The trained model saved in the Keras native format.

## Requirements
- Python 3.x
- Libraries:
  - `tensorflow`
  - `pandas`
  - `numpy`
  - `nltk`
  - `scikit-learn`

You can install all required packages with:
```bash
pip install tensorflow pandas numpy nltk scikit-learn ```

##Data Preparation
-The model is trained using two datasets:

-True News Dataset (true.csv)
-Fake News Dataset (fake.csv)
-Each dataset contains news text labeled as either 1 (real) or 0 (fake). These datasets should be in CSV format with a text column containing the article text.
