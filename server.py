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

    ret = v1.list_pod_for_all_namespaces(watch=False)
    for i in ret.items:
        pods.append(
            {
                "node": i.spec.node_name,
                "ip": i.status.pod_ip,
                "namespace": i.metadata.namespace,
                "name": i.metadata.name,            
                "status": i.status.phase,
            }
        )

    output = {"pods": pods}
    output = json.dumps(output)

    return output, 200

@app.route('/img-classification/free',methods=['POST'])
def post_free():

    f= open("job-free.yml")
    job_yml = yaml.safe_load(f)
    api_instance = client.BatchV1Api(v1)
    api_response = api_instance.create_namespaced_job(namespace='free-service',body=job_yml)
    return api_response

@app.route('/img-classification/premium', methods=['POST'])
def post_premium():
    f= open("job-premium.yml")
    job_yml = yaml.safe_load(f)
    api_instance = client.BatchV1Api(v1)
    api_response = api_instance.create_namespaced_job(namespace='default',body=job_yml)
    return api_response
    
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000)
