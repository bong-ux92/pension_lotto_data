import json
import sys
import os

def update_lottery_data():
    try:
        # 1. 입력값 받기
        draw_no = int(sys.argv[1])
        win_nums_str = sys.argv[2]
        bonus_nums_str = sys.argv[3]

        new_data = {
            "drawNo": draw_no,
            "group": int(win_nums_str[0]),
            "numbers": [int(n) for n in win_nums_str[1:]],
            "bonusNumbers": [int(n) for n in bonus_nums_str]
        }

        # 2. 최신본(latest_win.json) 저장 - (홈 화면용)
        with open('latest_win.json', 'w', encoding='utf-8') as f:
            json.dump(new_data, f, ensure_ascii=False, indent=2)

        # 3. 누적본(history.json) 관리 - (과거 기록 검색용)
        history_file = 'history.json'
        if os.path.exists(history_file):
            with open(history_file, 'r', encoding='utf-8') as f:
                history = json.load(f)
        else:
            history = []

        # 중복 체크: 이미 있는 회차면 업데이트, 없으면 추가
        exists = False
        for i, item in enumerate(history):
            if item['drawNo'] == draw_no:
                history[i] = new_data
                exists = True
                break
        
        if not exists:
            history.append(new_data)
        
        # 회차 순서대로 정렬 (최신순)
        history.sort(key=lambda x: x['drawNo'], reverse=True)

        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
        
        print(f"✅ {draw_no}회차 최신본 및 히스토리 업데이트 완료!")

    except Exception as e:
        print(f"❌ 데이터 처리 중 에러: {e}")
        exit(1)

if __name__ == "__main__":
    update_lottery_data()
