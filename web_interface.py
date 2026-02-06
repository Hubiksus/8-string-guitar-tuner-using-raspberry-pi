"""
Web interface module
Flask-based web server for remote control and monitoring
"""

from flask import Flask, request, jsonify, render_template_string
import threading
from tuning import TuningManager
from config import WEB_HOST, WEB_PORT


# HTML template for the web interface
HTML_TEMPLATE = """ 
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Zajebisty Stroik Inator</title>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    color: #eee;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 20px;
}
.container {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 20px;
    padding: 40px;
    max-width: 600px;
    width: 100%;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    backdrop-filter: blur(10px);
}
h1 {
    text-align: center;
    margin-bottom: 30px;
    color: #00d4ff;
    font-size: 2.5em;
    text-shadow: 0 0 20px rgba(0, 212, 255, 0.5);
}
h2 {
    text-align: center;
    margin: 25px 0 15px;
    color: #fff;
    font-size: 1.5em;
}
.guitar-select, .tuning-select {
    display: flex;
    flex-direction: column;
    gap: 15px;
    margin-top: 20px;
}
button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border: none;
    padding: 18px;
    border-radius: 12px;
    color: white;
    font-size: 18px;
    font-weight: bold;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}
button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
}
button:active {
    transform: translateY(0);
}
.tuner-display {
    background: rgba(0, 0, 0, 0.3);
    border-radius: 15px;
    padding: 25px;
    margin: 20px 0;
}
.current-info {
    text-align: center;
    margin-bottom: 20px;
}
.current-string {
    font-size: 3em;
    font-weight: bold;
    color: #00d4ff;
    margin: 10px 0;
    text-shadow: 0 0 20px rgba(0, 212, 255, 0.5);
}
.target-freq {
    font-size: 1.2em;
    color: #aaa;
    margin-bottom: 15px;
}
.cents-display {
    font-size: 2.5em;
    font-weight: bold;
    margin: 20px 0;
    text-align: center;
}
.cents-display.tuned { color: #00ff00; }
.cents-display.close { color: #ffff00; }
.cents-display.far { color: #ff0000; }
#bar {
    width: 100%;
    height: 40px;
    background: rgba(0, 0, 0, 0.4);
    border-radius: 20px;
    margin: 20px 0;
    position: relative;
    overflow: hidden;
}
#bar::before {
    content: '';
    position: absolute;
    left: 50%;
    top: 0;
    bottom: 0;
    width: 2px;
    background: #fff;
    z-index: 1;
}
#indicator {
    width: 20px;
    height: 40px;
    background: #00ff00;
    border-radius: 10px;
    position: absolute;
    left: calc(50% - 10px);
    transition: all 0.1s ease;
    box-shadow: 0 0 20px rgba(0, 255, 0, 0.8);
}
.string-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(80px, 1fr));
    gap: 10px;
    margin: 20px 0;
}
.string-item {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 10px;
    padding: 15px 10px;
    text-align: center;
    border: 2px solid transparent;
    transition: all 0.3s ease;
}
.string-item.tuned {
    background: rgba(0, 255, 0, 0.2);
    border-color: #00ff00;
    box-shadow: 0 0 15px rgba(0, 255, 0, 0.3);
}
.string-item.current {
    background: rgba(0, 212, 255, 0.2);
    border-color: #00d4ff;
    box-shadow: 0 0 15px rgba(0, 212, 255, 0.5);
}
.string-name {
    font-size: 1.3em;
    font-weight: bold;
    color: #fff;
}
.string-freq {
    font-size: 0.9em;
    color: #aaa;
    margin-top: 5px;
}
.controls {
    display: flex;
    gap: 10px;
    margin-top: 20px;
}
.controls button {
    flex: 1;
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}
.back-btn {
    background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%) !important;
    margin-top: 20px;
}
.status-indicator {
    text-align: center;
    padding: 15px;
    border-radius: 10px;
    margin: 15px 0;
    font-size: 1.2em;
    font-weight: bold;
}
.status-indicator.tuned {
    background: rgba(0, 255, 0, 0.2);
    color: #00ff00;
    border: 2px solid #00ff00;
}
.status-indicator.tuning {
    background: rgba(255, 255, 0, 0.2);
    color: #ffff00;
    border: 2px solid #ffff00;
}
.status-indicator.out {
    background: rgba(255, 0, 0, 0.2);
    color: #ff0000;
    border: 2px solid #ff0000;
}
</style>
</head>
<body>
<div class="container">
    <h1>Zajebisty Stroik Inator</h1>
    
    {% if not instrument %}
    <h2>Select Guitar</h2>
    <div class="guitar-select">
        <form method="post" action="/select_guitar">
            <button name="instrument" value="6">6-String Guitar</button>
        </form>
        <form method="post" action="/select_guitar">
            <button name="instrument" value="8">8-String Guitar</button>
        </form>
    </div>
    
    {% elif screen == 'tuning_menu' %}
    <h2>{{ instrument }}-String Guitar</h2>
    <h2>Select Tuning</h2>
    <div class="tuning-select">
        {% for t in tunings %}
        <form action="/set_tuning" method="post">
            <button name="tuning" value="{{t}}">{{t}}</button>
        </form>
        {% endfor %}
    </div>
    <form action="/back_to_guitar" method="post">
        <button class="back-btn">Back to Guitar Selection</button>
    </form>
    
    {% else %}
    <h2>{{ instrument }}-String Guitar</h2>
    <div class="tuner-display">
        <div style="text-align: center; color: #aaa; margin-bottom: 15px;">
            Tuning: <strong style="color: #00d4ff;">{{ tuning }}</strong>
        </div>
        
        <div class="current-info">
            <div class="current-string" id="current-string">---</div>
            <div class="target-freq" id="target-freq">Frequency: ---</div>
        </div>
        
        <div class="status-indicator" id="status">Waiting for sound...</div>
        
        <div class="cents-display" id="cents-display">--- cents</div>
        
        <div id="bar">
            <div id="indicator"></div>
        </div>
        
        <div style="text-align: center; color: #aaa; margin-top: 10px;">
            <small>Too low | In tune | Too high</small>
        </div>
    </div>
    
    <h2>Strings Status</h2>
    <div class="string-grid" id="string-grid">
    </div>
    
    <div class="controls">
        <form action="/change_string" method="post" style="flex: 1;">
            <button name="dir" value="-1">Previous String</button>
        </form>
        <form action="/change_string" method="post" style="flex: 1;">
            <button name="dir" value="1">Next String</button>
        </form>
    </div>
    
    <form action="/back_to_tuning" method="post">
        <button class="back-btn">Change Tuning</button>
    </form>
    {% endif %}
</div>

<script>
let currentScreenState = "{{ screen }}";

function updateDisplay() {
    fetch("/status").then(r=>r.json()).then(d=>{
        if (d.current_screen !== currentScreenState) {
            window.location.href = "/";
            return;
        }

        if (document.getElementById("current-string")) {
            document.getElementById("current-string").innerText = d.current_note;
            document.getElementById("target-freq").innerText = "Frequency: " + d.target_freq + " Hz";
            
            const centsEl = document.getElementById("cents-display");
            const statusEl = document.getElementById("status");
            
            if (d.cents === "---") {
                centsEl.innerText = "--- cents";
                centsEl.className = "cents-display";
                statusEl.innerText = "Waiting for sound...";
                statusEl.className = "status-indicator";
            } else {
                const cents = parseFloat(d.cents);
                const sign = d.cents_raw >= 0 ? "+" : "";
                centsEl.innerText = sign + d.cents_raw.toFixed(1) + " cents";
                
                if (Math.abs(cents) <= 15) {
                    centsEl.className = "cents-display tuned";
                    statusEl.className = "status-indicator tuned";
                    statusEl.innerText = "IN TUNE";
                } else if (Math.abs(cents) <= 30) {
                    centsEl.className = "cents-display close";
                    statusEl.className = "status-indicator tuning";
                    statusEl.innerText = d.cents_raw > 0 ? "A bit too high" : "A bit too low";
                } else {
                    centsEl.className = "cents-display far";
                    statusEl.className = "status-indicator out";
                    statusEl.innerText = d.cents_raw > 0 ? "Too high" : "Too low";
                }
                
                let pos = Math.max(0, Math.min(100, 50 + (d.cents_raw / 100 * 50)));
                document.getElementById("indicator").style.left = pos + "%";
                document.getElementById("indicator").style.transform = "translateX(-50%)";
                
                if (Math.abs(cents) <= 15) {
                    document.getElementById("indicator").style.background = "#00ff00";
                    document.getElementById("indicator").style.boxShadow = "0 0 20px rgba(0, 255, 0, 0.8)";
                } else if (Math.abs(cents) <= 30) {
                    document.getElementById("indicator").style.background = "#ffff00";
                    document.getElementById("indicator").style.boxShadow = "0 0 20px rgba(255, 255, 0, 0.8)";
                } else {
                    document.getElementById("indicator").style.background = "#ff0000";
                    document.getElementById("indicator").style.boxShadow = "0 0 20px rgba(255, 0, 0, 0.8)";
                }
            }
            
            const grid = document.getElementById("string-grid");
            if (grid && d.all_strings) {
                grid.innerHTML = "";
                d.all_strings.forEach((str, idx) => {
                    const div = document.createElement("div");
                    div.className = "string-item";
                    if (d.tuned_strings && d.tuned_strings.includes(str.name)) div.classList.add("tuned");
                    if (idx === d.current_string_index) div.classList.add("current");
                    div.innerHTML = `<div class="string-name">${str.name}</div><div class="string-freq">${str.freq} Hz</div>`;
                    grid.appendChild(div);
                });
            }
        }
    });
}

setInterval(updateDisplay, 300);
updateDisplay();
</script>
</body>
</html>
""" 


class WebInterface:
    """Flask web server for remote tuner control"""
    
    def __init__(self, app_state):
        self.app_state = app_state
        self.app = Flask(__name__)
        self._setup_routes()
    
    def _setup_routes(self):
        """Configure Flask routes"""
        
        @self.app.route("/")
        def index():
            tunings_list = TuningManager.get_tunings_list(self.app_state.instrument)
            tuning_name = tunings_list[self.app_state.selected_tuning_index] if tunings_list else None
            all_strings_data = []
            
            if tuning_name:
                order = TuningManager.get_string_order(tuning_name)
                for note, freq in order:
                    all_strings_data.append({"name": note, "freq": freq})
            
            return render_template_string(
                HTML_TEMPLATE,
                tunings=tunings_list,
                instrument=self.app_state.instrument,
                screen=self.app_state.current_screen,
                tuning=tuning_name,
                all_strings=all_strings_data
            )
        
        @self.app.route("/select_guitar", methods=["POST"])
        def select_guitar_web():
            self.app_state.set_instrument(request.form["instrument"])
            self.app_state.change_screen("tuning_menu")
            return index()
        
        @self.app.route("/set_tuning", methods=["POST"])
        def set_tuning_web():
            tunings_list = TuningManager.get_tunings_list(self.app_state.instrument)
            name = request.form["tuning"]
            if name in tunings_list:
                self.app_state.selected_tuning_index = tunings_list.index(name)
                self.app_state.reset_tuning_state()
                self.app_state.change_screen("tuner")
            return index()
        
        @self.app.route("/change_string", methods=["POST"])
        def change_string_web():
            direction = int(request.form["dir"])
            max_str = TuningManager.get_max_strings(self.app_state.instrument)
            self.app_state.navigate_string(direction, max_str)
            return index()
        
        @self.app.route("/back_to_guitar", methods=["POST"])
        def back_to_guitar():
            self.app_state.instrument = None
            self.app_state.reset_tuning_state()
            self.app_state.change_screen("select_guitar")
            return index()
        
        @self.app.route("/back_to_tuning", methods=["POST"])
        def back_to_tuning():
            self.app_state.reset_tuning_state()
            self.app_state.change_screen("tuning_menu")
            return index()
        
        @self.app.route("/status")
        def status():
            tunings_list = TuningManager.get_tunings_list(self.app_state.instrument)
            tuning_name = tunings_list[self.app_state.selected_tuning_index] if tunings_list else "---"
            order = TuningManager.get_string_order(tuning_name)
            
            current_note = order[self.app_state.current_string_index][0] if self.app_state.current_string_index < len(order) else "---"
            target_freq = order[self.app_state.current_string_index][1] if self.app_state.current_string_index < len(order) else 0
            
            all_strings_data = [{"name": n, "freq": f} for n, f in order]
            
            return jsonify({
                "instrument": self.app_state.instrument,
                "tuning": tuning_name,
                "current_note": current_note,
                "target_freq": f"{target_freq:.2f}",
                "cents": self.app_state.last_cents,
                "cents_raw": self.app_state.last_cents_raw,
                "current_string_index": self.app_state.current_string_index,
                "tuned_strings": list(self.app_state.tuned_strings.keys()),
                "current_screen": self.app_state.current_screen,
                "all_strings": all_strings_data
            })
    
    def start(self):
        """Start the web server in a background thread"""
        def run_web():
            self.app.run(host=WEB_HOST, port=WEB_PORT, debug=False, use_reloader=False)
        
        thread = threading.Thread(target=run_web, daemon=True)
        thread.start()
