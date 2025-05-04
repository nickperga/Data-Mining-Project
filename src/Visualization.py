import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re

df = pd.read_csv("save\data.csv", encoding="utf-8")

# Group by department and count entries
department_counts = df['department'].value_counts()

# Plot using seaborn
plt.figure(figsize=(10, 6))
sns.barplot(x=department_counts.index, y=department_counts.values, palette="viridis")
plt.title("Number of Cases per Department")
plt.xlabel("Department")
plt.ylabel("Number of Cases")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# List of legal code columns
legal_codes = ['ΠΚ', 'ΚΠΔ', 'ΚΠολΔ', 'ΑΚ']

# Count how many non-empty (or non-null) entries exist for each code
code_counts = {}
for code in legal_codes:
    code_counts[code] = df[code].apply(len).sum()

# Plot as a pie chart
plt.figure(figsize=(8, 8))
plt.pie(code_counts.values(), labels=code_counts.keys(), autopct='%1.1f%%', startangle=140, colors=plt.cm.Set3.colors)
plt.title("Legal Code References in Cases")
plt.axis('equal')  # Equal aspect ratio ensures the pie is a circle.
plt.show()


# Convert 'department number' to numeric (just in case) and drop NaNs
df['department number'] = df['department number'].astype(str).str.strip()
df = df.dropna(subset=['department number'])

# Count occurrences of each department number
dept_counts = df['department number'].value_counts().sort_index()

# Plot bar chart
plt.figure(figsize=(10, 6))
dept_counts.plot(kind='bar', color='mediumpurple', edgecolor='black')
plt.title('Number of Cases per Department Number')
plt.xlabel('Department Number')
plt.ylabel('Number of Cases')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

#first i put the (number of judges : count) in a dict
NumOfJudges = {}

for text in df["judges"]:
    match = re.search(r"(?:Συγκροτήθηκε|ΣΥΓΚΡΟΤΗΘΗΚΕ) από τους (?:Δικαστές|δικαστές)[,:]?\s*([^\.]+)", text)
    if match:
        names_str = match.group(1)
        names = re.split(r",\s*|και\s+", names_str)
        names = [name.strip() for name in names]
        if(len(names) not in NumOfJudges.keys()):
            NumOfJudges[len(names)] = 1
        else:
            NumOfJudges[len(names)] += 1


labels = [str(key) for key in NumOfJudges.keys()]
sizes = list(NumOfJudges.values())

# Calculate the total sum of values
total = sum(sizes)

# Calculate the percentages
percentages = [value / total * 100 for value in sizes]

# Create the pie chart without displaying percentages on the slices
plt.figure(figsize=(8, 8))
plt.pie(sizes, startangle=90, wedgeprops={'edgecolor': 'black'})

# Add a legend with the percentages
legend_labels = [f'{label}: {percent:.1f}%' for label, percent in zip(labels, percentages)]
plt.legend(legend_labels, title="Percentages", loc="best")

# Equal aspect ratio ensures that pie is drawn as a circle.
plt.axis('equal')

# Title for the chart
plt.title('Pie Chart with Percentages in Legend Only')

# Display the plot
plt.show()
