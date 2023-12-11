from flask import Flask, request, render_template, jsonify
from requests.auth import HTTPBasicAuth
import json
from dotenv import load_dotenv
import os
import requests
import hmac
import hashlib

app = Flask(__name__)

# Load environment variables
load_dotenv()

# Jira credentials
jira_email = os.environ.get("JIRA_EMAIL")
jira_api_token = os.environ.get("JIRA_API_TOKEN")
jira_base_url = "https://santoshtechguyjira.atlassian.net"

# Jira project key
jira_project_key = "TP"

# Jira issue type
jira_issue_type = "10006"


@app.route("/github_webhook", methods=["POST"])
def github_webhook():
    payload = request.json

    if "issue" in payload and "comment" in payload:
        issue_comment = payload["comment"]["body"]
        jira_keywords = ["/jira", "/Jira", "/JIRA"]

        if any(keyword in issue_comment for keyword in jira_keywords):
            result_message = create_jira_issue(payload)
            return render_template("result.html", result_message=result_message)

    return jsonify({"message": "Webhook received successfully"}), 200

def create_jira_issue(payload):
    url = f"{jira_base_url}/rest/api/3/issue"
    auth = HTTPBasicAuth(jira_email, jira_api_token)
    headers = {"Accept": "application/json", "Content-Type": "application/json"}

    issue_title = payload["issue"]["title"]
    issue_body = payload["comment"]["body"]

    jira_payload = {
        "fields": {
            "description": {
                "content": [
                    {
                        "content": [{"type": "text", "text": issue_body}],
                        "type": "paragraph",
                    }
                ],
                "type": "doc",
                "version": 1,
            },
            "issuetype": {"id": jira_issue_type},
            "project": {"key": jira_project_key},
            "summary": issue_title,
        },
        "update": {},
    }

    response = requests.request("POST", url, json=jira_payload, headers=headers, auth=auth)
    result_message = json.loads(response.text).get("key", "Unknown issue key")

    return result_message


if __name__ == "__main__":
    app.run("0.0.0.0", port=5000)