# NSRW Colab 재점검과 재개 tasks

최초 재점검: `2026-10-05` / 문서 갱신·실제 재작업 시작: `2026-10-06`

이 문서는 내부 실행 계획이다. 정식 연구 보고서나 새 execution receipt가 아니다.
기준 snapshot은 로컬 planning draft `CURRENT_POSITION_2026-10-05.md`이며,
10/5 snapshot은 보존한다. 10/6의 별도 strict-L2 실행 receipt 검수에 따라 해당
proposition만 승격했다. 작성과 문서 점검은 같은 신뢰영역에서 수행했으므로
독립적인 수학 검수로 표현하지 않는다.

## 1. 현재 위치와 다음 한 가지

**strict-L2와 L3는 별도의 commit-bound compiled receipt로 닫혔다.
다음은 source-defined DeltaM의 정확한 정의를 대조하고 두 비교의 composition을
formalize하는 것이다. DeltaM 자체는 아직 승격하지 않는다.**

```text
P2-L1 / P2-F1 / P2-L2-A
  historical compiled receipts: named propositions only

strict-L2
  claim_status: CONFIRMED (named pinned-source proposition only)
  check_status: PASS[COMMIT_BOUND_EXTERNAL_F1_STRICT_L2_REPLAY]
  commit-bound compiled receipt: reviewed, 2026-10-06

L3: k*A1 <= A0
  claim_status: CONFIRMED (named pinned-source proposition only)
  check_status: PASS[COMMIT_BOUND_EXTERNAL_P2_L3_REPLAY]
  receipt: stage_receipts/P2_L3_COLAB_2026-10-06.md

DeltaM / coefficient sign / first-repair zero
  not promoted by this document
```

strict-L2의 target은 다음 하나다.

```text
normalizedMainMoment c 0
  < Real.exp (-(3 / 20 : Real) * c.lam) * normalizedMainMoment c 1
```

약한 적분 비교 `F0 <= exp(-2 + 3*lam) * F1`를 먼저 얻고,
이미 compiled된 normalized `F1 > 0`를 이용해 마지막 strictness를 만든다.
추가 small-lambda 가정, ratio corollary, L3 또는 repair geometry를 섞지 않는다.

## 2. 재개 기준과 현재 관측의 한계

10/6 로컬 파일·Git 재확인 결과:

| 대상 | 재개 기준 |
| --- | --- |
| NSRW HEAD | `30c8c4fdd4854ee228d9fd6ea1178c8bf716484d` |
| OpenAI source commit | `8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538` |
| source tracked tree | clean; untracked/generated artifacts는 이 검사 범위 밖 |
| source toolchain 선언 | `leanprover/lean4:v4.34.0-rc2` |
| manifest portable Git blob SHA-1 | `f07a8454cb6200d90bcc4371bc9965e9f8f46c7d` |
| 현재 strict-L2 SHA-256 | `624f1aa042377db7e2bbe50ba70d08a35035cddc51697bd5a69a1ce0bd9bbcdd` |
| F1 SHA-256 | `df9f605fa7ad9fa2842f54ae2d67b6a9b1773849d72c695192ae1bebe2f01206` |

NSRW worktree는 **clean이 아니다**. strict proof와 기존 문서 수정 및 새 resource
문서가 있다. 이를 정리한다는 이유로 reset하거나 다른 작업을 덮어쓰지 않는다.
위 표는 재개 전 snapshot이다. 아래 §7의 실제 실행 관측과 구분한다.
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
  comparison을 시작한다. L2만으로 `DeltaM < 0`, `c1 > 0`, first-repair zero를
  승격하지 않는다. 이후 coefficient/amplitude decomposition, continuity, positive
  second-bump tail 및 first-window IVT bridge도 각각 닫아야 한다.

완료 기준은 문서 수나 theorem 파일 존재가 아니라 **exact strict theorem의 검수된
compiled receipt**다. T0–T6는 각각의 receipt 범위에서 닫혔다. L3의
[dated receipt](stage_receipts/P2_L3_COLAB_2026-10-06.md)는 cross-multiplied
template bound만 승격한다. DeltaM composition은 다음 미완료 작업이다.
[세션 index](sessions/P2_L3_SESSION_2026-10-06.md)는 development와 clean replay를
연결하는 기록이며 proof authority가 아니다.

## 5. 별도 안전보수: 주 연구선을 대체하지 않는다

- [ ] **A0 — 다음 authoritative raw-export 소비 전에 TOCTOU 보수.** normalizer가
  projection에 소비한 bytes와 digest를 같은 안정된 bounded snapshot에 묶는다.
  pass 사이 교체 및 projection 중 변경을 테스트한다. 전/후 hash만으로
  mutate-and-restore까지 막았다고 주장하지 않는다. strict-L2 Lean compile 경로는
  이 normalizer를 소비하지 않으므로 A0를 그 compile의 선행조건으로 만들지 않는다.
- [ ] **A1 — runner 안정화 뒤 P2 CI.** 현재 CI 성공과 P2 external compile은 별개다.
  hosted P2 CI를 Colab receipt 작성의 새로운 선행조건으로 만들지 않는다.
- [ ] **A2 — 후순위 정리.** legacy JSON, ledger hex validation, release 링크,
  M5 CI 보수는 별도 patch다. 이번 문서 재개 계획을 새 release/tag로 포장하지 않는다.

## 6. 이번 문서 갱신의 경계

ledger는 증거를 찾는 색인이지 새로운 proof authority가 아니다. source proposition과
그 hypotheses가 수학 의미를 정하고, commit/bytes/run-bound evidence가 실행 사실을
정한다. 충돌하면 보류하고 근거를 대조한다.

수학적 반례, compile/identity admission 실패, 재개 조건은 별도로 기록한다.
`Q`의 global obstruction과 endpoint-first-zero 가설 기각은
로컬 draft `NEGATIVE_RESULT_REGISTER.md`에 보존한다. 이 두 draft는 아직 Git에
포함되지 않았으므로 공개 실행 근거로 사용하지 않는다. 이는 OpenAI theorem의
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
