import os
import pandas as pd
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import seaborn as sns


# Function to extract data from HTML files
def extract_data_from_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    soup = BeautifulSoup(content, 'html.parser')
    table = soup.find('table')

    # Extract headers
    headers = [header.get_text() for header in table.find_all('th')]

    # Extract rows
    rows = []
    for row in table.find_all('tr')[1:]:  # Skip the header row
        cells = row.find_all('td')
        row_data = [cell.get_text() for cell in cells]
        rows.append(row_data)

    # Create DataFrame
    df = pd.DataFrame(rows, columns=headers)

    # Clean data
    df = df.apply(pd.to_numeric, errors='ignore')
    return df


run = "revamp_343_wide"

# Get all files in the directory
all_files = os.listdir(f"../exported_tables/{run}")

# Filter files that start with "tabelle" and end with ".html"
file_paths = [f"../exported_tables/{run}/{file}" for file in all_files if file.endswith(".html")]

# Extract data from all files and concatenate into a single DataFrame
data_frames = [extract_data_from_html(file_path) for file_path in file_paths]
combined_df = pd.concat(data_frames, ignore_index=True)


#combined_df['Tactic'] = combined_df['Team'].apply(lambda x: ' '.join(x.split()[2:]))
combined_df['Tactic'] = combined_df['Team'].apply(lambda x: ' '.join(x.split()[:2]))
#combined_df['Tactic'] = combined_df['Team'].apply(lambda x: ' '.join(x.split()[:1]))

# Plot aggregated data by Tactic
plt.figure(figsize=(18, 6))

# Box plot for Points by Tactic
plt.subplot(1, 3, 1)
sns.boxplot(x='Tactic', y='Pkt', data=combined_df, order=sorted(combined_df['Tactic'].unique()))
mean_values = combined_df.groupby('Tactic')['Pkt'].mean().reindex(sorted(combined_df['Tactic'].unique()))
for i, mean in enumerate(mean_values):
    plt.text(i, mean, f'{mean:.2f}', ha='center', va='bottom')
plt.title('Points by Tactic')
plt.xticks(rotation=45)
plt.ylim(30, 100)  # Set y-axis limit for Points

# Box plot for Goals by Tactic
plt.subplot(1, 3, 2)
sns.boxplot(x='Tactic', y='Tore', data=combined_df, order=sorted(combined_df['Tactic'].unique()))
mean_values = combined_df.groupby('Tactic')['Tore'].mean().reindex(sorted(combined_df['Tactic'].unique()))
for i, mean in enumerate(mean_values):
    plt.text(i, mean, f'{mean:.2f}', ha='center', va='bottom')
plt.title('Goals by Tactic')
plt.xticks(rotation=45)
plt.ylim(40, 130)  # Set y-axis limit for Goals

# Box plot for Goals Against (GGT) by Tactic
plt.subplot(1, 3, 3)
sns.boxplot(x='Tactic', y='Ggt', data=combined_df, order=sorted(combined_df['Tactic'].unique()))
mean_values = combined_df.groupby('Tactic')['Ggt'].mean().reindex(sorted(combined_df['Tactic'].unique()))
for i, mean in enumerate(mean_values):
    plt.text(i, mean, f'{mean:.2f}', ha='center', va='bottom')
plt.title('Goals Against (GGT) by Tactic')
plt.xticks(rotation=45)
plt.ylim(40, 130)  # Set y-axis limit for Goals Against

plt.tight_layout()
plt.savefig(f'../exported_tables/{run}/tactic_plots.png')
#plt.savefig(f'../exported_tables/{run}/team_plots.png')