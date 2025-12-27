import simpy, random, numpy as np
from dataclasses import dataclass
from typing import Optional

SIM_DURATION = 30 * 24 * 60
SERVICE_LEVEL_THRESHOLD = 30

@dataclass
class Patient:
    id: int
    arrival_time: float
    acuity_level: str
    bed_request_time: Optional[float] = None
    bed_assigned_time: Optional[float] = None
    disposition: Optional[str] = None

def run_simulation(med_surg_beds=160, stepdown_beds=6, triage_mean=5):
    random.seed(42)
    np.random.seed(42)

    env = simpy.Environment()
    med_surg = simpy.Resource(env, capacity=med_surg_beds)
    stepdown = simpy.Resource(env, capacity=stepdown_beds)

    patients = []
    pid = 0

    def arrival():
        nonlocal pid
        while True:
            yield env.timeout(random.expovariate(1/10))
            pid += 1
            p = Patient(pid, env.now, "medium")
            patients.append(p)
            env.process(flow(p))

    def flow(p):
        yield env.timeout(random.expovariate(1/triage_mean))
        p.disposition = random.choice(["med_surg", "stepdown"])
        p.bed_request_time = env.now
        bed = med_surg if p.disposition == "med_surg" else stepdown
        with bed.request() as req:
            yield req
            p.bed_assigned_time = env.now
            yield env.timeout(random.expovariate(1/(2*24*60)))

    env.process(arrival())
    env.run(until=SIM_DURATION)

    waits = [p.bed_assigned_time - p.bed_request_time for p in patients if p.bed_assigned_time]
    avg_wait = float(np.mean(waits)) if waits else 0.0
    service_level = float(np.mean([w <= SERVICE_LEVEL_THRESHOLD for w in waits]) * 100) if waits else 0.0

    return avg_wait, service_level

