import sys
import subprocess
import webbrowser
from threading import Timer
import os
import math
import json
import heapq
import re

# --- Dependency Verification ---
def install_dependencies():
    """A necessary, if vulgar, concession to the reality of environmental setup."""
    required_packages = ['Flask', 'Flask-Cors', 'numpy']
    print("Verifying dependencies...")
    for package in required_packages:
        try:
            # Check if module is importable
            __import__(package.split('[')[0].replace('-', '_'))
            print(f"  - {package} is already satisfied.")
        except ImportError:
            print(f"  - Installing missing dependency: {package}...")
            try:
                # Ensure pip is available before trying to use it
                subprocess.check_call([sys.executable, "-m", "pip", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            except subprocess.CalledProcessError:
                print(f"Error: Failed to install {package}.", file=sys.stderr)
                print("Your Python environment may be missing 'pip'. Please run 'python -m ensurepip --upgrade' and try again.", file=sys.stderr)
                sys.exit(1)
    print("All dependencies are satisfied.")

install_dependencies()

from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import numpy as np

# --- Engine Logic: Hyper-Geometrisomorphous ---
class HyperGeometrisomorphous:
    def __init__(self, text: str):
        self.original_text = text
        self.length = len(text)

    def _get_volume_permutations(self):
        permutations = set()
        for pages in range(1, int(self.length**0.33) + 2):
            if self.length % pages == 0:
                area = self.length // pages
                for rows in range(1, int(area**0.5) + 2):
                    if area % rows == 0:
                        cols = area // rows
                        if pages * rows * cols == self.length:
                           permutations.add(tuple(sorted((pages, rows, cols))))
        if not permutations: permutations.add((1, 1, self.length))
        return sorted(list(permutations), key=lambda x: x[0]*x[1]*x[2])[:30]

    def _find_shortest_path(self, points):
        if not points: return []
        path = [points.pop(0)]
        while points:
            last_point = path[-1]
            distances = [np.linalg.norm(np.array(last_point) - np.array(p)) for p in points]
            nearest_index = np.argmin(distances)
            path.append(points.pop(nearest_index))
        return path

    def _encode_path(self, path):
        if not path: return ""
        if len(path) == 1: return f"S{path[0][0]},{path[0][1]},{path[0][2]}"
        start_point = path[0]
        vectors = [tuple(np.array(path[i+1]) - np.array(path[i])) for i in range(len(path) - 1)]
        if not vectors: return f"S{','.join(map(str, start_point))}"
        rle_vectors = []
        count = 1
        for i in range(1, len(vectors)):
            if vectors[i] == vectors[i-1]:
                count += 1
            else:
                rle_vectors.append(f"{','.join(map(str, vectors[i-1]))}" + (f"*{count}" if count > 1 else ""))
                count = 1
        rle_vectors.append(f"{','.join(map(str, vectors[-1]))}" + (f"*{count}" if count > 1 else ""))
        return f"S{','.join(map(str, start_point))}|" + "|".join(rle_vectors)

    def find_best_algorithm_for_char(self, char_to_find, permutations):
        candidates = []
        all_indices = [i for i, char in enumerate(self.original_text) if char == char_to_find]
        if not all_indices: return None
        for dims in permutations:
            pages, rows, cols = dims
            points = [(idx // (rows * cols), (idx % (rows * cols)) // cols, idx % cols) for idx in all_indices]
            path = self._find_shortest_path(points.copy())
            path_desc = self._encode_path(path)
            candidates.append({'dims': dims, 'desc': path_desc, 'desc_len': len(path_desc)})
        return min(candidates, key=lambda x: x['desc_len']) if candidates else None

    def generate_blueprint(self):
        permutations = self._get_volume_permutations()
        unique_chars = sorted(list(set(self.original_text)))
        winning_algorithms = {char: self.find_best_algorithm_for_char(char, permutations) for char in unique_chars}
        winning_algorithms = {k: v for k, v in winning_algorithms.items() if v}
        
        codex = [[f"len:{self.length}"]]
        for char, algo in sorted(winning_algorithms.items()):
            codex.append([char, f"{algo['dims'][0]}x{algo['dims'][1]}x{algo['dims'][2]}", algo['desc']])
        
        serialized_codex = "§".join(["|".join(map(str, row)) for row in codex])
        return {"engine": "hyper-geometrisomorphous", "codex": codex, "serialized_codex": serialized_codex, "original_text": self.original_text}

# --- HTML/CSS/JS Frontend as a String Variable ---
HTML_CONTENT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hyper-Geometrisomorphous Engine</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&family=Roboto+Mono:wght@400;500&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Inter', sans-serif; background-color: #f8f7f2; color: #4c4a44; }
        .mono { font-family: 'Roboto Mono', monospace; }
        .key-entry:hover { background-color: #e9e7e0; cursor: pointer; }
    </style>
</head>
<body class="p-4 sm:p-6 lg:p-8">
    <div class="max-w-7xl mx-auto">
        <header class="text-center mb-10">
            <h1 class="text-3xl sm:text-4xl lg:text-5xl font-bold text-slate-800">Hyper-Geometrisomorphous Engine</h1>
            <p class="mt-2 text-lg text-slate-500">This is not compression. This is cartography.</p>
        </header>

        <main class="bg-white rounded-lg shadow-sm border border-slate-200 p-4 sm:p-6 lg:p-8">
            <div class="mb-8">
                <h2 class="text-2xl font-bold text-slate-700 mb-2">1. Input Universe (String)</h2>
                <p class="text-slate-500 mb-4">The engine will find the single most efficient path for each character's constellation across all volumetric projections.</p>
                <textarea id="input-text" class="w-full h-28 p-3 border border-slate-300 rounded-md focus:ring-2 focus:ring-teal-500 focus:outline-none mono bg-slate-50" placeholder="A string with a clear 3D structure works best..."></textarea>
                <div class="mt-4 flex items-center space-x-4">
                    <button id="analyze-button" class="w-full sm:w-auto bg-slate-800 text-white font-bold py-2 px-8 rounded-md hover:bg-slate-900 transition-colors disabled:bg-slate-400">Generate Codex</button>
                </div>
            </div>

             <div id="progress-container" class="hidden my-6">
                <p id="progress-label" class="text-sm text-center text-slate-500 mb-2">Surveying the universe...</p>
                <div class="w-full bg-slate-200 rounded-full h-2.5">
                    <div class="bg-teal-600 h-2.5 rounded-full animate-pulse"></div>
                </div>
            </div>
            
            <div id="results-area" class="hidden">
                <hr class="my-8 border-slate-200">
                <h2 class="text-2xl font-bold text-slate-700 mb-6">2. The Codex</h2>
                <div class="grid grid-cols-1 xl:grid-cols-5 gap-8">
                    <div class="xl:col-span-3">
                        <h3 class="text-xl font-semibold text-slate-600 mb-3">Constellation Map</h3>
                         <p class="text-slate-500 mb-4">The original string, unrolled. Stars are colored by their character's winning algorithm. Hover over a key entry to highlight its constellation.</p>
                        <div class="bg-slate-50 p-2 rounded-md border border-slate-200">
                           <canvas id="visualization-canvas"></canvas>
                        </div>
                    </div>
                    <div class="xl:col-span-2">
                        <h3 class="text-xl font-semibold text-slate-600 mb-3">Blueprint</h3>
                        <div class="space-y-6">
                             <div class="grid grid-cols-3 gap-4 text-center border-b border-slate-200 pb-4">
                                <div><p class="text-sm text-slate-500">Original</p><p id="original-length" class="text-2xl font-bold mono text-slate-700">-</p></div>
                                <div><p class="text-sm text-slate-500">Encoded</p><p id="final-length" class="text-2xl font-bold mono text-slate-700">-</p></div>
                                <div><p class="text-sm text-slate-500">Reduction</p><p id="ratio" class="text-2xl font-bold mono text-teal-600">-</p></div>
                            </div>
                            <div>
                                <h4 class="font-semibold text-slate-600 mb-2">Character Algorithms</h4>
                                <div id="key-output" class="text-sm mono space-y-1 max-h-64 overflow-y-auto pr-2 border border-slate-200 rounded-md p-3 bg-slate-50"></div>
                            </div>
                            <div>
                                <h4 class="font-semibold text-slate-600 mb-2">Serialized Codex</h4>
                                <div id="serialized-output" class="p-3 bg-slate-800 text-slate-100 border border-slate-600 rounded-md text-xs mono break-all max-h-32 overflow-y-auto"></div>
                                <button id="reconstitute-button" class="mt-2 w-full bg-white border border-slate-300 text-slate-700 font-bold py-2 px-4 rounded-md hover:bg-slate-50 transition-colors">Reconstitute from Codex</button>
                                <div id="reconstitution-output" class="mt-2 p-2 bg-slate-100 border border-slate-200 rounded-md text-xs mono break-all text-slate-500 hidden"></div>
                           </div>
                        </div>
                    </div>
                </div>
            </div>
        </main>
    </div>

    <script>
        document.addEventListener('DOMContentLoaded', () => {
            const analyzeBtn = document.getElementById('analyze-button');
            const inputEl = document.getElementById('input-text');
            const progressContainer = document.getElementById('progress-container');
            const resultsArea = document.getElementById('results-area');

            let analysisResult = null;
            let hoveredChar = null;

            const PALETTE = ['#0d9488', '#d97706', '#be185d', '#65a30d', '#57534e', '#8b5cf6', '#0ea5e9'];

            const analyze = async () => {
                const text = inputEl.value;
                if (!text) return;
                
                analyzeBtn.disabled = true;
                progressContainer.classList.remove('hidden');
                resultsArea.classList.add('hidden');

                try {
                    const response = await fetch('http://localhost:5000/analyze', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ text })
                    });
                    
                    if (!response.ok) {
                        const err = await response.json();
                        throw new Error(err.error || 'Unknown server error');
                    }
                    
                    analysisResult = await response.json();
                    displayResults();
                } catch (error) {
                    alert(`Analysis failed: ${error.message}`);
                } finally {
                    analyzeBtn.disabled = false;
                    progressContainer.classList.add('hidden');
                }
            };
            
            const displayResults = () => {
                const { serialized_codex, codex, original_text } = analysisResult;
                const algorithms = codex.slice(1);

                document.getElementById('original-length').textContent = original_text.length;
                document.getElementById('final-length').textContent = serialized_codex.length;
                const ratio = original_text.length > 0 ? (100 * (1 - serialized_codex.length / original_text.length)).toFixed(1) : 0;
                document.getElementById('ratio').textContent = `${ratio > 0 ? ratio : 0}%`;

                const keyOutput = document.getElementById('key-output');
                keyOutput.innerHTML = algorithms.length > 0 ? '' : '<p class="text-slate-500">None</p>';
                
                const charColorMap = {};
                algorithms.forEach((algo, index) => {
                    const [char, dims, desc] = algo;
                    charColorMap[char] = PALETTE[index % PALETTE.length];
                    const entry = document.createElement('div');
                    entry.className = 'key-entry p-1 rounded transition-colors';
                    entry.dataset.char = char;
                    entry.innerHTML = `<span class="inline-block w-3 h-3 rounded-full mr-2" style="background-color: ${charColorMap[char]};"></span><span>'${char}' &rarr; ${dims}: ${desc.substring(0, 30)}...</span>`;
                    entry.onmouseenter = () => { hoveredChar = char; drawVisualization(charColorMap); };
                    entry.onmouseleave = () => { hoveredChar = null; drawVisualization(charColorMap); };
                    keyOutput.appendChild(entry);
                });
                
                document.getElementById('serialized-output').textContent = serialized_codex;
                document.getElementById('reconstitute-button').onclick = runReconstruction;
                document.getElementById('reconstitution-output').classList.add('hidden');

                resultsArea.classList.remove('hidden');
                drawVisualization(charColorMap);
            };

            const drawVisualization = (charColorMap) => {
                const canvas = document.getElementById('visualization-canvas');
                if (!analysisResult || !canvas) return;
                const ctx = canvas.getContext('2d');
                const { original_text } = analysisResult;

                const dpr = window.devicePixelRatio || 1;
                const parentWidth = canvas.parentElement.clientWidth;
                canvas.width = parentWidth * dpr;
                const charSize = Math.min(24, parentWidth / 40);
                const charsPerRow = Math.floor(parentWidth / charSize);
                const numRows = Math.ceil(original_text.length / charsPerRow);
                canvas.height = (numRows * charSize * 1.5) * dpr;
                ctx.scale(dpr, dpr);
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                ctx.font = `500 ${charSize * 0.8}px 'Roboto Mono'`;
                
                for(let i = 0; i < original_text.length; i++) {
                    const char = original_text[i];
                    const row = Math.floor(i / charsPerRow), col = i % charsPerRow;
                    const x = col * charSize + (charSize / 2), y = row * charSize * 1.5 + (charSize / 2);
                    ctx.textAlign = 'center';
                    ctx.textBaseline = 'middle';
                    
                    ctx.fillStyle = charColorMap[char] || '#9ca3af';

                    if (hoveredChar === char) {
                        ctx.fillStyle = '#000';
                        ctx.fillRect(x - charSize/2, y - charSize/2, charSize, charSize);
                        ctx.fillStyle = '#fff';
                    }
                    ctx.fillText(char, x, y);
                }
            };
            
            const runReconstruction = () => {
                 if(!analysisResult) return;
                 const { serialized_codex, original_text } = analysisResult;
                 const reconstitutionOutput = document.getElementById('reconstitution-output');
                 try {
                    const rows = serialized_codex.split('§').map(r => r.split('|'));
                    const originalLength = parseInt(rows[0][0].split(':')[1], 10);
                    const algorithms = rows.slice(1);
                    const canvas = new Array(originalLength).fill('');
                    
                    algorithms.forEach(algoRow => {
                        const [char, dimsStr, pathDesc] = algoRow;
                        const [pages, rowsDim, cols] = dimsStr.split('x').map(Number);
                        const pathParts = pathDesc.split('|');
                        const startPointStr = pathParts[0].substring(1);
                        if (!startPointStr) return;
                        
                        const startPoint = startPointStr.split(',').map(Number);
                        let currentPos = [...startPoint];
                        let idx = Math.round(currentPos[0])*rowsDim*cols + Math.round(currentPos[1])*cols + Math.round(currentPos[2]);
                        if (idx < originalLength) canvas[idx] = char;
                        
                        if (pathParts.length > 1) {
                            pathParts.slice(1).forEach(vectorStr => {
                                if (!vectorStr) return;
                                const parts = vectorStr.split('*');
                                const vector = parts[0].split(',').map(Number);
                                const count = parts.length > 1 ? parseInt(parts[1], 10) : 1;
                                for (let i = 0; i < count; i++) {
                                    currentPos[0] += vector[0];
                                    currentPos[1] += vector[1];
                                    currentPos[2] += vector[2];
                                    idx = Math.round(currentPos[0])*rowsDim*cols + Math.round(currentPos[1])*cols + Math.round(currentPos[2]);
                                    if (idx < originalLength) canvas[idx] = char;
                                }
                            });
                        }
                    });

                    const reconstitutedText = canvas.join('');
                    const isLossless = reconstitutedText === original_text;
                    reconstitutionOutput.textContent = `Verification: ${isLossless ? 'Perfect Match!' : 'Mismatch Detected.'}\\n\\n${reconstitutedText}`;
                 } catch (e) {
                     reconstitutionOutput.textContent = `Error during reconstruction: ${e.message}`;
                 }
                 reconstitutionOutput.classList.remove('hidden');
            };

            analyzeBtn.addEventListener('click', analyze);
            
            inputEl.value = "a" + "z"*18 + "a" + "z"*19 + "a" + "z"*18 + "a" + "z" * 60;
            inputEl.value = inputEl.value.substring(0, 120);
        });
    </script>
</body>
</html>
"""

# --- Flask Server ---
app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    """Serves the main HTML page."""
    return Response(HTML_CONTENT, mimetype='text/html')

@app.route('/analyze', methods=['POST'])
def analyze_route():
    """The analysis endpoint."""
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({'error': 'Invalid request. Missing text.'}), 400
    
    text = data['text']

    try:
        # For simplicity, this unified script only runs the Hyper-Geometrisomorphous engine.
        engine = HyperGeometrisomorphous(text)
        result = engine.generate_blueprint()
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': f'An error occurred during analysis: {str(e)}'}), 500

def open_browser():
    """Opens the web browser to the server's URL."""
    webbrowser.open_new("http://localhost:5000")

def display_instructions():
    """Displays instructions for running the server."""
    instructions = """
    This script serves a dual purpose: a web server for the GUI and a command-line tool.

    --- To use the Web Interface ---
    1. Save this script as a single file (e.g., engine.py).
    2. Run this script. It will automatically install dependencies and start the server:
       python engine.py
    
    The server will be running at http://localhost:5000. Press CTRL+C to stop it.
    """
    print(instructions)

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help']:
        display_instructions()
    else:
        print("Starting Hyper-Geometrisomorphous server at http://localhost:5000")
        print("Your browser should open automatically.")
        print("For usage instructions, run: python engine.py --help")
        print("Press CTRL+C to stop the server.")
        Timer(1, open_browser).start()
        app.run(host='0.0.0.0', port=5000)

