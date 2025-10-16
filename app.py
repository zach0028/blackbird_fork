"""Minimal Flask application that wraps Blackbird in a web interface."""
from __future__ import annotations

import os
from typing import Any, Dict

from flask import Flask, render_template, request

from src.interface import (
    SearchOutcome,
    SearchServiceError,
    search_email,
    search_username,
)

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("BLACKBIRD_WEB_SECRET", "blackbird-web")


def _build_form_state(form: Dict[str, Any]) -> Dict[str, Any]:
    include_nsfw_value = form.get("include_nsfw")
    verbose_value = form.get("verbose")

    return {
        "search_type": form.get("search_type", "username"),
        "query": form.get("query", ""),
        "filter": form.get("filter", ""),
        "include_nsfw": include_nsfw_value == "on" if form else True,
        "verbose": verbose_value == "on" if form else False,
    }


@app.route("/", methods=["GET", "POST"])
def index():
    form_state = _build_form_state(request.form)
    outcome: SearchOutcome | None = None

    if request.method == "POST":
        query = form_state["query"].strip()
        search_type = form_state["search_type"]
        filter_text = form_state["filter"].strip() or None
        include_nsfw = form_state["include_nsfw"]
        verbose = form_state["verbose"]

        if not query:
            outcome = SearchOutcome(
                success=False,
                query=query,
                search_type=search_type,
                error="Please provide a username or email before launching the search.",
                log="",
            )
        else:
            try:
                if search_type == "email":
                    outcome = search_email(
                        query,
                        include_nsfw=include_nsfw,
                        verbose=verbose,
                    )
                else:
                    outcome = search_username(
                        query,
                        filter_text=filter_text,
                        include_nsfw=include_nsfw,
                        verbose=verbose,
                    )
            except SearchServiceError as exc:
                outcome = SearchOutcome(
                    success=False,
                    query=query,
                    search_type=search_type,
                    error=str(exc),
                    log="",
                )

    return render_template("index.html", form_state=form_state, outcome=outcome)


if __name__ == "__main__":  # pragma: no cover - manual execution helper
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
