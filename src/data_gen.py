import pandas as pd
import numpy as np
from faker import Faker
from datetime import timedelta

fake = Faker()
np.random.seed(42)

# =====================================
# Generate 500 Business-Tech Posts
# =====================================
platforms = ["LinkedIn"] * 250 + ["Twitter"] * 150 + ["Facebook"] * 100
post_types = (
    ["whitepaper"] * 150
    + ["case_study"] * 125
    + ["alert"] * 100
    + ["webinar"] * 75
    + ["product_update"] * 50
)

posts = []
for post_id in range(1, 501):
    platform = np.random.choice(platforms)
    post_type = np.random.choice(post_types)

    # Platform-specific engagement
    if platform == "LinkedIn":
        likes = np.random.randint(200, 5000)
        shares = np.random.randint(100, 2000)
    elif platform == "Twitter":
        likes = np.random.randint(100, 1500)
        shares = np.random.randint(20, 500)
    else:  # Facebook
        likes = np.random.randint(50, 1000)
        shares = np.random.randint(10, 300)

    # Business-focused post content (now includes product_update)
    content_map = {
        "whitepaper": f"{fake.random_element(['AI-Driven','Cloud-Native'])} {fake.random_element(['Digital Transformation','Compliance Framework'])} Whitepaper",
        "case_study": f"Case Study: {fake.company()} achieved {np.random.randint(40,95)}% {fake.random_element(['cost reduction','fraud prevention','API latency improvement'])}",
        "alert": f"Urgent: {fake.random_element(['Zero-Day','DDoS'])} mitigation strategy for {fake.random_element(['Azure','AWS','Hybrid Clouds'])}",
        "webinar": f"Live Session: {fake.random_element(['Generative AI Governance','SOC2 Compliance'])} Best Practices",
        "product_update": f"New Release: {fake.random_element(['v3.2','v4.0'])} introduces {fake.random_element(['real-time threat detection','multi-cloud cost analytics'])}",
    }
    post_text = content_map[post_type]  # Now handles all post types

    posts.append(
        {
            "post_id": post_id,
            "platform": platform,
            "post_text": post_text,
            "post_type": post_type,
            "likes": likes,
            "shares": shares,
            "comments": np.random.randint(20, 500),
            "date": fake.date_between(start_date="-1y", end_date="today"),
        }
    )

posts_df = pd.DataFrame(posts)

# =====================================
# Generate 1500+ B2B Comments
# =====================================
comments = []
comment_id = 1

tech_terms = ["Kubernetes", "LLM", "SIEM", "IaC", "Zero Trust"]
roles = ["CTO", "CIO", "Security Engineer", "Cloud Architect"]

for _, post in posts_df.iterrows():
    num_comments = np.random.randint(3, 6)

    for _ in range(num_comments):
        sentiment = np.random.choice(
            ["positive"] * 5 + ["neutral"] * 3 + ["negative"] * 2
        )
        user = f"@{fake.user_name()}_{fake.random_element(roles)}"

        if sentiment == "positive":
            text = fake.random_element(
                [
                    f"Deployed this across our {np.random.randint(10,50)} locations!",
                    f"{fake.random_element(tech_terms)} integration works flawlessly",
                    "Our {fake.random_element(['auditors','board'])} loved the compliance features",
                ]
            )
        elif sentiment == "negative":
            text = fake.random_element(
                [
                    f"{fake.random_element(tech_terms)} compatibility issues in v{np.random.choice(['2.1','3.0'])}",
                    "SLA breach during {fake.random_element(['migration','pen test'])}",
                    "Support ticket #{fake.random_int(1000,9999)} still unresolved",
                ]
            )
        else:
            text = fake.random_element(
                [
                    f"Pricing for {fake.random_element(['non-profits','enterprises'])}?",
                    "Terraform provider available?",
                    "Roadmap for {fake.random_element(['FedRAMP','GDPR'])} certification?",
                ]
            )

        comments.append(
            {
                "comment_id": comment_id,
                "post_id": post["post_id"],
                "platform": post["platform"],
                "comment_text": text,
                "user": user,
                "likes": np.random.randint(1, 100),
                "date": post["date"] + timedelta(days=np.random.randint(0, 3)),
            }
        )
        comment_id += 1

comments_df = pd.DataFrame(comments)

# Save to CSV
posts_df.to_csv("mock_posts_biz.csv", index=False)
comments_df.to_csv("mock_comments_biz.csv", index=False)
