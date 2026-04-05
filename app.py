import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Customer Churn Analysis", layout="wide", page_icon="📊")

# ── Load & Clean ──
df = pd.read_csv('WA_Fn-UseC_-Telco-Customer-Churn.csv')
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
df.dropna(inplace=True)
df['Churn'] = df['Churn'].map({'Yes': 1, 'No': 0})
df['tenure_group'] = pd.cut(df['tenure'], bins=[0,12,24,48,72],
                             labels=['0-1 yr','1-2 yr','2-4 yr','4-6 yr'])

# ── Header ──
st.title("Customer Churn Analysis")
st.markdown("Analysing churn patterns across **7,000+ telecom customers** to identify key retention drivers.")
st.divider()

# ── KPIs ──
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Customers", f"{len(df):,}")
c2.metric("Churned", f"{df['Churn'].sum():,}")
c3.metric("Retained", f"{(df['Churn']==0).sum():,}")
c4.metric("Churn Rate", f"{df['Churn'].mean()*100:.1f}%")

st.divider()

# ── Chart helper ──
def style(ax):
    ax.spines[['top','right','left']].set_visible(False)
    ax.yaxis.grid(True, linestyle='--', alpha=0.4)
    ax.set_axisbelow(True)
    ax.tick_params(colors='#444', labelsize=9)
    ax.set_ylabel(ax.get_ylabel(), color='#444', fontsize=10)

# ── Row 1 ──
col1, col2 = st.columns(2)

with col1:
    st.subheader("Churn Rate by Contract Type")
    contract_churn = df.groupby('Contract')['Churn'].mean() * 100
    fig, ax = plt.subplots(figsize=(5, 3.5))
    bars = ax.bar(contract_churn.index, contract_churn.values,
                  color=['#e74c3c','#f39c12','#2ecc71'], width=0.5, edgecolor='none')
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                f'{bar.get_height():.1f}%', ha='center', fontsize=9, color='#333')
    ax.set_ylabel('Churn Rate (%)')
    style(ax)
    plt.tight_layout()
    st.pyplot(fig)
    st.caption("💡 Month-to-month customers churn at 42% vs 11% on annual contracts")

with col2:
    st.subheader("Churn Rate by Tenure")
    tg = df.groupby('tenure_group', observed=True)['Churn'].mean() * 100
    fig, ax = plt.subplots(figsize=(5, 3.5))
    bars = ax.bar(tg.index.astype(str), tg.values,
                  color='#3498db', width=0.5, edgecolor='none')
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                f'{bar.get_height():.1f}%', ha='center', fontsize=9, color='#333')
    ax.set_ylabel('Churn Rate (%)')
    style(ax)
    plt.tight_layout()
    st.pyplot(fig)
    st.caption("💡 Highest churn risk is within the first 12 months")

st.divider()

# ── Row 2 ──
col1, col2 = st.columns(2)

with col1:
    st.subheader("Monthly Charges vs Churn")
    fig, ax = plt.subplots(figsize=(5, 3.5))
    stayed = df[df['Churn']==0]['MonthlyCharges']
    churned = df[df['Churn']==1]['MonthlyCharges']
    bp = ax.boxplot([stayed, churned], labels=['Stayed','Churned'],
                    patch_artist=True, widths=0.4,
                    medianprops=dict(color='white', linewidth=2),
                    whiskerprops=dict(color='#aaa'),
                    capprops=dict(color='#aaa'),
                    flierprops=dict(marker='o', color='#ccc', markersize=3))
    bp['boxes'][0].set_facecolor('#2ecc71')
    bp['boxes'][1].set_facecolor('#e74c3c')
    ax.set_ylabel('Monthly Charges ($)')
    style(ax)
    plt.tight_layout()
    st.pyplot(fig)
    st.caption("💡 Churned customers pay ~$20/month more on average")

with col2:
    st.subheader("Key Findings & Recommendations")
    st.markdown("""
**1. Contract Type** is the strongest churn predictor
- Month-to-month → **42% churn**
- Annual contract → **11% churn**

**2. Early Tenure** is the highest risk window
- Over 50% of churn happens within **first 12 months**

**3. Higher Bills** drive exits
- Churned customers avg **$74/month**
- Retained customers avg **$61/month**

---
**💡 Recommendation**

Offer discounted annual contracts to new customers in their first 3 months to significantly reduce early-tenure churn.
    """)

st.divider()
st.caption("Built by Katyayni Singh · github.com/katyayniii")