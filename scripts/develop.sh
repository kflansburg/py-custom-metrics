#!/bin/bash

case `uname` in
        Darwin)
            ip=$(ipconfig getifaddr en0)
            ;;
        *)
            ip="172.17.0.1"
esac


kubectl create namespace custom-metrics

export ENDPOINT=$ip

cat manifests/service-develop.yaml | envsubst | kubectl apply -f -

cat manifests/api-service.yaml | envsubst | kubectl apply -f -

FLASK_ENV=development python src/app.py

kubectl delete apiservice v1beta2.custom.metrics.k8s.io

kubectl delete namespace custom-metrics
