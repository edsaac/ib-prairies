import requests

COOK_COUNTY_GIS_URL = (
    "https://gis.cookcountyil.gov/imagery/rest/services/CookOrtho2023/ImageServer"
)


def get_tile_id(tile_number: list[str]):
    # SQL Query
    str_tiles = ",".join(tile_number)
    sql_query = f"Name IN ({str_tiles})"

    # REST API endpoint
    url = f"{COOK_COUNTY_GIS_URL}/query"

    # Adding parameters to query
    payload = dict(
        where=sql_query,
        returnIdsOnly=True,
        returnGeometry=True,
        f="pjson",
    )

    # A get request to the API
    response = requests.get(url, params=payload)
    response.raise_for_status()
    return response.json()


def get_tif_download_urls(tile_id):
    global COOK_COUNTY_GIS_URL

    # REST API endpoint
    url = url = f"{COOK_COUNTY_GIS_URL}/download"

    # Adding parameters to query
    payload = dict(rasterIds=tile_id, format="tif", f="pjson")

    # A get request to the API
    response = requests.get(url, params=payload)
    response.raise_for_status()
    return response.json()
