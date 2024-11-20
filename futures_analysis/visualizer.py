import matplotlib.pyplot as plt

def plot_graph(df, output_path="futures_market_plot.png"):
    """
    Plots the 'High', 'Low', and 'Mean' columns for the given dataframe
    """
    plt.figure(figsize=(12, 6))
    plt.plot(df['Contract Name'], df['High'], label='High', color='blue', marker='o')
    plt.plot(df['Contract Name'], df['Low'], label='Low', color='red', marker='o')
    plt.plot(df['Contract Name'], df['Mean'], label='Mean', color='green', linestyle='--', marker='o')
    
    # Customize plot
    plt.xlabel('Contract Name')
    plt.ylabel('Values')
    plt.title('High, Low, and Mean Values of Contracts')
    plt.xticks(rotation=45, ha='right')
    plt.legend()
    plt.tight_layout()
    plt.grid(alpha=0.3)
    plt.savefig(output_path)
    plt.show()
