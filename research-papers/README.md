# NSRW research papers

작성일: 2026-10-14 (Asia/Bangkok)
공개 저자: **Yun Kwansub**. 제공되지 않은 소속·ORCID는 기입하지 않는다.

이 폴더는 논문 작성과 검수의 작업 공간이다. `docs/`의 프로그램·재현·운영
문서와 구분한다. 논문 목록은 수학 claim ledger나 release 승인 시스템이 아니다.
이번 최초 공개 대상은 **NSRW 소프트웨어와 P01 수학 원고 v0.4**다.
P02는 다음 공개 단계, P03는 별도 개정·기여 검토 이후로 미룬다.
내부 검수 기록과 후속 원고는 이 공개 tree에 포함하지 않는다.
Zenodo 논문 레코드와 DOI는 실제 등록 후 연결한다.

## 현재 원고

| 원고 | 읽기 | 현재 상태 |
|---|---|---|
| P01 — 수학 | [Mass zero / angular mismatch](P01_MassZero_AngularMismatch.md) | v0.4: 정리 범위 유지; 논문 라이선스·재현 안내 보강 |
| P02 — 코드·재현 | 후속 원고, 이번 공개 제외 | 구현과 실제 연구 사용 경험을 다룬다 |
| P03 — 의미 변환 사례연구 | 후속 원고, 이번 공개 제외 | 별도 기여 검토 후 공개 여부를 결정한다 |

P01은 Markdown 원고와 standalone LaTeX 소스, 실제 PDF를 제공한다.
조판 검사는 수학적 실행 검증과 별개이며, 공개 승인 역시 외부 peer review를
의미하지 않는다. 두 후속 원고는 소프트웨어·수학 원고와 별개의 출판물이다.

- P01: [LaTeX](latex/P01_MassZero_AngularMismatch.tex) / [PDF](pdf/P01_MassZero_AngularMismatch.pdf)
- [조판 재현](latex/README.md) / [선정 배포 구성](PUBLICATION_CONTENTS.md)

이번 P01 공개 파일의 manifest는 `SHA256SUMS-P01-v0.4`이다.
이전 통합 manifest와 후보는 로컬에 보존되며 이번 공개 파일의 identity로
사용하지 않는다. 원고 0.4와 소프트웨어 0.4.0은 서로 다른 버전 축이다.

논문 본문·LaTeX·PDF는 [CC BY 4.0](LICENSE-PAPERS.md), 코드·Lean 증명은
기존 MIT다. [재현 안내](REPRODUCE.md)는 exact execution checkout과
후속 receipt 문서의 lineage를 구분한다.

## 작성 목록과 우선순위

아래 세 편을 작성 대상으로 관리한다. 제목은 작업 제목이며, 지금 반드시
완성할 첫 원고는 P01이다. P02/P03은 각각 별개의 기여와 근거가 있을 때
완성한다. 같은 결과를 세 편으로 나누거나 논문 수를 채우지 않는다.

| ID / 순서 | 논문 / 작업 제목 | 중심 질문과 독립된 기여 | 현재 재료 | 작성·공개 전 남은 일 |
|---|---|---|---|---|
| P01 / 최우선 | **수학 기술노트** — *A First-Repair Mass Zero Without Angular-Moment Cancellation* | 각 고정 source Profile의 작은 양의 η 영역에서 동일한 점의 M=0 및 J>0; separated supports와 weighted-tail 비교의 메커니즘 | Z-core/Z+J Lean 모듈, 두 dated receipt, 기존 영어 초안 | 정의·가정·정리·증명 정돈; upstream 인용과 제한된 문헌 비교; 3차 원고 검수; 공개 artifact 연결 |
| P02 / 두 번째 | **NSRW 코드·재현 방법론** — *From Source-Bound Proofs to Reproducible Research Artifacts: An NSRW Case Study* | 실제 연구에서 코드가 source binding, proof dependency, 실행 실패 분류 및 재현을 어떻게 지원했는가 | runner/test/CI 코드, 실패·수정·보존 기록, endpoint-first-zero 후보 폐기 사례 | 실제 caller·검사·실패 경로 추적; 기존 도구와 비교; 유지보수 비용·한계; 외부 재현 시도 경험 확보 후 완성 권장 |
| P03 / 세 번째 | **Equation to Artifact 거버넌스 사례연구** — *Equation to Artifact: Claim Boundaries and Operational Exposure in AI-Assisted Research* | source→proof→execution→public derivative 사이에서 claim 범위를 어떻게 보존하고, 어디서 잘못 확대될 수 있는가 | resource principles, operational exposure 문서, NSRW의 claim 변환·문서 drift·custody gap 사례 | 관련 provenance/reproducibility 문헌 비교; 실제 통제와 문서상 정책 구분; 놓친 오류·비용·same-trust-domain 한계 제시 |

P02는 **구현과 사용 경험**, P03은 **주장의 변환과 해석 경계**가 중심이다.
P03이 P02의 절차 설명을 반복하는 데 그친다면 독립 논문으로 내지 않고
P02의 방법론 절 또는 부록으로 통합한다. 거버넌스라는 이름만으로 효능,
보안성 또는 일반적 신뢰성을 주장하지 않는다. 외부 재현의 실패 사례도
방법론의 자료가 될 수 있지만 성공 또는 독립 확인으로 바꾸지 않는다.

## P01에서 고정할 수학적 범위

각 고정된 pinned-source `Profile F`에 대해:

\[
\exists\epsilon_F>0,\quad\forall\eta\in(0,\epsilon_F),\quad
\exists r\in(l_0,u_0):\quad
M_F(\eta,X_r)=0\ \land\ J_F(\eta,X_r)>0,
\qquad X_r=\exp(B_F)r.
\]

`B_F=F.data.core.pulseStart`, `l₀=F.data.core.lower 0`,
`u₀=F.data.core.upper 0`이다. epsilon은 Profile에, r은 η에 의존할 수 있다.
M/J는 동일한 F·η·r·X에서 평가한다.

별도 조건부 정리는 첫 window 내부의 `localMass=0`와 실제 두 번째 axial
repair coefficient `c1>0`에서 `localAngularMoment>0`를 얻는다. 이 조건부
정리에는 `eta>0`가 필요하지 않다. 작은 양의 η에 대한 존재 정리와 구별한다.

공통·수치 epsilon, 계산된 root, first/unique/simple zero, Q의 pole·limit,
문헌 신규성, upstream theorem 검증, 일반 Navier–Stokes 해법 또는 실용 solver
성능은 주장하지 않는다. `Q=J/(M H)`의 비영분모 조건 실패는 pole 증명이 아니다.

## 원고와 artifact는 별개의 출판물

- **수학 원고:** 정의·가정·논증·해석·관련 연구를 설명한다.
- **소프트웨어/재현 artifact:** exact inputs, 명령, 허용된 실행 요약 및
  receipt를 보존한다. 이것을 논문 한 편으로 계산하지 않는다.
- `CITATION.cff`는 현재 소프트웨어 인용 정보다. 논문 출판이나 DOI를 뜻하지 않는다.
- 논문 작성·검수는 지금 시작할 수 있다. GitHub Release나 artifact DOI 발급이
  초안 작성의 선행조건은 아니다. 공개 최종본에는 실제 확정된 artifact identity를
  연결하고, 없는 DOI·공개 URL은 만들어 넣지 않는다.
- 저자는 2026-10-14에 NSRW + P01 공개 순서를 승인했다. 파일 검수·실제
  업로드·DOI 회수는 별개의 관측으로 남긴다. 독립 재현을 수행했다고 주장하지 않는다.

## 3차 검수와 변경 관리

내부 기록에서 각 원고의 검수 대상 버전·검토자·근거와 남은 수정사항을
관리한다. 서로 다른 질문을 검토하는 세 차례이지, 같은 글을
반복 확인해서 자동으로 독립 검증을 얻는 절차가 아니다.

1. **1차 — 수학·source 의미:** quantifier, 가정, 좌표, 같은 witness,
   weighted-tail 부등호, 실제 Lean statement 및 upstream attribution 대조.
2. **2차 — 코드·재현·인용:** 논문 설명과 실제 구현·명령·receipt·artifact의
   일치; 문헌 인용, 원본/파생본 구분, 재현 가능 범위와 누락 근거 확인.
3. **3차 — 공개 최종본:** 설명의 가독성, 과장·중복, 저자/AI 기여,
   개인정보·권리·라이선스, 실제 링크 및 배포할 파일 목록 검수.

세 검수가 동일한 최종 원고 bytes를 포괄하고 미해결 중요 지적이 없을 때만
release **후보**로 넘긴다. 승인 후 정식 배포한다. 검수 후 변경이 생기면 영향받는
검수를 다시 연다. 세 scoped PASS는 peer review나 independent attestation이 아니다.
P01 검수 결과가 P02/P03에 자동 상속되지 않는다.

## 자료 위치

- [출판·국제 재현 계획](../docs/NSRW_PUBLICATION_AND_REPRODUCTION_PLAN_2026-10-08.md)
- [P2 수학 연구 본문](../docs/M5_P2_DILATION_RATIO_OBSTRUCTION_STUDY.md)
- [Z-core receipt](../docs/stage_receipts/P2_Z_CORE_COLAB_2026-10-12.md)
- [Z+J receipt](../docs/stage_receipts/P2_ZPLUS_J_COLAB_2026-10-12.md)
- [최종 source composition](../formal/p2/P2_ZPLUS_J_SourceComposition.lean)
- [CI/CD의 실제 검사 범위](../docs/CI_CD_VERIFICATION_BOUNDARIES.md)
- [Equation to Artifact 원칙](../docs/E2A_RESOURCE_PRINCIPLES.md)
- [Operational exposure 정의](../docs/OPERATIONALLY_EXPOSED.md)
- [소프트웨어 인용 정보](../CITATION.cff)

기존 P01 초안은 로컬 `publication/p2-z-phase-2026-10-12-candidate/TECHNICAL_NOTE_DRAFT.md`
에 있다. 이 파일은 Git-ignored 후보이므로 공개 독자가 읽을 수 있다고 가정하지
않는다. P01은 그 초안을 출발점으로 v0.1 학술 원고를 작성했고, 검토 의견을
반영한 v0.2 이후 source 링크·재현 안내·조판을 보강한 현재 v0.4로 개정됐다.
기존 초안·후보 ZIP은 이동·덮어쓰기하지 않았다. 원본 ZIP·raw logs·runtime
metadata는 계속 `colab/evidence/`의 비공개 보존 대상이며 이 폴더로 복사하지 않는다.

## 당장 다음 작업

1. 승인된 NSRW 소프트웨어 release의 실제 identity와 Zenodo 보존 결과를 확인한다.
2. P01을 별도 preprint 레코드로 연결한다. 발급되지 않은 DOI를 기입하지 않는다.
3. P02는 다음 공개 단계, P03은 별도 패치와 독립 기여 검토로 진행한다. 내부 검사 도구명·
   출력·작업 기록은 논문이나 배포 패키지에 포함하지 않는다.

v0.4.0은 현재 성과의 repository/artifact 기준점이다. 원고 v0.4와는 별도의
버전 축이다. 실제 tag/Release 상태는 GitHub Releases에서 확인한다. P03의 후속 schema와
코드 개선을 v0.4.0의 새 필수조건으로 추가하지 않는다. 이후 독립된 기여가
확인되면 방법론 원고를 공개하고, 다음 연구는 기존 roadmap의 실용화 후보를
실제 baseline·입력·측정으로 평가하는 방향으로 이어간다.

Fuller P2 study는 P01과 겹치지 않는 추가 결과가 생길 때 재검토한다.
응용 논문은 별도 domain·baseline·실험 근거가 생긴 이후의 후보이며, 현재
필수 원고 목록에 넣지 않는다. 웹사이트·홍보·새 framework는 원고 완성을
대체하는 작업이 아니다.
