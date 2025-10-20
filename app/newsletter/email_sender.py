# def newsletter_to_html(newsletter_text: str, logo_url: str = None) -> str:
#     """Convert LLM newsletter output to a warm, newsletter-style HTML"""
#     import re
#
#     # Extract sections using regex
#     subject_match = re.search(r"SUBJECT:\s*(.*)", newsletter_text)
#     summary_match = re.search(r"SUMMARY:\s*(.*?)LEARNING:", newsletter_text, re.DOTALL)
#     learning_match = re.search(r"LEARNING:\s*(.*)", newsletter_text)
#     action_match = re.search(r"ACTION:\s*(.*)", newsletter_text)
#     trends_match = re.search(r"TRENDS TO WATCH:\s*(.*)", newsletter_text, re.DOTALL)
#
#     subject = subject_match.group(1).strip() if subject_match else ""
#     summary = summary_match.group(1).strip().replace("\n", "<br>") if summary_match else ""
#     learning = learning_match.group(1).strip() if learning_match else ""
#     action = action_match.group(1).strip() if action_match else ""
#     trends_raw = trends_match.group(1).strip() if trends_match else ""
#
#     # Convert trends into styled blocks
#     trends_html = ""
#     for line in trends_raw.split("\n"):
#         line = line.strip()
#         if line:
#             # Convert [Link](url) to clickable button
#             link_match = re.search(r"\[Link\]\((.*?)\)", line)
#             link_html = link_match.group(1) if link_match else "#"
#             line_clean = re.sub(r"\[Link\]\(.*?\)", "", line)
#             # Remove numbering
#             line_clean = re.sub(r"^\d+\.\s*", "", line_clean)
#
#             trends_html += f"""
#             <div style="background-color:#fff3e0; padding:15px; margin-bottom:15px; border-radius:8px; box-shadow:0 2px 5px rgba(0,0,0,0.1);">
#                 <h3 style="margin:0; color:#e65100;">{line_clean.split(' - ')[0]}</h3>
#                 <p style="margin:5px 0 10px 0; color:#5d4037;">{" - ".join(line_clean.split(' - ')[1:])}</p>
#                 <a href="{link_html}" style="display:inline-block; padding:8px 15px; background-color:#fb8c00; color:white; text-decoration:none; border-radius:4px;">Read More</a>
#             </div>
#             """
#
#     html_content = f"""
#     <html>
#     <head>
#         <style>
#             body {{
#                 font-family: 'Arial', sans-serif;
#                 background-color: #fff8f0;
#                 color: #4e342e;
#                 line-height: 1.6;
#                 padding: 20px;
#             }}
#             h1 {{
#                 color: #bf360c;
#                 text-align: center;
#             }}
#             h2 {{
#                 color: #e64a19;
#                 border-bottom: 2px solid #ffccbc;
#                 padding-bottom: 5px;
#             }}
#             p {{
#                 margin-bottom: 15px;
#             }}
#             .section {{
#                 margin-bottom: 30px;
#             }}
#             .newsletter-logo {{
#                 display: block;
#                 margin: 0 auto 20px auto;
#                 max-width: 150px;
#             }}
#         </style>
#     </head>
#     <body>
#         {f'<img src="{logo_url}" class="newsletter-logo">' if logo_url else ''}
#         <h1>{subject}</h1>
#
#         <div class="section">
#             <h2>Summary</h2>
#             <p>{summary}</p>
#         </div>
#
#         <div class="section">
#             <h2>Key Learning</h2>
#             <p>{learning}</p>
#         </div>
#
#         <div class="section">
#             <h2>Action Item</h2>
#             <p>{action}</p>
#         </div>
#
#         <div class="section">
#             <h2>Trends to Watch</h2>
#             {trends_html}
#         </div>
#     </body>
#     </html>
#     """
#
#     return html_content

def newsletter_to_html(newsletter_json: dict, logo_url: str = None) -> str:
    """Convert curated newsletter JSON to warm HTML"""
    intro = newsletter_json.get("intro", "")
    curated_links = newsletter_json.get("curated_links", [])
    summaries = newsletter_json.get("summaries", [])
    commentary = newsletter_json.get("commentary", "")
    trends = newsletter_json.get("trends", [])

    # Curated links HTML
    curated_html = ""
    for link in curated_links:
        curated_html += f"""
        <div style="background-color:#fff3e0; padding:15px; margin-bottom:15px; border-radius:8px; box-shadow:0 2px 5px rgba(0,0,0,0.1);">
            <h3 style="margin:0; color:#e65100;">{link.get('title','')}</h3>
            <p style="margin:5px 0 10px 0; color:#5d4037;">{link.get('summary','')} ({link.get('source','')})</p>
            <a href="{link.get('link','#')}" style="display:inline-block; padding:8px 15px; background-color:#fb8c00; color:white; text-decoration:none; border-radius:4px;">Read More</a>
        </div>
        """

    # Summaries HTML
    summaries_html = ""
    for s in summaries:
        topic = s.get("topic", "")
        blurb = s.get("blurb", "")
        summaries_html += f"""
        <div style="margin-bottom:15px;">
            <h3 style="color:#bf360c;">{topic}</h3>
            <p>{blurb}</p>
        </div>
        """

    # Trends HTML (keep existing warm block style)
    trends_html = ""
    for t in trends:
        trends_html += f"""
        <div style="background-color:#fff3e0; padding:15px; margin-bottom:15px; border-radius:8px; box-shadow:0 2px 5px rgba(0,0,0,0.1);">
            <h3 style="margin:0; color:#e65100;">{t.get('title','')}</h3>
            <p style="margin:5px 0 10px 0; color:#5d4037;">{t.get('explainer','')}</p>
            <a href="{t.get('link','#')}" style="display:inline-block; padding:8px 15px; background-color:#fb8c00; color:white; text-decoration:none; border-radius:4px;">Read More</a>
        </div>
        """

    html_content = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: 'Arial', sans-serif;
                background-color: #fff8f0;
                color: #4e342e;
                line-height: 1.6;
                padding: 20px;
            }}
            h1 {{
                color: #bf360c;
                text-align: center;
            }}
            h2 {{
                color: #e64a19;
                border-bottom: 2px solid #ffccbc;
                padding-bottom: 5px;
            }}
            p {{
                margin-bottom: 15px;
            }}
            .section {{
                margin-bottom: 30px;
            }}
            .newsletter-logo {{
                display: block;
                margin: 0 auto 20px auto;
                max-width: 150px;
            }}
        </style>
    </head>
    <body>
        {f'<img src="{logo_url}" class="newsletter-logo">' if logo_url else ''}
        <div class="section">
            <h2>Intro</h2>
            <p>{intro}</p>
        </div>

        <div class="section">
            <h2>Curated Links</h2>
            {curated_html}
        </div>

        <div class="section">
            <h2>Summaries</h2>
            {summaries_html}
        </div>

        <div class="section">
            <h2>Commentary</h2>
            <p>{commentary}</p>
        </div>

        <div class="section">
            <h2>Trends to Watch</h2>
            {trends_html}
        </div>
    </body>
    </html>
    """

    return html_content