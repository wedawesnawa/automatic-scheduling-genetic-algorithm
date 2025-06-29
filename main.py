import streamlit as st
from pathlib import Path

from st_pages import add_page_title, get_nav_from_toml

st.set_page_config(layout="wide")

sections = st.sidebar.toggle("Sections", value=True, key="use_sections")

nav = get_nav_from_toml(
    ".streamlit/pages_sections.toml" if sections else ".streamlit/pages.toml"
)

logo_path = Path("logo.png")
if logo_path.exists():
    st.logo(logo_path)
else:
    st.warning("Logo not found.")

pg = st.navigation(nav)

add_page_title(pg)

pg.run()