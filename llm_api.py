import os
from flask import Flask, request, jsonify
from llama_cpp import Llama

MODEL_PATH = os.path.join("models", "Phi-3-mini-4k-instruct-q4.gguf")

print("Loading local LLM with llama-cpp-python...")
llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=4096,
    n_threads=8,
    n_gpu_layers=-1
)
print("LLM loaded successfully.")

app = Flask(__name__)

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    if not data or 'inputs' not in data:
        return jsonify({"error": "Missing 'inputs' in request body"}), 400

    prompt = data['inputs']
    params = data.get('parameters', {})

    output = llm(
        prompt,
        max_tokens=params.get('max_new_tokens', 20),
        stop=["<|end|>"],
        echo=False,
        temperature=params.get('temperature', 0.3) 
    )
    
    generated_text = output['choices'][0]['text']

    response_data = [{"generated_text": generated_text}]
    return jsonify(response_data)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)