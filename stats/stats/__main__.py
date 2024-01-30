
import pandas as pd
import sys 
import os 
# read excel file from argument 
df = pd.read_excel(sys.argv[1], sheet_name='DATA')

trnaslations = {
    "Regions": "Region",
    "Cine": "Bioskop",
    "Fine Arts": "Umetnost",
    "Sports": "Sport",
    "Music": "Muzika",
    "Theater": "Pozorište",
    "Halls": "Sale za događaje",
    "Heritage": "Nasleđe",
    "Literat": "Književnost",
}

df = df.rename(columns=trnaslations)

figures_dir = sys.argv[2]
if not os.path.exists(figures_dir):
    os.makedirs(figures_dir)

# delete zeros 
if len(sys.argv) > 3 and sys.argv[3] == 'delete_zeros':
    for column in df.columns:
        if column == 'Region':
            continue
        df = df[df[column] != 0]

# check if columns are normally distributed
from scipy.stats import shapiro
for column in df.columns:
    if column == 'Region':
        continue
    print(f"Column: {column}")
    print(f"Normality: {shapiro(df[column])}")

    # detect distribution 
    from scipy.stats import normaltest
    print(f"Distribution: {normaltest(df[column])}")



# draw distribution plots
import seaborn as sns
import matplotlib.pyplot as plt
for column in df.columns:
    if column == 'Region':
        continue
    plt.figure()
    plt.title(f"Column: {column}")
    sns.histplot(df[column])
    plt.savefig(os.path.join(figures_dir, f"{column}.png"))

for correlation_method in ['pearson', 'kendall', 'spearman']:
    print(f"Correlation Method: {correlation_method}")
    for region in list(df['Region'].unique()) + [None]:
        if region is None:
            print(f"Region: All")
            region_df = df
        else:
            print(f"Region: {region}")
            region_df = df[df['Region'] == region]


        # calculate correlations 
        corr = region_df.corr(method=correlation_method)

        # get ones with largest correlations
        corr = corr.unstack()
        corr = corr.sort_values(ascending=False)
        corr = corr[corr != 1]


        corr = [(index, correlation) for index, correlation in corr.items() if abs(correlation) > 0.5 and index[0] > index[1]]

        # print index and correlation
        for index, correlation in sorted(corr, key=lambda x: x[1], reverse=True)[:10]:
            print(f"Index: {index}, Correlation: {correlation}")


region_translations = {
    1: "Altenejo",
    2: "Centralni deo",
    3: "Severni deo",
    None: "Svi",
}

# draw correlogram
import seaborn as sns
import matplotlib.pyplot as plt
for region in list(df['Region'].unique()) + [None]:
    if region is None:
        print(f"Region: All")
        region_df = df
    else:
        print(f"Region: {region}")
        region_df = df[df['Region'] == region]

    plt.figure()
    if region is None:
        plt.title(f"Region: All")
    else:
        plt.title(f"Region: {region}")
    sns.heatmap(region_df.corr(method="spearman"), annot=True)
    plt.savefig(os.path.join(figures_dir, "correlogram_%s.png" % region_translations[region]))
