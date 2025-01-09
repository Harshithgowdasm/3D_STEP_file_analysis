import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from scipy.stats import ttest_ind

# Load your data
df = pd.read_csv("selected_analysis.csv")

# 1. Data Exploration
print(df.info())
print(df.describe())
print(df['Class'].value_counts())

# Check correlations
correlation_matrix = df.corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
plt.title("Correlation Matrix")
plt.show()

# 2. Statistical Analysis
for column in df.columns[1:-2]:  # Exclude File Name, Criteria Met, and Class
    group_0 = df[df['Class'] == 0][column]
    group_1 = df[df['Class'] == 1][column]
    t_stat, p_val = ttest_ind(group_0, group_1)
    print(f"{column}: t-stat={t_stat:.4f}, p-value={p_val:.4f}")

# 3. Pairwise Scatter Plots
sns.pairplot(df, hue='Class', vars=['Total Faces', 'Curved Faces', 'Total Edges',
                                    'Vertices', 'Bounding Box Volume', 'Mean Curvature',
                                    'Curvature Std Dev', 'Volume', 'Hole Count', 'size', 'ispart'])
plt.show()

# 4. Classification with Random Forest
X = df[['Total Faces', 'Curved Faces', 'Total Edges', 'Vertices',
        'Bounding Box Volume', 'Mean Curvature', 'Curvature Std Dev',
        'Volume', 'Hole Count', 'size', 'ispart']]
y = df['Class']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

rf_model = RandomForestClassifier(random_state=42)
rf_model.fit(X_train, y_train)
y_pred = rf_model.predict(X_test)

print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))

# Feature Importance
feature_importance = pd.DataFrame({
    'Feature': X.columns,
    'Importance': rf_model.feature_importances_
}).sort_values(by='Importance', ascending=False)

print("Feature Importance:")
print(feature_importance)

# Plot Feature Importance
sns.barplot(x='Importance', y='Feature', data=feature_importance)
plt.title("Feature Importance from Random Forest")
plt.show()
