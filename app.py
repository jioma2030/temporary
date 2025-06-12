from sklearn.linear_model import LinearRegression
import numpy as np

# 연도별 온실가스 합계 예측
df['연도'] = pd.to_datetime(df['기준년월'], format='%Y-%m').dt.year
yearly = df.groupby('연도')['합계'].sum().reset_index()

# 선형 회귀로 미래 예측
X = yearly[['연도']]
y = yearly['합계']
model = LinearRegression()
model.fit(X, y)

# 2024~2035년 예측
future_years = pd.DataFrame({'연도': list(range(2024, 2036))})
future_preds = model.predict(future_years)

# 시각화
st.subheader("📈 Predicted Total GHG Emissions (2024–2035)")
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(yearly['연도'], yearly['합계'], label="Actual", marker='o')
ax.plot(future_years['연도'], future_preds, label="Predicted", linestyle='--', marker='x', color='orange')
ax.set_xlabel("Year")
ax.set_ylabel("Total Emissions (kTon CO₂)")
ax.set_title("Future GHG Emissions Prediction")
ax.legend()
ax.grid()
st.pyplot(fig)
