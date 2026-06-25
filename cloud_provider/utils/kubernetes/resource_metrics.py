def parse_cpu(cpu_str):
    cpu_str = str(cpu_str)
    if cpu_str.endswith("n"):
        return int(cpu_str[:-1]) / 1_000_000_000
    elif cpu_str.endswith("u"):
        return int(cpu_str[:-1]) / 1_000_000
    elif cpu_str.endswith("m"):
        return int(cpu_str[:-1]) / 1000
    else:
        return float(cpu_str)

def parse_mem(mem_str):
    mem_str = mem_str.lower()
    if mem_str.endswith("ki"):
        return int(mem_str[:-2]) / 1024
    elif mem_str.endswith("mi"):
        return float(mem_str[:-2])
    elif mem_str.endswith("gi"):
        return float(mem_str[:-2]) * 1024
    elif mem_str.endswith("ti"):
        return float(mem_str[:-2]) * 1024**2
    else:
        return int(mem_str) / (1024**2)

def get_total_commited_resources(items):
    total_cpu_cores = 0
    total_mem_mib = 0
    for item in items:
        replicas = item.spec.replicas or 1
        for container in item.spec.template.spec.containers:
            res = container.resources.requests or {}
            cpu = res.get("cpu")
            mem = res.get("memory")
            if cpu:
                total_cpu_cores += parse_cpu(cpu) * replicas
            if mem:
                total_mem_mib += parse_mem(mem) * replicas
    return total_cpu_cores, total_mem_mib