import io
import re

import pandas as pd
from tqdm import tqdm


def read_html_in_chunks(file_path, headers, chunk_size=10000):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        rows = re.findall(r'<tr.*?/tr>', content, re.DOTALL)
        rows = rows[1:]

        dfs = []
        for i in tqdm(range(0, len(rows), chunk_size), desc="Processing Chunks"):
            chunk = ''.join(rows[i:i + chunk_size])
            chunk = f'<table>{chunk}</table>'
            chunk_io = io.StringIO(chunk)

            df = pd.read_html(chunk_io, header=None, keep_default_na=False, flavor='lxml')[0]
            df.columns = headers
            dfs.append(df)

        final_df = pd.concat(dfs, ignore_index=True)
        return final_df

    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return None