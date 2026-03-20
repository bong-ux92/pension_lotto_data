import os
import json
import time
import requests
from datetime import date

# 💡 파일이 저장될 정확한 경로 세팅
JSON_FILE_PATH = 'assets/data/pension_lucky_stores.json'
META_FILE_PATH = 'assets/data/last_lucky_draw.txt'

def get_latest_draw_no():
    """오늘 날짜를 기준으로 가장 최신 연금복권 회차를 자동 계산합니다."""
    # 연금복권 720+ 1회차 추첨일: 2020년 5월 7일
    first_draw_date = date(2020, 5, 7)
    today = date.today()
    days_diff = (today - first_draw_date).days
    current_draw = (days_diff // 7) + 1
    return current_draw

def fetch_stores_for_draw(draw_no):
    """특정 1개 회차의 명당 데이터를 긁어와서 '서랍장' 형태로 예쁘게 정리합니다."""
    print(f"🎯 [수집 시작] 제 {draw_no}회차 1등, 2등, 보너스 명당을 찾습니다!")
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    # 💡 307회차 서랍장 생성! (1등, 2등, 보너스를 따로따로 보관)
    draw_data = {
        "drawNo": draw_no,
        "1st_stores": [],
        "2nd_stores": [],
        "bonus_stores": []
    }
    
    # API 요청 코드와 JSON 서랍장 키를 매핑합니다.
    ranks_to_fetch = {
        '1': '1st_stores',
        '2': '2nd_stores',
        'bonus': 'bonus_stores'
    }

    for rank_code, list_key in ranks_to_fetch.items():
        url = "https://www.dhlottery.co.kr/wnprchsplcsrch/selectPtWnShp.do"
        params = {
            'srchWnShpRnk': rank_code,
            'srchLtEpsd': draw_no,
            'srchShpLctn': ''
        }
        
        try:
            response = requests.get(url, params=params, headers=headers, timeout=10)
            data = response.json()
            store_list = data.get('data', {}).get('list', [])
            
            for item in store_list:
                name = item.get('shpNm')
                address = item.get('shpAddr')
                lat = item.get('shpLat')
                lng = item.get('shpLot')
                
                # 🛡️ 인터넷 구매나 위치 정보 없는 데이터 필터링
                if not lat or not lng or lat == 0 or lng == 0 or "인터넷" in name:
                    continue
                
                # 💡 해당 등수 서랍장에 명당 정보를 쏙! 넣어줍니다.
                draw_data[list_key].append({
                    "name": name,
                    "address": address,
                    "lat": float(lat),
                    "lng": float(lng)
                })
                
        except Exception as e:
            print(f"  ❌ [{draw_no}회차 - {rank_code}등] 에러 발생: {e}")
            
        time.sleep(0.5) # 서버 보호 휴식
        
    return draw_data

def update_lucky_stores():
    print("=" * 60)
    print("⏳ [5000만 국민앱] 연금복권 명당 리스트(회차별) 업데이트 엔진 가동...")
    print("=" * 60)

    latest_draw = get_latest_draw_no()
    
    # 🛡️ 중복 업데이트 방어
    last_draw = 0
    if os.path.exists(META_FILE_PATH):
        with open(META_FILE_PATH, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if content.isdigit():
                last_draw = int(content)

    if latest_draw <= last_draw:
        print(f"✅ 이미 제 {latest_draw}회차 데이터가 최신화되어 있습니다. 안전하게 종료합니다.")
        return

    # 기존 JSON 데이터 불러오기 (리스트 형태)
    existing_data = []
    if os.path.exists(JSON_FILE_PATH):
        with open(JSON_FILE_PATH, 'r', encoding='utf-8') as f:
            try:
                existing_data = json.load(f)
            except json.JSONDecodeError:
                existing_data = []

    # 🚀 이번 주 최신 명당 데이터 서랍장 통째로 긁어오기!
    new_draw_data = fetch_stores_for_draw(latest_draw)

    # 🛡️ 이미 리스트에 이번 회차 서랍장이 있는지 혹시 몰라 한 번 더 검사
    existing_rounds = [item.get('drawNo') for item in existing_data]
    if new_draw_data['drawNo'] in existing_rounds:
        print(f"✅ JSON 내부에 이미 제 {new_draw_data['drawNo']}회 데이터가 존재합니다.")
        return

    # 💡 기존 데이터 리스트 맨 앞에 새 회차 서랍장을 추가합니다! (최신순 정렬)
    existing_data.append(new_draw_data)
    existing_data.sort(key=lambda x: x['drawNo'], reverse=True)

    # JSON 파일로 저장
    os.makedirs(os.path.dirname(JSON_FILE_PATH), exist_ok=True)
    with open(JSON_FILE_PATH, 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=2)

    # 완료 기록 남기기
    with open(META_FILE_PATH, 'w', encoding='utf-8') as f:
        f.write(str(latest_draw))

    print("\n" + "=" * 60)
    print(f"🎉 대성공! 제 {latest_draw}회차 명당 서랍장 반영 완료!")
    print("=" * 60)

if __name__ == "__main__":
    update_lucky_stores()
