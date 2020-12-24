from flask import Flask
from flask.json import jsonify
from typing import Optional, Dict, List
from dataclasses import dataclass, asdict, field

app = Flask(__name__)

API_PATH = "/apis/custom.metrics.k8s.io/v1beta2"

# The null values I use in this module are Go "null" values,
# which are of course "", {}, etc. 🙃


@dataclass
class MetricIdentifier:
    """ Identifies a metric by name and, optionally, selector.

    Args:
        name (str): The name of the given metric.
        selector (dict, optional): Default None. Represents the label selector
            that could be used to select this metric, and will generally just
            be the selector passed into the query used to fetch this metric.
    """
    name: str
    selector: Optional[Dict[str, str]] = field(default_factory=dict)


@dataclass
class MetricValue:
    """ The metric value for some object.

    Args:
        metric (MetricIdentifier): Identifier for the metric this value is
            associated with.
        value (str): A Kubernetes Quantity indicating the value of the metric.
        time (str, optional): Default None. An optional timestamp associated
            witht he value. Should follow RFC3339.
        windowSeconds (int, optional): Default None. Indicates the window over
            which the the metric was calculated. 0 for instantaneous metrics.
        describedObject (dict, optional): Default None. A Kubernetes
            ObjectReference describing the object that the metric was collected
            from.
    """
    metric: MetricIdentifier
    value: str
    time: Optional[str] = ""
    windowSeconds: Optional[int] = 0
    describedObject: Optional[Dict[str, str]] = field(default_factory=dict)


@dataclass
class MetricValueList:
    """ List of values for a given metric for some set of objects.

    Args:
       items (list): The value of the metric across the described objects.
    """
    items: List[MetricValue]
    apiVersion: str = "custom.metrics.k8s.io/v1beta2"
    kind: str = "MetricValueList"


@app.route(
    API_PATH
)
def root():
    """ Root API Path

    This appears to act as a health check and must return Ok
    to complete the API registration process with Kubernetes.
    """
    return jsonify({})


@app.route(
    "/openapi/v2"
)
def openapi():
    """ OpenAPI Spec for API Extensions

    Kubernetes API Server scrapes this, but it appears to be optional.
    """
    return jsonify({})


@app.route(
    f"{API_PATH}/namespaces/<namespace>/metrics/<metric_name>"
)
def namespace(
    namespace: str,
    metric_name: str
):
    """ Get metric for a Namespace.

    Args:
        namespace (str): The Kubernetes Namespace.
    """

    metric = MetricIdentifier(name=metric_name)
    metric_value = MetricValue(metric=metric, value="40")
    metric_value_list = MetricValueList(items=[metric_value])

    return jsonify(asdict(metric_value_list))


@app.route(
    f"{API_PATH}/<resource>/<name>/<metric_name>"
)
def cluster_objects(
    resource: str,
    name: str,
    metric_name: str
):
    """ Get metric for cluster-scoped objects.

    Args:
        resource (str): The Kubernetes Resource type (pod, service, etc.)
        name (str): The name of the specific resource.
            Could be '*' to match all or use label selector.
        metric_name (str): The metric being queries.
    """
    # label_selector: Optional[str] = \
    #     request.args.get('labelSelector')
    # metric_label_selector: Optional[str] = \
    #     request.args.get('metricLabelSelector')

    metric = MetricIdentifier(name=metric_name)
    metric_value = MetricValue(metric=metric, value="40")
    metric_value_list = MetricValueList(items=[metric_value])

    return jsonify(asdict(metric_value_list))


@app.route(
    f"{API_PATH}/namespaces/<namespace>/<resource>/<name>/<metric_name>"
)
def namespaced_objects(
    namespace: str,
    resource: str,
    name: str,
    metric_name: str
):
    """ Get metric for objects in Namespace.

    Args:
        namespace (str): The Kubernetes Namespace.
        resource (str): The Kubernetes Resource type (pod, service, etc.)
        name (str): The name of the specific resource.
            Could be '*' to match all or use label selector.
        metric_name (str): The metric being queries.
    """
    # label_selector: Optional[str] = \
    #     request.args.get('labelSelector')
    # metric_label_selector: Optional[str] = \
    #     request.args.get('metricLabelSelector')

    metric = MetricIdentifier(name=metric_name)
    metric_value = MetricValue(metric=metric, value="40")
    metric_value_list = MetricValueList(items=[metric_value])

    return jsonify(asdict(metric_value_list))


if __name__ == "__main__":
    app.run(ssl_context='adhoc', port=8443, host='0.0.0.0')
