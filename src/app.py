import pandas as pd
import streamlit as st
import plotly.express as px
from textblob import TextBlob

# =====================================
# Page Config & Custom CSS
# =====================================
st.set_page_config(page_title="Social Media Analytics POC", layout="wide")

st.markdown(
    """
<style>
    .header {
        font-size: 2.5em !important;
        color: #2E86AB !important;
        border-bottom: 2px solid #F18F01;
        padding-bottom: 10px;
    }
    .metric-card {
        background-color: #F6F7F8;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 15px;
    }
    .critical-alert {
        background-color: #FFEBEE !important;
        border-left: 4px solid #C62828;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .positive {
        color: #2E7D32 !important;
    }
    .negative {
        color: #C62828 !important;
    }
    .tech-term {
        background-color: #E3F2FD;
        padding: 2px 5px;
        border-radius: 3px;
        font-weight: 500;
    }
</style>
""",
    unsafe_allow_html=True,
)

# =====================================
# Header with Logo
# =====================================
col1, col2 = st.columns([1, 6])
with col1:
    st.image(
        "data:image/png;base64,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",
        width=80,
    )
with col2:
    st.markdown(
        '<h1 class="header">Business Solutions Social Analytics</h1>',
        unsafe_allow_html=True,
    )


# =====================================
# Data Loading
# =====================================
@st.cache_data
def load_data():
    posts = pd.read_csv("mock_posts_biz.csv")
    comments = pd.read_csv("mock_comments_biz.csv")

    # Sentiment analysis
    comments["sentiment"] = comments["comment_text"].apply(
        lambda x: TextBlob(x).sentiment.polarity
    )
    comments["sentiment_label"] = comments["sentiment"].apply(
        lambda x: "Positive" if x > 0.2 else "Negative" if x < -0.2 else "Neutral"
    )

    return posts, comments


posts_df, comments_df = load_data()

# Calculate urgent issues
urgent_issues = len(
    comments_df[
        (comments_df["sentiment_label"] == "Negative")
        & (
            comments_df["comment_text"].str.contains(
                "urgent|critical|outage", case=False
            )
        )
    ]
)

# =====================================
# Executive Summary Metrics
# =====================================
st.subheader("📊 Executive Summary")
cols = st.columns(4)
metric_styles = {"font-size": "24px", "font-weight": "bold", "margin-top": "-10px"}

with cols[0]:
    st.markdown(
        f"""
    <div class="metric-card">
        <p style="font-size:14px; color:#666;">Total Posts</p>
        <h3 style="{'; '.join(f'{k}:{v}' for k,v in metric_styles.items())}; color:#2E86AB;">{len(posts_df)}</h3>
    </div>
    """,
        unsafe_allow_html=True,
    )

with cols[1]:
    st.markdown(
        f"""
    <div class="metric-card">
        <p style="font-size:14px; color:#666;">High-Urgency Issues</p>
        <h3 style="{'; '.join(f'{k}:{v}' for k,v in metric_styles.items())}; color:#C62828;">{urgent_issues}</h3>
    </div>
    """,
        unsafe_allow_html=True,
    )

with cols[2]:
    pos = comments_df[comments_df["sentiment_label"] == "Positive"].shape[0]
    if len(comments_df) > 0:
        positive_percentage = int(pos / len(comments_df) * 100)
    else:
        positive_percentage = 0  # Default to 0% if no comments are available
    st.markdown(
        f"""
    <div class="metric-card">
        <p style="font-size:14px; color:#666;">Positive Sentiment</p>
        <h3 style="{'; '.join(f'{k}:{v}' for k,v in metric_styles.items())}; color:#2E7D32;">{positive_percentage}%</h3>
    </div>
    """,
        unsafe_allow_html=True,
    )

with cols[3]:
    st.markdown(
        f"""
    <div class="metric-card">
        <p style="font-size:14px; color:#666;">Avg. Engagement</p>
        <h3 style="{'; '.join(f'{k}:{v}' for k,v in metric_styles.items())}; color:#2E86AB;">{round(posts_df[['likes','shares','comments']].mean().mean())}</h3>
    </div>
    """,
        unsafe_allow_html=True,
    )

# =====================================
# Tabbed Interface
# =====================================
tab1, tab2, tab3, tab4 = st.tabs(
    ["Sentiment", "Engagement", "Post Details", "Tech Insights"]
)

# ------------------
# Sentiment Analysis
# ------------------
with tab1:
    col1, col2 = st.columns(2)
    with col1:
        fig = px.pie(
            comments_df,
            names="sentiment_label",
            title="<b>Overall Sentiment Distribution</b>",
            color="sentiment_label",
            color_discrete_map={
                "Positive": "#2E7D32",
                "Negative": "#C62828",
                "Neutral": "#2E86AB",
            },
            hole=0.4,
        )
        fig.update_layout(title_x=0.3)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.bar(
            comments_df.groupby(["platform", "sentiment_label"]).size().unstack(),
            title="<b>Sentiment by Platform</b>",
            barmode="group",
            color_discrete_map={
                "Positive": "#2E7D32",
                "Negative": "#C62828",
                "Neutral": "#2E86AB",
            },
        )
        fig.update_layout(
            xaxis_title="Platform", yaxis_title="Count", plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig, use_container_width=True)

# ------------------
# Engagement Trends
# ------------------
with tab2:
    posts_df["date"] = pd.to_datetime(posts_df["date"])
    fig = px.line(
        posts_df.sort_values("date"),
        x="date",
        y=["likes", "shares", "comments"],
        title="<b>Engagement Over Time</b>",
        markers=True,
        color_discrete_sequence=["#2E86AB", "#F18F01", "#C62828"],
    )
    fig.update_layout(xaxis_title="Date", yaxis_title="Count", hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)

# ------------------
# Post Details
# ------------------
with tab3:
    selected_post = st.selectbox("Select a Post", posts_df["post_text"], index=0)
    post_data = posts_df[posts_df["post_text"] == selected_post].iloc[0]
    post_comments = comments_df[comments_df["post_id"] == post_data["post_id"]]

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            f"""
        <div class="metric-card">
            <h4>Post Details</h4>
            <p><strong>Platform:</strong> {post_data['platform']}</p>
            <p><strong>Type:</strong> {post_data['post_type']}</p>
            <p><strong>Date:</strong> {post_data['date']}</p>
            <div style="display: flex; gap: 15px; margin-top: 10px;">
                <span>👍 {post_data['likes']}</span>
                <span>🔗 {post_data['shares']}</span>
                <span>💬 {post_data['comments']}</span>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        if not post_comments.empty:
            fig = px.pie(
                post_comments,
                names="sentiment_label",
                title="<b>Sentiment for Post</b>",
                hole=0.4,
                color="sentiment_label",
                color_discrete_map={
                    "Positive": "#2E7D32",
                    "Negative": "#C62828",
                    "Neutral": "#2E86AB",
                },
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No comments found for this post")

# ------------------
# Tech Insights
# ------------------
with tab4:
    st.subheader("🔍 Technical Deep Dive")

    tech_terms = {
        "AI": comments_df["comment_text"]
        .str.contains("AI|artificial intelligence", case=False)
        .sum(),
        "Cloud": comments_df["comment_text"]
        .str.contains("cloud|AWS|Azure", case=False)
        .sum(),
        "Security": comments_df["comment_text"]
        .str.contains("security|cyber|CVE", case=False)
        .sum(),
        "API": comments_df["comment_text"]
        .str.contains("API|integration", case=False)
        .sum(),
    }

    col1, col2 = st.columns(2)
    with col1:
        fig = px.treemap(
            names=list(tech_terms.keys()),
            parents=[""] * len(tech_terms),
            values=list(tech_terms.values()),
            title="<b>Technical Topic Volume</b>",
            color=list(tech_terms.values()),
            color_continuous_scale="Blues",
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        negative_comments = comments_df[comments_df["sentiment_label"] == "Negative"]
        st.markdown(
            """
        <div style="background-color:#F6F7F8; padding:20px; border-radius:10px;">
            <h4 style="color:#2E86AB; margin-top:0;">Top Technical Complaints</h4>
            <ul style="padding-left:20px;">
        """
            + "\n".join(
                [
                    f"<li><span class='tech-term'>{term}</span>: {negative_comments['comment_text'].str.contains(term, case=False).sum()} complaints</li>"
                    for term in tech_terms.keys()
                ]
            )
            + """
            </ul>
        </div>
        """,
            unsafe_allow_html=True,
        )

# ------------------
# Critical Alerts
# ------------------
critical = comments_df[
    (comments_df["sentiment_label"] == "Negative")
    & (comments_df["comment_text"].str.contains("urgent|critical|outage", case=False))
].sort_values("likes", ascending=False)

if not critical.empty:
    st.markdown(
        """
    <div class="critical-alert">
        <h3 style="color:#C62828; margin-top:0;">🚨 Critical Issues Needing Attention</h3>
    </div>
    """,
        unsafe_allow_html=True,
    )

    for _, row in critical.head(3).iterrows():
        st.markdown(
            f"""
        <div style="padding:12px; margin:8px 0; background-color:#FFF5F5; border-radius:5px; border-left: 3px solid #C62828;">
            <p style="margin:0; font-weight:bold;">{row['comment_text']}</p>
            <p style="margin:4px 0 0 0; font-size:0.8em; color:#666;">
                <strong>{row['platform']}</strong> • {row['date']} • 👍 {row['likes']} likes
            </p>
        </div>
        """,
            unsafe_allow_html=True,
        )
