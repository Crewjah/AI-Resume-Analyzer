#!/bin/bash
set -euo pipefail

# Simple smoke test script for local API
BASE_URL=${1:-http://127.0.0.1:5000}

echo "Checking health endpoint: ${BASE_URL}/health"
curl -s ${BASE_URL}/health | jq || true

echo "Posting sample resume to /analyze"
cat > /tmp/sample_resume.txt <<EOF
John Doe
Software Engineer
Experience: 5 years of experience in Python, Flask, AWS, Docker.
Skills: Python, Flask, Docker, AWS, SQL
Contact: john.doe@example.com
EOF

curl -s -F "file=@/tmp/sample_resume.txt" ${BASE_URL}/analyze | jq || true

echo "Smoke test complete"
