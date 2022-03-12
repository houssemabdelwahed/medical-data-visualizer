import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import sys


df = pd.read_csv('medical_examination.csv')


overweight = (df['weight'] / ((df['height'] / 100)**2) > 25).astype(int)

df['overweight'] = overweight


df['cholesterol'] = (df['cholesterol'] > 1).astype(int)

df['gluc'] = (df['gluc'] > 1).astype(int)





def draw_cat_plot():
   
    df_cat = df.melt(id_vars= 'cardio',value_vars=['cholesterol' 	,'gluc' ,	'smoke' ,	'alco' ,	'active' , 	'overweight'])


    df_cat = pd.DataFrame(df_cat.groupby(['cardio' ,	'variable' ,	'value'])['value'].count())
    df_cat.rename(columns={'value':'total'},inplace=True)
    df_cat.reset_index(inplace=True)


 
    graph = sns.catplot(
        x='variable',
        y='total',
        hue='value',
        col='cardio',
        data=df_cat,
        kind='bar')

    fig = graph.fig


    fig.savefig('catplot.png')
    return fig



def draw_heat_map():
  

    df_heat = df[ (df['ap_lo'] <= df['ap_hi']) &
                  (df['height'] >= df['height'].quantile(0.025)) &
                  (df['height'] <= df['height'].quantile(0.975)) &
                  (df['weight'] >= df['weight'].quantile(0.025)) &
                  (df['weight'] <= df['weight'].quantile(0.975))]

  
    corr = df_heat.corr()

   
    mask = np.zeros_like(corr)
    mask[np.triu_indices_from(mask)] = True

    
    fig, ax = plt.subplots(figsize=(12, 12))

    
    ax = sns.heatmap(
        corr,
        linewidths=.5,
        annot=True,
        fmt='.1f',
        mask=mask,
        square=True,
        center=0,
        vmin=-0.1,
        vmax=0.25,
        cbar_kws={
            'shrink': .45,
            'format': '%.2f'
        })

 
    fig.savefig('heatmap.png')
    return fig

