import pandas as pd

table = pd.read_csv('foodmaps.csv')

#equation pf = Wr * R + Wp * P + Wd * D
# Wr = 0.5, Wp = 0.25, Wd = 0.25
# R = rating, P = price, D = distance
# Normalize the data
# Min-Max scaling
# (x - min(x)) / (max(x) - min(x))

def normalize(df):
    # copy the dataframe
    df_norm = df.copy()
    # apply min-max scaling
    for column in df_norm.columns:
        df_norm[column] = (df_norm[column] - df_norm[column].min()) / (df_norm[column].max() - df_norm[column].min())
        
    return df_norm

def calc_score(restaurant):
    normed = normalize(table)
    # Find the index of the row with the given restaurant
    row_index = normed.index[normed.eq(restaurant).any(axis=1)][0]
    # Get the price, rating, distance values of the restaurant
    vals = normed.iloc[row_index].tolist()
    # Calculate the score
    score = vals[0] * 0.5 + vals[1] * 0.25 + vals[2] * 0.25

    return score.round(2) # round to 2 decimal places
