import streamlit as st
import numpy as np
import joblib
from sklearn.preprocessing import StandardScaler

# กำหนด URL หรือเส้นทางของภาพพื้นหลัง
background_image_url = "https://res.cloudinary.com/idemo/image/upload/qs3xs1limgx1hlijykif"
text_color = "#663333"  # สีตัวอักษร

# ใส่ CSS สำหรับพื้นหลังและสีตัวอักษร
st.markdown(
    f"""
    <style>
        .stApp {{
            background-image: url('{background_image_url}');
            background-size: cover;
            background-position: center;
            height: 100vh;
        }}
        h1, h2, h3, p, div {{
            color: {text_color} !important;
        }}
        .history {{
            background-color: rgba(255, 255, 255, 0.8);
            padding: 10px;
            border-radius: 5px;
            margin-top: 10px;
        }}
        /* ปรับขนาดตัวอักษรของ text_area */
        textarea {{
            font-size: 60px !important;
        }}
        /* ปรับขนาดตัวอักษรของ number_input */
        .stNumberInput label {{
            font-size: 60px !important;
        }}
    </style>
    """,
    unsafe_allow_html=True
)

# โหลดโมเดลที่เซฟไว้
model = joblib.load('model_mlp_best.pkl')

# โหลด scaler ที่ใช้ตอนเทรน (ถ้ามี)
scaler = joblib.load('scaler.pkl')

# พจนานุกรม mapping ชื่อฟีเจอร์ (อังกฤษ -> ไทย)
feature_labels = {
    'perimeter_worst': 'เส้นรอบวง (มากที่สุด)',
    'area_worst': 'พื้นที่ (มากที่สุด)',
    'radius_worst': 'รัศมี (มากที่สุด)',
    'concave points_worst': 'จุดเว้า (มากที่สุด)',
    'concave points_mean': 'ค่าเฉลี่ยจุดเว้า',
    'perimeter_mean': 'ค่าเฉลี่ยเส้นรอบวง',
    'area_mean': 'ค่าเฉลี่ยพื้นที่',
    'radius_mean': 'ค่าเฉลี่ยรัศมี',
    'area_se': 'ค่าเบี่ยงเบนมาตรฐานของพื้นที่',
    'concavity_mean': 'ค่าเฉลี่ยเว้า',
    'concavity_worst': 'ความเว้า (มากที่สุด)',
    'perimeter_se': 'ค่าเบี่ยงเบนเส้นรอบวง',
    'radius_se': 'ค่าเบี่ยงเบนรัศมี',
    'compactness_worst': 'ความหนาแน่น (มากที่สุด)',
    'compactness_mean': 'ค่าเฉลี่ยความหนาแน่น',
    'texture_worst': 'พื้นผิว (มากที่สุด)',
    'concave points_se': 'ค่าเบี่ยงเบนจุดเว้า',
    'smoothness_worst': 'ความเรียบ (มากที่สุด)',
    'texture_mean': 'ค่าเฉลี่ยพื้นผิว',
    'symmetry_worst': 'ความสมมาตร (มากที่สุด)'
}

feature_names = list(feature_labels.keys())

# ---------------- UI ---------------- #
st.title("🎗️ พยากรณ์โรคมะเร็งเต้านมด้วย MLP Model")
st.write("กรอกข้อมูลคุณลักษณะของก้อนเนื้อเพื่อให้โมเดลทำนายว่าเป็น **มะเร็งหรือไม่**")

# รับข้อมูลจากผู้ใช้
input_data = []
for feature in feature_names:
    label_th = feature_labels[feature]
    value = st.number_input(f"{label_th}", min_value=0.0, step=0.01)
    input_data.append(value)

# ทำนายผล
if st.button("ทำนายผล"):
    X = np.array(input_data).reshape(1, -1)

    # ถ้ามีการใช้ scaler ตอน train ต้องใช้ตอน predict ด้วย
    if scaler:
        X = scaler.transform(X)

    prediction = model.predict(X)[0]

    # แสดงผลลัพธ์
    if prediction == 1:
        st.error("💡 ผลการทำนาย: ผู้ป่วยมีแนวโน้มเป็นมะเร็ง (Malignant)")
    else:
        st.success("✅ ผลการทำนาย: ผู้ป่วยไม่มีแนวโน้มเป็นมะเร็ง (Benign)")
