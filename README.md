# cluster-resources-scaler
on off all services types in cluster for cost saving



    Scaling k8s daemonset down to zero

kubectl -n kube-system patch daemonset myDaemonset -p '{"spec": {"template": {"spec": {"nodeSelector": {"non-existing": "true"}}}}}'

    Scaling up k8s daemonset

kubectl -n kube-system patch daemonset myDaemonset --type json -p='[{"op": "remove", "path": "/spec/template/spec/nodeSelector/non-existing"}]'

