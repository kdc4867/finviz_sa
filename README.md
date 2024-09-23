# Stock Analysis Project

This project analyzes stock prices based on sentiment analysis of news headlines. It uses OpenAI's GPT for sentiment analysis and evaluates investment strategies.

## Directory Structure
```sh
stock_analysis_project/
│
├── data/
│ ├── stock_prices.csv
│ ├── finviz_sentiment_analysis_results.csv
│
├── models/
│ ├── trained_model.joblib
│ ├── company_encoder.joblib
│
├── src/
│ ├── init.py
│ ├── data_loader.py
│ ├── sentiment_analysis.py
│ ├── scraper.py
│ ├── strategy_evaluation.py
│
├── colab_notebooks/
│ ├── model_training.ipynb
│
├── main.py
├── requirements.txt
├── README.md


## Setup

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/stock_analysis_project.git
    cd stock_analysis_project
    ```

2. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```

3. Run the main script:
    ```sh
    python main.py
    ```

## Model Training

Train the model using the Colab notebook in `colab_notebooks/model_training.ipynb`. Save the trained model to the `models` directory.

## Usage

1. Scrape news headlines and analyze sentiment using OpenAI's API.
2. Merge sentiment analysis results with stock price data.
3. Evaluate investment strategies based on sentiment analysis.

## License

This project is licensed under the MIT License.
