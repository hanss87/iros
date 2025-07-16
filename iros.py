import requests
import json
import urllib3

# SSL 경고 메시지를 비활성화합니다.
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def search_iros_registration(registration_number: str):
    """
    대한민국 법원 인터넷등기소(iros.go.kr)에 등기번호로 정보를 요청하고 결과를 반환합니다.
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

    payload = {
        "websquare_param": { "move_cls": "A", "issue_rsvre_yn": "N", "regt_no": "0", "extn_regt_no": "", "corp_cls_cd": "0", "crgbk_stcd": "0", "hdbrc_cls": "0", "srch_cls": "PC03", "swrd": registration_number, "master_no": "", "crg_no": "", "bpay_obj_acnt": "", "login_yn": "", "crg_type_sel_yn": "", "enr_no_sel_yn": "", "read_date": "", "read_no": "", "svc_cls": "", "bpay_cls": "", "pageIndex": "", "prev_yn": "", "calg_scrn": "", "eras_yn": "", "eras_conm": "", "eras_rom_conm": "", "re_srch_yn": "", "appl_tcnt": "", "dg_suit_yn": "", "dgcf_issue_cls_cd": "" }
    }

    try:
        # SSL 인증서 검증을 건너뛰도록 verify=False 옵션을 추가합니다.
        response = requests.post(url, headers=headers, json=payload, verify=False)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"오류가 발생했습니다: {e}")
        return None

# --- 프로그램 실행 부분 ---
if __name__ == "__main__":
    target_registration_number = "134511-0072144"#"110111-1258220"
    print(f"등기번호 '{target_registration_number}' 조회를 시작합니다...")
    result_data = search_iros_registration(target_registration_number)

    if result_data:
        print("\n✅ 요청 성공!")
        print(json.dumps(result_data, indent=2, ensure_ascii=False))
    else:
        print("\n❌ 요청 실패.")