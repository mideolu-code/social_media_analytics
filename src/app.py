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
        "https://www.aimtechnologies.co/wp-content/uploads/2023/08/Data-Analytics-On-Social-Media.jpg",
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
    st.markdown(
        f"""
    <div class="metric-card">
        <p style="font-size:14px; color:#666;">Positive Sentiment</p>
        <h3 style="{'; '.join(f'{k}:{v}' for k,v in metric_styles.items())}; color:#2E7D32;">{int(pos/len(comments_df)*100)}%</h3>
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
