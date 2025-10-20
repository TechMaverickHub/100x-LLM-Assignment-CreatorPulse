import random

from app.sample.models import UserStyleSample


def style_examples_loader(user_id, max_samples=3, excerpt_length=250):
    """Fetch 20 most recent style samples for a user and pick 2–3 excerpts."""

    samples = UserStyleSample.objects.filter(user_id=user_id, is_active=True).order_by("-updated")

    if not samples:
        return [
            "Tone: warm, professional, concise. Style: clear summaries, actionable insights, and friendly editorial flow."
        ]

    all_text = " ".join([s.text for s in samples])
    paragraphs = [p.strip() for p in all_text.split("\n") if len(p.strip()) > 100]

    excerpts = random.sample(paragraphs, min(max_samples, len(paragraphs)))
    return excerpts
