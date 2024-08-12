import dataretrieval.nwis as nwis
import folium
import streamlit as st
from streamlit_folium import st_folium
from datetime import date
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from functools import partial


def _get_station_name(site: str, info: pd.DataFrame):
    return info[info["site_no"] == site]["station_nm"].values[0]


def main():
    # specify the USGS site code for which we want data.
    sites = [
        "413548087395901",  # Begin date is 2019-11-27
        "413516087442101",  # Begin date is 2019-06-27
    ]

    # get basic info about the sites
    basic_info = nwis.get_record(sites=sites, service="site")
    get_station_name = partial(_get_station_name, info=basic_info)

    st.dataframe(basic_info)

    m = folium.Map(
        location=[basic_info["dec_lat_va"].mean(), basic_info["dec_long_va"].mean()],
        zoom_start=13,
    )

    for idx, site in basic_info.iterrows():
        folium.Marker(
            [site["dec_lat_va"], site["dec_long_va"]],
            popup=site["station_nm"],
            tooltip=site["station_nm"],
        ).add_to(m)

    st_folium(m, use_container_width=True, height=400, returned_objects=None)

    # get instantaneous values (iv)
    data_filepath = Path("data/Precipitation/NWIS - USGS/precipitation.parquet")
    try:
        st.info("Loading data from cache...")
        data = pd.read_parquet(data_filepath)

    except FileNotFoundError:
        st.info("Data not found in cache. Fetching data from NWIS...")
        data = nwis.get_record(
            sites=sites, service="iv", start="2019-11-27", end=date.today()
        )
        data.to_parquet(data_filepath)

    site = st.selectbox("Select a site", sites, format_func=get_station_name)

    if site:
        site_data = data.loc[site]
        station_name = get_station_name(site)
        st.markdown(f"{station_name} - {site}")
        st.dataframe(site_data)

        # Plot the data
        fig, ax = plt.subplots()
        ax.plot(site_data.index, site_data["00045"], lw=1)
        ax.set_title("Precipitation")
        ax.set_xlabel("Date Time")
        ax.set_ylabel("Precipitation (mm)")
        ax.spines.right.set_visible(False)
        ax.spines.top.set_visible(False)
        st.pyplot(fig)

    # Get info about the data
    # codes = [x for x in data.columns.tolist() if "_cd" not in x]
    # df, _ = nwis.get_pmcodes(parameterCd=codes, partial=False)


if __name__ == "__main__":
    main()
