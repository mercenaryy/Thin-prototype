"""
app.py — Streamlit Web UI for the Personal Intelligence AI
Run with: streamlit run app.py
"""
import time
print(f"APP LOADED AT: {time.time()}")
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from collections import Counter
import pandas as pd
import os
from dotenv import load_dotenv

# ── Page config (must be first Streamlit call) ────────────────────────────────
st.set_page_config(
    page_title="Personal Intelligence AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Load env + data ───────────────────────────────────────────────────────────
load_dotenv()
from data_loader import load_user_data, format_data_summary

DATA_FILE = "AI_model-_Raw_Data.xlsx"

@st.cache_data
def get_user_data():
    return load_user_data(DATA_FILE)

@st.cache_data
def get_data_summary():
    return format_data_summary(get_user_data())

user_data    = get_user_data()
data_summary = get_data_summary()

signals   = user_data["signals"]
loops     = user_data["loops"]
decisions = user_data["decisions"]
patterns  = user_data["patterns"]

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap');

/* Global */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: #1a1a2e;
}

/* Background */
.stApp {
    background: #f7f5f0;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #1a1a2e !important;
    color: #f7f5f0 !important;
}
[data-testid="stSidebar"] * {
    color: #f7f5f0 !important;
}
[data-testid="stSidebar"] .stRadio label {
    color: #f7f5f0 !important;
    font-size: 15px;
    padding: 6px 0;
}

/* Hero header */
.hero-title {
    font-family: 'DM Serif Display', serif;
    font-size: 2.8rem;
    color: #1a1a2e;
    line-height: 1.1;
    margin-bottom: 0.2rem;
}
.hero-sub {
    font-size: 1.05rem;
    color: #6b6b80;
    font-weight: 300;
    margin-bottom: 2rem;
}

/* Metric cards */
.metric-card {
    background: white;
    border-radius: 16px;
    padding: 20px 24px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    border-left: 4px solid #e8704a;
    margin-bottom: 12px;
}
.metric-card .metric-value {
    font-family: 'DM Serif Display', serif;
    font-size: 2.4rem;
    color: #1a1a2e;
    line-height: 1;
}
.metric-card .metric-label {
    font-size: 0.82rem;
    color: #9090a0;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-top: 4px;
}

/* Insight cards */
.insight-card {
    background: white;
    border-radius: 14px;
    padding: 18px 22px;
    margin-bottom: 12px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    border-top: 3px solid #4a90e8;
}
.insight-type {
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #4a90e8;
    font-weight: 600;
    margin-bottom: 6px;
}
.insight-text {
    font-size: 0.95rem;
    color: #2a2a3e;
    line-height: 1.5;
}
.insight-reflection {
    font-size: 0.85rem;
    color: #e8704a;
    font-style: italic;
    margin-top: 8px;
}

/* Chat */
.chat-container {
    background: white;
    border-radius: 20px;
    padding: 28px;
    box-shadow: 0 4px 24px rgba(0,0,0,0.07);
    min-height: 480px;
}
.chat-msg-user {
    background: #1a1a2e;
    color: white;
    padding: 12px 18px;
    border-radius: 18px 18px 4px 18px;
    margin: 8px 0 8px 60px;
    font-size: 0.95rem;
    line-height: 1.5;
}
.chat-msg-ai {
    background: #f0ede8;
    color: #1a1a2e;
    padding: 12px 18px;
    border-radius: 18px 18px 18px 4px;
    margin: 8px 60px 8px 0;
    font-size: 0.95rem;
    line-height: 1.5;
}
.chat-label-user {
    text-align: right;
    font-size: 0.72rem;
    color: #9090a0;
    margin-bottom: 2px;
    text-transform: uppercase;
    letter-spacing: 0.07em;
}
.chat-label-ai {
    font-size: 0.72rem;
    color: #9090a0;
    margin-bottom: 2px;
    text-transform: uppercase;
    letter-spacing: 0.07em;
}

/* Loop badges */
.loop-badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
    margin-right: 6px;
}
.badge-closed  { background: #d4edda; color: #276336; }
.badge-open    { background: #fff3cd; color: #856404; }
.badge-delayed { background: #fde8e0; color: #a63a1a; }

/* Section headers */
.section-header {
    font-family: 'DM Serif Display', serif;
    font-size: 1.5rem;
    color: #1a1a2e;
    margin-bottom: 0.2rem;
}
.section-sub {
    font-size: 0.88rem;
    color: #9090a0;
    margin-bottom: 1.2rem;
}

/* Sample question pills */
.sample-q {
    display: inline-block;
    background: #f0ede8;
    border: 1px solid #ddd;
    border-radius: 20px;
    padding: 5px 14px;
    font-size: 0.82rem;
    color: #444;
    margin: 3px;
    cursor: pointer;
}
</style>
""", unsafe_allow_html=True)


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🧠 Personal Intel AI")
    st.markdown("*Prototype — Sample User Data*")
    st.markdown("---")

    page = st.radio(
        "Navigate",
        ["💬 Chat", "📊 Dashboard", "🔍 Patterns & Loops"],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("**About this demo**")
    st.markdown(
        "This AI has analysed one week of a test subject's behavioral data — "
        "events, emotions, decisions, and loops.",
        unsafe_allow_html=False
    )
    st.markdown("---")

    # Quick stats
    st.markdown(f"**{len(signals)}** events tracked")
    st.markdown(f"**{len(decisions)}** decisions logged")
    st.markdown(f"**{len(loops)}** loops identified")
    st.markdown(f"**{len(patterns)}** patterns found")


# ═══════════════════════════════════════════════════════════
#  PAGE 1 — CHAT
# ═══════════════════════════════════════════════════════════
if page == "💬 Chat":

    st.markdown('<div class="hero-title">Ask About Your Week</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">Your personal AI has read your full week. Ask it anything.</div>', unsafe_allow_html=True)

    # Lazy-load agent only when chat page is open
    if "agent_loaded" not in st.session_state:
        with st.spinner("Loading your personal AI agent…"):
            try:
                from agent import ask as agent_ask
                st.session_state.agent_ask   = agent_ask
                st.session_state.agent_loaded = True
            except Exception as e:
                st.error(f"Could not load agent: {e}")
                st.session_state.agent_loaded = False

    # Chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "ai",
                "content": (
                    "Hi! I've read your full week — 67 events, 22 decisions, "
                    "10 behavioral loops, and 10 pattern insights. "
                    "What would you like to explore about yourself?"
                )
            }
        ]

    # Sample questions
    SAMPLES = [
        "What time am I most productive?",
        "What triggers my stress?",
        "How is my relationship with family?",
        "What are my top 3 habits?",
        "When do I feel happiest?",
        "What decisions did I make when tired?",
        "Summarize my week in 3 sentences.",
        "What loops did I leave open?",
    ]

    st.markdown("**Try asking:**")
    cols = st.columns(4)
    for i, q in enumerate(SAMPLES):
        if cols[i % 4].button(q, key=f"sample_{i}", use_container_width=True):
            st.session_state.pending_question = q

    st.markdown("---")

    # Render chat history
    chat_box = st.container()
    with chat_box:
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.markdown(f'<div class="chat-label-user">You</div><div class="chat-msg-user">{msg["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-label-ai">🧠 Agent</div><div class="chat-msg-ai">{msg["content"]}</div>', unsafe_allow_html=True)

    # Input
    user_input = st.chat_input("Ask about your habits, emotions, patterns…")

    # Handle sample question click
    if "pending_question" in st.session_state:
        user_input = st.session_state.pop("pending_question")

    if user_input and st.session_state.get("agent_loaded"):
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.spinner("Thinking…"):
            try:
                response = st.session_state.agent_ask(user_input)
            except Exception as e:
                response = f"Something went wrong: {e}"

        st.session_state.messages.append({"role": "ai", "content": response})
        st.rerun()

    elif user_input and not st.session_state.get("agent_loaded"):
        st.warning("Agent failed to load. Check your .env API keys.")

    # Clear chat button
    if len(st.session_state.get("messages", [])) > 1:
        if st.button("🗑 Clear chat", type="secondary"):
            st.session_state.messages = [st.session_state.messages[0]]
            st.rerun()


# ═══════════════════════════════════════════════════════════
#  PAGE 2 — DASHBOARD
# ═══════════════════════════════════════════════════════════
elif page == "📊 Dashboard":

    st.markdown('<div class="hero-title">Behavioral Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">A visual breakdown of one week of life data.</div>', unsafe_allow_html=True)

    # ── Top metric cards ──────────────────────────────────────────────
    m1, m2, m3, m4 = st.columns(4)

    emotion_counts = Counter(s["Emotion"] for s in signals)
    top_emotion    = emotion_counts.most_common(1)[0][0]
    work_count     = sum(1 for s in signals if s["Type"] == "Work")
    social_count   = sum(1 for s in signals if s["Type"] == "Social")
    closed_loops   = sum(1 for l in loops if "Closed" in str(l.get("Status", "")))

    with m1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{len(signals)}</div>
            <div class="metric-label">Events Tracked</div>
        </div>""", unsafe_allow_html=True)

    with m2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{top_emotion}</div>
            <div class="metric-label">Top Emotion</div>
        </div>""", unsafe_allow_html=True)

    with m3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{work_count}</div>
            <div class="metric-label">Work Events</div>
        </div>""", unsafe_allow_html=True)

    with m4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{closed_loops}/{len(loops)}</div>
            <div class="metric-label">Loops Closed</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")

    # ── Row 1: Emotion bar + Activity type donut ──────────────────────
    col1, col2 = st.columns([3, 2])

    with col1:
        st.markdown('<div class="section-header">Emotion Frequency</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-sub">How often each emotional state appeared across the week</div>', unsafe_allow_html=True)

        emotions = dict(emotion_counts.most_common(10))
        color_map = {
            "Neutral": "#b0b0c0", "Relaxed": "#7ec8a0", "Focus": "#4a90e8",
            "Happy": "#f7c948", "Calm": "#90cce8", "Slight stress": "#e8a04a",
            "Professional": "#7b68ee", "Tired": "#c0a080", "Warm": "#f0a878",
            "Mild distraction": "#d0a0c0", "Excited": "#f06090",
            "Anxious": "#e87070", "Frustration": "#e05050",
        }
        colors = [color_map.get(e, "#cccccc") for e in emotions.keys()]

        fig_bar = go.Figure(go.Bar(
            x=list(emotions.values()),
            y=list(emotions.keys()),
            orientation="h",
            marker_color=colors,
            text=list(emotions.values()),
            textposition="outside",
        ))
        fig_bar.update_layout(
            height=360, margin=dict(l=0, r=40, t=10, b=10),
            paper_bgcolor="white", plot_bgcolor="white",
            font=dict(family="DM Sans", size=13),
            xaxis=dict(showgrid=False, showticklabels=False),
            yaxis=dict(autorange="reversed"),
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    with col2:
        st.markdown('<div class="section-header">Activity Breakdown</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-sub">How time was distributed across life areas</div>', unsafe_allow_html=True)

        type_counts = Counter(s["Type"] for s in signals)
        type_colors = {
            "Work": "#4a90e8", "Leisure": "#7ec8a0", "Routine": "#b0b0c0",
            "Social": "#f7c948", "Personal": "#f0a878", "Habit": "#7b68ee", "Health": "#e87070",
        }
        fig_pie = go.Figure(go.Pie(
            labels=list(type_counts.keys()),
            values=list(type_counts.values()),
            marker_colors=[type_colors.get(t, "#cccccc") for t in type_counts.keys()],
            hole=0.55,
            textinfo="label+percent",
            textfont=dict(size=12, family="DM Sans"),
        ))
        fig_pie.update_layout(
            height=360, margin=dict(l=0, r=0, t=10, b=10),
            paper_bgcolor="white", showlegend=False,
            font=dict(family="DM Sans"),
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    # ── Row 2: Hourly activity heatmap ────────────────────────────────
    st.markdown('<div class="section-header">Activity by Time of Day</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">When events happened across all 7 days</div>', unsafe_allow_html=True)

    hour_activity = Counter()
    for s in signals:
        if s.get("Time"):
            h = int(s["Time"].split(":")[0])
            hour_activity[h] += 1

    all_hours = list(range(0, 24))
    counts    = [hour_activity.get(h, 0) for h in all_hours]
    labels    = [f"{h:02d}:00" for h in all_hours]

    fig_hour = go.Figure(go.Bar(
        x=labels, y=counts,
        marker_color=["#e8704a" if c == max(counts) else "#4a90e8" for c in counts],
        text=counts, textposition="outside",
    ))
    fig_hour.update_layout(
        height=240, margin=dict(l=0, r=0, t=10, b=10),
        paper_bgcolor="white", plot_bgcolor="white",
        font=dict(family="DM Sans", size=12),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False, showticklabels=False),
    )
    fig_hour.add_vrect(x0="09:00", x1="17:00", fillcolor="#4a90e8",
                       opacity=0.06, layer="below", line_width=0,
                       annotation_text="Core work hours", annotation_position="top left",
                       annotation_font_size=11, annotation_font_color="#4a90e8")
    st.plotly_chart(fig_hour, use_container_width=True)

    # ── Row 3: Decisions confidence + day-by-day mood ─────────────────
    col3, col4 = st.columns(2)

    with col3:
        st.markdown('<div class="section-header">Decision Confidence</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-sub">How sure were the decisions made?</div>', unsafe_allow_html=True)

        valid_decisions = [d for d in decisions if d.get("Confidence") in ("High", "Medium", "Low")]
        conf_counts = Counter(d["Confidence"] for d in valid_decisions)
        conf_order  = ["High", "Medium", "Low"]
        conf_colors = {"High": "#7ec8a0", "Medium": "#f7c948", "Low": "#e87070"}

        fig_conf = go.Figure(go.Bar(
            x=conf_order,
            y=[conf_counts.get(c, 0) for c in conf_order],
            marker_color=[conf_colors[c] for c in conf_order],
            text=[conf_counts.get(c, 0) for c in conf_order],
            textposition="outside",
            width=0.4,
        ))
        fig_conf.update_layout(
            height=260, margin=dict(l=0, r=0, t=10, b=10),
            paper_bgcolor="white", plot_bgcolor="white",
            font=dict(family="DM Sans", size=13),
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=False, showticklabels=False),
        )
        st.plotly_chart(fig_conf, use_container_width=True)

    with col4:
        st.markdown('<div class="section-header">Positive vs Negative Emotions by Day</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-sub">Emotional tone across the week</div>', unsafe_allow_html=True)

        positive = {"Happy", "Relaxed", "Focus", "Calm", "Warm", "Excited",
                    "Motivated", "Comfort", "Curious", "Relief", "Enjoyment",
                    "Productive", "Prepared", "Professional"}
        negative = {"Slight stress", "Tired", "Anxious", "Frustration",
                    "Guilt", "Stress", "Bored", "Mild distraction", "Slight anxiety"}

        day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        pos_by_day = Counter()
        neg_by_day = Counter()
        for s in signals:
            day = s.get("Day")
            emo = s.get("Emotion", "")
            if emo in positive:
                pos_by_day[day] += 1
            elif emo in negative:
                neg_by_day[day] += 1

        fig_mood = go.Figure()
        fig_mood.add_trace(go.Bar(
            name="Positive", x=day_order,
            y=[pos_by_day.get(d, 0) for d in day_order],
            marker_color="#7ec8a0",
        ))
        fig_mood.add_trace(go.Bar(
            name="Negative", x=day_order,
            y=[-neg_by_day.get(d, 0) for d in day_order],
            marker_color="#e87070",
        ))
        fig_mood.update_layout(
            height=260, barmode="relative",
            margin=dict(l=0, r=0, t=10, b=10),
            paper_bgcolor="white", plot_bgcolor="white",
            font=dict(family="DM Sans", size=12),
            legend=dict(orientation="h", y=1.1),
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=False, zeroline=True, zerolinecolor="#ddd"),
        )
        st.plotly_chart(fig_mood, use_container_width=True)


# ═══════════════════════════════════════════════════════════
#  PAGE 3 — PATTERNS & LOOPS
# ═══════════════════════════════════════════════════════════
elif page == "🔍 Patterns & Loops":

    st.markdown('<div class="hero-title">Patterns & Loops</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">What the AI discovered from your behavioral data.</div>', unsafe_allow_html=True)

    # ── Pattern cards ─────────────────────────────────────────────────
    st.markdown('<div class="section-header">🔬 Pattern Engine Insights</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">10 patterns identified from the week\'s data</div>', unsafe_allow_html=True)

    conf_color = {"High": "#4a90e8", "Medium": "#e8a04a", "Low": "#e87070"}

    cols = st.columns(2)
    for i, p in enumerate(patterns):
        with cols[i % 2]:
            color = conf_color.get(p.get("Confidence", "Medium"), "#4a90e8")
            st.markdown(f"""
            <div class="insight-card" style="border-top-color: {color}">
                <div class="insight-type">{p.get('Pattern Type', '?')} · {p.get('Confidence', '?')} confidence</div>
                <div class="insight-text"><strong>{p.get('Insight', '')}</strong></div>
                <div class="insight-text" style="margin-top:6px; color:#555">{p.get('Observation', '')}</div>
                <div class="insight-reflection">💭 {p.get('Reflection Prompt', '')}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # ── Loops table ───────────────────────────────────────────────────
    st.markdown('<div class="section-header">🔁 Behavioral Loops</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Tasks and intentions tracked across the week</div>', unsafe_allow_html=True)

    # Loops by type chart
    loop_type_counts = Counter(l["Type"] for l in loops)
    loop_colors = {
        "Work": "#4a90e8", "Personal": "#f0a878",
        "Health": "#7ec8a0", "Leisure": "#f7c948", "Social": "#7b68ee"
    }

    fig_loops = go.Figure(go.Bar(
        x=list(loop_type_counts.keys()),
        y=list(loop_type_counts.values()),
        marker_color=[loop_colors.get(t, "#cccccc") for t in loop_type_counts.keys()],
        text=list(loop_type_counts.values()),
        textposition="outside",
        width=0.4,
    ))
    fig_loops.update_layout(
        height=220, margin=dict(l=0, r=0, t=10, b=10),
        paper_bgcolor="white", plot_bgcolor="white",
        font=dict(family="DM Sans", size=13),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False, showticklabels=False),
    )
    st.plotly_chart(fig_loops, use_container_width=True)

    # Loops detail table
    for l in loops:
        status = str(l.get("Status", ""))
        if "Open → Closed" in status:
            badge = '<span class="loop-badge badge-delayed">Delayed</span>'
        elif "Closed" in status:
            badge = '<span class="loop-badge badge-closed">Closed</span>'
        else:
            badge = '<span class="loop-badge badge-open">Open</span>'

        st.markdown(f"""
        <div style="background:white; border-radius:12px; padding:14px 20px;
                    margin-bottom:8px; box-shadow:0 2px 8px rgba(0,0,0,0.05);">
            {badge}
            <strong style="font-size:0.95rem">{l.get('Loop', '')}</strong>
            <span style="color:#9090a0; font-size:0.82rem; margin-left:10px">
                {l.get('Type', '')} · Mentioned {int(l.get('Mentions', 1))}x
            </span>
            <div style="color:#777; font-size:0.82rem; margin-top:4px">
                📅 {l.get('Opened', '')} → {l.get('Closed', 'Not closed')}
                &nbsp;·&nbsp; {l.get('Notes', '')}
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # ── Emotion → Decision mapping ────────────────────────────────────
    st.markdown('<div class="section-header">⚡ Emotion → Decision Patterns</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">What emotions drove which kinds of decisions</div>', unsafe_allow_html=True)

    valid_d = [d for d in decisions if d.get("Emotion") and d.get("Decision")]
    df = pd.DataFrame([{"Emotion": d["Emotion"], "Decision": d["Decision"],
                         "Confidence": d.get("Confidence", "Medium")} for d in valid_d])

    if not df.empty:
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Emotion":    st.column_config.TextColumn("Emotion", width="medium"),
                "Decision":   st.column_config.TextColumn("Decision Made", width="large"),
                "Confidence": st.column_config.TextColumn("Confidence", width="small"),
            }
        )
