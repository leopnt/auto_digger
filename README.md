# Auto Digger

## Overview

Auto Digger is a Python-based project designed for the extraction and analysis of audio features from tracks. It utilizes various libraries, including Librosa for audio analysis and processing, and machine learning techniques for feature extraction and similarity analysis. The project aims to provide a comprehensive toolset for audio data scientists and engineers to analyze and understand characteristics of audio tracks.

## Installation

### Prerequisites

- Python 3.x
- Librosa
- Numpy
- Pandas
- Scikit-learn
- Matplotlib
- Seaborn

### Steps

1. Clone the repository:
   ```bash
   git clone [repository-url]
   ```
2. Install dependencies:
   ```bash
   pip install librosa numpy pandas scikit-learn matplotlib seaborn
   ```

## Usage

### Feature Extraction

- `track_feature_extraction.py`: Extracts various features from an audio file, such as tempo, root mean square energy, spectral features, and Mel-frequency cepstral coefficients (MFCCs).

  ```bash
  python track_feature_extraction.py [path-to-audio-file]
  ```

### Data Parsing

- `parse_discogs_data.py`: Parses XML data, particularly focusing on exploring or counting elements in large XML files, like those from Discogs.

  ```bash
  python parse_discogs_data.py [path-to-xml-file] [num-elements]
  ```

### Similarity Analysis

- `most_similar.py`: Finds the most similar tracks based on their feature vectors.

  ```bash
  python most_similar.py [path-to-audio-file]
  ```

### Feature Exploration

- `explore_features.py`: Provides tools for visualizing correlations and principal component analysis (PCA) of audio features.

### Dataset Building

- `build_dataset.py`: Builds a dataset from a list of audio tracks for further analysis.

## Contributing

Contributions to Auto Digger are welcome! If you have suggestions or improvements, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add some feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Create a new Pull Request.

> Note: This project is using the Black formatter for Python

## License

## Contact
