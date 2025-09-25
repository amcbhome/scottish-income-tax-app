import pandas as pd
import streamlit as st
import altair as alt

from tax_logic import ScottishIncomeTax

st.set_page_config(
    page_title="Scottish Income Tax (2025/26)",
    page_icon="💷",
    layout="centered"
)

st.title("💷 Scottish Income Tax (NSND) — 2025/26")

with st.sidebar:
    st.header("Inputs")
    gross_income = st.number_input(
        "Gross annual income (£)",
        min_value=0.0, step=500.0, value=50_000.0, format="%.2f",
        help="Employment/self-employment/pension/rental (non-savings, non-dividend) income."
    )
    st.caption("Personal Allowance taper is auto-applied above £100,000.")

# Calculate
res = ScottishIncomeTax.calculate(gross_income)

# Top metrics
col1, col2, col3 = st.columns(3)
col1.metric("Personal Allowance", f"£{res.personal_allowance:,.0f}")
col2.metric("Taxable income", f"£{res.taxable_income:,.0f}")
col3.metric("Total tax", f"£{res.total_tax:,.0f}")

st.write(f"**Effective tax rate:** {res.effective_rate:.2f}% of gross (£{res.gross_income:,.0f})")
st.divider()

# Band table
rows = []
for b in res.band_breakdown:
    rows.append({
        "Band": b.name,
        "Rate": f"{int(b.rate*100)}%",
        "Taxable in band (£)": round(b.band_taxable, 2),
        "Tax due (£)": round(b.tax, 2),
    })
df = pd.DataFrame(rows)

st.subheader("Band breakdown")
st.dataframe(
    df.style.format({"Taxable in band (£)": "£{:.2f}", "Tax due (£)": "£{:.2f}"}),
    use_container_width=True,
    hide_index=True
)

# Chart
st.subheader("Tax by band")
chart_df = pd.DataFrame({
    "Band": [b.name for b in res.band_breakdown if b.band_taxable > 0 or b.name == "Top"],
    "Tax due": [round(b.tax, 2) for b in res.band_breakdown if b.band_taxable > 0 or b.name == "Top"]
})
bar = alt.Chart(chart_df).mark_bar().encode(
    x=alt.X("Band:N", sort=None, title=""),
    y=alt.Y("Tax due:Q", title="£"),
    tooltip=["Band", alt.Tooltip("Tax due:Q", format="£,.2f")]
).properties(width=600, height=320)
st.altair_chart(bar, use_container_width=True)

# Explanations
with st.expander("What’s included / excluded?"):
    st.markdown(
        """
- **Included:** Scottish **non-savings, non-dividend** (NSND) income bands and rates for **2025/26**, plus UK **Personal Allowance** with taper above **£100,000**.
- **Excluded:** UK-wide **savings** and **dividend** tax, National Insurance, student loans, marriage allowance transfer, gift-aid/pension gross-up, and other reliefs/adjustments.
- **Tip:** To model total tax across income types, extend the logic to add UK savings/dividend sections and combine the results.
        """
    )

with st.expander("Notes"):
    for n in res.notes:
        st.write("• " + n)

st.caption(f"Tax year: {res.tax_year}. For guidance only; verify against official sources.")
