#!/bin/bash
# Base functions
readonly LOG_TYPE_INFO=11
readonly LOG_TYPE_ERROR=12
readonly LOG_PLACEHOLDER_ERROR="[ERROR]"
readonly LOG_PLACEHOLDER_INFO="[INFO]"

log_output () {
  if [ -z "$1" ] || [ -z "$2" ]; then
    echo "$LOG_PLACEHOLDER_ERROR No log type or message given."
    exit 1
  fi
  if [[ "$1" -eq LOG_TYPE_INFO ]]; then
    echo "$LOG_PLACEHOLDER_INFO $2"
  fi
  if [[ "$1" -eq LOG_TYPE_ERROR ]]; then
    echo "$LOG_PLACEHOLDER_ERROR $2"
  fi
}

if [ -n "$(command -v apt-get)" ]; then
  ## APT package manager ##
  # Install Components
  log_output LOG_TYPE_INFO "Install components"
  sudo apt update -y
  sudo apt install python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools -y

  # Install python3-venv
  sudo apt install python3-venv -y

  log_output LOG_TYPE_INFO "Setup virtual python environment"
  python3 -m venv studenttracker

  source studenttracker/bin/activate

  log_output LOG_TYPE_INFO "Install gunicorn, wheel and flask"
  pip install wheel

  pip install gunicorn flask

  pip install requests

  log_output LOG_TYPE_INFO "Generating token and placing it in environmental variable"
  export TOKEN="127da7ef-bbdc-4789-9fda-e3c72a25e8b4"

  pip install -r requirements.txt

  gunicorn --bind 0.0.0.0:5000 wsgi:app
fi
