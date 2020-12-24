#!/bin/bash

kubectl create namespace custom-metrics

echo "Creating self-signed certificate"

./scripts/certs.sh

kubectl create secret tls -n custom-metrics certs --cert=server.crt --key=server.key

kubectl create configmap -n custom-metrics app --from-file=src/ 

kubectl apply -f manifests/deployment.yaml

kubectl apply -f manifests/service.yaml

case `uname` in
        Darwin)
            b64_opts='-b=0'
            ;;
        *)
            b64_opts='--wrap=0'
esac

export CA_BUNDLE=$(cat ca.crt | base64 ${b64_opts})

cat manifests/api-service.yaml | envsubst | kubectl apply -f -

rm server.crt
rm server.key
rm ca.crt
