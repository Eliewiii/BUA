import numpy as np
import matplotlib.pyplot as plt


class RadarChart:
    DEFAULT_NUM_TICK = 5

    DEFAULT_POSITION_LABEL = 1.15
    DEFAULT_POSITION_OUTER_TICK = 1.01

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

    def add_data(self, values, color, style="-", label="Data"):
        """
        Add a dataset to the radar chart.

        :param values: A list of values corresponding to the axes.
        :param color: Color for this dataset.
        :param label: A label for this dataset.
        """
        self.data.append({
            "values": values,
            "color": color,
            "style": style,
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

    def plot(self, filename=None, figsize=(8, 8), dpi=300, y_lim=1.1):
        """
        Plot the radar chart and save to a file (optional).

        :param filename: Optional filename to save the plot.
        """
        num_vars = len(self.axes)

        # Create angles for each axis
        angles = [(np.pi / 2. + 2 * np.pi / num_vars * i) % (2 * np.pi) for i in range(num_vars)]

        # Create figure and axis
        fig, ax = plt.subplots(figsize=figsize, dpi=dpi, subplot_kw=dict(polar=True))
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
            ax.plot(angles_for_data, normalized_values, color=data["color"], linewidth=2, label=data["label"],
                    linestyle=data["style"])

        # # Set category labels
        ax.set_xticks([])
        ax.set_yticklabels([])
        # ax.set_xticklabels([f"{axis['name']} \n[{axis['unit']}]" for axis in self.axes])

        # Add axis labels and custom grid lines/ticks in a single loop
        for i, axis in enumerate(self.axes):
            ticks = np.linspace(axis['min_value'], axis['max_value'], self._num_ticks)
            ticks_labels = [f"{t:.1f}" for t in ticks]

            # Compute text alignment based on angle
            label_angle = angles[i]
            angle_deg = np.degrees(label_angle)  # Convert radians to degrees

            if angle_deg == 90 or angle_deg == 270:
                ha = "center"  # Centered at top and bottom
            elif 90 < angle_deg < 270:
                ha = "right"  # Align right (left side of radar chart)
            else:
                ha = "left"  # Align left (right side of radar chart)

            if angle_deg == 0 or angle_deg == 180:
                va = "center"  # Centered at top and bottom
            elif angle_deg > 180:
                va = "top"  # Align
            else:
                va = "bottom"  # Align

            # Add axis label (category name)
            label_text = f"{axis['name']}" if axis['unit'] is None else f"{axis['name']}\n [{axis['unit']}]"
            ax.text(label_angle, self.DEFAULT_POSITION_LABEL, label_text,
                    horizontalalignment=ha, size=12, color='black', verticalalignment=va)

            # Process both grid lines and tick labels
            for j, (tick, tick_label) in enumerate(zip(ticks, ticks_labels)):
                # Compute radial position for each tick mark (scaled value)
                if axis['order'] == "descending":
                    radial_position = (axis['max_value'] - tick) / (axis['max_value'] - axis['min_value'])
                else:
                    radial_position = (tick - axis['min_value']) / (axis['max_value'] - axis['min_value'])

                # Draw grid line for this tick
                ax.plot([angles[i], angles[i]], [0, 1], color='gray', linewidth=1,
                        linestyle='--')

                # Skip the first tick label for better spacing (if needed)
                if (axis['order'] == "descending" and j == self._num_ticks - 1) or (
                        axis['order'] == "ascending" and j == 0):
                    continue  # Skip unwanted tick labels

                if (axis['order'] == "descending" and j == 0) or (
                        axis['order'] == "ascending" and j == self._num_ticks - 1):
                    # Add tick labels with correct alignment
                    ax.text(angles[i], radial_position * self.DEFAULT_POSITION_OUTER_TICK,
                            tick_label,
                            horizontalalignment=ha, size=10, color='black', verticalalignment=va)
                else:
                    # Add tick labels with correct alignment
                    ax.text(angles[i], radial_position, tick_label,
                            horizontalalignment='center',
                            size=10, color='black')

        # Draw the polygonal boundary (close the shape)
        polygon_values = [1] * num_vars
        polygon_values.append(polygon_values[0])  # Close the polygon by repeating the first value
        ax.plot(angles + [angles[0]], polygon_values, color="black", linewidth=2, linestyle="solid")

        # Set radial limits
        ax.set_ylim(0, y_lim)  # Set the radial limits to cover the normalized range of data

        # Adjust layout to prevent labels from being cropped
        plt.subplots_adjust(left=0.1, right=0.9, top=0.85, bottom=0.1)  # Adjust the plot margins
        plt.tight_layout(pad=2.0)  # Ensure enough space around the plot

        # Add legend
        ax.legend(loc="upper right", bbox_to_anchor=(1.1, 1.1))

        # Set title and show plot
        if self.title != "":
            plt.title(self.title)
        if filename:
            plt.savefig(filename, bbox_inches="tight", dpi=dpi)  # Ensure labels are not cropped
        else:
            plt.show()


# Example usage:
radar = RadarChart()
radar.add_axis("EROI", None, 2.5, 6.6, "value", order="ascending")
radar.add_axis("GHGEI", "gCO2eq/kWh", 20, 120, "value", order="descending")
radar.add_axis("BCR", None, 1, 2, "value", order="ascending")
radar.add_axis("Net Energy Compensation", "%", 0, 100, "percentage", order="ascending")
radar.add_axis("Harvested Electricity", "MWh/m2", 2, 4, "value", order="ascending")
radar.add_axis("Payback Time", "year", 30, 45, "value", order="descending")

# Add data
radar.add_data([3.56, 74.9, 1.66, 58, 2.36, 32], color="blue", label=" c-Si Low")
radar.add_data([3.49, 77.0, 1.65, 32.1, 2.57, 33], color="green", label=" c-Si Medium")
radar.add_data([3.19, 85.5, 1.55, 27.9, 3.33, 35], color="red", label=" c-Si High")
#
radar.add_data([6.55, 25.3, 1.76, 51.8, 2.09, 31], color="blue", style="--", label="CIGS Low")
radar.add_data([6.09, 27.3, 1.65, 33.4, 2.52, 33], color="green", style="--", label=" CIGS Medium")
radar.add_data([5.95,  28.3, 1.60, 28.0, 3.35, 34], color="red", style="--", label="CIGS High")

# Optionally, auto set boundaries
# radar.auto_set_boundaries()

# Plot or save the radar chart
radar.plot(filename="test", figsize=(8, 8), dpi=800)
