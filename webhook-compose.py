import logging
import os
import shlex
import sys

from flask import Flask, request, json
from werkzeug.exceptions import BadRequest

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

app = Flask(__name__)
home = os.getcwd()

with open("webhook-compose.conf") as f:
    config = json.load(f)


def deep_match(truth, subject):
    if type(truth) is not type(subject):
        return False

    if isinstance(truth, dict):
        for key, value in truth.items():
            if not deep_match(value, subject.get(key)):
                return False
        return True
    else:
        return truth == subject


@app.route("/", methods=["POST"])
def webhook():
    subject = {
        "headers": {key.lower(): value for key, value in request.headers.items()},
        "body": request.get_json(),
    }

    for rule, match in config.items():
        if deep_match(match, subject):
            break
    else:
        logger.warning("No rule found for %s.", repr(subject))
        raise BadRequest()

    if ":" in rule:
        path, project = rule.split(":", 1)
    else:
        path = rule
        project = os.path.filename(path)

    if not os.path.isabs(path):
        path = os.path.join(home, path)

    logger.info("Updating project %s in %s.", project, path)
    try:
        os.chdir(path)
        os.system(
            "docker-compose -p {project} pull && "
            "docker-compose -p {project} up -d --build".format(
                project=shlex.quote(project)
            )
        )
    finally:
        os.chdir(home)

    return json.jsonify({"result": "ok"})
