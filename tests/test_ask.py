import builtins
import importlib


def test_chat_accumulates_questions_and_answers(monkeypatch, capsys):
    ask_module = importlib.import_module("app.ask")
    user_inputs = iter(["最初の質問", "続きの質問", "/quit"])
    answers = iter(["最初の回答", "続きの回答"])
    prompts = []

    monkeypatch.setattr(builtins, "input", lambda _: next(user_inputs))
    monkeypatch.setattr(
        ask_module,
        "ask",
        lambda prompt: prompts.append(prompt) or next(answers),
    )

    ask_module.run_chat()

    assert prompts[0].endswith(
        "こちらが以前の会話履歴です。最後の質問に回答してください。"
    )
    assert "ユーザー: 最初の質問" in prompts[0]
    assert "アシスタント: 最初の回答" not in prompts[0]
    assert "ユーザー: 最初の質問" in prompts[1]
    assert "アシスタント: 最初の回答" in prompts[1]
    assert "ユーザー: 続きの質問" in prompts[1]
    assert prompts[1].endswith(
        "こちらが以前の会話履歴です。最後の質問に回答してください。"
    )
    assert "続きの回答" in capsys.readouterr().out
