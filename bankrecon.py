import streamlit as st
from authentic import signup_user, login_user, update_password, verify_access_code, self_password, verify_update_code
from email_utils import send_verification_email, send_password_reset_email
from supabase import create_client, Client
from pathlib import Path
import streamlit as st
import pandas as pd
import pdfplumber
import io
import time
from sklearn.ensemble import IsolationForest
url = "https://xmldlgpddskwenpdbwcw.supabase.co"  # replace with your real Supabase URL
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhtbGRsZ3BkZHNrd2VucGRid2N3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQ1NzYwNDcsImV4cCI6MjA3MDE1MjA0N30.NoxLZ-rOeWzuVJ9DJELCSBYFP4MczBtl8ezD_T4WzoI"
supabase = create_client(url, key)

#st.set_page_config(page_title="Bank Reconciliator", layout="wide", initial_sidebar_state="expanded")

if "page" not in st.session_state:
    st.session_state.page = "auth"


def logout():
    st.set_page_config(page_title="Bank Reconciliator", layout="wide", initial_sidebar_state="expanded")
    st.session_state.page = "auth"
    st.session_state.user = None

def styled_df(df):
    styled = df.style.set_table_styles([
        {"selector": "thead th",
         "props": [("background-color", "white"),
                   ("color", "green"),
                   ("font-weight", "bold"),
                   ("max-width", "150px"),
                   ("white-space", "nowrap"),
                   ("text-align", "center")]},
     {"selector": "td",
         "props": [("text-align", "center"),
                   ("max-width", "100px"),
                   ("white-space", "nowrap"),
                   ("overflow", "hidden"),
                   ("text-overflow", "ellipsis"),
                   ("padding", "6px")]}
    ]).set_properties(**{"text-align": "center"})
    return styled

#st.dataframe(styled_df, height=400)

def render_df(df):
    st.markdown(
        styled_df(df).to_html(),
        unsafe_allow_html=True
    )

def main_app():
    st.set_page_config(page_title="SmartRecon", page_icon="Smart.png", layout="wide", initial_sidebar_state="expanded")
    st.markdown('<style>div.block-container{padding-top:2rem;}</style>',unsafe_allow_html=True)
    with st.sidebar:
        st.image("smarteklogo.jpg", use_container_width=True)
        st.markdown("---")
    
    st.image("smart.png", width=100,)  # Adjust width to your liking
# Display page title next to the logo
    #st.markdown("<h1 style='display: inline-block; vertical-align: middle; margin-left: 10px;'>SmartRecon</h1>", unsafe_allow_html=True)
    
    # This part adds polished layout and styling
    st.markdown("""
        <style>
            .block-container {
                padding-top: 2rem;
                background-color: #FFFFFF;
            }
            .title {
                font-size: 2rem;
                font-weight: bold;
                color: #196B24;
            }
            .title1{
                font-size: 3rem;
                font-weight: bold;
                color: #196B24;
            }
            .header {
                background-color: #FFFFFF;
            }
            .subtitle {
                font-size: 1.5rem;
                font-weight: bold;
                color: #E97132;
            }
            .subtitle2 {
                font-size: 1rem;
                font-weight: bold;
                color: #47D45A;
            }
            .subtitle3 {
                font-size: 1.5rem;
                font-weight: bold;
                color: #FFFFFF;
            }
                /* Change sidebar background color */
    [data-testid="stSidebar"] {
        background-color: #196B24;
    
    } 
     /* Style buttons inside sidebar */
    [data-testid="stSidebar"] button {
        background-color: white !important;
        color: green !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 8px 16px;
        font-weight: bold;
        cursor: pointer;
    }

    /* Button hover effect */
    [data-testid="stSidebar"] button:hover {
        background-color: #d4f7d4 !important;
        color:  #196B24 !important;
        border: none !important;
    }
     /* Target the file uploader */
    [data-testid="stFileUploader"] section {
        background-color: white !important;
        color: #E97132 !important;
        border-radius: 8px;
        border: 2px solid #E97132;
        padding: 10px;
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease-in-out;
    }
    /* Hover effect on the whole box */
    [data-testid="stFileUploader"] section:hover {
        box-shadow: 0px 6px 14px rgba(0, 0, 0, 0.15);
    }

    /* Change text color inside the uploader */
    [data-testid="stFileUploader"] section * {
        color: #196B24 !important;
    }

    /* Optional: Change hover effect */
    [data-testid="stFileUploader"] section:hover {
        border-color:#F6C6AD !important;
    }
    /* Browse files button styling */
    [data-testid="stFileUploader"] button {
        background-color: #196B24  !important;
        color: white !important;
        border-radius: 5px;
        border: none;
        padding: 6px 12px;
        font-weight: bold;
        transition: all 0.3s ease-in-out;
    }

    /* Hover effect for Browse files button */
    [data-testid="stFileUploader"] button:hover {
        background-color: #E97132  !important;
        color: white !important;
        transform: scale(1.03);
    }
        </style>
    """, unsafe_allow_html=True)
    # Sidebar styling


    st.markdown('<div class="header"><div class="title1">🏦 SmartRecon Bank Reconciliator</div></div>', unsafe_allow_html=True)
    
    # Co/ntinue with your main app logic here..# === Add logo to sidebar ==
    #st.title("🏦 SmartRecon Bank Reconciliator")
    st.success(f"Welcome {st.session_state.user['email']}!")
    # === Your bank reconciliation logic goes here ===
    # st.write("Put your bank reconciliation logic here...")
# Inject custom style
    # st.title("🏦 SmartRecon Bank Reconciliator")
# --- Sidebar Inputs ---
    #st.sidebar.header("Closing Balances")
    with st.sidebar:
        st.markdown('<div class="subtitle3">Closing Balances</div></div>', unsafe_allow_html=True)
    
    closing_cash_balance = st.sidebar.number_input("Closing Cashbook Balance", value=0.0)
    closing_bank_balance = st.sidebar.number_input("Closing Bank Statement Balance", value=0.0)

# --- File Upload ---
    #st.header("Upload Files")
    st.markdown('<div class="header"><div class="title"> Upload Files</div></div>', unsafe_allow_html=True)
    bank_file = st.file_uploader("Upload Bank Statement (Excel, CSV or PDF)", type=["xlsx", "xls", "csv", "pdf"], key="bank")
    cashbook_file = st.file_uploader("Upload Cash Book (Excel, CSV or PDF)", type=["xlsx", "xls", "csv", "pdf"], key="cashbook")

# --- Functions ---
    def read_excel_or_csv(file):
     if file.name.endswith(".csv"):
            return pd.read_csv(file)
     else:
         return pd.read_excel(file)

    def read_pdf(file):
        with pdfplumber.open(file) as pdf:
            all_text = ""
            for page in pdf.pages:
                all_text += page.extract_text() + "\n"
        return pd.DataFrame([line.split() for line in all_text.splitlines() if line.strip()])

    def load_file(file):
        if file.name.endswith(".pdf"):
            return read_pdf(file)
        else:
            return read_excel_or_csv(file)

# --- ML Anomaly Detection ---
    def prepare_features(df, date_col, desc_col, dr_col, cr_col):
        df = df.copy()
        df["amount"] = pd.to_numeric(df[dr_col], errors="coerce").fillna(0) - pd.to_numeric(df[cr_col], errors="coerce").fillna(0)
        df["weekday"] = pd.to_datetime(df[date_col], errors='coerce').dt.dayofweek.fillna(0)
        df["desc_length"] = df[desc_col].astype(str).str.len()
        df["desc_word_count"] = df[desc_col].astype(str).str.split().apply(len)
        return df[["amount", "weekday", "desc_length", "desc_word_count"]]

    def detect_anomalies_isolation_forest(df, features_df):
        model = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)
        model.fit(features_df)
        df["anomaly"] = model.predict(features_df)
        df["anomaly_flag"] = df["anomaly"].map({-1: "Anomaly", 1: ""})
        return df[df["anomaly_flag"] == "Anomaly"]

    def run_fraud_detection(bank_df, cashbook_df, bank_cols, cash_cols):
        bank_date_col, bank_desc_col, bank_dr_col, bank_cr_col = bank_cols
        cash_date_col, cash_desc_col, cash_dr_col, cash_cr_col = cash_cols

        bank_features = prepare_features(bank_df, bank_date_col, bank_desc_col, bank_dr_col, bank_cr_col)
        cash_features = prepare_features(cashbook_df, cash_date_col, cash_desc_col, cash_dr_col, cash_cr_col)

        fraud_bank_ml = detect_anomalies_isolation_forest(bank_df.copy(), bank_features)
        fraud_cash_ml = detect_anomalies_isolation_forest(cashbook_df.copy(), cash_features)

        return fraud_bank_ml, fraud_cash_ml

# --- Reconciliation Logic ---
    if bank_file and cashbook_file:
        #st.header("Preview Data")
        st.markdown('<div class="header"><div class="title"> Preview Data</div></div>', unsafe_allow_html=True)
        bank_df = load_file(bank_file)
        cashbook_df = load_file(cashbook_file)

        #st.subheader("Bank Statement Preview")
        st.markdown('<div class="header"><div class="subtitle">Bank Statement Preview</div></div>', unsafe_allow_html=True)
        #st.dataframe(bank_df.head())
        render_df(bank_df.head())
        #st.subheader("Cash Book Preview")
        st.markdown('<div class="header"><div class="subtitle">Cash Book Preview</div></div>', unsafe_allow_html=True)
        #st.dataframe(cashbook_df.head())
        render_df(cashbook_df.head())

        #st.markdown("**Select required columns for Bank Statement**")
        st.markdown('<div class="header"><div class="subtitle2">Select Required Bank Columns</div></div>', unsafe_allow_html=True)
        #st.dataframe(bank_df.head())
        bank_date_col = st.selectbox("Bank Date Column", bank_df.columns, key="bank_date")
        bank_desc_col = st.selectbox("Bank Description Column", bank_df.columns, key="bank_desc")
        bank_dr_col = st.selectbox("Bank Debit Column", bank_df.columns, key="bank_dr")
        bank_cr_col = st.selectbox("Bank Credit Column", bank_df.columns, key="bank_cr")

        #st.markdown("**Select required columns for Cash Book**")
        st.markdown('<div class="header"><div class="subtitle2">Select Required Cash Book Columns</div></div>', unsafe_allow_html=True)
        #st.dataframe(cashbook_df.head())
        cash_date_col = st.selectbox("Cash Book Date Column", cashbook_df.columns, key="cash_date")
        cash_desc_col = st.selectbox("Cash Book Description Column", cashbook_df.columns, key="cash_desc")
        cash_dr_col = st.selectbox("Cash Book Debit Column", cashbook_df.columns, key="cash_dr")
        cash_cr_col = st.selectbox("Cash Book Credit Column", cashbook_df.columns, key="cash_cr")

        include_desc = st.checkbox("Include Description in reconciling", value=False)
        enable_ml = st.checkbox("Run Anomaly Detection", value=False)

        if st.button("🔍 Reconcile"):
            #st.header("Perform Reconciliation")
            st.markdown('<div class="header"><div class="title">Reconciliation</div></div>', unsafe_allow_html=True)

            progress = st.progress(0)
            for pct in range(0, 101, 10):
                time.sleep(0.5)
                progress.progress(pct)

            bank_exp = pd.DataFrame({
                "date": pd.to_datetime(bank_df[bank_date_col], errors='coerce'),
                "description": bank_df[bank_desc_col].astype(str).str.lower().str.strip(),
                "debit": pd.to_numeric(bank_df[bank_dr_col], errors='coerce').fillna(0),
                "credit": pd.to_numeric(bank_df[bank_cr_col], errors='coerce').fillna(0)
            })

            cash_exp = pd.DataFrame({
                "date": pd.to_datetime(cashbook_df[cash_date_col], errors='coerce'),
                "description": cashbook_df[cash_desc_col].astype(str).str.lower().str.strip(),
                "debit": pd.to_numeric(cashbook_df[cash_dr_col], errors='coerce').fillna(0),
                "credit": pd.to_numeric(cashbook_df[cash_cr_col], errors='coerce').fillna(0)
            })

            matched_pairs = []
            unmatched_bank = bank_exp.copy()
            unmatched_cash = cash_exp.copy()

            for i, bank_row in bank_exp.iterrows():
                amt = bank_row['debit'] if bank_row['debit'] > 0 else bank_row['credit']
                side = 'debit' if bank_row['debit'] > 0 else 'credit'
                match_col = 'credit' if side == 'debit' else 'debit'

                candidates = unmatched_cash[(unmatched_cash[match_col].between(amt - 5, amt + 5))]
                if include_desc:
                    candidates = candidates[candidates['description'] == bank_row['description']]

                if not candidates.empty:
                    match_row = candidates.iloc[0]
                    match_index = match_row.name
                    matched_pairs.append({
                        "Bank Date": bank_row['date'],
                        "Bank Desc": bank_row['description'],
                        "Bank Dr": bank_row['debit'],
                        "Bank Cr": bank_row['credit'],
                        "Cash Date": match_row['date'],
                        "Cash Desc": match_row['description'],
                        "Cash Dr": match_row['debit'],
                        "Cash Cr": match_row['credit']
                    })
                    unmatched_bank = unmatched_bank.drop(i)
                    unmatched_cash = unmatched_cash.drop(match_index)

            matched_df = pd.DataFrame(matched_pairs)

            # Display results
            st.success(f"✅ Reconciled items: {len(matched_df)}")
            st.warning(f"⚠️ Unreconciled in Bank: {len(unmatched_bank)} | Cashbook: {len(unmatched_cash)}")
            #st.subheader("✅ Reconciled")
            st.markdown('<div class="header"><div class="subtitle">✅ Reconciled </div></div>', unsafe_allow_html=True)
            st.dataframe(matched_df)
            #render_df(matched_df)
            #st.subheader("❌ Unreconciled - Bank")
            st.markdown('<div class="header"><div class="subtitle">❌ Unreconciled - Bank </div></div>', unsafe_allow_html=True)
            st.dataframe(unmatched_bank)
            #render_df(unmatched_bank, height=400)
            #st.subheader("❌ Unreconciled - Cash Book")
            st.markdown('<div class="header"><div class="subtitle">❌ Unreconciled - Cash </div></div>', unsafe_allow_html=True)
            st.dataframe(unmatched_cash)

            # Summary
            outflows_cash_not_in_bank = unmatched_cash['credit'].sum()
            inflows_bank_not_in_cash = unmatched_bank['credit'].sum()
            inflows_cash_not_in_bank = unmatched_cash['debit'].sum()
            outflows_bank_not_in_cash = unmatched_bank['debit'].sum()

            derived_bank_balance = closing_cash_balance + outflows_cash_not_in_bank + inflows_bank_not_in_cash - inflows_cash_not_in_bank - outflows_bank_not_in_cash
            status = "✅ Complete" if abs(derived_bank_balance - closing_bank_balance) < 1 else "❌ Not Complete"

            summary_df = pd.DataFrame({
                "Bank Reconciliation Summary": [
                    "Balance as per cashbook", "Add:",
                    "Outflows in cash not in bank", "Inflows in bank not in cash",
                    "Less:", "Inflows in cash not in bank", "Outflows in bank not in cash",
                    "Balance as per bank statement", "STATUS"
                ],
                "Amount": [
                    closing_cash_balance, "", outflows_cash_not_in_bank, inflows_bank_not_in_cash,
                    "", inflows_cash_not_in_bank, outflows_bank_not_in_cash,
                    derived_bank_balance, status
                ]
            })

            # ML anomaly detection
            if enable_ml:
                fraud_bank_ml, fraud_cash_ml = run_fraud_detection(
                    bank_df, cashbook_df,
                    (bank_date_col, bank_desc_col, bank_dr_col, bank_cr_col),
                    (cash_date_col, cash_desc_col, cash_dr_col, cash_cr_col)
                )
                #st.subheader("🚨 Anomalies Detection - Bank Statement")
                st.markdown('<div class="header"><div class="subtitle">🚨 Anomalies Detection - Bank Statement</div></div>', unsafe_allow_html=True)
                st.dataframe(fraud_bank_ml)
                #st.subheader("🚨 Anomalies Detection - Cash Book")
                st.markdown('<div class="header"><div class="subtitle">🚨 Anomalies Detection - Cash </div></div>', unsafe_allow_html=True)
                st.dataframe(fraud_cash_ml)

            # Excel Report
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                matched_df.to_excel(writer, sheet_name='Reconciled', index=False)
                unmatched_bank.to_excel(writer, sheet_name='Unreconciled_Bank', index=False)
                unmatched_cash.to_excel(writer, sheet_name='Unreconciled_CashBook', index=False)
                summary_df.to_excel(writer, sheet_name='Reconciliation_Summary', index=False)
                if enable_ml:
                    fraud_bank_ml.to_excel(writer, sheet_name='Anomalies_Detection_Bank', index=False)
                    fraud_cash_ml.to_excel(writer, sheet_name='Anomalies_Detection_Cashbook', index=False)

                # Remove gridlines from all sheets
                for sheet in writer.sheets.values():
                    sheet.hide_gridlines(option=2)

            output.seek(0)
            st.download_button(
                label="📥 Download Reconciliation Report (Excel)",
                #label="st.markdown('<div class="header"><div class="subtitle">📥 Download Reconciliation Report (Excel) </div></div>', unsafe_allow_html=True)",
                data=output.getvalue(),
                file_name="bank_reconciliation_report.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    else:
     st.warning("Please upload both the bank statement and the cashbook to proceed.")
    

    with st.sidebar:
        st.markdown("---")
        st.markdown('<div class="subtitle3">User Action</div></div>', unsafe_allow_html=True)
        if st.button("Logout"):
            logout()
   

def auth_app():
    st.set_page_config(page_title="Bank Reconciliator",  page_icon="Smart.png", layout="centered", initial_sidebar_state="expanded")
    with st.sidebar:
        
        st.image("smarteklogo.png", use_container_width=True)
        st.markdown("---")
        st.markdown('<div class="subtitle3">WELCOME</div></div>', unsafe_allow_html=True)
    
    st.markdown('<style>div.block-container{padding-top:2rem;}</style>',unsafe_allow_html=True)
    st.markdown("""
        <style>
            .block-container {
                padding-top:0.5rem;
                background-color: white;
                background-size: cover;
                border-radius: 8px;
                box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
                font-size: 2rem;
                font-weight: bold;
                color: #196B24
                width: 150%;
                padding: 5rem;
                position: relative;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                margin: auto;
            }
            .title {
                font-size: 2rem;
                font-weight: bold;
                color: #196B24;
            }
            .title1{
                font-size: 3rem;
                font-weight: bold;
                color: #196B24;
                text-align: center;
            }
            .header {
                background-color: #FFFFFF;
            }
            .subtitle {
                font-size: 1rem;
                font-weight: italic;
                color: #BFBFBF;
                text-align: center;
                padding: 0.5px;
            }
            .subtitle2 {
                font-size: 1rem;
                font-weight: bold;
                color: black;
                text-align: center;
            }
            .subtitle3 {
                font-size: 3rem;
                font-weight: bold;
                color: #FFFFFF;
                Text-align: center;
                PAdding:2rem;
            }
                /* Change sidebar background color */
    [data-testid="stSidebar"] {
        background-color: #196B24;
    
    } 
     /* Style buttons inside sidebar */
    [data-testid="stSidebar"] button {
        background-color: white !important;
        color: #196B24 !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 8px 16px;
        font-weight: bold;
        cursor: pointer;
    }

    /* Button hover effect */
    [data-testid="stSidebar"] button:hover {
        background-color: #d4f7d4 !important;
        color:  #196B24 !important;
        border: none !important;
    }
        </style>
    """, unsafe_allow_html=True)
    #st.title("🔐 SMARTEK FINANCE")
    st.markdown('<div class="header"><div class="title1">SMARTEK FINANCE</div></div>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown('<div class="header"><div class="subtitle">Sign in to your Smartrecon App</div></div>', unsafe_allow_html=True)

      # ✅ Initialize all session state variables here
    if "stage" not in st.session_state:
        st.session_state.stage = "email"
        
    if "signup_stage" not in st.session_state:
        st.session_state.signup_stage = "start"
    
    if "reset_stage" not in st.session_state:
        st.session_state.reset_stage = "email"
    
    if "reset_stage" not in st.session_state:
        st.session_state.reset_stage = "start"


    if "temp_email" not in st.session_state:
        st.session_state.temp_email = None

    if "signup_email" not in st.session_state:
        st.session_state.signup_email = " "

    choice = st.radio("Choose Action", ["Login", "Signup", "Reset Password"], index=0)
    #choice = st.selectbox("Login, Signup or Reset Password", ["Login", "Signup", "Reset Password"], index=0)

    if choice == "Signup":
        if st.session_state.signup_stage == "start":
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            if st.button("Register"):
                success, response = signup_user(email, password)
                if success:
                    st.success("Verification code sent. Check your email. Re-enter to verify.")
                    st.session_state.signup_email = email
                    st.session_state.signup_stage = "verify"
                else:
                    st.error(response)

        elif st.session_state.signup_stage == "verify":
            st.info(f"Verification code sent to {st.session_state.signup_email}")
            code = st.text_input("Enter Verification Code")
            if st.button("Verify"):
                if verify_access_code(supabase, st.session_state.signup_email, code):
                    st.success("Email verified! You can now log in.")
                    st.session_state.signup_stage = "start"  # Reset stage
                else:
                    st.error("Invalid code.")

    elif choice == "Login":
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            user = login_user(email, password)
            if user:
                st.session_state.user = user
                st.session_state.page = "main"
            else:
                st.error("Invalid login or not verified.")

    elif choice == "Reset Password":
        if st.session_state.reset_stage =="email":
            email = st.text_input("Enter your registered email")
            if st.button("Generate access code"):
                success, msg = update_password(email)
                if success:
                    st.success("Check your email for the new password.Reclick to update.")
                    st.session_state.reset_stage =email
                    st.session_state.reset_stage ="update"
                else:
                        st.error("Not registered.")

        elif st.session_state.reset_stage == "update":
            st.info(f"Access code sent to {st.session_state.reset_stage}")
            code = st.text_input("Enter Verification Code")
            email = st.text_input("Enter your registered email")
            new_password = st.text_input("Enter new password", type="password")
            if st.button("Update"):
                if verify_update_code(supabase, email, code, new_password):
                    st.success("Code verified! Password updated. You can now log in.")
                    st.session_state.signup_stage = "email"  # Reset stage
                else:
                    st.error("Invalid code.")
        
                    
        
                   
                    #success, msg = self_password(email, code, new_password)
                #if verify_update_code(supabase, st.session_state.reset_stage, code, new_password)
                    #st.success("Code verified! Password updated.")
    
                    #if success:
                 #st.success("Password updated successfully.")
            
        
           
             # go back to start
           
        

        

if st.session_state.page == "auth":
    auth_app()
else:
        main_app()
