# app.py - Amazon Product Recommender Dashboard (Enhanced Version)

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import MaxNLocator

# 🎯 App Title and Description
st.set_page_config(page_title="Amazon Product Recommender", layout="wide")
st.title("🏆 Amazon Product Recommender")
st.markdown(
    """
    A smart product ranking system that helps you find the best deals using scraped data  
    and a **30% price**, **50% rating**, **20% reviews** model.
    """
)

# 📁 Load CSV Safely
try:
    df = pd.read_csv("ranked_products_pt.csv")

    # Convert to numeric and drop invalid rows
    df['price_clean'] = pd.to_numeric(df['price_clean'], errors='coerce')
    df['rating_clean'] = pd.to_numeric(df['rating_clean'], errors='coerce')
    df['reviews_clean'] = pd.to_numeric(df['reviews_clean'], errors='coerce')

    df.dropna(subset=['price_clean', 'rating_clean', 'reviews_clean'], inplace=True)

    if df.empty:
        st.error("❌ No valid product data found in the CSV. Please re-run the ranking script with valid inputs.")
        st.stop()

except FileNotFoundError:
    st.error("❌ File `ranked_products_pt.csv` not found. Please run the ranking script first.")
    st.stop()

# 🔧 Recalculate contributions if needed
WEIGHT_PRICE = 0.3
WEIGHT_RATING = 0.5
WEIGHT_REVIEWS = 0.2

if 'Price' not in df.columns:
    df['price_norm'] = (df['price_clean'].max() - df['price_clean']) / (df['price_clean'].max() - df['price_clean'].min())
    df['rating_norm'] = (df['rating_clean'] - df['rating_clean'].min()) / (
                df['rating_clean'].max() - df['rating_clean'].min())
    df['reviews_norm'] = (df['reviews_clean'] - df['reviews_clean'].min()) / (
                df['reviews_clean'].max() - df['reviews_clean'].min())

    df['Price'] = df['price_norm'] * WEIGHT_PRICE
    df['Rating'] = df['rating_norm'] * WEIGHT_RATING
    df['Reviews'] = df['reviews_norm'] * WEIGHT_REVIEWS
    df['score'] = df['Price'] + df['Rating'] + df['Reviews']
    df.sort_values('score', ascending=False, inplace=True)

# 🛠️ Sidebar Filters
with st.sidebar:
    st.header("🔍 Filter Products")
    st.markdown("Adjust filters to narrow down your search.")

    # Handle max price fallback
    default_max_price = int(df['price_clean'].max()) if not df['price_clean'].isnull().all() else 500
    default_mean_price = int(df['price_clean'].mean()) if not df['price_clean'].isnull().all() else default_max_price // 2

    max_price = st.slider("💰 Max Price ($)", 0, default_max_price, default_mean_price)
    min_rating = st.slider("⭐ Min Rating", 1.0, 5.0, 4.0, step=0.1)
    st.markdown("---")
    st.markdown("📊 Adjust weights in code for different priorities.")

# 🔍 Apply Filters
filtered_df = df[(df['price_clean'] <= max_price) & (df['rating_clean'] >= min_rating)]

# 📋 Top Products Table with Styling
st.header("🎯 Top Ranked Products")
if not filtered_df.empty:
    display_df = filtered_df[['title', 'price_clean', 'rating_clean', 'reviews_clean', 'score']]
    display_df = display_df.rename(columns={
        "title": "Product",
        "price_clean": "Price ($)",
        "rating_clean": "Rating ★",
        "reviews_clean": "Reviews",
        "score": "Score"
    })

    # Style DataFrame for better visuals
    styled_df = display_df.style.background_gradient(cmap='Blues', subset=['Score']) \
                                .background_gradient(cmap='Greens', subset=['Rating ★']) \
                                .background_gradient(cmap='Oranges', subset=['Price ($)']) \
                                .format({'Price ($)': '${:.2f}', 'Score': '{:.3f}'})
    
    st.dataframe(styled_df, use_container_width=True)
else:
    st.warning("🚫 No products match your current filters.")

# 📊 Stacked Bar Chart: Feature Contribution
st.header("🧩 How Each Product Scores")
if not filtered_df.empty:
    contribution_data = filtered_df.set_index('title')[['Price', 'Rating', 'Reviews']]
    st.bar_chart(contribution_data)
else:
    st.warning("No data to show here yet.")

# 📈 Price vs Reviews Scatter Plot
st.header("📉 Price vs Popularity")
if not filtered_df.empty:
    fig, ax = plt.subplots(figsize=(10, 6))
    scatter = sns.scatterplot(
        data=filtered_df,
        x='price_clean',
        y='reviews_clean',
        size='score',
        hue='rating_clean',
        alpha=0.7,
        sizes=(20, 200),
        palette='viridis',
        ax=ax
    )
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))

    plt.title("Price vs Review Count | Color = Rating | Size = Score")
    plt.xlabel("Price ($)")
    plt.ylabel("Number of Reviews")
    plt.tight_layout()
    st.pyplot(fig)
else:
    st.warning("No data to visualize.")

# 🧾 Raw Data Section
with st.expander("📁 View Full Dataset"):
    st.markdown("This is the full dataset used to generate recommendations:")
    st.dataframe(df[['title', 'price_clean', 'rating_clean', 'reviews_clean', 'score']].head(20).style.format({
        'price_clean': '${:.2f}',
        'score': '{:.3f}'
    }))