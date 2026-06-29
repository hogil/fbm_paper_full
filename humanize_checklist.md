# Humanize checklist - full_paper_rev197_codex

- [PASS] Abstract 15줄 이내: Abstract는 한 단락으로 유지했고, 담당자가 의심 wafer를 다시 찾고 map과 수치를 맞춰 보는 현업 흐름을 유지하였다.
- [PASS] "본 연구는" 반복 없음: 본문 스캔에서 `본 연구는`과 `본 논문은` 표현이 검출되지 않았다.
- [PASS] 한 문장에 metric 과다 나열 없음: Abstract와 주요 결과 문단은 Known, Unknown, chip-level 결과를 분리해 읽히도록 정리하였다.
- [PASS] validation scope 유지: field validation, field review, generated development, controlled synthetic benchmark 구분을 유지하였다.
- [PASS] object-id overclaim 없음: object-id map은 detector를 이긴 작은 모델이 아니라 fixed chip coordinate를 사용해 Stage 2 문제를 바꾼 결과로 설명하였다.
- [PASS] FCM-PM production claim 없음: FCM-PM은 controlled synthetic benchmark로 유지하였다.
- [PASS] Unknown 13→7 precision 오해 없음: Unknown 13→7은 운영 wafer를 13개 검토 group으로 정리해 7개 신규 불량을 확인한 field review 결과이며 classifier precision이 아니라고 유지하였다.
- [PASS] 123억 official/certified 표현 유지: internally certified quantified contribution 및 메모리제조기술센터 내부 성과 인정 기준 표현을 유지하였다.
- [PASS] 깨진 dash 없음: 본문 스캔에서 `—`, `–`, `‑`, `−` 문자가 검출되지 않았다.
- [PASS] 깨진 공백/하이픈 없음: `파 이프라인`, `해 야`, `확 인`, `single￾failure`, `A￾B`, `FCM￾PM` 패턴이 검출되지 않았다.
- [PASS] 항목 요약식 완화: `기여는`, `첫째`, `둘째`, `정리하면`, `중요한 점은`, `아래 결과는` 표현이 본문 스캔에서 검출되지 않았다.
- [PASS] 추상 구조어 완화: `data asset layer`, `AI analysis layer`, `operation layer`, `validation-scope separation`, `운영형 분석 파이프라인` 표현이 본문 스캔에서 검출되지 않았다.
- [PASS] 지적 표현 제거: `candidate compression`, `candidate-compression`, `compression candidate`, `담당자가 볼 후보`, `generated-chip development`, `같은 metric`, `하나의 metric`, `metric처럼`, `합산하지` 표현이 본문 스캔에서 검출되지 않았다.
- [PASS] 현업자 톤 보강: review 화면에서 wafer 검색, map overlay, chip measure 확인, review label 기록, 판단 라벨 재사용이 본문에 직접 드러나도록 보강하였다.
- [PASS] 새 수치 추가 없음: rev197 수정은 문체 보정만 수행했고 새 metric이나 운영 수치를 추가하지 않았다.

Notes:
- `Known failure`와 `Unknown failure`는 논문 용어로 유지하였다. `Known fail은` / `Unknown fail은` 식의 구어적 반복은 제거하였다.
- `defect`는 참고문헌 원제에만 남아 있으며, 본문/표/캡션에서는 사용하지 않았다.
- 자동 verifier는 PDF 미생성과 오래된 figure/table/reference count 기준 때문에 FAIL을 보고한다. 이번 cycle에서도 stale PDF를 만들지 않았고, DOCX/Markdown의 텍스트·scope·hidden XML 스캔을 중심으로 확인하였다.
