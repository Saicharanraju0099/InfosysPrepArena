# ==========================================
# STEP 1: Import Necessary Tools (Libraries)
# ==========================================
# Libraries are like toolboxes that contain pre-written code we can use.
import pandas as pd            # 'pandas' is the ultimate tool for working with data tables.
import matplotlib.pyplot as plt # 'matplotlib' helps with the underlying structure of our charts.
import seaborn as sns          # 'seaborn' is our upgrade tool to make charts look modern and professional.

# ==========================================
# STEP 2: Load the Data
# ==========================================
# We load our CSV (Comma Separated Values) file into a pandas "DataFrame" (df).
# on_bad_lines='skip' tells Python to skip any broken or messy rows instead of crashing.
df = pd.read_csv('/Users/saicharan/DATA ANALYST /DATASET/products_asos.csv', on_bad_lines='skip')

# ==========================================
# STEP 3: Clean the Data (Focusing on 'price')
# ==========================================
# To calculate revenue, we need the 'price' column to be actual numbers, not text.
# errors='coerce' turns text like 'Free' or '$' into a blank value (NaN).
df['price'] = pd.to_numeric(df['price'], errors='coerce')

# Drop (delete) any rows where the price is blank (NaN). We can't analyze revenue without a price!
df.dropna(subset=['price'], inplace=True)

# Print out how many rows of data we successfully loaded and cleaned.
print(f"Data loaded successfully: {len(df)} rows")


# ==========================================
# STEP 4: Extract the 'Brand' from the Description
# ==========================================
# The brand name is hidden inside the 'description' column (e.g., "Jacket by Topshop").
# First, ensure the description column is treated as text (strings).
df['description'] = df['description'].astype(str)

def get_brand(text):
    """
    Looks at a sentence, finds the word 'by ', and grabs the first word immediately after it.
    """
    try:
        if 'by ' in text:
            return text.split('by ')[1].split(' ')[0]
        else:
            return 'unknown'
    except:
        return 'unknown'

# Apply our custom function to every row to create a new 'brand_row' column.
df['brand_row'] = df['description'].apply(get_brand)

# Map partial names to their correct full brand names using a dictionary.
brand_map = {
    'New': 'New Look',
    'River': 'River Island',
    'Miss': 'Miss Selfridge',
    'Topshop': 'Topshop'
}
df['brand'] = df['brand_row'].map(brand_map).fillna(df['brand_row'])

# Only keep brands that have a meaningful amount of products (more than 5).
brand_counts = df['brand'].value_counts()
valid_brands = brand_counts[brand_counts > 5].index

# Create a clean table (df_clean) with only our valid brands.
df_clean = df[df['brand'].isin(valid_brands)].copy()


# ==========================================
# STEP 5: Analyze "Stockouts" (Missed Sales)
# ==========================================
# The 'size' column contains text like "UK 6, UK 8, Out of stock, UK 10".

def calculate_phantom_revenue(size_str):
    """
    Counts how many sizes exist for an item, and how many specifically say 'Out of stock'.
    Returns the count of out-of-stock sizes, and the percentage (rate).
    """
    if not isinstance(size_str, str):
        return 0, 0
    
    sizes = size_str.split(',')
    total_sizes = len(sizes)
    
    out_of_stock_count = size_str.count('Out of stock')
    rate = out_of_stock_count / total_sizes if total_sizes > 0 else 0
    
    return out_of_stock_count, rate

# Apply the function to our sizes.
matrix = df_clean['size'].apply(lambda x: calculate_phantom_revenue(x))

# Split the results into two separate columns.
df_clean['stockout_count'] = [x[0] for x in matrix]
df_clean['stockout_rate'] = [x[1] for x in matrix]

# Calculate exactly how much money we are losing!
# Lost Revenue = (Price of the item) multiplied by (How many sizes are out of stock)
df_clean['lost_revenue'] = df_clean['price'] * df_clean['stockout_count']


# ==========================================
# STEP 6: Group Data by Brand (The Big Picture)
# ==========================================
# Group everything together by Brand to see overall strategy metrics.
brand_strategic = df_clean.groupby('brand').agg({
    'price': 'mean',           # Average price for the brand
    'stockout_rate': 'mean',   # Average stockout rate
    'lost_revenue': 'sum',     # Total lost revenue for this brand
    'name': 'count'            # Total products listed by this brand
})

# Filter out very small brands (keep only those with more than 10 products).
brand_strategic = brand_strategic[brand_strategic['name'] > 10]


# ==========================================
# STEP 7: Visualize the Strategy
# ==========================================
# 1. Set a clean, modern theme with a subtle grid background
sns.set_theme(style="whitegrid")

# 2. Set the canvas size (12 inches wide, 8 inches tall)
plt.figure(figsize=(12, 8))

# 3. Draw the Bubble Chart using Seaborn
sns.scatterplot(
    data=brand_strategic,
    x='price',
    y='stockout_rate',
    size='lost_revenue',   # Bubble size represents the lost revenue
    sizes=(50, 800),       # Minimum and maximum size of the bubbles
    alpha=0.7,             # Makes bubbles slightly transparent so overlapping dots are visible
    color='#2C3E50',       # A sleek, professional dark blue color
    legend=False           # Hides the legend for a cleaner look
)

# 4. Identify the "Winners" (VIP List: High price > 40 AND High stockout rate > 0.4)
winners = brand_strategic[(brand_strategic['price'] > 40) & (brand_strategic['stockout_rate'] > 0.4)]

# 5. Add the brand names next to the winning bubbles ONLY
for brand in winners.index:
    plt.text(
        x=winners.loc[brand, 'price'] + 1.5,   # Shift text right so it doesn't cover the bubble
        y=winners.loc[brand, 'stockout_rate'], 
        s=brand,
        fontsize=10,
        fontweight='bold',
        color='#C0392B'  # Dark red text to make the winners stand out
    )

# 6. Add the Quadrant Lines to divide the chart into 4 strategic zones
plt.axvline(x=40, color='#E74C3C', linestyle='--', alpha=0.5)
plt.axhline(y=0.4, color='#E74C3C', linestyle='--', alpha=0.5)

# 7. Add professional titles and labels
plt.title('ASOS Brand Strategy: High-Value Restock Targets', fontsize=16, fontweight='bold', pad=15)
plt.xlabel('Average Item Price (£)', fontsize=12, fontweight='bold')
plt.ylabel('Demand (Stockout Rate %)', fontsize=12, fontweight='bold')

# 8. Show the masterpiece!
plt.show()