# NSRW Colab 재점검과 재개 tasks

최초 재점검: `2026-10-05` / 문서 갱신·실제 재작업 시작: `2026-10-06`

이 문서는 내부 실행 계획이다. 정식 연구 보고서나 새 execution receipt가 아니다.
기준 snapshot은 `CURRENT_POSITION_2026-10-05.md`이며,
10/5 snapshot은 보존한다. 10/6의 별도 strict-L2, L3, D, C01 실행 receipt 검수에 따라
각 named proposition만 승격했다. 작성과 문서 점검은 같은 신뢰영역에서 수행했으므로
독립적인 수학 검수로 표현하지 않는다.

## 1. 현재 위치와 다음 한 가지

**strict-L2, L3, D, C-01의 별도 commit-bound compiled receipts는 닫혔다. 다음 작업은
C-02: actual coefficient의 source decomposition 확인이다.** 이후 순차 실행은 §8의 AI 체크리스트를
사용한다. 이 문서 패치는 docs-only이며, 체크리스트 작성 자체가 후속 코드 수정,
Colab 실행, 설치, commit/push의 승인은 아니다.

```text
P2-L1 / P2-F1 / P2-L2-A
  historical compiled receipts: named propositions only

strict-L2
  claim_status: CONFIRMED (named pinned-source proposition only)
  check_status: PASS[COMMIT_BOUND_EXTERNAL_F1_STRICT_L2_REPLAY]
  commit-bound compiled receipt: reviewed, 2026-10-06

L3: k*A1 <= A0
  claim_status: CONFIRMED at the named pinned-source proposition scope
  check_status: PASS[COMMIT_BOUND_EXTERNAL_P2_L3_REPLAY]
  receipt: stage_receipts/P2_L3_COLAB_2026-10-06.md

D: source-linked NSRW deltaM negativity and two debt identities
  claim_status: CONFIRMED at the named pinned-source proposition scope
  check_status: PASS[COMMIT_BOUND_EXTERNAL_P2_D_REPLAY]
  receipt: stage_receipts/P2_D_COLAB_2026-10-06.md

C-01: main-only coefficient
  development compile: PASS[LOCAL_PROOF_COMPILE:P2_C01_MAIN_ONLY_FRESH_CHAIN]
  commit-bound claim admission: CONFIRMED for three named main-only propositions
  check_status: PASS[COMMIT_BOUND_EXTERNAL_P2_C01_REPLAY]
  receipt: stage_receipts/P2_C01_COLAB_2026-10-06.md

Actual coefficient sign / first-repair zero
  not promoted by this document
```

닫힌 strict-L2의 target은 다음 하나다.

```text
normalizedMainMoment c 0
  < Real.exp (-(3 / 20 : Real) * c.lam) * normalizedMainMoment c 1
```

이 proof는 약한 적분 비교 `F0 <= exp(-2 + 3*lam) * F1`와 compiled normalized
`F1 > 0`를 소비해 strictness를 얻었다. 추가 small-lambda 가정이나 ratio corollary는
없다. L3와 repair geometry는 이 receipt의 승인 범위가 아니다.

## 2. 재개 기준과 현재 관측의 한계

10/6 재작업 **시작 전** 로컬 파일·Git snapshot; 현재 HEAD 표가 아니다:

| 대상 | 재개 기준 |
| --- | --- |
| NSRW HEAD | `30c8c4fdd4854ee228d9fd6ea1178c8bf716484d` |
| OpenAI source commit | `8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538` |
| source tracked tree | clean; untracked/generated artifacts는 이 검사 범위 밖 |
| source toolchain 선언 | `leanprover/lean4:v4.34.0-rc2` |
| manifest portable Git blob SHA-1 | `f07a8454cb6200d90bcc4371bc9965e9f8f46c7d` |
| 재개 당시 strict-L2 SHA-256 | `624f1aa042377db7e2bbe50ba70d08a35035cddc51697bd5a69a1ce0bd9bbcdd` |
| F1 SHA-256 | `df9f605fa7ad9fa2842f54ae2d67b6a9b1773849d72c695192ae1bebe2f01206` |

재개 당시 NSRW worktree에는 미커밋 strict proof와 문서 변경이 있었다. strict proof와
runner는 이후 §7의 commit에 고정됐다. 이번 체크리스트 패치 전 관측 HEAD는
`aa4ec39821f72ba1c91699ff0724c1c5296cffdb`이며, 기존 tracked 문서 변경과 untracked
resource draft는 여전히 별도 작업으로 남아 있다. 로컬 repo 전체를 clean이라고
표현하거나 이를 정리한다는 이유로 reset하지 않는다. authority replay checkout의
clean 관측과 이 로컬 planning worktree는 구분한다. 다음 세션에는 실제 상태를 다시
관측하며, 이 문서의 HEAD를 앞으로의 영구 실행 pin으로 사용하지 않는다.
raw SHA-256은 해당 checkout의 bytes identity다. Linux 실행 bytes가 line ending으로
달라지면 runtime hash와 portable Git blob identity를 따로 기록한다.

L2-A receipt는 `a0d42a8...` / `9766f9ab...f919`의 representation/positivity bridge다.
같은 경로의 현재 `624f1aa...` strict implementation에 그 receipt를 상속하지 않는다.
기존 receipt는 기록된 commit/bytes에 대해 그대로 보존한다.

초기 문서 작성에서는 Colab runtime·cache·실행 셀·프로세스를 관측하지 않았다.
10/6 재작업의 실제 관측과 개발/clean replay 실행은 §7에 별도로 기록한다.
10/5 접근 차단 기록은 과거 관측이지 현재 runtime이 없거나 멈췄다는 증거가 아니다.
새 관측 전에는 `claim_status: UNVERIFIED`로 두고 `RUNNING`으로 쓰지 않는다.
10/5 focused Python 결과 `27 passed, 3 skipped` 및 공개 HEAD CI 성공은 당시의
별도 증거다. 오늘 재실행한 결과도, strict-L2 compile 증거도 아니다.

## 3. Colab을 사용하는 이유

Colab은 pinned inputs에서 project state를 재구성하는 **일회성 Linux executor**다.
새 상시 build service나 로컬 시스템 변경 없이 작은 proof chain을 실행할 수 있어,
현재 작업에 부담이 적은 현실적인 선택이다. 무료 여부나 노트북 저장 공간만을
선택 근거로 삼지 않는다. 자원·세션 지속·실행 시간은 실제 접속 후 측정한다.

notebook은 launcher이고 source/proof/runner identity와 로그가 실행 증거다.
같은 bounded runner는 다른 Linux host에서도 쓸 수 있어야 한다. GPU, ML training,
외부 dataset, application benchmark는 이 run의 범위가 아니다.

## 4. 재개 tasks와 완료 조건

- [x] **T0 — executor 관측.** 사용자가 notebook을 열고 필요한 로그인을 완료한다.
  RAM/disk/CPU, 실제 source-root Lean/Lake version, checkout·cache·실행 셀을 확인한다.
  runtime이 교체됐으면 pinned inputs에서 재구성한다. login/runtime 준비와 로컬 T1/T2
  준비는 병렬로 가능하다. 접속 성공이나 cache 존재만으로 compile PASS를 주지 않는다.

- [x] **T1 — bridge/strict 분리 필요성 검토.** 권장 구조는 기존 logical module
  `P2_L2_NormalizedMainMomentComparison`에 receipt-bound L2-A 내용을 보존하고,
  strict lemmas/final theorem을 새 `P2_L2_StrictMainMomentComparison.lean`으로
  분리해 기존 bridge를 import하는 것이다. 이는 가독성과 dependency 준비를 위한
  개선이지 현재 같은 경로를 쓴 것 자체가 수학 오류라는 뜻은 아니다. 분리 전후
  declaration·hypotheses·source objects를 대조하고 정확한 bytes를 기록한다.
  **10/6 판정: 물리적 분리는 보류한다.** 성공한 strict proof bytes를 변경하지 않고
  같은 module을 유지한다. historical L2-A receipt의 commit/bytes와 새 strict receipt를
  명시적으로 구분한다. 이 항목의 완료는 파일 분리 구현이 아니라 검토·처리 결정이다.

- [x] **T2 — 얇은 dependency runner.** 범용 framework를 만들지 않는다.
  `scripts/run-p2-l2-replay.py`로 `lake build +NavierStokes.PulseAmplitude` → exact F1의
  fresh `.olean` → bridge와 strict theorem을 담은 L2 module compile을 같은 run에서
  연결한다. 별도 bridge module이 없으므로 존재하지 않는 bridge `.olean` gate를 만들지
  않는다. pinned CLI의
  module-root 설정과 explicit `LEAN_PATH`를 사용하며, 외부 dependencies는 이번 run의
  출력만 소비한다. source cache를 재사용하더라도 source target command/exit는 기록한다.
  각 단계 command, exit, stdout/stderr hash, external `.olean` hash를 따로 남긴다.
  실행 전후 commit·tracked clean·manifest·proof·runner identity를 실제로 관측한다.
  source의 untracked shadow modules 등 compiler가 소비할 수 있는 입력도 확인한다.
  clean이라는 고정 문자열이나 source commit만으로 실제 입력 검사를 대체하지 않는다.

- [x] **T3 — strict-L2 개발 compile.** 실패는 invocation/module path, dependency,
  Lean API/tactic, 또는 실제 수학/specification 문제로 나눠 진단한다. 실패 로그와
  bytes를 먼저 보존하고 필요한 부분만 고친다. 개발 compile 성공은 commit-bound
  최종 receipt가 아니다. compile 실패 자체를 부등식의 수학적 반례로 기록하지 않는다.

- [x] **T4 — exact bytes 고정과 clean replay.** commit/push는 별도 명시적 승인 뒤에만
  한다. 성공한 proof/runner의 pinned commit을 clean checkout으로 재실행한다.
  source/F1/L2의 모든 필수 단계가 같은 run에서 exit 0이어야 한다.
  strict theorem의 `#print axioms`를 포착하고 `sorryAx` 및 예상 밖 axiom을 검수한다.
  stderr가 있으면 내용과 원인을 검수한다. stderr가 비었다는 사실만으로 성공을 판정하지
  않는다. pre/post identity와 로그 hash까지 일치해야 새 receipt admission이 가능하다.

- [x] **T5 — 성공 run 하나의 receipt.** T4의 단일 실행으로 dated receipt를 작성한다.
  claim ledger, current snapshot, root/capsule README, P2 note의 해당 범위만 동기화한다.
  안정적인 direction map은 정책이 달라질 때만 수정한다. 새 strict proposition만
  `claim_status: CONFIRMED`로 승격한다. 다른 run의 source PASS와 proof PASS를 합치지
  않는다. 기존 L2-A receipt와 실패 기록을 덮어쓰지 않는다.

- [x] **T6 — L3 진입.** strict-L2 compiled receipt 검수가 닫힌 뒤 template moment
  comparison을 시작한다. 실제 작업 순서는 §8의 `L3-01`부터 따른다.
  L2만으로 `DeltaM < 0`, `c1 > 0`, first-repair zero를
  승격하지 않는다. 이후 coefficient/amplitude decomposition, continuity, positive
  second-bump tail 및 first-window IVT bridge도 각각 닫아야 한다.

완료 기준은 문서 수나 theorem 파일 존재가 아니라 **exact strict theorem의 검수된
compiled receipt**다. T0–T6는 각각의 receipt 범위에서 닫혔다. L3의
cross-multiplied bound만 그 L3 receipt로 승격했다. D composition은 별도 D receipt로
닫혔다. C-01도 별도 receipt로 닫혔으며 다음 미완료 작업은 C-02 actual decomposition이다.

## 5. 별도 안전보수: 주 연구선을 대체하지 않는다

- [ ] **A0 — 다음 authoritative raw-export 소비 전에 TOCTOU 보수.** normalizer가
  projection에 소비한 bytes와 digest를 같은 안정된 bounded snapshot에 묶는다.
  pass 사이 교체 및 projection 중 변경을 테스트한다. 전/후 hash만으로
  mutate-and-restore까지 막았다고 주장하지 않는다. strict-L2 Lean compile 경로는
  이 normalizer를 소비하지 않으므로 A0를 그 compile의 선행조건으로 만들지 않는다.
- [ ] **A1 — runner 안정화 뒤 P2 CI.** 일반 software CI와 P2 external compile은 별개다.
  hosted P2 CI를 Colab receipt 작성의 새로운 선행조건으로 만들지 않는다.
- [ ] **A2 — 후순위 정리.** legacy JSON, ledger hex validation, release 링크,
  M5 CI 보수는 별도 patch다. 이번 문서 재개 계획을 새 release/tag로 포장하지 않는다.

## 6. 이번 문서 갱신의 경계

ledger는 증거를 찾는 색인이지 새로운 proof authority가 아니다. source proposition과
그 hypotheses가 수학 의미를 정하고, commit/bytes/run-bound evidence가 실행 사실을
정한다. 충돌하면 보류하고 근거를 대조한다.

수학적 반례, compile/identity admission 실패, 재개 조건은 별도로 기록한다.
`Q`의 global obstruction과 endpoint-first-zero 가설 기각은
`NEGATIVE_RESULT_REGISTER.md`에 보존한다. resource ledger와 register는 이번 문서
동기화에 함께 공개하는 색인이며, 스스로 공개 실행 근거가 되지 않는다. 이는 OpenAI theorem의
오류가 아니라 우리가 선택한 ratio 후보와 가설의 한계다.

초기 문서 갱신은 docs-only였다. 그 갱신에서 proof·runner·기존 receipt·Git index/commit/remote는
변경하지 않았으며, 그 초기 갱신 자체로 Colab 실행이나 새 Lean compile을 수행했다는
claim도 하지 않았다. 아래 실행 기록은 별도의 후속 작업이다.

## 7. 10/6 재작업: 실제 관측과 strict-L2 closure

- Colab source checkout, toolchain, 11개 dependency revision 및 cache bootstrap을 확인했다.
  관측 Lean은 `4.34.0-rc2`, CPU 2개, RAM 약 12 GiB이다. source target probe는
  2786 jobs / exit 0이다. cache나 이 probe를 strict proof authority로 사용하지 않는다.
- 과거 notebook 33개 셀·51개 출력을 로컬 evidence store에 보존한 뒤 오래된 셀
  26개를 정리했다. 실패 출력도 보존본에 남았다.
- 개발 run `nsrw-l2-development.kl0m2dvw`에서 source/F1/L2가 모두 exit 0이다.
  fresh F1 `.olean` hash와 3개 strict-module axiom 출력, 빈 stderr를 확인했다.
  axiom surface는 `[propext, Classical.choice, Quot.sound]`이며 `sorryAx`는 없다.
  개발 archive SHA-256은
  `03b689ced389c811ccf7f5f15b1c75bd412962ebc2210fea26053c9bcf782ea7`이다.
  이는 **uncommitted bytes의 개발 증거**이지 최종 receipt가 아니다.
- proof-only checkpoint `70456c53a2d132cac3a1529b98413a4f686953f6`를 커밋·푸시했고
  remote main SHA를 대조했다. 다른 수정 중 문서는 이 checkpoint에 포함하지 않았다.
- 현재 runner negative controls: `unittest` 6 tests PASS. 확인된 기존
  프로젝트 외부의 기존 venv에서 전체 pytest: `258 passed, 3 skipped, 3 subtests passed`,
  src coverage `90.29%`. replay runner는 coverage 대상 `src/nsrw` 밖이므로 이 수치는
  runner coverage를 의미하지 않는다. Ruff와 Python syntax compile도 통과했다.
- proof와 runner를 함께 고정한 `b02002b1ab954e34e7017a45e3afb338b21abfc5`를
  fresh clean checkout으로 실행했다. run `nsrw-l2-clean-replay.Bmph8w`에서 source,
  fresh F1, strict-L2가 모두 exit 0이고 pre/post identity와 axiom surface가 통과했다.
  기존 개발 PASS를 조립하지 않았다.
- launcher가 실제 checkout bytes와 committed Git blob bytes를 직접 비교했다.
  이번 Linux proof raw SHA는 Windows 개발 bytes와 동일한 `624f1aa...`였다.
  line-ending 동등성을 가정하지 않고 실제 bytes 및 compile 결과로 확인했다.
- 단일 run의 metadata/logs/inputs/fresh F1 artifact를 로컬 evidence store로 보존하고
  hashes를 대조했다. archive SHA-256:
  `ef825f4b1d45df191455cb155516558c135e156f62d500c20cc9de6cb7203699`.
  [strict-L2 dated receipt](stage_receipts/P2_L2_COLAB_2026-10-06.md)로 T4/T5를 닫았다.
  다음은 L3이며, downstream claim은 승격하지 않았다.
- 독립된 executor/verifier 신뢰영역이나 hosted attestation은 없다. receipt는 같은
  작업 세션의 기록된 실행과 로컬 archive 대조이며 독립적 인증으로 표현하지 않는다.

## 8. AI 전용 순차 실행 체크리스트

이 절은 실행 순서와 중단 조건이다. 아래 미체크 항목은 아직 수행되지 않았다.
체크는 **해당 항목의 직접 증거**가 생겼을 때만 한다. 설계 검토, 개발 compile,
commit-bound replay, 수학 claim의 승격을 서로 다른 완료 사건으로 기록한다.
T0–T5의 체크는 §7의 과거 실행 완료이지 현재 Colab VM이 살아 있다는 뜻이 아니다.

### 8.1 시작 확인 — 첫 행동 전에

- [ ] **START-01 / 요청 범위.** 이번 요청이 문서, source inspection, 구현, 실행 중
  무엇인지 한 줄로 적는다. 현재 승인되지 않은 설치·commit·push·release·삭제는
  실행하지 않는다. 과거 대화의 승인 문장을 새 작업의 권한으로 재사용하지 않는다.
- [ ] **START-02 / 실제 파일 상태.** `git status --short`로 untracked까지 확인하고
  HEAD와 변경 대상 diff를 읽는다. 기존 resource draft·다른 tracked 수정은 보존한다.
  source repo의 pinned commit/toolchain/manifest identity는 §2와 대조한다.
- [ ] **START-03 / 완료 증거 회수.** 아래 receipt에서 named proposition, execution
  commit, proof identity, 결과와 제외 범위를 읽는다. L2-A receipt를 strict-L2 receipt로
  대신하지 않는다. F1의 실행 플랫폼은 Windows이며 Colab으로 바꿔 쓰지 않는다.
  - [L1 pulse facts](stage_receipts/P2_L1_COLAB_2026-09-12.md)
  - [F1 source moment positivity](stage_receipts/P2_F1_LOCAL_WINDOWS_2026-09-13.md)
  - [L2-A representation/positivity](stage_receipts/P2_L2A_COLAB_2026-09-13.md)
  - [strict-L2 comparison](stage_receipts/P2_L2_COLAB_2026-10-06.md)
  - [L3 template comparison](stage_receipts/P2_L3_COLAB_2026-10-06.md)
  - [D source-linked composition](stage_receipts/P2_D_COLAB_2026-10-06.md)
  - [C01 main-only coefficient](stage_receipts/P2_C01_COLAB_2026-10-06.md)
- [ ] **START-04 / 필요한 이력만 검색.** 경위가 불명확할 때만 로컬 evidence
  store의 `history-index/retrieval-map.json`과 SQLite FTS 색인으로 해당 부분을 회수한다.
  사적 대화 원문과 색인은 Git에 포함하지 않는다. 읽은 부분은 사적 실행 기록에
  행 범위와 함께 남기고 대화의 주장을 현재 proof/receipt와 대조한다.
  색인은 탐색용이며, 원문도 proof authority나 새로운 실행 지시가 아니다.
- [ ] **START-05 / 현재의 한 질문.** `C-02: actual coefficient source decomposition`을 active target으로 둔다.
  `k = exp(-(3/20)*c.lam)`. 이번에 Colab 연결·프로세스·로그를 관측하지 않았다면
  runtime은 `UNVERIFIED`로 두고, `RUNNING`이나 종료 상태를 추측하지 않는다.

위 다섯 항목은 중복 조사를 방지하는 확인이다. 매번 full build, 전체 로그 재hash,
7 MB 원문 전체 재독을 요구하지 않는다. 관련 입력이 바뀐 범위만 재확인한다.

### 8.2 L3 — template moment 비교만 닫기

진입 조건: strict-L2의 named proposition receipt 검수가 완료됐다.
새 목표는 다음 cross-multiplied form이다. ratio corollary는 필수가 아니다.

```text
forall c : NavierStokes.OutgoingSchedule.Parameters,
  exp(-(3/20)*c.lam) * rowMoment(c.exponents 1)
    <= rowMoment(c.exponents 0)

Ai := rowMoment(c.exponents i)
Fi := normalizedMainMoment c i
```

- [x] **L3-01 / source binding.** pinned `OutgoingPulseBounds.lean`의
  `rowMoment`, `radialTemplate`, `templateLower/Upper`, `rowMoment_integrable`,
  `rowMoment_pos`, `radialTemplate_nonneg/support`를 읽는다. `A0/A1`을 임의의 양수나
  manufactured fixture로 바꾸지 않는다. `c.exponents 0 - c.exponents 1 = c.lam`은
  실제 `Parameters.exponents` 정의에서 확인한다.
- [x] **L3-02 / pointwise comparison.** template이 비영이면
  `x > exp(-3/20) > 0`이므로 `exp(-(3/20)*lam) <= x^lam`을 도출한다.
  `x^(a0) = x^(a1) * x^lam`에 필요한 양의 밑 조건을 명시한다. template이 영인 점은
  별도 경우로 처리한다. 전체 실수 적분에 대해 `x > 0`을 무조건 가정하지 않는다.
- [x] **L3-03 / source integral.** 각 integrand의 integrability와 template의
  비음수성을 사용해 적분을 비교하고, 마지막에 source-defined `rowMoment`로 돌아온다.
  `rowMoment_bounds`의 거친 절댓값 평가만으로 목표 비율을 얻었다고 하지 않는다.
  기본 `Parameters`로 충분한지 확인하고, 새 smallness 가정이 필요하면 이유를 기록한다.
- [x] **L3-04 / 작은 module.** 구현을 승인받았을 때만
  `formal/p2/P2_L3_TemplateMomentComparison.lean`을 추가한다. 필요한 import와
  target만 둔다. 성공한 L2 bytes를 refactor하지 않는다. L3가 L2를 소비하지 않으면
  불필요하게 import하지 않는다. 실제 `rowMoment` 비교를 검증한다.
- [x] **L3-05 / compile과 receipt.** §8.6의 공통 gate를 실시한다. 현행
  `run-p2-l2-replay.py`는 F1/L2 전용이며 L3를 지원한다고 취급하지 않는다.
  별도 `run-p2-l3-replay.py`와 negative controls를 검증하고 clean replay를 실시했다.
- [x] **L3-06 / 완료 조건.** 검수된 L3 compiled receipt로 이 비교만
  `claim_status: CONFIRMED`로 변경한다. `DeltaM`, 계수 부호, 영점을 함께 승격하지 않는다.
  이때 T6를 닫고 다음 active target을 D-01로 옮긴다.

완료 증거: [L3 dated receipt](stage_receipts/P2_L3_COLAB_2026-10-06.md),
execution commit `15108c35a2e5df948ece653a7f3fcfa02f3180f8`.
source build / fresh L3 compile exit `0`, stderr empty, expected axioms captured,
pre/post identities 일치. ZIP과 내부 hashes를 D: evidence store에서 대조했다.
[세션 index](sessions/P2_L3_SESSION_2026-10-06.md)는 연결 기록이며 proof authority가 아니다.

### 8.3 D — 두 비교를 source-defined DeltaM에 연결

진입 조건: strict-L2와 L3의 receipt가 각각 검수 완료됐다.

- [x] **D-01 / exact definition.** `DeltaM := F0/A0 - F1/A1`을 source의
  normalized debt 분해와 대조한다. 부호·row index·center·지수 인자가 일치하는지
  확인한다. `Fi`를 정규화되지 않은 `mainMoment`로 바꾸지 않는다.
- [x] **D-02 / division conditions.** `A0 > 0`, `A1 > 0`, normalized `F1 > 0`을
  named source/compiled lemmas로 얻는다. L2의 `F0 < k*F1`과 L3의 `k*A1 <= A0`에서
  `F0*A1 < F1*A0`, 이어서 `DeltaM < 0`을 도출한다.
  단순 대수 fixture의 성공으로 source-object theorem을 닫지 않는다.
- [x] **D-03 / 완료 조건.** 조합 theorem을 §8.6으로 닫는다. 해당 receipt는
  `DeltaM < 0`만 승격 가능하며, 실제 계수와 first-window zero는 보류한다.

완료 증거: [D dated receipt](stage_receipts/P2_D_COLAB_2026-10-06.md),
execution commit `06cb400667c433b076599aabadc5d5f9d13f8f24`.
source → fresh F1 → strict L2 → L3 → D가 같은 run에서 exit `0`이다.
`deltaM_neg`과 두 debt identities만 승격했으며 계수·영점은 그 receipt 범위 밖이다.

### 8.4 C — affine coefficient에서 실제 small-positive-eta 부호로

진입 조건: source-defined `DeltaM < 0`의 compiled receipt가 검수 완료됐다.

- [x] **C-01A / source bridge와 구현.** source의 normalized 2×2 system에서
  `affineCoefficients c 0 1 1 = -DeltaM / (rho0-rho1)`을 정확한 index로 연결한다.
  `rhoi = exp(2*beta c i)`와 gap positivity를 확인하고 main-only coefficient의
  양수를 증명한다. matrix invertibility만으로 계수 부호를 얻을 수는 없다.
  `P2_C_MainOnlyCoefficient.lean`의 SHA-256은
  `6be4e26255568f5b45c297b548ecadceb35f807519e01bf21e372eb9fbd22fcf`다.
- [x] **C-01B / 개발 fresh-chain compile.** source → fresh F1 → L2 → L3 → D → C를
  한 development run에서 compile했다. 모두 exit `0`, stderr empty, 12개 axiom
  observations에 `sorryAx`가 없다. private archive SHA-256은
  `d2efe58d0c7e2c07c384704a14bdcc69a24a4163d7588a13b41e6eb6713268aa`다.
  범위는 `PASS[LOCAL_PROOF_COMPILE:P2_C01_MAIN_ONLY_FRESH_CHAIN]`이며 claim admission이 아니다.
- [x] **C-01C / commit-bound closure.** exact proof checkpoint, 얇은 C replay runner와
  negative controls, 별도 clean checkout의 동일 fresh chain, 단일 dated receipt 검수를
  §8.6에 따라 닫는다. 그 전에는 main-only positivity도 최종 claim으로 승격하지 않는다.
  완료 증거: [C01 dated receipt](stage_receipts/P2_C01_COLAB_2026-10-06.md),
  execution commit `304f2adc3f26310554dfa64a572329b6a7ff8cf8`.
  source → fresh F1 → L2 → L3 → D → C가 모두 exit `0`, pre/post identities가 일치했다.
  main-only gap/formula/positivity만 승격했다. 기존 development archive를 재사용해
  receipt를 조립하지 않았다. actual `c1(0)`/`c1(eta)`는 이 정리의 별칭이 아니다.
- [ ] **C-02 / actual coefficient.** `OutgoingSchedule`과 실제 profile의
  debt/amplitude/correction 연결을 읽고 prefix/main 성분 분해를 확인한다.
  `affineCoefficients c 0 1 1`과 실제 `c1(eta)`를 동일시하지 않는다.
  `q(eta) = eta*(1+eta^2)`, amplitude positivity/continuity의 사용 지점과
  `eta^2 <= 1` 등의 적용 조건을 source 정의에서 확정한다.
- [ ] **C-03 / eta=0 bridge와 continuity.** C-02의 actual decomposition에서
  main-only positive contribution을 실제 `c1(0)`에 연결하고 amplitude 조건과
  연속성을 확인한다. main-only coefficient 자체를 `c1(0)`라고 이름 바꾸지 않는다.
- [ ] **C-04 / small-positive-eta quantifiers와 완료 조건.** 고정된 admissible construction마다
  `exists epsilon > 0, forall eta, 0 < eta < epsilon -> actual c1(eta) > 0`을
  목표로 둔다. 필요하면 `epsilon <= 1`로 specification domain을 유지한다.
  모든 construction에 공통인 epsilon, 모든 양의 eta, 음의 eta 확장은 별도 문제다.
  construction의 파라미터가 eta에 의존한다면 고정-parameter 논증을 멈추고,
  그 의존성을 포함한 statement와 필요한 estimate를 다시 확인한다.
  continuity 또는 명시적 one-sided estimate로 닫고 §8.6의 receipt에 정확한 범위를 기록한다.
  selected numerical `TailData`를
  만들어내지 않는다. parametric proof에 불필요한 numerical witness를 gate로 두지 않는다.

### 8.5 Z — 첫 repair window 내부 영점을 source mass로 연결

진입 조건: 실제 small-positive-eta coefficient sign의 compiled receipt가 검수 완료됐다.

- [ ] **Z-01 / geometry.** main pulse와 두 bump의 support, window 순서와 분리를
  확인한다. `lower(0)`, `upper(0)`, `lower(1)`, terminal endpoint의 radial/log/profile
  coordinate를 통일한다. source의 `massMoment`와 profile의 `M`을 연결하는
  양의 scale factor를 정확한 bridge로 유지한다.
- [ ] **Z-02 / endpoint signs.** small positive eta에서 첫 window 진입점의
  `M > 0`을 source primitive에서 얻는다. second bump의 비음수성뿐 아니라 positive
  subinterval과 양의 weight로 full weighted integral의 strict positivity를 얻는다.
  tail representation과 `c1 > 0`으로 **첫 window 상단**에서 `M < 0`을 닫는다.
  gap 내부 한 점의 음수 값만으로 window 내부의 영점 위치까지 확인했다고 하지 않는다.
- [ ] **Z-03 / continuity와 IVT.** 같은 mass object의 연속성과 양 끝의 strict
  signs로 `exists r in (lower(0), upper(0)), M(eta,r)=0`을 증명한다.
  개구간 포함, XR/log/radial 변환, epsilon과 specification 조건을 유지한다.
- [ ] **Z-04 / 완료·제외 범위.** §8.6을 닫은 named existence proposition만 승격한다.
  영점 유일성, 첫 영점, 모든 eta의 부호, Q의 removable extension, Navier–Stokes
  전체의 새 증명을 주장하지 않는다. terminal zero plateau와 endpoint-first-zero
  가설 기각은 지우지 않고 Q의 domain obstruction을 정리한다.
- [ ] **Z-05 / 다음 수학 질문.** 가정·비자명성·source 대비 추가 내용을 사람의
  수학적 검토에 전달한다. compiled proposition과 독립적인 수학적 novelty를 구분한다.
  Q 후보의 한계에서 다음에 시도할 질문 하나를 고르고, framework 증설을 연구 성과로
  세지 않는다.

### 8.6 공통 gate — 새로운 named proposition마다 적용

아래 항목은 새로운 source bytes에 적용한다. 기존 receipt를 재작성하라는 요구가 아니다.

- [ ] **RUN-01 / statement review.** exact target, source object, 전체 hypotheses,
  import dependency를 먼저 대조한다. `sorry`/`admit`/새 axiom/target 약화로 통과시키지
  않는다. proof가 목표를 정확히 의미하는지 여부는 compile exit와 별도로 검토한다.
- [ ] **RUN-02 / 개발 compile.** pinned source root의 environment에서 module-root와
  logical module name을 맞춘다. 외부 import의 `.olean`은 이번 exact source에서
  생성한다. 과거 `-I`/path/OOM/tactic 실패는 실패 기록으로 보존하며 수학적 반례로
  바꾸지 않는다. 개발 compile은 `PASS[LOCAL_PROOF_COMPILE]` 범위로 제한한다.
- [ ] **RUN-03 / exact bytes 고정.** commit/push의 명시적 승인을 받은 뒤 대상만
  stage하고 성공 bytes의 identity를 대조한다. 무관한 draft를 포함하지 않는다.
  proof/runner가 변경되면 새로운 execution record로 취급한다.
- [ ] **RUN-04 / 동일 clean replay.** 새로운 bounded run directory에서 pinned source,
  NSRW commit, source-root에서 관측한 toolchain version, manifest portable identity,
  proof/runner bytes, 실제 소비 inputs를 pre/post 확인한다. 로컬 planning worktree의
  dirty 상태와 별도의 clean execution checkout을 혼동하지 않는다.
  source target과 필요한 external dependencies의 compile을 같은 run에서 연결하고,
  command/exit/time, stdout/stderr hash, fresh `.olean` hash를 각각 기록한다.
  기존 runner가 해당 source inputs/module을 처리하는지 먼저 확인한다.
- [ ] **RUN-05 / 결과 판정.** 필수 command의 exit 0, 해당 theorem의 `#print axioms`,
  stderr 내용, identity consistency를 함께 검수한다. `sorryAx` 부재는 axiom-surface
  observation이며 전체 source의 semantic audit가 아니다. cache 사용을 공개하고
  target compile을 full clean library rebuild라고 부르지 않는다.
- [ ] **RUN-06 / 단일 receipt와 다음 gate.** 같은 성공 run의 저장 로그·inputs만으로
  dated receipt를 만들고 named proposition과 제외 범위를 적는다. Linux raw hash와
  Git blob identity는 실제 관측으로 구분한다. private paths/hostname/token을 공개
  문서에 넣지 않는다. executor와 reviewer가 같은 신뢰영역이면 명시한다.
  검수 후 해당 status만 동기화하고 다음 stage를 active로 둔다. historical receipt와
  실패 로그는 덮어쓰지 않는다.

### 8.7 중단·인계 — 불완전한 GREEN과 끝없는 준비 작업 방지

- [ ] **STOP-01 / failure boundary.** 불일치가 inputs, environment, invocation,
  Lean API, 수학 statement 중 어디에 있는지 기록한다. 필요한 증거가 없는 대상만
  `task_status: HELD`, 미확인 claim은 `UNVERIFIED`로 둔다. 구현·자원 부족은 자동으로
  `FALSIFIED`가 아니다. 무관한 연구 lane까지 중단하지 않는다.
- [ ] **STOP-02 / 다음 세션 인계.** active target / 마지막 성공 receipt /
  proof·runner identity / 마지막으로 관측한 run과 exit / 미해결 한 건 / 다음 구체적
  command 또는 source-reading target / 추가 승인 필요 여부를 남긴다.
  `RUNNING`은 실제 process/run의 새로운 관측이 있을 때만 사용한다.
- [ ] **STOP-03 / scope audit.** 변경이 수학 obligation 하나를 전진시켰거나 구체적
  오주장을 배제했는지 확인한다. 불필요한 새 parser/framework, HF 실험,
  full-library stress build, release/tag를 이 chain에 추가하지 않는다.
  direction map은 안정된 방침 변경 때만 수정하고 실행 이력은 dated receipt에 둔다.

다음 구체적 작업은 **C-02: actual coefficient의 prefix/main/amplitude 분해와 parameter 의존성 대조**다.
C-01 receipt는 main-only 세 proposition만 닫았다. actual 계수 부호와 first-window zero는
C-02~04와 Z의 별도 proof/receipt를 요구한다.
이후 proof 구현·실행은 해당 작업의 승인 범위에 따라 진행한다.
