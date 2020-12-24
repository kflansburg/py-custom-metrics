#!/bin/bash

kubectl delete -f manifests/service.yaml

kubectl delete -f manifests/deployment.yaml

kubectl delete secret -n custom-metrics certs

kubectl delete configmap -n custom-metrics app

kubectl delete apiservice v1beta2.custom.metrics.k8s.io

kubectl delete namespace custom-metrics
