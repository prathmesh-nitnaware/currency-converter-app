import streamlit as st
import requests
import json

st.set_page_config(page_title="Currency Converter", page_icon="💱")

st.title("💱 Currency Converter")
st.markdown("Convert currencies using real-time exchange rates from [exchangerate.host](https://exchangerate.host)")

# Load currency symbols
@st.cache_data
def get_currency_list():
    url = "https://api.exchangerate.host/symbols"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()

        if "symbols" in data:
            # Save for debug (optional)
            with open("sample_api_response.json", "w") as f:
                json.dump(data, f, indent=4)
            return list(data["symbols"].keys())
        else:
            st.warning("⚠️ API returned no 'symbols'. Using default list.")
            return ["USD", "INR", "EUR", "GBP", "JPY"]
    except Exception as e:
        st.error(f"❌ Error fetching currency list: {e}")
        return ["USD", "INR", "EUR", "GBP", "JPY"]

currencies = get_currency_list()

# User Inputs
amount = st.number_input("Enter amount", min_value=0.0, format="%.2f", value=1.0)
from_currency = st.selectbox("From Currency", currencies, index=currencies.index("USD"))
to_currency = st.selectbox("To Currency", currencies, index=currencies.index("INR"))

# Conversion
if st.button("Convert"):
    try:
        url = f"https://api.exchangerate.host/convert?from={from_currency}&to={to_currency}&amount={amount}"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        result = response.json()

        # Show raw JSON response for debug
        with open("sample_api_response.json", "a") as f:
            json.dump(result, f, indent=4)

        if "result" in result and "info" in result:
            converted = result["result"]
            rate = result["info"]["rate"]

            st.success(f"💸 {amount} {from_currency} = {converted:.2f} {to_currency}")
            st.caption(f"📊 Exchange Rate: 1 {from_currency} = {rate:.4f} {to_currency}")

            # Optional: Display JSON in app
            with st.expander("📦 See Raw JSON Response"):
                st.json(result)

        else:
            st.error("⚠️ Conversion failed. Unexpected API response.")

    except Exception as e:
        st.error(f"❌ Error during conversion: {e}")
