import json
import sys
import os

def create_json_manually():
    try:
        # GitHub Action에서 보낸 인자(Arguments) 받기
        draw_no = int(sys.argv[1])
        win_nums_str = sys.argv[2]
        bonus_nums_str = sys.argv[3]

        # 데이터 가공 (유저님 앱 규격)
        data = {
            "drawNo": draw_no,
            "group": int(win_nums_str[0]), # 첫 글자를 '조'로 사용
            "numbers": [int(n) for n in win_nums_str[1:]], # 나머지 6개
            "bonusNumbers": [int(n) for n in bonus_nums_str] # 보너스 6개
        }

        # 파일 저장
        with open('latest_win.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ {draw_no}회차 데이터가 수동으로 생성되었습니다!")

    except Exception as e:
        print(f"❌ 데이터 처리 중 에러: {e}")
        exit(1)

if __name__ == "__main__":
    create_json_manually()
