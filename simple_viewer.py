#!/usr/bin/env python3
"""
Simple HTTP server for viewing PhysiCell SVG files
"""
import http.server
import socketserver
import webbrowser
import os
import glob

PORT = 8001

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            # Create index page
            svg_files = sorted(glob.glob('outputs/*/snapshot*.svg'))
            
            html = f"""<!DOCTYPE html>
<html>
<head>
    <title>PhysiCell SVG Viewer</title>
    <meta charset="utf-8">
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .container {{ max-width: 800px; margin: 0 auto; }}
        .svg-frame {{ border: 1px solid #ccc; margin: 10px 0; text-align: center; }}
        select {{ padding: 10px; margin: 10px; width: 300px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>PhysiCell Simulation Results Viewer</h1>
        <p>Found {len(svg_files)} simulation snapshots</p>
        
        <label for="fileSelect">Select Time Step:</label>
        <select id="fileSelect" onchange="loadSVG()">
            <option value="">-- Select File --</option>
"""
            
            for i, file in enumerate(svg_files):
                html += f'<option value="/{file}">Step {i+1}: {os.path.basename(file)}</option>\n'
            
            html += """
        </select>
        
        <div id="svgDisplay" class="svg-frame">
            <p>Please select a time step to view cell states</p>
        </div>
    </div>
    
    <script>
        function loadSVG() {
            const select = document.getElementById('fileSelect');
            const display = document.getElementById('svgDisplay');
            
            if (select.value) {
                fetch(select.value)
                    .then(response => response.text())
                    .then(data => {
                        display.innerHTML = data;
                    })
                    .catch(error => {
                        display.innerHTML = '<p>Loading failed: ' + error + '</p>';
                    });
            }
        }
    </script>
</body>
</html>"""
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(html.encode('utf-8'))
        else:
            super().do_GET()

if __name__ == "__main__":
    os.chdir('/home/cl140/research/grammar_samples')
    
    with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
        print(f"Server running on port {PORT}")
        print(f"Open in browser: http://localhost:{PORT}")
        httpd.serve_forever()