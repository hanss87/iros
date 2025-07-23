import requests
import sys
import json
import certifi
import re
from flask import Flask, render_template, request

app = Flask(__name__)

def search_iros(query: str, search_by: str = "number"):
    """
    대한민국 법원 인터넷등기소(iros.go.kr)에 등기번호 또는 법인명으로 정보를 요청하고 결과를 반환합니다.

    Args:
        query (str): 조회할 법인 등기번호 또는 법인명.
        search_by (str): 'number' (등기번호) 또는 'name' (법인명). 기본값은 'number'.

    Returns:
        dict: 요청 성공 시 JSON 응답 데이터.
        None: 요청 실패 시.
    
    Raises:
        requests.exceptions.RequestException: 네트워크 오류, HTTP 오류 등 요청 관련 예외 발생 시.
        json.JSONDecodeError: 응답 내용을 JSON으로 파싱할 수 없을 때.
    """
    url = "https://www.iros.go.kr/biz/Pc20ViaCrgSrchCtrl/retrieveDroknoSrchRslt.do"
    
    headers = {
        "Accept": "application/json",
        "Accept-Language": "ko-KR,ko;q=0.6",
        "Content-Type": "application/json; charset=UTF-8",
        "Origin": "https://www.iros.go.kr",
        "Referer": "https://www.iros.go.kr/index.jsp",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
    }

    # Payload 초기화
    regt_no = "0"
    extn_regt_no = ""
    swrd = query
    # PC01: 상호, PC03: 등록번호
    search_class = "PC03" if search_by == "number" else "PC01"

    # 검색 유형에 따라 payload 재구성
    if search_by == "number":
        parts = query.split('-')
        if len(parts) == 2:
            regt_no = parts[0]
            extn_regt_no = parts[1]
            swrd = "" # 번호 검색 시 swrd는 사용하지 않음
    
    payload = {
        "websquare_param": { "move_cls": "A", "issue_rsvre_yn": "N", "regt_no": regt_no, "extn_regt_no": extn_regt_no, "corp_cls_cd": "0", "crgbk_stcd": "0", "hdbrc_cls": "0", "srch_cls": search_class, "swrd": swrd, "master_no": "", "crg_no": "", "bpay_obj_acnt": "", "login_yn": "", "crg_type_sel_yn": "", "enr_no_sel_yn": "", "read_date": "", "read_no": "", "svc_cls": "", "bpay_cls": "", "pageIndex": "", "prev_yn": "", "calg_scrn": "", "eras_yn": "", "eras_conm": "", "eras_rom_conm": "", "re_srch_yn": "", "appl_tcnt": "", "dg_suit_yn": "", "dgcf_issue_cls_cd": "" }
    }

    try:
        response = requests.post(url, headers=headers, json=payload, verify=certifi.where())
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"오류가 발생했습니다: {e}", file=sys.stderr)
        raise
    except json.JSONDecodeError as e:
        print(f"JSON 파싱 오류: {e}", file=sys.stderr)
        print(f"받은 응답 내용: {response.text}", file=sys.stderr)
        raise

@app.route("/", methods=["GET", "POST"])
def index():
    """메인 페이지 및 검색 결과 처리"""
    results = None
    query = ""
    if request.method == "POST":
        query = request.form.get("query", "").strip()
        if query:
            try:
                # 법인등록번호 형식(숫자6-숫자7) 및 총 14자리(하이픈 포함)인지 확인
                if re.match(r"^\d{6}-\d{7}$", query) and len(query) == 14:
                    search_by = "number"
                else:
                    search_by = "name"
                search_result = search_iros(query, search_by)
                results = search_result.get("data", {}).get("list", [])
            except (requests.exceptions.RequestException, json.JSONDecodeError):
                results = [] # 오류 발생 시 빈 리스트를 전달하여 템플릿에 메시지 표시

    return render_template("index.html", results=results, query=query)

if __name__ == "__main__":
    # 외부에서 접근 가능하도록 host='0.0.0.0'으로 설정합니다.
    app.run(host="0.0.0.0", port=5000, debug=True)
