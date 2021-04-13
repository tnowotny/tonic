import numpy as np
from matplotlib import animation, rc
import matplotlib.pyplot as plt
import tonic.transforms as transforms


def plot_event_grid(events, sensor_size, ordering, axis_array=(3, 3)):
    events = events.squeeze()
    events = np.array(events)
    transform = transforms.Compose(
        [transforms.ToVoxelGrid(num_time_bins=np.product(axis_array))]
    )
    volume = transform(events, sensor_size=sensor_size, ordering=ordering)
    fig, axes_array = plt.subplots(*axis_array)
    for i in range(axis_array[0]):
        for j in range(axis_array[1]):
            axes_array[i, j].imshow(volume[i * axis_array[0] + j, :, :])
            axes_array[i, j].axis("off")
            axes_array[i, j].title.set_text(str(i * axis_array[0] + j))
    plt.tight_layout()


def pad_events(batch):
    max_length = 0
    for sample, target in batch:
        if len(sample) > max_length:
            max_length = len(sample)
    samples_output = []
    targets_output = []
    for sample, target in batch:
        sample = np.vstack((np.zeros((max_length - len(sample), 4)), sample))
        samples_output.append(sample)
        targets_output.append(target)
    return np.stack(samples_output), targets_output
