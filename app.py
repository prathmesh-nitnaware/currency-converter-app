import streamlit as st
import requests

# Streamlit page config
st.set_page_config(page_title="Currency Converter", page_icon="💱")

st.title("💱 Currency Converter")
st.markdown("Convert currencies using real-time exchange rates from [exchangerate.host](https://exchangerate.host)")

# Function to fetch available currencies
@st.cache_data
def get_currency_list():
    url = "https://api.exchangerate.host/symbols"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()

        if "symbols" in data:
            return list(data["symbols"].keys())
        else:
            st.error("⚠️ API response invalid. 'symbols' not found.")
            return ["USD", "INR", "EUR"]  # Fallback
    except Exception as e:
        st.error(f"❌ Failed to load currency list: {e}")
        return ["USD", "INR", "EUR"]  # Fallback

# Load currency list
currencies = get_currency_list()

# Input fields
amount = st.number_input("Enter amount", min_value=0.0, format="%.2f", value=1.0)
from_currency = st.selectbox("From Currency", currencies, index=currencies.index("USD"))
to_currency = st.selectbox("To Currency", currencies, index=currencies.index("INR"))

# Conversion logic
if st.button("Convert"):
    url = f"https://api.exchangerate.host/convert?from={from_currency}&to={to_currency}&amount={amount}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        result = response.json()

        if "result" in result and "info" in result:
            converted_amount = result["result"]
            rate = result["info"]["rate"]
            st.success(f"💸 {amount} {from_currency} = {converted_amount:.2f} {to_currency}")
            st.caption(f"💱 Exchange Rate: 1 {from_currency} = {rate:.4f} {to_currency}")
        else:
            st.error("❌ Conversion failed. Unexpected API response.")
    except Exception as e:
        st.error(f"❌ Error during conversion: {e}")
