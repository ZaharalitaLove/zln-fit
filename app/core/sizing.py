import json
from dataclasses import dataclass
from pathlib import Path

@dataclass
class SizeResult:
    size: str | None
    confidence: str #high, low , out_of_range
    note: str|None = None

def load_chart(path)-> dict:
    return json.loads(Path(path).read_text())
def reccomended(width_mm:float, chart:dict)-> SizeResult:

    sizes = sorted(chart["sizes"], key= lambda s: s["width_mm"], reverse=True)
    tol = chart.get("boundary_tolerance_mm", 0.3)
    policy = chart.get("policy", "round_up")
    if policy not in ("round_up","nearest"):
        raise ValueError(f"Unknown policy: {policy}")

    if width_mm > sizes[0]["width_mm"] + tol or width_mm < sizes[-1]["width_mm"] - tol:
        return SizeResult(None, "out_of_range", "Outside the size chart. Try the sizing kit.")
    
    if policy == "nearest":
        idx = min(range(len(sizes)), key= lambda i: abs(sizes[i]["width_mm"]-width_mm))

        dif = abs(sizes[idx]["width_mm"]-width_mm)

        other_difs = [abs(s["width_mm"]- width_mm)for i,s in enumerate(sizes) if i != idx]

        ambiguous = bool(other_difs) and (min(other_difs)-dif)<=tol

    else: #policy = round up
        idx = next(((len(sizes)-1)-i for i,s in enumerate(reversed(sizes)) if s["width_mm"] >= width_mm),0)
        ambiguous = idx < len(sizes)-1 and width_mm -sizes[idx+1]["width_mm"] <=tol



    chosen_size = sizes[idx]["size"]
    if ambiguous:
        return SizeResult(chosen_size,"low","Close to another size. A sizing kit is reccomended for a more precise fit.")
    return SizeResult(chosen_size, "high")













        

