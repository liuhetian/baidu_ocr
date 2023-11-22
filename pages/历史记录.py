import base64, urllib.parse, requests, json, os
from pathlib import Path
os.environ['STREAMLIT_SERVER_ENABLE_STATIC_SERVING'] = 'true'

import pandas as pd
import streamlit as st

directory = Path('static/')
file_list = list(directory.glob('*'))
file_list = [file_path for file_path in file_list if not file_path.name.startswith('.')]


data_df = pd.DataFrame(
    {
        "apps": ['app/static/'+i.name for i in file_list],
        "文件名": [i.name for i in file_list]
    },
    
)

with open('result.txt', 'r') as f:
    results = eval(f.read())
    
data_df['识别结果'] = data_df['文件名'].map(results)

st.data_editor(
    data_df,
    column_config={
        "apps": st.column_config.ImageColumn(
            "Preview Image", help="Streamlit app preview screenshots"
        )
    },
    hide_index=True,
    use_container_width=True
)
