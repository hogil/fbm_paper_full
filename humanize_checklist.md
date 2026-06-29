# Humanize and layout checklist - full_paper_rev203_codex

- [PASS] 10페이지 이내: Word/PDF 렌더 기준 9매.
- [PASS] 마지막 페이지 상태: page 9는 참고문헌을 포함하며 빈 trailing page가 아님.
- [PASS] Abstract 15줄 이내: Abstract는 한 단락으로 유지하고, scope 문장은 짧게 유지.
- [PASS] "본 연구는" 반복 없음: DOCX 텍스트 스캔에서 `본 연구는` 반복 패턴 없음.
- [PASS] 한 문장에 metric 과다 나열 없음: Known, Unknown, object-id, FCM-PM 결과를 각각 분리해 서술.
- [PASS] validation scope 유지: field validation, field review, generated development, controlled synthetic benchmark 구분 유지.
- [PASS] object-id overclaim 없음: object-id map은 generated-chip development이며, detector를 이긴 작은 모델이 아니라 fixed chip coordinate 기반 문제 전환으로 설명.
- [PASS] FCM-PM production claim 없음: FCM-PM은 controlled synthetic benchmark로 유지.
- [PASS] Unknown 13→7 precision 오해 없음: Unknown 13→7은 field review candidate compression이며 classifier precision이 아님.
- [PASS] 123억 certified 표현 유지: internally certified quantified contribution 및 메모리제조기술센터 내부 성과 인정 기준 표현 유지.
- [PASS] Table 2 layout: caption과 table body를 축약했고, rendered page 4에서 컬럼 침범/겹침 없음.
- [PASS] Table 3 layout: Item / Value / Scope wording을 유지했고, rendered page 5 하단에 통째로 배치되어 page split 없음.
- [PASS] Table style: DOCX tables are real Word tables; raw markdown table syntax does not appear in DOCX text scan.
- [PASS] caption 위치: table captions are above tables and figure captions are below figures in rendered pages.
- [PASS] Figure 6/7 readability: rendered pages에서 A+B, A-only/B-only, Pair Mask, Whole 4-bit shape is scored 계열 label이 확인 가능.
- [PASS] 깨진 dash 없음: DOCX 텍스트 스캔에서 `—`, `–`, `‑`, `−` 문자가 검출되지 않음.
- [PASS] 깨진 공백/soft-hyphen 없음: `파 이프라인`, `해 야`, `확 인`, `single￾failure`, `micro￾F1`, `FCM￾PM`, `coordinate￾preserving`, U+00AD 패턴이 검출되지 않음.
- [PASS] 금지/위험 표현 없음: `P1`, `P2`, `Pipeline speed`, `candidate update`, `LLM agent`, `Known·Unknown` 패턴이 DOCX 스캔에서 검출되지 않음.
- [PASS] InfoNCE 표현 정리: `Information Noise-Contrastive Estimation` 식의 어색한 확장을 제거하고 `InfoNCE contrastive loss` / `InfoNCE loss`로 기능 중심 표현을 사용.
- [PASS] 검토군/group 표현 정리: 국문 prose에서는 `검토군`, `신규 불량군`, `신규 불량` 중심으로 정리하고, English caption/table에서는 `group` 표현 유지.
- [PASS] 새 수치 추가 없음: rev203은 rev202의 claim/scope를 유지하고 InfoNCE 표현, abstract의 불량군 표현, conclusion의 신규 불량 표현만 polish한 revision.

Notes:
- `tools\verify_full_paper_package.py`는 legacy expected figure/table/reference count와 old Abstract-heading assumption 때문에 FAIL을 보고한다. 현재 rev203의 core checks는 A4, margins, header/footer, two columns, figure files, citation/reference consistency, hidden XML scan, PDF page count 9를 통과했다.
- `full_paper_rev203_codex.docx`는 Table 3이 빌드 결과만으로 page split 없이 들어간 제출용 Word 파일이다.
