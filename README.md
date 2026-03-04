# 🛍️ ASOS E-Commerce Data Analytics: Uncovering "Phantom Revenue"

## 📖 Project Overview
This project is an end-to-end data analytics audit of a real-world e-commerce dataset scraped from ASOS. The goal of this analysis is to act as a "Data Detective," looking beyond basic sales metrics to identify operational bottlenecks—specifically, how much potential revenue the company is losing daily due to high-demand items being out of stock.

By cleaning and analyzing over 18,000 product listings, this project calculates the "Phantom Revenue" (missed sales opportunities) and delivers a clear, data-driven inventory strategy using a visual quadrant analysis.

## 🎯 The Business Problem
In e-commerce, an "Out of Stock" badge doesn't just mean a product is popular; it means the business is actively losing money from willing buyers. 
* **The Question:** Which specific brands and price points are losing the company the most money due to poor inventory management?
* **The Solution:** Quantify the missed revenue and group brands into strategic categories so the purchasing team knows exactly what to restock first to maximize profit.

## 🛠️ Tech Stack & Tools
* **Language:** Python
* **Data Manipulation:** `pandas` (for data cleaning, string extraction, and aggregation)
* **Data Visualization:** `matplotlib` & `seaborn` (for building the modern, strategic scatter plot matrix)

## 🔍 Methodology (Step-by-Step)
1. **Data Ingestion & Cleaning:** * Loaded a messy, real-world CSV file of ASOS products, handling bad data lines and forcing the `price` column into a clean numeric format.
2. **Feature Engineering (Text Parsing):**
   * The dataset lacked a dedicated "Brand" column. Used Python text-splitting techniques to extract brand names (e.g., Topshop, Mango) hidden within the product `description` strings.
3. **Calculating "Phantom Revenue":**
   * Parsed the `size` column to calculate the exact **Stockout Rate** (percentage of sizes currently unavailable for a single item).
   * Created a new metric: **Lost Revenue** = `Item Price` × `Number of Out-of-Stock Sizes`.
4. **Strategic Aggregation:**
   * Grouped the raw product data by brand to find the average price, average stockout rate, and total lost revenue for each brand.
5. **Data Visualization (Quadrant Analysis):**
   * Built a customized, multi-dimensional Bubble Chart using Seaborn to visualize the relationship between Price, Demand (Stockout Rate), and Financial Impact (Bubble Size).

## 📈 Key Insights & Recommendations
The final output is a strategic quadrant chart that divides the brands into four actionable categories:

* 🏆 **The Winners (Top-Right):** Brands like *Mango* and *Topshop* command premium prices (> £40) but suffer from massive stockout rates (> 40%). **Recommendation:** Immediately reallocate budget to secure more inventory for these specific brands. They are the biggest source of phantom revenue.
* 🛑 **The Money Pits (Bottom-Right):** High-priced items that rarely sell out. **Recommendation:** Liquidate this inventory and stop over-ordering.
* 👕 **Everyday Essentials (Top-Left):** Cheaper items with high demand. **Recommendation:** Maintain a steady, automated supply chain for these traffic-drivers.
* 📉 **Dead Weight (Bottom-Left):** Low price, low demand. **Recommendation:** Phase these items out to save warehouse space.

---

## 🚀 How to Run This Project (Step-by-Step)

### 1. Prerequisites
You need to have **Python** installed on your computer. 
* If you don't have it, download it from [python.org](https://www.python.org/downloads/). 
* *Crucial Step for Windows Users:* During the installation process, make sure to check the box that says **"Add Python to PATH"** before clicking install.

### 2. Set Up Your Project Folder
* Create a new folder on your computer and name it something like `asos-data-project`.
* Copy the Python code from this repository and save it as a file named `asos_analysis.py` inside that folder.
* Download the `products.csv` dataset and place it in the **exact same folder** as your Python script.

### 3. Install Required Libraries
You need to install the data science toolkits used in this code. 
* Open your computer's **Terminal** (Mac) or **Command Prompt** (Windows).
* Run the following command and press Enter:
  ```bash
  pip install pandas matplotlib seaborn