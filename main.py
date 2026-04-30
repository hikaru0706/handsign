import fitz  # PyMuPDF
import datetime

def sign_all_pages(input_pdf, output_pdf, font_file):
    # 1. PDFファイルを開く
    doc = fitz.open(input_pdf)
    
    # 2. サインの内容（今日の日付と名前）
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    weekday = today.weekday()  # 0=月, 4=金, 5=土, 6=日
    days_to_monday = {4: 3, 5: 2, 6: 1}
    if weekday in days_to_monday:  # 金土日 → 月曜
        monday = today + datetime.timedelta(days=days_to_monday[weekday])
        formatted_date = f"{monday.year}.{monday.month}.{monday.day}"
    else:
        formatted_date = f"{tomorrow.year}.{tomorrow.month}.{tomorrow.day}"
    
    signature_lines = [
        formatted_date,
        "Hikaru Miyashita"
    ]
    
    # 3. 挿入する基準位置と設定（税関告知書の署名欄を想定した目安）
    # ※ 実際の出力を見て微調整してください
    x_pos = 180             # 「X」マークの少し右あたりを想定
    y_pos = 365             # 署名欄の縦位置を想定
    font_size = 15          # 枠に収まるよう少し小さめに
    line_height = 10        # 行間も狭めに
    text_color = (0.1, 0.1, 0.5) 
    font_name = "handwriting"

    # 4. 全ページに対してループ処理を行う
    for page in doc:
        # ページごとにフォントを登録する必要があります
        page.insert_font(fontname=font_name, fontfile=font_file)
        
        # 1ページ内のサイン書き込み
        for index, line in enumerate(signature_lines):
            point = fitz.Point(x_pos, y_pos + (index * line_height))
            page.insert_text(
                point, 
                line, 
                fontname=font_name, 
                fontsize=font_size, 
                color=text_color
            )
    
    # 5. 保存して閉じる
    page_count = len(doc)
    doc.save(output_pdf)
    doc.close()

    # 処理したページ数を表示
    print(f"全 {page_count} ページの署名欄にサイン（{formatted_date}）を追加しました: {output_pdf}")

# 実行部分
if __name__ == "__main__":
    input_file = "document.pdf" # 元のPDFファイル名（必要に応じて変更）
    output_file = "document_signed.pdf"    # 出力されるPDFファイル名
    font = "GreatVibes-Regular.ttf"          # 用意した手書きフォントファイル名
    
    sign_all_pages(input_file, output_file, font)
