import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def plot_style_setup(ax, title, x_label):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.tick_params(axis='y', which='both', left=False)
    ax.set_xlabel(x_label)
    ax.set_title(title, fontsize=16)

def add_year(ax, year):
    ax.text(0.9, 0.1, str(year), transform=ax.transAxes, ha='center', fontsize=20)

def create_animation(df, column, x_label, normalize=False):
    frames = df['Year'].unique()
    
    if normalize:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6), gridspec_kw={'width_ratios': [1, 1]})
    else:
        fig, ax1 = plt.subplots(figsize=(8, 6))

    def animate(frame):
        ax1.clear()
        if normalize:
            ax2.clear()

        # Filter data for the current frame
        df_frame = df[df['Year'] == frame]
        
        # Top 10 countries for the main column
        top_countries = df_frame.nlargest(10, column).sort_values(column, ascending=True)

        # Plot the first graph (original column)
        ax1.barh(top_countries['Country'], top_countries[column], color='skyblue')
        for i, row in top_countries.iterrows():
            ax1.text(row[column], row['Country'], f'{row[column]:,.1f}', va='center')
        plot_style_setup(ax1, f'Top 10 by {column}', x_label)

        # If normalize is True, plot the second graph
        if normalize:
            top_countries_ratio = (
                df_frame.assign(ratio=lambda x: x[column] / x['Pop'])
                .nlargest(10, 'ratio')
                .sort_values('ratio', ascending=True)
            )
            ax2.barh(top_countries_ratio['Country'], top_countries_ratio['ratio'], color='salmon')
            for i, row in top_countries_ratio.iterrows():
                ax2.text(row['ratio'], row['Country'], f'{row["ratio"]:,.1f}', va='center')
            plot_style_setup(ax2, f'Top 10 by {column} per capita', 'Normalized Value')

        # Add year to both plots
        add_year(ax1, frame)
        if normalize:
            add_year(ax2, frame)

        plt.tight_layout()

    anim = animation.FuncAnimation(fig, animate, frames=frames, interval=300)
    return anim

if __name__ == '__main__':
    # Load the data
    df = pd.read_excel('data/data.xlsx', sheet_name='Sheet1')

    # Set parameters
    column = 'Pop_growth'  # Column for the main graph
    x_label = 'Population growth'  # X-axis label
    normalize = False  # Whether to add the second graph

    # Create and save the animation
    anim = create_animation(df, column, x_label, normalize)
    anim.save(f'{column}_{"comparison" if normalize else "single"}.gif', fps=1)
    plt.show()
