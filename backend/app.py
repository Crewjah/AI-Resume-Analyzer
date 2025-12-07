import os
import tempfile
from flask import Flask, request, jsonify

# CORS: prefer flask-cors if available; otherwise add a tiny fallback
try:
    from flask_cors import CORS  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    CORS = None

from src.analyzer import ResumeAnalyzer

app = Flask(__name__)
if CORS:
    CORS(app)
else:
    @app.after_request
    def _cors_fallback(resp):
        resp.headers.setdefault("Access-Control-Allow-Origin", "*")
        resp.headers.setdefault("Access-Control-Allow-Headers", "Content-Type, Authorization")
        resp.headers.setdefault("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
        return resp


def _extract_job_description(req: request) -> str:
    # Accept job description via form field or JSON for flexibility
    jd = req.form.get("job_description") if req.form else None
    if jd:
        return jd
    try:
        data = req.get_json(silent=True) or {}
        return data.get("job_description", "") if isinstance(data, dict) else ""
    except Exception:
        return ""


@app.route("/health")
def health() -> jsonify:
    return jsonify({"status": "healthy", "service": "AI Resume Analyzer", "version": "2.0"})


@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        if "file" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files["file"]
        if file.filename == "":
            return jsonify({"error": "No file selected"}), 400

        job_description = _extract_job_description(request)

        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp_file:
            file.save(tmp_file.name)
            analyzer = ResumeAnalyzer()

            try:
                resume_text = analyzer.extract_text_from_file(tmp_file.name)
            except Exception:
                # Fallback: read bytes and decode
                try:
                    with open(tmp_file.name, "rb") as f:
                        resume_text = f.read().decode("utf-8", errors="ignore")
                except Exception:
                    resume_text = ""

            try:
                analysis = analyzer.analyze_resume(resume_text, job_description)
            finally:
                try:
                    os.unlink(tmp_file.name)
                except Exception:
                    pass

            if isinstance(analysis, dict) and analysis.get("valid") is False:
                return jsonify({"error": analysis.get("message", "Invalid resume content")}), 400

            return jsonify(analysis)

    except Exception as e:
        return jsonify({"error": f"Analysis failed: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
