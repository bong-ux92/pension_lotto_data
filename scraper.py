import requests
from bs4 import BeautifulSoup
import json
import os

def get_latest_pension_result():
    try:
        url = "https://www.dhlottery.co.kr/gameResult.do?method=win720"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')

        # 데이터 추출 (데이터가 없으면 여기서 에러가 나도록 설계)
        draw_no_element = soup.select_one('.win_result h4 strong')
        if not draw_no_element:
            raise Exception("회차 정보를 찾을 수 없습니다. 사이트 구조를 확인하세요.")
            
        draw_no = int(draw_no_element.text.replace('회', '').strip())
        
        win_area = soup.select('.win720_num .num span')
        group = int(win_area[0].text.replace('조', '').strip())
        numbers = [int(span.text.strip()) for span in win_area[1:7]]

        bonus_area = soup.select('.win720_num_bonus .num span')
        bonus_numbers = [int(span.text.strip()) for span in bonus_area]

        data = {
            "drawNo": draw_no,
            "group": group,
            "numbers": numbers,
            "bonusNumbers": bonus_numbers
        }

        # 💡 파일을 현재 폴더에 확실히 생성
        file_path = os.path.join(os.getcwd(), 'latest_win.json')
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 파일 생성 완료: {file_path}")

    except Exception as e:
        print(f"❌ 에러 상세 발생: {e}")
        # 💡 에러가 나면 억지로 프로세스를 종료시켜서 깃허브가 알게 합니다.
        exit(1) 

if __name__ == "__main__":
    get_latest_pension_result()
