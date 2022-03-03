import pandas  as pd
import seaborn as sb
import matplotlib.pyplot as plt
import numpy as np


df = pd.read_csv('csv_data/medical_examination.csv')

# Add an overweight column to the data. To determine if a 
# person is overweight, first calculate their BMI by dividing 
# their weight in kilograms by the square of their height in meters. 
# If that value is > 25 then the person is overweight.

df['overweight'] = df['weight']/((df['height']/100)**2)

# Use the value 0 for NOT overweight and the value 1 for overweight.
df['overweight'] = df['overweight'].apply(lambda x: 1 if x > 25 else 0) #works better than bellow
# df['overweight'].values[(df['overweight'] > 25)] = 1
# df['overweight'].values[(df['overweight'] < 25) & (df['overweight'] != 1)] = 0

# Normalize the data by making 0 always good and 1 always bad. 
# If the value of cholesterol or gluc is 1, make the value 0. 
# If the value is more than 1, make the value 1.

df['cholesterol'].values[(df['cholesterol']==1)], df['cholesterol'].values[(df['cholesterol']>1)] = 0,1
df['gluc'].values[(df['gluc']==1)], df['gluc'].values[(df['gluc']>1)] = 0,1

# Convert the data into long format and create a chart that shows the 
# value counts of the categorical features using seaborn's catplot(). 
# The dataset should be split by 'Cardio' so there is one chart for each 
# cardio value. The chart should look like examples/Figure_1.png.

def draw_cat_plot():
    #Create Dataframe for cat plot using pd.melt
    df_cat = pd.melt(df, id_vars=['cardio'], 
                    value_vars= ['active', 'alco', 'cholesterol', 'gluc', 'overweight', 'smoke']) #creates new df, cardio is id, valu_vars are stored under variable, their value are stored under value
    # Group and reformat the data to split it by 
    # 'cardio'. Show the counts of each feature.
    #  You will have to rename one of the columns 
    # for the catplot to work correctly.

    df_cat['total'] = 1 #create column total to count each variable
    df_cat = df_cat.groupby(['cardio', 'variable', 'value'], as_index=False).count() #will group by cardio:0,1, then variable:value_vars, then value of variable:0,1, then total; count

    # Draw the catplot with 'sns.catplot()'
    figure = sb.catplot(x = 'variable', y = 'total', data= df_cat, hue= 'value', kind = 'bar', col= 'cardio')
    figure.savefig('catplot.png')
    
    print(df_cat.head)

def draw_heat_map():
    # Clean the data
    df_heat = df[(df['ap_lo'] <= df['ap_hi']) & 
                (df['height'] >= df['height'].quantile(0.025)) &
                (df['height'] <= df['height'].quantile(0.975)) &
                (df['weight'] >= df['weight'].quantile(0.025))&
                (df['weight'] <= df['weight'].quantile(0.975))]
    
    # Calculate the correlation matrix
    corr = df_heat.corr(method="pearson")

    # Generate a mask for the upper triangle
    m = np.triu(corr) #use numpy triu function



    # Set up the matplotlib figure
    fig, ax = plt.subplots(figsize = (10,10))

    # Draw the heatmap with 'seaborn.heatmap()'

    sb.heatmap(corr, linewidths= 1, annot = True, square= True, mask = m, fmt= ".1f",cmap="YlGnBu",
                center=0.08)

    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    
    
    

# draw_cat_plot()
# draw_heat_map()