import streamlit as st
import pandas as pd
import numpy as np
import pickle
import random
from datetime import date

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Business AI App", page_icon="💼", layout="centered")

# ---------------- UI STYLE ----------------
st.markdown("""
<style>

/* 🌌 Background */
body {
    background: linear-gradient(135deg, #020617, #0f172a);
    color: white;
}

/* 🧊 Glass Card */
.glass {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(12px);
    border-radius: 20px;
    padding: 25px;
    margin-bottom: 20px;
    box-shadow: 0px 0px 30px rgba(0,0,0,0.4);
}

/* 🧠 Title */
.title {
    text-align: center;
    font-size: 42px;
    font-weight: bold;
    background: linear-gradient(90deg, #22c55e, #3b82f6);
    -webkit-background-clip: text;
    color: transparent;
}

/* ✨ Subtitle */
.sub {
    text-align: center;
    color: #94a3b8;
    margin-bottom: 20px;
}

/* 🔘 Buttons */
.stButton>button {
    width: 100%;
    height: 60px;
    border-radius: 15px;
    font-size: 18px;
    background: linear-gradient(90deg, #22c55e, #16a34a);
    color: white;
    border: none;
    transition: 0.3s;
}

.stButton>button:hover {
    transform: scale(1.05);
}

/* 📊 Metrics */
.css-1xarl3l {
    background: rgba(255,255,255,0.05);
    border-radius: 15px;
    padding: 10px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- LOAD MODEL ----------------
model = pickle.load(open("model.pkl", "rb"))

# ---------------- SESSION ----------------
if "page" not in st.session_state:
    st.session_state.page = "login"

if "otp" not in st.session_state:
    st.session_state.otp = ""

if "user" not in st.session_state:
    st.session_state.user = ""

# ---------------- LOGIN ----------------
if st.session_state.page == "login":

    st.markdown('<div class="title">🔐 Secure Login</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub">Enter your number to continue</div>', unsafe_allow_html=True)

    phone = st.text_input("Enter Mobile Number")

    if st.button("Send OTP"):
        otp = random.randint(1000, 9999)
        st.session_state.otp = str(otp)
        st.success(f"OTP (Demo): {otp}")

    otp_input = st.text_input("Enter OTP")

    if st.button("Verify"):
        if otp_input == st.session_state.otp:
            st.session_state.user = phone

            try:
                users = pd.read_csv("users.csv")
                if phone in users["phone"].values:
                    st.session_state.page = "dashboard"
                else:
                    st.session_state.page = "profile"
            except:
                st.session_state.page = "profile"

            st.rerun()
        else:
            st.error("Wrong OTP ❌")

# ---------------- PROFILE ----------------
elif st.session_state.page == "profile":

    st.title("👤 Create Your Profile")

    name = st.text_input("Name")
    business = st.text_input("Business Type")
    location = st.text_input("Location")

    if st.button("Save Profile"):

        data = pd.DataFrame({
            "phone": [st.session_state.user],
            "name": [name],
            "business": [business],
            "location": [location]
        })

        try:
            old = pd.read_csv("users.csv")
            data = pd.concat([old, data])
        except:
            pass

        data.to_csv("users.csv", index=False)

        st.session_state.page = "dashboard"
        st.rerun()

# ---------------- DASHBOARD ----------------
elif st.session_state.page == "dashboard":

    st.markdown('<div class="title">🚀 Business AI System</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub">Next-gen smart business intelligence platform</div>', unsafe_allow_html=True)

    st.image("https://picsum.photos/1200/400", use_container_width=True)
    st.title("🚀 Smart Business Dashboard")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="glass">', unsafe_allow_html=True)
        if st.button("💰 Optimize Pricing"):
            st.session_state.page = "price"
        if st.button("📦 Predict Sales"):
            st.session_state.page = "sales"
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="glass">', unsafe_allow_html=True)
        if st.button("📊 Profit Analytics"):
            st.session_state.page = "profit"
        if st.button("💼 Daily Tracker"):
            st.session_state.page = "daily"
        if st.button("📈 Dashboard Analytics"):
            st.session_state.page = "summary"
        st.markdown('</div>', unsafe_allow_html=True)

# ---------------- PRICE ----------------
elif st.session_state.page == "price":

    st.image("bg.jpg", use_container_width=True)
    st.title("💰 Price Optimizer")

    cost = st.slider("Cost Price", 1, 200, 30)
    demand = st.slider("Demand", 1, 100, 50)

    if st.button("Calculate Best Price"):
        best_price = 0
        max_profit = -999

        for price in np.arange(cost+1, cost+50):
            units = model.predict([[price, demand]])[0]
            profit = (price - cost) * units

            if profit > max_profit:
                max_profit = profit
                best_price = price

        st.success(f"Best Price: ₹{best_price}")
        st.info(f"Max Profit: ₹{max_profit:.2f}")

    if st.button("⬅ Back"):
        st.session_state.page = "dashboard"

# ---------------- SALES ----------------
elif st.session_state.page == "sales":

    st.image("https://images.unsplash.com/photo-1556742049-0cfed4f6a45d", use_container_width=True)
    st.title("📦 Sales Predictor")

    price = st.number_input("Selling Price")
    demand = st.number_input("Demand")

    if st.button("Predict Sales"):
        units = model.predict([[price, demand]])[0]
        st.success(f"Estimated Units Sold: {int(units)}")

    if st.button("⬅ Back"):
        st.session_state.page = "dashboard"

# ---------------- PROFIT ----------------
elif st.session_state.page == "profit":

    st.image("https://images.unsplash.com/photo-1559526324-593bc073d938", use_container_width=True)
    st.title("📊 Profit Calculator")

    cost = st.number_input("Cost Price")
    price = st.number_input("Selling Price")
    units = st.number_input("Units Sold")

    if st.button("Calculate Profit"):
        profit = (price - cost) * units
        st.success(f"Total Profit: ₹{profit:.2f}")

    if st.button("⬅ Back"):
        st.session_state.page = "dashboard"

# ---------------- DAILY ----------------
elif st.session_state.page == "daily":

    st.image("https://images.unsplash.com/photo-1563013544-824ae1b704d3", use_container_width=True)
    st.title("💼 Daily Collection")

    sales = st.number_input("Total Sales ₹")
    expense = st.number_input("Total Expense ₹")

    if st.button("Save Data"):
        profit = sales - expense

        data = pd.DataFrame({
            "user": [st.session_state.user],
            "date": [date.today()],
            "sales": [sales],
            "expense": [expense],
            "profit": [profit]
        })

        try:
            old = pd.read_csv("records.csv")
            data = pd.concat([old, data])
        except:
            pass

        data.to_csv("records.csv", index=False)
        st.success("Saved Successfully ✅")

    if st.button("⬅ Back"):
        st.session_state.page = "dashboard"

# ---------------- SUMMARY ----------------
elif st.session_state.page == "summary":

    st.title("📊 Business Analytics Dashboard")

    try:
        df = pd.read_csv("records.csv")
        user_df = df[df["user"] == st.session_state.user]

        # 🧊 Glass card start
        st.markdown('<div class="glass">', unsafe_allow_html=True)

        # 📊 Metrics
        st.metric("💰 Total Profit", int(user_df["profit"].sum()))
        st.metric("📦 Total Sales", int(user_df["sales"].sum()))

        # 📈 Chart
        st.line_chart(user_df[["sales","profit"]])

        # 📋 Table
        st.dataframe(user_df)

        # 🧊 Glass card end
        st.markdown('</div>', unsafe_allow_html=True)

    except:
        st.warning("No data available yet")

    # 🔙 Back button
    if st.button("⬅ Back"):
        st.session_state.page = "dashboard"