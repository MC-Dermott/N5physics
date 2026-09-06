import random
from utils.make_question import make_question
from utils.notes import NOTES

_CONTEXTS = ["trolley", "cyclist", "car", "runner", "go-kart", "toy car"]


def _dedup(options_data, correct):
    seen = {round(float(correct), 2)}
    cleaned = []
    for opt in options_data:
        key = round(float(opt["value"]), 2)
        if key not in seen:
            seen.add(key)
            cleaned.append(opt)
        elif opt["mistake"] is None:
            cleaned.insert(0, opt)
    if not any(opt["mistake"] is None for opt in cleaned):
        cleaned.insert(0, {"value": correct, "mistake": None, "working": []})
    return cleaned


def _segment_area(t0, v0, t1, v1):
    """Area under a straight-line segment from (t0,v0) to (t1,v1), as rectangle + triangle."""
    base = t1 - t0
    rect = base * min(v0, v1)
    tri = 0.5 * base * abs(v1 - v0)
    return rect + tri


# ── Section A — simple shapes (rectangle or triangle) ───────────────────────

def gen_vt_distance_simple(level="S3"):
    ctx = random.choice(_CONTEXTS)
    shape = random.choice(["rectangle", "triangle_up", "triangle_down"])
    t = random.choice([4, 5, 6, 7, 8])

    if shape == "rectangle":
        v = random.choice([6, 8, 9, 10, 12, 15])
        correct = v * t
        working = [
            {"type": "text", "content": f"Points: A(0, {v}), B({t}, {v}) — a rectangle."},
            {"type": "latex", "content": r"\text{distance} = \text{area} = \text{base} \times \text{height}"},
            {"type": "latex", "content": rf"\text{{distance}} = {t} \times {v}"},
            {"type": "latex", "content": rf"\text{{distance}} = {correct}\ \mathrm{{m}}"},
        ]
        question = (
            f"A speed-time graph for a {ctx} shows it travelling at a constant {v} m/s from A(0, {v}) "
            f"to B({t}, {v}).\n\nCalculate the distance travelled between A and B."
        )
        halved = round(correct / 2, 1)
        distractors = [
            {"value": halved,
             "mistake": "You halved the area as if this were a triangle — it's a rectangle (constant speed), "
                        "so distance = base × height, with no ½.",
             "working": working},
            {"value": t + v,
             "mistake": "You added the base and height instead of multiplying. distance = base × height.",
             "working": working},
        ]
    else:
        v_end = random.choice([12, 15, 16, 18, 20, 24])
        correct = round(0.5 * t * v_end, 1)
        if shape == "triangle_up":
            points = f"A(0, 0), B({t}, {v_end})"
            desc = f"speeding up from rest"
        else:
            points = f"A(0, {v_end}), B({t}, 0)"
            desc = f"slowing down to rest"
        working = [
            {"type": "text", "content": f"Points: {points} — a triangle."},
            {"type": "latex", "content": r"\text{distance} = \text{area} = \tfrac{1}{2} \times \text{base} \times \text{height}"},
            {"type": "latex", "content": rf"\text{{distance}} = \tfrac{{1}}{{2}} \times {t} \times {v_end}"},
            {"type": "latex", "content": rf"\text{{distance}} = {correct}\ \mathrm{{m}}"},
        ]
        question = (
            f"A speed-time graph for a {ctx} {desc} shows {points}.\n\n"
            f"Calculate the distance travelled between A and B."
        )
        doubled = round(t * v_end, 1)
        distractors = [
            {"value": doubled,
             "mistake": "You forgot the ½ — this is a triangle, not a rectangle, so "
                        "distance = ½ × base × height.",
             "working": working},
            {"value": round(t + v_end, 1),
             "mistake": "You added the base and height instead of using the triangle area formula.",
             "working": working},
        ]

    options_data = [{"value": correct, "mistake": None, "working": working}] + distractors
    options_data = _dedup(options_data, correct)
    return make_question(question, correct, options_data, "m", scaffold=None,
                         notes=NOTES["vt_graph_distance_s3"], topic="Dynamics",
                         question_type="V-T Graphs", level=level)


# ── Section B — trapezium shapes ─────────────────────────────────────────────

def gen_vt_distance_trapezium(level="S3"):
    ctx = random.choice(_CONTEXTS)
    t_start = random.choice([0, 0, 0, 2, 3, 4])
    duration = random.choice([5, 6, 7, 8, 9])
    t_end = t_start + duration
    v_lo = random.choice([4, 5, 6, 8, 10])
    v_hi = v_lo + random.choice([6, 8, 9, 10, 12])
    speeding_up = random.choice([True, False])
    v_start, v_end = (v_lo, v_hi) if speeding_up else (v_hi, v_lo)
    lower_v, higher_v = v_lo, v_hi

    rect = duration * lower_v
    tri = 0.5 * duration * (higher_v - lower_v)
    correct = rect + tri

    working = [
        {"type": "text", "content": f"Points: A({t_start}, {v_start}), B({t_end}, {v_end}) — a trapezium "
                                     f"(rectangle + triangle)."},
    ]
    if t_start != 0:
        working.append({"type": "text", "content": f"base (time interval) = {t_end} − {t_start} = {duration} s"})
    working += [
        {"type": "latex", "content": rf"\text{{Rectangle: base}} = {duration}, \text{{height}} = {lower_v} \Rightarrow {duration} \times {lower_v} = {rect}"},
        {"type": "latex", "content": rf"\text{{Triangle: base}} = {duration}, \text{{height}} = {higher_v} - {lower_v} \Rightarrow \tfrac{{1}}{{2}} \times {duration} \times {higher_v - lower_v} = {tri}"},
        {"type": "latex", "content": rf"\text{{distance}} = {rect} + {tri} = {correct}\ \mathrm{{m}}"},
    ]

    question = (
        f"A speed-time graph for a {ctx} shows A({t_start}, {v_start}), B({t_end}, {v_end}).\n\n"
        f"Calculate the distance travelled between A and B."
    )

    wrong_base = round(t_end * lower_v + 0.5 * t_end * (higher_v - lower_v), 1) if t_start != 0 else None
    rect_only = rect
    tri_only = tri

    distractors = [
        {"value": rect_only,
         "mistake": "That's only the rectangle part of the shape — don't forget to add the triangle on top.",
         "working": working},
        {"value": tri_only,
         "mistake": "That's only the triangle part of the shape — don't forget to add the rectangle "
                    "underneath it.",
         "working": working},
    ]
    if wrong_base is not None:
        distractors.append({
            "value": wrong_base,
            "mistake": f"You used t = {t_end} as the base instead of the time interval "
                       f"({t_end} − {t_start} = {duration} s). The graph doesn't start at t = 0 here.",
            "working": working,
        })

    options_data = [{"value": correct, "mistake": None, "working": working}] + distractors
    options_data = _dedup(options_data, correct)
    scaffold = [
        {"question": "What is the area of the rectangle part?", "answer": float(rect)},
        {"question": "What is the area of the triangle part?", "answer": float(tri)},
        {"question": "What is the total distance travelled?", "answer": float(correct)},
    ]
    return make_question(question, correct, options_data, "m", scaffold=scaffold,
                         notes=NOTES["vt_graph_distance_s3"], topic="Dynamics",
                         question_type="V-T Graphs", level=level)


# ── Section C — compound (multi-segment) graphs ──────────────────────────────

def gen_vt_distance_compound(level="S3"):
    ctx = random.choice(_CONTEXTS)
    pattern = random.choice(["up_down", "up_flat_up", "up_flat_down"])

    t1 = random.choice([3, 4, 5])
    v1 = random.choice([12, 16, 18, 20, 24])

    if pattern == "up_down":
        t2 = t1 + random.choice([4, 5, 6])
        points = [(0, 0, "A"), (t1, v1, "B"), (t2, 0, "C")]
        labels = ["A to B", "B to C"]
    elif pattern == "up_flat_up":
        flat_dur = random.choice([3, 4, 5])
        t2 = t1 + flat_dur
        rise2 = random.choice([6, 8, 10])
        rise2_dur = random.choice([3, 4, 5])
        t3 = t2 + rise2_dur
        v3 = v1 + rise2
        points = [(0, 0, "A"), (t1, v1, "B"), (t2, v1, "C"), (t3, v3, "D")]
        labels = ["A to B", "B to C", "C to D"]
    else:  # up_flat_down
        flat_dur = random.choice([3, 4, 5])
        t2 = t1 + flat_dur
        fall_dur = random.choice([3, 4, 5])
        t3 = t2 + fall_dur
        points = [(0, 0, "A"), (t1, v1, "B"), (t2, v1, "C"), (t3, 0, "D")]
        labels = ["A to B", "B to C", "C to D"]

    areas = []
    for i in range(len(points) - 1):
        t0, v0, _ = points[i]
        tt1, vv1, _ = points[i + 1]
        areas.append(_segment_area(t0, v0, tt1, vv1))
    total = sum(areas)

    points_desc = ", ".join(f"{lbl}({t}, {v})" for t, v, lbl in points)
    working = [{"type": "text", "content": f"Points: {points_desc}"}]
    for lbl, area in zip(labels, areas):
        working.append({"type": "latex", "content": rf"\text{{{lbl}}} = {area}\ \mathrm{{m}}"})
    working.append({"type": "latex", "content": rf"\text{{total distance}} = "
                                                  rf"{' + '.join(str(a) for a in areas)} = {total}\ \mathrm{{m}}"})

    question = (
        f"A speed-time graph for a {ctx} shows {points_desc}.\n\n"
        f"Calculate the total distance travelled from A to {points[-1][2]}."
    )

    partial = round(sum(areas[:-1]), 1)
    distractors = [
        {"value": partial,
         "mistake": f"That's the distance up to the second-to-last point only — the final section "
                    f"({labels[-1]}) still needs to be added.",
         "working": working},
        {"value": round(areas[0], 1),
         "mistake": f"That's only the first section ({labels[0]}) — add the distance for every section "
                    f"of the graph.",
         "working": working},
    ]
    options_data = [{"value": total, "mistake": None, "working": working}] + distractors
    options_data = _dedup(options_data, total)

    scaffold = [{"question": f"What is the distance for section {lbl}?", "answer": float(area)}
                for lbl, area in zip(labels, areas)]
    scaffold.append({"question": "What is the total distance travelled?", "answer": float(total)})

    return make_question(question, total, options_data, "m", scaffold=scaffold,
                         notes=NOTES["vt_graph_distance_s3"], topic="Dynamics",
                         question_type="V-T Graphs", level=level)


def generate_vt_graph_distance(level="S3"):
    return random.choice([gen_vt_distance_simple, gen_vt_distance_trapezium, gen_vt_distance_compound])(level=level)
