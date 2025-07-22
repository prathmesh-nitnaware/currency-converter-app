import streamlit as st

st.set_page_config(page_title="Offline Currency Converter", page_icon="💱")
st.title("💱 Offline Currency Converter")
st.markdown("This app uses hardcoded exchange rates and works without internet.")

exchange_rates = {
    "USD": 1.0,
    "INR": 83.5,
    "EUR": 0.91,
    "GBP": 0.78,
    "JPY": 141.2,
    "AUD": 1.49,
    "CAD": 1.35,
    "CNY": 7.15,
}

currencies = list(exchange_rates.keys())

amount = st.number_input("Enter amount", min_value=0.01, value=1.0, format="%.2f")
from_currency = st.selectbox("From Currency", currencies, index=currencies.index("USD"))
to_currency = st.selectbox("To Currency", currencies, index=currencies.index("INR"))

if st.button("Convert"):
    try:
        usd_amount = amount / exchange_rates[from_currency]
        converted = usd_amount * exchange_rates[to_currency]
        rate = exchange_rates[to_currency] / exchange_rates[from_currency]

        st.success(f"💸 {amount} {from_currency} = {converted:.2f} {to_currency}")
        st.caption(f"📊 1 {from_currency} = {rate:.4f} {to_currency}")
    except Exception as e:
        st.error(f"❌ Error during conversion: {e}")
