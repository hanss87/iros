import json
from flask import Flask, render_template, request

# Flask 애플리케이션 생성
app = Flask(__name__)

# 1. 사용자로부터 제공받은 원본 데이터
# HTTP 응답에서 순수 JSON 데이터만 추출하여 저장
raw_json_data = """
{
    "searchErrorFlag": "",
    "crgSrchRsltList": [
        {"rmasterregt_ver": "01", "regt_no": "1101", "crgbk_stcd": "12300", "conm": "한국토지신탁", "rmastercorp_cd_ver": "01", "rmasteruse_cls": "13601", "master_no": 89825, "corp_cls_cd": "11", "tb_re614corp_cd": "11", "rsanghos_malso": "N", "crg_no": "125822", "hdbrc_cls": "1", "drokno": "110111-1258220", "juso": "서울특별시 강남구 테헤란로 137(역삼동)", "regt_name": "서울중앙지방법원 등기국", "rom_conm": " ", "crgbk_stcd_name": "살아있는 등기", "corp_cls_cd_name": "주식회사", "eras_yn": "N"},
        {"rmasterregt_ver": "01", "regt_no": "1412", "crgbk_stcd": "12344", "conm": "한국토지신탁", "rmastercorp_cd_ver": "01", "rmasteruse_cls": "13602", "master_no": 955569, "corp_cls_cd": "11", "tb_re614corp_cd": "11", "rsanghos_malso": "N", "crg_no": "003778", "hdbrc_cls": "2", "drokno": "110111-1258220", "juso": "서울특별시 강남구 역삼동 702-2", "regt_name": "춘천지방법원 원주지원 등기과", "rom_conm": " ", "crgbk_stcd_name": "기타폐쇄", "corp_cls_cd_name": "주식회사", "eras_yn": "N"},
        {"rmasterregt_ver": "01", "regt_no": "1615", "crgbk_stcd": "12344", "conm": "한국토지신탁", "rmastercorp_cd_ver": "01", "rmasteruse_cls": "13602", "master_no": 582419, "corp_cls_cd": "11", "tb_re614corp_cd": "11", "rsanghos_malso": "N", "crg_no": "005031", "hdbrc_cls": "2", "drokno": "110111-1258220", "juso": "서울 강남구 삼성동 144-25", "regt_name": "대전지방법원 천안지원 등기과", "rom_conm": " ", "crgbk_stcd_name": "기타폐쇄", "corp_cls_cd_name": "주식회사", "eras_yn": "N"},
        {"rmasterregt_ver": "01", "regt_no": "1701", "crgbk_stcd": "12344", "conm": "한국토지신탁", "rmastercorp_cd_ver": "01", "rmasteruse_cls": "13602", "master_no": 764859, "corp_cls_cd": "11", "tb_re614corp_cd": "11", "rsanghos_malso": "N", "crg_no": "026488", "hdbrc_cls": "2", "drokno": "110111-1258220", "juso": "서울 강남구 삼성동 144-25", "regt_name": "대구지방법원 등기국", "rom_conm": " ", "crgbk_stcd_name": "기타폐쇄", "corp_cls_cd_name": "주식회사", "eras_yn": "N"},
        {"rmasterregt_ver": "01", "regt_no": "1801", "crgbk_stcd": "12344", "conm": "한국토지신탁", "rmastercorp_cd_ver": "01", "rmasteruse_cls": "13602", "master_no": 252827, "corp_cls_cd": "11", "tb_re614corp_cd": "11", "rsanghos_malso": "N", "crg_no": "022544", "hdbrc_cls": "2", "drokno": "110111-1258220", "juso": "서울특별시 강남구 역삼동 702-2", "regt_name": "부산지방법원 등기국", "rom_conm": " ", "crgbk_stcd_name": "기타폐쇄", "corp_cls_cd_name": "주식회사", "eras_yn": "N"},
        {"rmasterregt_ver": "01", "regt_no": "2001", "crgbk_stcd": "12344", "conm": "한국토지신탁", "rmastercorp_cd_ver": "01", "rmasteruse_cls": "13602", "master_no": 233131, "corp_cls_cd": "11", "tb_re614corp_cd": "11", "rsanghos_malso": "N", "crg_no": "007309", "hdbrc_cls": "2", "drokno": "110111-1258220", "juso": "서울특별시 강남구 역삼동 702-2", "regt_name": "광주지방법원 등기국", "rom_conm": " ", "crgbk_stcd_name": "기타폐쇄", "corp_cls_cd_name": "주식회사", "eras_yn": "N"}
    ]
}
"""
# 2. JSON 데이터를 파이썬 딕셔너리로 변환
corporate_data = json.loads(raw_json_data)
all_records = corporate_data.get('crgSrchRsltList', [])

# 3. 웹페이지 라우팅 및 검색 로직
@app.route('/', methods=['GET', 'POST'])
def search_page():
    results = None
    query = ""
    if request.method == 'POST':
        # 사용자가 입력한 검색어를 가져옴
        query = request.form.get('query', '').strip()
        if query:
            # 전체 데이터에서 법인등록번호(drokno)가 일치하는 모든 기록을 찾음
            results = [record for record in all_records if record.get('drokno') == query]
            
            # 본점/지점 구분 코드(hdbrc_cls)를 한글로 변환하여 추가
            for r in results:
                if r.get('hdbrc_cls') == '1':
                    r['hdbrc_cls_name'] = '본점'
                elif r.get('hdbrc_cls') == '2':
                    r['hdbrc_cls_name'] = '지점'
                else:
                    r['hdbrc_cls_name'] = '기타'

    # index.html 템플릿을 렌더링하면서 검색 결과와 검색어를 전달
    return render_template('index.html', results=results, query=query)

# 4. 서버 실행
if __name__ == '__main__':
    # 디버그 모드로 실행 (개발 중에 유용)
    app.run(debug=True)