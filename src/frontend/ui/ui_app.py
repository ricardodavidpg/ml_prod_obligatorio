import os
import requests
import gradio as gr

API_URL = os.getenv("API_URL", "http://localhost:8080")


def classify(property_type, area, bedrooms, bathrooms, neighborhood):
    payload = {
        "properties": [
            {
                "property_type": property_type,
                "area": int(area),
                "bedrooms": int(bedrooms),
                "bathrooms": int(bathrooms),
                "neighborhood": neighborhood,
            }
        ]
    }

    response = requests.post(
        f"{API_URL}/properties-valuation/houses",
        json=payload,
        timeout=10,
    )

    response.raise_for_status()

    result = response.json()["properties"][0]

    return result["predicted_price"]


ui = gr.Interface(
    fn=classify,
    inputs=[
        gr.Dropdown(["House", "Apartment"], label="Property type"),
        gr.Number(label="Area (m²)"),
        gr.Number(label="Bedrooms", precision=0),
        gr.Number(label="Bathrooms", precision=0),
        gr.Textbox(label="Neighborhood"),
    ],
    outputs=[
        gr.Number(label="Predicted price"),
    ],
)

ui.launch(server_name="0.0.0.0", server_port=8081)