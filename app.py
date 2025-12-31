import argparse
from typing import Optional

from flask import Flask, render_template, request

from faq_bot import FAQItem, find_best_match, load_faq


def create_app() -> Flask:
    app = Flask(__name__)

    # 事前にFAQを読み込んでメモリに保持（小規模データ想定）
    app.config["FAQ_ITEMS"] = load_faq()

    @app.route("/", methods=["GET", "POST"])
    def index():
        faq_items = app.config.get("FAQ_ITEMS", [])
        user_question = ""
        best_match: Optional[FAQItem] = None
        error: Optional[str] = None

        if request.method == "POST":
            user_question = request.form.get("question", "").strip()
            if not user_question:
                error = "質問を入力してください。"
            else:
                try:
                    best_match = find_best_match(user_question, faq_items)
                except Exception as exc:  # pragma: no cover - defensive
                    error = f"検索中にエラーが発生しました: {exc}"

        return render_template(
            "index.html", question=user_question, best_match=best_match, error=error
        )

    return app


app = create_app()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the FAQ Flask app")
    parser.add_argument(
        "--port",
        type=int,
        default=5000,
        help="Port number for the Flask development server (default: 5000)",
    )
    args = parser.parse_args()
    app.run(debug=False, port=args.port)
