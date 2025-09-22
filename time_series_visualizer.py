from calendar import month_name

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=["date"],
                 index_col="date")

# Clean data
df = df[
    (df['value'] >= df['value'].quantile(0.025)) &
    (df['value'] <= df['value'].quantile(0.975))
    ]


def draw_line_plot():
    line_plot = df.copy()
    # Draw line plot
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(line_plot.index, line_plot['value'], color='red', linewidth=1)
    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig


def draw_bar_plot():
    bar_plot = df.copy()
    # Copy and modify data for monthly bar plot
    months = month_name[1:]
    bar_plot['months'] = pd.Categorical(bar_plot.index.strftime('%B'), categories=months, ordered=True)
    dfp = pd.pivot_table(data=bar_plot, index=bar_plot.index.year, columns='months', values='value', aggfunc='mean', observed=False)

    # Draw bar plot
    ax = dfp.plot(kind='bar', figsize=(8, 8), ylabel='Average Page Views', xlabel='Years', rot=0)
    _ = ax.legend(loc='upper left')
    fig = ax.get_figure()
    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig


def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    months_order = [m[:3] for m in month_name[1:]]
    df_box['month'] = pd.Categorical(df_box['month'],
                                     categories=months_order,
                                     ordered=True)
    fig, axes = plt.subplots(1, 2, figsize=(20, 8))
    sns.boxplot(x=df_box['year'], y=df_box['value'], hue=df_box['year'], legend=False, ax=axes[0])
    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel("Year")
    axes[0].set_ylabel("Page Views")

    sns.boxplot(x=df_box['month'], y=df_box['value'], hue=df_box['month'], legend=False, ax=axes[1])
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_xlabel("Month")
    axes[1].set_ylabel("Page Views")
    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig

draw_box_plot()