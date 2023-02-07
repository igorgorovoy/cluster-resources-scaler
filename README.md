# cluster-resources-scaler
on off all services types in cluster for cost saving



    Scaling k8s daemonset down to zero

kubectl -n kube-system patch daemonset myDaemonset -p '{"spec": {"template": {"spec": {"nodeSelector": {"non-existing": "true"}}}}}'

    Scaling up k8s daemonset

kubectl -n kube-system patch daemonset myDaemonset --type json -p='[{"op": "remove", "path": "/spec/template/spec/nodeSelector/non-existing"}]'


```python
def scale_deployments(dep_name, direction):
    if direction == "down":
        scale = 0
    elif direction == "up":
        scale = 1
    print("Direction towards ", scale)
    try:
        print("Scaling ", direction ," all the deployments in", dep_name)
        print("-" * 80)
        command.run(["kubectl", "scale", "deployment", "-n", dep_name, "--replicas", scale, "--all"])
    except Exception as e:
        print("Skipping due to error", e)
```

```python
def scale_daemonsets(daemon_name, direction):
    if direction == "down":
        try:

            print("Scaling ", direction ,"  deamonset  ",daemon_name," in ", name)
            print("-" * 180)
            command.run(["kubectl", "patch", "daemonset", daemon_name , "-n", name, "-p",
                         "{\"spec\": {\"template\": {\"spec\": {\"nodeSelector\": {\"non-existing\": \"true\"}}}}}"])

        except Exception as e:
            print("Skipping due to error in scale_daemonsets DOWN", e)
    elif direction == "up":
        try:

            print("Scaling ", direction ," deamonset ",daemon_name," in ", name)
            print("-" * 180)
            command.run(["kubectl", "patch", "daemonset", daemon_name, "-n", name, "-p",
                         "[{\"op\": \"remove\", \"path\": \"/spec/template/spec/nodeSelector/non-existing\"}]"])

        except Exception as e:
            print("Skipping due to error scale_daemonsets UP", e)


```