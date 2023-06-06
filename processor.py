#!python3
import command


direction = "down"

namespaces = command.run(["kubectl", "get", "namespaces", "-o", "jsonpath={.items[*].metadata.name}"]).output.decode(
    'utf-8').split(" ")
print(namespaces)



exclusionlist = ['default',   'kube-node-lease', 'kube-public', 'kube-system']
#'istio-ingress', 'istio-system', 'istio-ingress-private',

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
           print("-" * 180)
           print()
           command.run(["kubectl", "-n", name, "scale", "deployment", "--replicas", str(scale_dir), "--all"])
       except Exception as e:
           print("Skipping due to error", e)

       # try:
       #     print("-" * 180)
       #     print()
       #     print("Statefulsets  .... ")
       #     stateful_sets = command.run(
       #         ["kubectl", "-n", name, "get", "statefulsets", "-o", "jsonpath={.items[*].metadata.name}" ]).output.decode(
       #         'utf-8').split(" ")
       #     print(stateful_sets)
       #     print("-" * 180)
       #     print()
       #     for statefulset in stateful_sets:
       #         # scale_daemonsets(daemon, "up")
       #         if direction == "down":
       #             try:
       #
       #                 print("Scaling ", direction, "  statefulsets  ", statefulset, " in ", name)
       #                 print("-" * 180)
       #                 command.run(["kubectl", "patch", "statefulset", statefulset, "-n", name, "-p",
       #                              "{\"spec\": {\"template\": {\"spec\": {\"nodeSelector\": {\"non-existing\": \"true\"}}}}}"])
       #
       #             except Exception as e:
       #                 print("Skipping due to error in statefulset DOWN", e)
       #         elif direction == "up":
       #             try:
       #
       #                 print("Scaling ", direction, " deamonset ", statefulset, " in ", name)
       #                 print("-" * 180)
       #                 command.run(["kubectl", "-n", name, "patch", "statefulset", statefulset, "--type", "json",
       #                              "-p=[{\"op\": \"remove\", \"path\": \"/spec/template/spec/nodeSelector/non-existing\"}]"])
       #
       #             except Exception as e:
       #                 print("Skipping due to error statefulset UP", e)
       #         else:
       #             print("Skipping. WRONG direction for daemonset")
       # except Exception as e:
       #     print("Skipping due to error", e)

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

