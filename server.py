from kubernetes import client, config
from flask import Flask,request
from os import path
import yaml, random, string, json
import sys
import json

# Configs can be set in Configuration class directly or using helper utility
config.load_kube_config()
v1 = client.CoreV1Api()
app = Flask(__name__)
# app.run(debug = True)

@app.route('/config', methods=['GET'])
def get_config():
    pods = []

    # pods = v1.list_pod_for_all_namespaces()

    output = {"pods": pods}
    output = json.dumps(output)

    return output, 200

@app.route('/img-classification/free',methods=['POST'])
def post_free():

    f= open("free-job.yaml")
    job_yml = yaml.safe_load(f)
    v1.create_namespaced_job(job_yml)
    return "success", 200

@app.route('/img-classification/premium', methods=['POST'])
def post_premium():
    f= open("job-premium.yaml")
    job_yml = yaml.safe_load(f)
    v1.create_namespaced_job(job_yml)
    return "success", 200

    
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000)
