import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("📊 Futures ROI & PNL Calculator")

st.markdown("""
### 📝 Input Values:
Fill in the following details to calculate your Futures trading performance.
""")

# User Inputs
entry_price = st.number_input("1️⃣ Current Price / Entry Price", min_value=0.0, value=3339.0, format="%.10f")
capital = st.number_input("2️⃣ Capital (USDT)", min_value=1.0, value=100.0)
leverage = st.number_input("3️⃣ Leverage (e.g. 10x, 20x, etc.)", min_value=1, value=30)
take_profit = st.number_input("4️⃣ Take Profit / Close Position Price", min_value=0.0, value=3450.0, format="%.10f")
stop_loss = st.number_input("5️⃣ Stop Loss Price", min_value=0.0, value=3290.0, format="%.10f")
decimal_places = st.number_input("🔢 Decimal Digits After Price (e.g. 2 for 0.01, 4 for 0.0001)", min_value=0, max_value=10, value=2)

# Calculations
position_size = capital * leverage
quantity = position_size / entry_price
step = 1 / (10 ** decimal_places)

# Generate price ranges
price_up = [round(p, decimal_places) for p in list(pd.Series([entry_price + i * step for i in range(int((take_profit - entry_price) / step) + 1)]))]
price_down = [round(p, decimal_places) for p in list(pd.Series([entry_price - i * step for i in range(1, int((entry_price - stop_loss) / step) + 1)]))]

def calculate_metrics(price_list):
    data = []
    for price in price_list:
        unrealized_pnl = (price - entry_price) * quantity
        roi = (unrealized_pnl / capital) * 100
        margin_ratio = (capital / (capital + unrealized_pnl)) * 100 if (capital + unrealized_pnl) != 0 else float('inf')
        data.append({
            'Price': price,
            'Unrealized PNL (USDT)': round(unrealized_pnl, 4),
            'ROI (%)': round(roi, 4),
            'Margin Ratio (%)': round(margin_ratio, 2)
        })
    return pd.DataFrame(data)

if st.button("🔍 Calculate"):
    df_up = calculate_metrics(price_up)
    df_down = calculate_metrics(price_down)

    st.subheader("📈 Price Increasing Table")
    st.dataframe(df_up, use_container_width=True)

    st.subheader("📉 Price Decreasing Table")
    st.dataframe(df_down, use_container_width=True)

    # Plotting ROI Chart
    fig, ax = plt.subplots()
    ax.plot(df_up['Price'], df_up['ROI (%)'], label='ROI Up', color='green')
    ax.plot(df_down['Price'], df_down['ROI (%)'], label='ROI Down', color='red')
    ax.set_xlabel("Price")
    ax.set_ylabel("ROI (%)")
    ax.set_title("ROI vs Price")
    ax.legend()
    st.pyplot(fig)

    st.markdown("---")
    st.markdown(f"**✅ Profit at Take Profit ({take_profit}):** {round((take_profit - entry_price) * quantity, 4)} USDT")
    st.markdown(f"**❌ Loss at Stop Loss ({stop_loss}):** {round((stop_loss - entry_price) * quantity, 4)} USDT")
