# Humanize and layout checklist - full_paper_rev200_codex

- [PASS] 10페이지 이내: Word/PDF 렌더 기준 9매.
- [PASS] 마지막 페이지 상태: page 9는 참고문헌 [8]~[22]를 포함하며 빈 trailing page가 아님.
- [PASS] Abstract 15줄 이내: Abstract는 한 단락으로 유지하고, scope 문장은 짧게 유지.
- [PASS] "본 연구는" 반복 없음: DOCX 텍스트 스캔에서 `본 연구는` 반복 패턴 없음.
- [PASS] 한 문장에 metric 과다 나열 없음: Known, Unknown, object-id, FCM-PM 결과를 각각 분리해 서술.
- [PASS] validation scope 유지: field validation, field review, generated development, controlled synthetic benchmark 구분 유지.
- [PASS] object-id overclaim 없음: object-id map은 generated-chip development이며, detector를 이긴 작은 모델이 아니라 fixed chip coordinate 기반 문제 전환으로 설명.
- [PASS] FCM-PM production claim 없음: FCM-PM은 controlled synthetic benchmark로 유지.
- [PASS] Unknown 13→7 precision 오해 없음: Unknown 13→7은 field review candidate compression이며 classifier precision이 아님.
- [PASS] 123억 certified 표현 유지: internally certified quantified contribution 및 메모리제조기술센터 내부 성과 인정 기준 표현 유지.
- [PASS] Table 2 layout: caption과 table body를 축약했고, rendered page 4에서 컬럼 침범/겹침 없음.
- [PASS] Table 3 layout: DOCX에서 table keep-together를 적용해 rendered page 6 상단에 통째로 배치, page split 없음.
- [PASS] Table style: DOCX tables are real Word tables; raw markdown table syntax does not appear in DOCX text scan.
- [PASS] caption 위치: table captions are above tables and figure captions are below figures in rendered pages.
- [PASS] Figure 6/7 readability: rendered pages에서 A+B, A-only/B-only, Pair Mask, Whole 4-bit shape is scored 계열 label이 확인 가능.
- [PASS] 깨진 dash 없음: DOCX 텍스트 스캔에서 `—`, `–`, `‑`, `−` 문자가 검출되지 않음.
- [PASS] 깨진 공백/soft-hyphen 없음: `파 이프라인`, `해 야`, `확 인`, `single￾failure`, `micro￾F1`, `FCM￾PM`, `coordinate￾preserving`, U+00AD 패턴이 검출되지 않음.
- [PASS] 금지/위험 표현 없음: `P1`, `P2`, `Pipeline speed`, `candidate update`, `LLM agent`, `Known·Unknown` 패턴이 DOCX 스캔에서 검출되지 않음.
- [PASS] 새 수치 추가 없음: rev200은 rev199의 claim/scope를 유지하고 Table 2/3 caption 및 row text를 압축한 layout polish revision.

Notes:
- `tools\verify_full_paper_package.py`는 legacy expected figure/table/reference count와 old Abstract-heading assumption 때문에 FAIL을 보고한다. 현재 rev200의 core checks는 A4, margins, header/footer, two columns, figure files, citation/reference consistency, hidden XML scan, PDF page count 9를 통과했다.
- `full_paper_rev200_codex.docx`는 Table 3 keep-together post-processing이 적용된 제출용 Word 파일이다. 빌더를 다시 돌리면 이 post-processing을 다시 적용해야 한다.
