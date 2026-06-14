import json
import pandas as pd
from io import BytesIO


def export_csv(df):

    return df.to_csv(
        index=False
    ).encode("utf-8")


def export_excel(df):

    output = BytesIO()

    with pd.ExcelWriter(
        output,
        engine="xlsxwriter"
    ) as writer:

        df.to_excel(
            writer,
            index=False,
            sheet_name="Hasil Clustering"
        )

    return output.getvalue()


def export_json(df):

    return json.dumps(
        df.to_dict(
            orient="records"
        ),
        indent=4,
        ensure_ascii=False
    )
