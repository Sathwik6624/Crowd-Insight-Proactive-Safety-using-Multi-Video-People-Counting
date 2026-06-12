import matplotlib.pyplot as plt

def prepare_graph(data, cam_id):
    plt.figure()
    plt.plot(data)
    plt.title(f"Camera {cam_id} People Count")
    plt.xlabel("Frames")
    plt.ylabel("Count")
    plt.grid()