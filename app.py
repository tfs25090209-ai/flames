"""FLAMES Relationship Game — Single-file Streamlit App."""
import re
import streamlit as st

# -------------------------------------------------
# Page config
# -------------------------------------------------
st.set_page_config(
    page_title="FLAMES • Find Your Vibe",
    page_icon="🔥",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# -------------------------------------------------
# Data
# -------------------------------------------------
FLAMES_DATA = {
    "F": {
        "title": "Friends",
        "emoji": "🫂",
        "tagline": "Partners in crime & late-night laughs",
        "desc": "You vibe effortlessly. Trust, jokes and unbreakable loyalty — the foundation of everything good.",
        "gradient": "linear-gradient(135deg,#38bdf8,#818cf8)",
        "glow": "rgba(56,189,248,.55)",
    },
    "L": {
        "title": "Lovers",
        "emoji": "❤️‍🔥",
        "tagline": "Sparks are flying everywhere",
        "desc": "Magnetic chemistry! Hearts race, eyes linger — this is the stuff of movies and playlists.",
        "gradient": "linear-gradient(135deg,#fb7185,#f43f5e,#fb923c)",
        "glow": "rgba(251,113,133,.6)",
    },
    "A": {
        "title": "Affection",
        "emoji": "🥰",
        "tagline": "Warm, fuzzy & full of care",
        "desc": "A tender bond with genuine warmth. You care deeply, protect softly and smile easily together.",
        "gradient": "linear-gradient(135deg,#f9a8d4,#c084fc)",
        "glow": "rgba(240,171,252,.55)",
    },
    "M": {
        "title": "Marriage",
        "emoji": "💍",
        "tagline": "Forever looks good on you two",
        "desc": "Wedding bells! Deep commitment, shared dreams and a future built side-by-side.",
        "gradient": "linear-gradient(135deg,#fbbf24,#f59e0b,#f43f5e)",
        "glow": "rgba(251,191,36,.6)",
    },
    "E": {
        "title": "Enemies",
        "emoji": "⚔️",
        "tagline": "Uh oh… rivalry mode activated",
        "desc": "Fiery clash! You challenge each other — but even great rivals secretly respect one another.",
        "gradient": "linear-gradient(135deg,#64748b,#1e293b,#ef4444)",
        "glow": "rgba(239,68,68,.55)",
    },
    "S": {
        "title": "Siblings",
        "emoji": "👯",
        "tagline": "Same weird energy, different story",
        "desc": "Playful, protective and effortlessly familiar — like family you actually choose to hang with.",
        "gradient": "linear-gradient(135deg,#34d399,#22d3ee)",
        "glow": "rgba(52,211,153,.55)",
    },
}
ORDER = ["F", "L", "A", "M", "E", "S"]

# -------------------------------------------------
# Core algorithm
# -------------------------------------------------
def sanitize(name: str) -> str:
    return re.sub(r"\s+", "", name).lower()


def flames_engine(name1: str, name2: str):
    """Traditional FLAMES logic. Returns (winner, count, elimination_order, left1, left2)."""
    s1 = list(sanitize(name1))
    s2 = list(sanitize(name2))

    # Remove common characters (one-to-one, case-insensitive already lowered)
    i = 0
    while i < len(s1):
        ch = s1[i]
        if ch in s2:
            s2.remove(ch)
            s1.pop(i)
        else:
            i += 1

    count = len(s1) + len(s2)

    # Edge: identical names -> count 0. Celebrate as Friends soul-match.
    if count == 0:
        return "F", 0, ["L", "A", "M", "E", "S"], [], []

    flames = ORDER.copy()
    elimination = []
    idx = 0
    while len(flames) > 1:
        idx = (idx + count - 1) % len(flames)
        elimination.append(flames.pop(idx))

    return flames[0], count, elimination, s1, s2


def validate_inputs(raw1: str, raw2: str):
    n1 = raw1.strip()
    n2 = raw2.strip()
    if not n1 or not n2:
        return False, "Both names are required — don't leave destiny hanging! ✍️"
    if len(n1) < 2 or len(n2) < 2:
        return False, "Each name needs at least 2 letters to spark the flames. 🔤"
    pattern = re.compile(r"^[A-Za-z ]+$")
    if not pattern.match(n1) or not pattern.match(n2):
        return False, "Only letters A–Z and spaces allowed — no numbers, emojis or special characters. 🚫"
    if len(n1) > 30 or len(n2) > 30:
        return False, "Keep each name under 30 characters for best vibes. ✂️"
    return True, ""


# -------------------------------------------------
# Global CSS + HTML helpers
# -------------------------------------------------
GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Clash+Display:wght@600;700&display=swap');

.stApp {
  background:
    radial-gradient(900px 500px at 15% 5%, rgba(168,85,247,.28), transparent 60%),
    radial-gradient(800px 500px at 85% 10%, rgba(56,189,248,.22), transparent 60%),
    radial-gradient(900px 600px at 50% 100%, rgba(244,114,182,.18), transparent 60%),
    linear-gradient(180deg, #0b0817 0%, #141026 45%, #1b1440 100%);
  color: #f1efff;
  font-family: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
}
[data-testid="stHeader"], [data-testid="stToolbar"], footer { visibility: hidden; }
[data-testid="stAppViewContainer"] > .main { padding-top: 1rem; }
.block-container { max-width: 760px !important; padding-top: 1.2rem !important; }

/* ---------- HERO ---------- */
.hero {
  text-align: center;
  padding: 28px 20px 18px;
  border-radius: 28px;
  background: rgba(255,255,255,.055);
  border: 1px solid rgba(255,255,255,.12);
  backdrop-filter: blur(18px);
  -webkit-backdrop-filter: blur(18px);
  box-shadow: 0 20px 60px rgba(0,0,0,.45), inset 0 1px 0 rgba(255,255,255,.15);
  position: relative;
  overflow: hidden;
}
.hero::before {
  content:"";
  position:absolute; inset:-40%;
  background: conic-gradient(from 0deg, transparent 0 70%, rgba(251,113,133,.18), rgba(56,189,248,.18), transparent);
  animation: spinGlow 9s linear infinite;
  pointer-events:none;
}
@keyframes spinGlow { to { transform: rotate(360deg); } }
.hero-inner { position: relative; z-index: 2; }
.flames-badge {
  display:inline-flex; align-items:center; gap:8px;
  font-size:12px; font-weight:800; letter-spacing:.18em;
  padding:8px 16px; border-radius:999px;
  background: linear-gradient(135deg, #ff6a88, #ff9a44);
  color:#1a0b12; text-transform:uppercase;
  box-shadow: 0 8px 24px rgba(255,106,136,.45);
  animation: floatY 3.2s ease-in-out infinite;
}
@keyframes floatY { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-5px)} }
.hero h1 {
  font-size: clamp(2.4rem, 6vw, 3.6rem);
  font-weight: 800; line-height:1.02; margin:14px 0 8px;
  background: linear-gradient(90deg,#fff,#fbcfe8,#a5f3fc,#fff);
  background-size: 200% auto;
  -webkit-background-clip:text; background-clip:text; color:transparent;
  animation: shine 5s linear infinite;
}
@keyframes shine { to { background-position: 200% center; } }
.hero p { color:#c4bce6; margin:0; font-size:1.02rem; }

/* ---------- INPUTS ---------- */
[data-testid="stTextInput"] label {
  color:#e9e4ff !important; font-weight:700 !important; font-size:.9rem !important;
  letter-spacing:.02em;
}
[data-testid="stTextInput"] input {
  background: rgba(255,255,255,.07) !important;
  border: 1.5px solid rgba(255,255,255,.16) !important;
  border-radius: 16px !important;
  color: #fff !important;
  padding: 14px 16px !important;
  font-size: 1.02rem !important;
  font-weight: 600 !important;
  caret-color: #f0abfc !important;
  transition: border-color .25s ease, box-shadow .25s ease, transform .25s ease, background .25s ease !important;
}
[data-testid="stTextInput"] input::placeholder { color: rgba(255,255,255,.38) !important; }
[data-testid="stTextInput"] input:hover {
  border-color: rgba(240,171,252,.55) !important;
  background: rgba(255,255,255,.09) !important;
}
[data-testid="stTextInput"] input:focus {
  outline: none !important;
  border-color: #f0abfc !important;
  background: rgba(255,255,255,.11) !important;
  box-shadow: 0 0 0 4px rgba(240,171,252,.22), 0 0 28px rgba(168,85,247,.45) !important;
  transform: translateY(-1px);
}
/* name chips under inputs */
.chip-row { display:flex; gap:8px; flex-wrap:wrap; margin:.35rem 0 0; }
.chip {
  font-size:.78rem; font-weight:700; padding:6px 12px; border-radius:999px;
  background:rgba(255,255,255,.08); border:1px solid rgba(255,255,255,.14); color:#dcd4ff;
  cursor:pointer; transition: all .2s ease;
}
.chip:hover { background:rgba(240,171,252,.2); border-color:rgba(240,171,252,.6); transform:translateY(-1px); }

/* ---------- BUTTONS ---------- */
div[data-testid="stButton"] > button {
  width: 100%;
  border: none !important;
  border-radius: 18px !important;
  padding: 16px 22px !important;
  font-weight: 800 !important;
  font-size: 1.08rem !important;
  letter-spacing:.02em;
  color: #1a0b18 !important;
  background: linear-gradient(135deg, #f0abfc 0%, #fb7185 50%, #fb923c 100%) !important;
  box-shadow: 0 12px 32px rgba(251,113,133,.38), inset 0 1px 0 rgba(255,255,255,.6) !important;
  transition: transform .22s cubic-bezier(.34,1.56,.64,1), box-shadow .22s ease, filter .22s ease !important;
  position: relative; overflow:hidden;
}
div[data-testid="stButton"] > button::after {
  content:""; position:absolute; top:0; left:-70%; width:45%; height:100%;
  background: linear-gradient(105deg, transparent, rgba(255,255,255,.65), transparent);
  transform: skewX(-20deg);
  transition: left .6s ease;
}
div[data-testid="stButton"] > button:hover {
  transform: scale(1.035) translateY(-1px) !important;
  box-shadow: 0 18px 44px rgba(251,113,133,.55), 0 0 0 4px rgba(240,171,252,.22), inset 0 1px 0 rgba(255,255,255,.7) !important;
  filter: saturate(1.12) !important;
}
div[data-testid="stButton"] > button:hover::after { left: 130%; }
div[data-testid="stButton"] > button:active {
  transform: scale(.97) translateY(1px) !important;
  box-shadow: 0 6px 16px rgba(251,113,133,.32), inset 0 2px 8px rgba(0,0,0,.22) !important;
}
div[data-testid="stButton"] > button:focus:not(:active) {
  box-shadow: 0 12px 32px rgba(251,113,133,.38), 0 0 0 5px rgba(240,171,252,.3) !important;
}
.secondary-btn div[data-testid="stButton"] > button, .secondary-btn button {
  background: rgba(255,255,255,.08) !important;
  color:#e9e4ff !important;
  border:1px solid rgba(255,255,255,.16) !important;
  box-shadow:none !important;
  font-size:.92rem !important; padding:11px 16px !important;
}

/* ---------- ERROR ---------- */
.error-card {
  margin-top:16px; padding:14px 16px; border-radius:16px;
  background: linear-gradient(135deg, rgba(239,68,68,.18), rgba(239,68,68,.08));
  border:1px solid rgba(248,113,113,.45);
  color:#fecaca; font-weight:600; font-size:.94rem;
  display:flex; gap:10px; align-items:center;
  animation: riseIn .45s cubic-bezier(.22,1,.36,1) both, shake .45s ease .15s;
  box-shadow: 0 10px 30px rgba(239,68,68,.18);
}
@keyframes shake { 0%,100%{transform:translateX(0)} 25%{transform:translateX(-6px)} 50%{transform:translateX(6px)} 75%{transform:translateX(-3px)} }

/* ---------- RESULT CARD ---------- */
.flames-result-card {
  margin-top: 22px;
  border-radius: 26px;
  padding: 28px 24px 24px;
  text-align:center;
  background: rgba(255,255,255,.07);
  border:1px solid rgba(255,255,255,.14);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  box-shadow: 0 24px 70px rgba(0,0,0,.5), inset 0 1px 0 rgba(255,255,255,.18);
  position:relative; overflow:hidden;
  animation: riseIn .75s cubic-bezier(.22,1,.36,1) both;
}
@keyframes riseIn {
  from { opacity:0; transform: translateY(46px) scale(.96); filter: blur(6px); }
  to { opacity:1; transform: translateY(0) scale(1); filter: blur(0); }
}
.flames-result-card::before {
  content:""; position:absolute; inset:0 0 auto 0; height:120px;
  background: var(--winner-grad);
  opacity:.32; filter: blur(10px);
  mask-image: linear-gradient(to bottom, black, transparent);
  pointer-events:none;
}
.count-pill {
  display:inline-flex; align-items:center; gap:8px;
  font-size:.8rem; font-weight:800; letter-spacing:.08em; text-transform:uppercase;
  color:#0f0b1e; background:#fff; border-radius:999px; padding:7px 14px;
  box-shadow:0 8px 20px rgba(0,0,0,.25);
}
.result-emoji {
  font-size: 86px; line-height:1; display:inline-block; margin:14px 0 4px;
  filter: drop-shadow(0 12px 28px var(--winner-glow));
  animation: rockPulse 2.4s ease-in-out infinite;
  transform-origin: 50% 60%;
}
@keyframes rockPulse {
  0%,100% { transform: rotate(-9deg) scale(1); }
  25% { transform: rotate(6deg) scale(1.08); }
  50% { transform: rotate(-4deg) scale(1.12); }
  75% { transform: rotate(8deg) scale(1.06); }
}
.result-title {
  font-size: clamp(2rem,6vw,2.9rem); font-weight:800; margin:6px 0 2px;
  background: var(--winner-grad);
  -webkit-background-clip:text; background-clip:text; color:transparent;
  letter-spacing:-.02em;
}
.result-tag { color:#fff; font-weight:700; font-size:1.04rem; margin:2px 0 8px; }
.result-desc { color:#c9c2ea; font-size:.96rem; line-height:1.6; max-width:520px; margin:0 auto; }
.names-line { margin-top:12px; color:#e9e4ff; font-weight:700; }
.names-line span.hl {
  background:rgba(255,255,255,.12); border:1px solid rgba(255,255,255,.18);
  padding:4px 12px; border-radius:999px; margin:0 4px; display:inline-block;
}

/* ---------- FLAMES STRIP ---------- */
.flames-strip {
  display:flex; gap:10px; justify-content:center; align-items:stretch;
  margin:18px 0 6px; flex-wrap:wrap;
}
.flame-letter {
  width:64px; height:74px; border-radius:18px;
  display:flex; flex-direction:column; align-items:center; justify-content:center;
  font-weight:800; background:rgba(255,255,255,.06);
  border:1px solid rgba(255,255,255,.12); color:#fff;
  transition: all .3s ease;
  animation: letterIn .6s cubic-bezier(.22,1,.36,1) both;
}
.flame-letter small { font-size:.62rem; letter-spacing:.12em; opacity:.75; font-weight:700; }
.flame-letter b { font-size:1.55rem; line-height:1; }
.flame-letter.eliminated {
  opacity:.32; filter:grayscale(1) brightness(.7); transform:scale(.94);
  text-decoration: line-through; text-decoration-thickness:2px;
}
.flame-letter.winner {
  background: var(--winner-grad);
  color:#14091a; border-color:transparent;
  transform: scale(1.14);
  box-shadow: 0 12px 34px var(--winner-glow), 0 0 0 3px rgba(255,255,255,.55);
  animation: letterIn .6s cubic-bezier(.22,1,.36,1) both, winnerPulse 1.9s ease-in-out .7s infinite;
}
@keyframes letterIn { from{opacity:0; transform:translateY(18px) scale(.9)} to{opacity:1; transform:translateY(0) scale(1)} }
@keyframes winnerPulse {
  0%,100% { transform: scale(1.14); box-shadow: 0 12px 34px var(--winner-glow), 0 0 0 3px rgba(255,255,255,.55); }
  50% { transform: scale(1.22); box-shadow: 0 18px 48px var(--winner-glow), 0 0 0 6px rgba(255,255,255,.35), 0 0 32px var(--winner-glow); }
}

/* ---------- ELIMINATION TIMELINE ---------- */
.timeline {
  display:flex; gap:8px; justify-content:center; flex-wrap:wrap; margin-top:14px;
}
.step {
  font-size:.76rem; font-weight:800; letter-spacing:.06em;
  padding:7px 12px; border-radius:999px;
  background:rgba(255,255,255,.08); border:1px solid rgba(255,255,255,.14); color:#d8d1ff;
  animation: letterIn .5s ease both;
}
.step.out { opacity:.55; text-decoration:line-through; }
.step.final { background:#fff; color:#111; border-color:#fff; }

/* meter */
.meter-wrap { max-width:440px; margin:16px auto 0; text-align:left; }
.meter-label { display:flex; justify-content:space-between; font-size:.8rem; font-weight:800; color:#d8d1ff; margin-bottom:8px; letter-spacing:.06em; }
.meter { height:12px; border-radius:999px; background:rgba(255,255,255,.12); overflow:hidden; border:1px solid rgba(255,255,255,.14); }
.meter > div {
  height:100%; border-radius:999px; background: var(--winner-grad);
  box-shadow:0 0 18px var(--winner-glow);
  animation: fillBar 1.2s cubic-bezier(.22,1,.36,1) .3s both;
}
@keyframes fillBar { from{width:0 !important} }

/* history */
.hist-card {
  background:rgba(255,255,255,.06); border:1px solid rgba(255,255,255,.12);
  border-radius:16px; padding:12px 14px; margin-top:10px;
  display:flex; align-items:center; justify-content:space-between; gap:10px;
  animation: riseIn .5s ease both;
  font-size:.9rem;
}
.hist-card b { color:#fff; }
.footer { text-align:center; color:rgba(255,255,255,.45); font-size:.8rem; margin:26px 0 10px; }

/* floating hearts */
.float-layer { position:fixed; inset:0; pointer-events:none; overflow:hidden; z-index:0; }
.float-layer span { position:absolute; bottom:-40px; opacity:.5; animation: floatUp linear infinite; filter:blur(.2px); }
@keyframes floatUp { to { transform: translateY(-110vh) rotate(20deg); opacity:0; } }

@media (max-width:560px){
  .flame-letter{ width:52px; height:64px; border-radius:14px; }
  .result-emoji{ font-size:70px; }
}
</style>
"""

st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

# Floating background emojis (pure CSS animation)
st.markdown(
    """
<div class="float-layer">
  <span style="left:6%; font-size:22px; animation-duration:11s;">💖</span>
  <span style="left:18%; font-size:16px; animation-duration:14s; animation-delay:1s;">✨</span>
  <span style="left:32%; font-size:20px; animation-duration:12s; animation-delay:.5s;">💍</span>
  <span style="left:48%; font-size:14px; animation-duration:15s; animation-delay:2s;">💜</span>
  <span style="left:63%; font-size:22px; animation-duration:10s; animation-delay:.8s;">🔥</span>
  <span style="left:76%; font-size:16px; animation-duration:13s; animation-delay:1.4s;">🥰</span>
  <span style="left:88%; font-size:20px; animation-duration:12s; animation-delay:.2s;">✨</span>
</div>
""",
    unsafe_allow_html=True,
)

# -------------------------------------------------
# Hero
# -------------------------------------------------
st.markdown(
    """
<div class="hero"><div class="hero-inner">
  <div class="flames-badge">🔥 Classic playground game • Remastered</div>
  <h1>FLAMES</h1>
  <p>Enter two names. Let the letters decide — <b style="color:#fff">Friends, Lovers, Affection, Marriage, Enemies</b> or <b style="color:#fff">Siblings</b>?</p>
</div></div>
""",
    unsafe_allow_html=True,
)

# -------------------------------------------------
# Inputs
# -------------------------------------------------
if "history" not in st.session_state:
    st.session_state.history = []
if "n1" not in st.session_state:
    st.session_state.n1 = ""
if "n2" not in st.session_state:
    st.session_state.n2 = ""

col1, col2 = st.columns(2, gap="medium")
with col1:
    name1 = st.text_input("Your name ✨", value=st.session_state.n1, placeholder="e.g. Alex", key="in1", max_chars=30)
with col2:
    name2 = st.text_input("Their name 💘", value=st.session_state.n2, placeholder="e.g. Sam", key="in2", max_chars=30)

st.markdown(
    """<div class="chip-row" style="margin-bottom:6px;">
      <span style="font-size:.78rem;color:#b9b0e6;font-weight:700;align-self:center;">Try:</span>
    </div>""",
    unsafe_allow_html=True,
)
c1, c2, c3, c4 = st.columns(4)
if c1.button("Romeo ♥ Juliet", key="s1"):
    st.session_state.in1 = "Romeo"
    st.session_state.in2 = "Juliet"
    st.rerun()
if c2.button("Harry ⚡ Ginny", key="s2"):
    st.session_state.in1 = "Harry Potter"
    st.session_state.in2 = "Ginny Weasley"
    st.rerun()
if c3.button("Tom & Jerry", key="s3"):
    st.session_state.in1 = "Tom"
    st.session_state.in2 = "Jerry"
    st.rerun()
if c4.button("Ava × Liam", key="s4"):
    st.session_state.in1 = "Ava"
    st.session_state.in2 = "Liam"
    st.rerun()
st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

calc = st.button("🔥  Calculate FLAMES  ✨", key="calc", use_container_width=True)

# -------------------------------------------------
# Result handling
# -------------------------------------------------
def render_error(msg: str):
    st.markdown(f"""<div class="error-card"><span style="font-size:1.3rem;">⚠️</span><span>{msg}</span></div>""", unsafe_allow_html=True)


def render_result(n1: str, n2: str, winner: str, count: int, elimination: list):
    info = FLAMES_DATA[winner]
    # FLAMES strip with staggered delays
    letters_html = ""
    for idx, L in enumerate(ORDER):
        cls = "winner" if L == winner else "eliminated"
        delay = idx * 0.12
        sub = FLAMES_DATA[L]["title"]
        mark = "★" if L == winner else "✕" if L in elimination else "•"
        letters_html += (
            f"""<div class="flame-letter {cls}" style="animation-delay:{delay}s,.{delay}s; --winner-grad:{info['gradient']}; --winner-glow:{info['glow']}">"""
            f"""<b>{L}</b><small>{sub[:4].upper()} {mark}</small></div>"""
        )

    # elimination timeline
    steps_html = ""
    for i, L in enumerate(elimination):
        steps_html += f"""<span class="step out" style="animation-delay:{0.5 + i*0.15}s">{i+1}. {L} eliminated</span>"""
    steps_html += f"""<span class="step final" style="animation-delay:{0.5 + len(elimination)*0.15}s">👑 {winner} wins</span>"""

    # fun vibe meter (deterministic from count + name lengths)
    vibe = 42 + ((count * 13 + len(n1) * 7 + len(n2) * 11) % 57)  # 42–98
    if winner in ("L", "M"):
        vibe = max(vibe, 86)
    if winner == "E":
        vibe = min(vibe, 48)

    st.markdown(
        f"""
<div class="flames-result-card" style="--winner-grad:{info['gradient']}; --winner-glow:{info['glow']};">
  <span class="count-pill">🔢 Unmatched letters: {count} &nbsp;•&nbsp; {n1.strip().title()} ♥ {n2.strip().title()}</span>
  <div><span class="result-emoji">{info['emoji']}</span></div>
  <div class="result-title">{info['title']}!</div>
  <div class="result-tag">{info['tagline']}</div>
  <div class="result-desc">{info['desc']}</div>
  <div class="flames-strip">{letters_html}</div>
  <div class="timeline">{steps_html}</div>
  <div class="meter-wrap">
    <div class="meter-label"><span>VIBE METER</span><span>{vibe}%</span></div>
    <div class="meter"><div style="width:{vibe}%"></div></div>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )


if calc:
    ok, msg = validate_inputs(name1, name2)
    if not ok:
        render_error(msg)
    else:
        winner, count, elimination, _, _ = flames_engine(name1, name2)
        render_result(name1, name2, winner, count, elimination)
        # save history
        st.session_state.history.insert(
            0, {"a": name1.strip(), "b": name2.strip(), "r": FLAMES_DATA[winner]["title"], "e": FLAMES_DATA[winner]["emoji"]}
        )
        st.session_state.history = st.session_state.history[:6]
        # celebratory micro-interaction
        if winner in ("L", "M", "A"):
            try:
                st.balloons()
            except Exception:
                pass
        elif winner == "F":
            try:
                st.toast(f"🫂 {name1.strip()} & {name2.strip()} — {FLAMES_DATA[winner]['title']}!", icon="🔥")
            except Exception:
                pass

# -------------------------------------------------
# How it works + history
# -------------------------------------------------
with st.expander("🧮 How FLAMES works"):
    st.markdown(
        """
1. Lowercase both names and **remove spaces**.
2. **Cancel out common letters** one-for-one (e.g. the two `a`s in *Alex* & *Sam*… you get the idea).
3. **Count** the leftover letters → say `N`.
4. Write `F-L-A-M-E-S` in a circle and **count N circularly**, striking off one letter at a time until a single letter survives.
5. Map it: **F**riends • **L**overs • **A**ffection • **M**arriage • **E**nemies • **S**iblings.
"""
    )

if st.session_state.history:
    st.markdown("### 🕘 Recent flames", unsafe_allow_html=True)
    for h in st.session_state.history:
        st.markdown(
            f"""<div class="hist-card"><span><b>{h['a']}</b> ♥ <b>{h['b']}</b></span><span style="font-weight:800;">{h['e']} {h['r']}</span></div>""",
            unsafe_allow_html=True,
        )
    st.markdown('<div class="secondary-btn">', unsafe_allow_html=True)
    if st.button("Clear history 🧹", key="clear"):
        st.session_state.history = []
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='footer'>Made with 🔥 in Streamlit • One file • Zero backend • All vibes</div>", unsafe_allow_html=True)
