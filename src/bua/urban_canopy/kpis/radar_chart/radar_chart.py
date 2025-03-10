import numpy as np
import matplotlib.pyplot as plt


class RadarChart:
    DEFAULT_NUM_TICK = 5

    DEFAULT_POSITION_LABEL = 1.25
    DEFAULT_POSITION_OUTER_TICK = 1.05

    def __init__(self, title=""):
        self.title = title
        self.axes = []
        self.data = []
        self._num_ticks = self.DEFAULT_NUM_TICK


    def add_axis(self, name, unit, min_value, max_value, axis_type, order="ascending"):
        """
        Add a new axis to the radar chart.

        :param name: The name of the axis.
        :param unit: The unit of measurement for the axis.
        :param min_value: The minimum boundary of the axis.
        :param max_value: The maximum boundary of the axis.
        :param axis_type: Type of axis: "year", "percentage", "ratio", "value".
        :param order: "ascending" or "descending" (to control axis order).
        """
        axis = {
            "name": name,
            "unit": unit,
            "min_value": min_value,
            "max_value": max_value,
            "type": axis_type,
            "order": order
        }
        self.axes.append(axis)

    def add_data(self, values, color, label="Data"):
        """
        Add a dataset to the radar chart.

        :param values: A list of values corresponding to the axes.
        :param color: Color for this dataset.
        :param label: A label for this dataset.
        """
        self.data.append({
            "values": values,
            "color": color,
            "label": label
        })

    def auto_set_boundaries(self):
        """
        Automatically adjust axis boundaries based on the data.
        """
        for i, axis in enumerate(self.axes):
            data_values = [data["values"][i] for data in self.data]
            min_data = min(data_values)
            max_data = max(data_values)
            self.axes[i]["min_value"] = min_data
            self.axes[i]["max_value"] = max_data

    def plot(self, filename=None):
        """
        Plot the radar chart and save to a file (optional).

        :param filename: Optional filename to save the plot.
        """
        num_vars = len(self.axes)

        # Create angles for each axis
        angles = [(np.pi / 2. + 2 * np.pi / num_vars * i) % (2 * np.pi) for i in range(num_vars)]

        # Create figure and axis
        fig, ax = plt.subplots(figsize=(7, 7), subplot_kw=dict(polar=True))
        ax.axis("off")

        # Prepare the data for each dataset
        for data in self.data:
            values = data["values"]
            values += values[:1]  # Close the shape by repeating the first value

            # Make sure angles have the same length as values
            angles_for_data = angles + [angles[0]]  # Close the shape by repeating the first angle

            # Normalize the values for each axis
            normalized_values = []
            for i, value in enumerate(values[:-1]):  # Skip the last value (which is a duplicate)
                axis = self.axes[i]
                min_value = axis['min_value']
                max_value = axis['max_value']
                order = axis['order']

                if order == "ascending":
                    # Normalizing for ascending axis
                    normalized_value = (value - min_value) / (max_value - min_value)  # Normalize to [0, 1]
                else:
                    # Normalizing for descending axis (flip the scale)
                    normalized_value = (max_value - value) / (max_value - min_value)  # Inverted scale

                normalized_values.append(normalized_value)
            normalized_values.append(normalized_values[0])  # Close the shape by repeating the first value

            # Plot each dataset (fill and outline)
            # ax.fill(angles_for_data, normalized_values, color=data["color"], alpha=0.3)
            ax.plot(angles_for_data, normalized_values, color=data["color"], linewidth=2, label=data["label"])

        # # Set category labels
        ax.set_xticks([])
        ax.set_yticklabels([])
        # ax.set_xticklabels([f"{axis['name']} \n[{axis['unit']}]" for axis in self.axes])


        # Set category labels (axis labels)
        for i, axis in enumerate(self.axes):
            # Adjust the radial position of labels (further out)
            label_angle = angles[i]
            # Set the position of the label by adjusting the angle and radial distance
            ax.text(label_angle, self.DEFAULT_POSITION_LABEL, f"{axis['name']}\n [{axis['unit']}]",
                    horizontalalignment='center',
                    size=12, color='black', verticalalignment='center')

        # Remove the default grid and tick labels
        ax.grid(True)

        # Add custom grid lines and value labels
        for i, axis in enumerate(self.axes):
            ticks = np.linspace(axis['min_value'], axis['max_value'], self._num_ticks)
            ticks_labels = [f"{t:.1f}" for t in ticks]

            # Add custom grid lines for each axis graduation
            for tick in ticks:
                ax.plot([angles[i], angles[i]],
                        [0, (tick - axis['min_value']) / (axis['max_value'] - axis['min_value'])],
                        color='gray', linewidth=1, linestyle='--')

            # Add value labels at each graduation, skipping the first axis (i == 0)
            for j, (tick, tick_label) in enumerate(zip(ticks, ticks_labels)):
                # Compute radial position for each tick mark (scaled value)
                if axis['order'] == "descending":
                    # Reverse the scaling for descending axes (higher value closer to center)
                    radial_position = (axis['max_value'] - tick) / (axis['max_value'] - axis['min_value'])
                else:
                    radial_position = (tick - axis['min_value']) / (axis['max_value'] - axis['min_value'])

                # Skip the value label for the first tick on the first axis (if needed)
                if (axis['order'] == "descending" and j == self._num_ticks - 1) or (
                        axis['order'] == "ascending" and j == 0):
                    continue  # For descending axes, we skip the first label

                if (axis['order'] == "descending" and j == 0 ) or (
                        axis['order'] == "ascending" and j == self._num_ticks - 1):
                    radial_position = radial_position * self.DEFAULT_POSITION_OUTER_TICK

                ax.text(angles[i], radial_position, tick_label, horizontalalignment='center', size=10,
                        color='black')

        # Draw the polygonal boundary (close the shape)
        polygon_values = [1] * num_vars
        polygon_values.append(polygon_values[0])  # Close the polygon by repeating the first value
        ax.plot(angles + [angles[0]], polygon_values, color="black", linewidth=2, linestyle="solid")


        # Set radial limits
        ax.set_ylim(0, 1.1)  # Set the radial limits to cover the normalized range of data

        # Add legend
        ax.legend(loc="upper right", bbox_to_anchor=(1.1, 1.1))

        # Set title and show plot
        if self.title !="":
            plt.title(self.title)
        if filename:
            plt.savefig(filename)
        else:
            plt.show()


# Example usage:
radar = RadarChart()
radar.add_axis("Speed", "km/h", 0, 200, "value", order="ascending")
radar.add_axis("Strength", "kg", 0, 300, "value", order="descending")
radar.add_axis("Agility", "m/s", 0, 10, "value", order="ascending")
radar.add_axis("Stamina", "minutes", 0, 150, "value", order="ascending")
radar.add_axis("Skill", "score", 0, 100, "percentage", order="descending")

# Add data
radar.add_data([120, 250, 8, 90, 50], color="blue", label="Player A")
radar.add_data([100, 200, 7, 120, 60], color="green", label="Player B")

# Optionally, auto set boundaries
# radar.auto_set_boundaries()

# Plot or save the radar chart
radar.plot()
