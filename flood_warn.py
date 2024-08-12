import pandas as pd
import streamlit as st
from sodapy import Socrata


url = "data.cityofchicago.org"
resource = "v6vf-nfxy"
client = Socrata(url, app_token=st.secrets.socrata.app_token)

results = client.get(resource, limit=100)
df = pd.DataFrame.from_records(results)
st.dataframe(df)
