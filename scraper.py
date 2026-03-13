import requests
from bs4 import BeautifulSoup
import json

def get_latest_pension_result():
    try:
        url = "https://www.dhlottery.co.kr/gameResult.do?method=win720"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')

        # 1. 회차 정보 추출 (String -> Int 변환)
        draw_no = int(soup.select_one('.win_result h4 strong').text.replace('회', '').strip())
        
        # 2. 1등 당첨 번호 추출
        win_area = soup.select('.win720_num .num span')
        # '조' 정보 (String -> Int 변환)
        group = int(win_area[0].text.replace('조', '').strip())
        # 6자리 번호 (String -> Int 리스트 변환)
        numbers = [int(span.text.strip()) for span in win_area[1:7]]

        # 3. 보너스 번호 추출 (String -> Int 리스트 변환)
        bonus_area = soup.select('.win720_num_bonus .num span')
        bonus_numbers = [int(span.text.strip()) for span in bonus_area]

        # 4. 유저님의 앱 규격에 완벽히 맞춘 데이터 구조
        data = {
            "drawNo": draw_no,
            "group": group,
            "numbers": numbers,
            "bonusNumbers": bonus_numbers
        }

        # 5. JSON 파일로 저장
        with open('latest_win.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ {draw_no}회차 데이터 생성 완료 (규격 일치)")

    except Exception as e:
        print(f"❌ 에러 발생: {e}")

if __name__ == "__main__":
    get_latest_pension_result()
