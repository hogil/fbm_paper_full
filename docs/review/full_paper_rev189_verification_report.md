# full_paper_rev189_codex verification report

Status: FAIL

Passes: 55
Warnings: 1
Failures: 18

## Failures
- markdown References section missing
- markdown figure reference count is 9, expected 2-6
- markdown table caption count is 0, expected 3-4
- DOCX media count is 9, expected 2-6
- DOCX app Pages is 1, expected 4-10
- DOCX app Words is unsafe: '0'
- DOCX figure caption count is 9, expected 2-6
- DOCX table caption count is 8, expected 3-4
- DOCX table count is 8, expected 3-4
- Abstract heading font mismatch: size=12.0, bold=True
- too few section headings found: 0
- caption paragraph count is 17, expected 5-10
- body paragraph alignment is not justified: 1. 서론; 2. 본론; 2.1.1. 데이터 표현과 정합 적재; 2.1.2. Known fail 분류 구조; 2.1.3. Unknown fail 군집화 구조
- reference paragraph count is 25, expected 7-20
- reference run formatting mismatch: [1] 약 0.31 GFLOPs(307.9 MFLOPs size=9.0; [1] 약 0.31 GFLOPs(307.9 MFLOPs size=9.0; [2] 채택 in_ch=5와 비채택 in_ch=6을 동 size=9.0; [2] 채택 in_ch=5와 비채택 in_ch=6을 동 size=9.0; [3] 약 90% 공수 절감은 현업 운영 성과 집계·인 size=9.0
- references with italic publication title runs: 21/25
- reference publication title casing mismatch: [3] Khosla, P. et al., "Superv: in; [5] Woo, S. et al., "ConvNeXt : and, on; [6] Chen, T. et al., "A simple: on; [7] Campello, R. J. G. B. et a: and, on; [8] He, K. et al., "Momentum c: and, on
- PDF title/author/Abstract-to-Keywords range not found

## Warnings
- subsection heading count is 6

## Passed Checks
- markdown exists: D:\project\fbm_paper_full\full_paper_rev189_codex.md
- DOCX exists: D:\project\fbm_paper_full\full_paper_rev189_codex.docx
- PDF exists: D:\project\fbm_paper_full\full_paper_rev189_codex.pdf
- markdown title line exists
- markdown Abstract heading is bold
- markdown uses current figure folder: figures/full_paper_rev189
- markdown has no stale figure folders
- markdown risk-pattern scan complete
- markdown standalone abbreviation scan passed
- figure file exists: figures/full_paper_rev189/fig01_dram_to_fbm.png
- figure file exists: figures/full_paper_rev189/fig02_pipeline_architecture.png
- figure file exists: figures/full_paper_rev189/fig03_roi_yolo.png
- figure file exists: figures/full_paper_rev189/fig04_objid_flow.png
- figure file exists: figures/full_paper_rev189/fig05_chip_label_space.png
- figure file exists: figures/full_paper_rev189/fig06_fcm_pm.png
- figure file exists: figures/full_paper_rev189/fig07_probability_control.png
- figure file exists: figures/full_paper_rev189/fig_objid_compare.png
- figure file exists: figures/full_paper_rev189/fig09_webapp_viewer.png
- citations match references: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]
- DOCX hidden XML risk-pattern scan passed
- unexpected DOCX part absent: word/comments.xml
- unexpected DOCX part absent: word/footnotes.xml
- unexpected DOCX part absent: word/endnotes.xml
- unexpected DOCX part absent: docProps/custom.xml
- DOCX contains no embedded objects
- DOCX core title is set
- DOCX core creator is set: 최호길, 홍지훈, 김성호
- DOCX core description is submission-specific
- DOCX app Application is Microsoft Word
- DOCX app Company is Samsung Electronics
- DOCX header contains Samsung Best Paper Awards
- DOCX footer contains affiliation company
- DOCX has 2 sections
- section 1 A4 page size
- section 1 margins/header/footer match rules
- section 2 A4 page size
- section 2 margins/header/footer match rules
- body section has 2 columns with 0.5 cm gap
- DOCX run font mappings match Times New Roman / 바탕체: 402 runs
- title font matches: 20.0 pt bold=True
- author font matches: 12.0 pt bold=True
- Abstract body font matches: 10.0 pt bold=True
- title alignment matches rule
- author alignment matches rule
- Abstract heading alignment matches rule
- Abstract body alignment matches rule
- keywords alignment matches rule
- all non-empty top-level paragraphs use line spacing 1.0
- reference paragraphs contain no raw markdown emphasis markers
- at least one journal volume run is bold
- PDF page count is within full-paper limit: 9
- PDF first page visibly contains Samsung Best Paper Awards header
- PDF first page visibly contains affiliation footer
- PDF first page visibly contains page number
- render folder contains 9 page PNGs and contact sheet
