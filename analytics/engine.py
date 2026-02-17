import numpy as np

def calculate_stats(data):
    if not data:return None
    return{
        "mean": np.mean(data),
        "variance": np.var(data),
        "std_dev": np.std(data),
        "count": len(data),
    }
def get_interpretation(stats):
    if not stats:return None
    return "Very diverse group" if stats["std_dev"] > 4 else "Homogeneous group"