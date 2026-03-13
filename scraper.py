import requests
import json
import os
from datetime import date

def get_lottery_data():
    try:
        # 1. 유저님이 알려주신 306회차(2026-03-12)를 기준으로 정확히 계산
        base_date = date(2026, 3, 12) 
        base_round = 306
        today = date.today()
        
        # 기준일로부터 지난 주 수 계산
        diff_weeks = (today - base_date).days // 7
        draw_no = base_round + diff_weeks
        
        print(f"📅 기준일: {base_date} ({base_round}회)")
        print(f"🔢 현재 계산된 회차: {draw_no}회")

        # 2. 동행복권 API 호출
        api_url = f"https://www.dhlottery.co.kr/common.do?method=get720Number&drwNo={draw_no}"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        
        response = requests.get(api_url, headers=headers, timeout=10)
        result = response.json()

        if result.get('returnValue') == 'success':
            # 3. 데이터 정제 (Int 타입)
            data = {
                "drawNo": draw_no,
                "group": int(result['prizNo1']),
                "numbers": [
                    int(result['prizNo2']), int(result['prizNo3']), int(result['prizNo4']),
                    int(result['prizNo5']), int(result['prizNo6']), int(result['prizNo7'])
                ],
                "bonusNumbers": [
                    int(result['drwtNo1']), int(result['drwtNo2']), int(result['drwtNo3']),
                    int(result['drwtNo4']), int(result['drwtNo5']), int(result['drwtNo6'])
                ]
            }
            
            # JSON 저장
            file_path = os.path.join(os.getcwd(), 'latest_win.json')
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"✅ {draw_no}회차 데이터 생성 성공!")
        else:
            # 아직 데이터가 안 올라왔을 경우 (목요일 저녁 8시 직전 등)
            print(f"⚠️ {draw_no}회차 데이터가 아직 서버에 없습니다. 이전 회차를 유지하거나 잠시 후 시도하세요.")

    except Exception as e:
        print(f"❌ 에러 발생: {e}")
        exit(1)

if __name__ == "__main__":
    get_lottery_data()
