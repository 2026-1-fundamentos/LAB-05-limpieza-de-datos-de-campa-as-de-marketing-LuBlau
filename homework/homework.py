"""
Escriba el codigo que ejecute la accion solicitada.
"""

# pylint: disable=import-outside-toplevel

import glob
import os

import pandas as pd

def clean_campaign_data():
    """
    En esta tarea se le pide que limpie los datos de una campaña de
    marketing realizada por un banco, la cual tiene como fin la
    recolección de datos de clientes para ofrecerls un préstamo.

    La información recolectada se encuentra en la carpeta
    files/input/ en varios archivos csv.zip comprimidos para ahorrar
    espacio en disco.

    Usted debe procesar directamente los archivos comprimidos (sin
    descomprimirlos). Se desea partir la data en tres archivos csv
    (sin comprimir): client.csv, campaign.csv y economics.csv.
    Cada archivo debe tener las columnas indicadas.

    Los tres archivos generados se almacenarán en la carpeta files/output/.

    client.csv:
    - client_id
    - age
    - job: se debe cambiar el "." por "" y el "-" por "_"
    - marital
    - education: se debe cambiar "." por "_" y "unknown" por pd.NA
    - credit_default: convertir a "yes" a 1 y cualquier otro valor a 0
    - mortage: convertir a "yes" a 1 y cualquier otro valor a 0

    campaign.csv:
    - client_id
    - number_contacts
    - contact_duration
    - previous_campaing_contacts
    - previous_outcome: cmabiar "success" por 1, y cualquier otro valor a 0
    - campaign_outcome: cambiar "yes" por 1 y cualquier otro valor a 0
    - last_contact_day: crear un valor con el formato "YYYY-MM-DD",
        combinando los campos "day" y "month" con el año 202 2.

    economics.csv:
    - client_id
    - const_price_idx
    - eurobor_three_months



    """
    archivos = glob.glob("files/input/*.csv.zip")

    dataframes = []
    for archivo in archivos:
        df = pd.read_csv(archivo, compression="zip", sep=",")

        if df.columns[0].startswith(","):
            df = df.rename(columns={df.columns[0]: "index"})
            df = df.drop(columns=["index"])

        dataframes.append(df)

    dataframe = pd.concat(dataframes, ignore_index=True)


    os.makedirs("files/output", exist_ok=True)

    client = dataframe[
        [
            "client_id",
            "age",
            "job",
            "marital",
            "education",
            "credit_default",
            "mortgage",
        ]
    ].copy()

    client["job"] = (
        client["job"]
        .str.replace(".", "", regex=False)
        .str.replace("-", "_", regex=False)
    )

    client["education"] = (
        client["education"]
        .replace("unknown", pd.NA)
        .str.replace(".", "_", regex=False)
    )

    client["credit_default"] = (client["credit_default"] == "yes").astype(int)

    client["mortgage"] = (client["mortgage"] == "yes").astype(int)

    client.to_csv(
        "files/output/client.csv",
        index=False,
    )

    meses = {
        "jan": "01",
        "feb": "02",
        "mar": "03",
        "apr": "04",
        "may": "05",
        "jun": "06",
        "jul": "07",
        "aug": "08",
        "sep": "09",
        "oct": "10",
        "nov": "11",
        "dec": "12",
    }

    campaign = dataframe[
        [
            "client_id",
            "number_contacts",
            "contact_duration",
            "previous_campaign_contacts",
            "previous_outcome",
            "campaign_outcome",
            "day",
            "month",
        ]
    ].copy()

    campaign["previous_outcome"] = (
        campaign["previous_outcome"] == "success"
    ).astype(int)

    campaign["campaign_outcome"] = (
        campaign["campaign_outcome"] == "yes"
    ).astype(int)

    campaign["last_contact_date"] = (
        "2022-"
        + campaign["month"].map(meses)
        + "-"
        + campaign["day"].astype(int).astype(str).str.zfill(2)
    )

    campaign = campaign.drop(columns=["day", "month"])

    campaign.to_csv(
        "files/output/campaign.csv",
        index=False,
    )

    economics = dataframe[
        [
            "client_id",
            "cons_price_idx",
            "euribor_three_months",
        ]
    ].copy()

    economics.to_csv(
        "files/output/economics.csv",
        index=False,
    )


if __name__ == "__main__":
    clean_campaign_data()