#!/usr/bin/env python3
"""
Simple web server to visualize PhysiCell simulation results
"""
import http.server
import socketserver
import os
import glob
import json
from urllib.parse import urlparse, parse_qs

class PhysiCellViewer(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            # Find all SVG files - prioritize tumor_immune_base if available
            svg_files = []
            # First try tumor_immune_base
            tumor_immune_files = glob.glob('outputs/tumor_immune_base/snapshot*.svg')
            if tumor_immune_files:
                svg_files = sorted(tumor_immune_files)
            else:
                # Fall back to any available outputs
                output_dirs = glob.glob('outputs/*/snapshot*.svg')
                if output_dirs:
                    svg_files = sorted(output_dirs)
            
            # Create HTML viewer
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>PhysiCell Simulation Viewer</title>
                <meta charset="utf-8">
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 20px; background: #f0f0f0; }}
                    .container {{ max-width: 1400px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; }}
                    .controls {{ margin-bottom: 20px; padding: 15px; background: #e8e8e8; border-radius: 5px; }}
                    .main-content {{ display: flex; gap: 20px; align-items: flex-start; }}
                    .viewer {{ flex: 1; text-align: center; }}
                    .sidebar {{ width: 300px; padding: 15px; background: #f8f8f8; border-radius: 5px; }}
                    .info {{ margin: 10px 0; padding: 10px; background: #f8f8f8; border-radius: 5px; }}
                    button {{ padding: 8px 15px; margin: 5px; border: none; border-radius: 4px; cursor: pointer; }}
                    .play {{ background: #4CAF50; color: white; }}
                    .pause {{ background: #f44336; color: white; }}
                    .nav {{ background: #2196F3; color: white; }}
                    input[type="range"] {{ width: 300px; }}
                    select {{ padding: 5px; margin: 5px; }}
                    .file-list {{ max-height: 200px; overflow-y: auto; border: 1px solid #ccc; padding: 10px; }}
                    .cell-type {{ display: flex; align-items: center; margin: 10px 0; padding: 8px; background: white; border-radius: 4px; border: 1px solid #ddd; }}
                    .cell-circle {{ width: 30px; height: 30px; border-radius: 50%; border: 2px solid black; margin-right: 10px; position: relative; }}
                    .cell-inner {{ width: 15px; height: 15px; border-radius: 50%; position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); }}
                    .grey-cell {{ background: grey; }}
                    .red-cell {{ background: red; }}
                    .black-cell {{ background: black; }}
                    .saddlebrown-cell {{ background: saddlebrown; }}
                    .yellow-cell {{ background: yellow; }}
                    .grey-inner {{ background: grey; border: 1px solid grey; }}
                    .red-inner {{ background: red; border: 1px solid red; }}
                    .black-inner {{ background: black; border: 1px solid black; }}
                    .saddlebrown-inner {{ background: saddlebrown; border: 1px solid saddlebrown; }}
                    .yellow-inner {{ background: yellow; border: 1px solid orange; }}
                    #svgContainer {{ 
                        border: 2px solid #ccc; 
                        background: white; 
                        display: flex; 
                        justify-content: center; 
                        align-items: center; 
                        min-height: 500px; 
                        height: 600px; 
                        overflow: hidden; 
                        padding: 20px;
                        box-sizing: border-box;
                    }}
                    #svgContainer svg {{ 
                        max-width: 100%; 
                        max-height: 100%; 
                        width: auto; 
                        height: auto; 
                        object-fit: contain;
                        transform-origin: center center;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>PhysiCell Cell Interaction Visualization</h1>
                    
                    <div class="info">
                        <h3>Simulation Data Overview</h3>
                        <p>Total snapshots found: <strong>{len(svg_files)}</strong> time steps</p>
                        <p>Model: Tumor-Immune System Interaction Model</p>
                    </div>
                    
                    <div class="controls">
                        <h3>Playback Controls</h3>
                        <button id="playBtn" class="play" onclick="togglePlay()">Play Animation</button>
                        <button class="nav" onclick="prevFrame()">Previous Frame</button>
                        <button class="nav" onclick="nextFrame()">Next Frame</button>
                        <br><br>
                        
                        <label>Time Step: </label>
                        <input type="range" id="frameSlider" min="0" max="{len(svg_files)-1}" value="0" 
                               oninput="goToFrame(this.value)">
                        <br><br>
                        
                        <label>Playback Speed: </label>
                        <select id="speedSelect" onchange="changeSpeed()">
                            <option value="1000">Slow (1 sec/frame)</option>
                            <option value="500" selected>Normal (0.5 sec/frame)</option>
                            <option value="250">Fast (0.25 sec/frame)</option>
                            <option value="100">Very Fast (0.1 sec/frame)</option>
                        </select>
                    </div>
                    
                    <div class="main-content">
                        <div class="viewer">
                            <div id="svgContainer">
                                <p>Loading...</p>
                            </div>
                        </div>
                        
                        <div class="sidebar">
                            <h3>Cell Types Legend</h3>
                            
                            <div class="cell-type">
                                <div class="cell-circle grey-cell">
                                    <div class="cell-inner grey-inner"></div>
                                </div>
                                <div>
                                    <strong>Tumor Cells (Grey)</strong><br>
                                    <small>Cancer cells that proliferate and consume oxygen</small>
                                </div>
                            </div>
                            
                            <div class="cell-type">
                                <div class="cell-circle red-cell">
                                    <div class="cell-inner red-inner"></div>
                                </div>
                                <div>
                                    <strong>Macrophages (Red)</strong><br>
                                    <small>Immune cells that secrete inflammatory factors and clean up debris</small>
                                </div>
                            </div>
                            
                            <div class="cell-type">
                                <div class="cell-circle yellow-cell">
                                    <div class="cell-inner yellow-inner"></div>
                                </div>
                                <div>
                                    <strong>CD8 T Cells (Yellow)</strong><br>
                                    <small>Cytotoxic T lymphocytes that attack tumor cells</small>
                                </div>
                            </div>
                            
                            <div class="cell-type">
                                <div class="cell-circle black-cell">
                                    <div class="cell-inner black-inner"></div>
                                </div>
                                <div>
                                    <strong>Necrotic Cells (Black)</strong><br>
                                    <small>Dead cells due to oxygen deprivation or immune attack</small>
                                </div>
                            </div>
                            
                            <div class="cell-type">
                                <div class="cell-circle saddlebrown-cell">
                                    <div class="cell-inner saddlebrown-inner"></div>
                                </div>
                                <div>
                                    <strong>Apoptotic Cells (Brown)</strong><br>
                                    <small>Cells undergoing programmed cell death</small>
                                </div>
                            </div>
                            
                            <h4>Immune Interactions</h4>
                            <div style="font-size: 12px; line-height: 1.4;">
                                <p><strong>Macrophage Functions:</strong><br>
                                • Secrete pro/anti-inflammatory factors<br>
                                • Clean up dead cell debris<br>
                                • Respond to oxygen levels</p>
                                
                                <p><strong>CD8 T Cell Activity:</strong><br>
                                • Attack tumor cells directly<br>
                                • Respond to inflammatory signals<br>
                                • Migration speed affected by contact</p>
                                
                                <p><strong>Tumor Response:</strong><br>
                                • Damaged by immune attacks<br>
                                • Die from oxygen deprivation<br>
                                • Release debris when dead</p>
                            </div>
                            
                            <h4>Current Frame Info</h4>
                            <div id="frameDetails" style="font-size: 12px; background: white; padding: 8px; border-radius: 4px; border: 1px solid #ddd;">
                                <span id="frameInfo">Frame 1 / {len(svg_files)}</span>
                            </div>
                        </div>
                    </div>
                    
                    <div class="info">
                        <h3>File List</h3>
                        <div class="file-list">
                            <p><strong>SVG Snapshot Files:</strong></p>
                            {'<br>'.join([f"• {f}" for f in svg_files[:10]])}
                            {f"<br>... and {len(svg_files)-10} more files" if len(svg_files) > 10 else ""}
                        </div>
                    </div>
                </div>
                
                <script>
                    const svgFiles = {json.dumps(svg_files)};
                    let currentFrame = 0;
                    let isPlaying = false;
                    let playInterval = null;
                    let speed = 500;
                    
                    function loadFrame(index) {{
                        if (index >= 0 && index < svgFiles.length) {{
                            currentFrame = index;
                            const container = document.getElementById('svgContainer');
                            
                            fetch('/' + svgFiles[index])
                                .then(response => response.text())
                                .then(data => {{
                                    container.innerHTML = data;
                                    // Update SVG styling to fit container properly
                                    const svg = container.querySelector('svg');
                                    if (svg) {{
                                        // Remove any inline dimensions to allow responsive scaling
                                        svg.removeAttribute('width');
                                        svg.removeAttribute('height');
                                        svg.style.width = '100%';
                                        svg.style.height = '100%';
                                        svg.style.maxWidth = '100%';
                                        svg.style.maxHeight = '100%';
                                        svg.style.objectFit = 'contain';
                                        // Add viewBox if missing for proper scaling
                                        if (!svg.getAttribute('viewBox')) {{
                                            svg.setAttribute('viewBox', '0 0 1700 1605');
                                        }}
                                    }}
                                }})
                                .catch(error => {{
                                    container.innerHTML = '<p>Loading failed: ' + error + '</p>';
                                }});
                            
                            document.getElementById('frameSlider').value = index;
                            const frameInfoElement = document.getElementById('frameInfo');
                            if (frameInfoElement) {{
                                frameInfoElement.textContent = `Frame ${{index + 1}} / ${{svgFiles.length}}`;
                            }}
                        }}
                    }}
                    
                    function togglePlay() {{
                        const btn = document.getElementById('playBtn');
                        if (isPlaying) {{
                            clearInterval(playInterval);
                            btn.textContent = 'Play Animation';
                            btn.className = 'play';
                            isPlaying = false;
                        }} else {{
                            playInterval = setInterval(() => {{
                                if (currentFrame >= svgFiles.length - 1) {{
                                    currentFrame = 0;
                                }} else {{
                                    currentFrame++;
                                }}
                                loadFrame(currentFrame);
                            }}, speed);
                            btn.textContent = 'Pause Animation';
                            btn.className = 'pause';
                            isPlaying = true;
                        }}
                    }}
                    
                    function nextFrame() {{
                        if (currentFrame < svgFiles.length - 1) {{
                            loadFrame(currentFrame + 1);
                        }}
                    }}
                    
                    function prevFrame() {{
                        if (currentFrame > 0) {{
                            loadFrame(currentFrame - 1);
                        }}
                    }}
                    
                    function goToFrame(index) {{
                        loadFrame(parseInt(index));
                    }}
                    
                    function changeSpeed() {{
                        speed = parseInt(document.getElementById('speedSelect').value);
                        if (isPlaying) {{
                            // 重启播放以应用新速度
                            togglePlay();
                            togglePlay();
                        }}
                    }}
                    
                    // Keyboard controls
                    document.addEventListener('keydown', function(event) {{
                        switch(event.code) {{
                            case 'Space':
                                event.preventDefault();
                                togglePlay();
                                break;
                            case 'ArrowLeft':
                                prevFrame();
                                break;
                            case 'ArrowRight':
                                nextFrame();
                                break;
                        }}
                    }});
                    
                    // Load first frame initially
                    if (svgFiles.length > 0) {{
                        loadFrame(0);
                    }} else {{
                        document.getElementById('svgContainer').innerHTML = '<p>No SVG files found</p>';
                    }}
                </script>
            </body>
            </html>
            """
            
            self.wfile.write(html_content.encode())
            
        elif parsed_path.path == '/api/files':
            # Return file list as JSON - prioritize tumor_immune_base
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            # First try tumor_immune_base
            tumor_immune_files = glob.glob('outputs/tumor_immune_base/snapshot*.svg')
            if tumor_immune_files:
                svg_files = sorted(tumor_immune_files)
            else:
                # Fall back to any available outputs
                svg_files = sorted(glob.glob('outputs/*/snapshot*.svg'))
            
            self.wfile.write(json.dumps(svg_files).encode())
            
        else:
            # Serve files normally
            super().do_GET()

def start_server(port=8000):
    """Start the web server"""
    os.chdir('/home/cl140/research/grammar_samples')
    
    with socketserver.TCPServer(("", port), PhysiCellViewer) as httpd:
        print(f"PhysiCell Visualization Server Started!")
        print(f"Open in browser: http://localhost:{port}")
        print("Keyboard controls: Space=Play/Pause, Left/Right arrows=Frame navigation")
        print("Press Ctrl+C to stop server")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped")

if __name__ == "__main__":
    start_server(8092)