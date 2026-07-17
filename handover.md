# PetPawCalc 인수인계 문서

최종 갱신: 2026-07-17 (세션 M)
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
- `_layouts/checklist.html` — tool.html과 동일한 head/meta/analytics 구조 유지, `{{ content }}` 뒤에 **공용 JS**(체크박스 상태를 `localStorage`에 저장/복원, 진행률바 업데이트, reset, print) 추가. 이 JS는 `.checklist-page[data-checklist-id]`와 `.checklist-check[data-check-id]`만 있으면 어떤 체크리스트 페이지에서도 동일하게 작동 — **개별 체크리스트 파일엔 JS를 전혀 안 넣어도 됨**(재사용성을 위해 의도적으로 레이아웃에 공용 로직을 둠, tool 파일들이 매번 JS를 반복 작성하던 것과 다른 패턴).
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

**QA**: YAML 전수 검증(체크리스트 4개 파일 전부 통과), `_config.yml` YAML 유효성, JSON-LD(ItemList+FAQPage) 3개 파일 전부 유효성 검증 통과, div/label/span 태그 개수 매칭(3개 체크리스트 전부 일치), Liquid 태그(`{% %}`, `{{ }}`) 균형 확인(header.html, checklist.html), **FAQ 스키마-본문 1:1 매칭(3/3, 3/3, 3/3 전부 일치)**, **ItemList 스키마 항목수 vs 실제 체크박스 개수 매칭(24/24, 23/23, 21/21)**, 화면에 표시되는 "0 of N done" 초기 텍스트가 실제 체크박스 개수와 일치하는지 확인, 전체 저장소 링크 재스캔(체크리스트 포함, 브로큰 링크 0건).

**다음 세션에서 확인할 것**:
- Checklists 섹션의 첫 GSC 노출/색인 여부 — 완전히 새로운 URL 네임스페이스(`/checklists/`)라 색인 속도 자체가 관찰 포인트.
- **Compare(비교) 허브를 다음 세션 우선순위로 진행** — 품종 성향 비교 아니라 비용/실용 축으로 스코프 좁혀서(품종별 연간비용, 보험 비교, 사료 급여방식 비교) 착수. 기존 계산기 데이터 재활용 가능한 것부터.
- 체크리스트 3개 다음으로 후보군: 이사(반려동물과 이사), 여행, 시니어 반려동물, 응급상자 준비 체크리스트 등 — 사용자가 "폭넓게 생각해도 된다"고 했으니 종 확장(기니피그·잉꼬 등)도 계속 후보로 열어둘 것, 다만 매번 웹 검색으로 경쟁강도 확인 먼저.
- localStorage 기반 진행률 저장은 브라우저/기기별로 분리 저장됨(동기화 안 됨) — 사용자가 여러 기기에서 확인하고 싶어할 경우 계정 시스템 없이는 한계가 있음을 인지해둘 것(별도 요청 없으면 현재 방식 유지).
- **CSS 스코프 교훈(위 버그 수정 항목 참고)을 앞으로도 계속 지킬 것** — 새 레이아웃이나 새 컴포넌트를 만들 때 여러 페이지 타입에서 재사용될 가능성이 있다면 처음부터 `css/style.css`에 스코프 없이 넣을 것, 특정 레이아웃 파일 안에 스코프해서 나중에 재사용성 문제가 반복되지 않도록.
