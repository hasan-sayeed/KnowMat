import json
import os
import shutil

from flask import Flask, render_template_string, request

# Import your original classes exactly as-is:
from json_extractor import JSONExtractor
from post_processing import PostProcessor
from response_parser import ResponseParser

app = Flask(__name__)

model_options = {
    "Llama 3.1 8B Instruct (Slower model)": "llama3.1:8b-instruct-fp16",
    "Llama 3.2 3B Instruct (Faster)": "llama3.2:3b-instruct-fp16",
    "Llama 3.3 70B Instruct": "llama3.3:70b-instruct-fp16",
}


@app.route("/")
def index():
    """
    Main page with two-column layout:
      Left column: "🔧 Extraction Settings" (model dropdown, PDF file input, path, filename).
      Right column: sticky header with "KnowMat / Materials Science Data Extractor / 📊 Extracted Data",
                    plus a bottom area that displays results as we go.
    """
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8" />
      <title>KnowMat Extraction</title>
      <style>
        /* Reset page scroll */
        html, body {
          margin: 0;
          padding: 0;
          width: 100%;
          height: 100%;
          overflow: hidden; /* no global scrolling */
          font-family: sans-serif;
        }
        .container {
          display: grid;
          grid-template-columns: 320px 1fr; /* left col ~320px, right col flexible */
          width: 100%;
          height: 100%;
        }
        /* LEFT COLUMN */
        .left-column {
          display: flex;
          flex-direction: column;
          background: #f0f2f6;
          overflow-y: auto; /* independent scroll */
        }
        .left-header {
          position: sticky;
          top: 20px;
          background: #f0f2f6;
          padding: 1rem;
          font-size: 1.2rem;
          font-weight: bold;
          border-bottom: 1px solid #ddd;
          z-index: 10;
        }
        .left-content {
          padding-top: 4rem;
          padding-left: 2rem;
        }
        /* RIGHT COLUMN */
        .right-column {
          display: flex;
          flex-direction: column;
          overflow: hidden; /* we'll scroll in bottom-right only */
        }
        .top-right {
          position: sticky;
          top: 0;
          background: white;
          padding: 1rem;
          border: 1px solid #ddd;
          z-index: 10;
          flex-shrink: 0;
          text-align: center;
        }
        .separator {
          width: 100%;
          margin: 1rem auto;
          border: none;
          border-top: 2px solid #ccc;
          box-shadow: 0 2px 2px -2px gray;
        }
        .bottom-right {
          flex: 1;
          overflow-y: auto;
          margin-top: 1rem;
          padding: 1rem;
        }
        /* Some styling for messages */
        .waiting-msg {
          font-weight: bold;
          color: gray;
          margin-bottom: 0.5rem;
        }
        .error-msg {
          color: red;
          font-weight: bold;
          margin-top: 0.5rem;
        }
        .success-msg {
          color: green;
          font-weight: bold;
          margin-top: 0.5rem;
        }
        .extract-btn {
          padding: 0.5rem 1rem;
          background: #4CAF50;
          color: white;
          border: none;
          cursor: pointer;
          font-size: 1rem;
          margin-top: 1rem;
        }
        .extract-btn:hover {
          background: #45a049;
        }
        /* Spinner CSS */
        .spinner {
          border: 4px solid #f3f3f3; /* Light gray */
          border-top: 4px solid #3498db; /* Blue */
          border-radius: 50%;
          width: 16px;
          height: 16px;
          animation: spin 1s linear infinite;
          display: inline-block;
          vertical-align: middle;
          margin-right: 5px;
        }
        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }
      </style>
    </head>
    <body>
      <div class="container">
        <!-- LEFT COLUMN: Extraction Settings -->
        <div class="left-column">
          <div class="left-header">🔧 Extraction Settings</div>
          <div class="left-content">
            <label for="selected_model"><b>Select Model:</b></label><br>
            <select id="selected_model">
              {% for label, val in model_options.items() %}
              <option value="{{ label }}">{{ label }}</option>
              {% endfor %}
            </select>
            <br><br>

            <label for="pdf_files"><b>Upload PDFs:</b></label><br>
            <input type="file" id="pdf_files" multiple><br><br>

            <label for="output_path"><b>Output Folder Path:</b></label><br>
            <input type="text" id="output_path"><br><br>

            <label for="output_file_name"><b>Output File Name (e.g., extracted_data.csv):</b></label><br>
            <input type="text" id="output_file_name"><br><br>

            <button class="extract-btn" id="extractBtn">🚀 Extract Data</button>
          </div>
        </div>

        <!-- RIGHT COLUMN -->
        <div class="right-column">
          <div class="top-right">
            <h1>KnowMat</h1>
            <h3>Materials Science Data Extractor</h3>
            <hr class="separator">
            <h3>📊 Extracted Data</h3>
          </div>
          <div class="bottom-right" id="bottomRight">
            <!-- We'll append file-by-file messages here via JS -->
          </div>
        </div>
      </div>

      <!-- JavaScript to handle multi-file step-by-step uploads -->
      <script>
        const extractBtn = document.getElementById('extractBtn');
        const bottomRight = document.getElementById('bottomRight');

        extractBtn.addEventListener('click', async () => {
          bottomRight.innerHTML = ""; // clear previous content

          const selectedModel = document.getElementById('selected_model').value;
          const outputPath = document.getElementById('output_path').value.trim();
          const outputFileName = document.getElementById('output_file_name').value.trim();
          const pdfFiles = document.getElementById('pdf_files').files;

          if (!pdfFiles.length || !outputPath || !outputFileName) {
            bottomRight.innerHTML = "<div class='error-msg'>⚠️ Please select files, output path, and file name.</div>";
            return;
          }

          // Process each file in a loop, making one request per file.
          for (let i = 0; i < pdfFiles.length; i++) {
            const file = pdfFiles[i];
            const fileName = file.name;

            // 1) Show a waiting message for this file with a spinner.
            const waitingDiv = document.createElement('div');
            waitingDiv.classList.add('waiting-msg');
            waitingDiv.innerHTML = `<span class="spinner"></span> Waiting for LLM to extract data from <b>${fileName}</b>...`;
            bottomRight.appendChild(waitingDiv);

            // 2) Build form data for this single file.
            const formData = new FormData();
            formData.append('selected_model', selectedModel);
            formData.append('output_path', outputPath);
            formData.append('output_file_name', outputFileName);
            formData.append('pdf', file); // single file

            // 3) Make request to server.
            try {
              const response = await fetch('/extract_one', {
                method: 'POST',
                body: formData
              });
              const resultHTML = await response.text();

              // 4) Replace the waiting message with the final results.
              waitingDiv.remove(); // remove waiting message

              // Insert the results.
              const resultContainer = document.createElement('div');
              resultContainer.innerHTML = resultHTML;
              bottomRight.appendChild(resultContainer);

            } catch (err) {
              waitingDiv.remove();
              const errorDiv = document.createElement('div');
              errorDiv.classList.add('error-msg');
              errorDiv.innerHTML = `❌ Error processing ${fileName}: ${err.message}`;
              bottomRight.appendChild(errorDiv);
              return;
            }
          }

          // All files processed:
          const doneMsg = document.createElement('div');
          doneMsg.classList.add('success-msg');
          doneMsg.textContent = "✅ Data extraction completed!";
          bottomRight.appendChild(doneMsg);
        });
      </script>
    </body>
    </html>
    """

    return render_template_string(html_template, model_options=model_options)


@app.route("/extract_one", methods=["POST"])
def extract_one():
    """
    Receives a single file to process.
    Runs the same extraction logic as your original code.
    Returns an HTML snippet showing the results for this file.
    """
    selected_model_key = request.form.get("selected_model", "")
    output_path = request.form.get("output_path", "")
    output_file_name = request.form.get("output_file_name", "")

    file = request.files.get("pdf")  # single PDF from the form
    if not file or not output_path or not output_file_name:
        return "<div class='error-msg'>⚠️ Missing inputs (PDF, output path, or file name).</div>"

    file_name = file.filename
    results_html = ""

    try:
        # 1) Create temp folder for each file.
        temp_root = "temp_pdfs"
        if not os.path.exists(temp_root):
            os.makedirs(temp_root, exist_ok=True)

        # Each file in its own subfolder.
        temp_folder = os.path.join(temp_root, os.path.splitext(file_name)[0])
        if os.path.exists(temp_folder):
            shutil.rmtree(temp_folder)
        os.makedirs(temp_folder, exist_ok=True)

        file_path = os.path.join(temp_folder, file_name)
        with open(file_path, "wb") as f:
            f.write(file.read())

        # 2) Extract with your LLM logic.
        model_name = model_options.get(selected_model_key, "")
        extracted_result = JSONExtractor.extract(temp_folder, model_name)

        # 3) Save to CSV.
        extracted_data_file = os.path.join(output_path, output_file_name)
        ResponseParser.save_to_csv(extracted_result, output_path, output_file_name)

        # 4) Post-process (update CSV) and update JSON with new keys.
        processor = PostProcessor("src/knowmat/properties.json", extracted_data_file)
        processor.process_extracted_data()
        extracted_result = processor.update_extracted_json(extracted_result)

        # 5) Build HTML for the results, now including new keys after property_name.
        results_html += f"<h3>📄 File: {file_name}</h3>"
        for composition in extracted_result[0]["data"].compositions:
            composition_dict = {
                "composition": composition.composition,
                "processing_conditions": composition.processing_conditions,
                "characterization": composition.characterization,
                "properties": [],
            }
            for prop in composition.properties_of_composition:
                prop_dict = {
                    "property_name": prop.property_name,
                    "value": prop.value,
                    "unit": prop.unit,
                    "measurement_condition": prop.measurement_condition,
                    "standard_property_name": prop.standard_property_name,
                    "category": prop.category,
                    "domain": prop.domain,
                }
                composition_dict["properties"].append(prop_dict)
            results_html += f"<pre>{json.dumps(composition_dict, indent=2, ensure_ascii=False)}</pre>"

        return results_html

    except Exception as e:
        return f"<div class='error-msg'>❌ Error processing {file_name}: {e}</div>"


if __name__ == "__main__":
    app.run(debug=True)
