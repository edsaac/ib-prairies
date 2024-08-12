import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime
from natsort import natsorted
import numpy as np

LOCATION_PATH = Path("data/Processed Water Level Data/wl_position_meta.csv")


def main():
    ## Layout
    filters_plh = st.container()
    plot_plh = st.container()

    with filters_plh:
        df = pd.read_csv(LOCATION_PATH)

        sw_sensors = natsorted(
            set(df["sensor"].loc[df["sensor"].str.contains("WLS")].values)
        )

        gw_sensors = natsorted(
            set(df["sensor"].loc[df["sensor"].str.contains("WLW")].values)
        )

        cols = st.columns(2)

        with cols[0]:
            sw_selection = st.multiselect("Surface water sensors", sw_sensors)

        with cols[1]:
            gw_selection = st.multiselect("Groundwater sensors", gw_sensors)

    with plot_plh:
        if sw_selection or gw_selection:
            selections = sw_selection + gw_selection

            if len(selections) > 5:
                st.warning("Too many sensors selected. Please select 5 or less.")
                st.stop()

            fig, ax = plt.subplots()
            fig2, ax2 = plt.subplots()

            for sensor_id in selections:
                file_path = LOCATION_PATH.parent / f"{sensor_id}_ibp_main.csv"
                data = pd.read_csv(file_path)
                data["date_time"] = pd.to_datetime(data["date_time"])
                ax.plot("date_time", "WS_elevation_m", data=data, lw=1, label=sensor_id)
                ax2.hist(data["WS_elevation_m"], bins="scott")
                # ax.plot("qual_c", "WS_elevation_m", data=data, lw=1, label=sensor_id)

            ax.legend(title="Sensor ID")
            ax.set_title("Water Levels")
            ax.set_xlabel("Date Time")
            ax.set_ylabel("Water Level (m)")
            # ax.set_xlim(datetime(2019, 1, 1), datetime(2020, 1, 1))
            ax.spines.right.set_visible(False)
            ax.spines.top.set_visible(False)
            st.pyplot(fig)
            st.pyplot(fig2)


if __name__ == "__main__":
    main()
