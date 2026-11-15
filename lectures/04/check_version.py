import os
from google import genai
from dotenv import load_dotenv
import sys

# .envファイルから環境変数を読み込む
load_dotenv()

# APIキーを設定
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("エラー: GEMINI_API_KEYが設定されていません。", file=sys.stderr)
    sys.exit(1)

print("利用可能なモデルの一覧を取得します...\n")

with genai.Client(api_key=api_key) as client:
    # 利用可能なモデルをリストアップ
    for model in client.models.list():
        # 'generateContent'（文章生成）が可能なモデルのみを表示する
        if "generateContent" in (model.supported_actions or []):
            print(model.name)