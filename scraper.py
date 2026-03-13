import requests
import json
import os
from datetime import date

def get_lottery_data():
    try:
        # 1. 날짜 기반 회차 계산
        base_date = date(2026, 3, 12) 
        base_round = 306
        today = date.today()
        diff_weeks = (today - base_date).days // 7
        draw_no = base_round + diff_weeks
        
        # 2. 풀헤더 설정 (서버를 완벽하게 속이기)
        url = f"https://www.dhlottery.co.kr/common.do?method=get720Number&drwNo={draw_no}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Referer': 'https://www.dhlottery.co.kr/gameResult.do?method=win720',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest'
        }
        
        # 3. 요청 및 응답 확인
        session = requests.Session()
        # 메인 페이지 한 번 들렀다가 쿠키 구워오기
        session.get("https://www.dhlottery.co.kr/", headers=headers, timeout=5)
        response = session.get(url, headers=headers, timeout=10)

        # 💡 [중요] 응답이 JSON인지 확인
        if response.status_code == 200:
            try:
                result = response.json()
            except:
                print("⚠️ 서버가 JSON이 아닌 HTML을 보냈습니다. 차단된 것 같습니다.")
                print(f"서버 응답 앞부분: {response.text[:100]}")
                exit(1)

            if result.get('returnValue') == 'success':
                data = {
                    "drawNo": draw_no,
                    "group": int(result['prizNo1']),
                    "numbers": [int(result[f'prizNo{i}']) for i in range(2, 8)],
                    "bonusNumbers": [int(result[f'drwtNo{i}']) for i in range(1, 7)]
                }
                with open('latest_win.json', 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                print(f"✅ {draw_no}회차 데이터 생성 성공!")
            else:
                print(f"⚠️ {draw_no}회 데이터가 아직 없습니다.")
        else:
            print(f"❌ 접속 실패 (상태 코드: {response.status_code})")

    except Exception as e:
        print(f"❌ 에러 상세 발생: {e}")
        exit(1)

if __name__ == "__main__":
    get_lottery_data()
