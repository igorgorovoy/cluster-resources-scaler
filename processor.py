#!python3
import command


direction = "up" 
            
# def scale_deployments(dep_name, direction):
#     if direction == "down":
#         scale = 0
#     elif direction == "up":
#         scale = 1
#     print("Direction towards ", scale)
#     try:
#         print("Scaling ", direction ," all the deployments in", dep_name)
#         print("-" * 80)
#         command.run(["kubectl", "scale", "deployment", "-n", dep_name, "--replicas", scale, "--all"])
#     except Exception as e:
#         print("Skipping due to error", e)


# def scale_daemonsets(daemon_name, direction):
#     if direction == "down":
#         try:
# 
#             print("Scaling ", direction ,"  deamonset  ",daemon_name," in ", name)
#             print("-" * 180)
#             command.run(["kubectl", "patch", "daemonset", daemon_name , "-n", name, "-p",
#                          "{\"spec\": {\"template\": {\"spec\": {\"nodeSelector\": {\"non-existing\": \"true\"}}}}}"])
# 
#         except Exception as e:
#             print("Skipping due to error in scale_daemonsets DOWN", e)
#     elif direction == "up":
#         try:
# 
#             print("Scaling ", direction ," deamonset ",daemon_name," in ", name)
#             print("-" * 180)
#             command.run(["kubectl", "patch", "daemonset", daemon_name, "-n", name, "-p",
#                          "[{\"op\": \"remove\", \"path\": \"/spec/template/spec/nodeSelector/non-existing\"}]"])
# 
#         except Exception as e:
#             print("Skipping due to error scale_daemonsets UP", e)



namespaces = command.run(["kubectl", "get", "namespaces", "-o", "jsonpath={.items[*].metadata.name}"]).output.decode(
    'utf-8').split(" ")
print(namespaces)

exclusionlist = ['argocd', 'cert-manager', 'default', 'experimental', 'istio-ingress', 'istio-system',
                 'kube-node-lease', 'kube-public', 'kube-system', 'kuna-experimental', 'observability',
                 'socket-cluster', 'test-helm', 'test-helm2', 'vault', 'vault-webhook']

# Deployments scale
for name in namespaces:
    if name not in exclusionlist:
        
       if direction == "down":
          scale_dir = 0
       elif direction == "up":
          scale_dir = 1
       else:
          scale_dir =  direction
    
       print("Direction towards ", scale_dir)
       
       try:
           print("Scaling ", direction ," all the deployments in", name)
           print("-" * 80)
           print()
           command.run(["kubectl", "scale", "deployment", "-n", name, "--replicas", str(scale_dir), "--all"])
       except Exception as e:
           print("Skipping due to error", e)
        

       try:

            daemonsets = command.run(
                ["kubectl", "-n", name, "get", "daemonsets", "-o", "jsonpath={.items[*].metadata.name}"]).output.decode(
                'utf-8').split(" ")
            print(daemonsets)

            for daemon in daemonsets:
                #scale_daemonsets(daemon, "up")
                if direction == "down":
                    try:

                        print("Scaling ", direction, "  deamonset  ", daemon, " in ", name)
                        print("-" * 180)
                        command.run(["kubectl", "patch", "daemonset", daemon, "-n", name, "-p",
                                     "{\"spec\": {\"template\": {\"spec\": {\"nodeSelector\": {\"non-existing\": \"true\"}}}}}"])

                    except Exception as e:
                        print("Skipping due to error in scale_daemonsets DOWN", e)
                elif direction == "up":
                    try:

                        print("Scaling ", direction, " deamonset ", daemon, " in ", name)
                        print("-" * 180)
                        command.run(["kubectl", "-n", name, "patch", "daemonset", daemon,  "--type", "json", "-p=[{\"op\": \"remove\", \"path\": \"/spec/template/spec/nodeSelector/non-existing\"}]"])

                    except Exception as e:
                        print("Skipping due to error scale_daemonsets UP", e)
                else:
                    print("Skipping. WRONG direction for daemonset")

       except Exception as e:
            print("Skipping due to error in daemonsets loop", e)