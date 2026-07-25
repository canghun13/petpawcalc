# PetPawCalc 인수인계 문서

최종 갱신: 2026-07-22 (세션 O)
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
_config.yml          # baseurl, permalink(/blog/:slug/), 플러그인, defaults(레이아웃 매핑 — posts/tools/checklists 경로별 지정)
_layouts/
  default.html        # 공통 뼈대, canonical 태그 포함
  post.html           # 블로그 포스트 레이아웃 — Article+FAQPage Schema, 테이블 CSS(table-wrapper), canonical 전부 여기 있음
  tool.html            # 계산기 툴 레이아웃
  checklist.html       # 체크리스트 레이아웃(세션 M 신규) — 체크박스 localStorage 저장/진행률바/프린트 공용 JS가 여기 있음(개별 체크리스트 파일엔 JS 없이 마크업만)
_includes/
  header.html, footer.html
_posts/               # 블로그 포스트 33개 (2026-MM-DD-slug.md 형식)
tools/                # 계산기 툴 22개 (개별 .html, front matter로 title/description/permalink 지정)
  index.html           # 툴 전체 목록 페이지 (검색 가능)
checklists/            # 체크리스트 3개(세션 M 신규) — tools/와 동일 패턴(front matter, permalink)
  index.html           # 체크리스트 목록 페이지
index.html             # 홈페이지 (툴 카드 전체 노출)
blog/index.html        # 블로그 목록 (Liquid로 site.posts 자동 순회, 신규 포스트 추가해도 별도 수정 불필요)
llms.txt               # LLM 크롤러용 사이트 요약 — 신규 콘텐츠 생성 시 반드시 동기화
css/style.css           # 전역 스타일시트 — table-wrapper, checklist-* 등 여러 레이아웃이 공유하는 CSS는 반드시 여기(스코프 없이) 넣을 것. _layouts/post.html처럼 특정 레이아웃 안에 스코프해서 넣으면 다른 레이아웃(tool.html 등)에서 안 먹는 버그가 남(세션 M에서 실제로 발생, 아래 참고)
CNAME                  # petpawcalc.com (정상 설정 확인됨)
```


---

## 2. 현재 콘텐츠 자산 (2026-07-15 기준)

### 블로그 포스트 33개
날짜순 전체 목록은 `_posts/` 참고. 최근 추가분:
- `puppy-kitten-vaccination-schedule`, `spay-neuter-cost-and-timing`, `dog-cat-dental-cleaning-cost` — 각 계산기의 짝 콘텐츠 (7/10)
- `pet-euthanasia-cost-and-what-to-expect` — **계산기 없이 순수 정보글로만 작성** (아래 3번 항목 참고, 의도적 선택)
- `cat-quality-of-life-assessment` — 세션 I. 사이트에서 유일하게 dog만 있고 cat이 없던 비대칭 항목을 발견해 제작. `dog-quality-of-life-assessment`와 완전히 동일한 HHHHHMM 스케일 구조지만, 고양이가 통증/질병을 숨기는 습성 때문에 그루밍 중단·점프 기피·litter box 회피 등 고양이 특화 신호로 새로 작성.
- `what-to-feed-pregnant-cat`, `how-to-reduce-vet-costs-for-cats`(세션 K), `how-to-tell-if-cat-is-pregnant`(세션 L) — dog 전용으로만 있던 포스트의 cat 짝을 채움(세션 I의 "dog/cat 페어링 빈 자리 점검" 방법론을 blog에도 적용). 이 세 페어링 빈 자리는 세션 L 기준 모두 해소됨.
- `kitten-weight-chart-by-breed-size`(세션 M, 7/17) — 사이트에서 두 번째로 노출 많고 순위도 가장 좋은(9.66위, 29노출) 최고 성과 포스트 `puppy-weight-chart-by-breed-size`의 cat 짝이 없었던 걸 발견해 신규 제작.
- `flea-tick-prevention-cost`(세션 M, 7/17) — **사이트에 전혀 없던 완전 신규 카테고리(구충제/기생충 예방 비용)**. 신규 계산기 `flea-tick-prevention-cost-calculator`의 짝 콘텐츠. 자세한 내용은 세션 M 6번 항목 참고.

### 구조 변경 (세션 M, 7/17): "Checklists" 신규 최상위 섹션
`Tools`/`Blog`에 이은 사이트의 **세 번째 콘텐츠 축**. `/checklists/` 경로, 전용 레이아웃(`_layouts/checklist.html`), nav에 탭 추가(`Tools | Checklists | Blog | About | Contact`). 인터랙티브 체크박스(localStorage로 진행상황 저장) + 인쇄/PDF 저장 기능. 자세한 배경과 콘텐츠 목록은 아래 "세션 M — 카테고리 확장" 항목 참고.

### 계산기 툴 22개 (tools/)
연령: dog-age, cat-age
체중: dog-weight, cat-weight, pet-weight(통합)
발정/임신: dog-heat-cycle, cat-heat-cycle, dog-pregnancy, cat-pregnancy
비용: annual-pet-cost, pet-insurance-cost-estimator, pet-food-calorie
건강/방문: dog-vet-visit-scheduler, cat-vet-visit-scheduler
삶의 질: dog-quality-of-life(Paw Score), cat-quality-of-life(Paw Score) — 세션 I 신규
백신: dog-vaccination-schedule-calculator, cat-vaccination-schedule-calculator
수술/케어 비용: spay-neuter-cost-calculator, dental-cleaning-cost-calculator, pet-grooming-cost-calculator
**구충/예방 비용**: flea-tick-prevention-cost-calculator — 세션 M 신규, 사이트 최초의 "구충제/기생충 예방" 카테고리

**tools/ 21개 전부 FAQ 본문 가시화 완료(세션 L 기준)** — dog/cat 페어링도 전부 완성 상태(비교/통합형 6개 제외 전부 페어 존재).

모든 신규 툴은 다음 공통 패턴을 따름:
- front matter: `layout: tool`, `title`, `description`, `permalink`
- `<script type="application/ld+json">` 2개: WebApplication Schema + FAQPage Schema
- PDF 저장 기능: `.print-area` 또는 `.result-box` + `doPrint()` JS 함수 + `@media print` CSS
- `.post-cta` div로 관련 툴/블로그 상호 링크
- `.disclaimer-box`, `.no-print`(교육 콘텐츠, 500단어 이상 권장)
- **FAQ는 스키마뿐 아니라 본문에도 `<h2>Frequently Asked Questions</h2>` + h3/p로 가시화할 것** (세션 H에서 발견된 사각지대, 세션 L 기준 기존 tool 전부 소급 적용 완료 + 신규 제작 시 처음부터 반영)

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

### 세션 I — "신규 할 만한 거 진짜 없냐"는 재확인 요청에 따른 재조사 (7/14, 같은 날 후속 세션)

세션 H에서 "신규 콘텐츠 없음"으로 결론 냈던 걸 사용자가 재검증 요청 → 다시 파고든 결과 **사이트 자체의 구조적 비대칭을 발견**:

- **모든 카테고리(연령/체중/발정/임신/백신/비용/vet-visit)는 dog·cat 페어로 존재하는데, Quality of Life(Paw Score)만 dog 전용이고 cat 버전이 없었음.** 세션 H에서는 GSC 쿼리 매칭에만 집중하느라 "사이트 자체 구조의 빈 자리"를 놓쳤던 것 — 신규 콘텐츠 판단 기준에 "GSC 쿼리 매칭"뿐 아니라 "우리 사이트 자체의 페어링 패턴 대비 빠진 게 있는지"도 포함해야 한다는 교훈.
- 웹 검색으로 확인: HHHHHMM Scale(Villalobos)은 원래 dog/cat 공용으로 개발된 스케일이고, 실제로 Omnicalculator·Catster·VCA·Ask My Cats 등에서 "cat quality of life calculator"가 이미 존재함 — 즉 수요와 선례가 명확히 있고, 경쟁 강도도 (Omnicalculator 정도를 빼면) 소규모 사이트들 위주라 아주 심한 레드오션은 아님.
- **신규 제작**: `tools/cat-quality-of-life-calculator.html` + `_posts/2026-07-14-cat-quality-of-life-assessment.md`. `dog-quality-of-life-calculator.html`/`dog-quality-of-life-assessment.md`와 완전히 동일한 구조(HHHHHMM 7개 카테고리, 스코어링 로직, PDF 저장)를 재사용하되, 힌트/본문 텍스트는 고양이 특화로 전부 새로 씀 — 특히 Hygiene 카테고리는 dog는 "청결 유지/욕창"이 핵심인데 cat은 "그루밍을 스스로 하는지 여부"가 핵심이라 완전히 다르게 작성(그루밍 중단이 고양이 쇠약의 초기 신호로 가장 유용), Mobility는 "산책"이 아니라 "점프·litter box 접근"으로, Happiness는 "숨는 행동"이 핵심 신호로.
- **역링크(고아 페이지 방지) 4곳에 추가**: `dog-quality-of-life-calculator.html`(post-cta로 cat 버전 링크), `dog-quality-of-life-assessment.md`(Related Articles), `pet-euthanasia-cost-and-what-to-expect.md`(Related Articles), `how-much-should-senior-cat-eat.md`(Related Articles, dog 버전의 senior-dog-eat 포스트가 이미 dog QoL 링크 갖고 있던 것과 대칭 맞춤).
- **공통 파일 4종 동기화 확인**: `index.html`·`tools/index.html`에 cat QoL 카드 추가 + New 배지를 이 카드로 이동(기존 dog-vaccination/cat-vaccination/pet-grooming의 오래된 New 배지 제거). `llms.txt`에 툴/블로그 항목 각 1개씩 추가. **`footer.html`은 원래 20개 툴 중 13개만 싣는 큐레이션된 목록이고 dog-quality-of-life도 애초에 없었어서, 대칭성 유지 차원에서 footer는 그대로 둠**(의도적 결정, 빠뜨린 게 아님). sitemap.xml은 `jekyll-sitemap` 플러그인이 자동 생성하는 정적 파일이 아니므로 손댈 필요 없음(세션 A 이전부터 확인된 사항).
- **세션 H 이전 작업(tool FAQ 가시화)과의 연계**: 신규 cat 계산기는 처음부터 본문에 가시적 FAQ 섹션을 포함해서 제작 — 세션 H에서 발견한 "tools/는 스키마만 있고 본문에 안 보임" 문제를 신규 제작 시점부터 반복하지 않도록 반영함.

**교훈**: "신규 콘텐츠 없음" 결론은 GSC 쿼리 매칭 관점에서만 봤을 때 맞았을 뿐, **사이트 자체 콘텐츠 구조를 페어/패턴 단위로 다시 훑어보는 별도의 체크가 필요**하다는 게 이번 세션의 핵심 교훈. 다음에 신규 콘텐츠 유무를 판단할 때는 (1) GSC 쿼리 미커버 클러스터 확인 + (2) **사이트 자체의 dog/cat 페어링 등 구조적 패턴에 빠진 게 없는지 확인**, 이 두 가지를 모두 체크할 것.

### 세션 J — Coverage "크롤링됨/발견됨-미색인" 정밀 분석 + 미색인 tool 7개 FAQ 가시화 (7/15)

사용자 요청: 새 GSC Performance/Coverage 내보내기(7/15) 확인 후, 특히 **"크롤링됨-현재 색인이 생성되지 않음"과 "발견됨-현재 색인이 생성되지 않음"** 두 카테고리를 꼼꼼히 분석. 신규 콘텐츠는 중복 체크 + 경쟁강도 웹 검색 후 판단. 대시보드/시각화 없이 텍스트로만 보고.

**1. Coverage 수치 자체는 개선 중 — "그대로 38개"였던 세션 F/H 때와 다름**
- 이번 Coverage 내보내기: 크롤링됨-미색인 6개, 발견됨-미색인 15개 (합계 21개) + 적절한 표준 태그 대체 페이지 1개(무해, 정상적인 canonical 처리) + 리디렉션 포함 3개(사용자 지시로 계속 무시).
- 세션 F(7/12)·세션 H(7/14) 때는 "발견됨-미색인 38개"로 2세션 연속 동일했는데, 이번엔 **21개로 감소** — 실제로 색인이 진행되고 있다는 명확한 신호. "기다리면 된다"가 아니라 데이터로 확인된 진전.

**2. Coverage 리포트는 URL 목록을 안 주기 때문에, Performance 페이지 목록과 대조해서 "미색인 추정 URL"을 직접 역산함**
- 방법: 사이트 전체 URL(tools 21개+tools 인덱스, 포스트 28개, 홈/about/contact/privacy/disclaimer/blog 인덱스/tools 인덱스 = 총 56개) vs Performance `페이지.csv`에 노출이 잡힌 33개 URL을 diff.
- **주의**: 포스트 URL을 파일명에서 바로 유추하면 안 됨 — 일부 포스트는 front matter `slug:`가 파일명과 다름(예: `true-cost-cat-vs-dog.md`의 실제 slug는 `true-cost-cat-vs-dog-year-by-year`). 반드시 `grep "^slug:"`로 실제 slug를 확인해서 URL을 만들 것. 이걸 놓치면 오탐이 남(이번 세션에서 실제로 한 번 오탐 냈다가 재검증해서 바로잡음).
- 결과: 23개 URL이 Performance에 노출 0 (Coverage의 21개 미색인과 거의 일치, 소폭 오차는 GSC 집계 시점 차이로 추정) — tools 7개 + blog posts 16개.

**3. 이 과정에서 진짜 버그 하나 발견 및 수정: 깨진 내부 링크**
- `_posts/2026-06-18-how-much-does-a-cat-vet-visit-cost.md`가 `/blog/true-cost-cat-vs-dog/`로 링크 걸었는데, 실제 해당 포스트의 slug는 `true-cost-cat-vs-dog-year-by-year`라서 **404 링크**였음. `/blog/true-cost-cat-vs-dog-year-by-year/`로 수정.
- 전체 저장소(_posts, tools, index, footer, llms.txt 등)에서 슬러그/파일명 불일치로 인한 깨진 링크를 파이썬으로 전수 스캔 — 이 1건 외에는 없음을 확인.

**4. 미색인 tool 7개 — 원인 분석 및 FAQ 가시화 작업**
- 미색인 tool: `annual-pet-cost-calculator`, `cat-pregnancy-calculator`, `cat-vet-visit-scheduler`, `dog-heat-cycle-calculator`, `dog-pregnancy-calculator`, `pet-grooming-cost-calculator`, `spay-neuter-cost-calculator` — 전부 세션 H에서 발견한 "FAQ가 스키마에만 있고 본문에 안 보이는" 문제가 있었음(그리고 이 7개는 세션 H/I가 미처리로 남긴 14개 중 일부).
- **단, FAQ 비가시성이 미색인의 유일한 원인은 아님** — 같은 문제를 가진 tool 7개(`cat-age`, `cat-heat-cycle`, `cat-vaccination-schedule`, `dental-cleaning-cost`, `dog-age`, `dog-vaccination-schedule`, `dog-vet-visit-scheduler`)는 FAQ 미가시 상태에서도 이미 색인됨. 상관관계는 있지만 인과관계 단정은 보류.
- **`dog-pregnancy-calculator`/`cat-pregnancy-calculator`가 특히 우선순위 높음**: "dog pregnancy diagnosis/confirmation/check/signs" 등 관련 쿼리 노출을 합치면 20회 이상 되는데, 정작 계산기 자체는 미색인. 이미 인기 포스트(`how-to-tell-if-dog-is-pregnant`, 80노출)에서 역링크도 걸려있어 내부링크 문제는 아님 — 순수하게 페이지 자체의 콘텐츠 품질/신선도 신호 문제로 판단, FAQ 가시화로 대응.
- `annual-pet-cost-calculator`는 site: 검색으로 실제 미색인 확인, 경쟁 강도 웹서치 결과 calcuja.com/pawcalculator.com/petcalc.com/petcost-calculator.com/petcostestimator.com 등 콘텐츠량이 훨씬 많은 경쟁자가 다수 — 레드오션. 신규 페이지보다 기존 페이지 보강이 맞는 판단.
- **작업**: 위 7개 tool 전부에 기존 FAQPage 스키마 질문/답변을 그대로 본문에 `<h2>Frequently Asked Questions</h2>` + h3/p 페어로 노출 (세션 H 패턴 그대로 재사용, 신규 주장 없음). 스키마 질문 리스트와 본문 h3 리스트를 코드로 1:1 대조해서 전부 일치 확인. div 개수도 파일별로 open/close 매칭 확인.
- 이제 21개 tool 중 FAQ 가시화 완료 = 7(세션 H) + 1(세션 I, cat-quality-of-life는 신규 제작 시 처음부터 포함) + 7(세션 J) = **15개 완료, 6개 남음**(`cat-age`, `cat-heat-cycle`, `cat-vaccination-schedule`, `dental-cleaning-cost`, `dog-age`, `dog-vaccination-schedule`, `dog-vet-visit-scheduler` — 정확히는 7개, 위 문단과 동일 리스트). 이 6~7개는 이미 색인된 페이지들이라 우선순위는 낮지만, 다음 세션에서 마저 처리 권장(패턴 재현이라 빠르게 끝남).

**5. 미색인 blog 포스트 16개 — 대부분 "오래된 페이지가 아직 재크롤 안 된 것"으로 판단, 신규 보강 없이 관찰**
- 16개 전부 세션 B(7/4~7/10)의 날짜조작 수정 **이전에 작성된 포스트**(5/1~6/18 사이, `cat-quality-of-life-assessment` 7/14 제외 — 이건 너무 최근이라 미색인이 당연함). 반면 6/22 이후 작성된 포스트 7개는 전부(100%) 색인됨.
- 이 패턴은 세션 B에서 고친 "front matter 날짜가 파일명과 불일치"(조작 신호로 Google이 인식했을 가능성) 문제가, **레이아웃 차원에서 스키마를 넣어도 이미 한 번 안 좋게 평가받은 개별 URL은 Google이 알아서 재크롤하기 전까지 그대로 남는다**는 가설을 강하게 뒷받침함. Coverage 미색인 수가 38→21로 줄어든 것도 이 가설과 일치(Google이 순차적으로 재평가 중).
- 이 16개는 다음 특징 확인: 전부 관련 계산기/타 포스트로부터 정상적인 역링크 있음(고아 페이지 아님), FAQ도 포스트 레이아웃 특성상 이미 본문에 가시적으로 있음(세션 B에서 전체 적용됨) — 즉 **온페이지 요인으로 설명되는 문제가 아니라 크롤 스케줄/신뢰도 누적 문제**로 판단, 이번 세션엔 콘텐츠 수정 안 함.
- 다음 세션에서도 여전히 미색인이면(특히 `dog-age-human-years`처럼 5/1 작성 후 2.5개월째 미색인인 최고령 케이스), 그때는 GSC UI에서 "색인 생성 요청"을 사용자가 직접 눌러보는 것을 고려. 이건 에이전트가 GSC API 접근 권한이 없어 직접 할 수 없음 — 사용자에게 요청 필요.

**6. GSC 쿼리 데이터(191개 전체 확인) — 신규 콘텐츠 클러스터 없음, 세션 H/I 결론과 동일**
- 노출 3회 이상 쿼리는 전부 기존 27개 포스트+21개 tool로 커버됨. 4회 미만 쿼리는 비영어권/경쟁사 브랜드명/노이즈로 세션 H와 동일하게 분류.
- **AdSense 수익화 관점 우선순위 판단**: 신규 콘텐츠보다 (a) 미색인 페이지 색인 유도(FAQ 가시화 등 온페이지 신호 강화)와 (b) 이미 노출 있는 페이지 순위 개선이 압도적으로 ROI가 높음 — 트래픽 자체가 아직 거의 없는 단계라 신규 페이지를 늘려봐야 같은 문제(미색인)가 반복될 뿐. 이 판단은 세션 H부터 계속 유지 중.

**다음 세션 우선순위**:
1. 나머지 tool 7개(`cat-age`, `cat-heat-cycle`, `cat-vaccination-schedule`, `dental-cleaning-cost`, `dog-age`, `dog-vaccination-schedule`, `dog-vet-visit-scheduler`) FAQ 가시화 마무리 — 이미 색인된 페이지라 급하진 않지만 패턴 통일 차원에서 정리.
2. Coverage "발견됨/크롤링됨-미색인" 21개 → 다음 데이터에서 숫자가 계속 줄어드는지 확인(38→21 추세가 이어지는지). 안 줄어들면 개별 URL 재크롤 요청을 사용자에게 권유.
3. `dog-pregnancy-calculator`/`cat-pregnancy-calculator`가 다음 데이터에서 색인되는지 우선 확인(수요가 명확한 페이지라 색인만 되면 바로 노출 기대).
4. 세션 H의 미해결 이슈(`what-to-feed-pregnant-dog` vs `how-to-tell-if-dog-is-pregnant` 자기잠식 의심)는 이번에도 GSC UI 교차확인 없이는 미확정 — 여전히 열린 항목.

### 세션 K — "확장을 안 하고 있다"는 사용자 피드백에 따른 신규 콘텐츠 재추진 (7/15, 세션 J 직후 후속)

세션 J까지는 보강 위주였고, 사용자가 "주간 작업 때도 확장을 안 한 것 같다, 조금씩이라도 확장은 해야 한다"고 명확히 피드백함. 이에 따라 신규 콘텐츠 후보를 체계적으로 웹 검색하며 경쟁강도를 확인:

**레드오션으로 판단해 보류한 후보들** (전부 웹 검색으로 경쟁사 확인 후 기각):
- **Dog Exercise Calculator**: SpotOn, Sniffspot, PetMade, calculatorsfordogs.com, worldanimalfoundation, dogscalculators.com, vivaessencepet, petdrifts 등 8개 이상의 기존 사이트가 이미 장악 — 일부는 브랜드 인지도 높은 업체(SpotOn, Sniffspot). 레드오션.
- **Pet Boarding Cost Calculator**: CalcBee, AgentCalc, FurCalc, dogvetexpert, petcostestimator, Yelp, formts.com 등 다수 — 마찬가지로 레드오션.
- **Pet Food Toxicity Checker**: ToxiPets(앱), Safe Pet Treats(앱), dietpaw.com, dogscalculators.com의 "Dog Toxicity Calculator"(구체적 mg/kg 독성 임계값 제공) 등 이미 다수 존재. 게다가 이 유형(용량/독성 임계값 계산)은 **의료 안전 정보라 정확도·법적 리스크가 높아 이 사이트가 직접 만들 카테고리가 아니라고 판단** — 보류.
- **Cat Age(년→인간나이) 블로그 글**: Daily Paws, litter-robot, catcalculator.com, holistapet, miniwebtool, PetMorph 등 매우 포화된 데다, 이미 사이트에 `cat-age-calculator` 툴이 있어 블로그로 또 만들면 자기잠식 우려 — 기각.

**실제로 진행한 것 — GSC 쿼리가 아니라 "사이트 자체 dog/cat 페어링 빈 자리"를 다시 훑어서 발견한 진짜 기회**:
사이트의 기존 27개 포스트를 dog/cat 페어 단위로 재점검한 결과, dog 전용으로만 있고 cat 짝이 없는 포스트 2개를 발견 (세션 I가 Quality of Life에서 썼던 방법론을 blog 포스트에도 적용):
1. `what-to-feed-pregnant-dog`(101 노출, 사이트에서 두 번째로 노출 많은 페이지) — **cat 버전이 없었음**
2. `how-to-reduce-vet-costs-for-dogs` — **cat 버전이 없었음**

이 두 주제는 웹 검색으로 경쟁강도 확인한 결과 Hill's/VCA/Purina/Cats.com 같은 대형 사이트가 있긴 하지만, **dog 버전이 이미 같은 수준의 경쟁(Hill's/VCA/Purina 개 버전) 속에서도 101 노출을 기록하며 정상적으로 작동 중**이라 사이트의 콘텐츠 포맷(계산기 연계 + FAQ 스키마)이 이 정도 경쟁권에서는 통한다는 근거가 있음. "vet cost 절감" 주제는 오히려 개별 소규모 블로그(catsluvus.com 등) 위주라 경쟁이 상대적으로 낮음.

**신규 작성**:
- `_posts/2026-07-15-what-to-feed-pregnant-cat.md` — `what-to-feed-pregnant-dog` 구조를 그대로 따르되(주차별 급여표, FAQ 6개, 표 2개), 고양이 고유 사실을 웹 검색으로 확인 후 반영: **타우린**(개는 자체 합성 가능하지만 고양이는 불가 — 이게 "개밥을 고양이에게 주면 안 되는" 핵심 이유), **생선 날것 금지**(티아미나아제 효소가 비타민 B1 파괴), 이유기 급여 감량 프로토콜(VCA 기준 1일차 금식→2일차 25%→4~5일에 걸쳐 정상화, 고양이 특유의 유선염 방지 목적).
- `_posts/2026-07-15-how-to-reduce-vet-costs-for-cats.md` — `how-to-reduce-vet-costs-for-dogs` 구조를 따르되, 고양이 특유의 보험료(개 평균 $55~62/월 vs 고양이 $28~32/월, 나이 들수록 개보다 가파르게 오름 — 웹 검색으로 NerdWallet/Pawlicy/Cats.com 등에서 수치 확인), 고양이가 아픈 걸 잘 숨기는 습성 때문에 정기 혈액검사가 특히 중요하다는 점, 고비용 품종(Maine Coon/Ragdoll/Persian/Scottish Fold 등 유전 질환), TNR 프로그램 등 고양이 고유 내용으로 채움.
- 둘 다 세션 H/J 패턴 그대로 FAQ를 front matter(스키마용)와 본문(가시성용) 양쪽에 동일하게 작성, 1:1 매칭 코드로 검증 완료(6/6, 4/4 일치).

**역링크(고아 페이지 방지) 추가**:
- `what-to-feed-pregnant-cat` → `tools/cat-pregnancy-calculator.html`(신규 post-cta), `how-long-are-cats-pregnant.md`·`signs-of-cat-labor.md`(Related Articles), `what-to-feed-pregnant-dog.md`(Related Articles, 종간 교차링크)
- `how-to-reduce-vet-costs-for-cats` → `tools/cat-vet-visit-scheduler.html`(신규 post-cta), `how-much-does-a-cat-vet-visit-cost.md`·`how-often-vet-visits-cat.md`(Related Articles), `how-to-reduce-vet-costs-for-dogs.md`(Related Articles, 종간 교차링크)

**공통 파일 동기화**: `llms.txt`에 두 항목 추가(각각 관련 주제 근처에 배치). `index.html`/`tools/index.html`은 blog 포스트를 안 실으므로 수정 불필요(기존 패턴과 동일). `blog/index.html`은 Liquid 자동 순회라 손댈 필요 없음.

**QA**: 두 신규 파일 + 수정된 6개 파일 전체 대상으로 — div open/close 매칭(수정된 tool 2개), YAML front matter 파싱 검증(전체 28→30개 포스트 전수), slug 중복 검사(전수, 중복 없음), 전체 저장소 링크 재스캔(신규 포스트 포함, 깨진 링크 없음), FAQ front matter-본문 1:1 매칭(6/6, 4/4) 전부 통과.

**교훈**: "레드오션이라 신규 안 함"이라는 결론에 사용자가 동의하지 않을 수 있다는 걸 이번에 배움. 순수 계산기(calculator) 카테고리는 이 틈새 자체가 이미 많이 포화됐지만, **블로그 포스트(정보성 글)는 계산기보다 진입장벽이 낮고, 사이트 자체 구조의 dog/cat 페어링 빈 자리를 찾는 방법론(세션 I에서 시작)이 계산기뿐 아니라 블로그에도 그대로 적용 가능**하다는 게 이번 세션의 핵심 발견. 앞으로 "신규 콘텐츠 검토"를 할 때는 계산기 레드오션 여부만 보지 말고, **블로그 포스트 dog/cat 페어링 빈 자리도 항상 같이 훑을 것** (`grep "^slug:" _posts/*.md`로 전체 슬러그 뽑아서 dog/cat 대응 쌍이 있는지 눈으로 대조).

**다음 세션에서 확인할 것 추가**:
- 신규 작성한 `what-to-feed-pregnant-cat`, `how-to-reduce-vet-costs-for-cats`의 첫 GSC 노출 확인 (다음 zip에서 색인/노출 여부 체크)
- 블로그 dog/cat 페어링을 이번에 2건 더 채웠지만, 전수 재점검은 아직 안 함 — 다음 세션에서 `_posts/*.md` slug 전체를 다시 한 번 dog/cat 페어로 교차 대조해서 놓친 게 더 있는지 확인 권장

---

## 4. GSC 색인 현황 (7/15 기준)

- **심각한 문제**: "발견됨-미색인" 15개, "크롤링됨-미색인" 6개(합계 21개), "적절한 표준 태그가 포함된 대체 페이지" 1개(무해, 정상 canonical), "리디렉션 포함 페이지" 3개(→ **사용자 지시로 계속 무시**).
- **세션 F(7/12)·세션 H(7/14) 때 "발견됨-미색인 38개"로 2세션 연속 정체돼 있던 것이 이번엔 21개로 감소** — Coverage 리포트가 실제로 갱신되고 있고, 색인이 진행 중이라는 확실한 근거. "기다리면 된다"가 아니라 숫자로 확인됨(세션 J).
- **Coverage는 URL 목록을 안 주므로, 사이트 전체 URL(56개) vs Performance `페이지.csv`에 노출이 잡힌 URL(33개)을 diff해서 미색인 추정 23개 URL을 역산함** (tool 7개 + blog 16개). Coverage의 21개와 근접 — 방법은 세션 J 항목 참고, **주의: 포스트 URL은 파일명이 아니라 front matter `slug:`로 만들 것** (하나 불일치 사례 있었음, 세션 J에서 발견 후 수정).
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
2-1. **GSC 쿼리 매칭만으로 "신규 콘텐츠 없음"이라고 결론 내지 말 것 — 사이트 자체의 dog/cat 페어링 등 구조적 패턴에 빠진 게 없는지도 별도로 확인할 것** (세션 I에서 Quality of Life가 dog만 있고 cat이 없던 걸 뒤늦게 발견한 사례 참고). `ls tools/ | grep -i cat`, `ls tools/ | grep -i dog` 등으로 카테고리별 페어 여부를 주기적으로 점검.
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
5. **tools/ 페이지는 FAQ가 스키마에만 있고 본문에 안 보이는 경우가 많았음(세션 H에서 발견) — 세션 K에서 전체 21개 tool 완료.** 보강 작업 시에도 여전히 이 패턴(스키마 질문 그대로 `<h2>Frequently Asked Questions</h2>` + h3/p 페어로 본문 노출)을 신규 tool 제작 시 처음부터 적용할 것 — 신규 tool은 항상 이렇게 만들어야 함(체크리스트 4번 참고).
6. FAQ에 새 사실을 추가할 때는(예: "OO 계산기 있나요?" 류) **반드시 웹 검색으로 사실관계부터 확인** — 세션 H에서 "고양이는 BMI가 없다"고 쓸 뻔했다가 검색으로 FBMI 공식이 실제 존재함을 확인하고 정정한 사례 있음. 확신에 근거해 서술하지 말고 검색으로 검증할 것.

### 검증 습관
- 파일 수정 후 `<div>` 개수 짝 맞는지 python으로 체크 (`c.count('<div')` vs `c.count('</div>')`)
- YAML front matter는 `yaml.safe_load()`로 파싱 검증
- JSON-LD Schema는 `json.loads()`로 검증
- 전부 검증 통과 후에만 commit
- **아래 최종 QA는 매 세션 종료 전 기본으로 항상 수행할 것 — 사용자가 매번 요청 안 해도 알아서 할 것:**
  - 신규/수정된 모든 파일의 링크(`/tools/...`, `/blog/...`)를 실제 존재하는 파일·slug와 전수 대조 (python으로 tools/ 파일 목록, `_posts/*.md`의 slug 목록 뽑아서 매칭)
  - 신규 페이지가 있으면: `index.html`/`tools/index.html`의 tool-card 개수가 실제 `tools/*.html` 개수와 일치하는지, New 배지가 정확히 새 항목에만 있고 오래된 건 제거됐는지 확인
  - permalink(`tools/*.html`)와 slug(`_posts/*.md`) 전체 중복 검사 (`grep -h "^permalink:" tools/*.html | sort | uniq -c`, slug도 동일)
  - dog/cat 버전을 서로 복사해서 만든 경우, diff로 로직(JS)이 의도한 부분만 바뀌었는지, 복붙하다 남은 반대쪽 종(species) 단어가 실수로 남아있지 않은지 확인
  - FAQ를 스키마+본문 양쪽에 넣은 경우 스키마 질문 리스트와 본문 h3 질문 리스트가 실제로 1:1 일치하는지 코드로 비교
  - 이 QA를 하고 나서 결과를 대화에 요약해서 보여줄 것 — "다 했습니다"로 퉁치지 말고 뭘 어떻게 확인했는지 구체적으로 보고할 것

### 절대 하지 말 것
- `@page` CSS를 `@media print` 안에 중첩 (무시됨, 최상위에 둘 것)
- `position: absolute`/`fixed`를 print 영역에 사용 (빈 페이지/페이지 중복 유발 — 세션 A 참고)
- 안일하게 "기다리면 된다"고 결론 내고 데이터 안 파는 것 — 사용자가 이 부분에 대해 강하게 지적한 바 있음
- 신규 페이지 만들고 역링크 깜빡하는 것

---

## 6. 다음에 확인해야 할 것 (Open Items)

- **나머지 tool 7개 FAQ 가시화 마무리**: `cat-age`, `cat-heat-cycle`, `cat-vaccination-schedule`, `dental-cleaning-cost`, `dog-age`, `dog-vaccination-schedule`, `dog-vet-visit-scheduler`. 전부 이미 색인된 페이지라 우선순위는 낮음 — 패턴은 세션 H/J 커밋 참고, 스키마 질문 그대로 본문에 노출하면 됨(신규 리서치 불필요, 빠르게 끝남).
- **미색인 tool 7개(세션 J에서 FAQ 가시화 완료 — `annual-pet-cost-calculator`, `cat-pregnancy-calculator`, `cat-vet-visit-scheduler`, `dog-heat-cycle-calculator`, `dog-pregnancy-calculator`, `pet-grooming-cost-calculator`, `spay-neuter-cost-calculator`)의 다음 GSC 데이터에서 색인 여부 확인** — 특히 `dog-pregnancy-calculator`/`cat-pregnancy-calculator`는 수요가 이미 검증된 페이지라 색인만 되면 바로 노출 기대. FAQ 가시화가 실제로 색인에 영향 줬는지도 이걸로 검증 가능.
- **Coverage "발견됨/크롤링됨-미색인" 21개(38→21로 감소 확인됨, 세션 J) → 다음 데이터에서도 계속 줄어드는지 확인**. 계속 줄면 자연 회복 중인 것, 정체되면 개별 URL별로 GSC UI에서 "색인 생성 요청"을 사용자가 직접 눌러보는 걸 권유(에이전트는 GSC API 권한이 없어 직접 요청 불가).
- **미색인 blog 16개는 전부 세션 B 날짜조작 수정(7/4~7/10) 이전에 작성된 포스트(5/1~6/18)** — 6/22 이후 작성 포스트는 100% 색인됨. 온페이지 요인(FAQ, 역링크, 스키마)은 이미 정상이라 판단, 크롤 스케줄/신뢰도 누적 문제로 보고 이번엔 콘텐츠 수정 안 함. 다음 데이터에서도 그대로면(특히 5/1 작성 `dog-age-human-years`처럼 2.5개월 이상 정체된 케이스) 사용자가 GSC에서 직접 색인 요청 고려.
- **신규 제작한 `cat-quality-of-life-calculator`/`cat-quality-of-life-assessment`의 첫 GSC 노출 확인** — "cat quality of life calculator", "paw score cat" 등 관련 쿼리가 잡히기 시작하는지 다음 데이터에서 확인.
- **`what-to-feed-pregnant-dog`(101 노출) vs `how-to-tell-if-dog-is-pregnant`(54 노출) 자기잠식 의심 — GSC 웹 UI에서 두 URL 필터로 실제 쿼리 교차 확인 필요** (zip 내보내기는 페이지×쿼리 교차표가 없어 계속 미확정). 겹치는 게 확인되면 what-to-feed 포스트의 증상 관련 서술을 줄이고 how-to-tell-if 포스트로 명확히 유도.
- 세션 H에서 FAQ 가시화한 6개 tool(`pet-weight`, `cat-weight`, `pet-food-calorie`, `pet-insurance-cost-estimator`, `dog-weight`, `dog-quality-of-life`)의 다음 GSC 데이터에서 순위/노출 변화 확인.
- **다음에 신규 콘텐츠 여부를 판단할 때 사이트 자체의 dog/cat 페어링 등 구조적 패턴에 빠진 게 없는지도 항상 재확인할 것** (세션 I 교훈, 체크리스트 5번 참고). 세션 J에서는 191개 쿼리 전수 확인 결과 신규 클러스터 없음 재확인.
- `pet-euthanasia-cost-and-what-to-expect` 포스트는 영어 톤 검수를 사용자가 직접 하지 못한 상태("나 영어는 잘 몰라서 톤은 모르는데") — 필요시 재검토 여지 있음.
- **깨진 링크 전수 스캔은 매 세션 QA에 포함시킬 것** (세션 J에서 `how-much-does-a-cat-vet-visit-cost.md`의 `/blog/true-cost-cat-vs-dog/` 404 링크를 발견/수정함 — 슬러그가 파일명과 다른 포스트에서 발생한 실수였음). 방법: `_posts/*.md`의 실제 `slug:` 값과 `tools/*.html` 파일명을 모아서, 전체 파일에서 `/blog/xxx/`, `/tools/xxx.html` 패턴을 정규식으로 추출해 매칭 안 되는 것 찾기.

---

### 세션 L — "할 수 있는건 다하자": tool FAQ 가시화 전체 완료 + 블로그 페어링 3번째 빈 자리 발견/제작 (7/15, 세션 K 직후 연속)

세션 K 직후 사용자가 "할 수 있는건 다하자"고 요청 → 밀려있던 작업들을 전부 정리:

**1. tools/ FAQ 가시화 — 21개 전부 완료**
세션 H(6개) + 세션 I(신규 제작 시 처음부터 반영, 1개) + 세션 J(7개)에 이어 마지막 남은 7개(`cat-age`, `cat-heat-cycle`, `cat-vaccination-schedule`, `dental-cleaning-cost`, `dog-age`, `dog-vaccination-schedule`, `dog-vet-visit-scheduler`)에 동일 패턴 적용 완료. **이제 tools/ 21개 전부 스키마 FAQ가 본문에도 가시적으로 노출됨** — 세션 H에서 발견한 사각지대가 완전히 해소됨. 스키마 질문-본문 h3 1:1 매칭, div 개수 매칭 전부 코드로 검증 통과.
- 이 과정에서 `dog-age-calculator.html`의 blog 링크(`/blog/dog-age-human-years`)에 **trailing slash가 빠져있던 걸 발견해 수정**(`/blog/dog-age-human-years/`) — 이전 링크 스캔 스크립트가 trailing slash를 필수로 요구하는 정규식이라 못 잡아냈던 사각지대. 이후 스캔 스크립트를 trailing slash 선택적으로 고쳐서 재검증.

**2. 블로그 dog/cat 페어링 재점검 → 3번째 빈 자리 발견**
세션 K에서 이미 2개(`what-to-feed-pregnant-cat`, `how-to-reduce-vet-costs-for-cats`)를 채웠는데, 전체 슬러그를 다시 한 번 훑어본 결과 **`how-to-tell-if-dog-is-pregnant`(54 노출)의 cat 짝이 없었던 것도 발견**. `how-long-are-cats-pregnant`의 FAQ에 "첫 신호가 뭔가요" 정도만 부분적으로 있었을 뿐, dog 버전처럼 전용 페이지로 깊게 다룬 콘텐츠는 없었음.
- 웹 검색으로 경쟁강도 확인: PetMD, Hill's, Purina, Blue Cross, Whisker 등 동일 수준의 경쟁자 존재 — dog 버전이 이미 이 경쟁권에서 54노출을 내고 있다는 게 진행 근거.
- **신규 작성**: `_posts/2026-07-15-how-to-tell-if-cat-is-pregnant.md`. `how-to-tell-if-dog-is-pregnant.md` 구조를 그대로 따르되, 고양이 고유 사실을 웹 검색으로 검증 후 반영:
  - **"Pinking up"**(니플이 분홍색으로 변하는 것)이 dog의 "nipple darkening"보다 더 뚜렷하고 이른(day 16-20) 신호
  - **가성임신(pseudopregnancy)이 개보다 고양이에서 훨씬 드물고 증상도 약함** — Merck Veterinary Manual, PetMD, Vet Help Direct 등 다수 소스가 "uncommon/rare in cats" 명시(단, Vetster 1곳만 반대 의견을 냈으나 소수 의견으로 판단해 다수 컨센서스 채택). 원인 메커니즘도 다르게 서술(고양이는 유도배란 동물이라 비생식적 교미로 배란만 일어나도 가성임신 가능하다는 게 개와 다른 지점).
  - 확인 시기도 dog와 다르게(고양이는 day 17-25 촉진, day 21+ 초음파, day 42+ X-ray — 개의 주차 단위와 다른 일수 단위로 정확히 구분해서 서술)
- 역링크(고아 페이지 방지): `cat-pregnancy-calculator.html`(신규 post-cta), `how-long-are-cats-pregnant.md`·`signs-of-cat-labor.md`·`what-to-feed-pregnant-cat.md`(Related Articles), `how-to-tell-if-dog-is-pregnant.md`(Related Articles, 종간 교차링크).
- `llms.txt` 동기화.

**3. QA**: 신규 포스트 1개 + 수정 파일 전체 대상 — YAML 전수 검증(31개 포스트 전부 통과), slug 중복 없음, div 매칭, FAQ front matter-본문 1:1 매칭(6/6), **전체 저장소 링크 재스캔(trailing slash 유무 관계없이 매칭하도록 스크립트 개선 후 재실행, 깨진 링크 없음 확인)**.

**세션 K+L 종합**: 이번 두 세션에서 블로그 dog/cat 페어링 빈 자리 3개(`what-to-feed-pregnant-cat`, `how-to-reduce-vet-costs-for-cats`, `how-to-tell-if-cat-is-pregnant`)를 전부 채우고, tools/ FAQ 가시화도 21개 전부 완료. 사이트의 구조적 개선 작업(세션 H~L에 걸쳐 진행된 두 축: ①FAQ 가시성, ②dog/cat 페어링)이 이번 세션으로 사실상 마무리됨.

**다음 세션에서 확인할 것**:
- 이번 세션의 신규 3개 포스트(`what-to-feed-pregnant-cat`, `how-to-reduce-vet-costs-for-cats`, `how-to-tell-if-cat-is-pregnant`)와 tool FAQ 가시화 7개의 다음 GSC 데이터에서 노출/색인 변화 확인
- 블로그/tool의 dog/cat 페어링은 이제 거의 다 채워졌다고 판단됨 — 다음 신규 콘텐츠는 아마도 완전히 새로운 카테고리(현재 사이트에 없는 주제)를 찾아야 할 가능성이 높음. 다만 계산기(calculator) 카테고리는 세션 K에서 확인했듯 레드오션이 많으니, 신규 카테고리를 검토할 땐 웹 검색으로 경쟁강도부터 반드시 확인할 것.

### 세션 M — GSC 7/17 데이터 분석 + kitten weight chart 신규 + AI검색 대응 비교분석형 콘텐츠 보강 (7/17)

사용자 요청 핵심: (1) 신규 GSC 내보내기 확인 후 신규/보강 작업 진행, (2) 신규 콘텐츠는 기존 파일과 중복 체크 + 웹 검색으로 키워드 경쟁 확인, 롱테일 키워드 전략 활용, (3) **최근 AI 검색은 도메인 권위보다 콘텐츠 자체(문제해결·비교분석 위주)가 중요하다는 트렌드를 반영**, (4) AdSense 수익화 관점에서 우선순위 판단, (5) 대시보드/시각화 없이 텍스트로만 보고.

**1. GSC 데이터 분석 (5/13~7/15 누적, Coverage/Performance 둘 다 확인)**

- **Coverage 미색인 수치가 세션 L(7/15) 대비 완전히 동일함 — 발견됨-미색인 15개 + 크롤링됨-미색인 6개 = 21개, 변화 없음.** 세션 J에서 38→21로 줄어든 이후 이번엔 정체. 세션 F·H 때 2세션 연속 정체(38개)됐던 패턴과 유사 — Coverage 리포트 자체의 집계 지연 가능성(세션 F 가설)과 실제 정체 가능성 둘 다 열어두고 다음 데이터에서 계속 지켜볼 것. Coverage 차트(일별 데이터)는 7/10일자까지만 찍혀있어 실시간성이 없는 건 여전함(색인생성됨 32, 세션 J 시점과 동일 — 이 차트 자체가 며칠 지연되는 구조로 보임).
- **Performance 일별 노출 추이**: 7/11(80) → 7/12(58) → 7/13(103, 누적 최고치) → 7/14(53) → 7/15(69). 지난 세션까지의 뚜렷한 우상향(23→39→61→80)이 7/13 피크 이후 등락하는 패턴으로 바뀜 — 아직 우려할 수준은 아니지만(103 자체가 최고 기록), 계속 우상향이라고 단정하기보다 다음 데이터에서 추세 재확인 필요.
- **클릭은 여전히 극소수**: 세션 동안 누적 클릭 4건(7/12, 7/14 각 1건 — 인과 특정 불가한 개별 클릭). 전체 사이트 클릭수가 통계적으로 유의미해지려면 아직 시간이 더 필요한 단계.
- **`how-to-tell-if-dog-is-pregnant` 노출이 54 → 110으로 2배 이상 급증** (세션 L 이전 대비) — 세션 L에서 이 포스트로 역링크(`how-to-tell-if-cat-is-pregnant` 신규 제작 시 교차링크 추가)와 내부 연결이 강화된 시점과 일치. 다만 클릭은 여전히 0건, 평균 순위 75.57위로 아직 클릭 임계선까지는 거리가 있음.
- **미해결로 계속 열려있는 이슈**: `what-to-feed-pregnant-dog`(101노출, 27위, 클릭 0)의 자기잠식 의심(세션 H부터 3세션째 미확정). 이번 세션에도 GSC UI 교차확인 없이는 확정 불가 — 열린 항목으로 유지.

**2. 신규 콘텐츠 후보 탐색 — 사이트 구조 dog/cat 페어링 재점검**

세션 K/L의 방법론(`grep "^slug:" _posts/*.md`로 전체 슬러그를 뽑아 dog/cat 페어 대조)을 이번에도 반복 적용한 결과, **`puppy-weight-chart-by-breed-size`의 cat 짝이 없다는 걸 발견**. 이 포스트는 사이트 전체에서 **두 번째로 노출이 많고(29회), 평균 순위는 사이트 전체 1위(9.66위)** — 가장 검증된 성과 패턴인데 cat 버전이 없는 구조적 빈틈이었음.

- 웹 검색으로 "kitten weight chart" 경쟁강도 확인: Kinship, WALTHAM(수의사 검증 데이터, 권위 높음), Pawlicy, PupPilot, thepetcalculator.com(경쟁사 자체 cat weight 허브 보유), 그리고 AI 생성으로 보이는 저품질 사이트(siipet.com 2건, catacats.com) 다수 확인 — puppy 버전보다 확실히 포화된 니치. 다만 dog 버전이 같은 급의 경쟁(대형 브랜드 다수) 속에서도 사이트 최고 성과를 내고 있다는 근거가 있어, 포맷 자체(계산기 연계+FAQ+비교표)가 이 경쟁권에서 통한다고 판단해 진행.
- **차별화 포인트(AI검색 대응 겸용)**: 단순 나이별 체중표만 있는 경쟁사 다수와 달리, (1) "1파운드=1개월" 같은 빠른 어림규칙, (2) 대형묘종(메인쿤/랙돌/노르웨이숲) vs 일반 잡종묘 성장 타임라인 **비교표**, (3) "왜 우리 새끼고양이가 체중이 안 느나요" **문제해결형 트러블슈팅 섹션**(정상 범위 vs 수의사 상담 필요 범위 구분)을 넣어 단순 정보 나열이 아닌 문제해결/비교분석 콘텐츠로 구성 — 이번 세션 사용자 지시(AI검색은 도메인 권위보다 콘텐츠 품질/실질 가치가 중요)를 신규 제작 시점부터 반영.
- **신규 작성**: `_posts/2026-07-17-kitten-weight-chart-by-breed-size.md`. Birth~12개월 체중표, "1파운드=1개월" 규칙, 대형묘종 비교표, 트러블슈팅 섹션, FAQ 6개(front matter + 본문 1:1 매칭 검증 완료). 기존 `how-much-should-a-cat-weigh`(성묘 체중 가이드, BCS 중심)와 내용이 겹치지 않도록 확인 — 이쪽은 생후~12개월 성장 곡선이 주제라 별도 앵글로 확인됨.
- **역링크(고아 페이지 방지)**: `puppy-weight-chart-by-breed-size.md`(Related Articles, 종간 교차링크), `how-much-should-a-cat-weigh.md`·`why-is-my-cat-always-hungry.md`(Related Articles), `cat-weight-calculator.html`·`cat-age-calculator.html`(신규 post-cta).
- `llms.txt` 동기화 완료. `index.html`/`tools/index.html`은 blog 포스트를 안 실으므로 수정 불필요(기존 패턴과 동일).

**3. AI검색 대응 — 기존 고노출 페이지에 비교분석형 콘텐츠 보강**

사용자가 이번 세션에 명시한 "AI검색은 도메인 권위보다 콘텐츠 자체(문제해결·비교분석)가 중요하다"는 방향을 신규 제작뿐 아니라 **기존 페이지 보강에도 적용**. GSC 쿼리 중 `dog pregnancy diagnosis`(8노출)·`dog pregnancy confirmation`(7노출)·`dog pregnancy check`(7노출) 등 "확인/진단" 계열 쿼리가 상당한 볼륨으로 존재하는데, `dog-pregnancy-calculator`/`cat-pregnancy-calculator` 두 툴 모두 이 정확한 앵글(진단 방법 비교)을 다루는 섹션이 없었음(이번 세션 시작 시점 두 툴 다 여전히 GSC Performance 페이지 목록에 노출 자체가 안 잡히는 상태 — 세션 J에서 발견한 미색인 7개 tool에 포함됐던 페이지들).

- **`dog-pregnancy-calculator.html`, `cat-pregnancy-calculator.html`에 "Pregnancy Confirmation and Diagnosis: Methods Compared" 비교표 섹션 신규 추가**: 촉진(palpation)/혈액검사(relaxin, dog만 해당)/초음파/X-ray 4가지(cat은 3가지, 고양이는 relaxin 혈액검사가 실무에서 잘 안 쓰임) 방법을 "가장 이른 신뢰 가능 시기 / 정확도 / 알 수 있는 정보" 축으로 비교. 신규 사실 주장이 아니라 두 페이지에 이미 흩어져 있던 정보(도입부의 "week 4 ultrasound", "week 7-8 X-ray" 등)를 명시적인 비교표로 재구성한 것이라 콘텐츠 리스크는 낮음.
- 스키마 FAQ + 본문 가시적 FAQ 양쪽에 "How can I confirm or diagnose my dog's/cat's pregnancy?" 신규 질문 추가 — `diagnosis`/`confirm` 정확 문구가 페이지 텍스트에 없었던 걸 세션 C의 핵심 교훈(정확 문구 매칭)에 따라 채움. 스키마-본문 1:1 매칭 코드로 검증 완료(dog 4/4, cat 4/4).
- **`what-to-feed-pregnant-dog`(101노출, 0클릭 이상신호)는 이번 세션엔 손대지 않기로 결정**: 313줄 분량으로 이미 트라이메스터별 상세 가이드, 주차별 급여표, 금지 음식표, 산후 급여 변화까지 매우 깊은 콘텐츠가 있어 추가 비교/문제해결 섹션을 얹어도 한계효용이 낮다고 판단. 0클릭의 원인이 콘텐츠 깊이 부족이 아니라 순위(27위, 아직 1페이지 밖) 자체 또는 자기잠식 의심(미확정, 세션 H부터 열린 이슈) 쪽에 더 가깝다고 보고, 콘텐츠 재작업보다 다음 세션에서 GSC UI 교차확인을 사용자에게 요청하는 쪽이 더 정확한 다음 스텝이라고 판단.

**4. AdSense 수익화 관점 우선순위 판단 (사용자 요청)**

- 사이트가 여전히 클릭 자체가 거의 없는 초기 단계(누적 클릭 한 자릿수)라, **신규 페이지 1개보다 이미 노출이 잡히는 페이지의 순위/클릭률 개선이 여전히 ROI가 높다**는 세션 H 이후의 판단을 유지. 이번 세션에 신규 콘텐츠(kitten weight chart)를 하나만 추가하고, 나머지 리소스는 이미 검증된 수요가 있는 두 페이지(dog/cat pregnancy calculator — 쿼리 노출 20회 이상, 색인만 되면 바로 트래픽 기대)의 콘텐츠 깊이를 높이는 데 집중한 것도 이 판단에 따른 것.
- kitten weight chart는 "완전 신규 니치 개척"이 아니라 "이미 검증된 사이트 최고 성과 포맷(puppy 버전)의 반쪽을 채우는" 저위험 확장이라 우선순위를 높게 잡음 — 세션 K/L에서 확립된 "구조적 페어링 빈자리 = 저위험 신규 콘텐츠" 원칙을 계속 적용.
- 비교/문제해결형 콘텐츠 보강은 AI 검색(예: ChatGPT/Perplexity류 답변엔진) 노출 가능성까지 고려한 선제 투자 성격 — 전통 SEO 순위 데이터로는 아직 효과 측정이 어려우므로(AI 검색 유입은 GSC에 잡히지 않음) 다음 세션에서도 GA 데이터의 referrer 쪽을 함께 볼 필요가 있음(현재 GA 데이터는 이번 세션에 별도로 받지 않아 미확인).

**5. QA**: 신규 포스트 1개 + 수정 파일 6개(dog/cat-pregnancy-calculator, cat-weight-calculator, cat-age-calculator, puppy-weight-chart-by-breed-size, how-much-should-a-cat-weigh, why-is-my-cat-always-hungry, llms.txt) 전체 대상 — YAML 전수 검증(32개 포스트 전부 통과), slug/permalink 중복 없음, div 개수 매칭(4개 tool 파일 전부 open=close), table/tr 태그 매칭, JSON-LD 스키마 유효성(전체 tools 21개 재검증, 에러 없음), FAQ front matter-본문 1:1 매칭(신규 포스트 6/6, dog-pregnancy 4/4, cat-pregnancy 4/4), 전체 저장소 링크 재스캔(브로큰 링크 0건).

**6. 사용자 추가 요청 — "GSC 데이터만 보면 기존 레퍼토리 안에서만 신규가 나온다, 카테고리 확장을 어서 해야 한다" 피드백에 따른 완전 신규 카테고리 추가**

세션 M 1차 작업(위 1~5번)까지는 GSC 쿼리 보강 + 사이트 구조 dog/cat 페어링 빈자리 채우기 위주였음. 사용자가 이 방식 자체의 한계를 지적함 — GSC 데이터는 "우리가 이미 만든 콘텐츠 근처의 검색"만 보여주므로, 이 방식만 반복하면 사이트가 다루는 주제 범위 자체는 넓어지지 않고 계속 같은 카테고리 안에서만 맴돈다는 지적. 이에 따라 **사이트에 아예 없는 새 카테고리**를 웹 검색으로 발굴해 경쟁강도를 확인하는 작업을 추가로 진행.

- **탈락시킨 후보들** (전부 웹 검색으로 경쟁강도 확인 후 기각):
  - **강아지 성견 체중/사이즈 예측 계산기(Dog Size Predictor)**: Newtum, Pearson, Pawlicy, spiritdogtraining, calcviva, fourdogpaws, omnicalculator, puppygrowthcalculator.com(전용 사이트), yourpaws 등 매우 많은 기존 계산기 확인 — 이미 사이트의 `dog-weight-calculator`가 유사 기능(현재 나이/체중으로 성견 체중 추정)을 커버하고 있기도 해서 자기잠식 우려까지 겹쳐 기각.
  - **반려동물 이름 생성기(Pet Name Generator)**: commentpicker, 4menearme, randomlists, namegeneratorfun, petdecorart, digitalkw, iluvtool, petnicki, 그리고 **직접 경쟁사인 pawcalculator.com**까지 이름 생성기를 운영 중 — 트래픽은 클 수 있으나 극도로 포화됐고, 사이트의 "수의학 기반 계산기" 포지셔닝과도 결이 달라(재미/네이밍 콘텐츠) 기각.
  - **반려동물 기대수명 계산기(Life Expectancy Calculator)**: Newtum, worldanimalfoundation, omnicalculator, pawcalculator, thepetcalculator.com, dogscalculators.com, furcalc(NIH Dog Aging Project·VetCompass·AKC 데이터 인용, DVM 감수까지 명시)까지 — 데이터 권위 경쟁이 매우 치열한 레드오션이라 기각.
  - **체중 감량/칼로리 결핍 계산기(Weight Loss Calculator)**: Association for Pet Obesity Prevention·World Pet Obesity Association(실제 수의사 단체) 및 thepetcalculator.com이 이미 深이 있는 전용 계산기 보유 — 권위 있는 경쟁자와 직접 부딪히는 영역이라 이번엔 보류(다음 후보군에 남겨둠, 아래 참고).
- **선정: 벼룩·진드기 예방 비용 계산기(Flea & Tick Prevention Cost Calculator)** — 웹 검색 결과 이 주제는 **"계산기" 형태의 경쟁자가 거의 없고 대부분 정적 비용표/블로그 글(vetreceipt.com, spectrumcare.pet, 동물병원 블로그 등)뿐**이라는 걸 확인 — 인터랙티브 계산기 포맷 자체가 비어있는 진짜 저경쟁 틈새. 동시에 반려동물 예방접종/구충 비용이라는 실질적·반복적 지출(연 1회성 아닌 매달 발생)이라 검색 의도가 뚜렷하고, 사이트가 이미 검증한 "비용 계산기" 포맷(spay-neuter, dental, grooming과 동일 패턴)과 정확히 맞아떨어져 우선 선정.
- **신규 제작**:
  - `tools/flea-tick-prevention-cost-calculator.html` — dog/cat 통합, dog는 체중 구간별 배율(0.85~1.5x) 적용, 제품 유형 4종(basic topical / oral chewable / combo+heartworm / 8개월 collar) 선택 → 연간+월평균 비용 추정. 본문에 제품 유형 비교표, **"예방 비용 vs 방치했을 때 치료 비용" 비교 섹션**(벼룩 감염 가정치료 $50-200+, 개 심장사상충 치료 $500-1,000+ 및 고양이는 승인된 치료제 자체가 없음, 진드기매개질환 검사·치료 $250-525 — 전부 웹 검색으로 확인한 수치)을 넣어 이번 세션 AI검색 방향(비교분석·문제해결)을 처음부터 반영. FAQ 3개(스키마+본문 1:1 매칭 검증).
  - `_posts/2026-07-17-flea-tick-prevention-cost.md` — 계산기 짝 콘텐츠. 제품유형별 비용표, 가격 편차 원인 분석(체중/묶음구매/브랜드vs제네릭/콤보vs단일), 예방 vs 치료 비용 비교, **"이미 감염됐다면?" 문제해결형 체크리스트**(동거 반려동물 동시치료·침구 세탁·진공청소·최소 3개월 지속 등), FAQ 6개(제네릭 안전성, 개 구충제를 고양이에 쓰면 안 되는 이유=퍼메트린 독성, 실내묘도 필요한 이유 등 롱테일 키워드 다수 포함).
  - **롱테일 키워드 전략 반영**: 본문·FAQ에 "flea and tick prevention cost per month", "Frontline/Nexgard/Seresto/Revolution Plus" 등 구체 제품명, "generic flea medication", "indoor cat flea prevention", "dog flea medication on cat"(안전 경고 겸 검색 의도 대응) 등 세부 롱테일을 의도적으로 다수 배치 — 메인 키워드("flea tick calculator") 하나가 아니라 주변 롱테일 클러스터를 넓게 점거하는 전략.
- **역링크(고아 페이지 방지) 6곳**: `annual-pet-cost-calculator.html`(신규 post-cta), `dog-cat-dental-cleaning-cost.md`·`spay-neuter-cost-and-timing.md`·`annual-cost-of-owning-a-dog.md`(Related Articles).
- **공통 파일 4종 전부 동기화**: `index.html`·`tools/index.html`에 신규 tool-card 추가(New 배지를 `cat-quality-of-life-calculator`에서 이번 신규로 이동 — 세션 L 이후 배지가 오래 남아있던 걸 정리), `_includes/footer.html`의 Tools 목록에 추가(footer는 큐레이션 목록이지만 비용 계산기 계열은 이미 다수 포함돼 있어 동일 계열로 추가), `llms.txt`에 tool+blog 항목 각 1개씩 추가.
- **QA 재실행**: 전체 포스트 33개(신규 포함) YAML 전수 통과, slug/permalink 중복 없음(tool 22개), 신규/수정 파일 div 매칭, JSON-LD 스키마 22개 tool 전수 재검증 에러 없음, flea-tick 스키마-본문 FAQ 1:1 매칭(3/3), 신규 포스트 FAQ 매칭(6/6), index.html/tools/index.html 카드 개수(22) = 실제 tool 파일 개수(22) 일치 확인, 전체 링크 재스캔 브로큰 0건.

**다음 세션 신규 카테고리 후보 파이프라인** (경쟁강도 조사는 이번 세션에 완료, 진행은 보류):
- **체중 감량/칼로리 결핍 계산기**: 권위 있는 수의사 단체(APOP, WPOA) 경쟁자가 있지만, 우리 사이트의 기존 `pet-food-calorie-calculator`(이미 색인·노출 있음)에 "감량 모드" 토글을 추가하는 확장형으로 접근하면 신규 페이지 리스크 없이 시도 가능 — 완전 신규 페이지보다 기존 계산기 확장을 권장.
- **첫해 강아지/고양이 입양 비용 계산기(초기 셋업 비용, annual-pet-cost와 다른 앵글)**: 이번 세션엔 경쟁강도 조사를 하지 못함 — 다음 세션 후보.
- 계속 레드오션인 카테고리(사이즈 예측/이름생성기/기대수명): 재검토 불필요, 계속 배제.

**다음 세션에서 확인할 것**:
- Coverage 미색인 21개가 다음 데이터에서도 정체면(2세션 연속), 개별 URL 재크롤 요청을 사용자에게 권유할 시점 — 계속 "며칠 더 보자"고 미루지 말 것.
- `dog-pregnancy-calculator`/`cat-pregnancy-calculator`가 이번 콘텐츠 보강(비교표+FAQ) 이후 색인/노출되는지 최우선 확인 — 색인만 되면 이미 검증된 수요(20회 이상 노출 쿼리 클러스터)라 바로 트래픽 전환 기대.
- 신규 `kitten-weight-chart-by-breed-size`의 첫 노출/색인 확인.
- **신규 카테고리 `flea-tick-prevention-cost-calculator`/`flea-tick-prevention-cost`(포스트)의 첫 노출/색인 확인 — 사이트 최초의 완전 신규 카테고리라 GSC에 관련 쿼리("flea tick cost", "flea prevention calculator" 등)가 새로 잡히기 시작하는지가 카테고리 확장 전략이 통하는지 확인하는 첫 신호가 될 것.**
- `what-to-feed-pregnant-dog` vs `how-to-tell-if-dog-is-pregnant` 자기잠식 의심은 4세션째 미확정 — 사용자에게 GSC UI 교차확인을 다시 한번 요청하거나, 계속 미확인이면 "확정 불가로 보류"로 공식 종결하는 것도 고려.
- GA 데이터(referrer, AI 검색엔진발 유입 여부)를 다음 세션에 받아서 organic 검색 외 유입 채널 변화도 함께 볼 것 — 이번 세션엔 GSC만 받아 GA 쪽은 미확인 상태.
- **다음 세션 신규 카테고리 후보**: pet-food-calorie-calculator에 "체중 감량 모드" 확장(APOP/WPOA 등 권위 있는 경쟁자 있지만 기존 계산기 확장이라 리스크 낮음), 첫해 입양 비용 계산기(경쟁강도 미조사, 다음 세션 후보). 사용자가 "GSC 데이터만으로는 레퍼토리 확장이 안 된다"고 명확히 피드백했으므로, **매 세션 GSC 보강과 별개로 최소 1개는 완전 신규 카테고리 후보를 웹 검색으로 발굴하는 걸 정례화할 것.**

### 세션 M (계속) — 버그 수정: tool 페이지 표 반응형 깨짐 (7/17)

사용자가 `flea-tick-prevention-cost-calculator` 페이지 모바일 스크린샷을 보내며 표가 반응형으로 안 잘리고 깨진다고 리포트.

**원인**: `.table-wrapper` 스타일(`overflow-x:auto` + `table min-width:480px` 등)이 `_layouts/post.html` 안에 `.post-body .table-wrapper`로 **블로그 포스트 레이아웃에만 스코프**돼 있었음. `tools/*.html`은 `_layouts/tool.html`(별도 레이아웃)을 쓰는데, 여기엔 이 스타일 자체가 아예 없어서 `class="table-wrapper"`를 붙여도 무용지물이었음. 세션 M 앞부분에서 `dog/cat-pregnancy-calculator`, `flea-tick-prevention-cost-calculator`에 비교표를 추가하면서 이 문제가 새로 생김(이전엔 tool 페이지에 표가 있는 파일 자체가 없어서 잠재해있던 버그가 이번에 처음 표면화됨).

**수정**: `css/style.css`(전역 스타일시트)에 스코프 없는 `.table-wrapper` 규칙을 새로 추가. 블로그 포스트는 기존 `.post-body .table-wrapper`가 더 구체적이라 그대로 우선 적용(충돌 없음), tool 페이지는 이제 전역 규칙이 적용됨.

**교훈(중요, 체크리스트 항목에도 반영)**: 여러 레이아웃(post/tool/checklist)이 공유해야 하는 CSS는 특정 레이아웃 파일 안에 스코프해서 넣지 말고 **반드시 `css/style.css`에 스코프 없이 넣을 것**. 이번 체크리스트 섹션 신규 제작 시에도 이 교훈을 바로 적용해서 `checklist-*` 관련 CSS를 전부 처음부터 `css/style.css`에 넣었음(아래 참고).

### 세션 M (계속) — "카테고리 확장" 논의 및 실행: Checklists 신규 섹션 + 반려동물 종 확장 (7/17)

**배경**: 세션 M 앞부분에서 신규 콘텐츠 후보를 웹 검색으로 탐색했으나(체중감량 계산기 등) 전부 GSC 쿼리 보강이나 기존 계산기 카테고리 안에서의 확장이었음. 사용자가 "GSC 데이터만 보면 기존 레퍼토리 안에서만 신규가 나온다", "카테고리 확장도 이제는 어서 해야 한다"고 명확히 피드백 — nav바(Tools/Blog/About/Contact) 스크린샷을 보여주며 **완전히 새로운 최상위 섹션**을 요청.

**후보 조사 (웹 검색)**:
- **품종(breed) 디렉토리/비교/선택 퀴즈 — 전부 기각**: 직접 경쟁사(calculatorsfordogs.com, thepetcalculator.com, dogscalculators.com)가 이미 품종별 200개+ 페이지와 품종 전용 계산기까지 만들어놨고, 품종 비교 도구도 breedfinder.org·dogell.com·breedlookup.com·omnipawhub.com·petzdaddy.com·mybreedmatch.com·breedtools.com에 **AKC 본사**까지 이미 다수 존재 — 이 시점에 진입하면 승산 없음. 이 조사 결과를 사용자에게 투명하게 공유하고 다른 방향 제안.
- **체크리스트 — 선정**: "새 강아지/고양이 체크리스트" 자체는 검색량이 있지만 경쟁자 거의 전부가 AAHA·Banfield·Chewy·Kinship 같은 정적 블로그 글이거나 유료 다운로드(gumroad, littlebeasttreats)이고, **"체크박스 누르고 저장/출력하는 인터랙티브 웹 도구" 자체를 만든 곳은 거의 없음**(puppygrowthcalculator.com이 거의 유일한 예). 사이트가 이미 가진 PDF 저장(print) 패턴을 그대로 재사용할 수 있고, 기존 계산기 22개와 자연스럽게 상호링크되는 구조라 선정.
- **Compare(비교 허브) — 조건부 보류**: 사용자가 "그 분야에 꼭 있어야 될 것" 관점에서 재고 요청 → 품종 성향(성격/미용/운동량) 비교는 여전히 레드오션이라 배제하되, **우리가 이미 데이터를 가진 "비용/실용" 축 비교**(품종별 연간비용, 보험 플랜, 사료 급여방식 비교 등 기존 계산기 데이터 재활용)로 스코프를 좁히면 승산 있다고 판단 — **이번 세션엔 시간 관계상 미착수, 다음 세션 우선순위로 넘김** (Checklists 하나를 제대로 만드는 데 집중, 두 개를 동시에 어설프게 만들지 않기 위한 판단 — 사용자가 "둘 다 퀄리티 떨어지면 안 된다"고 명시).
- **종 확장(사용자 요청 "폭넓게 생각")**: 개·고양이 외 반려동물(토끼 등)도 고려해보라는 요청에 따라 웹 검색으로 "new rabbit checklist" 경쟁강도 확인 — 역시 정적 블로그/유료 다운로드뿐이고 인터랙티브 도구는 없음. 우리 직접 경쟁사(calculatorsfordogs 등)는 전부 개·고양이 전용이라 토끼는 진짜 블루오션. 계산기는 종별로 새로 만들려면 검증된 수치 데이터가 많이 필요해 리스크가 크지만, **체크리스트는 상대적으로 적은 리서치로 새 종을 다룰 수 있어 "종 확장의 첫 시도"로 적합한 포맷**이라고 판단.

**인프라 구축 (신규)**:
- `_layouts/checklist.html` — tool.html과 동일한 head/meta/analytics 구조 유지, 본문이 삽입되는 지점(content 변수 출력) 뒤에 **공용 JS**(체크박스 상태를 `localStorage`에 저장/복원, 진행률바 업데이트, reset, print) 추가. 이 JS는 `.checklist-page[data-checklist-id]`와 `.checklist-check[data-check-id]`만 있으면 어떤 체크리스트 페이지에서도 동일하게 작동 — **개별 체크리스트 파일엔 JS를 전혀 안 넣어도 됨**(재사용성을 위해 의도적으로 레이아웃에 공용 로직을 둠, tool 파일들이 매번 JS를 반복 작성하던 것과 다른 패턴).
- `_config.yml`에 `path: "checklists"` → `layout: "checklist"` 기본값 scope 추가(tools와 동일 패턴).
- `css/style.css`에 `.checklist-*` 전용 CSS 블록 신규 추가(진행률바, 커스텀 체크박스 — `appearance:none` + `::after` 체크마크로 직접 그려서 프린트 시에도 정상 렌더링되게 함, 프린트 미디어쿼리에서는 진행상태와 무관하게 항상 빈 체크박스로 인쇄되도록 처리 — "출력해서 직접 손으로 체크하는" 용도에 맞춤).
- `_includes/header.html` nav에 "Checklists" 탭 추가 (Tools와 Blog 사이, 데스크톱+모바일 양쪽).
- `_includes/footer.html`에 Checklists 컬럼 추가(4컬럼 그리드로 변경, `css/style.css`의 `.footer-inner` grid-template-columns도 `2fr 1fr 1fr` → `2fr 1fr 1fr 1fr`로 수정).

**신규 콘텐츠 3개** (전부 `ItemList` + `FAQPage` 스키마, 진행률바, 프린트 버튼, 관련 tool 링크, 면책 문구 포함):
1. `checklists/new-puppy-checklist.html` — 24개 항목(공급품 9 / 첫 동물병원 방문·건강 8 / 홈 준비·첫 달 루틴 5 / 예산 2), dog-vaccination-schedule-calculator·annual-pet-cost-calculator·spay-neuter-cost-calculator·puppy-weight-chart-by-breed-size로 상호링크.
2. `checklists/new-kitten-checklist.html` — 23개 항목(공급품 9 / 첫 동물병원 방문·건강 7 / 홈 준비·첫 달 루틴 5 / 예산 2), cat-vaccination-schedule-calculator·annual-pet-cost-calculator·spay-neuter-cost-calculator·kitten-weight-chart-by-breed-size로 상호링크. 백신 스케줄(FVRCP)·FeLV/FIV 검사·백합 등 고양이 독성 식물 경고 등 고양이 고유 내용 반영.
3. `checklists/new-rabbit-checklist.html` — **사이트 최초의 개·고양이 외 콘텐츠**, 21개 항목(주거/용품 9 / 동물병원 4 / 홈 준비·안전 4 / 핸들링·루틴 3 / 예산 1). 웹 검색으로 검증한 토끼 고유 사실 반영: GI stasis(장운동 정지, 12-24시간 무배변/무식욕이면 응급), 고양이용 응고형 리터 사용 금지(섭취 시 장폐색 위험), 최소 6x10ft 운동 공간, 80°F(27°C) 이하 온도 유지 필요(더위에 매우 취약), exotic/rabbit-savvy 수의사를 미리 찾아둬야 하는 이유(일반 동물병원 다수가 토끼 진료 안 함), 8-12년 수명(예상보다 긴 장기 커밋). 이 페이지는 사이트에 토끼 전용 계산기가 없어서 tool 링크는 넣지 않고 체크리스트 허브(`/checklists/`)로만 연결.
4. `checklists/index.html` — 체크리스트 허브 페이지, `tools/index.html`과 동일한 `.tool-card` 스타일 재사용(신규 클래스 안 만들고 기존 패턴 재활용).

**역링크(고아 페이지 방지) 5곳**: `dog-vaccination-schedule-calculator.html`(신규 post-cta → new-puppy-checklist), `cat-vaccination-schedule-calculator.html`(→ new-kitten-checklist), `annual-pet-cost-calculator.html`(→ 둘 다), `spay-neuter-cost-calculator.html`(→ 체크리스트 허브). `llms.txt`에 "## Checklists" 섹션 신규 추가(Tools와 Blog 사이, "Checklists는 Tools와 달리 개·고양이 외 종도 다룬다"는 설명 포함 — LLM이 이 구조적 차이를 인지하도록).

**면책 사항**: 사용자가 "면책사항은 잘해놔야겠지, 알아서 잘하겠지 생각하고 있다"고 명시적으로 신뢰 표현 → 기존 tool 페이지와 동일한 `.disclaimer-box` 패턴을 3개 체크리스트 전부에 적용, 특히 토끼 체크리스트는 "일반 수의사가 아니라 rabbit-savvy 수의사의 안내를 대체하지 않는다"는 문구로 종 특이성까지 반영.

**QA**: YAML 전수 검증(체크리스트 4개 파일 전부 통과), `_config.yml` YAML 유효성, JSON-LD(ItemList+FAQPage) 3개 파일 전부 유효성 검증 통과, div/label/span 태그 개수 매칭(3개 체크리스트 전부 일치), Liquid 태그 균형 확인(header.html, checklist.html — 여는 태그와 닫는 태그 개수 매칭), **FAQ 스키마-본문 1:1 매칭(3/3, 3/3, 3/3 전부 일치)**, **ItemList 스키마 항목수 vs 실제 체크박스 개수 매칭(24/24, 23/23, 21/21)**, 화면에 표시되는 "0 of N done" 초기 텍스트가 실제 체크박스 개수와 일치하는지 확인, 전체 저장소 링크 재스캔(체크리스트 포함, 브로큰 링크 0건).

**다음 세션에서 확인할 것**:
- Checklists 섹션의 첫 GSC 노출/색인 여부 — 완전히 새로운 URL 네임스페이스(`/checklists/`)라 색인 속도 자체가 관찰 포인트.
- **Compare(비교) 허브를 다음 세션 우선순위로 진행** — 품종 성향 비교 아니라 비용/실용 축으로 스코프 좁혀서(품종별 연간비용, 보험 비교, 사료 급여방식 비교) 착수. 기존 계산기 데이터 재활용 가능한 것부터.
- 체크리스트 3개 다음으로 후보군: 이사(반려동물과 이사), 여행, 시니어 반려동물, 응급상자 준비 체크리스트 등 — 사용자가 "폭넓게 생각해도 된다"고 했으니 종 확장(기니피그·잉꼬 등)도 계속 후보로 열어둘 것, 다만 매번 웹 검색으로 경쟁강도 확인 먼저.
- localStorage 기반 진행률 저장은 브라우저/기기별로 분리 저장됨(동기화 안 됨) — 사용자가 여러 기기에서 확인하고 싶어할 경우 계정 시스템 없이는 한계가 있음을 인지해둘 것(별도 요청 없으면 현재 방식 유지).
- **CSS 스코프 교훈(위 버그 수정 항목 참고)을 앞으로도 계속 지킬 것** — 새 레이아웃이나 새 컴포넌트를 만들 때 여러 페이지 타입에서 재사용될 가능성이 있다면 처음부터 `css/style.css`에 스코프 없이 넣을 것, 특정 레이아웃 파일 안에 스코프해서 나중에 재사용성 문제가 반복되지 않도록.

### 세션 M (계속) — 🚨 실제 배포 장애: GitHub Pages 빌드 실패 + 원인 규명 (7/17)

**사고 개요**: Checklists 신규 섹션 커밋(80fa9e1)을 push한 직후 GitHub Pages 빌드가 **실패**하기 시작했고, 몇 시간 동안(사용자가 "push에서 뭐가 문제가 생긴거 같은데"라고 알려줄 때까지) **petpawcalc.com이 이전 버전(구버전)으로 멈춰있는 상태**였음. `git push` 자체는 매번 성공했기 때문에(로컬 git 관점에서는 아무 에러 없음) 이전까지는 이 문제를 전혀 인지하지 못하고 있었음 — **매우 중요한 사각지대**.

**원인**: `handover.md`가 **YAML front matter가 없는 순수 마크다운 파일**인데, GitHub Pages가 쓰는 Jekyll 환경에는 `jekyll-optional-front-matter` 플러그인이 항상 로드되어 있어서, front matter 없는 `.md` 파일도 자동으로 렌더링 가능한 "페이지"로 취급하고 **Liquid 템플릿 엔진으로 처리**해버림. 이번 세션에 handover.md의 QA 기록 부분에 문서화 목적으로 리터럴하게 적어둔 `{{ content }}`, `` `{% %}` ``(Liquid 태그 예시를 텍스트로 설명한 것)가 진짜 Liquid 문법으로 파싱 시도되면서, 특히 내용 없는 `{% %}`가 **Liquid 문법 오류**를 일으켜 전체 사이트 빌드가 크래시남. `README.md`/`Gemfile`/`Gemfile.lock`은 원래부터 `_config.yml`의 `exclude:` 목록에 있어서 안전했지만, **`handover.md`는 처음부터 이 목록에 빠져 있었던 게 근본 원인** — 지금까지는 단순히 handover.md 안에 우연히 `{{`나 `{%` 같은 문자열이 들어간 적이 없어서 문제가 드러나지 않았을 뿐, 잠재된 위험이었음.

**진단 과정**: `git push`가 성공해도 실제 배포(GitHub Pages 빌드)가 실패할 수 있다는 걸 이번에 처음 확인 — **앞으로는 push 후 반드시 GitHub Pages 빌드 상태까지 확인할 것** (아래 "작업 방식" 섹션에 체크리스트로 추가함). 진단은 GitHub API(`/repos/{repo}/pages/builds/latest`, `/repos/{repo}/actions/runs`)로 최근 빌드의 `conclusion`이 `failure`인지 먼저 확인 → 실패한 job의 check-run annotation에서 에러 로그 일부 확인(단, annotation 메시지는 앞부분에서 잘려서 실제 에러 지점이 안 보이는 경우가 많음, 이번에도 그랬음) → 로그 전문은 Azure Blob Storage로 리다이렉트되는데 이 도메인은 에이전트의 네트워크 화이트리스트에 없어 접근 불가 → **결국 실제 push를 통한 이진 탐색(bisection)으로 원인을 좁힘**: 의심되는 변경사항을 하나씩 되돌리며 재푸시 → GitHub Pages 빌드 결과 확인을 반복(총 3라운드: `_config.yml` scope 되돌리기 → 여전히 실패 → 체크리스트 인프라 전체 제거 → 여전히 실패 → `handover.md`를 `exclude:`에 추가 → **성공**, 이걸로 확정).

**부수적으로 확인된 사실**: 로컬 샌드박스에 `apt-get install jekyll` 등으로 **Jekyll 4.3.2를 설치해 로컬 빌드는 시도해봤지만 에러 없이 성공**해버림 — GitHub Pages는 `jekyll v3.10.0`을 정확히 고정해서 쓰는데(`github-pages` gem이 버전을 강제 고정), 로컬에는 rubygems.org 접근이 막혀 있어 동일 버전 설치가 불가능해 로컬 재현이 안 됐음. **로컬 Jekyll 빌드가 성공해도 GitHub Pages 빌드가 실패할 수 있다는 걸 인지할 것** — 완전히 신뢰할 수 있는 사전 검증 수단이 아님.

**수정**: `_config.yml`의 `exclude:` 목록에 `handover.md` 추가(README.md/Gemfile과 동일하게 사이트 빌드에서 완전히 제외). 추가로 handover.md 본문에서 리터럴 `{{ }}`/`{% %}` 표현은 전부 우회 서술로 변경(방어적 조치 — exclude 처리로 이미 근본 해결됐지만, 혹시 나중에 exclude 목록에서 실수로 빠지더라도 재발하지 않도록).

**다음 세션부터 반드시 지킬 것 (작업 방식에도 반영)**:
1. **`git push` 성공 = 배포 성공이 아니다.** push 후 반드시 GitHub Pages 빌드 상태를 확인할 것 — `curl -H "Authorization: Bearer $TOKEN" https://api.github.com/repos/canghun13/petpawcalc/pages/builds/latest`로 최신 빌드의 `status`/`error` 필드를 확인하거나, `/actions/runs?per_page=1`로 가장 최근 run의 `conclusion`이 `success`인지 확인. 매 세션 마지막 push 후 이 확인을 빠뜨리지 말 것.
2. **front matter 없는 `.md` 파일을 새로 만들 때는 반드시 `_config.yml`의 `exclude:`에 추가할 것** (또는 front matter를 넣어 명시적으로 페이지로 관리할 것). 현재 exclude 목록: `README.md`, `handover.md`, `Gemfile`, `Gemfile.lock`. **`llms.txt`는 절대 exclude에 넣지 말 것** — `.txt` 확장자라 `jekyll-optional-front-matter` 플러그인의 대상이 아니라 애초에 안전하고(이번 사고와 무관), 무엇보다 `llms.txt`는 `petpawcalc.com/llms.txt`로 **공개 서빙되어야 하는 파일**이라 exclude에 넣으면 그 자체로 기능이 깨짐(실제로 이번에 실수로 넣었다가 바로 되돌림 — `.md` 확장자 파일과 `.txt` 확장자 파일을 혼동하지 말 것).
3. **문서(handover.md 등) 안에 Liquid 문법 예시를 적을 때는 리터럴 `{{ }}`/`{% %}`를 절대 쓰지 말 것** — 코드가 아니라 설명 텍스트로 풀어 쓸 것 (예: "이중 중괄호 문법" 같은 서술로 대체). exclude 처리로 근본 해결됐지만 습관화할 것.
4. **GH Pages는 Jekyll 3.10.0에 고정**돼 있고 로컬에서 동일 버전 재현이 안 됨(rubygems.org 네트워크 차단) — 로컬 빌드 성공을 과신하지 말 것. 의심스러운 변경은 실제 push 기반 이진 탐색이 가장 확실한 검증 수단임을 기억할 것.

---

### 세션 N — GSC 7/20 데이터 분석 + 체중감량 계산기 확장(기존 자산 강화) + 신규 카테고리 후보 2건 조사 (7/20, 주간 작업)

사용자 요청 핵심: 밀린 주간 작업 진행. (1) 신규 GSC(Search Console + Analytics) 내보내기 확인 후 신규/보강 판단, (2) 신규 콘텐츠는 기존 파일 중복 체크 + 웹 검색 경쟁강도 확인 + 롱테일 키워드 전략, (3) AI검색은 도메인 권위보다 콘텐츠(문제해결·비교분석)가 중요하다는 트렌드를 신규뿐 아니라 보강에도 반영, (4) AdSense 수익화 관점 우선순위 판단, (5) 대시보드 없이 텍스트로만 보고, (6) 작업 후 handover.md 갱신 후 같이 push.

**1. GSC 데이터 분석 (Coverage + Performance, 지난 3개월 누적 / GA는 6/22~7/19)**

- **Coverage 미색인 수치가 세션 J(7/15) 이후 4개 데이터 포인트 연속 완전히 동일함 — 발견됨-미색인 15개 + 크롤링됨-미색인 6개 = 21개, 세션 J→L→M→이번 전부 21개로 변화 없음.** 세션 F·H 때 2세션 연속 정체(38개)됐던 것보다 훨씬 긴 정체 — 이번 세션부터는 "Coverage 리포트 집계 지연" 가설보다 "실제로 정체" 가능성에 무게를 두는 게 맞다고 판단. **사용자에게 개별 URL 재크롤 요청("색인 생성 요청" 버튼, GSC UI)을 적극 권유할 시점.** 에이전트는 GSC API 접근 권한이 없어 직접 요청 불가 — 아래 "미노출 URL" 목록 중 우선순위 높은 것부터 사용자가 직접 눌러보는 걸 권장.
- **Performance 페이지별 노출 대조로 "미노출 추정 URL"을 다시 역산(방법은 세션 J와 동일, trailing slash 포함 매칭)**: 사이트 전체 URL 66개 중 Performance에 노출이 잡힌 건 35개, 나머지 31개가 미노출 추정. 이 중 체크리스트 3개+인덱스, `flea-tick-prevention-cost`(post+tool), `kitten-weight-chart-by-breed-size`는 전부 세션 M(7/17)에 만든 지 3일밖에 안 된 페이지라 미노출이 당연함 — 제외하고 보면:
  - **세션 J에서 FAQ 가시화까지 마쳤던 미색인 tool 7개 중 5개가 이번에도 여전히 노출 0**: `annual-pet-cost-calculator`, `cat-pregnancy-calculator`, `cat-vet-visit-scheduler`, `dog-heat-cycle-calculator`, `dog-pregnancy-calculator`, `pet-grooming-cost-calculator`, `spay-neuter-cost-calculator` — 이 중 온페이지 요인(FAQ 가시성)은 이미 다 고쳤는데도 세션 J(7/15)부터 지금까지 5일 이상 그대로. 특히 `dog-pregnancy-calculator`/`cat-pregnancy-calculator`는 세션 M에서 "진단방법 비교표"까지 추가했는데도 미노출 — **온페이지 콘텐츠 보강만으로는 안 되는 구간에 들어선 것으로 보이고, 위 Coverage 정체와 함께 재크롤 요청이 필요한 핵심 근거.**
  - `cat-quality-of-life-calculator`(tool)도 미노출 — 짝 포스트 `cat-quality-of-life-assessment`는 노출 2건 있음(비대칭).
  - blog 쪽 미노출은 대부분 세션 B 날짜조작 수정(7/10) 이전 작성 포스트라는 기존 가설과 일치하는 오래된 포스트들(`dog-age-human-years` 등) — 이 패턴은 세션 H/J 이후 변화 없음.
- **Performance 쿼리 데이터의 새로운 신호 — "maine coon weight predictor"**: 세션 M에서 만든 `kitten-weight-chart-by-breed-size`(작성 3일 차) 관련 쿼리가 **벌써 17위·클릭 1건**으로 잡힘. 신생 페이지치고 이례적으로 빠른 반응이고, 정확 문구("weight predictor")가 페이지 본문에 없었던 걸 발견해 이번 세션에 보강함(아래 3번 참고) — 저경쟁 롱테일 하나가 실제로 통하기 시작한 첫 사례라 다음 세션에서 순위 변화를 꼭 확인할 것.
- **`what-to-feed-pregnant-dog`(101노출대) 자기잠식 의심은 이번에도 미확정 — 세션 H부터 5세션째 열린 이슈.** GSC 웹 UI 페이지×쿼리 교차확인 없이는 계속 확정 불가. 사용자가 직접 GSC UI에서 두 URL을 필터링해 확인해주지 않는 한 이 항목은 계속 "보류"로 열어둘 수밖에 없음 — 다음에도 사용자가 대신 스크린샷 등으로 알려주지 않으면 "확정 불가로 공식 종결" 처리 권장(세션 M 마지막 항목에서 이미 이 옵션이 언급됐었음).

**2. 신규 카테고리 후보 조사 (세션 M이 남긴 파이프라인 2건 웹 검색으로 마무리)**

- **첫해 입양 비용 계산기 (annual-pet-cost-calculator와 다른 앵글) — 레드오션 확정, 기각**: 웹 검색 결과 CalcBee의 "Kitten First Year Cost Calculator" 전용 페이지, petcost-calculator.com(300+ 품종별 첫해/평생 비용 리포트), breedtools.com("Cost of Owning a Dog Calculator" — first year vs ongoing 브레이크다운 포함), calcuja.com(세션 I에서 이미 확인된 경쟁사, dog/cat/rabbit 첫해 비용까지 다룸) 등이 이미 이 앵글을 깊게 다루고 있음. 게다가 사이트에 이미 `annual-pet-cost-calculator`가 있어 첫해 비용 전용 신규 페이지는 자기잠식 위험도 있음 — 기각.
- **체중감량/칼로리 결핍 계산기 — 세션 M 평가(권위 있는 경쟁자 있음)보다 더 포화된 것으로 재확인**: World Pet Obesity Association과 Association for Pet Obesity Prevention 둘 다 RER/MER 기반 체중감량 계산기·단계별(step-based) 감량 플랜 도구를 무료로 제공 중이고, Pet Nutrition Alliance도 수의사 전용 버전을 운영. 상업 경쟁사도 petcalorie.com(290+ 품종 DB, DVM 감수 명시)까지 가세 — **완전 신규 페이지로는 승산이 낮다는 세션 M의 판단이 재확인됨.**
- **판단**: 신규 페이지 대신 세션 M이 제안했던 대로 **기존에 이미 노출·색인이 있는 `pet-food-calorie-calculator`를 체중감량 모드로 확장**하는 저위험 접근으로 진행(아래 3번). 새 URL을 만들지 않으니 위에서 확인한 "미노출 문제"에 페이지 하나를 더 얹는 리스크도 없음.

**3. 실제 진행한 작업**

- **`tools/pet-food-calorie-calculator.html` 체중감량 모드 신규 추가**(신규 페이지 아님, 기존 지표 있는 페이지 확장):
  - "Goal" 선택(현재 체중 유지 / 체중 감량)을 추가, 감량 선택 시 목표/이상 체중 입력 필드가 나타나고 생애주기·활동량·중성화 필드는 숨겨짐(감량 계산은 목표체중 기반 RER 방식이라 해당 입력이 불필요 — 경쟁사인 WPOA/APOP가 실제로 쓰는 "목표체중 RER × 1.0" 방식을 그대로 채용, 웹 검색으로 확인한 공식).
  - 결과에 안전한 감량 속도(개 월 3~5%, 고양이 월 1~2% — 복수 수의사 단체 소스로 확인) 기준 예상 소요 기간을 함께 표시.
  - **AI검색 대응 콘텐츠 신규 추가(사용자 이번 세션 지시 반영)**: "Two Ways Vets Calculate Weight-Loss Calories" **비교표**(목표체중 RER 방식 vs 퍼센트 감량 방식, 각각 어떤 케이스에 맞는지), "Why Isn't My Pet Losing Weight?" **문제해결형 체크리스트**(간식 과다·타인 급여·오래된 체중값·정체기·갑상선저하증 등 원인별로 정리).
  - FAQ 4개 신규(스키마+본문 1:1): "Is there a dog or cat weight loss calculator?", "How fast should my dog/cat lose weight safely?"(고양이는 hepatic lipidosis 위험 명시 — 웹 검색으로 확인한 사실), "Why isn't my pet losing weight even though I'm feeding less?".
  - 헤더 문구·meta description에도 "weight-loss" 문구 반영(정확 문구 노출, 세션 C 교훈 적용).
- **`dog-weight-calculator.html`/`cat-weight-calculator.html`에 "ideal weight calculator" 정확 문구 FAQ 각 1개 추가**: "ideal dog weight calculator"(8노출)·"ideal cat weight calculator"(1노출)·"dog ideal weight calculator"(2노출) 등 근접 변형 쿼리 합계 11노출에 대응, 정확 문구가 본문에 없었던 걸 보강(세션 C 패턴 재적용).
- **`kitten-weight-chart-by-breed-size` 포스트에 "maine coon weight predictor" 정확 문구 FAQ 1개 추가**: 신생 페이지인데도 벌써 17위·클릭 1건 나온 쿼리라 우선순위 높게 판단, front matter `faqs:`와 본문 양쪽에 동일 질문("Is there a Maine Coon weight predictor?") 추가.
  - **⚠️ 이 작업 중 실수 발생 및 즉시 수정**: str_replace로 FAQ 항목을 추가하면서 front matter를 닫는 `---` 구분자를 실수로 함께 지워버림(front matter가 안 닫혀서 YAML 파싱 자체가 깨지는 상태였음). **commit 전 QA 단계에서 발견해 바로 복구** — 실서비스에 반영된 적은 없음. **교훈: front matter 배열(`faqs:` 등) 끝부분에 str_replace로 새 항목을 추가할 때는 old_str/new_str에 뒤따르는 `---` 구분자까지 반드시 포함시킬 것 — 배열 마지막 항목 바로 뒤에 무엇이 오는지(닫는 `---`인지 다음 필드인지) 매번 확인 후 편집.** 세션 M의 Liquid 문법 배포 장애와는 다른 유형이지만, "handover.md 등 문서 편집 시 안전장치"뿐 아니라 "콘텐츠 파일의 YAML 편집 시에도 종결자 보존을 매번 명시적으로 확인할 것"을 체크리스트에 추가함(아래 5번 참고).

**4. AdSense 수익화 관점 우선순위 판단**

- 클릭 자체가 여전히 극소수인 단계라(사이트 전체 누적 클릭 한 자릿수 수준 유지), 이번 세션도 **"신규 페이지보다 이미 노출/색인 있는 자산 강화"** 원칙을 유지 — 실제로 신규 URL은 0개 추가(체중감량 모드는 기존 페이지 확장), 대신 이미 지표가 있는 3개 페이지(calorie calculator, dog/cat-weight-calculator, kitten-weight-chart)를 보강.
- **Coverage 21개 정체가 4세션 연속 이어지는 것과, FAQ 가시화까지 마친 tool 5개가 여전히 미노출인 것은 온페이지 작업만으로는 더 이상 해결이 안 되는 구간에 들어섰다는 신호** — 다음 세션 최우선 순위는 콘텐츠 보강이 아니라 **사용자가 GSC UI에서 개별 URL 재크롤을 직접 요청하는 것**. 온페이지 보강은 계속하되, 이 부분은 콘텐츠로 해결할 수 있는 한계에 도달했다고 명확히 보고.
- "maine coon weight predictor"처럼 신생 페이지의 롱테일 쿼리가 3일 만에 클릭까지 나온 사례는 **롱테일 전략이 실제로 작동하고 있다는 첫 정량적 근거** — 이런 신호가 나오면 해당 정확 문구를 즉시 본문에 반영해 강화하는 게(이번 세션에 한 것처럼) 신규 페이지 제작보다 훨씬 빠르고 리스크 낮은 ROI라는 걸 다음 세션에도 원칙으로 유지.

**5. QA**

- 전체 `_posts/*.md`(33개) + `tools/*.html`·`checklists/*.html`(27개) front matter YAML 파싱 전수 통과.
- 수정 파일 3개(`pet-food-calorie-calculator`, `dog-weight-calculator`, `cat-weight-calculator`) JSON-LD FAQPage 스키마-본문 h3 1:1 매칭 코드로 확인(9/9, 5/5, 5/5), div 개수 매칭(15/15, 15/15, 18/18), table/tr/thead/tbody 태그 매칭(신규 비교표).
- `kitten-weight-chart-by-breed-size` front matter 종결자 사고 발견 즉시 복구 후 재검증(YAML 파싱 성공, FAQ 스키마-본문 7/7 매칭 확인).
- 전체 저장소(post+tool+checklist+index+header+footer+llms.txt) 링크 재스캔(trailing slash 무관 매칭) — 깨진 링크 0건.
- slug/permalink 전체 중복 검사(포스트 33개, tool/checklist 25개) — 중복 없음.
- `index.html`/`tools/index.html`의 tool-card 개수(22) = 실제 `tools/*.html` 파일 개수(22) 일치 확인 — 이번 세션은 신규 URL을 만들지 않았으므로 공통 파일(index/footer/llms.txt) 동기화 작업 자체가 불필요했음(고아 페이지 리스크 없음).

**다음 세션에서 확인할 것**:
- **Coverage 21개가 5번째 데이터에서도 그대로면, "관찰"이 아니라 사용자에게 개별 URL 재크롤 요청을 명확히 권유할 것** — 특히 `dog-pregnancy-calculator`/`cat-pregnancy-calculator`/`annual-pet-cost-calculator`/`cat-vet-visit-scheduler`/`dog-heat-cycle-calculator`/`pet-grooming-cost-calculator`/`spay-neuter-cost-calculator`/`cat-quality-of-life-calculator` 8개 tool 우선순위.
- 이번 세션 보강한 3개 페이지(calorie calculator 체중감량모드, dog/cat-weight-calculator ideal weight FAQ, kitten-weight-chart maine coon predictor FAQ)의 다음 GSC 데이터에서 노출/순위 변화 확인.
- "maine coon weight predictor" 순위가 17위에서 더 개선되는지, 그리고 이 신호가 "신생 페이지의 저경쟁 롱테일이 조기에 반응한다"는 가설을 뒷받침하는 재현 사례로 이어지는지 계속 관찰.
- `what-to-feed-pregnant-dog` 자기잠식 의심(5세션째 미확정) — 사용자가 GSC UI 크로스 체크를 해줄 수 없다면 다음 세션에 "확정 불가로 보류 종결" 처리를 제안할 것.
- GA 데이터(6/22~7/19)는 이번에 받았지만 신규/보강 판단에 직접 쓸 만한 신호는 없었음(활성 사용자 61명, 유입은 여전히 (direct)/pitchwall.co/Findly.tools 등 런칭 디렉토리 위주, organic은 bing 3명·google 2명 수준) — AI 검색엔진(ChatGPT/Perplexity 등)발 유입은 이번 GA 리포트의 소스/매체 목록에서 식별되지 않음(있었다면 referral로 잡혔을 것). 다음 세션에도 계속 확인 필요.
- **문서/콘텐츠 파일 편집 시 종결자 보존 확인을 QA 체크리스트에 정식 추가**: front matter의 배열형 필드(`faqs:` 등) 끝에 새 항목을 str_replace로 추가할 때, old_str/new_str 양쪽에 뒤따르는 `---` 구분자(또는 다음 필드)까지 포함해서 편집 전후 구조가 그대로 보존되는지 diff로 확인할 것 — 이번 세션에 실제로 한 번 놓쳤다가 QA 단계에서 발견(3번 항목 참고).

### 세션 N (계속) — 사용자 리포트 버그 수정: cat-weight-calculator 품종별 체중표 모바일 반응형 깨짐 (7/20)

세션 N 작업물 배포 직후 사용자가 396px 모바일 뷰 스크린샷으로 `cat-weight-calculator.html`의 "Typical Healthy Weight Ranges by Breed" 표가 반응형으로 안 잡힌다고 리포트.

**원인**: 이 표는 세션 M에서 만들어 전역 적용한 `.table-wrapper` 클래스(`css/style.css`)를 쓰지 않고, 그보다 오래된 인라인 스타일(`padding: 10px 14px` 고정)로 만들어져 있었음 — **세션 M의 table-wrapper 전역 적용 작업(session M 항목 참고)이 `class="table-wrapper"`를 쓰는 표들만 대상으로 했기 때문에, 인라인 스타일로 따로 만들어진 이 레거시 표는 그 작업에서 완전히 누락됐던 것**. `.table-wrapper` 클래스에는 `@media (max-width: 600px)`에서 padding/font-size를 축소하는 규칙이 있는데 이 표엔 그게 없어서, 3컬럼(Breed/Female/Male) + 긴 텍스트("Domestic Shorthair / Mixed")가 좁은 화면에서 제대로 줄어들지 않고 깨짐.

**수정**: 인라인 스타일을 전부 제거하고 공용 `.table-wrapper` 패턴(다른 페이지들과 동일)으로 교체.

**부수 발견 (다음 세션 확인 필요)**: 전체 저장소를 `<table` 태그 기준으로 재스캔한 결과 같은 인라인 스타일 패턴(class="table-wrapper" 미사용)의 표가 `annual-pet-cost-calculator.html`, `pet-insurance-cost-estimator.html`에도 있음 — 단 이 둘은 JS로 동적 생성되는 **2컬럼(라벨+금액) result-box 내부 표**라 컬럼 수·텍스트 길이가 훨씬 짧고 현재까지 신고된 증상도 없음. `.table-wrapper` 클래스는 `min-width: 480px`를 강제하는데, 이 두 표가 들어가는 `result-box`는 `.tool-box`(`padding: 32px`) 안에 있어 모바일에서 480px보다 훨씬 좁은 게 거의 확실 — 그대로 적용하면 지금은 없는 불필요한 가로 스크롤바가 새로 생길 위험이 있어 이번엔 보류. **다음 세션에서 이 두 페이지도 실제 모바일 스크린샷으로 확인 후, 필요하면 `.table-wrapper`를 그대로 쓰지 말고 이 2컬럼 result 표 전용의 더 가벼운 반응형 규칙(예: 좁은 화면에서 padding만 줄이는 별도 클래스)을 만들 것.**

**교훈(체크리스트에 반영)**: `.table-wrapper` 같은 공용 CSS 클래스를 "전체 적용 완료"로 표시할 때는 **`class="table-wrapper"` 문자열로 검색하지 말고 `<table` 태그 자체로 전수 검색**해야 함 — 클래스를 안 쓰고 인라인 스타일로 따로 만들어진 표는 클래스명 검색으로는 잡히지 않음(이번에 실제로 이렇게 놓친 사례). 앞으로 "표 관련 작업 완료" QA 항목에는 `class="table-wrapper"` 검색이 아니라 `<table` 태그 전수 검색 + 각각이 table-wrapper로 감싸져 있는지 확인하는 스크립트를 표준으로 쓸 것.

**QA**: div(18/18), table/tr/thead/tbody/th/td 태그 매칭, JSON-LD 2개 유효성, FAQ 스키마-본문 1:1 매칭(5/5) 유지 확인, front matter YAML 파싱 통과. 커밋 → push → GitHub Pages 빌드 `built` 확인(에러 없음, 커밋 해시 일치).

---

### 세션 O — ⚠️ 경쟁 지형 대전환 확인 + 신규 클러스터 "훈련(Training)" 추가 (7/22)

사용자 요청: 오늘은 신규 콘텐츠 우선(클러스터가 먼저, 그래야 롱테일이 더 나온다는 논리) + 공격적으로, 단 경쟁사보다 더 디테일하게 만들어서 이기는 전략. 대시보드 없이 텍스트 분석만.

**⚠️ 가장 중요한 발견 — pet-calculator 니치의 경쟁 지형이 최근 몇 주 사이 완전히 바뀜.** 앞으로 모든 신규 키워드 조사에서 이 경쟁사 목록을 최우선으로 체크할 것:

- **furcalc.com** — 개/고양이/수족관/가금류/파충류/축산까지 **167개 이상**의 계산기를 보유한 대형 경쟁사. "DVM 검수", AAFCO/NRC/AKC/Merck 수의학매뉴얼 출처 인용까지 갖춤. 우리 사이트의 거의 모든 카테고리(체중/나이/칼로리/임신/예방접종)와 겹치고, 우리가 없는 것도 다수(초콜릿 독성, 물 섭취량, 크레이트 사이즈, 배변훈련, 산책거리/속도, 기대수명, 리터/구충제 용량)까지 보유. 단, **콘텐츠가 전반적으로 얕음** — 공식 하나 + 반복되는 "Why this next" 크로스프로모 박스 위주의 정형화된 패턴(AI 대량생성 느낌). 우리가 "디테일로 이긴다"는 전략의 핵심 타겟.
- **calcbee.com** — 다마리반려동물 비용, 펫디파짓vs펫렌트 계산기 등 보유 (기존에도 알려진 경쟁사, 범위 계속 확장 중)
- **calculatorsfordogs.com** — 응급실비용, 크레이트사이즈(IATA 항공규격까지), 월핑박스사이즈 계산기 등 개 전문 계산기 사이트
- **vetcostcalc.com** — 주(state)별·30개 이상 시술별 수의사 비용 추정, 도시별 비교까지 갖춘 정교한 전문 사이트, 임베드 위젯까지 제공
- **kittycalcs.com, superpawculators.com** — 고양이 특화 계산기(리터, 그로스, 임신 등)
- **dogsizeguide.com, mylittleandlarge.com, puppygrowthcalculator.com, thepetbench.com, petcratesdirect.com** — 크레이트 사이즈만 8곳 이상이 경쟁 중인 완전 레드오션

**오늘 기각한 후보 (전부 위 경쟁사가 이미 보유)**: 강아지 배변훈련 계산기(furcalc, 단독 — 그래도 얕아서 채택함, 아래 참고), 크레이트 사이즈 계산기(8곳+), 2번째 반려동물/다마리가구 비용 계산기(calcbee + AKC/Trupanion/Rover 가이드까지), 고양이 리터/급수량 계산기(furcalc+kittycalcs+superpawculators 3중), 응급실 비용 계산기(calculatorsfordogs+vetcostcalc), 펫디파짓/펫렌트 계산기(calcbee+rentlatefee.com), 월핑박스 사이즈 계산기(calculatorsfordogs, 게다가 브리더 한정 수요라 우선순위 낮음), 반려동물 상실/그리프 지원 콘텐츠(계산기 경쟁자는 없지만 RSPCA·대학 수의대 등 대형 기관 콘텐츠가 이미 장악, 계산기 포맷과도 안 맞고 애드센스 수익화도 약함 — 사이트 정체성과 안 맞아 보류).

**신규 클러스터로 채택: 훈련(Training) — 개/고양이 페어링**
- 근거: 강아지 쪽은 furcalc 단 1곳만 있고 그마저 "나이+1시간" 공식 하나만 제공하는 얕은 버전(품종크기별 차이, 주/야간 차이 없음) — 디테일로 이길 여지가 명확함. 고양이 쪽(리터훈련 타임라인, 리터박스 "부피/비용" 계산기가 아니라 "행동/훈련 타임라인" 앵글)은 **계산기 경쟁자 0곳** — PetMD/Chewy/Purina/Hill's 등 가이드 글만 있고 인터랙티브 툴은 없음.
- 기존 예방접종 스케줄 계산기(사회화 시기=접종 시기)와 자연스럽게 교차링크되는 것도 채택 이유.

**신규 파일 (2개, dog/cat 페어링 원칙 유지)**:
1. `tools/puppy-potty-training-calculator.html` — 나이(주/개월 선택) + 예상 성견 크기(toy/medium/large) + 훈련방식(crate/pad/mixed) 입력 → 주간/야간 방광보유시간 분리 계산, 하루 배변브레이크 횟수, 트리거별(기상/식후/낮잠후/놀이후) 체크리스트, 품종크기별 하우스트레이닝 완료 예상시기(토이종 9-12개월 vs 대형 6-8개월) 테이블. **AI검색 대응 콘텐츠**: 크레이트훈련 vs 패드훈련 비교표, "6개월인데 왜 아직도 실수하나" 원인별 문제해결 섹션(스케줄 미조정/환경변화/감독공백/사후처벌/의학적원인/품종기대치 오해). FAQ 6개.
2. `tools/kitten-litter-training-timeline.html` — 주령 입력(+가구 내 고양이 수) → 단계별(3주 미만/3-4주/5-8주/9-16주/4-6개월/6개월+) 기대행동·박스크기·리터종류 안내, n+1 박스개수 규칙 자동계산. **비교분석**: 클럼핑vs논클럼핑(10주 미만 삼킴위험 명시), 커버드vs오픈박스 비교표. **문제해결**: "리터박스를 안 써요" 원인을 설정/영역다툼/환경변화/의학적 4갈래로 분류. FAQ 6개.

**교차링크(양방향 처리)**: 신규 2개 → 기존 예방접종계산기/체중계산기/체크리스트로 링크 추가. 역방향으로 `dog/cat-vaccination-schedule-calculator.html`, `checklists/new-puppy-checklist.html`, `checklists/new-kitten-checklist.html`에도 신규 훈련 툴 링크를 추가해 넣음 — 새 페이지가 고아 페이지가 되지 않도록 기존 강한 페이지에서 들어오는 링크를 처음부터 확보.

**사이트 공통 파일 동기화**: `index.html`, `tools/index.html`(검색용 data-title/desc/tags 속성 포함), `_includes/footer.html`, `llms.txt` 전부 갱신. "New" 뱃지를 `flea-tick-prevention-cost-calculator`에서 신규 2개로 이동(사이트는 최신 항목에만 New 뱃지를 붙이는 관행).

**QA**: 전체 `_posts`+`tools`+`checklists`(62개) front matter YAML 전수 통과, JSON-LD 오류 0건, 신규 2개 FAQ 스키마-본문 1:1 매칭(6/6, 6/6), tool-card 개수 index.html/tools/index.html 모두 24개로 실제 파일과 일치, 전체 링크 재스캔 0건 깨짐, permalink 중복 없음. **JS 계산 로직은 node로 직접 실행해서 FAQ에 명시한 수치(2개월=3시간, 4개월=5시간 등)와 실제 계산 결과가 일치하는지까지 검증함** — 이번 세션에 새로 도입한 검증 방식, 앞으로 계산기형 신규 툴을 만들 때 표준 QA 단계로 포함시킬 것.

**부수 발견**: `dog-cat-dental-cleaning-cost` 블로그 포스트에 이미 "무마취 스케일링을 주요 수의학 단체가 반대하는 이유"가 언급돼 있음을 확인 — 지난 세션 중반에 "무마취 vs 마취 덴탈클리닝 비교"를 신규 롱테일 후보로 검토했었는데, 이미 부분적으로 다뤄지고 있어 완전 신규는 아님. 다음에 이 앵글을 확장하려면 기존 포스트 내용부터 먼저 확인할 것.

**다음 세션에서 확인할 것**:
- 오늘 만든 훈련 클러스터 2개의 GSC 노출/색인 여부 확인(신규라 최소 1-2주는 필요).
- **사용자가 오늘 "기존 자산 롱테일도 다 할거다"라고 했는데 시간상 신규 클러스터까지만 진행함 — 다음 세션(또는 이어지는 대화)에서 기존 자산 롱테일 파고들기를 이어서 할 것.**
- 훈련 클러스터에 동반 블로그 포스트(예: "Puppy Potty Training Timeline: How Long It Really Takes")를 페어링할지 검토 — 지금은 tool 페이지 자체에 비교/문제해결 콘텐츠를 충분히 넣어서 급하지 않지만, 다른 클러스터들처럼 tool+post 페어링이 사이트 관행이라 트래픽 보고 판단.
- furcalc.com 등 위 경쟁사 목록은 앞으로 매 키워드 조사 세션마다 반복 체크할 것 — 확장 속도가 빨라서(관찰된 페이지들이 대부분 "Updated 2026-05-16" 근처로 최근 갱신됨) 몇 주 전엔 비어있던 자리가 금방 채워질 수 있음.

---

### 세션 O (계속) — 강아지 동반 블로그(Potty Training Regression) 추가, 고양이는 보류 (7/22)

사용자가 "강아지 쪽은 할 수 있는 거 다 진행, 고양이는 강아지 끝나고 다시 보자"고 요청. 강아지 배변훈련 계산기의 롱테일 블로그 후보를 추가로 4개 조사:

1. **Potty Training Regression** (4-6개월/7-9개월 재발) — **채택**. 경쟁자가 SpiritDog·Sniffspot·Woofz·Zigzag·AlphaPaws 같은 소규모 훈련서비스 블로그뿐이고 AKC/Chewy/WebMD급 대형 브랜드나 pet-calculator 경쟁사는 이 앵글을 다루지 않음.
2. **품종별 하우스트레이닝 기간** ("how long by breed size") — 기각. SpiritDog, Vety, Rover, Chewy, Sniffspot, USServiceAnimals 등이 이미 두껍게 커버 + **우리 계산기 툴 자체 콘텐츠와도 내용이 겹쳐서** 블로그로 따로 만들 실익이 낮음.
3. **흥분성/복종성 배뇨** (excited/submissive urination) — 기각. AKC, Chewy, WebMD, Preventive Vet, Four Paws, Pupford 등 대형 브랜드가 이미 장악. 애초에 하우스트레이닝 실패가 아니라 별개의 감정적 반응이라 우리 계산기 툴과의 연결성도 약함.
4. **야간 배변훈련** ("sleep through the night") — 기각. Rover, Chewy, Beco, Bulldogology, Suburban K9, PiddlePatch 등이 이미 두껍게 커버.

**신규 파일**: `_posts/2026-07-22-puppy-potty-training-regression.md` — 4-6개월/7-9개월 두 재발구간을 표로 구조화, 행동적 원인 vs 의학적 원인(UTI 등) 구분표, 6단계 리셋플랜, FAQ 6개. `puppy-potty-training-calculator.html`에서 이 포스트로, 포스트에서 계산기로 양방향 링크.

**⚠️ 기술적 이슈 발견 (중요, 앞으로 블로그 포스트에 표 넣을 때마다 적용할 것)**: 처음에 표를 `<div class="table-wrapper">` + 마크다운 테이블 조합으로 넣었다가, QA 단계에서 **이 사이트의 kramdown 설정에 `markdown="1"` 속성이 없어서 raw HTML div 안의 마크다운 테이블이 처리 안 될 위험**을 발견함(`_config.yml`에 별도 kramdown 옵션 없음 = 기본값 사용, 기본값은 raw HTML 블록 내부를 마크다운으로 처리하지 않음). 기존 블로그 포스트(`flea-tick-prevention-cost.md`)를 확인해보니 전부 `table-wrapper` div 없이 **순수 마크다운 테이블만** 쓰고 있었음 — 이번 포스트도 동일하게 순수 마크다운 테이블로 바꿔서 회피함. **앞으로 블로그 포스트(`_posts/`)에 표를 넣을 때는 절대 `<div class="table-wrapper">`로 감싸지 말 것 — tool 페이지(`tools/`, HTML 파일)에서만 이 패턴을 쓸 것.** 만약 블로그에서도 반응형 표 스타일이 필요하다고 판단되면, 먼저 로컬에서 `markdown="1"` 속성 추가 후 실제 빌드로 검증하거나, 순수 HTML `<table>` 태그로 직접 작성하는 방식을 검토할 것 — 마크다운 문법을 raw div 안에 그대로 넣는 방식은 검증 없이 쓰지 말 것.

**QA**: 전체 63개 파일 YAML 통과, JSON-LD 오류 0, slug 중복 없음(34개), front matter-본문 FAQ 1:1 매칭(6/6), 링크 재스캔 0건. 커밋 → push → GitHub Pages 빌드 `built` 확인.

**다음(고양이)**: 사용자가 "강아지 끝나면 고양이 다시 보자"고 했음 — 이전에 조사한 3개 각도(리터박스 안써요/리터를 먹어요/나이든고양이 리터훈련)는 전부 Hepper/Best Friends/IAMS/Hill's/PetMD/Rover/Cats.com/Lemonade급 대형 브랜드가 장악한 상태라 재검토 필요. 고양이 전용으로 더 좁은 각도(예: 다마리 가정에서의 영역다툼형 리터박스 회피, 이사/이사 후 재훈련 등)를 다음에 조사할 것.

---

### 세션 O (계속) — ⚠️ 전략 전환: "완벽한 무경쟁"보다 "페이지 수" 우선 (7/22)

**배경**: 세션 O 후반부에 기존 클러스터 강화용 신규 키워드를 GSC → 영어 웹서치 → 한국어(네이버) 검색 → 포럼(레딧류)까지 방식을 바꿔가며 총 15개 이상 조사했으나(고양이 리터훈련 관련 5개 + 치석관리비교/토끼나이계산기/간식10%룰/성견입양체크리스트/강아지목욕주기/저체중강아지/생식비율계산기/펫보딩비용 등) 전부 대형 브랜드나 furcalc 같은 전용 계산기 사이트가 이미 장악한 상태였음. 에이전트가 "완벽하게 무경쟁인 키워드만" 고집하며 계속 기각하자, **사용자가 명확히 방향을 수정**: "우리 2달 넘어가는데 페이지 수 너무 적어 승부 자체가 안 된다. 이대로 가면 도메인 폐쇄로 갈 수밖에 없다 — 경쟁이 있어도 롱테일로, 또는 우리 강점에 붙여서 진행해라."

**교훈(중요, 앞으로 계속 적용할 것)**: 신규 콘텐츠 판단 기준을 "경쟁자가 0곳" 에서 **"경쟁자가 있어도 우리만의 차별화 각도(주로 비용 계산)를 붙일 수 있으면 진행"** 으로 낮춤. 페이지 수 자체가 사이트의 존속과 직결된 문제라는 걸 이번에 명확히 인지함. 다음 세션들에서도 이 기준을 유지할 것 — 경쟁자 존재 자체를 기각 사유로 쓰지 말고, "우리가 뭘 다르게 할 수 있나"를 먼저 물을 것.

**신규 파일 4개 (이 새 기준으로 진행)**:
1. `tools/raw-feeding-calculator.html` — 생식(BARF/PMR) 계산기는 furcalc 포함 7곳 경쟁자가 있었지만, **전부 비율 계산만 하고 비용은 안 다룸** — 월간/연간 비용 추정을 붙여 차별화(그로서리/정육점벌크/프리미엄브랜드 3단계 비용 비교표 포함). 개/고양이 페어링, 80/10/10(PMR) vs 70/10/10+10%veg(BARF, 개 전용) 비교, FDA/AVMA 식중독균 경고, 전환 스케줄 포함.
2. `tools/pet-boarding-cost-calculator.html` — 경쟁자 다수(TrustedHousesitters, Yelp, CareCredit, HomeGuide, furcalc, AgentCalc 등) 있었지만, 우리 COST 클러스터 확장이자 예방접종계산기와의 자연스러운 교차링크(보딩 시설 대부분 접종증명 요구) 때문에 진행. 켄넬/펫호텔/럭셔리리조트/인홈시터 4개 옵션 + 공휴일 프리미엄(+22%) + 부가서비스 반영.
3. `_posts/2026-07-22-how-to-tell-if-dog-is-underweight.md`, `_posts/2026-07-22-how-to-tell-if-cat-is-underweight.md` — 기존 "과체중 판별" 포스트(개/고양이 둘 다 있음)의 반대편을 채워 **체중 클러스터를 완성**. 외부 경쟁(DogTime/AKC/Hill's/WebMD 등)은 있지만 우리 사이트 내부적으로는 완전히 새로운 콘텐츠(자기잠식 없음, 오히려 클러스터 완결성 강화). 사이트하운드 등 자연적으로 마른 견종 구분, 원인별 표, 안전한 체중증량 플랜. 고양이는 갑상선기능항진증/신부전 등 의학적 원인과 지방간(hepatic lipidosis) 위험을 강조.

**교차링크**: 신규 4개 전부 기존 강한 페이지(pet-food-calorie-calculator, annual-pet-cost-calculator, dog/cat-weight-calculator, 예방접종계산기)와 양방향 연결.

**사이트 공통 파일**: index.html/tools/index.html(검색용 data속성 포함)/footer.html/llms.txt 전부 동기화. New뱃지를 신규 2개(raw-feeding, pet-boarding)로 이동.

**QA**: 전체 67개 파일 front matter YAML 전수 통과, JSON-LD 오류 0, FAQ 스키마-본문 1:1 매칭(신규 4개 전부), slug/permalink 중복 없음(36/29개), tool-card 개수 일치(26=26=26), 전체 링크 재스캔 0건 깨짐. 계산기 2개는 JS 로직을 node로 직접 실행해 FAQ 명시 수치와 대조 검증(생식: 45lb 성견 PMR $3.5/lb → 월 $118, FAQ의 "$60-$150/month" 범위 안에 정확히 들어옴 확인).

**배포 이슈 발견 및 해결**: 이번 커밋(4개 신규 파일, 12개 파일 변경) push 후 GitHub Pages `/pages/builds/latest` API가 **약 4분 이상 이전 커밋 해시를 계속 반환**하며 새 빌드를 안 잡는 것처럼 보였음(웹훅 지연으로 추정 — 원격 저장소 자체는 `git ls-remote`로 정상 push 확인됨). **`git commit --allow-empty` + push로 빈 커밋을 만들어 재트리거하니 즉시(45초 내) 새 커밋 기준으로 정상 빌드됨.** 다음 세션에서 push 후 builds API가 몇 분째 이전 커밋에 머물러 있으면, 에러 상태가 아닌 이상 걱정하지 말고 이 방법(빈 커밋 재트리거)을 먼저 시도할 것 — 원격에 실제로 반영이 안 된 건 아니었음.

**다음 세션에서 반드시 확인할 것**:
- 이번 세션에 만든 6개 신규 페이지(훈련 계산기 2개+동반블로그, 생식계산기, 보딩계산기, 저체중 포스트 2개) 전부 GSC에 잡히는지 다음 데이터에서 확인.
- **페이지 수 확장은 이번 세션에 시작했을 뿐 — 다음 세션에도 "경쟁자 있어도 우리 강점(비용) 붙여서 진행" 기준으로 계속 신규 페이지를 늘려나갈 것.** 고양이 쪽 롱테일도 이 새 기준으로 다시 봐야 함(이전엔 무경쟁 기준으로 전부 기각했었음).
- 사이트 총 페이지 수 추이를 다음 세션 시작할 때 카운트해서 handover에 기록하는 걸 습관화할 것 (오늘 기준: tools 26 + posts 36 + checklists 3 = 65페이지, index 포함).

---

### 세션 O (계속) — 롱테일 재검증 후 타이터 검사 계산기 추가 (7/22)

사용자가 방금 만든 raw-feeding/pet-boarding 계산기에 대해 "경쟁 높은데 너무 막 진행한 거 아니냐, 롱테일로 경쟁도를 최대한 줄여야 한다"고 지적. 자체 평가 결과 인정: pet-boarding-cost-calculator는 롱테일화 없이 넓은 헤드키워드("pet boarding cost calculator")를 그대로 만든 것에 가까웠음. raw-feeding-calculator는 비용 추정을 붙여 어느 정도 차별화했지만 타이틀/타겟은 여전히 넓은 편.

**교훈 보강**: "경쟁자 있어도 우리 강점 붙이면 진행"이라는 세션 O 전반부의 기준은 유지하되, **가능하면 먼저 롱테일로 좁혀서 경쟁도 자체를 낮추는 시도를 먼저 하고, 그래도 넓은 헤드키워드로 갈 수밖에 없다면 그때 우리 강점(비용)으로 차별화하는 게 순서**라는 걸 명확히 함. "페이지 수 늘리기"가 "아무거나 만들기"는 아니라는 사용자의 명확한 정정.

**추가 조사 (총 8개, 전부 좁혀서 바로 검색)**: 강아지 ACL/CCL(TPLO) 수술비용(9곳+, 기각), 반려동물 화장 비용(계산기 4곳, 기각), 강아지 인지기능장애 체크리스트(Dr. Buzby's가 이미 CADES/DISHA 정식 체크리스트 보유 + 진단형 콘텐츠라 정책상 리스크, 기각), 강아지산책서비스비용(8곳, 기각), 마이크로칩비용(7곳 + vetcostcalc.com 검색결과에 AI콘텐츠생성 프롬프트가 그대로 노출됨 — 경쟁사가 AI 대량생산 중이라는 물증, 기각), 관절보조제 용량계산기(경쟁있음+용량가이드는 정책상 안 만드는 게 맞음, 기각).

**유일하게 뚫린 것 — 신규 파일**: `tools/titer-test-vs-revaccination-calculator.html`
- 근거: "titer test cost" 관련 아티클(Dogs Naturally, Kinship, AdoptAPet, AVMA, Texans for Vaccine Choice 등)은 많지만 **비교 계산기는 0곳** — 순수 신규 포맷 갭.
- 종/비교연수/타이터검사주기/마리수 입력 → 표준 재접종 비용 vs 타이터검사 비용(양성유지시/부스터 1회 필요시) 비교.
- **중요 설계 결정**: 광견병(rabies)은 계산 대상에서 명시적으로 제외 — 미국 대부분 주에서 타이터 결과와 무관하게 법적 의무이기 때문에, 이를 포함하면 "타이터로 광견병 접종을 건너뛸 수 있다"는 위험한 오해를 줄 수 있어 FAQ로 명확히 경고함.
- WSAVA/AAHA/AAFP/AVMA 입장 비교표로 수의학계 의견이 갈린다는 걸 균형있게 전달 — "타이터가 항상 저렴하다"고 단정하지 않음. 실제로 계산 결과 자체가 이를 뒷받침(같은 주기로 비교하면 검사비($60)가 접종비($30)보다 비싸서 재접종이 더 저렴하게 나오는 경우가 많음 — node로 실행 검증 완료, 콘텐츠 메시지와 계산 결과가 일치).
- 기존 `dog/cat-vaccination-schedule-calculator`와 양방향 링크.

**QA**: 전체 68개 파일 YAML 통과, JSON-LD 오류 0, FAQ 매칭(5/5), permalink 중복없음(30개), tool-card 개수 일치(27=27=27), 링크 재스캔 0건. 커밋 → push → GitHub Pages 빌드 즉시(40초 내) 정상 확인(이번엔 웹훅 지연 없었음).

**다음 세션에서 확인할 것**:
- 오늘 만든 7개 신규 페이지(훈련계산기2+동반블로그, 생식계산기, 보딩계산기, 저체중포스트2, 타이터계산기) 전부 GSC 노출 확인.
- 신규 콘텐츠 판단 순서를 다음처럼 정리해서 유지할 것: **① 먼저 롱테일로 최대한 좁혀서 경쟁도 자체를 낮출 방법부터 찾기 → ② 그래도 넓은 헤드키워드로 갈 수밖에 없으면 우리 강점(비용계산)으로 차별화 → ③ 그마저 안 되면 그때 기각.** 오늘 세션 초반(펫보딩)엔 ②를 ①보다 먼저 써서 사용자에게 지적받았음.
- 오늘 기준 사이트 전체 페이지 수: tools 27 + posts 36 + checklists 3 = 66페이지.

**추가 수정**: 타이터 계산기를 툴만 만들고 동반 블로그를 안 붙인 걸 사용자가 바로 지적("클러스터 추가인데 툴만 한 거야?"). `_posts/2026-07-22-titer-testing-for-dogs-and-cats.md` 추가로 페어링 완성 — 툴 페이지는 비용비교, 블로그는 작동원리/결과해석(양성·음성·경계)/non-responder 개(항체가 아예 안 생기는 유전적 패턴, 계속 재접종해도 매번 음성 나오는 문제)/광견병 등 비적용 대상 등 완전히 다른 각도로 내용을 채워 중복 없이 깊이를 더함. QA(69개 파일 YAML, JSON-LD 0오류, slug 중복없음 37개, 링크 0건) 통과 후 커밋·push·빌드 확인. **교훈: 신규 클러스터/신규 콘텐츠 만들 때는 툴만 만들고 끝내지 말고 항상 동반 블로그 페어링까지 세트로 완료했는지 스스로 체크리스트로 확인할 것.**

**최종 정정**: 위 "추가 수정"에서 붙인 동반 블로그를 재검증 결과 철회함. "결정 프레임워크"로 포맷을 바꿔 재작성했지만, 다시 확인해보니 이 시나리오 구성 자체가 AAHA/WSAVA 공식 "타이터검사 적용 상황" 리스트(입양견 이력불명/번식견/시니어/백신반응이력)를 재구성한 것에 가까웠고, 이 공식 리스트는 KSVDL, AdoptAPet, Kinship, PetMD, AVMA, Paws & Claws 등 최소 8곳에서 이미 재인용되고 있음을 확인. 계산기(실제 비교수치를 뽑아주는 유일한 툴)라는 차별점은 여전히 유효하지만, 별도 블로그로 동일 시나리오를 재설명하는 건 부가가치가 낮다고 최종 판단해 `_posts/2026-07-22-titer-testing-for-dogs-and-cats.md` 삭제, 계산기 페이지의 블로그 링크·llms.txt 항목 제거. 계산기는 자체 FAQ 5개 + WSAVA/AAHA/AAFP/AVMA 비교표로 단독 유지(오늘 만든 raw-feeding-calculator, pet-boarding-cost-calculator와 동일하게 동반 블로그 없이 단독).

**최종 교훈**: "계산기가 무경쟁이니 동반 블로그도 무경쟁일 것"이라는 가정은 틀렸다 — **툴(계산기/인터랙티브 기능)의 경쟁도와 그 주제에 대한 편집 콘텐츠(설명글)의 경쟁도는 완전히 별개로 확인해야 한다.** 같은 주제라도 포맷이 다르면(계산기 vs 설명글) 경쟁 구도가 딴판일 수 있음 — 이번처럼 계산기는 비어있어도 그 주제의 "설명 콘텐츠"는 이미 대형 수의학 매체·협회가 공식 문서로 꽉 채워놓은 경우가 있음. **모든 신규 클러스터가 반드시 "계산기+블로그" 페어링이어야 하는 건 아니다** — 툴 자체 페이지 콘텐츠(FAQ+비교표)로 충분한 깊이가 나오면 블로그 없이 단독으로 두는 것도 정상적인 선택지. 다음부터는 동반 블로그를 만들지 여부를 "관행이니까 무조건"이 아니라, 그 블로그 각도의 경쟁도를 별도로 확인한 후 결정할 것.

**오늘(세션 O) 최종 페이지 수**: tools 27 + posts 36 + checklists 3 = 66페이지. 신규 순증: 훈련계산기2(강아지 배변훈련, 고양이 리터훈련) + 동반블로그1(퇴행) + 저체중포스트2(개/고양이) + 생식계산기1 + 펫보딩계산기1 + 타이터계산기1 = 총 8개 신규 페이지 확정 게시(타이터 동반블로그는 철회로 최종 미게시).
