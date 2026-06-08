import os
import requests
import gradio as gr

API_URL = os.getenv("API_URL", "http://localhost:8080")


def classify(property_type, area, owner_price):
    payload = {
        "properties": [
            {
                "property": {
                    "property_type": property_type,
                    "area": int(area),
                },
                "owner_price": float(owner_price),
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

    return result["predicted_price"], result["rating"]


demo = gr.Interface(
    fn=classify,
    inputs=[
        gr.Dropdown(["House", "Apartment"], label="Property type"),
        gr.Number(label="Area"),
        gr.Number(label="Owner price"),
    ],
    outputs=[
        gr.Number(label="Predicted price"),
        gr.Textbox(label="Rating"),
    ],
)

demo.launch(server_name="0.0.0.0", server_port=8081)