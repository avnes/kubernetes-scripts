#!/usr/bin/env python3
import csv

# export KUBECONFIG=<REDACTED>
# kubectl get pods -A \
# -o custom-columns='NAMESPACE:.metadata.namespace,NAME:.metadata.name,LIVENESS_PROBE_TIMEOUT:spec.containers[*].livenessProbe.timeoutSeconds,READINESS_PROBE_TIMEOUT:spec.containers[*].readinessProbe.timeoutSeconds' \
# | awk '{if ($3 != "<none>" || $4 != "<none>") print $0 }' | grep -v NAMESPACE > all_pods_in_all_ns.txt


def find_pods_with_probes(unique: bool = False):
    with open("all_pods_in_all_ns.txt", "r") as pod_file:
        lines: list = pod_file.readlines()
        old_pod: str = ""
        counter: int = 0
        with open("all_pods_in_all_ns.csv", "w", newline="") as csvfile:
            dp_writer = csv.writer(csvfile, delimiter=",")
            dp_writer.writerow(
                [
                    "Namespace",
                    "Pod unique name",
                    "Liveness Probe timeout",
                    "Readiness Probe timeout",
                ]
            )
            for line in lines:
                compacted: str = " ".join(
                    line.split()
                ).split()  # Basically remove all additional spaces
                ns: str = compacted[0]
                pod: str = compacted[1]
                if unique:
                    pod_unique: str = pod[0 : pod.rfind("-")]
                    if pod_unique != old_pod:
                        dp_writer.writerow(
                            [
                                ns,
                                pod_unique,
                                compacted[2],
                                compacted[3],
                            ]
                        )
                        counter += 1
                    old_pod = pod_unique
                else:
                    dp_writer.writerow(
                        [
                            ns,
                            pod,
                            compacted[2],
                            compacted[3],
                        ]
                    )
                    counter += 1

    print(f"Found {counter} instances.")


if __name__ == "__main__":
    find_pods_with_probes()
