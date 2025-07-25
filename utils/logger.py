import csv
import os
import pandas as pd
import matplotlib.pyplot as plt

def log_results_csv(filepath, results):
    """
    Write a list of dicts to CSV. Creates header if file doesn't exist.
    """
    file_exists = os.path.exists(filepath)
    with open(filepath, mode='a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        if not file_exists:
            writer.writeheader()
        writer.writerows(results)

def log_convergence_csv(filepath, values, algo_name):
    import csv
    with open(filepath, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Iteration", "Best Cost", "Algorithm"])
        for i, val in enumerate(values):
            writer.writerow([i, val, algo_name])
            
def plot_performance_metrics(csv_path="results/performance_metrics.csv"):
    df = pd.read_csv(csv_path)

    # Execution Time
    plt.figure(figsize=(8, 5))
    plt.bar(df["Algorithm"], df["Time (s)"], color='skyblue')
    plt.title("Execution Time by Algorithm")
    plt.ylabel("Time (seconds)")
    plt.xlabel("Algorithm")
    plt.grid(True, axis='y')
    plt.tight_layout()
    plt.savefig("results/execution_time.png")

    # Path Cost
    plt.figure(figsize=(8, 5))
    plt.bar(df["Algorithm"], df["Path Cost"], color='lightcoral')
    plt.title("Path Cost by Algorithm")
    plt.ylabel("Cost")
    plt.xlabel("Algorithm")
    plt.grid(True, axis='y')
    plt.tight_layout()
    plt.savefig("results/path_cost.png")

    # Path Length
    plt.figure(figsize=(8, 5))
    plt.bar(df["Algorithm"], df["Path Length"], color='mediumseagreen')
    plt.title("Path Length by Algorithm")
    plt.ylabel("Number of Steps")
    plt.xlabel("Algorithm")
    plt.grid(True, axis='y')
    plt.tight_layout()
    plt.savefig("results/path_length.png")

def plot_convergence(ga_csv="results/ga_convergence.csv", sa_csv="results/sa_convergence.csv"):
    ga_df = pd.read_csv(ga_csv)
    sa_df = pd.read_csv(sa_csv)

    plt.figure(figsize=(10, 6))
    plt.plot(ga_df["Iteration"], ga_df["Best Cost"], label="GA", color="magenta", linewidth=2)
    plt.plot(sa_df["Iteration"], sa_df["Best Cost"], label="SA", color="orange", linewidth=2)
    plt.title("Convergence of GA and SA")
    plt.xlabel("Iteration")
    plt.ylabel("Best Path Cost")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig("results/convergence_plot.png")