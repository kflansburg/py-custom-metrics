#!/bin/bash
kubectl get --raw '/apis/custom.metrics.k8s.io/v1beta2/namespace/default/metric_name'
