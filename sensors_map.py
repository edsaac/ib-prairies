import matplotlib.pyplot as plt
import folium
import streamlit as st
from streamlit_folium import st_folium
import pandas as pd
from pathlib import Path

WL_POSITION_META = Path("data/Processed Water Level Data/wl_position_meta.csv")


def main():
    sensors_metadata = pd.read_csv(WL_POSITION_META)
    without_dups = sensors_metadata.drop_duplicates(subset=["sensor"], keep="last")
    st.dataframe(without_dups)

    gw_sensors = sensors_metadata[sensors_metadata["sensor"].str.contains("WLW")]
    st.write("Sensor Locations")
    st.dataframe(gw_sensors)

    m = folium.Map(
        location=[
            gw_sensors["latitude"].mean(),
            gw_sensors["longitude"].mean(),
        ],
        zoom_start=15,
    )

    for idx, sensor in gw_sensors.iterrows():
        folium.Marker(
            [sensor["latitude"], sensor["longitude"]],
            # popup=sensor["sensor"],
            tooltip=sensor["sensor"],
            icon=folium.Icon(color="lightred", icon="arrow-up", prefix="fa"),
        ).add_to(m)

    st_folium(m, use_container_width=True, height=400, returned_objects=None)


if __name__ == "__main__":
    main()
