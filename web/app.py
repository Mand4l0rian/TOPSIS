import streamlit as st
import pandas as pd
import numpy as np
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

# TOPSIS

def calculate_topsis(df, weights, impacts):

    data = df.iloc[:, 1:].values.astype(float)
    
    w_list = np.array([float(w) for w in weights.split(',')])
    i_list = [i.strip() for i in impacts.split(',')]

    rss = np.sqrt((data ** 2).sum(axis=0))
    
    rss[rss == 0] = 1 
    normalized = data / rss

    weighted_mat = normalized * w_list

    ideal_best = []
    ideal_worst = []

    for i in range(len(i_list)):
        col = weighted_mat[:, i]
        if i_list[i] == '+':
            ideal_best.append(col.max())
            ideal_worst.append(col.min())
        else:
            ideal_best.append(col.min())
            ideal_worst.append(col.max())

    ideal_best = np.array(ideal_best)
    ideal_worst = np.array(ideal_worst)

    dist_best = np.sqrt(((weighted_mat - ideal_best) ** 2).sum(axis=1))
    dist_worst = np.sqrt(((weighted_mat - ideal_worst) ** 2).sum(axis=1))

    total_dist = dist_best + dist_worst
    scores = np.divide(dist_worst, total_dist, out=np.zeros_like(dist_worst), where=total_dist != 0)


    df['Topsis Score'] = scores
    df['Rank'] = df['Topsis Score'].rank(ascending=False).astype(int)
    
    return df

# EMAIL 
def send_email(receiver_email, result_df):
    SENDER_EMAIL = "rajgupta1803@gmail.com" 
    SENDER_PASSWORD = "vpne pghw jdxl wred"  
    
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = receiver_email
    msg['Subject'] = "Your TOPSIS Result"
    
    body = "Hello,\n\nPlease find attached the result of your TOPSIS analysis.\n\nBest,\nTOPSIS Web Service"
    msg.attach(MIMEText(body, 'plain'))
    
    filename = "topsis_result.csv"
    result_df.to_csv(filename, index=False)
    
    attachment = open(filename, "rb")
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(part)
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        text = msg.as_string()
        server.sendmail(SENDER_EMAIL, receiver_email, text)
        server.quit()
        attachment.close()
        os.remove(filename) 
        return True
    except Exception as e:
        st.error(f"Error sending email: {e}")
        return False

# USER INTERFACE (Streamlit)
# ---------------- FRONTEND UI ----------------

st.set_page_config(page_title="TOPSIS Web Service", layout="centered")

st.markdown("""
    <style>
        .main {
            background-color: #f5f7fa;
        }
        .title {
            text-align: center;
            font-size: 40px;
            font-weight: bold;
            color: #2c3e50;
        }
        .subtitle {
            text-align: center;
            color: #7f8c8d;
        }
        .box {
            background: white;
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0px 0px 15px rgba(0,0,0,0.1);
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>TOPSIS Web Service</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Upload your file, enter weights & impacts, and receive results via email</div><br>", unsafe_allow_html=True)

with st.container():
    st.markdown("<div class='box'>", unsafe_allow_html=True)

    uploaded_file = st.file_uploader("📁 Upload CSV File", type=['csv'])
    
    col1, col2 = st.columns(2)

    with col1:
        weights_input = st.text_input("⚖ Weights", "1,1,1,1")
    with col2:
        impacts_input = st.text_input("📊 Impacts", "+,+,-,+")

    email_input = st.text_input("📧 Email ID")

    submit_btn = st.button("🚀 Submit", use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)



    if uploaded_file is not None and email_input:
        try:
            df = pd.read_csv(uploaded_file)
            
            num_cols = df.shape[1] - 1 
            w_len = len(weights_input.split(','))
            i_len = len(impacts_input.split(','))
            
            if w_len != num_cols or i_len != num_cols:
                st.error(f"Error: Weights/Impacts length ({w_len}/{i_len}) must match number of criteria columns ({num_cols}).")
            else:
                result_df = calculate_topsis(df, weights_input, impacts_input)
                
                st.write("Result Preview:")
                st.dataframe(result_df)
                
                with st.spinner('Sending Email...'):
                    success = send_email(email_input, result_df)
                    if success:
                        st.success(f"Result sent to {email_input} successfully!")
                        
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please upload a file and enter an email ID.")