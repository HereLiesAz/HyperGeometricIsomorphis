from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import math
import json

class HyperGeometrisomorphous:
    """
    An engine that treats a string as a set of collapsed 3D point clouds (constellations),
    finding the single most efficiently expressed path for each character's constellation
    across all possible volumetric projections. The final blueprint is a 2D matrix (codex).
    """

    def __init__(self, text: str, update_callback=None):
        self.original_text = text
        self.length = len(text)
        self.log = update_callback or print

    def _get_volume_permutations(self):
        """Generates plausible 3D matrix dimensions (pages, rows, cols)."""
        permutations = set()
        # Limit the search space for performance.
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
        """
        Finds a 'good enough' path through a point cloud using the Nearest Neighbor heuristic.
        A true TSP solution is computationally intractable. This is an admission of reality.
        """
        if not points:
            return []
        
        path = [points.pop(0)]
        while points:
            last_point = path[-1]
            distances = [np.linalg.norm(np.array(last_point) - np.array(p)) for p in points]
            nearest_index = np.argmin(distances)
            path.append(points.pop(nearest_index))
        return path

    def _encode_path(self, path):
        """Encodes a path of 3D points into a compact series of vectors."""
        if not path:
            return ""
        if len(path) == 1:
            return f"S{path[0][0]},{path[0][1]},{path[0][2]}"

        start_point = path[0]
        vectors = []
        for i in range(len(path) - 1):
            p1 = np.array(path[i])
            p2 = np.array(path[i+1])
            vectors.append(tuple(p2 - p1))
            
        if not vectors: return f"S{','.join(map(str, start_point))}"
        
        rle_vectors = []
        count = 1
        for i in range(1, len(vectors)):
            if vectors[i] == vectors[i-1]:
                count += 1
            else:
                rle_vectors.append(f"{vectors[i-1][0]},{vectors[i-1][1]},{vectors[i-1][2]}" + (f"*{count}" if count > 1 else ""))
                count = 1
        rle_vectors.append(f"{vectors[-1][0]},{vectors[-1][1]},{vectors[-1][2]}" + (f"*{count}" if count > 1 else ""))

        return f"S{','.join(map(str, start_point))}|" + "|".join(rle_vectors)

    def find_best_algorithm_for_char(self, char_to_find, permutations):
        """
        Generates all possible path algorithms for a single character and returns the best one.
        "Best" is defined as the one with the most compact descriptor string.
        """
        candidates = []
        all_indices = [i for i, char in enumerate(self.original_text) if char == char_to_find]
        if not all_indices: return None

        for dims in permutations:
            pages, rows, cols = dims
            
            points = []
            for idx in all_indices:
                p = idx // (rows * cols)
                r = (idx % (rows * cols)) // cols
                c = idx % cols
                points.append((p, r, c))

            path = self._find_shortest_path(points.copy())
            path_desc = self._encode_path(path)

            candidates.append({
                'dims': dims,
                'desc': path_desc,
                'desc_len': len(path_desc)
            })

        if candidates:
            return min(candidates, key=lambda x: x['desc_len'])
        return None

    def generate_blueprint(self):
        """The main orchestration method."""
        permutations = self._get_volume_permutations()
        unique_chars = sorted(list(set(self.original_text)))
        
        winning_algorithms = {}
        for char in unique_chars:
            best_algorithm = self.find_best_algorithm_for_char(char, permutations)
            if best_algorithm:
                winning_algorithms[char] = best_algorithm

        codex = [[f"len:{self.length}"]]
        for char, algo in sorted(winning_algorithms.items()):
            codex.append([
                char, 
                f"{algo['dims'][0]}x{algo['dims'][1]}x{algo['dims'][2]}",
                algo['desc']
            ])

        serialized_codex = "§".join(["|".join(row) for row in codex])
        return {
            "engine": "hyper-geometrisomorphous",
            "codex": codex,
            "serialized_codex": serialized_codex,
            "original_text": self.original_text
        }


# --- Flask Server ---
app = Flask(__name__)
CORS(app) # Allow cross-origin requests

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({'error': 'Invalid request. Missing text.'}), 400
    
    text = data['text']

    try:
        engine = HyperGeometrisomorphous(text)
        result = engine.generate_blueprint()
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': f'An error occurred during analysis: {str(e)}'}), 500

if __name__ == '__main__':
    print("Starting Hyper-Geometrisomorphous server at http://localhost:5000")
    print("Press CTRL+C to stop the server.")
    app.run(host='0.0.0.0', port=5000)

