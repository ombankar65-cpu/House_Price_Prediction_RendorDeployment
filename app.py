import os
import pickle
import numpy as np
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# Load the pickle model
MODEL_PATH = "model.pkl"
model = None

if os.path.exists(MODEL_PATH):
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
else:
    print(f"Error: {MODEL_PATH} not found. Please ensure it is in the same directory.")

# Modern, elegant HTML/CSS layout embedded directly for easy single-file deployment
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Property Price Predictor</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Inter', sans-serif; }
    </style>
</head>
<body class="bg-slate-50 min-h-screen flex flex-col justify-between">

    <header class="bg-white border-b border-slate-200 py-5 shadow-sm">
        <div class="max-w-4xl mx-auto px-4 flex justify-between items-center">
            <h1 class="text-xl font-bold text-slate-800 tracking-tight flex items-center gap-2">
                🏠 <span class="text-indigo-600">PropertyVal</span> AI
            </h1>
            <span class="text-xs bg-indigo-50 text-indigo-700 font-semibold px-2.5 py-1 rounded-full border border-indigo-100">
                KNN Regressor Active
            </span>
        </div>
    </header>

    <main class="max-w-4xl mx-auto px-4 py-10 w-full flex-grow">
        <div class="bg-white rounded-2xl shadow-xl border border-slate-100 overflow-hidden grid md:grid-cols-5">
            
            <div class="p-8 md:col-span-3">
                <h2 class="text-2xl font-bold text-slate-800 mb-2">Estimate Valuation</h2>
                <p class="text-sm text-slate-500 mb-6">Enter the structural details below to query the prediction model.</p>
                
                <form id="predictionForm" class="space-y-4">
                    <div class="grid grid-cols-2 gap-4">
                        <div>
                            <label class="block text-xs font-semibold uppercase tracking-wider text-slate-600 mb-1">Bedrooms</label>
                            <input type="number" name="beds" required min="0" placeholder="e.g. 3" 
                                class="w-full px-4 py-2.5 rounded-lg border border-slate-200 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition outline-none">
                        </div>
                        <div>
                            <label class="block text-xs font-semibold uppercase tracking-wider text-slate-600 mb-1">Bathrooms</label>
                            <input type="number" name="baths" required step="0.5" min="0" placeholder="e.g. 2.5" 
                                class="w-full px-4 py-2.5 rounded-lg border border-slate-200 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition outline-none">
                        </div>
                    </div>

                    <div>
                        <label class="block text-xs font-semibold uppercase tracking-wider text-slate-600 mb-1">Interior Size (sqft)</label>
                        <input type="number" name="size" required min="1" placeholder="e.g. 1800" 
                            class="w-full px-4 py-2.5 rounded-lg border border-slate-200 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition outline-none">
                    </div>

                    <div>
                        <label class="block text-xs font-semibold uppercase tracking-wider text-slate-600 mb-1">Lot Size (sqft)</label>
                        <input type="number" name="lot_size" required min="0" placeholder="e.g. 5000" 
                            class="w-full px-4 py-2.5 rounded-lg border border-slate-200 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition outline-none">
                    </div>

                    <div>
                        <label class="block text-xs font-semibold uppercase tracking-wider text-slate-600 mb-1">Zip Code</label>
                        <input type="number" name="zip_code" required placeholder="e.g. 90210" 
                            class="w-full px-4 py-2.5 rounded-lg border border-slate-200 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition outline-none">
                    </div>

                    <button type="submit" 
                        class="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-medium py-3 rounded-lg shadow-md transition-all transform hover:-translate-y-0.5 mt-4">
                        Calculate Price
                    </button>
                </form>
            </div>

            <div class="bg-slate-900 p-8 text-white md:col-span-2 flex flex-col justify-center items-center text-center relative border-t md:border-t-0 md:border-l border-slate-800">
                <div id="placeholderResult">
                    <div class="w-16 h-16 bg-slate-800 rounded-full flex items-center justify-center mb-4 mx-auto border border-slate-700">
                        <span class="text-2xl text-slate-400">📊</span>
                    </div>
                    <h3 class="text-lg font-semibold tracking-wide">Awaiting Inputs</h3>
                    <p class="text-xs text-slate-400 max-w-[200px] mt-1 mx-auto">Fill out the property characteristics to view the AI prediction index.</p>
                </div>

                <div id="loadingResult" class="hidden">
                    <div class="animate-spin rounded-full h-10 w-10 border-b-2 border-indigo-400 mb-4 mx-auto"></div>
                    <p class="text-sm text-slate-300">Evaluating nearest spatial data...</p>
                </div>

                <div id="successResult" class="hidden animate-fade-in">
                    <span class="text-xs font-bold uppercase tracking-widest text-indigo-400 block mb-1">Estimated Valuation</span>
                    <h2 id="predictedPrice" class="text-4xl font-extrabold text-white mb-4 tracking-tight">$0.00</h2>
                    <div class="bg-slate-800/60 border border-slate-750 rounded-xl p-3 text-left w-full max-w-[240px] mx-auto">
                        <p class="text-[10px] uppercase font-bold text-slate-400 tracking-wider">Features Used</p>
                        <p id="featureSummary" class="text-xs text-slate-300 mt-1 leading-relaxed"></p>
                    </div>
                </div>
            </div>
        </div>
    </main>

    <footer class="text-center py-6 border-t border-slate-200 bg-white text-xs text-slate-400">
        &copy; 2026 Analytics Dashboard. Powered by Flask & Render.
    </footer>

    <script>
        document.getElementById('predictionForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const placeholder = document.getElementById('placeholderResult');
            const loading = document.getElementById('loadingResult');
            const success = document.getElementById('successResult');
            
            placeholder.classList.add('hidden');
            success.classList.add('hidden');
            loading.classList.remove('hidden');

            const formData = new FormData(this);
            const data = {
                beds: parseFloat(formData.get('beds')),
                baths: parseFloat(formData.get('baths')),
                size: parseFloat(formData.get('size')),
                lot_size: parseFloat(formData.get('lot_size')),
                zip_code: parseInt(formData.get('zip_code'))
            };

            try {
                const response = await fetch('/predict', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                
                const result = await response.json();
                loading.classList.add('hidden');

                if (result.success) {
                    // Format prediction dynamically
                    const formatter = new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' });
                    document.getElementById('predictedPrice').innerText = formatter.format(result.prediction);
                    
                    document.getElementById('featureSummary').innerHTML = `
                        • <b>${data.beds}</b> Bed / <b>${data.baths}</b> Bath<br>
                        • <b>${data.size}</b> sqft Living Space<br>
                        • Zip code <b>${data.zip_code}</b>
                    `;
                    success.classList.remove('hidden');
                } else {
                    alert('Error: ' + result.error);
                    placeholder.classList.remove('hidden');
                }
            } catch (err) {
                loading.classList.add('hidden');
                placeholder.classList.remove('hidden');
                alert('Failed to connect to backend server.');
            }
        });
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({'success': False, 'error': 'Model file missing or uninitialized on server.'}), 500
    
    try:
        data = request.get_json()
        
        # Exact feature array matching your tracking attributes: beds, baths, size, lot_size, zip_code
        features = np.array([[
            data['beds'],
            data['baths'],
            data['size'],
            data['lot_size'],
            data['zip_code']
        ]])
        
        prediction = model.predict(features)[0]
        
        return jsonify({
            'success': True,
            'prediction': float(prediction)
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

if __name__ == '__main__':
    # Clean port assignments for seamless cloud hosting
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
