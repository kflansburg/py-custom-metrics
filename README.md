# py-custom-metrics

![Code Quality](https://github.com/kflansburg/py-custom-metrics/workflows/Code%20Quality/badge.svg?branch=main)

Kubernetes custom metrics plumbing for Python

## Architecture

This code includes a Flask API which implements the Kubernetes Custom Metrics
API which is described in detail
[here](https://stupefied-goodall-e282f7.netlify.app/contributors/design-proposals/instrumentation/custom-metrics-api/).

The three major routes that you may wish to implement are:

- `namespace`: Get metrics on a Namespace.
- `cluster_objects`: Get metrics for one or more cluster-scoped objects, by
  name or label selector.
- `namespaced_objects`: Get metrics for one or more namespace-scoped objects,
  by name or label selector.

For instance, a Horizontal Pod Autoscaler (HPA) v2 configured for a Deployment
with the following metrics will query the `namespaced_objects` endpoint for the
`foo` metric with the label selector defined in the Deployment.

```yaml
  - type: Pods
    pods:
      metric:
        name: foo
      target:
        averageValue: 50
        type: "AverageValue"
```

All three routes should return a `MetricValueList`, which is defined in
[this proto file](https://github.com/kubernetes/metrics/blob/master/pkg/apis/custom_metrics/v1beta2/generated.proto).
This is reimplemented with `dataclasses` here.

The application is installed as a [Deployment](manifests/deployment.yaml) and
[Service](manifests/service.yaml) in the `custom-metrics` Namespace. It serves
a self-signed certificate. The API is registered with Kubernetes using an
[APIService](manifests/api-service.yaml) which includes the signing CA bundle
for TLS authentication.

Kubernetes will query the root API path, as well as for an OpenAPI
specification (unimplemented). If the root path query is successful, the API
registration will complete and Kubernetes will begin
[aggregating](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/apiserver-aggregation/)
these API endpoints.

## Development

For easy development, run `scripts/develop.sh`. This will configure Kubernetes
(tested in [Kind](https://kind.sigs.k8s.io/)) to query your host machine on
8443, and start Flask in development mode on the same port (with
live-reloading).

As a smoke test, you may wish to run `scripts/test.sh` which will query
for the metric `metric_name` on the `default` namespace.

## Deployment

Once you have finished development, the script `scripts/deploy.sh` will deploy
the code to run in Kubernetes with a more secure TLS configuration. If your
code can run in a distributed manner (there is no shared state), you may wish
to increase the number of replicas of this Deployment.

## Removal

Run `scripts/remove.sh` to reverse `scripts/deploy.sh`.
