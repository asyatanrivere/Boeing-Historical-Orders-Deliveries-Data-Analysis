# -------------------------------
# Boeing Orders & Deliveries Analysis
# -------------------------------

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
import os

# CONFIG
# -------------------------------
DATA_PATH="dataset/OrdersandDeliveries.csv"
OUTPUT_DIR="images"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# LOAD DATA
# -------------------------------
def load_data(path):
    df=pd.read_csv(path)
    df.columns=df.columns.str.strip()
    return df

# INSPECT DATA
# -------------------------------
def inspect_data(df):
    print("\n--- HEAD ---")
    print(df.head(10))

    print("\n--- TAIL ---")
    print(df.tail(10))

    print("\n--- INFO ---")
    print(df.info())

    print("\n--- DESCRIBE ---")
    print(df.describe())

    print("\n--- DUPLICATES ---")
    print(df.duplicated().sum())

    print("\n--- MISSING VALUES ---")
    print(df.isnull().sum())

# CLEAN DATA
# -------------------------------
def clean_data(df):
    df = df.copy()

    df = df[df["Country"] != "All"]

    # Drop missing values
    df = df.dropna(subset=["Delivery Year"])
    df = df.dropna(subset=["Region"])

    # Drop unnecessary column
    df.drop(columns=["Unfilled Orders"], inplace=True)

    # Type conversions
    df["Delivery Year"] = df["Delivery Year"].astype(int)
    df["Order Year"] = df["Order Year"].astype(int)
    df["Order Total"] = df["Order Total"].astype(int)
    df["Delivery Total"] = df["Delivery Total"].astype(int)

    return df

# MONTHLY ANALYSIS
# -------------------------------
def monthly_orders_analysis(df):
    monthly_order = df["Order Month"].value_counts()

    sb.barplot(
        x=monthly_order.index,
        y=monthly_order.values,
        order=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    )
    plt.title("Orders by Month")
    plt.xlabel("Months")
    plt.ylabel("Number of Orders")
    plt.grid()
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/monthly_order.png")
    plt.show()

# YEARLY ANALYSIS
# -------------------------------
def yearly_orders_analysis(df):
    yearly = df["Order Year"].value_counts()

    sb.lineplot(x=yearly.index, y=yearly.values)
    plt.title("Orders by Year")
    plt.xlabel("Years")
    plt.ylabel("Number of Orders")
    plt.grid()
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/yearly_order.png")
    plt.show()

# COUNTRY ANALYSIS
# -------------------------------
def country_analysis(df):
    most_countries = df["Country"].value_counts().sort_values(ascending=False).head(10)

    sb.barplot(x=most_countries.index, y=most_countries.values)
    plt.title("Orders by Countries")
    plt.xlabel("Countries")
    plt.ylabel("Number of Orders")
    plt.xticks(rotation=45, ha="right")
    plt.grid()
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/order_by_countries.png")
    plt.show()

# CORRELATION ANALYSIS
# -------------------------------
def correlation_analysis(df):
    corr = df.corr(numeric_only=True)

    plt.figure(figsize=(8,8))
    sb.heatmap(data=corr, annot=True, cmap='RdYlBu', linewidths=0.5)
    plt.xticks(rotation=45, ha="right")
    plt.yticks(rotation=45, ha="right")
    plt.title("Correlation of Boeing Order Dataset")
    plt.savefig(f"{OUTPUT_DIR}/correlation_heatmap.png")
    plt.show()

# MODEL ANALYSIS
# -------------------------------
def model_analysis(df):
    models = df["Model Series"].value_counts().sort_values(ascending=False).head(10)

    sb.barplot(x=models.index, y=models.values)
    plt.title("Top 10 Orders by Model Series")
    plt.xlabel("Model Series")
    plt.ylabel("Number of Orders")
    plt.xticks(rotation=45, ha="right")
    plt.grid()
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/orders_by_modelseries.png")
    plt.show()

#REGION ANALYSIS
# -------------------------------
def region_analysis(df):
    regions = df["Region"].value_counts().sort_values(ascending=False)

    sb.barplot(y=regions.index, x=regions.values)

    plt.title("Number of Orders by Regions")
    plt.ylabel("Regions")
    plt.xlabel("Number of Orders")
    plt.grid(axis="x")
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/orders_by_regions.png")
    plt.show()


# ENGINE ANALYSIS
# -------------------------------
def engine_analysis(df):
    engines = df["Engine"].value_counts()

    sb.barplot(x=engines.index, y=engines.values)

    plt.title("Number of Engines")
    plt.xlabel("Engines")
    plt.grid()
    plt.tight_layout()
    plt.show()


# TOTAL ORDERS BY COUNTRIES (TOP 10)
# -------------------------------
def total_orders_by_countries_Anaylsis(df):
    
    totalorders_by_countries=df.groupby("Country")["Order Total"].sum().sort_values(ascending=False).head(10)
    sb.barplot(y=totalorders_by_countries.index, x=totalorders_by_countries.values)

    plt.title("Total Orders by Countries (TOP 10)")
    plt.ylabel("Total Orders")
    plt.xlabel("Countries")
    plt.grid()
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/total_orders_by_countries.png")
    plt.show()

# TOTAL ORDERS BY US AIRLINES TOP 20
# -------------------------------
def total_orders_by_US_Airlines_Analysis(df):
    df_USA=df[df["Country"]=="USA"]
    total_orders_by_US_Airlines=df_USA.groupby("Customer Name")["Order Total"].sum().sort_values(ascending=False).head(20)
    sb.barplot(y=total_orders_by_US_Airlines.index, x=total_orders_by_US_Airlines.values)
    plt.title("Total Orders by USA Airlines TOP 20")
    plt.ylabel("USA Airlines")
    plt.xlabel("Total Order")
    plt.grid()
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/total_orders_by_US_Airlines.png")
    plt.show()

# TOTAL ORDERS BY ENGINE
# -------------------------------
def total_orders_by_Engine_Analysis(df):
    total_orders_by_engine=df.groupby(["Engine","Order Year"])["Order Total"].sum().reset_index(name="count")
    sb.lineplot(data=total_orders_by_engine,y="count", x="Order Year",hue="Engine")
    plt.title("Total Orders by Engine")
    plt.ylabel("Total Order of That Year")
    plt.xlabel("Years")
    plt.grid()
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/total_orders_by_engine.png")
    plt.show()


# MAIN PIPELINE
# -------------------------------
def main():
    df = load_data(DATA_PATH)

    inspect_data(df)

    df = clean_data(df)

    monthly_orders_analysis(df)
    yearly_orders_analysis(df)
    country_analysis(df)
    correlation_analysis(df)
    model_analysis(df)
    region_analysis(df)
    engine_analysis(df)
    total_orders_by_countries_Anaylsis(df)
    total_orders_by_US_Airlines_Analysis(df)
    total_orders_by_Engine_Analysis(df)

    print("\n Analysis completed successfully.")

# -------------------------------
# RUN
# -------------------------------
if __name__ == "__main__":
    main()