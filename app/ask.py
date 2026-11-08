"""第1回: 素のLLMに質問するスクリプト。

使い方:
    uv run python -m app.ask "LoRAとは何ですか？"
    uv run python -m app.ask            # 質問を省略すると、講座に固有の質問をする
    uv run python -m app.ask --chat     # 対話モード

通常モードは、ツールも会話履歴も持たない「素の」1回呼び出し。
--chat では質問と回答を文字列の履歴に追加し、次の質問と一緒にモデルへ渡す。
講座に固有のことを聞くと、「分からない」と答えるか、一般論でもっともらしく答える
（講座の実際とは違う）ことを確かめよう。
（第3回で、用語集を検索できるエージェントにして改善する）
"""

import argparse

from google import genai
from google.genai import errors

from app.config import MODEL, api_error_message, get_api_key

# 講座に固有の質問。正しい答えは data/glossary.json の homework-levels にある
DEFAULT_QUESTION = "AIE2026の講座の宿題にある「3レベル」とは何ですか？"


def ask(question: str) -> str:
    client = genai.Client(api_key=get_api_key())
    response = client.models.generate_content(model=MODEL, contents=question)

    usage = response.usage_metadata
    if usage is None:
        print("[usage] 入力トークン数: 取得不可, 出力トークン数: 取得不可")
    else:
        print(
            f"[usage] 入力トークン数: {usage.prompt_token_count}, "
            f"出力トークン数: {usage.candidates_token_count}"
        )

    return response.text


def run_chat() -> None:
    chat = ""
    while True:
        try:
            question = input("質問（終了するには /quit）: ").strip()
        except EOFError:
            print()
            return
        if question == "/quit":
            return
        if not question:
            continue

        # chat += f"{question}\n"
        chat += f"ユーザー: {question}\n"
        prompt = f"{chat}"
        # prompt = f"{chat}\nこちらが以前の会話履歴です。最後の質問に回答してください。"
        answer = ask(prompt)
        print(answer)
        # chat += f"{answer}\n"
        chat += f"モデル: {answer}\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="素のLLMに質問する")
    parser.add_argument("--chat", action="store_true", help="質問を続ける対話モード")
    parser.add_argument("question", nargs="?")
    args = parser.parse_args()

    print(f"[model] {MODEL}")
    try:
        if args.chat:
            if args.question:
                parser.error("--chat と質問文は同時に指定できません")
            run_chat()
        else:
            question = args.question or DEFAULT_QUESTION
            print(f"[質問] {question}\n")
            print(ask(question))
    except errors.APIError as e:
        print(api_error_message(e.code, e.message))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
