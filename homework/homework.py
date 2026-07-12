"""
Escriba el codigo que ejecute la accion solicitada.
"""

# pylint: disable=import-outside-toplevel


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
        combinando los campos "day" y "month" con el año 2022.

    economics.csv:
    - client_id
    - const_price_idx
    - eurobor_three_months



    """
    import os
    import glob
    import pandas as pd # type:ignore

    os.makedirs("files/output", exist_ok=True)

    archivos = sorted(glob.glob("files/input/*.csv.zip"))

    tablas = []

    for archivo in archivos:
        tablas.append(pd.read_csv(archivo, compression="zip"))

    datos = pd.concat(tablas, ignore_index=True)

    datos.insert(0, "client_id", range(len(datos)))

    #
    # client.csv
    #
    client = pd.DataFrame()

    client["client_id"] = datos["client_id"]
    client["age"] = datos["age"]

    client["job"] = (
        datos["job"]
        .str.replace(".", "", regex=False)
        .str.replace("-", "_", regex=False)
    )

    client["marital"] = datos["marital"]

    client["education"] = (
        datos["education"]
        .replace("unknown", pd.NA)
        .str.replace(".", "_", regex=False)
    )

    client["credit_default"] = datos["default"].map(
        lambda x: 1 if x == "yes" else 0
    )

    client["mortgage"] = datos["housing"].map(
        lambda x: 1 if x == "yes" else 0
    )

    client.to_csv(
        "files/output/client.csv",
        index=False,
    )

    #
    # campaign.csv
    #
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

    campaign = pd.DataFrame()

    campaign["client_id"] = datos["client_id"]
    campaign["number_contacts"] = datos["campaign"]
    campaign["contact_duration"] = datos["duration"]
    campaign["previous_campaign_contacts"] = datos["previous"]

    campaign["previous_outcome"] = datos["poutcome"].map(
        lambda x: 1 if x == "success" else 0
    )

    campaign["campaign_outcome"] = datos["y"].map(
        lambda x: 1 if x == "yes" else 0
    )

    campaign["last_contact_date"] = (
        "2022-"
        + datos["month"].map(meses)
        + "-"
        + datos["day"].astype(str).str.zfill(2)
    )

    campaign.to_csv(
        "files/output/campaign.csv",
        index=False,
    )

    #
    # economics.csv
    #
    economics = pd.DataFrame()

    economics["client_id"] = datos["client_id"]
    economics["cons_price_idx"] = datos["cons.price.idx"]
    economics["euribor_three_months"] = datos["euribor3m"]

    economics.to_csv(
        "files/output/economics.csv",
        index=False,
    )


if __name__ == "__main__":
    clean_campaign_data()
