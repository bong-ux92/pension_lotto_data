import requests
from bs4 import BeautifulSoup
import json
import os

def get_latest_pension_result():
    try:
        # 1. 주소와 헤더 설정 (브라우저인 척 속이기)
        url = "https://www.dhlottery.co.kr/gameResult.do?method=win720"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        }
        
        res = requests.get(url, headers=headers, timeout=10)
        res.encoding = 'utf-8' # 한글 깨짐 방지
        soup = BeautifulSoup(res.text, 'html.parser')

        # [디버깅용] 접속한 페이지 제목 출력
        print(f"📡 접속 페이지 제목: {soup.title.text if soup.title else '제목 없음'}")

        # 2. 회차 정보 추출 (더 넓은 범위로 탐색)
        # .win_result h4 strong이 안될 경우를 대비해 텍스트 검색 활용
        draw_no_element = soup.find('div', class_='win_result')
        if not draw_no_element:
            # 대안 선택자 시도
            draw_no_element = soup.select_one('.section_title h4 strong')
            
        if not draw_no_element:
            raise Exception("회차 영역(win_result)을 찾을 수 없습니다. 사이트 점검 중일 수 있습니다.")
            
        # "254회" 에서 숫자만 추출
        draw_no_text = draw_no_element.find('strong').text if draw_no_element.find('strong') else draw_no_element.text
        draw_no = int(''.join(filter(str.isdigit, draw_no_text)))
        
        # 3. 당첨 번호 추출
        win_area = soup.select('.win720_num .num span')
        if not win_area:
            raise Exception("당첨 번호 영역을 찾을 수 없습니다.")
            
        group = int(''.join(filter(str.isdigit, win_area[0].text)))
        numbers = [int(span.text.strip()) for span in win_area[1:7]]

        # 4. 보너스 번호 추출
        bonus_area = soup.select('.win720_num_bonus .num span')
        bonus_numbers = [int(span.text.strip()) for span in bonus_area]

        # 5. 데이터 조립 (유저님 앱 규격)
        data = {
            "drawNo": draw_no,
            "group": group,
            "numbers": numbers,
            "bonusNumbers": bonus_numbers
        }

        # 6. 파일 저장
        file_path = os.path.join(os.getcwd(), 'latest_win.json')
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ {draw_no}회차 데이터 생성 성공!")

    except Exception as e:
        print(f"❌ 에러 상세 발생: {e}")
        # 에러 발생 시 깃허브 액션도 실패로 표시
        exit(1)

if __name__ == "__main__":
    get_latest_pension_result()
