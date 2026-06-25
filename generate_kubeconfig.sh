#!/bin/sh

# Define the API server URL using environment variables
API_SERVER="https://${KUBERNETES_SERVICE_HOST}:${KUBERNETES_SERVICE_PORT}"

# Read the service account token, CA certificate, and namespace
TOKEN=$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)
NAMESPACE=$(cat /var/run/secrets/kubernetes.io/serviceaccount/namespace)
CA_CERT="/var/run/secrets/kubernetes.io/serviceaccount/ca.crt"

mkdir -p /home/django/.kube/

# Specify the output path for kubeconfig
KUBECONFIG_PATH="/home/django/.kube/config"

# Create the kubeconfig file
cat <<EOF > $KUBECONFIG_PATH
apiVersion: v1
kind: Config
clusters:
- name: kubernetes
  cluster:
    certificate-authority: $CA_CERT
    server: $API_SERVER
contexts:
- name: default
  context:
    cluster: kubernetes
    user: default
current-context: default
users:
- name: default
  user:
    token: $TOKEN
EOF

echo "Kubeconfig created at $KUBECONFIG_PATH"