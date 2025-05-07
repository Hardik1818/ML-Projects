# 🛒 Amazon Product Recommendation System

An intelligent recommendation system that ranks Amazon products using a weighted score based on **price**, **rating**, and **number of reviews**. Built using **Python** and **Streamlit**, this tool helps users find the best products based on custom filters and real-time insights.

---

## 📌 Project Overview

This dashboard processes scraped product data from Amazon and ranks products using a scoring model:
- **30% Price**
- **50% Rating**
- **20% Reviews**

Users can filter the product list based on max price and minimum rating, and visualize how each product's features contribute to its overall ranking.

---

## 🎯 Features

- ✅ Interactive Streamlit web app
- ✅ Filters for price and rating
- ✅ Ranking based on custom weighted scoring
- ✅ Stacked bar chart to visualize feature contributions
- ✅ Scatter plot to view relationship between price, reviews, and ratings
- ✅ CSV-based data ingestion for scalability

---

## 🧠 Learnings & Concepts Applied

- Feature Engineering: Normalization, scoring metrics
- Data Cleaning: Handling missing and inconsistent values
- Data Visualization: Seaborn & Matplotlib
- Web Scraping: Custom headers for bot avoidance
- Streamlit: Building intuitive, interactive dashboards

---

## ⚙️ Project Workflow

1. **Data Collection**: Scraped product data using `requests` + `BeautifulSoup`
2. **Data Cleaning**: Handled missing, inconsistent, and dirty values
3. **Feature Normalization**: Scaled price, rating, and review values
4. **Scoring**: Applied weighted formula to rank products
5. **Frontend**: Created interactive UI using Streamlit
6. **Visualization**: Used bar and scatter plots to illustrate rankings and patterns

---

## 🛠️ Technologies Used

- Python 3.x  
- Streamlit  
- Pandas, NumPy  
- Matplotlib, Seaborn  
- BeautifulSoup (for scraping)

---

## ⚠️ Challenges Faced

- **Scraping Issues**: Required headers (User-Agent) to avoid being blocked by Amazon
- **Data Cleaning**: Several entries had missing or malformed price/review/rating values
- **Balancing Weights**: Fine-tuned the scoring formula to produce fair and meaningful results

---

## 📁 File Structure

├── app.py # Main Streamlit dashboard <br>
├── ranked_products_pt.csv # Input CSV containing scraped product data <br>
├── requirements.txt # Project dependencies <br>
├── README.md # This documentation



