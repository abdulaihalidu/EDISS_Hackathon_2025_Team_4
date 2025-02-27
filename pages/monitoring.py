import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import cv2
import threading
import base64
import time
from ultralytics import YOLO

# Register the page with Dash
dash.register_page(__name__, path="/monitoring")

# Dummy Data for Dropdowns
PLANTS = ["Plant A", "Plant B", "Plant C"]
ZONES = {
    "Plant A": ["Zone 1", "Zone 2"],
    "Plant B": ["Zone 3", "Zone 4"],
    "Plant C": ["Zone 5"]
}

# Video Source 
video_source = "BoxesVideo.mp4"

# Threading globals for video processing
frame_lock = threading.Lock()
latest_frame = None
processing_thread = None
video_running = False  # Global flag to track if the video is running

# Load the Model
model = YOLO("./yolov8m.pt")

def process_video():
    global latest_frame, video_running
    cap = cv2.VideoCapture(video_source) 
    if not cap.isOpened():
        print("Error: Unable to open video file.")
        video_running = False
        return
    skip_interval = 20
    frame_cnt = 0
    while video_running:
        ret, frame = cap.read()
        if not ret:
            video_running = False  # End processing when video is finished
            break
        
        frame_cnt += 1
        if frame_cnt % skip_interval != 0:
            continue
        
        # Run YOLO inference and draw bounding boxes
        results = model(frame)
        annotated_frame = results[0].plot()

        # Encode frame as JPEG for web display
        _, buffer = cv2.imencode(".jpg", annotated_frame)
        frame_bytes = buffer.tobytes()

        with frame_lock:
            latest_frame = base64.b64encode(frame_bytes).decode("utf-8")

    cap.release()

# Layout Definition
layout = dbc.Container([
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardHeader(html.H2("Real-Time Monitoring", className="text-center")),
            dbc.CardBody([
                html.Label("Select Plant:", className="fw-bold"),
                dcc.Dropdown(
                    id="plant-dropdown", 
                    options=[{"label": p, "value": p} for p in PLANTS],
                    placeholder="Select a plant"
                ),
                html.Br(),
                html.Label("Select Zone:", className="fw-bold"),
                dcc.Dropdown(id="zone-dropdown", placeholder="Select a zone"),
                html.Br(),
                dbc.Button("Start Monitoring", id="start-monitoring", color="primary", className="mt-3"),
                html.Br(), html.Br(),
                html.Img(
                    id="video-feed",
                    style={
                        "width": "100%",
                        "border-radius": "5px",
                        "box-shadow": "2px 2px 10px #aaa"
                    }
                ),
                # Interval to refresh frames every 50ms (initially disabled)
                dcc.Interval(id="frame-update", interval=50, n_intervals=0, disabled=True),
                # Hidden store to hold video running state
                dcc.Store(id="video-running-store", data=False),
                # Div to show status messages
                html.Div(id="status-output", className="mt-3")
            ])
        ], className="shadow p-4"), width=8)
    ], justify="center")
], className="mt-4")

# Callback to update the Zone dropdown based on the selected Plant
@dash.callback(
    Output("zone-dropdown", "options"),
    Input("plant-dropdown", "value")
)
def update_zones(selected_plant):
    if selected_plant:
        return [{"label": z, "value": z} for z in ZONES.get(selected_plant, [])]
    return []

# Callback to toggle monitoring when the button is clicked.
# This callback resets the frame counter, updates the video-running store,
# updates the status message and toggles the button text.
@dash.callback(
    [Output("frame-update", "n_intervals"),
     Output("video-running-store", "data"),
     Output("status-output", "children"),
     Output("start-monitoring", "children")],
    Input("start-monitoring", "n_clicks"),
    State("video-running-store", "data"),
    prevent_initial_call=True
)
def toggle_monitoring(n_clicks, running_state):
    global video_running, processing_thread
    if not running_state:
        video_running = True
        processing_thread = threading.Thread(target=process_video, daemon=True)
        processing_thread.start()
        status_message = "✅ Monitoring started..."
        button_text = "Stop Monitoring"
        return 0, True, status_message, button_text
    else:
        video_running = False
        status_message = "🛑 Monitoring stopped."
        button_text = "Start Monitoring"
        return dash.no_update, False, status_message, button_text

# Callback to continuously update the video feed and control the interval.
@dash.callback(
    [Output("video-feed", "src"),
     Output("frame-update", "disabled")],
    [Input("frame-update", "n_intervals"),
     Input("video-running-store", "data")]
)
def update_video(n_intervals, running_state):
    global video_running
    with frame_lock:
        src = f"data:image/jpeg;base64,{latest_frame}" if latest_frame else dash.no_update

    # Disable the interval if the video is not running.
    if not running_state or not video_running:
        return src, True

    return src, False
