#!python3
import command

direction="down"

namespaces=command.run(["kubectl","get","namespaces","-o","jsonpath={.items[*].metadata.name}"]).output.decode('utf-8').split(" ")
print(namespaces)

exclusionlist=['argocd', 'cert-manager', 'default', 'experimental', 'istio-ingress', 'istio-system', 'kube-node-lease', 'kube-public', 'kube-system', 'kuna-experimental', 'observability', 'socket-cluster',  'test-helm', 'test-helm2', 'vault', 'vault-webhook']

#Deployments scale
for name in namespaces:
        if name not in exclusionlist:
                try:
                        print("Scaling down all the deployments in",name)
                        print("-" * 80)
                        command.run(["kubectl","scale","deployment","-n",name,"--replicas","0","--all"])
                except Exception as e:
                        print("Skipping due to error",e)
                try:  
                         daemonsets=command.run(["kubectl","-n", name ,"get","daemonsets","-o","jsonpath={.items[*].metadata.name}"]).output.decode('utf-8').split(" ")          
                         print(daemonsets)
                except Exception as e:
                       print("Skipping due to error", e)
            
                try:
                        print("Scaling down all deamonset in ", name)
                        print("-" * 80)
                        command.run(["kubectl", "patch", "daemonset", "fluentd-elasticsearch", "-n", name, "-p", "{\"spec\": {\"template\": {\"spec\": {\"nodeSelector\": {\"non-existing\": \"true\"}}}}}"])
                        
                except Exception as e:
                       print("Skipping due to error", e)
