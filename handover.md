# PetPawCalc 인수인계 문서

최종 갱신: 2026-07-14 (세션 H)
저장소: `canghun13/petpawcalc` (GitHub Pages, Jekyll)
운영 도메인: https://petpawcalc.com

이 문서는 새 대화에서 작업을 이어받을 때 이것만 읽으면 바로 작업 가능하도록 작성됨. 작업할 때마다 이 파일을 최신 상태로 갱신하고 push할 것.

---

## 0. 작업 방식 (중요 — 반드시 읽을 것)

- 사용자가 그날그날 **GitHub Personal Access Token**을 대화에 직접 붙여넣는다. 세션이 끝나면 토큰은 revoke됨 (일회성).
- 토큰 받으면 즉시 `git clone https://<TOKEN>@github.com/canghun13/petpawcalc.git`으로 저장소를 로컬에 받아서 작업.
- **zip 파일을 만들어서 사용자에게 전달하는 방식은 더 이상 쓰지 않는다.** 예전 세션들은 zip 방식이었지만, 지금은 git으로 직접 clone → 수정 → commit → push까지 전부 처리.
- commit/push는 **작업 완료 즉시 바로 실행**해도 됨 (매번 확인받을 필요 없음 — 사용자가 "다음부턴 바로 commit push까지 해도 된다"고 명시적으로 허용함).
- commit 메시지는 무엇을 왜 했는지 구체적으로 남길 것 (다음 세션이나 사용자가 나중에 git log만 보고도 이해할 수 있게).
- 모든 작업 완료 후 **이 handover.md 파일도 최신 상태로 갱신해서 같이 push**할 것. 이게 이제 세션 간 인수인계의 유일한 창구임 (예전처럼 새 채팅에 내용을 요약해서 넘기는 방식 아님).
- 사용자는 "대시보드나 시각화 자료 만들지 말고 텍스트로만 얘기해"라고 요청한 바 있음 — GSC 데이터 분석 시 차트/HTML 아티팩트 만들지 말고 대화 내에서 텍스트로 정리.
- 사용자는 한국어로 대화하며 다혈질적인 어조를 자주 쓴다. 실수했을 때는 변명 없이 인정하고 바로 고칠 것. 안일하게 "기다리면 된다"는 식의 결론은 피하고, 데이터를 실제로 파고들어 액션 아이템을 찾아낼 것.

---

## 1. 사이트 개요

- **주제**: 반려동물(개·고양이) 전용 무료 계산기 + 정보성 블로그
- **스택**: Jekyll (GitHub Pages 빌드), `jekyll-sitemap` + `jekyll-seo-tag` 플러그인 사용 (sitemap.xml은 자동 생성, 저장소에 정적 파일로 존재하지 않음 — 신경 안 써도 됨)
- **수익 모델**: Google AdSense (심사 진행/통과 여부는 사용자가 별도로 관리, 이 문서 갱신 시점 기준 트래픽 자체가 워낙 적어 심사보다 트래픽 확보가 급선무)
- **디자인 톤**: 따뜻한 크림/오렌지 톤, `--font-display`(세리프 헤딩) + `--font-body`, 반려동물 오너 대상 친근한 톤

### 디렉토리 구조
```
_config.yml          # baseurl, permalink(/blog/:slug/), 플러그인, defaults(레이아웃 매핑)
_layouts/
  default.html        # 공통 뼈대, canonical 태그 포함
  post.html           # 블로그 포스트 레이아웃 — Article+FAQPage Schema, 테이블 CSS(table-wrapper), canonical 전부 여기 있음
  tool.html           # 계산기 툴 레이아웃
_includes/
  header.html, footer.html
_posts/               # 블로그 포스트 27개 (2026-MM-DD-slug.md 형식)
tools/                # 계산기 툴 20개 (개별 .html, front matter로 title/description/permalink 지정)
  index.html           # 툴 전체 목록 페이지 (검색 가능)
index.html             # 홈페이지 (툴 카드 전체 노출)
blog/index.html        # 블로그 목록 (Liquid로 site.posts 자동 순회, 신규 포스트 추가해도 별도 수정 불필요)
llms.txt               # LLM 크롤러용 사이트 요약 — 신규 콘텐츠 생성 시 반드시 동기화
CNAME                  # petpawcalc.com (정상 설정 확인됨)
```

---

## 2. 현재 콘텐츠 자산 (2026-07-12 기준)

### 블로그 포스트 27개
날짜순 전체 목록은 `_posts/` 참고. 최근 추가분(2026-07-10, 이번 세션들에서 신규):
- `puppy-kitten-vaccination-schedule` — 백신 계산기 2개의 짝 콘텐츠
- `spay-neuter-cost-and-timing` — Spay/Neuter 계산기 짝 콘텐츠
- `dog-cat-dental-cleaning-cost` — Dental 계산기 짝 콘텐츠
- `pet-euthanasia-cost-and-what-to-expect` — **계산기 없이 순수 정보글로만 작성** (아래 3번 항목 참고, 의도적 선택)

### 계산기 툴 20개 (tools/)
연령: dog-age, cat-age
체중: dog-weight, cat-weight, pet-weight(통합)
발정/임신: dog-heat-cycle, cat-heat-cycle, dog-pregnancy, cat-pregnancy
비용: annual-pet-cost, pet-insurance-cost-estimator, pet-food-calorie
건강/방문: dog-vet-visit-scheduler, cat-vet-visit-scheduler, dog-quality-of-life(Paw Score)
백신: dog-vaccination-schedule-calculator, cat-vaccination-schedule-calculator
수술/케어 비용: spay-neuter-cost-calculator, dental-cleaning-cost-calculator, **pet-grooming-cost-calculator(신규, 7/12)**

모든 신규 툴은 다음 공통 패턴을 따름:
- front matter: `layout: tool`, `title`, `description`, `permalink`
- `<script type="application/ld+json">` 2개: WebApplication Schema + FAQPage Schema
- PDF 저장 기능: `.print-area` 또는 `.result-box` + `doPrint()` JS 함수 + `@media print` CSS
- `.post-cta` div로 관련 툴/블로그 상호 링크
- `.disclaimer-box`, `.no-print`(교육 콘텐츠, 500단어 이상 권장)

---

## 3. 지금까지의 작업 이력 (세션별 요약)

### 세션 A — PDF 다운로드 기능 (7/4)
`window.print()` + print CSS로 5개 계산기(annual-pet-cost, pet-insurance, dog/cat-vet-visit-scheduler, dog-quality-of-life)에 "Save as PDF" 버튼 추가. **여러 차례 시행착오**(빈 페이지, 페이지 중복, 마진 안 잡힘 등)를 거쳐 최종적으로 `@page`를 `@media print` 밖 최상위 룰로 두고, `body { margin: 20mm !important }`가 아니라 **프린트 다이얼로그 자체의 여백 설정("기본"으로)**이 핵심이었음. 이후 만든 모든 신규 툴은 처음부터 이 패턴 그대로 사용.

### 세션 B — SEO 근본 문제 진단 및 수정 (7/4~7/10 초반)
- **핵심 문제 발견**: `_layouts/post.html`에 **Article/FAQPage Schema가 아예 없었음** — 포스트 23개 전부 Schema 없이 배포된 상태. 레이아웃에 한 번 추가해서 전체 일괄 해결.
- **날짜 조작 신호**: 19개 포스트의 front matter `date`가 파일명 날짜와 불일치 (실제로는 5월에 쓴 글인데 6/27, 7/4로 찍혀 있었음) → Google이 이를 조작 신호로 인식해 크롤/색인을 거부했을 가능성 높음 → 전부 파일명 날짜로 통일.
- FAQ 없던 4개 포스트에 FAQ 신규 작성 + 나머지 19개는 기존 FAQ를 파싱해 `faqs:` front matter(Schema용)로 이식.
- 23개 포스트 전부 Related Articles 상호 링크 추가.
- **테이블 CSS 버그**: `border-collapse: collapse` + `border-radius` + `overflow:hidden` 조합이 3컬럼 이상 테이블에서 우측 잘림/가로 스크롤 불가 문제 발생 → `.table-wrapper` div로 JS가 자동 감싸고 `overflow-x: auto`로 해결 (`_layouts/post.html` 안에 있음).

### 세션 C — GSC 데이터 기반 보강 (7/10, 여러 라운드)
GSC Performance 데이터(쿼리별 노출/순위)를 반복적으로 받아서, 순위가 근접한(30~90위권) 쿼리들을 페이지 title/H1/FAQ에 정확히 매칭시키는 작업을 여러 라운드 진행:
- `dog-quality-of-life-calculator`: H1에 "Paw Score" 추가, 인트로에 "free" 추가 (쿼리 "paw score calculator free"가 "paw score calculator"보다 순위 좋았음)
- `how-to-tell-if-cat-is-overweight`: "is my cat fat", "kitten overweight" FAQ 추가
- `what-to-feed-pregnant-dog`: title에 "Diet" 추가 (14개 쿼리 변형 중 절반이 "diet" 포함했는데 title에 없었음)
- `how-much-should-senior-dog-eat`: "feed" 표현 FAQ 추가 (기존엔 "eat" 표현만 있었음)
- `pet-insurance-cost-estimator`, `pet-food-calorie-calculator`: "calculator" 단어, 구체적 수치 예시 FAQ 추가

**교훈**: 순위가 이미 근접한(page 1 근처) 쿼리에 대해, 페이지에 이미 있는 콘텐츠인데 **정확한 문구(exact phrase)가 안 박혀 있어서** 놓치는 경우가 반복적으로 나타남. 새 콘텐츠보다 기존 페이지의 문구 미세조정이 훨씬 빠르고 효과적.

### 세션 D — 고아 페이지(orphan page) 문제 (7/10)
신규 백신 계산기 2개를 만들 때 vet-scheduler로는 링크를 걸었지만 **반대 방향 링크가 없어서** 사이트 내부 링크망에서 고립돼 있던 걸 발견. index/tools-index/footer/llms.txt에는 있어도 콘텐츠 내부 링크가 없으면 Google이 중요도를 낮게 봄 → 이후 신규 툴 만들 때마다 **반드시 관련 허브 페이지(vet-scheduler, age-calculator, annual-cost)에서 역링크 추가**를 체크리스트에 포함.

### 세션 E — 신규 콘텐츠 확장 (7/10)
경쟁사 존재로 수요 검증 후 진행:
- 신규 툴 2개: Spay/Neuter Cost Calculator, Dental Cleaning Cost Calculator (둘 다 dog/cat 통합 단일 페이지, `pet-weight-calculator`의 species-selector 패턴 재사용)
- 짝 블로그 3개: 백신 가이드(기존 계산기의 빠진 짝), Spay/Neuter 가이드, Dental 가이드
- **Pet Euthanasia**: 검색 수요는 있었지만 감정적으로 민감한 주제라 **계산기 형태로 만들지 않기로 사용자와 논의 후 결정** — 계산기 폼 없이 담담한 톤의 순수 정보글로만 작성. 이 판단 기준은 앞으로도 유지: 죽음/상실과 직결된 주제는 "입력→버튼→숫자" UI가 부적절하다고 판단되면 계산기 대신 글로만 다룰 것.

### 세션 F — 2차 보강 (7/12)
GSC 7/12 데이터 확인 → 신규 콘텐츠 필요성 웹 검색으로 검증 → **"Dog Pregnancy Signs" 클러스터(13개 쿼리 변형)는 이미 강자들(Pets4Homes, Daily Paws, PetPace)이 있는 레드오션이라 새 글 대신 기존 `how-to-tell-if-dog-is-pregnant` 포스트 보강으로 처리** (자기잠식 방지). `dog-weight-calculator`도 adult 체중 체크 기능은 이미 있었는데 FAQ가 puppy 위주였던 걸 보강.

### 세션 G — Pet Grooming Cost Calculator 신규 (7/12, 오후)
GSC 쿼리에는 아직 안 잡히지만(=진짜 블라인드 스팟), 웹 검색으로 grooming cost calculator 경쟁사(calculatorsfordogs.com, usecalcpro.com, calculatorian.com, tooliro.com, agentcalc.com) 다수 확인 → 수요 검증됨. 기존 19개 툴 grep 검색으로 중복 없음 확인 후 신규 제작.
- `pet-grooming-cost-calculator.html`: dog/cat 통합, 사이즈(dog만)+coat type+grooming frequency 입력 → 연간 비용 추정 (전문 그루밍 + 홈케어 용품 비용 분리 표시)
- `annual-pet-cost-calculator`, `dog-vet-visit-scheduler`에서 역링크 추가 (고아 페이지 방지 원칙 계속 적용)
- 공통 파일 4종(index, tools/index, footer, llms.txt) 동기화, 오래된 "New" 배지(spay-neuter, dental) 정리하고 이번 신규분으로 이동

### 세션 H — GSC/GA 구조적 문제 발견 + Tool 페이지 FAQ 가시화 (7/14, 주간 작업)

**GA 데이터(6/16~7/13)**: 활성 사용자 72명, 신규 71명. 유입은 여전히 (direct)/pitchwall.co/Findly.tools 등 런칭 디렉토리 위주고 organic(google+bing)은 4명뿐 — 검색 유입 자체가 아직 미미한 단계.

**GSC Performance(5/13~7/14) 핵심 발견**:
1. **구조적 문제 발견 — tools/ 20개 전부 "FAQ가 schema에만 있고 본문에 안 보임"**: `_layouts/post.html`은 `faqs:` front matter를 스키마로만 렌더링하는데, 블로그 포스트는 마크다운 본문에 FAQ를 **수동으로 별도 작성**해서 가시적 텍스트가 있었던 반면(세션 B 확인), tools/ 파일들은 FAQPage 스키마만 JSON-LD에 박아넣고 본문엔 그 질문/답이 텍스트로 노출된 적이 없었음. 이번 세션 전까지 아무도 몰랐던 사각지대. Google 입장에서 스키마에만 있고 화면에 없는 FAQ는 신뢰도가 낮고(가이드라인상 FAQ 리치결과는 보이는 콘텐츠 기준), 무엇보다 "정확한 쿼리 문구가 텍스트에 박혀야 한다"는 세션 C의 핵심 교훈이 tools 20개에는 전혀 적용이 안 되고 있었던 셈.
   - 이번 세션에서 노출 상위 6개 tool에 **가시적 FAQ 섹션(`<h2>Frequently Asked Questions</h2>` + h3/p 페어)을 신규 추가**: `pet-weight-calculator`, `cat-weight-calculator`, `pet-food-calorie-calculator`, `pet-insurance-cost-estimator`, `dog-weight-calculator`, `dog-quality-of-life-calculator`. 기존 스키마 질문을 그대로 본문에 노출시킨 것이라 콘텐츠 리스크 없음(신규 주장 없음, 검증만 하면 됨).
   - **나머지 14개 tool 페이지(dog/cat-age, heat-cycle, pregnancy, vet-scheduler, vaccination, annual-cost, spay-neuter, dental, grooming 등)는 아직 미적용 — 다음 세션 우선순위**. 노출 낮은 순으로 미뤄도 되지만, 이 패턴 자체가 재현 가능한 작업이라 다음 세션에 나머지도 일괄 적용 권장.
2. **cat-weight-calculator FAQ 신규 1개 추가 — "feline bmi calculator" 쿼리(3 노출) 대응**: 웹 검색으로 확인한 결과 실제로 "FBMI(Feline Body Mass Index)" 공식이 존재함(Butterwick 2000 논문 기반, 갈비뼈 둘레/뒷다리 길이로 계산) — 처음엔 "고양이는 BMI가 없다"고 잘못 쓸 뻔했다가 검색으로 사실관계 정정함. 다만 이 쿼리는 omnicalculator.com, cats.com, embrace 펫보험, catcalculator.com 등 고권위 경쟁사가 이미 다수 장악한 데다 검색량 자체가 극히 낮아(3 노출) 전용 계산기 신설은 보류 — 기존 cat-weight-calculator에 정확한 사실 기반 FAQ만 추가해 대응.
3. **pet-insurance-cost-estimator**: "pet insurance calculator"(4 노출)·"pet insurance estimate"(4 노출) 등 정확 문구가 스키마 질문명에 없었음 → 스키마+본문 질문 문구를 "Is there a free pet insurance calculator?"로 통일.
4. **큰 표본 크기의 CTR 이상 신호 1건 발견, 원인 미확정**: `what-to-feed-pregnant-dog` 포스트가 101 노출·27위인데 클릭 0건(이 정도 노출/순위면 통계적으로 눈에 띄는 이상치). 쿼리 목록 중 "pregnant dog symptoms"(1노출, 27위)가 이 페이지 평균 순위와 정확히 일치하는데, 이 포스트는 "먹이는 법(feed)" 주제이고 "증상(symptoms)"은 별도 포스트(`how-to-tell-if-dog-is-pregnant`, 54노출·77위)가 담당 — **두 페이지 간 자기잠식(cannibalization) 가능성 의심되지만, 이번 GSC 내보내기는 페이지×쿼리 교차표가 아니라서 확정 불가**. 다음 세션에서 GSC 웹 UI로 이 두 URL을 직접 필터링해서 교차 확인 필요 — 확정되면 what-to-feed 포스트에서 증상 언급을 최소화하고 대신 how-to-tell-if 포스트로 명확히 연결하는 정리가 필요할 수 있음.
5. **신규 콘텐츠는 만들지 않기로 결정**: GSC 쿼리를 전수 분류한 결과 대부분 기존 27개 포스트+20개 tool로 이미 커버되고 있었고(위 1~3번은 보강), 나머지 미매칭 쿼리는 대부분 (a) 비영어권 쿼리, (b) "pet alliance calculator"/"fido score calculator"/"journeys home quality-of-life calculator" 같은 **경쟁사 브랜드명 검색**(대응 불가), (c) 노출 1~2회의 통계적 노이즈였음. 진짜 새로운 수요 클러스터는 발견되지 않음 — 이번 주는 순수 보강 위주.
6. **Coverage 리포트**: "발견됨-미색인" 38개, 그대로 — 세션 F 때와 동일한 숫자. 여러 세션째 변화 없어 Coverage 리포트 갱신 지연이 의심되는 세션 F 가설이 유지됨. Performance 리포트의 차트(일별 노출) 기준으로는 7/8~7/11에 노출이 23→39→61→80으로 뚜렷하게 증가 중 — 실제로는 색인/트래픽이 진행되고 있는 것으로 보임.

---

## 4. GSC 색인 현황 (7/14 기준)

- **심각한 문제**: "발견됨-미색인" 38개, "크롤링됨-미색인" 3개, "리디렉션 포함 페이지" 3개(→ **사용자 지시로 무시**) — 세션 F(7/12) 때와 완전히 동일한 숫자. 2세션 연속 변화 없음 확인 — Coverage 리포트 자체가 갱신 지연이 있는 것으로 보이며, **실제 상태는 Performance 리포트(쿼리/페이지별 노출)가 더 정확한 지표**로 판단하고 있음.
- Performance 리포트 기준 일별 노출은 7/8(41) → 7/9(39) → 7/10(61) → 7/11(80)로 최근 뚜렷하게 증가 추세. 실제로 색인/트래픽이 진행되고 있다는 신호.
- 사이트 전체가 아직 authority가 낮은 신생 사이트라 대부분의 쿼리가 30~90위권. 여전히 클릭이 거의 없음(2개월 누적 실질 클릭 1~2건 수준) — **수익화(AdSense) 관점에서 지금 단계의 최우선 순위는 신규 콘텐츠가 아니라 "이미 노출은 있는 페이지의 순위/CTR 개선"** (세션 H에서 이 판단으로 tool 페이지 FAQ 가시화 작업 진행).
- **"petcalculators.xyz", 헝가리어/네덜란드어 등 비영어권 쿼리, "pet alliance calculator"/"fido score calculator" 등 경쟁사 브랜드 검색은 의도적으로 무시** — 온페이지로 해결 안 되는 authority/언어/브랜드 문제.

### 순위 근접 페이지 (다음 라운드에서 우선 재확인할 것)
- `dog-quality-of-life-assessment` (포스트): 4.33위, 노출 3개뿐 — 표본이 작아 CTR 판단 보류, 노출 늘어나면 재확인
- `how-often-vet-visits-dog-cost-by-age`: 5.8위, 노출 10개, 클릭 0 — 표본 작지만 최상위권에서 클릭 0은 계속 지켜볼 것
- `how-much-should-senior-dog-eat`: 14.1위, 노출 149개(전체 최다), **클릭 2건 — 사이트에서 유일하게 클릭이 나오는 페이지**. CTR 1.34%는 순위 대비 정상 범위, 추가 여지는 크지 않음
- `what-to-feed-pregnant-dog`: 27위, 노출 101개(두 번째로 많음), **클릭 0건 — 표본 크기 대비 이상 신호**. 원인 후보: `how-to-tell-if-dog-is-pregnant`와의 자기잠식 의심(세션 H 4번 참고, 미확정)
- `dog-age-calculator`, `cat-age-calculator`, `dog-vaccination-schedule-calculator`: 11~15위권 — 안정적, 계속 지켜볼 것
- `dog-weight-calculator`: 66.65위, 노출 31개 — 세션 F에서 adult 체중 FAQ 보강, 세션 H에서 FAQ 가시화 추가 — 다음 데이터에서 순위 변화 확인
- `cat-weight-calculator`: 49.69위, 노출 16개 — 세션 H에서 FAQ 가시화 + BMI 문항 추가, 다음 데이터에서 확인
- `pet-weight-calculator`: 34.75위, 노출 12개 — 이미 준수한 순위, 세션 H에서 FAQ 가시화 추가

---

## 5. 앞으로 작업할 때 체크리스트

### 신규 콘텐츠(툴/블로그) 만들 때
1. **기존 파일과 중복 체크 먼저** — `_posts/`, `tools/` 목록 grep해서 겹치는 주제 없는지 확인
2. 웹 검색으로 키워드 경쟁 강도 확인 — 이미 강자 있는 레드오션이면 신규 글보다 기존 페이지 보강을 우선 고려
3. 감정적으로 민감한 주제(안락사 등)는 계산기 형태가 적절한지 먼저 판단, 애매하면 사용자에게 먼저 물어볼 것
4. 신규 파일 만들면:
   - front matter 패턴 기존 파일 그대로 따르기 (title/description/permalink 또는 slug/category/date/read_time/faqs)
   - Schema(WebApplication+FAQPage 또는 Article+FAQPage) 반드시 포함, JSON 유효성 `python3 -c "json.loads(...)"`로 검증
   - `.post-cta`로 관련 페이지 최소 1~2개 상호 링크
   - **반드시 역방향 링크도 추가할 것** (고아 페이지 방지 — 세션 D 참고)
5. 공통 파일 4종 동기화: `index.html`, `tools/index.html`, `_includes/footer.html`, `llms.txt`
   - `blog/index.html`은 Liquid 자동 순회라 신규 포스트 추가 시 손댈 필요 없음
   - "New" 배지는 최근 것만 유지, 오래된 건 정리 (배지 남발 방지)

### 보강 작업할 때
1. GSC Performance 데이터에서 순위 30~90위권, 노출 있는 쿼리 확인
2. 해당 쿼리가 이미 존재하는 페이지와 매칭되는지 확인 (대부분 매칭됨 — 신규 콘텐츠보다 보강이 우선)
3. 페이지의 title/H1/FAQ에 **정확한 쿼리 문구가 그대로 박혀 있는지** 확인 — 없으면 추가 (세션 C의 반복된 패턴)
4. front matter `faqs:` 배열과 본문 `## Frequently Asked Questions` 섹션 **양쪽 다** 동일하게 추가할 것 (Schema용 + 가시적 텍스트용)
5. **tools/ 페이지는 FAQ가 스키마에만 있고 본문에 안 보이는 경우가 많음(세션 H에서 발견, 20개 중 14개 아직 미해결) — 보강 작업 시 항상 먼저 확인하고, 없으면 스키마 질문 그대로 `<h2>Frequently Asked Questions</h2>` + h3(질문)/p(답변) 페어로 본문에 노출시킬 것.** 새 주장을 만드는 게 아니라 이미 있는 스키마 텍스트를 화면에 노출만 시키는 작업이라 리스크가 낮음 — 이 패턴을 다음 세션에서 나머지 14개 tool에도 일괄 적용 권장.
6. FAQ에 새 사실을 추가할 때는(예: "OO 계산기 있나요?" 류) **반드시 웹 검색으로 사실관계부터 확인** — 세션 H에서 "고양이는 BMI가 없다"고 쓸 뻔했다가 검색으로 FBMI 공식이 실제 존재함을 확인하고 정정한 사례 있음. 확신에 근거해 서술하지 말고 검색으로 검증할 것.

### 검증 습관
- 파일 수정 후 `<div>` 개수 짝 맞는지 python으로 체크 (`c.count('<div')` vs `c.count('</div>')`)
- YAML front matter는 `yaml.safe_load()`로 파싱 검증
- JSON-LD Schema는 `json.loads()`로 검증
- 전부 검증 통과 후에만 commit

### 절대 하지 말 것
- `@page` CSS를 `@media print` 안에 중첩 (무시됨, 최상위에 둘 것)
- `position: absolute`/`fixed`를 print 영역에 사용 (빈 페이지/페이지 중복 유발 — 세션 A 참고)
- 안일하게 "기다리면 된다"고 결론 내고 데이터 안 파는 것 — 사용자가 이 부분에 대해 강하게 지적한 바 있음
- 신규 페이지 만들고 역링크 깜빡하는 것

---

## 6. 다음에 확인해야 할 것 (Open Items)

- **최우선: 나머지 tool 페이지 14개에 가시적 FAQ 섹션 적용** (세션 H에서 6개만 처리함) — dog/cat-age-calculator, dog/cat-heat-cycle, dog/cat-pregnancy-calculator, dog/cat-vet-visit-scheduler, dog/cat-vaccination-schedule-calculator, annual-pet-cost-calculator, spay-neuter-cost-calculator, dental-cleaning-cost-calculator, pet-grooming-cost-calculator. 패턴은 세션 H 커밋 참고 — 스키마 질문을 그대로 h3/p로 본문에 노출.
- **`what-to-feed-pregnant-dog`(101 노출) vs `how-to-tell-if-dog-is-pregnant`(54 노출) 자기잠식 의심 — GSC 웹 UI에서 두 URL 필터로 실제 쿼리 교차 확인 필요** (이번 zip 내보내기는 페이지×쿼리 교차표가 없어 이 세션에선 확정 불가). 겹치는 게 확인되면 what-to-feed 포스트의 증상 관련 서술을 줄이고 how-to-tell-if 포스트로 명확히 유도.
- Spay/Neuter, Dental Cleaning, Pet Grooming 계산기는 아직 GSC Performance에 노출 데이터가 부족(너무 최근) — 다음 데이터에서 첫 노출/순위 확인
- 세션 H에서 FAQ 가시화한 6개 tool(`pet-weight`, `cat-weight`, `pet-food-calorie`, `pet-insurance-cost-estimator`, `dog-weight`, `dog-quality-of-life`)의 다음 GSC 데이터에서 순위/노출 변화 확인
- `pet-euthanasia-cost-and-what-to-expect` 포스트는 영어 톤 검수를 사용자가 직접 하지 못한 상태("나 영어는 잘 몰라서 톤은 모르는데") — 필요시 재검토 여지 있음
- Coverage 리포트의 "발견됨-미색인 38개"가 세션 F(7/12)·세션 H(7/14) 2회 연속 완전히 동일한 숫자로 나옴 — 다음 데이터에서도 그대로면 Performance 데이터만으로는 안 보이는 다른 근본 원인이 있을 수 있으니 재점검 필요 (예: Coverage 리포트 자체가 이 사이트 규모에서는 갱신 주기가 매우 긴 것일 수도 있음)
