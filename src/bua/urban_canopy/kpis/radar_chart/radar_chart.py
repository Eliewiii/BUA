import numpy as np
import matplotlib.pyplot as plt


class RadarChart:
    DEFAULT_NUM_TICK = 6

    DEFAULT_POSITION_LABEL = 1.15
    DEFAULT_POSITION_OUTER_TICK = 1.01
    DEFAULT_TICK_LENGTH = 0.1

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

        plt.rcParams.update({
            "font.family": "Arial",  # e.g. "sans-serif", "serif", "monospace"
        })

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
                    normalized_value = (value - min_value) / (max_value - min_value) *(1-1/(self._num_ticks-1)) + 1/(self._num_ticks-1) # Normalize to [0, 1]
                else:
                    # Normalizing for descending axis (flip the scale)
                    normalized_value = (max_value - value) / (max_value - min_value)*(1-1/(self._num_ticks-1))+ 1/(self._num_ticks-1)  # Inverted scale

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
            ticks = np.linspace(axis['min_value'], axis['max_value'], self._num_ticks-1)
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

            # # # Add axis label (category name)
            # label_text = f"{axis['name']}" if axis['unit'] is None else f"{axis['name']}\n[{axis['unit']}]"
            # ax.text(label_angle, self.DEFAULT_POSITION_LABEL, label_text,
            #         horizontalalignment=ha, size=12, color='black', verticalalignment=va)

            # Process both grid lines and tick labels
            for j, (tick, tick_label) in enumerate(zip(ticks, ticks_labels)):
                # Compute radial position for each tick mark (scaled value)
                if axis['order'] == "descending":
                    radial_position = (axis['max_value'] - tick) / (axis['max_value'] - axis['min_value'])*(1-1/(self._num_ticks-1)) + 1/(self._num_ticks-1)
                else:
                    radial_position = (tick - axis['min_value']) / (axis['max_value'] - axis['min_value'])*(1-1/(self._num_ticks-1)) + 1/(self._num_ticks-1)


                # Draw grid line for this tick
                ax.plot([angles[i], angles[i]], [1/(self._num_ticks-1), 1], color='gray', linewidth=0.8,
                        linestyle='--')

                # ax.plot([angles[i], angles[i]], [0, 1], color='gray', linewidth=1,
                #         linestyle='--')

                # Skip the first tick label for better spacing (if needed)
                if (axis['order'] == "descending" and j == self._num_ticks - 1):
                    continue  # Skip unwanted tick labels

                if (axis['order'] == "descending" and j == 0) or (
                        axis['order'] == "ascending" and j == self._num_ticks - 1):

                    # # Add tick labels with correct alignment
                    # ax.text(angles[i], radial_position * self.DEFAULT_POSITION_OUTER_TICK,
                    #         tick_label,
                    #         horizontalalignment=ha, size=10, color='black', verticalalignment=va)
                    None

                else:
                    if (self._num_ticks%2==0 and j%2 == 0) or (self._num_ticks%2!=0 and j%2 != 0):

                        # # Add tick labels with correct alignment
                        # ax.text(angles[i], radial_position, tick_label,
                        #         horizontalalignment='center',
                        #         size=10, color='black')
                        None

                    if axis['order'] == "ascending" and j == self._num_ticks - 2:
                        continue
                    # === NEW CODE: draw perpendicular tick marks in polar coords ===
                    theta = angles[i]

                    # Small angular offset for tick mark (controls tick length)
                    delta_theta = 0.02  # adjust for longer/shorter ticks


                    ax.plot(
                        [(theta - delta_theta / radial_position), (theta + delta_theta / radial_position)],
                        [radial_position, radial_position],
                        color="black", linewidth=1.2)



        # Draw the polygonal boundary (close the shape)
        polygon_values = [1] * num_vars
        polygon_values.append(polygon_values[0])  # Close the polygon by repeating the first value
        ax.plot(angles + [angles[0]], polygon_values, color="black", linewidth=1.5, linestyle="solid")

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
radar.add_axis("EROI", None, 2, 10, "value", order="ascending")
radar.add_axis("GHGEI", "gCO2eq/kWh", 20, 130, "value", order="descending")
radar.add_axis("BCR", None, 1, 2, "value", order="ascending")
radar.add_axis("Net Energy Compensation", "%", 0, 100, "percentage", order="ascending")
radar.add_axis("Harvested Electricity", "MWh/m2", 1.5, 6, "value", order="ascending")
radar.add_axis("Net profit density", "usd/m2", 70, 200, "value", order="ascending")
radar.add_axis("Payback Time", "year", 0, 15, "value", order="descending")
radar.add_axis("Payback Time 2", "year", 0, 15, "value", order="descending")
radar.add_axis("Payback Time 3", "year", 25, 50, "value", order="descending")





#Sustanainble
radar.add_data([4.40 , 64.0 , 1.83 , 52.8, 2.13, 136 , 3.94 , 4.89 , 29.0], color="blue", label="Sustainable Low")
radar.add_data([4.20 , 67.3 , 1.79 , 28.8 , 2.31 , 143 , 4.70 , 4.97 , 30.0], color="green", label="Sustainable Medium")
radar.add_data([4.12 , 68.6 , 1.79 , 21.2 , 2.53 , 156 , 4.72 , 5.74 , 30.0], color="red", label="Sustainable High")

# Balanced
radar.add_data([3.59 , 79 , 1.64 , 72.4 , 2.92 , 159 , 4.99 , 6.80 , 34.9], color="cornflowerblue", label="Balanced Low")
radar.add_data([3.35 , 85 , 1.56 , 41.8 , 3.35 , 169 , 5.83 , 6.90 , 36.0], color="mediumseagreen", label="Balanced Medium")
radar.add_data([3.15 , 90.5 , 1.51 , 35.2 , 4.20 , 199 , 5.92 , 7.81 , 37.9], color="lightcoral", label="Balanced High")
#
#
# # Production
radar.add_data([2.82 , 101 , 1.41 , 80.0 , 3.23 , 130 , 6.98 , 8.93 , 41.9], color="cyan", label="Production Low")
radar.add_data([2.52 , 113 , 1.30 , 48.8 , 3.91 , 128 , 7.95 , 9.95 , 44.9], color="limegreen", label="Production Medium")
radar.add_data([2.33 , 123 , 1.24 , 42.6 , 5.07 , 138 , 8.91 , 10.9 , 46.9], color="magenta", label="Production High")

# Optionally, auto set boundaries
# radar.auto_set_boundaries()

# Plot or save the radar chart
radar.plot(filename="C_SI_no_lable", figsize=(8, 8), dpi=300,y_lim=1.5)


# Example usage:
radar_cigs = RadarChart()
radar_cigs.add_axis("EROI", None, 2, 10, "value", order="ascending")
radar_cigs.add_axis("GHGEI", "gCO2eq/kWh", 20, 130, "value", order="descending")
radar_cigs.add_axis("BCR", None, 1, 2, "value", order="ascending")
radar_cigs.add_axis("Net Energy Compensation", "%", 0, 100, "percentage", order="ascending")
radar_cigs.add_axis("Harvested Electricity", "MWh/m2", 1.5, 6, "value", order="ascending")
radar_cigs.add_axis("Net profit density", "usd/m2", 70, 200, "value", order="ascending")
radar_cigs.add_axis("Payback Time", "year", 0, 15, "value", order="descending")
radar_cigs.add_axis("Payback Time 2", "year", 0, 15, "value", order="descending")
radar_cigs.add_axis("Payback Time 3", "year", 25, 50, "value", order="descending")


#Sustanainble CIGS
radar_cigs.add_data([8.69 , 23.3 , 1.56 , 48.5 , 1.96 , 98.8 , 1.94 , 1.76 , 34.0], color="blue", label="Sustainable Low")
radar_cigs.add_data([8.37 , 24.3 , 1.53 , 25.4 , 2.04 , 98.5 , 2.55 , 1.81 , 35.9], color="green", label="Sustainable Medium")
radar_cigs.add_data([7.99 , 25.3 , 1.51 , 22.6 , 2.70 , 128 , 2.58 , 1.87 , 35.9], color="red", label="Sustainable High")

# Balanced
radar_cigs.add_data([8.18 , 24.7 , 1.50 , 56.4 , 2.27 , 107 , 2.61 , 1.90 , 37.9], color="cornflowerblue", label="Balanced Low")
radar_cigs.add_data([7.60 , 26.6 , 1.44 , 33.0 , 2.65 , 114 , 2.68 , 2.56 , 39.9], color="mediumseagreen", label="Balanced Medium")
radar_cigs.add_data([7.35 , 27.4 , 1.43 , 28.7 , 3.42 , 144 , 2.71 , 2.58 , 40.0], color="lightcoral", label="Balanced High")
#
#
# # Production
radar_cigs.add_data([6.69 , 30.1 , 1.29 , 61.5 , 2.48 , 78.4 , 2.94 , 2.77 , 45.0], color="cyan", label="Production Low")
radar_cigs.add_data([5.85 , 34.3 , 1.19 , 39.3 , 3.15 , 70.5 , 3.76 , 2.92 , 48.9], color="limegreen", label="Production Medium")
radar_cigs.add_data([5.62 , 35.7 , 1.18 , 34.6 , 4.12 , 86.5 , 3.80 , 2.97 , 49.8], color="magenta", label="Production High")



# Plot or save the radar chart
radar_cigs.plot(filename="CIGS_no_label", figsize=(8, 8), dpi=300,y_lim=1.5)




# Low
radar_low = RadarChart()
radar_low.add_axis("EROI", None, 2, 10, "value", order="ascending")
radar_low.add_axis("GHGEI", "gCO2eq/kWh", 20, 130, "value", order="descending")
radar_low.add_axis("BCR", None, 1, 2, "value", order="ascending")
radar_low.add_axis("Net Energy Compensation", "%", 0, 100, "percentage", order="ascending")
radar_low.add_axis("Harvested Electricity", "MWh/m2", 1.5, 6, "value", order="ascending")
radar_low.add_axis("Net profit density", "usd/m2", 70, 200, "value", order="ascending")
radar_low.add_axis("Payback Time", "year", 0, 15, "value", order="descending")
radar_low.add_axis("Payback Time 2", "year", 0, 15, "value", order="descending")
radar_low.add_axis("Payback Time 3", "year", 25, 50, "value", order="descending")

radar_low.add_data([4.40 , 64.0 , 1.83 , 52.8, 2.13, 136 , 3.94 , 4.89 , 29.0], color="black", style="-", label="Sustainable c-Si Low")
radar_low.add_data([3.59 , 79 , 1.64 , 72.4 , 2.92 , 159 , 4.99 , 6.80 , 34.9], color="darkgray",style="-", label="Balanced c-Si Low")
radar_low.add_data([2.82 , 101 , 1.41 , 80.0 , 3.23 , 130 , 6.98 , 8.93 , 41.9], color="lightgrey",style="-", label="Production c-Si Low")

radar_low.add_data([8.69 , 23.3 , 1.56 , 48.5 , 1.96 , 98.8 , 1.94 , 1.76 , 34.0], color="black", style="--", label="Sustainable CIGS Low")
radar_low.add_data([8.18 , 24.7 , 1.50 , 56.4 , 2.27 , 107 , 2.61 , 1.90 , 37.9], color="darkgray",style="--", label="Balanced CIGS Low")
radar_low.add_data([6.69 , 30.1 , 1.29 , 61.5 , 2.48 , 78.4 , 2.94 , 2.77 , 45.0], color="lightgrey",style="--", label="Production Low")

radar_low.plot(filename="low_no_label", figsize=(8, 8), dpi=300,y_lim=1.5)


# Medium
radar_medium = RadarChart()
radar_medium.add_axis("EROI", None, 2, 10, "value", order="ascending")
radar_medium.add_axis("GHGEI", "gCO2eq/kWh", 20, 130, "value", order="descending")
radar_medium.add_axis("BCR", None, 1, 2, "value", order="ascending")
radar_medium.add_axis("Net Energy Compensation", "%", 0, 100, "percentage", order="ascending")
radar_medium.add_axis("Harvested Electricity", "MWh/m2", 1.5, 6, "value", order="ascending")
radar_medium.add_axis("Net profit density", "usd/m2", 70, 200, "value", order="ascending")
radar_medium.add_axis("Payback Time", "year", 0, 15, "value", order="descending")
radar_medium.add_axis("Payback Time 2", "year", 0, 15, "value", order="descending")
radar_medium.add_axis("Payback Time 3", "year", 25, 50, "value", order="descending")

radar_medium.add_data([4.20 , 67.3 , 1.79 , 28.8 , 2.31 , 143 , 4.70 , 4.97 , 30.0], color="black", style="-", label="Sustainable c-Si medium")
radar_medium.add_data([3.35 , 85 , 1.56 , 41.8 , 3.35 , 169 , 5.83 , 6.90 , 36.0], color="darkgray",style="-", label="Balanced c-Si medium")
radar_medium.add_data([2.52 , 113 , 1.30 , 48.8 , 3.91 , 128 , 7.95 , 9.95 , 44.9], color="lightgrey",style="-", label="Production c-Si medium")

radar_medium.add_data([8.37 , 24.3 , 1.53 , 25.4 , 2.04 , 98.5 , 2.55 , 1.81 , 35.9], color="black", style="--", label="Sustainable CIGS medium")
radar_medium.add_data([7.60 , 26.6 , 1.44 , 33.0 , 2.65 , 114 , 2.68 , 2.56 , 39.9], color="darkgray",style="--", label="Balanced CIGS medium")
radar_medium.add_data([5.85 , 34.3 , 1.19 , 39.3 , 3.15 , 70.5 , 3.76 , 2.92 , 48.9], color="lightgrey",style="--", label="Production medium")
radar_medium.plot(filename="medium_no_label", figsize=(8, 8), dpi=300,y_lim=1.5)


# High
radar_high = RadarChart()
radar_high.add_axis("EROI", None, 2, 10, "value", order="ascending")
radar_high.add_axis("GHGEI", "gCO2eq/kWh", 20, 130, "value", order="descending")
radar_high.add_axis("BCR", None, 1, 2, "value", order="ascending")
radar_high.add_axis("Net Energy Compensation", "%", 0, 100, "percentage", order="ascending")
radar_high.add_axis("Harvested Electricity", "MWh/m2", 1.5, 6, "value", order="ascending")
radar_high.add_axis("Net profit density", "usd/m2", 70, 200, "value", order="ascending")
radar_high.add_axis("Payback Time", "year", 0, 15, "value", order="descending")
radar_high.add_axis("Payback Time 2", "year", 0, 15, "value", order="descending")
radar_high.add_axis("Payback Time 3", "year", 25, 50, "value", order="descending")

radar_high.add_data([4.20 , 67.3 , 1.79 , 28.8 , 2.31 , 143 , 4.70 , 4.97 , 30.0], color="black", style="-", label="Sustainable c-Si high")
radar_high.add_data([3.35 , 85 , 1.56 , 41.8 , 3.35 , 169 , 5.83 , 6.90 , 36.0], color="darkgray",style="-", label="Balanced c-Si high")
radar_high.add_data([2.52 , 113 , 1.30 , 48.8 , 3.91 , 128 , 7.95 , 9.95 , 44.9], color="lightgrey",style="-", label="Production c-Si high")

radar_high.add_data([8.37 , 24.3 , 1.53 , 25.4 , 2.04 , 98.5 , 2.55 , 1.81 , 35.9], color="black", style="--", label="Sustainable CIGS high")
radar_high.add_data([7.60 , 26.6 , 1.44 , 33.0 , 2.65 , 114 , 2.68 , 2.56 , 39.9], color="darkgray",style="--", label="Balanced CIGS high")
radar_high.add_data([5.85 , 34.3 , 1.19 , 39.3 , 3.15 , 70.5 , 3.76 , 2.92 , 48.9], color="lightgrey",style="--", label="Production high")
radar_high.plot(filename="high_no_label", figsize=(8, 8), dpi=300,y_lim=1.5)

