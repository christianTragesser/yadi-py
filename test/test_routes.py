import pytest
import requests
import json
import os

# UAT tests for simple flask routes.

host = 'yadi'
port = '5000'

def test_get_root_no_headers():
    path = '/'
    url = 'http://{0:s}:{1:s}{2:s}'.format(host, port, path)
    r = requests.get(url)
    assert r.status_code == 404

def test_get_root_with_headers():
    path = '/'
    url = 'http://{0:s}:{1:s}{2:s}'.format(host, port, path)
    headers = {
        'number': '4'
    }
    r = requests.get(url, headers = headers)
    assert r.status_code == 200
    assert r.text == 'Yadi, Yadi, Yadi...\n'

def test_get_status():
    path = '/status'
    url = 'http://{0:s}:{1:s}{2:s}'.format(host, port, path)
    # Read in version file provided by automated pipeline
    versionFile = '../GIT_SHA'
    if os.path.exists(versionFile):
        shaFile = open(versionFile, 'r')
        gitSHA = shaFile.read()
        gitSHA = gitSHA.replace('\n', '')
        shaFile.close()
    else:
        gitSHA = 'non-pipeline build'
    expected_status = {"sha": gitSHA, "path": "/webhook"}

    r = requests.get(url)
    assert r.status_code == 200
    assert json.dumps(r.json()) == json.dumps(expected_status)

def test_post():
    path = '/webhook'
    url = 'http://{0:s}:{1:s}{2:s}'.format(host, port, path)
    payload = json.load(open('test.json', 'r'))
    headers = { 'X-Gitlab-Event': 'Pipeline Hook' }
    r = requests.post(url, json=payload, headers=headers)
    assert r.status_code == 200
    assert r.text == 'OK'