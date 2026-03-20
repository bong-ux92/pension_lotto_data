import json
import os
# import requests  # 유저님이 쓰시는 크롤링 라이브러리 추가

# 💡 유저님의 JSON 파일이 있는 정확한 경로
JSON_FILE_PATH = 'assets/data/final_pension_history.json'

def fetch_latest_pension_data():
    # ========================================================
    # 🚀 여기에 유저님의 [데이터 얻어오는 코드]를 넣어주세요!
    # ========================================================
    # 예시: 동행복권 사이트를 긁어서 딕셔너리로 만듭니다.
    
    '''
    # 유저님의 코드가 실행된 후, 이런 형태의 딕셔너리가 반환되어야 합니다.
    new_data = {
        "drawNo": 307,
        "drawDate": "2024-04-18",
        "group": 1,
        "numbers": [1, 2, 3, 4, 5, 6],
        "bonusNumbers": [1, 2, 3, 4, 5, 6]
    }
    return new_data
    '''
    pass 

def update_json():
    print("⏳ 연금복권 업데이트 로봇 가동 시작...")

    # 1. 기존 JSON 파일 읽어오기
    if os.path.exists(JSON_FILE_PATH):
        with open(JSON_FILE_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        print("❌ 기존 JSON 파일을 찾을 수 없습니다!")
        data = []

    # 2. 새로운 1개 회차 데이터 가져오기
    new_data = fetch_latest_pension_data()
    if not new_data:
        print("❌ 새로운 데이터를 가져오지 못했습니다. (추첨 전이거나 사이트 에러)")
        return

    # 3. 🛡️ 중복 방어막 (이미 307회가 저장되어 있다면 스킵!)
    existing_rounds = [item['drawNo'] for item in data]
    if new_data['drawNo'] in existing_rounds:
        print(f"✅ 이미 제 {new_data['drawNo']}회 데이터가 존재합니다. 쿨하게 종료합니다.")
        return

    # 4. 새 데이터 추가 및 최신순(내림차순)으로 정렬!
    data.append(new_data)
    data.sort(key=lambda x: x['drawNo'], reverse=True)

    # 5. 기존 파일에 덮어쓰기 (깔끔하게 들여쓰기 2칸)
    with open(JSON_FILE_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"🎉 제 {new_data['drawNo']}회 연금복권 데이터가 성공적으로 꽂혔습니다!")

if __name__ == "__main__":
    update_json()
