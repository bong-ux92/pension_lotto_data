import requests
import json
import os
from bs4 import BeautifulSoup

def get_latest_pension_result():
    try:
        # 1. 먼저 '최신 회차 번호'가 몇 회인지 알아내기
        main_url = "https://www.dhlottery.co.kr/common.do?method=main"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
        
        main_res = requests.get(main_url, headers=headers)
        soup = BeautifulSoup(main_res.text, 'html.parser')
        
        # 메인 페이지에서 "연금복권 720+ 제 254회" 같은 텍스트에서 숫자만 추출
        # 이 부분은 메인 페이지의 아주 기초적인 부분이라 잘 안 바뀝니다.
        latest_draw_text = soup.find('strong', id='lottoDrwNo') # 로또 번호 기준일 수 있으니 720용으로 필터링
        # 만약 위 코드로 안 잡히면, 가장 안전하게 '날짜 기반' 혹은 '검색'으로 회차를 찾습니다.
        
        # [가장 확실한 방법] 결과 페이지에서 회차 숫자만 강제로 뽑아내기
        res = requests.get("https://www.dhlottery.co.kr/gameResult.do?method=win720", headers=headers)
        import re
        draw_no_match = re.search(r'<strong>(\d+)회</strong>', res.text)
        if not draw_no_match:
            raise Exception("회차 정보를 읽어오는 데 실패했습니다.")
        
        draw_no = int(draw_no_match.group(1))
        print(f"📡 확인된 최신 회차: {draw_no}회")

        # 2. [핵심] 공식 API를 호출하여 데이터 가져오기
        # 이 주소는 동행복권에서 공식적으로 데이터를 뿌려줄 때 쓰는 경로입니다.
        api_url = f"https://www.dhlottery.co.kr/common.do?method=get720Number&drwNo={draw_no}"
        api_res = requests.get(api_url, headers=headers)
        api_data = api_res.json()

        if api_data.get('returnValue') != 'success':
            raise Exception("API로부터 데이터를 가져오지 못했습니다.")

        # 3. 유저님의 앱 규격에 맞춰 데이터 정제 (Int 타입 변환)
        # API에서 오는 데이터: 'drwtNo1', 'drwtNo2' ... 'prizNo1' 등
        data = {
            "drawNo": draw_no,
            "group": int(api_data['prizNo1']), # 조 (1등)
            "numbers": [
                int(api_data['prizNo2']),
                int(api_data['prizNo3']),
                int(api_data['prizNo4']),
                int(api_data['prizNo5']),
                int(api_data['prizNo6']),
                int(api_data['prizNo7'])
            ],
            "bonusNumbers": [
                int(api_data['drwtNo1']),
                int(api_data['drwtNo2']),
                int(api_data['drwtNo3']),
                int(api_data['drwtNo4']),
                int(api_data['drwtNo5']),
                int(api_data['drwtNo6'])
            ]
        }

        # 4. JSON 파일 저장
        file_path = os.path.join(os.getcwd(), 'latest_win.json')
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ {draw_no}회차 데이터 저장 완료!")

    except Exception as e:
        print(f"❌ 에러 발생: {e}")
        exit(1)

if __name__ == "__main__":
    get_latest_pension_result()
