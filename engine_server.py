import sys
import subprocess

def install_dependencies():
    """
    A necessary, if vulgar, concession to the reality of environmental setup.
    """
    required_packages = ['Flask', 'Flask-Cors', 'numpy']
    print("Verifying dependencies...")
    for package in required_packages:
        try:
            __import__(package.split('[')[0])
            print(f"  - {package} is already satisfied.")
        except ImportError:
            print(f"  - Installing missing dependency: {package}...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            except subprocess.CalledProcessError as e:
                print(f"Error: Failed to install {package}. Please install it manually.", file=sys.stderr)
                sys.exit(1)
    print("All dependencies are satisfied.")

# Run dependency check at the start
install_dependencies()

from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import math
import json
import heapq
import re
import os
import webbrowser
from threading import Timer

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

# --- Engine Logic: Holographic ---
class HolographicEngine:
    def __init__(self, text: str):
        self.text = text
        self.length = len(text)
        self.SIGIL_START_MOTIF = 0xE000
        self.SIGIL_START_NUMERICAL = 0xF000

    def _find_resonance_candidates(self):
        candidates = []
        max_stride = self.length // 2
        for stride in range(1, max_stride + 1):
            for offset in range(stride):
                i = offset
                while i < self.length:
                    char = self.text[i]
                    count = 1
                    current_pos = i + stride
                    while current_pos < self.length and self.text[current_pos] == char:
                        count += 1
                        current_pos += stride
                    if count > 1:
                        desc = f"({char},{stride},{count},{i})"
                        savings = count - len(desc)
                        if savings > 0:
                            positions = [i + k * stride for k in range(count)]
                            candidates.append({'type': 'resonance', 'savings': savings, 'positions': positions, 'data': {'char': char, 'stride': stride, 'count': count, 'offset': i}})
                        i += count * stride
                    else:
                        i += stride
        return candidates

    def _find_motif_candidates(self):
        candidates = []
        counts = {}
        max_len = min(self.length // 2, 50)
        for length in range(max_len, 1, -1):
            for i in range(self.length - length + 1):
                substring = self.text[i:i+length]
                if substring not in counts:
                    counts[substring] = []
                counts[substring].append(i)
        
        for motif, positions in counts.items():
            if len(positions) > 1:
                savings = (len(positions) * len(motif)) - (len(positions) + len(motif) + 1)
                if savings > 0:
                    all_pos = [p + i for p in positions for i in range(len(motif))]
                    candidates.append({'type': 'motif', 'savings': savings, 'positions': all_pos, 'data': {'motif': motif}})
        return candidates
        
    def _find_numerical_candidates(self):
        candidates = []
        for match in re.finditer(r'\d{2}', self.text):
            num_str = match.group(0)
            savings = 1
            positions = list(range(match.start(), match.end()))
            candidates.append({'type': 'numerical', 'savings': savings, 'positions': positions, 'data': {'num': num_str}})
        return candidates

    def _huffman_encode(self, text):
        if not text:
            return {}, ''
        frequency = {char: text.count(char) for char in set(text)}
        heap = [[weight, [char, ""]] for char, weight in frequency.items()]
        heapq.heapify(heap)
        while len(heap) > 1:
            lo = heapq.heappop(heap)
            hi = heapq.heappop(heap)
            for pair in lo[1:]: pair[1] = '0' + pair[1]
            for pair in hi[1:]: pair[1] = '1' + pair[1]
            heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
        huffman_dict = dict(sorted(heapq.heappop(heap)[1:], key=lambda p: (len(p[-1]), p)))
        encoded_text = "".join([huffman_dict[char] for char in text])
        return huffman_dict, encoded_text

    def generate_blueprint(self):
        resonance_candidates = self._find_resonance_candidates()
        motif_candidates = self._find_motif_candidates()
        numerical_candidates = self._find_numerical_candidates()
        
        all_candidates = resonance_candidates + motif_candidates + numerical_candidates
        all_candidates.sort(key=lambda x: x['savings'], reverse=True)

        final_resonances, final_motifs, final_numericals = [], {}, {}
        claimed_positions = np.zeros(self.length, dtype=bool)
        motif_sigil_counter, numerical_sigil_counter = 0, 0

        for candidate in all_candidates:
            if not any(claimed_positions[pos] for pos in candidate['positions']):
                for pos in candidate['positions']:
                    claimed_positions[pos] = True
                
                if candidate['type'] == 'resonance':
                    final_resonances.append(candidate['data'])
                elif candidate['type'] == 'motif':
                    sigil = chr(self.SIGIL_START_MOTIF + motif_sigil_counter)
                    final_motifs[sigil] = candidate['data']['motif']
                    motif_sigil_counter += 1
                elif candidate['type'] == 'numerical':
                    letter = chr(97 + numerical_sigil_counter)
                    final_numericals[letter] = candidate['data']['num']
                    numerical_sigil_counter += 1
        
        remnant = "".join([char for i, char in enumerate(self.text) if not claimed_positions[i]])
        huffman_dict, encoded_remnant = self._huffman_encode(remnant)

        return {
            'engine': 'holographic',
            'originalText': self.text,
            'resonances': sorted(final_resonances, key=lambda r: r['offset']),
            'motifs': final_motifs,
            'numericals': final_numericals,
            'huffmanDict': huffman_dict,
            'encodedRemnant': encoded_remnant
        }

# --- Flask Server ---
app = Flask(__name__)
CORS(app)

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    if not data or 'text' not in data or 'engine' not in data:
        return jsonify({'error': 'Invalid request.'}), 400
    
    text = data['text']
    engine_type = data['engine']

    try:
        if engine_type == 'hyper-geometrisomorphous':
            engine = HyperGeometrisomorphous(text)
        elif engine_type == 'holographic':
            engine = HolographicEngine(text)
        else:
            return jsonify({'error': 'Unknown engine type.'}), 400
        
        result = engine.generate_blueprint()
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

def display_instructions():
    print("""
    This script serves a dual purpose: a web server for the GUI and a command-line tool.

    --- To use the Web Interface ---
    1. Clone the repository from GitHub.
    2. Run this script. It will automatically install dependencies and start the server:
       python engine_server.py
    3. Open the accompanying .html file in your web browser.
    """)

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help']:
        display_instructions()
    else:
        print("Starting Structural Compression Engine server at http://localhost:5000")
        app.run(host='0.0.0.0', port=5000)

