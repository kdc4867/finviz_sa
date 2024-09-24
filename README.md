# FinViz Sentiment Analysis for Financial Markets

## Overview

This project implements an automated system for sentiment analysis of financial news headlines, leveraging the power of OpenAI's GPT models. By scraping daily news from FinViz and applying advanced NLP techniques, we generate valuable insights for financial market analysis and investment strategy evaluation.

## Key Features

- **Automated News Scraping**: Daily collection of financial headlines from FinViz.
- **AI-Powered Sentiment Analysis**: Utilization of OpenAI's GPT for nuanced sentiment classification.
- **Daily Market Summaries**: Generation of comprehensive daily market sentiment reports.
- **Investment Strategy Evaluation**: Analysis of potential trading strategies based on sentiment data.
- **Continuous Integration**: Automated daily runs via GitHub Actions for consistent data updates.

## Technical Architecture

```
finviz_sa/
├── data/
│   ├── finviz_sentiment_analysis_results.csv
│   ├── stock_prices.csv
│   └── summaries/
│       └── summary_YYYY-MM-DD.txt
├── src/
│   ├── data_loader.py
│   ├── sentiment_analysis.py
│   ├── scraper.py
│   ├── strategy_evaluation.py
│   └── analysis.py
├── .github/workflows/
│   └── scraper.yml
├── main.py
├── requirements.txt
└── README.md
```

## Installation and Setup

1. Clone the repository:
   ```
   git clone https://github.com/kdc4867/finviz_sa.git
   cd finviz_sa
   ```

2. Set up a virtual environment (recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   - Create a `.env` file in the root directory.
   - Add: `OPENAI_API_KEY=your_api_key_here`

## Usage

Execute the main script to run the entire pipeline:

```
python main.py
```

This will:
1. Scrape the latest financial news from FinViz.
2. Perform sentiment analysis on new headlines.
3. Update the sentiment analysis results in `data/finviz_sentiment_analysis_results.csv`.
4. Generate a daily summary in `data/summaries/`.
5. Evaluate investment strategies based on the latest sentiment data.

## Continuous Integration

This project utilizes GitHub Actions for daily automated runs. The workflow is defined in `.github/workflows/scraper.yml`.

To set up GitHub Actions:
1. Navigate to your GitHub repository settings.
2. Go to Secrets and Variables > Actions.
3. Add the following repository secrets:
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `PAT`: A Personal Access Token with repo scope for GitHub Actions

## Data Analysis and Visualization

For detailed analysis of the sentiment data and its correlation with market movements, refer to the Jupyter notebooks in the `analysis/` directory (if available).

## Contributing

Contributions to improve the project are welcome. Please follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This project is for educational and research purposes only. The financial insights generated should not be considered as investment advice. Always consult with a qualified financial advisor before making investment decisions.