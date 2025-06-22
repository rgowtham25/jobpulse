# app.py
from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
from scrapers.google_job_scraper import fetch_job_links
from notifier.whatsapp_sender import send_whatsapp_message_custom

app = Dash(__name__)
app.title = "JobPulse WhatsApp Bot"

app.layout = html.Div(
    style={"fontFamily": "Arial", "margin": "50px"},
    children=[
        html.H2("📲 Job Alerts via WhatsApp"),
        html.Div("Enter job role, location, and your WhatsApp number (sandbox):"),
        
        html.Label("Job Role:"),
        dcc.Input(id='input-role', type='text', value='Data Analyst', style={"marginBottom": "10px"}),

        html.Br(),
        html.Label("Location:"),
        dcc.Input(id='input-location', type='text', value='Bangalore', style={"marginBottom": "10px"}),

        html.Br(),
        html.Label("WhatsApp Number (with +91):"),
        dcc.Input(id='input-number', type='text', value='+919750257792', style={"marginBottom": "20px"}),

        html.Br(),
        html.Button("🚀 Send Jobs to WhatsApp", id='submit-btn', n_clicks=0),
        html.Div(id='output-message', style={"marginTop": "20px", "fontWeight": "bold", "color": "green"}),
    ]
)

@app.callback(
    Output('output-message', 'children'),
    Input('submit-btn', 'n_clicks'),
    State('input-role', 'value'),
    State('input-location', 'value'),
    State('input-number', 'value')
)
def handle_submit(n_clicks, role, location, phone_number):
    if n_clicks == 0:
        return ""

    # Fetch jobs
    jobs = fetch_job_links(role, location, time_filter="h", max_pages=3)

    if not jobs:
        return "❌ No jobs found."

    # Send to WhatsApp
    success = send_whatsapp_message_custom(jobs, phone_number)
    if success:
        return f"✅ Sent {len(jobs)} job links to {phone_number}"
    else:
        return "❌ Failed to send WhatsApp message."

if __name__ == '__main__':
    app.run(debug=True)
