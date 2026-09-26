"""Interactive answer fields reproducing the Moodle quiz behaviour (Check / Try again, hints, feedback).

Usage in a notebook (the cells calling these functions are collapsed):

    from quiz_widgets import load, question
    load("quiz_data.json")
    question(1)
"""
import base64
import json
import mimetypes
import os
import re
import uuid

import ipywidgets as widgets
from IPython.display import HTML, display

_QUIZ = {}
_DIR = "."
_ALIVE = []  # keep references to the widgets of every question

_RED, _GREEN, _ORANGE, _GREY = "#c62828", "#1a7f37", "#b35900", "#555555"
_BOX = ("background:#fcefdc;border-radius:4px;padding:8px 12px;margin-top:6px;"
        "color:#333;line-height:1.45")


def load(path="quiz_data.json"):
    """Load the questions, answer keys and Moodle feedback of the quiz."""
    global _QUIZ, _DIR
    with open(path, encoding="utf-8") as f:
        _QUIZ = json.load(f)
    _DIR = os.path.dirname(os.path.abspath(path))


def _decode(q):
    return json.loads(base64.b64decode(q["fb"]).decode("utf-8"))


def _inline_images(html):
    """Replace local image paths by data URIs so that the images show inside the notebook output."""
    def repl(m):
        path = os.path.join(_DIR, m.group(1))
        if not os.path.exists(path):
            return m.group(0)
        mime = mimetypes.guess_type(path)[0] or "image/png"
        with open(path, "rb") as f:
            data = base64.b64encode(f.read()).decode("ascii")
        return f'src="data:{mime};base64,{data}"'
    return re.sub(r'src="([^":]+)"', repl, html or "")


def question(n):
    """Display the answer area of question n."""
    if not _QUIZ:
        load()
    q = _QUIZ["questions"][str(n)]
    fb = _decode(q)
    {"single": _Choice, "multi": _Choice, "input": _Input, "marker": _Marker}[q["type"]](q, fb)


# --------------------------------------------------------------------------- common Moodle flow

class _Flow:
    """Check / Try again cycle with a limited number of tries, like Moodle's interactive behaviour."""

    def __init__(self, q, fb, answer_rows):
        self.q, self.fb = q, fb
        self.tries = max(1, int(fb.get("tries", 1)))
        self.used = 0
        self.mode = "check"
        self.button = widgets.Button(description="Check", button_style="primary",
                                     layout=widgets.Layout(width="110px", margin="8px 0 0 0"))
        self.button.on_click(self._click)
        self.info = widgets.HTML(self._tries_text())
        self.out = widgets.HTMLMath(layout=widgets.Layout(width="100%"))
        box = widgets.VBox(answer_rows + [widgets.HBox([self.button, self.info],
                                                      layout=widgets.Layout(align_items="center")),
                                          self.out],
                           layout=widgets.Layout(width="98%", overflow="hidden"))
        _ALIVE.append(self)
        self.box = box
        display(box)

    def _tries_text(self):
        left = self.tries - self.used
        return f'<span style="color:{_GREY};margin-left:12px">Tries remaining: {left}</span>'

    # to be provided by subclasses
    def answered(self): return True
    def evaluate(self): return "incorrect"
    def show_details(self, state, final): pass
    def clear_details(self): pass
    def set_enabled(self, enabled): pass

    def _click(self, _b):
        if self.mode == "tryagain":
            self.mode = "check"
            self.button.description = "Check"
            self.out.value = ""
            self.clear_details()
            self.set_enabled(True)
            return
        if not self.answered():
            self.out.value = f'<div style="color:{_GREY};margin-top:4px">Please answer the question before checking.</div>'
            return
        state = self.evaluate()
        self.used += 1
        final = state == "correct" or self.used >= self.tries
        parts = []
        spec = self.fb.get("spec", {}).get(state)
        if spec:
            parts.append(spec)
        self.show_details(state, final)
        if not final:
            hints = self.fb.get("hints", [])
            if self.used - 1 < len(hints):
                parts.append(f'<div style="margin-top:6px">{hints[self.used - 1]}</div>')
            self.mode = "tryagain"
            self.button.description = "Try again"
        else:
            if self.fb.get("general"):
                parts.append(f'<div style="margin-top:6px">{self.fb["general"]}</div>')
            if self.fb.get("show_right") and self.fb.get("right"):
                parts.append(f'<div style="margin-top:6px">The correct answer is: {self.fb["right"]}</div>')
            self.button.layout.display = "none"
        self.set_enabled(False)
        self.info.value = self._tries_text() if not final else ""
        self.out.value = (f'<div style="{_BOX}">' + "".join(parts) + "</div>") if parts else ""
        self.out.value = _inline_images(self.out.value)


# --------------------------------------------------------------------------- choice questions

class _Choice(_Flow):
    def __init__(self, q, fb):
        self.single = q["type"] == "single"
        self.options = q["options"]
        self.boxes, self.notes, rows = [], [], []
        for opt in self.options:
            if self.single:
                w = widgets.RadioButtons(options=[""], value=None,
                                         layout=widgets.Layout(width="32px", flex="0 0 auto", margin="0"))
                w.observe(self._exclusive, names="value")
            else:
                w = widgets.Checkbox(value=False, indent=False,
                                     layout=widgets.Layout(width="28px", flex="0 0 auto"))
            note = widgets.HTMLMath(layout=widgets.Layout(margin="0 0 0 34px"))
            self.boxes.append(w)
            self.notes.append(note)
            rows.append(widgets.VBox([
                widgets.HBox([w, widgets.HTMLMath(value=opt, layout=widgets.Layout(flex="1 1 auto"))],
                             layout=widgets.Layout(align_items="center")),
                note]))
        super().__init__(q, fb, rows)

    def _exclusive(self, change):
        if change["new"] is not None:
            for other in self.boxes:
                if other is not change["owner"]:
                    other.value = None

    def _selected(self):
        if self.single:
            return {i for i, b in enumerate(self.boxes) if b.value is not None}
        return {i for i, b in enumerate(self.boxes) if b.value}

    def answered(self):
        return bool(self._selected())

    def evaluate(self):
        chosen, key = self._selected(), set(self.fb["key"])
        if chosen == key or (self.fb.get("extra_ok") and key <= chosen):
            return "correct"
        if not self.single and chosen & key:
            return "partial"
        if self.single and chosen & set(self.fb.get("partial", [])):
            return "partial"
        return "incorrect"

    def show_details(self, state, final):
        optfb = self.fb.get("optfb", {})
        for i in self._selected():
            text = optfb.get(str(i))
            if text:
                self.notes[i].value = f'<div style="color:{_GREY};font-style:italic">{text}</div>'

    def clear_details(self):
        for note in self.notes:
            note.value = ""

    def set_enabled(self, enabled):
        for b in self.boxes:
            b.disabled = not enabled


# --------------------------------------------------------------------------- fill-in blanks

def _to_float(text):
    try:
        return float(text.strip().replace(",", ".").replace(" ", ""))
    except ValueError:
        return None


class _Input(_Flow):
    def __init__(self, q, fb):
        choices = q.get("choices")
        self.fields, rows = [], []
        for row in q["rows"]:
            parts = row.split("___")
            items = []
            for i, part in enumerate(parts):
                if part.strip():
                    items.append(widgets.HTMLMath(value=part.strip(), layout=widgets.Layout(margin="0 6px 0 0")))
                if i < len(parts) - 1:
                    if choices:
                        w = widgets.Dropdown(options=[("Choose...", None)] + [(c, c) for c in choices], value=None,
                                             layout=widgets.Layout(width="max-content", margin="0 6px 0 0"))
                    else:
                        w = widgets.Text(layout=widgets.Layout(width="140px", margin="0 6px 0 0"))
                    mark = widgets.HTMLMath(layout=widgets.Layout(margin="0 10px 0 0"))
                    self.fields.append((w, mark))
                    items += [w, mark]
            rows.append(widgets.HBox(items, layout=widgets.Layout(align_items="center", flex_flow="row wrap")))
        super().__init__(q, fb, rows)

    def answered(self):
        return all(w.value not in (None, "") for w, _m in self.fields)

    def _ok(self):
        res = []
        for i, (w, _m) in enumerate(self.fields):
            k = self.fb["key"][i]
            if isinstance(k, dict):
                x = _to_float(w.value)
                res.append(x is not None and abs(x - k["value"]) <= k.get("tol", 0) + 1e-9 * max(1, abs(k["value"])))
            else:
                res.append(w.value == k)
        return res

    def evaluate(self):
        res = self._ok()
        if all(res):
            return "correct"
        if any(res) and len(res) > 1:
            return "partial"
        return "incorrect"

    def show_details(self, state, final):
        subfb = self.fb.get("subfb", [])
        for i, ((_w, mark), ok) in enumerate(zip(self.fields, self._ok())):
            sign = (f'<span style="color:{_GREEN}">&#10004;</span>' if ok
                    else f'<span style="color:{_RED}">&#10008;</span>')
            text = ""
            if final and i < len(subfb) and subfb[i]:
                text = subfb[i].get("correct" if ok else "incorrect") or ""
            mark.value = sign + (f' <span style="color:{_GREY};font-size:90%">{text}</span>' if text else "")

    def clear_details(self):
        for _w, mark in self.fields:
            mark.value = ""

    def set_enabled(self, enabled):
        for w, _m in self.fields:
            w.disabled = not enabled


# --------------------------------------------------------------------------- drag and drop markers

def grade_markers(zones, placed):
    """placed: list of (label, x, y) in image pixels. Returns (state, list of booleans per placed marker)."""
    used = [False] * len(placed)
    hit = 0
    for zone in zones:
        for i, (label, x, y) in enumerate(placed):
            if not used[i] and label == zone["label"] and any(
                    x0 <= x <= x1 and y0 <= y <= y1 for x0, y0, x1, y1 in zone["rects"]):
                used[i] = True
                hit += 1
                break
    wrong = used.count(False)
    if hit == len(zones) and wrong == 0:
        return "correct", used
    return ("partial" if hit else "incorrect"), used


class _Marker:
    """Draggable markers on the image with Check / Try again, hints and feedback (runs in the browser)."""

    def __init__(self, q, fb):
        with open(os.path.join(_DIR, q["image"]), "rb") as f:
            data = base64.b64encode(f.read()).decode("ascii")
        mime = mimetypes.guess_type(q["image"])[0] or "image/png"
        labels = []
        for label in q["markers"]:
            labels += [label] * q.get("count", 1)
        conf = {"labels": labels, "zones": fb.get("zones", []), "tries": int(fb.get("tries", 1)),
                "hints": fb.get("hints", []), "spec": fb.get("spec", {}),
                "general": _inline_images(fb.get("general") or "")}
        conf_js = json.dumps(conf).replace("</", "<\\/")
        uid = "qm" + uuid.uuid4().hex[:10]
        _ALIVE.append(self)
        display(HTML(f"""
<div id="{uid}" style="max-width:100%">
 <div class="area" style="position:relative;display:inline-block;max-width:100%;user-select:none;touch-action:none">
  <img src="data:{mime};base64,{data}" draggable="false" style="display:block;max-width:100%">
  <div class="home" style="display:flex;flex-wrap:wrap;gap:8px;padding:8px 0;min-height:30px"></div>
 </div>
 <div style="display:flex;align-items:center;gap:12px;margin-top:6px">
  <button class="check" style="background:#1976d2;color:white;border:none;border-radius:2px;padding:5px 22px;cursor:pointer">Check</button>
  <span class="tries" style="color:#555"></span>
 </div>
 <div class="out"></div>
</div>
<script>
(function() {{
  const C = {conf_js};
  const root = document.getElementById("{uid}");
  const area = root.querySelector(".area"), img = area.querySelector("img"), home = root.querySelector(".home");
  const btn = root.querySelector(".check"), tries = root.querySelector(".tries"), out = root.querySelector(".out");
  let used = 0, mode = "check", locked = false;
  const BOX = "{_BOX}";
  function showTries() {{ tries.textContent = "Tries remaining: " + (C.tries - used); }}
  showTries();
  const markers = C.labels.map(function(text) {{
    const m = document.createElement("div");
    m.label = text;
    m.innerHTML = '<span class="cross" style="color:#c62828;font-size:18px;line-height:14px">&#8853;</span> ' + text;
    m.style.cssText = "cursor:move;background:rgba(255,255,255,0.85);border:2px solid #888;border-radius:4px;" +
                      "padding:1px 5px;font:13px sans-serif;white-space:nowrap;z-index:10";
    home.appendChild(m);
    m.addEventListener("pointerdown", function(e) {{
      if (locked) return;
      e.preventDefault(); e.stopPropagation();
      const r = area.getBoundingClientRect(), mr = m.getBoundingClientRect();
      const dx = e.clientX - mr.left, dy = e.clientY - mr.top;
      m.style.position = "absolute";
      area.appendChild(m);
      function move(ev) {{ m.style.left = (ev.clientX - r.left - dx) + "px"; m.style.top = (ev.clientY - r.top - dy) + "px"; }}
      move(e);
      m.setPointerCapture(e.pointerId);
      m.onpointermove = move;
      m.onpointerup = function() {{ m.onpointermove = null; m.onpointerup = null; }};
    }});
    return m;
  }});
  function placed() {{
    const ir = img.getBoundingClientRect(), sx = img.naturalWidth / ir.width, sy = img.naturalHeight / ir.height;
    return markers.filter(m => m.style.position === "absolute").map(function(m) {{
      const c = m.querySelector(".cross").getBoundingClientRect();
      return {{m: m, x: (c.left + c.width / 2 - ir.left) * sx, y: (c.top + c.height / 2 - ir.top) * sy}};
    }}).filter(p => p.x >= 0 && p.y >= 0 && p.x <= img.naturalWidth && p.y <= img.naturalHeight);
  }}
  function grade(P) {{
    const ok = P.map(() => false); let hit = 0;
    C.zones.forEach(function(z) {{
      for (let i = 0; i < P.length; i++) {{
        if (!ok[i] && P[i].m.label === z.label && z.rects.some(r => P[i].x >= r[0] && P[i].x <= r[2] && P[i].y >= r[1] && P[i].y <= r[3])) {{ ok[i] = true; hit++; break; }}
      }}
    }});
    const wrong = ok.filter(v => !v).length;
    return {{state: (hit === C.zones.length && wrong === 0) ? "correct" : (hit ? "partial" : "incorrect"), ok: ok}};
  }}
  function typeset() {{ try {{ if (window.MathJax && MathJax.typesetPromise) MathJax.typesetPromise([out]); }} catch (e) {{}} }}
  btn.onclick = function() {{
    if (mode === "tryagain") {{
      mode = "check"; btn.textContent = "Check"; out.innerHTML = ""; locked = false;
      markers.forEach(m => m.style.borderColor = "#888");
      return;
    }}
    const P = placed();
    if (!P.length) {{ out.innerHTML = '<div style="color:#555;margin-top:4px">Please place the markers before checking.</div>'; return; }}
    const g = grade(P);
    used++;
    P.forEach((p, i) => p.m.style.borderColor = g.ok[i] ? "#1a7f37" : "#c62828");
    const final = g.state === "correct" || used >= C.tries;
    let html = C.spec[g.state] || "";
    if (!final) {{
      if (C.hints[used - 1]) html += '<div style="margin-top:6px">' + C.hints[used - 1] + "</div>";
      mode = "tryagain"; btn.textContent = "Try again"; showTries();
    }} else {{
      if (C.general) html += '<div style="margin-top:6px">' + C.general + "</div>";
      btn.style.display = "none"; tries.textContent = "";
    }}
    locked = true;
    out.innerHTML = '<div style="' + BOX + '">' + html + "</div>";
    typeset();
  }};
}})();
</script>
"""))


