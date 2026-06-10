import os
import requests
import gradio as gr

API_URL = os.getenv("API_URL", "http://localhost:8080")

PROPERTY_TYPES = ["House", "Apartment"]
NEIGHBORHOODS = ["Pocitos", "Cordón", "Centro", "Malvín", "Buceo", "Punta Carretas"]

COLUMNS = ["property_type", "area", "bedrooms", "bathrooms", "neighborhood"]


def render_properties(rows):
    if not rows:
        return "_No properties added yet._"

    lines = [
        "| # | Type | Area | Bedrooms | Bathrooms | Neighborhood |",
        "|---|------|------|----------|-----------|--------------|",
    ]

    for i, row in enumerate(rows, start=1):
        lines.append(
            f"| {i} | {row['property_type']} | {row['area']} | "
            f"{row['bedrooms']} | {row['bathrooms']} | {row['neighborhood']} |"
        )

    return "\n".join(lines)


def add_property(property_type, neighborhood, area, bedrooms, bathrooms, rows):
    rows = rows or []

    rows = rows + [{
        "property_type": property_type,
        "area": int(area),
        "bedrooms": int(bedrooms),
        "bathrooms": int(bathrooms),
        "neighborhood": neighborhood,
    }]

    return rows, render_properties(rows)


def remove_last(rows):
    rows = rows or []
    rows = rows[:-1]

    return rows, render_properties(rows)


def clear_properties():
    rows = []
    return rows, render_properties(rows), ""


def classify(rows):
    rows = rows or []

    if not rows:
        return "_No properties to predict._"

    payload = {
        "properties": rows
    }

    response = requests.post(
        f"{API_URL}/properties-valuation/houses",
        json=payload,
        timeout=10,
    )
    response.raise_for_status()

    results = response.json()["properties"]

    lines = [
        "| # | Type | Area | Bedrooms | Bathrooms | Neighborhood | Predicted price |",
        "|---|------|------|----------|-----------|--------------|-----------------|",
    ]

    for i, result in enumerate(results, start=1):
        p = result["property"]
        price = round(result["predicted_price"], 2)

        lines.append(
            f"| {i} | {p['property_type']} | {p['area']} | "
            f"{p['bedrooms']} | {p['bathrooms']} | {p['neighborhood']} | {price} |"
        )

    return "\n".join(lines)


with gr.Blocks(title="Property Valuation") as ui:
    gr.Markdown("# 🏠 Property Valuation")

    rows_state = gr.State([])

    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("## Add Property")

            property_type = gr.Dropdown(
                PROPERTY_TYPES,
                value="House",
                label="Property Type",
            )

            neighborhood = gr.Dropdown(
                NEIGHBORHOODS,
                value="Pocitos",
                label="Neighborhood",
            )

            area = gr.Number(label="Area (m²)", value=100)
            bedrooms = gr.Number(label="Bedrooms", value=2, precision=0)
            bathrooms = gr.Number(label="Bathrooms", value=1, precision=0)

            with gr.Row():
                add_btn = gr.Button("➕ Add")
                remove_btn = gr.Button("🗑 Remove Last")

            with gr.Row():
                clear_btn = gr.Button("Clear")
                predict_btn = gr.Button("🚀 Predict", variant="primary")

        with gr.Column(scale=2):
            gr.Markdown("## Properties")
            properties_view = gr.Markdown("_No properties added yet._")

            gr.Markdown("## Predictions")
            predictions_view = gr.Markdown("")

    add_btn.click(
        fn=add_property,
        inputs=[property_type, neighborhood, area, bedrooms, bathrooms, rows_state],
        outputs=[rows_state, properties_view],
    )

    remove_btn.click(
        fn=remove_last,
        inputs=rows_state,
        outputs=[rows_state, properties_view],
    )

    clear_btn.click(
        fn=clear_properties,
        outputs=[rows_state, properties_view, predictions_view],
    )

    predict_btn.click(
        fn=classify,
        inputs=rows_state,
        outputs=predictions_view,
    )


ui.launch(server_name="0.0.0.0", server_port=8081)