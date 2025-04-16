import pandas as pd
import streamlit as st
import plotly.express as px
from textblob import TextBlob


# =====================================
# Data Loading & Preprocessing
# =====================================
st.set_page_config(page_title="Social Media Analytics POC", layout="wide")


@st.cache_data
def load_data():
    # Load posts and comments
    posts = pd.read_csv("mock_posts_biz.csv")
    comments = pd.read_csv("mock_comments_biz.csv")

    # Sentiment analysis for comments
    comments["sentiment"] = comments["comment_text"].apply(
        lambda x: TextBlob(x).sentiment.polarity
    )
    comments["sentiment_label"] = comments["sentiment"].apply(
        lambda x: "Positive" if x > 0.2 else "Negative" if x < -0.2 else "Neutral"
    )

    # Merge with posts
    merged = pd.merge(
        posts,
        comments.groupby("post_id")["sentiment_label"]
        .value_counts()
        .unstack()
        .fillna(0),
        left_on="post_id",
        right_index=True,
    )

    return posts, comments, merged


posts_df, comments_df, merged_df = load_data()

# =====================================
# Dashboard UI
# =====================================
st.title("🚀 AI-Powered Social Media Analytics")

# ------------------
# Key Metrics Row
# ------------------
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Posts", len(posts_df))
with col2:
    st.metric(
        "Avg Engagement", f"{posts_df[['likes','shares','comments']].sum().mean():.0f}"
    )
with col3:
    pos = comments_df[comments_df["sentiment_label"] == "Positive"].shape[0]
    st.metric("Positive Comments", pos)
with col4:
    neg = comments_df[comments_df["sentiment_label"] == "Negative"].shape[0]
    st.metric("Critical Comments", neg)

# ------------------
# Visualizations
# ------------------
# tab1, tab2, tab3 = st.tabs(["Sentiment Analysis", "Engagement Trends", "Post Details"])
tab1, tab2, tab3, tab4 = st.tabs(
    ["Sentiment", "Engagement", "Post Details", "Tech Insights"]
)

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        # Sentiment distribution
        fig = px.pie(
            comments_df,
            names="sentiment_label",
            title="Overall User Sentiment",
            color="sentiment_label",
            color_discrete_map={
                "Positive": "#2ecc71",
                "Negative": "#e74c3c",
                "Neutral": "#3498db",
            },
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Sentiment by platform
        fig = px.bar(
            comments_df.groupby(["platform", "sentiment_label"]).size().unstack(),
            title="Sentiment by Platform",
            barmode="group",
        )
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    # Engagement timeline
    posts_df["date"] = pd.to_datetime(posts_df["date"])
    fig = px.line(
        posts_df.sort_values("date"),
        x="date",
        y=["likes", "shares", "comments"],
        title="Engagement Over Time",
        markers=True,
    )
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    # Post selector
    selected_post = st.selectbox("Select a Post", posts_df["post_text"], index=0)

    post_data = posts_df[posts_df["post_text"] == selected_post].iloc[0]
    post_comments = comments_df[comments_df["post_id"] == post_data["post_id"]]

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Post Details")
        st.markdown(f"""
        - **Platform**: {post_data['platform']}
        - **Post Type**: {post_data['post_type']}
        - **Engagement**: 
          - 👍 {post_data['likes']} 
          - 🔗 {post_data['shares']} 
          - 💬 {post_data['comments']}
        """)

    with col2:
        st.subheader("User Reactions")
        if not post_comments.empty:
            fig = px.pie(
                post_comments,
                names="sentiment_label",
                title=f"Sentiment for: {selected_post}",
                hole=0.4,
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No comments found for this post")

# ------------------
# Critical Comments Table
# ------------------
st.subheader("⚠️ Top Critical Feedback")
critical = comments_df[comments_df["sentiment_label"] == "Negative"].sort_values(
    "likes", ascending=False
)
if not critical.empty:
    st.dataframe(
        critical[["comment_text", "platform", "likes"]],
        column_config={
            "comment_text": "Comment",
            "platform": "Platform",
            "likes": "Likes",
        },
        hide_index=True,
    )
else:
    st.success("No critical comments found! 🎉")
with tab4:
    st.subheader("Technical Topic Breakdown")

    # Tech term frequency
    tech_terms = ["AI", "cloud", "cybersecurity", "API", "compliance"]
    term_counts = {
        term: comments_df["comment_text"].str.contains(term, case=False).sum()
        for term in tech_terms
    }

    fig = px.bar(
        x=list(term_counts.keys()),
        y=list(term_counts.values()),
        title="Most Discussed Technical Topics",
    )
    st.plotly_chart(fig, use_container_width=True)

    # Negative comments by topic
    st.subheader("Critical Feedback by Topic")
    negative_comments = comments_df[comments_df["sentiment_label"] == "Negative"]
    topic_complaints = {}

    for term in tech_terms:
        topic_complaints[term] = (
            negative_comments["comment_text"].str.contains(term, case=False).sum()
        )

    fig = px.pie(
        names=list(topic_complaints.keys()),
        values=list(topic_complaints.values()),
        title="Negative Comments by Technical Area",
    )
    st.plotly_chart(fig, use_container_width=True)
