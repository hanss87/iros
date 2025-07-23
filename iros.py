import requests
import argparse
import sys
import json
import certifi

def search_iros_registration(registration_number: str):
    """
    대한민국 법원 인터넷등기소(iros.go.kr)에 등기번호로 정보를 요청하고 결과를 반환합니다.

    Args:
        registration_number (str): 조회할 법인 등기번호.

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

    payload = {
        "websquare_param": { "move_cls": "A", "issue_rsvre_yn": "N", "regt_no": "0", "extn_regt_no": "", "corp_cls_cd": "0", "crgbk_stcd": "0", "hdbrc_cls": "0", "srch_cls": "PC03", "swrd": registration_number, "master_no": "", "crg_no": "", "bpay_obj_acnt": "", "login_yn": "", "crg_type_sel_yn": "", "enr_no_sel_yn": "", "read_date": "", "read_no": "", "svc_cls": "", "bpay_cls": "", "pageIndex": "", "prev_yn": "", "calg_scrn": "", "eras_yn": "", "eras_conm": "", "eras_rom_conm": "", "re_srch_yn": "", "appl_tcnt": "", "dg_suit_yn": "", "dgcf_issue_cls_cd": "" }
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


def main():
    """메인 실행 함수"""
    # Windows 터미널(cmd, PowerShell)에서 유니코드 문자가 깨지는 현상을 방지합니다.
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding='utf-8')

    parser = argparse.ArgumentParser(description="인터넷 등기소에서 법인 등록번호를 조회합니다.")
    parser.add_argument("registration_number", help="조회할 법인 등기번호")
    args = parser.parse_args()

    print(f"등기번호 '{args.registration_number}' 조회를 시작합니다...")
    
    try:
        result_data = search_iros_registration(args.registration_number)
        print("\n✅ 요청 성공!")
        print(json.dumps(result_data, indent=2, ensure_ascii=False))
    except (requests.exceptions.RequestException, json.JSONDecodeError):
        print("\n❌ 요청 실패.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
