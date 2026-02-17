import matplotlib.pyplot as plt

def display_histogram(data,name,stats):
    plt.figure(figsize = (8,5))
    plt.hist(data, bins = 10,color = "blue",edgecolor = "black",alpha=0.7)
    plt.axvline(stats["mean"],color='red',linestyle='--')
    plt.title(f"{name} Distribution")
    plt.xlabel("Grades")
    plt.ylabel("Number of Students")
    plt.show()