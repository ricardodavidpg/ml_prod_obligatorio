import gradio as gr

def classify(property_type, area, owner_price):
    predicted_price = area * 1500

    if owner_price > predicted_price * 1.1:
        rating = "Overpriced"
    elif owner_price < predicted_price * 0.9:
        rating = "Underpriced"
    else:
        rating = "Fairly priced"

    return predicted_price, rating

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