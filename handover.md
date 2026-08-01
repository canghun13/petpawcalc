# PetPawCalc 인수인계 문서

최종 갱신: 2026-08-01 (세션 Z)
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
- **빌드 확인은 legacy Pages Builds API(`/repos/canghun13/petpawcalc/pages/builds/latest`)가 아니라 Actions API(`/repos/canghun13/petpawcalc/actions/runs`)로 할 것.** 이 저장소는 GitHub Actions 기반으로 Pages를 배포하는데, legacy Builds API는 이 배포 방식을 제대로 추적하지 못해 최신 커밋이 아니라 예전 커밋을 계속 보여주는 경우가 있었다(세션 T 직후 실제로 겪음 — 몇 분을 기다려도 legacy API가 새 커밋을 안 잡아서 헤맸는데, Actions API로 확인하니 이미 배포가 성공해 있었음).
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
  - **모든 `<script>` 블록을 인덱스 상관없이 전부 `node --check`할 것 — `scripts[0]`만 검사하지 마라.** (세션 T 직후 실제 사고: 페이지에 `<script>` 태그가 2개였는데 첫 번째 작은 프린트 함수만 검사하고 "문법 오류 없음"이라 잘못 보고했고, 실제 버그는 두 번째 메인 로직 블록에 있어서 계산기 전체가 죽었던 적이 있음.)
  - **JS 문자열에는 축약형 아포스트로피(aren't, isn't, don't 등)를 쓰지 말 것 — 항상 풀어써라("are not" 등).** 부득이하게 넣어야 한다면 그 문자열이 큰따옴표(")로 감싸져 있는지 반드시 확인(작은따옴표 문자열 안의 아포스트로피는 이스케이프가 꼬이기 쉬움 — 세션 T 직후 실제 사고: 이스케이프가 겹쳐써져서(`\\\\'`) 문자열이 중간에 끊기고 전체 스크립트 블록이 파싱 실패한 적이 있음).
  - **새로 추가하는 고정 안내/경고 박스는 `no-print` 클래스 여부를 반드시 확인할 것.** `.tool-box` 앞에 위치한, 인라인 `background` 스타일이 있는 박스인데 `no-print`가 빠지면 인쇄 시 결과 박스가 다음 페이지로 밀려나 첫 페이지가 빈 페이지가 됨(세션 T 직후 실제 사고 — `pet-travel-timeline-planner.html`의 상단 경고박스).
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

---

### 세션 P — GSC/GA 7/27 데이터 분석 + 고양이 리터훈련 퇴행 포스트 + 신규 카테고리 "펫 비상 대비 키트 체크리스트" (7/27, 주간 작업)

사용자 요청 핵심: 밀린 주간 작업. 첨부된 Coverage/Performance(GSC) zip + Analytics(GA) CSV 확인 후 신규/보강 판단. 신규 콘텐츠는 기존 파일 중복 체크 + 웹 검색 경쟁강도 확인 + 롱테일 전략. 신규·보강 둘 다 AI검색 대응(문제해결·비교분석 콘텐츠) 반영. AdSense 수익화 관점 우선순위. 대시보드 없이 텍스트 분석만. 작업 후 handover.md 갱신 후 push. 화면 깨짐 확인이 꼭 필요한 페이지만 링크로 제공.

**1. GSC 데이터 분석 (Coverage + Performance, 지난 3개월 누적 / GA는 6/29~7/26)**

- **Coverage 미색인 수치가 세션 J(7/15)부터 지금까지 사실상 계속 21개(발견됨-미색인 15 + 크롤링됨-미색인 6)로 정체** — 세션 J→L→M→N→이번까지 사실상 5개 데이터 포인트 연속 21개. 세션 N에서 이미 "정체로 판단, 재크롤 요청 권유 시점"이라고 결론 냈던 것이 이번에도 그대로 유지됨. **사용자에게 GSC UI에서 개별 URL "색인 생성 요청"을 직접 눌러볼 것을 다시 한번 명확히 권한다** — 에이전트는 GSC API 접근 권한이 없어 대신 요청 불가.
- **하지만 완전히 정체된 것만은 아님 — `dog-pregnancy-calculator`가 드디어 색인되어 처음으로 노출 데이터에 등장 (63노출, 평균순위 54.71).** 세션 J(7/15)부터 5세션 이상 미색인 상태였던 페이지가 세션 M에서 추가한 "임신 진단방법 비교표"+FAQ 보강 이후 결국 색인된 것으로 보임 — 온페이지 보강이 시간차를 두고 효과를 낸 사례로 볼 수 있어, "재크롤 요청 필요"와 "보강이 결국 통했다"는 두 신호가 동시에 존재하는 상황.
- **비대칭 발견 — `cat-pregnancy-calculator`는 dog 버전과 완전히 동일한 보강(비교표+FAQ)을 세션 M에서 동시에 받았는데도 여전히 노출 0.** 두 페이지가 받은 온페이지 처리가 동일한데 결과가 갈렸다는 건 순수 크롤/색인 우선순위 문제일 가능성이 높음 — 다음 세션에서 재크롤 요청 시 `cat-pregnancy-calculator`를 최우선으로 삼을 것.
- **Performance 페이지별 노출 대조로 미노출 URL 재역산(방법은 세션 J/N과 동일)**: 사이트 전체 74개 URL 중 41개가 노출 있음(35→41로 증가), 미노출 32개. 이 중 상당수는 세션 O(7/22)에 만든 지 5일밖에 안 된 신규 페이지라 당연히 미노출(훈련계산기2, 생식계산기, 펫보딩계산기, 타이터계산기, 저체중포스트2, 퇴행포스트, 체크리스트2개) — 제외하고 보면:
  - 세션 J 때부터 미색인이던 tool 7개 중 `annual-pet-cost-calculator`, `cat-pregnancy-calculator`, `cat-vet-visit-scheduler`, `pet-grooming-cost-calculator`, `spay-neuter-cost-calculator`, `cat-quality-of-life-calculator` 6개는 여전히 노출 0(12일 이상 정체). `dog-heat-cycle-calculator`는 이번에 노출 8건으로 확인되어 이미 회복됨.
  - blog 쪽 미노출은 여전히 세션 B 날짜조작 수정(7/10) 이전 작성 포스트 위주(`dog-age-human-years`, `how-long-are-cats-pregnant`, `signs-of-cat-labor` 등)로 기존 가설과 일치. `how-to-reduce-vet-costs-for-cats`(7/15 작성, 12일차)도 아직 미노출 — 살짝 오래 걸리는 편이라 다음 세션에서 계속 관찰.
- **정확 문구 점검**: GSC 쿼리 397개 전수 확인 결과, "paw score calculator"(22노출), "cat dental cleaning cost"(25노출+"cat teeth cleaning cost" 12노출), "dog heat cycle calculator"(8노출), "how to tell if your kitten is overweight"(8노출) 등은 이미 페이지 본문에 정확 문구가 존재함을 확인(추가 조치 불필요) — 다만 **"how big will my cat get calculator"(5노출, 94.8위)는 사이트 어디에도 없던 문구**라 `kitten-weight-chart-by-breed-size` 포스트에 신규 FAQ로 추가함(front matter+본문 양쪽, 세션 C 패턴).
- 쿼리 테이블 자체의 클릭 합계(1건, "maine coon weight predictor")가 페이지 테이블의 클릭 합계(4건)보다 적음 — GSC가 저노출 쿼리를 개인정보 보호 목적으로 일부 익명화/생략하는 것으로 추정, 특이사항 아님.
- **GA(6/29~7/26)**: 활성 사용자 74명. 유입은 여전히 (direct) 59명 압도적, pitchwall.co/Findly.tools 등 런칭 디렉토리 위주, organic은 bing 3·google 2·yahoo 1. AI 검색엔진(ChatGPT/Perplexity 등)발 유입은 이번에도 소스/매체 목록에서 식별 안 됨 — 계속 관찰 필요.

**2. 신규 콘텐츠 후보 검토 (웹 검색으로 경쟁강도 확인)**

- **기각**: `how-much-to-feed-a-cat`(dog의 `how-much-to-feed-a-dog`과 페어링 빈자리이긴 하나, PetMD·APOP·thepetcalculator.com 등 강력한 기존 계산기/권위 콘텐츠 다수 + 이미 사이트에 `pet-food-calorie-calculator`가 동일 니즈를 계산기로 커버 중이라 중복 리스크, 게다가 dog 버전 자체도 현재 미노출 상태라 "검증된 포맷" 근거가 약함), `why-is-my-dog-always-hungry`(cat의 `why-is-my-cat-always-hungry` 페어링 빈자리, 그러나 JustFoodforDogs·GreatPetCare·IAMS·DogFoodAdvisor·Waggle 등 대형 브랜드가 이미 두껍게 장악), 고양이 리터박스 회피 일반 주제(`cat not using litter box` — Cats.com·Chewy·Petco·Litter-Robot·alleycat.org 등 대형 브랜드 다수, 세션 O에서 이미 기각된 것과 동일 결론 재확인), 강아지/고양이 물 섭취량 계산기(worldanimalfoundation·omnicalculator·ratedcalculator·Nom Nom·ctrlcalculator 등 9곳 이상의 기존 계산기 확인, furcalc 외에도 훨씬 포화됨).
- **채택 1 — 신규 포스트 `kitten-litter-training-regression`**: 세션 O의 `kitten-litter-training-timeline` 계산기(신규 카테고리)의 동반 블로그가 없었던 빈자리를 채움. 강아지 쪽은 이미 `puppy-potty-training-regression`으로 계산기+블로그 페어링이 완성돼 있었는데 고양이 쪽만 없었음(세션 O가 "고양이는 나중에" 라고 명시적으로 미룬 항목). 웹 검색으로 좁혀서 확인(일반 "리터박스 회피"가 아니라 "이미 훈련됐던 고양이가 갑자기 회귀"라는 좁은 앵글) — Cats.com 관련 글 1건, Kitten Lady·Integricare·tinyinherbox.com 등 소규모 블로그/전문가 사이트 위주로 대형 브랜드 독점이 아님을 확인 후 진행.
  - 개와 다른 점을 정확히 반영(웹 검색으로 사실 확인): 고양이는 배변훈련이 학습이 아니라 본능이라 회귀 시 "훈련 실패"가 아니라 "환경 변화 신호"로 프레이밍을 다르게 함. 중성화 수술 후 절개부위 보호 목적으로 신문지 조각/비클럼핑 리터로 임시 교체를 권장하는 관행(여러 동물병원 소스로 확인) 반영. 의학적 원인은 개의 UTI 프레임이 아니라 **고양이 특발성 방광염(FIC, Feline Idiopathic Cystitis)**이 실제로는 UTI보다 훨씬 흔한 원인이라는 걸 MSPCA·BluePearl·International Cat Care·Hill's 등 복수 수의학 소스로 확인해 정확히 반영 — 수컷 고양이의 요도폐쇄 응급 경고도 포함.
  - `kitten-litter-training-timeline.html` ↔ 신규 포스트 양방향 링크, `puppy-potty-training-regression.md`에도 종간 교차링크 추가(dog↔cat 페어링 관행 유지).
- **채택 2 — 신규 체크리스트 `checklists/pet-emergency-kit-checklist.html`**: 세션 M이 남긴 다음 체크리스트 후보 파이프라인("이사/여행/시니어/응급상자 준비") 중 하나를 웹 검색으로 검증 후 진행. Red Cross·ASPCA·CDC·Best Friends·Ready.gov·Pawlicy 등 정적 체크리스트/PDF는 매우 많지만 **체크박스 누르고 진행률 저장하는 인터랙티브 웹 도구는 검색 결과에 전혀 없음** — 세션 M의 New Puppy/Kitten/Rabbit Checklist와 정확히 동일한 패턴의 빈 니치. 개·고양이 공용(종 구분 없이 하나의 체크리스트, 필요한 항목만 종별 표기 — new-rabbit-checklist처럼 단독 페이지가 아니라 auto-pet-cost-calculator처럼 통합형)으로 제작. 문서/ID·식량+물+투약·용품/컴포트·계획+연습 4개 섹션, 20개 항목, FAQ 6개(공식 재난 대비 기관 가이드라인을 종합해 근거 확보 — 3~7일 분 권장량, 반려동물 동반 불가 대피소가 많다는 점, 안전 스티커, 중성화 수술과 무관하게 항상 정확 사실 위주로 서술).
  - 역링크(고아 페이지 방지): `annual-pet-cost-calculator.html`(신규 post-cta), `checklists/new-puppy-checklist.html`, `checklists/new-kitten-checklist.html`(각각 post-cta 추가) — 3곳에서 신규 체크리스트로 연결.
  - 공통 파일 동기화: `checklists/index.html`(카드 추가, New 배지를 신규 항목으로 이동), `_includes/footer.html`(Checklists 컬럼에 링크 추가), `llms.txt`(Checklists 섹션에 항목 추가).

**3. AI검색 대응(문제해결·비교분석) 반영**

- 신규 포스트(`kitten-litter-training-regression`)에 행동적/환경적 원인 vs 의학적 원인 **비교표**, 흔한 유발요인 6가지 **비교표**(원인/실제상황/해결법), 단계별 **리셋플랜**을 처음부터 포함 — 세션 M부터 이어지는 방향을 신규 제작 시점부터 반영.
- 기존 페이지 보강은 정확 문구 FAQ 1건 추가(`kitten-weight-chart-by-breed-size`의 "how big will my cat get?") 외에는 이번 세션엔 진행하지 않음 — GSC 쿼리 전수 확인 결과 대부분 이미 정확 문구가 커버돼 있었고, 신규 콘텐츠 제작에 리소스를 집중하는 게 이번 세션의 우선순위 판단이었음(아래 4번 참고).

**4. AdSense 수익화 관점 우선순위 판단**

- Coverage 정체(21개, 5데이터포인트 연속)와 `dog-pregnancy-calculator`가 결국 색인된 사례가 공존하는 상황 — 온페이지 보강은 계속 유효하지만, **지금 가장 확실한 다음 액션은 콘텐츠가 아니라 사용자가 GSC UI에서 개별 URL(특히 `cat-pregnancy-calculator`)에 색인 생성을 요청하는 것**이라고 명확히 판단.
- 신규 콘텐츠 2건(포스트 1 + 체크리스트 1)은 둘 다 "이미 검증된 사이트 자체 포맷(페어링 완성/체크리스트 인터랙티브 도구)의 빈자리를 채우는" 저위험 확장이라 우선순위를 높게 잡음 — 완전히 새로운 카테고리 개척보다 리스크가 낮음.
- 트래픽/클릭이 여전히 극소수인 단계라 화려한 신규 시도보다 "사이트가 이미 증명한 패턴의 빈자리 채우기"를 이번 세션의 핵심 원칙으로 유지.

**5. QA**
- 전체 `_posts`(37개)+`tools`+`checklists`(31개) front matter YAML 전수 통과.
- 신규 체크리스트 JSON-LD(ItemList 20개 항목=실제 체크박스 20개, FAQPage 6개=본문 h3 6개) 1:1 매칭 코드로 확인, div(13/13)·label(20/20) 개수 매칭.
- 신규 포스트 FAQ front matter-본문 1:1 매칭(6/6), 마크다운 테이블에 `table-wrapper` div를 쓰지 않음(세션 O의 kramdown 교훈 준수 확인).
- `kitten-weight-chart-by-breed-size` FAQ 추가 후 YAML 재검증(8개 FAQ 정상 파싱, front matter 종결자 `---` 보존 확인 — 세션 N의 실수 재발 방지 체크리스트 항목 적용).
- 전체 저장소 링크 재스캔(신규 파일 포함) — 브로큰 링크 0건(정규식 오탐 1건은 `llms.txt`의 일반 문장 내 `/checklists/.`로 확인, 실제 문제 아님).
- slug 중복 없음(37개), permalink 중복 없음(31개).
- `index.html`/`tools/index.html` tool-card 27개 = 실제 tool 파일 27개 일치(이번 세션 신규 tool 없음). `checklists/index.html` 카드 4개 = 실제 checklist 파일 4개 일치.

**오늘(세션 P) 최종 페이지 수**: tools 27 + posts 37 + checklists 4 = 68페이지. 신규 순증 2개(고양이 리터훈련 퇴행 포스트, 펫 비상 대비 키트 체크리스트).

**다음 세션에서 확인할 것**:
- **Coverage 21개 정체가 6번째 데이터에서도 유지되면 재크롤 요청을 더 강하게 재권유할 것 — 특히 `cat-pregnancy-calculator`(dog 버전과 동일 보강인데 결과가 갈린 비대칭 사례) 최우선.**
- 신규 2개 페이지(`kitten-litter-training-regression`, `pet-emergency-kit-checklist`)의 첫 GSC 노출/색인 확인.
- `kitten-weight-chart-by-breed-size`에 추가한 "how big will my cat get" FAQ가 다음 데이터에서 관련 쿼리 노출/순위에 변화를 주는지 확인.
- `dog-pregnancy-calculator`가 색인된 것처럼, 세션 J 때부터 미노출이던 나머지 tool 6개(`annual-pet-cost-calculator`, `cat-pregnancy-calculator`, `cat-vet-visit-scheduler`, `pet-grooming-cost-calculator`, `spay-neuter-cost-calculator`, `cat-quality-of-life-calculator`)도 시간차를 두고 자연 회복되는지 계속 관찰(재크롤 요청과 별개로).
- GA 데이터에서 AI 검색엔진(ChatGPT/Perplexity 등)발 유입이 referral로 잡히는지 계속 확인 — 이번에도 식별 안 됨.
- `what-to-feed-pregnant-dog` 자기잠식 의심은 이번 세션엔 다루지 않음 — 여전히 열린 항목(세션 H부터 6세션째 미확정), 사용자가 GSC UI 교차확인을 해줄 수 없다면 다음엔 공식 종결 처리 고려.

---

### 세션 Q — 신규 클러스터 발굴(별도 대화에서 기획) 후 실행: 회복 캘린더 + 보험 대기기간 트래커 (7/27, 세션 P 직후)

**배경**: 사용자가 세션 P 직후 별도 채팅에서 "기획만 담당하고 코드/커밋/푸시는 하지 마라"는 조건으로 신규 클러스터 후보를 대량 발굴하도록 요청. 그 채팅에서 12개 신규 아이디어(S급 4개, A급 4개, B급 4개)를 웹 검색 경쟁조사 완료 후 실행 프롬프트 형태로 정리해 전달함. 이번 세션은 그 중 **배치 1(S급 2개)**을 사용자가 그대로 복사해 지시한 것을 실행.

**1. 신규 도구 2개 제작**

- **`tools/spay-neuter-recovery-timeline.html`**: 수술 날짜+종+성별+나이대 입력 → 실제 날짜가 박힌 회복 캘린더(절개부위 확인 기간/콘 제거 예상일/활동제한 해제 예상일, 고양이 수컷은 리터 교체 기간 별도). 4개 프로필(개 중성화/개 스페이/고양이 중성화/고양이 스페이)로 구분, 스페이가 중성화보다 더 긴 회복기간(활동제한 14-21일 vs 10-14일)을 반영 — Concordia Pet Care 등 복수 소스로 확인. 고양이 중성화는 절개부위가 봉합사 없이 노출돼 있어 리터 더스트 자극 위험 때문에 신문지/비클럼핑 리터를 5-14일 권장(SNAP, Toby Project, LifeLine Animal Project 등 다수 동물병원/구조단체 출처로 확인, 출처마다 4일~14일로 편차가 있어 범위로 제시).
  - **필수 콘텐츠**: "정상 vs 즉시 병원 연락" 비교표, "콘을 일찍 벗기면 안 되는 이유"(7일차에 겉만 아물어도 재개방 위험) 문제해결 섹션, 콘 vs 리커버리슈트 비교표.
  - **안전**: 투약/용량 정보는 전혀 다루지 않음 — 일정과 관찰 포인트만.
  - 오늘 날짜(현재 진행 단계)를 하이라이트하는 타임라인 카드 UI를 `dog-pregnancy-calculator`의 주차별 타임라인 패턴에서 재사용.
- **`tools/pet-insurance-waiting-period-tracker.html`**: 보험 효력 시작일+사고/질병/정형외과 대기기간(드롭다운 선택) 입력 → 각 보장 시작 실제 날짜 산출. 특정 보험사 추천/순위 없이 업계 일반 범위(사고 0-15일, 질병 14-30일, 정형외과 6-12개월 또는 30일 또는 질병과 통합)만 중립적으로 제시.
  - **필수 콘텐츠**: 대기기간 유형별 비교표, "대기기간 중 증상이 나타나면 기존질환으로 영구 제외될 수 있다"는 핵심 함정을 문제해결 섹션으로 명확히 서술, 보험사 갈아타면 대기기간이 리셋된다는 점 별도 섹션으로 명시.
- **node로 두 계산기의 날짜 산출 로직을 직접 실행해 검증**: `spay-neuter-recovery-timeline`은 4개 프로필 전부(개 중성화/스페이, 고양이 중성화/스페이) 콘 제거일·활동제한 해제일·리터교체 종료일이 FAQ/본문에 쓴 일수(10-14일, 14-21일, 5-14일 등)와 정확히 일치하는 실제 날짜로 계산됨을 확인. `pet-insurance-waiting-period-tracker`는 3개 시나리오(사고0/질병14/정형외과=질병과동일, 사고15/질병30/정형외과180일, 사고2/질병21/정형외과365일)로 날짜 산출 검증, 웰니스는 항상 효력일과 동일(즉시 보장) 확인.

**2. 역링크(양방향, 고아 페이지 방지)**

- `spay-neuter-recovery-timeline` ↔ `spay-neuter-cost-calculator`(양방향), ↔ `spay-neuter-cost-and-timing` 블로그 포스트(Related Articles에 추가), `new-puppy-checklist`/`new-kitten-checklist`에서 신규 링크 추가.
- `pet-insurance-waiting-period-tracker` ↔ `pet-insurance-cost-estimator`(양방향, 기존 대기기간 언급 문단 바로 아래에 삽입), ↔ `annual-pet-cost-calculator`(양방향).
- `annual-pet-cost-calculator`에는 두 신규 도구 모두 링크 추가(비용 계산기 허브 성격이라 신규 확장 시 항상 여기부터 연결하는 관행 유지).

**3. 공통 파일 4종 동기화**: `index.html`(카드 2개 추가), `tools/index.html`(검색용 data-title/desc/tags 속성 포함 카드 2개 추가), `_includes/footer.html`(Tools 컬럼에 2개 추가, 큐레이션 목록이지만 spay-neuter/insurance 계열은 이미 있어 동일 계열로 추가), `llms.txt`(Tools 섹션에 2개 항목 추가). New 배지를 `titer-test-vs-revaccination-calculator`에서 신규 2개로 이동.

**4. QA**
- 전체 `_posts`(37개)+`tools`+`checklists`(35개, index 2개 포함) front matter YAML 전수 통과.
- JSON-LD 스키마(WebApplication+FAQPage) 신규 2개 파일 유효성 검증 통과, FAQ 스키마-본문 h3 1:1 매칭(5/5, 5/5).
- div 개수 매칭: 신규 2개(23/23, 19/19) + 역링크 추가로 수정된 기존 5개 파일(spay-neuter-cost-calculator, pet-insurance-cost-estimator, annual-pet-cost-calculator, new-puppy-checklist, new-kitten-checklist) 전부 짝 맞음.
- table/tr/thead/tbody 태그 매칭(신규 2개 전부).
- **JS 계산 로직을 node로 직접 실행해 검증**(세션 O에서 도입한 표준 QA 단계) — 4개 회복 프로필 + 3개 보험 시나리오 전부 본문에 명시한 수치와 실제 계산된 날짜가 정확히 일치함을 확인. `node --check`로 두 파일의 임베디드 JS 문법 오류 없음도 별도 확인.
- 전체 저장소 링크 재스캔(신규 파일 포함) — 브로큰 링크 0건.
- slug 중복 없음(37개), permalink 중복 없음(33개, index 제외).
- `index.html`/`tools/index.html` tool-card 개수(29) = 실제 tool 파일 개수(29) 일치. `checklists/index.html` 카드 개수(4) = 실제 checklist 파일 개수(4) 일치.

**오늘(세션 Q) 최종 페이지 수**: tools 29 + posts 37 + checklists 4 = 70페이지. 신규 순증 2개(`spay-neuter-recovery-timeline`, `pet-insurance-waiting-period-tracker`).

**다음 세션에서 확인할 것**:
- 오늘 만든 신규 2개의 GSC 노출/색인 여부 확인(최소 1-2주 필요).
- **별도 채팅에서 발굴한 12개 후보 중 배치 1(S급 2개, 오늘 완료)을 제외한 나머지 — 배치 2(품종별 중성화 시기 비교 도구, 강아지 사회화 창 트래커), 배치 3(기니피그 체크리스트, 고양이 합사 타임라인), 배치 4(해외 이동 타임라인, 구충 스케줄) — 를 다음 세션들에서 순서대로 진행할 것.** 배치 2·4는 건강/규제 정보라 추론 강도를 높게 유지하고 표현 수위(연구 인용 vs 권고 단정 구분, 국가별 단정 금지)에 특히 주의할 것 — 실행 프롬프트에 이미 구체적으로 명시돼 있음.
- Coverage 21개 미색인 정체는 이번 세션엔 다루지 않음(별도 채팅에서 이미 세션 P가 분석) — 여전히 `cat-pregnancy-calculator` 등 개별 URL 재크롤 요청이 사용자 액션으로 남아있는 상태.

---

### 세션 R — 배치 2 실행: 품종별 중성화 시기 비교 도구 + 강아지 사회화 체크리스트 (7/27, 세션 Q 직후)

**배경**: 별도 채팅에서 발굴한 12개 후보 중 배치 2(건강/규제 정보, 추론 강도 높게 유지 지시)를 사용자가 그대로 지시. 표현 수위(연구 인용 vs 권고 단정 구분)를 특히 신경써서 진행.

**1. 사전 리서치 (웹서치로 원문/AKC 요약 검증)**

- UC Davis Hart et al. 연구 계열 전체를 웹서치로 재확인: 2020년 35개 품종 연구(Frontiers in Veterinary Science), 별도의 믹스견 5개 체급 연구, 2024년 5개 대형견종 추가 연구(German Shorthaired/Wirehaired Pointer, Mastiff, Newfoundland, Rhodesian Ridgeback, Siberian Husky). 각 품종별 정확한 수치(예: Golden Retriever 암컷 — 어느 나이에 중성화해도 암 위험 2-4배 증가/Labrador 수컷 관절질환 22% vs 8%, 암컷 33% vs 10%/German Shepherd 수컷 33% vs 2%, 암컷 29% vs 9%+요실금 7% vs 0%/Boston Terrier 수컷만 암 위험 증가, 암컷은 표준 6개월 중성화도 위험 증가 없음/Shih Tzu는 반대로 암컷만 암 위험/Great Dane·Irish Wolfhound는 어느 나이든 관절질환 위험 증가 없음/Doberman 수컷은 관절질환 유의차 없음, 암 발생 경향(비유의)/Shetland Sheepdog 암컷은 오히려 24개월 이후로 늦추면 요실금 위험 증가라는 반대 방향 소견)를 원문·2차 요약 교차 확인 후 반영.
- AVSAB(American Veterinary Society of Animal Behavior)의 강아지 사회화 공식 입장문 확인: "완전 백신 접종 전에 사회화를 시작하는 것이 표준진료여야 한다"는 명시적 입장, 7-8주부터 시작 가능(1차 접종 7일 경과 + 첫 구충 전제), 3세 미만 개의 사망원인 1위가 감염병이 아니라 행동문제라는 근거, 단 개공원/펫샵 등 고위험 장소는 피하고 통제된 환경 위주로 진행해야 한다는 안전조건까지 정확히 확인.

**2. 신규 도구 A — `tools/neuter-timing-by-breed-size.html`**

- 입력: 체급(믹스견/미등재품종용 5단계: 소형<10kg/중형10-19kg/표준20-29kg/대형30-39kg/초대형40kg+) 또는 개별 연구된 품종 16개(Golden Retriever, Labrador Retriever, German Shepherd Dog, Doberman Pinscher, Boston Terrier, Shih Tzu, Great Dane, Irish Wolfhound, Maltese, Chihuahua, Shetland Sheepdog, German Shorthaired/Wirehaired Pointer, Mastiff, Newfoundland, Rhodesian Ridgeback, Siberian Husky) — 총 21개 그룹 × 성별.
- **프레이밍 원칙을 코드/문구 양쪽에 강제 적용**: 모든 결과 문구를 "the study found/reported"로 시작(우리 권고 아님), 결과창 하단에 고정 경고박스("이건 연구 요약이지 PetPawCalc의 권고가 아니다, 수의사와 최종 결정할 것") 항상 노출 — JS 조건부 표시가 아니라 결과 렌더링 시 항상 포함되도록 구현.
- **선택적 인용 금지 원칙 반영**: 소형견 대부분 무위험 + Great Dane·Irish Wolfhound(초대형인데도 무위험, 예외) + Boston Terrier·Shih Tzu(소형인데 성별 특이적 암 위험, 반대 예외) + Golden Retriever 암컷(모든 연령에서 위험 지속, 가장 강한 반례) + Shetland Sheepdog 암컷(늦게 중성화가 오히려 위험 증가, 방향이 반대인 소견) 등 상반되는 방향의 소견을 전부 포함해 균형 확보.
- **개체군 관리 근거 존중**: "전통적 6개월 권고 vs 연구 기반 관점" 비교표 뒤에 별도 문단으로 "두 관점 다 틀린 게 아니다 — 보호소/구조단체는 재입양 후 재방문을 보장할 수 없어 조기중성화가 여전히 합리적 근거를 가진다"는 문장을 명시적으로 포함(과잉번식 방지 근거를 깎아내리지 말라는 지시 반영).
- 비교표 2개: 체급별×성별 위험 프로파일(믹스견 연구 기준), 전통적 6개월 권고 vs 연구 기반 관점.
- FAQ 6개, 스키마+본문 1:1.
- QA: 21개 드롭다운 옵션 = NEUTER_DATA 객체 키 21개 100% 일치(양방향 diff 0건), 각 항목 label/male/female 필드 전부 존재(node로 검증), JSON-LD·div·table·tr·optgroup·select 태그 전부 짝 맞음.

**3. 신규 체크리스트 B — `checklists/puppy-socialization-checklist.html`**

- 항목 26개, 7개 카테고리(사람 유형4/소리4/표면·바닥4/이동수단3/핸들링4/다른 동물3/환경4), 각 항목에 "왜 필요한지" 한 줄 설명 포함.
- **추가 기능(생년월일 → 16주 창 카운트다운)을 개별 파일 JS가 아니라 `_layouts/checklist.html`(공용 레이아웃)에 범용 기능으로 추가**: `#checklist-age-input`(date, `data-window-days` 속성) + `#checklist-countdown-result` 요소가 있으면 자동으로 작동하는 제네릭 로직으로 구현 — 특정 체크리스트에 종속되지 않아 향후 다른 나이-구간 체크리스트에도 재사용 가능. 기존 체크리스트(new-puppy/new-kitten/new-rabbit/pet-emergency-kit)는 해당 요소가 없어 이 코드 블록이 조건부로 스킵됨 → 기존 페이지 영향 없음 확인.
- `css/style.css`에 `.checklist-countdown`/`.checklist-countdown-active`/`.checklist-countdown-closed` 스타일 추가.
- **핵심 차별화 섹션 "Do I Need to Wait Until Vaccines Are Complete?"**: AVSAB 입장을 정확히 인용(7-8주부터 가능, 1차 접종 7일 경과+구충 전제) + 안전조건(개공원/펫샵 등 고위험 장소 회피, 통제된 환경 우선)을 같은 문단 안에 반드시 함께 명시 — 위험 완화 조건 없이 "빨리 시작하라"는 메시지만 단독으로 나가지 않도록 프레이밍.
- FAQ 6개(백신 전 사회화 가능 여부/critical window 정의/16주 지나면 늦었는지/안전한 장소/스트레스 신호 구분법/퍼피클래스 백신요건).
- QA: ItemList 26개 = 실제 체크박스 26개 일치, FAQ 스키마-본문 6/6 매칭, div(21/21)·label(27/27, DOB input용 label 1개 포함해 정상) 균형, 카운트다운 날짜 로직 node로 검증(생후 56일 시점 16주 창 잔여일수 56일로 정확히 계산됨 등 3개 시나리오 확인).

**4. 역링크(양방향, 지시사항 그대로 이행)**

- `dog-vaccination-schedule-calculator` ↔ `puppy-socialization-checklist` (양방향).
- `new-puppy-checklist` → 체크리스트 B, `puppy-potty-training-calculator` → 체크리스트 B.
- `spay-neuter-cost-calculator` ↔ `neuter-timing-by-breed-size` (양방향), `spay-neuter-cost-and-timing` 블로그 포스트 Related Articles에도 추가.

**5. 공통 파일 동기화**: `index.html`(도구A 카드 추가, New배지 이동), `tools/index.html`(검색용 data속성 포함 카드 추가), `checklists/index.html`(체크리스트B 카드 추가, New배지 이동), `_includes/footer.html`(양쪽 컬럼에 항목 추가), `llms.txt`(Tools/Checklists 섹션 각각 항목 추가).

**6. QA(전수)**
- 전체 `_posts`(37개)+`tools`+`checklists`(74개 파일) front matter YAML 전수 통과.
- JSON-LD 오류 0건, FAQ 스키마-본문 1:1 매칭(6/6 도구A, 6/6 체크리스트B).
- slug 중복 없음(37개), permalink 중복 없음(35개, index 제외).
- 전체 링크 재스캔 — 브로큰 링크 0건.
- tool-card 개수: `index.html`/`tools/index.html` 30개 = 실제 tool 파일 30개 일치. `checklists/index.html` 카드 5개 = 실제 checklist 파일 5개 일치.
- div 균형: 역링크 추가로 수정한 기존 파일(dog-vaccination-schedule-calculator, new-puppy-checklist, puppy-potty-training-calculator, spay-neuter-cost-calculator, index.html, tools/index.html, checklists/index.html) 전부 짝 맞음. `_layouts/checklist.html`에서 div 개수 불일치가 감지됐으나 확인 결과 JS 주석 안의 예시 텍스트("Each checklist page provides: <div ...")가 정규식에 걸린 오탐임을 확인(실제 HTML 태그 아님, 실제 문제 없음).
- 신규 도구A 21개 드롭다운 옵션 = NEUTER_DATA 객체 21개 키 완전 일치(diff 0), 각 항목 label/male/female 필드 결측 0건.
- `node --check`로 신규 2개 파일 + 레이아웃 수정분의 임베디드 JS 문법 오류 없음 확인. 카운트다운 날짜 계산 로직 node 시뮬레이션으로 정확성 검증.

**오늘(세션 R) 최종 페이지 수**: tools 30 + posts 37 + checklists 5 = 72페이지. 신규 순증 2개(`neuter-timing-by-breed-size`, `puppy-socialization-checklist`).

**다음 세션에서 확인할 것**:
- 오늘 만든 신규 2개의 GSC 노출/색인 여부 확인(최소 1-2주 필요).
- **배치 3(기니피그 체크리스트, 고양이 합사 타임라인), 배치 4(해외 이동 타임라인, 구충 스케줄 — ⚠️ 둘 다 건강/규제 정보라 추론 강도 높게 유지할 것)를 다음 세션들에서 순서대로 진행할 것.**
- `_layouts/checklist.html`에 추가한 범용 카운트다운 기능은 이번 체크리스트 하나에만 쓰였음 — 다음에 나이-구간 기반 체크리스트(예: 배치3의 고양이 합사 타임라인은 체크리스트가 아니라 도구라 해당 없음)를 만들 때 동일 패턴(`data-window-days` 속성)으로 재사용 가능하다는 걸 기억할 것.
- 도구A(`neuter-timing-by-breed-size`)는 건강 정보 민감도가 높은 페이지라, 실제 배포 후 혹시 사용자나 방문자로부터 "권고처럼 읽힌다"는 피드백이 오면 프레이밍 문구를 추가로 완화할 준비할 것.

---

### 세션 S — 배치 3 실행: 기니피그 체크리스트 + 고양이 합사 타임라인 도구 (7/27, 세션 R 직후)

**배경**: 별도 채팅에서 발굴한 12개 후보 중 배치 3("기존 패턴 복제라 빠르게 끝난다"는 사용자 설명대로 진행)을 그대로 지시받음. `new-rabbit-checklist.html`을 구조 템플릿으로 삼고, 기니피그 고유 사실은 전부 웹서치로 검증 후 반영.

**1. 사전 리서치 (웹서치로 사실 확인)**

- 기니피그 케이지 최소 면적: Humane Society 기준 1마리 7.5 sq ft, 2마리 이상은 10.5 sq ft 이상 권장(대부분의 펫샵 케이지는 4-6 sq ft로 훨씬 미달) — 사용자 브리핑 수치와 정확히 일치 확인.
- 비타민C: 인간과 마찬가지로 L-굴로노락톤 산화효소가 없어 자체 합성 불가, 하루 10-30mg 필요, 신선 채소(특히 파프리카)가 물에 타는 첨가제보다 훨씬 신뢰도 높음(빛에 몇 시간 내 분해) — PetMD, Merck Veterinary Manual, guinealynx.info 등 복수 소스로 교차 확인.
- 사회적 동물 단독사육 비권장 + 스위스는 실제로 법적 의무(2008년 동물보호법, Animal Protection Ordinance)로 명문화돼 있음을 다수 소스(FSVO 공식 확인 포함)로 검증.
- 알팔파는 생후 6개월 미만/임신·수유 중만, 이후 성체는 티모시/오차드 그라스로 전환(칼슘 과다로 인한 방광/신장결석 위험) — 다수 수의학 소스 일치.
- 삼나무(cedar)·소나무(pine) 베딩 금지(페놀 화합물로 호흡기+간 문제), 와이어 바닥 금지(bumblefoot 발쪽 염증) — PetMD, Kaytee, wheekcare.org 등으로 확인.
- 수명 5-7년(우수한 관리 시 8년+) — 확인.

**2. 신규 체크리스트 A — `checklists/new-guinea-pig-checklist.html`**

- 사이트 세 번째 비(非)개·고양이 콘텐츠(토끼에 이은 두 번째 확장). `new-rabbit-checklist.html`을 구조 템플릿으로 그대로 복제(스키마 2종, 진행률바, 프린트, disclaimer, 본문 FAQ 패턴).
- 항목 20개, 6개 섹션(Housing & Supplies 7 / Companionship 2 / Vet Care 3 / Home Prep & Safety 3 / Handling & Routine 3 / Budget & Planning 2).
- **토끼 체크리스트에 없던 차별화 각도(사용자 지시 반영)**: Companionship 섹션을 별도로 신설해 "단독 사육 비권장 + 스위스 법적 의무" 항목을 명시적으로 넣음 — 토끼는 이 각도가 없었던 지점.
- 전용 계산기가 없으므로 tool 링크 대신 `/checklists/` 허브만 안내(사용자 지시대로 도구 링크 생략).
- FAQ 6개, 스키마+본문 1:1.
- QA: ItemList 20개 = 실제 체크박스 20개 일치, FAQ 6/6 매칭, div(15/15)·label(20/20) 균형.

**3. 신규 도구 B — `tools/cat-introduction-timeline.html`**

- 입력: 합사 시작일(월/일/년) / 새 고양이 유형(새끼·성묘) / 기존 고양이 나이대(새끼·성체·시니어) / 기존 고양이 마릿수(1/2/3+).
- 출력: 6단계 타임라인(격리방 → 냄새교환 → 문 사이 급여 → 영역교환(site swapping) → 시각접촉 → 감독하 대면), 각 단계마다 "다음 단계로 넘어가도 되는 신호"/"한 단계 되돌려야 하는 신호"를 고정 텍스트로 표시.
- **핵심 원칙 반영(사용자 지시)**: 날짜는 고정값이 아니라 시작일 기준 day-range(예: 격리방 day0-7)로 계산해 "빠르면 O월 O일 ~ 늦으면 O월 O일"로 표시, 결과창 하단에 "이건 전형적 범위이지 고정 일정이 아니다 — 고양이 속도에 맞춰라, 서두르는 게 합사 실패의 가장 흔한 원인이다" 경고문을 항상 고정 노출.
- 새끼고양이 합사(더 빠른 편, day 0-21)와 성묘 합사(더 느린 편, day 0-42, 완전한 우정은 6-12개월 걸릴 수 있음)를 별도 PACE 데이터셋으로 분리해 정확히 다른 범위 적용 — 웹서치로 "새끼고양이가 대체로 덜 위협적으로 인식돼 더 빠르게 진행되지만 기존 고양이가 시니어면 오히려 더 오래 걸릴 수 있다"는 소견 확인 후 반영.
- 비교표 2개: 새끼고양이 합사 vs 성묘 합사(속도/주요 리스크/도움되는 것/우정까지 걸리는 시간), 순조로운 신호 vs 경고 신호.
- **문제해결 섹션**: 하악질·하울링·리터박스 회피가 나타났을 때 "마지막으로 평온했던 단계로 되돌아가라"는 원칙 설명 + 이번 세션 이전에 만든 `kitten-litter-training-regression` 포스트로 연결(사용자 지시대로).
- n+1 리터박스 규칙은 `kitten-litter-training-timeline`과 중복이라 간단히 언급 후 링크로 넘김(사용자 지시대로).
- FAQ 6개, 스키마+본문 1:1.
- QA: node로 PACE 데이터 객체의 날짜 계산 로직 검증(새끼고양이/성묘 두 시나리오 각 6단계, 시작일 2026-07-31 기준 계산 결과가 코드에 명시한 day-range와 정확히 일치함을 확인), `node --check`로 JS 문법 오류 없음 확인.

**4. 역링크(양방향, 지시사항 그대로 이행)**

- `kitten-litter-training-timeline` ↔ `cat-introduction-timeline` (양방향).
- `kitten-litter-training-regression` 포스트 ↔ `cat-introduction-timeline` (양방향, Related Articles에 추가).
- `new-kitten-checklist` → `cat-introduction-timeline`.
- `/checklists/` 허브(`checklists/index.html`) → `new-guinea-pig-checklist` 카드 추가.

**5. 공통 파일 동기화**: 체크리스트는 `checklists/index.html`(카드 추가, New배지 이동) + `_includes/footer.html`(Checklists 컬럼) + `llms.txt`(Checklists 섹션). 도구는 `index.html`(카드 추가, New배지 이동) + `tools/index.html`(검색용 data속성 포함 카드 추가) + `_includes/footer.html`(Tools 컬럼) + `llms.txt`(Tools 섹션).

**6. QA(전수)**
- 전체 `_posts`(37개)+`tools`+`checklists`(76개 파일) front matter YAML 전수 통과.
- JSON-LD 오류 0건, FAQ 스키마-본문 1:1 매칭(체크리스트A 6/6, 도구B 6/6).
- slug 중복 없음(37개), permalink 중복 없음(37개, index 제외).
- 전체 링크 재스캔 — 브로큰 링크 0건.
- tool-card 개수: `index.html`/`tools/index.html` 31개 = 실제 tool 파일 31개 일치. `checklists/index.html` 카드 6개 = 실제 checklist 파일 6개 일치.
- div 균형: 역링크 추가로 수정한 기존 파일(kitten-litter-training-timeline, new-kitten-checklist, checklists/index.html, index.html, tools/index.html) 전부 짝 맞음.

**오늘(세션 S) 최종 페이지 수**: tools 31 + posts 37 + checklists 6 = 74페이지. 신규 순증 2개(`new-guinea-pig-checklist`, `cat-introduction-timeline`).

**다음 세션에서 확인할 것**:
- 오늘 만든 신규 2개의 GSC 노출/색인 여부 확인(최소 1-2주 필요).
- **배치 4(해외 이동 타임라인, 구충 스케줄)만 남았음 — ⚠️ 둘 다 건강/규제 정보라 추론 강도 높게 유지할 것. 특히 해외 이동 타임라인은 국가별 요건을 단정하지 말고 "등급(tier)" 추상화로만 다뤄야 한다는 지시가 있었음.**
- 구충 스케줄 계산기는 사용자 지시에 따라 "기존 백신 계산기와 너무 겹친다고 판단되면 새 URL 대신 기존 계산기 확장"도 선택지로 열려 있음 — 진행 시 이 판단부터 먼저 내리고 근거를 보고할 것.
- 이번 세션으로 별도 채팅에서 발굴한 12개 후보(S급4+A급4+B급4) 중 배치1·2·3(총 8개, S급4+A급4)이 전부 완료됨. 배치4(B급 중 2개)만 남음.

---

### 세션 T — 배치 4 실행(최종): 펫 해외이동 타임라인 플래너 + 구충 스케줄(기존 계산기 확장 판단) (7/27, 세션 S 직후)

**배경**: 별도 채팅에서 발굴한 12개 후보 중 마지막 배치 4. 도구 A(해외이동)는 정확도 리스크가 크다고 사용자가 명시적으로 경고해 추론 강도를 높게 유지하며 진행. 도구 B(구충 스케줄)는 "기존 백신 계산기와 겹치면 새 URL 대신 확장" 판단권을 위임받음.

**1. 신규 도구 A — `tools/pet-travel-timeline-planner.html`**

- 사전 리서치(웹서치, 정확도 리스크 높은 페이지라 USDA APHIS·CDC 공식 페이지 포함 다수 소스 교차검증):
  - **마이크로칩 → 광견병 접종 순서**: USDA APHIS·CDC 공식 페이지(프랑스/독일/스페인/일본 등 개별 국가 안내 다수)에서 "광견병 백신은 반드시 마이크로칩 삽입 이후에 접종해야 유효"라는 문구를 반복 확인. 순서가 바뀌면 재접종 필요.
  - **항체검사(FAVN) 대기기간**: 채혈은 접종 후 최소 30일 경과 필요, 검사기관 처리기간 통상 2-6주(성수기 6-8주), 결과 통과 후 추가 대기기간이 목적지에 따라 30일(하와이)~90일(EU 다수)~180일(호주·뉴질랜드·일본)까지 편차가 큼을 6개 이상 소스로 확인.
  - **건강증명서 유효기간**: EU向은 USDA 배서로부터 도착까지 10일 이내라는 규정을 USDA 공식 독일/스페인 페이지에서 직접 확인.
  - **USDA 인증 수의사 요건**: 인증받지 않은 수의사는 서류 작성 자체가 불가하며 VEHCS 시스템을 통해 제출해야 한다는 점을 APHIS 공식 페이지로 확인.
- **국가별 단정 금지 원칙을 철저히 준수**: 입력은 특정 국가가 아니라 "등급(tier) 1/2/3"(항체검사 불필요/항체검사+중간대기/항체검사+최장대기)로만 추상화. FAQ에서도 "왜 국가명을 명시하지 않는가"를 별도 문항으로 만들어 이유(요건이 자주 바뀜)를 설명.
- **출발일 기준 역산 마일스톤**: 건강증명서(출발 10일 전) → [등급2/3만] 결과 후 대기 시작일 → 채혈일(대기+검사기간 역산) → 광견병 접종일(채혈 30일 전) → 마이크로칩(접종과 동일 시점, 반드시 그 이전). 대표 수치는 등급1(백신 후 30일), 등급2(대기 90일+검사 30일), 등급3(대기 180일+검사 30일)로 설정 — 전부 "일반적으로 이 정도"라는 문구와 함께, 정확한 수치는 목적지마다 다르다는 점을 반복 명시.
- **고정 경고문 2곳 배치(사용자 지시 그대로)**: 페이지 상단(입력 폼 위)과 결과 영역 하단 양쪽에 "실제 요건은 목적지 정부와 USDA APHIS 공식 페이지에서 반드시 확인하세요. 이 도구는 일정 계획 보조용입니다." 고정 노출 — JS 코드로도 확인.
- 마일스톤 중 오늘 날짜보다 과거인 항목은 빨간색으로 강조하고 "이미 지난 날짜 — 즉시 수의사에게 연락하세요" 경고 표시.
- 역링크(양방향): `titer-test-vs-revaccination-calculator` ↔ 신규 도구(항체검사가 두 도구의 공통 접점).
- FAQ 6개, 스키마+본문 1:1 — 최초 작성 시 스키마와 본문의 따옴표 스타일 불일치(작은따옴표 vs 큰따옴표)로 5/6 매칭 실패가 발견되어 즉시 수정, 재검증 후 6/6 통과.
- **내부 일관성 재검증**: 결과 텍스트에 "최장 등급은 출발 3-6개월 전부터 준비"라고 썼다가, 실제 도구의 계산 로직(node로 직접 실행 검증)이 등급3 기준 약 8개월 전 마일스톤을 산출한다는 걸 발견 — 본문·FAQ 문구를 "6-9개월"로 수정해 도구의 실제 계산 결과와 서술이 어긋나지 않도록 정합성 확보. (이 점검이 이번 세션에서 가장 중요했던 정확도 검증 단계.)

**2. 도구 B 판단 — 구충 스케줄은 신규 URL 대신 기존 백신 계산기 확장으로 결정**

- **판단 근거(사용자에게 보고)**: (1) 입력값이 완전히 동일함 — 백신 계산기가 이미 "나이(년/월/주)" 입력을 받고 있어 별도 나이 입력 UI를 다시 만드는 게 중복. (2) 현재 사이트의 최우선 리스크가 "미색인 URL 증가"라고 handover에 여러 세션째 명시돼 있음 — 새 URL을 늘리기보다 이미 트래픽이 있는 페이지를 보강하는 쪽이 낫다고 판단. (3) 신규 오너가 백신 일정과 구충 일정을 동시에 궁금해하는 경우가 많아, 같은 페이지에서 같이 보여주는 게 사용자 경험상으로도 자연스러움.
- **실행**: `dog-vaccination-schedule-calculator.html`, `cat-vaccination-schedule-calculator.html` 양쪽에 각각 "🪱 Deworming Schedule" 미니 계산기 섹션을 추가. 기존 나이 입력(`pup-age-*`/`kit-age-*`)을 그대로 재사용하는 별도 버튼("Get My Dog's/Cat's Deworming Schedule →")으로 구현 — 새 입력 필드 없음.
- 사전 리서치(웹서치, CAPC 공식 페이지 capcvet.org 직접 확인): "2주령부터 시작, 2주 간격으로 반복하다가 생후 2개월부터 매월, 생후 6개월부터 분기별"이 CAPC 공식 일반 가이드라인. 새끼고양이는 태반을 통한 감염이 없어(강아지는 임신 중 태반감염 가능) 통상 1주 늦은 3주령부터 시작한다는 점을 복수 2차 소스(UW-Madison 수의대, petcare-ai)로 확인 후 반영 — 사용자 브리핑과 정확히 일치.
- **필수 콘텐츠 전부 반영**: "왜 한 번으로 안 끝나는가"(성충만 죽고 조직 내 유충은 다음 세대로 재성숙) 문제해결 섹션, 회충의 인수공통 위험(아동 특히 취약) 별도 섹션, 분변검사 병행 권장(연 2회 이상, CAPC) 섹션.
- **절대 금지 원칙 준수**: 약물 용량·mg/kg·제품별 투여량은 전혀 다루지 않음 — JS 로직도 "단계(phase)"와 "간격"만 계산하고 결과 텍스트에도 명시적으로 "이 계산기는 일정과 간격만 다루며, 정확한 제품·용량은 수의사가 결정한다"는 문구를 FAQ에 고정 포함.
- 역링크(양방향): `flea-tick-prevention-cost-calculator` ↔ 두 백신 계산기(사용자 지시대로 — 구충·벼룩진드기가 종종 같은 예방 스케줄로 묶여 다뤄지므로).
- FAQ 각 페이지에 5개씩 추가(스키마+본문 1:1), front matter description을 구충 기능 반영해 갱신, llms.txt의 두 항목도 구충 기능 설명 추가.
- QA: 두 페이지 모두 JSON-LD FAQ 8/8 매칭(기존 3개+신규 5개), div 균형, `node --check`로 JS 문법 확인, **구충 단계 경계값(강아지 2주/8주/26주, 고양이 3주/9주/26주)을 node로 직접 여러 나이값 대입해 시뮬레이션 검증** — CAPC 수치와 정확히 일치 확인.

**3. 공통 파일 동기화**
- 도구A(신규 URL): `index.html`(카드 추가, New배지 이동) + `tools/index.html`(검색용 data속성 포함) + `_includes/footer.html`(Tools 컬럼) + `llms.txt`(Tools 섹션 신규 항목).
- 도구B(기존 확장, 신규 URL 아님): `llms.txt`의 기존 dog/cat 백신 계산기 항목에 구충 기능 설명 추가. index.html/tools/index.html의 카드 `<p>` 설명문은 그대로 둠(핵심 기능인 백신 위주 설명 유지, 과도한 변경 지양).

**4. QA(전수)**
- 전체 `_posts`(37개)+`tools`+`checklists`(77개 파일) front matter YAML 전수 통과.
- JSON-LD 오류 0건. FAQ 스키마-본문 1:1: 신규 도구A 6/6(따옴표 불일치 1건 발견 후 즉시 수정), dog-vaccination-schedule-calculator 8/8, cat-vaccination-schedule-calculator 8/8.
- slug 중복 없음(37개), permalink 중복 없음(38개, index 제외 — 신규 URL 1개만 추가).
- 전체 링크 재스캔 — 브로큰 링크 0건.
- tool-card 개수: `index.html`/`tools/index.html` 32개 = 실제 tool 파일 32개 일치.
- div 균형: 역링크·확장으로 수정한 모든 기존 파일(titer-test-vs-revaccination-calculator, flea-tick-prevention-cost-calculator, dog/cat-vaccination-schedule-calculator, index.html, tools/index.html, footer.html) 전부 짝 맞음.
- **정확도 리스크가 높은 도구A는 계산 로직을 node로 3개 등급 전부 실행해 마일스톤 날짜 체인이 내부적으로 일관됨을 확인**(예: 등급2/3에서 "대기 시작일" 마일스톤 = 채혈일+검사기간과 정확히 같은 날짜로 산출됨을 확인) — 계산 로직과 서술 텍스트("6-9개월") 간의 불일치를 발견해 즉시 수정한 것이 이번 세션 QA의 핵심 성과.

**오늘(세션 T) 최종 페이지 수**: tools 32 + posts 37 + checklists 6 = 75페이지. 신규 순증 1개(`pet-travel-timeline-planner`) — 구충 스케줄은 신규 URL이 아니라 기존 2개 페이지 보강이므로 페이지 수에 포함 안 됨.

**별도 채팅에서 발굴한 12개 후보(S급4+A급4+B급4) 중 배치1~4 전부 완료.** 최종 집계: 신규 URL 11개(spay-neuter-recovery-timeline, pet-insurance-waiting-period-tracker, neuter-timing-by-breed-size, puppy-socialization-checklist, new-guinea-pig-checklist, cat-introduction-timeline, pet-travel-timeline-planner = 7개 신규 페이지) + 기존 페이지 보강 다수(구충 스케줄은 신규 URL 없이 흡수).

**다음 세션에서 확인할 것**:
- 오늘 만든 `pet-travel-timeline-planner`의 GSC 노출/색인 여부 확인(최소 1-2주 필요).
- 구충 스케줄을 추가한 두 백신 계산기(`dog-vaccination-schedule-calculator`, `cat-vaccination-schedule-calculator`)의 노출 변화 확인 — 콘텐츠 보강이 기존 트래픽에 긍정적 영향을 주는지 관찰(세션 M 이후 반복 확인해온 "보강 효과 시차" 패턴과 비교).
- 12개 후보 전부 소진됐으므로, 다음 GSC/GA 데이터 확인 시점에는 다시 신규 클러스터 발굴부터 시작해야 함(이번처럼 별도 기획 전용 대화에서 웹서치 기반 후보 리스트를 새로 뽑는 방식 반복 권장).
- Coverage 21개 미색인 이슈는 여러 세션째 미해결 — 사용자가 GSC UI에서 개별 URL 재크롤 요청(특히 `cat-pregnancy-calculator`)을 해줬는지 다음 GSC 데이터에서 확인.

---

### 버그 수정 (세션 T 직후, 세션 U 이전 — 별도 커밋, handover 기록 누락분 소급 반영)

세션 T 직후 사용자가 화면 캡처로 버그 2건을 신고해 별도 커밋(`7aef55e`)으로 수정함. 이번 세션 U 진행 전에 기록을 남겨둔다.

1. **`cat-vaccination-schedule-calculator.html` 스크립트 전체 파손**: 구충 스케줄 텍스트의 `aren't` 축약형을 이스케이프하다가 백슬래시가 4개로 겹쳐써져서(`aren\\\\'t`) 문자열이 중간에 끊기고 JS 파싱 자체가 깨짐(`Uncaught SyntaxError: Unexpected identifier 't'`). 스크립트 블록 전체가 실패해 백신·구충 버튼 둘 다 죽음.
   - **QA 프로세스 자체의 결함 발견**: 기존 QA 스크립트가 `scripts[0]`(작은 프린트 함수)만 `node --check`했고, 실제 버그가 있던 두 번째(메인) `<script>` 블록은 검사하지 않아 "문법 오류 없음"으로 잘못 보고했었음. → **이후 모든 세션의 QA는 페이지의 모든 `<script>` 블록을 인덱스 상관없이 전부 검사**하도록 교정(이번 세션 U부터 실제 반영, 79개 파일 49개 스크립트 블록 전수 검사 완료).
   - 수정: 축약형 자체를 없애고 "are not infected"로 재작성.
2. **`pet-travel-timeline-planner.html` 프린트 첫 페이지 빈 페이지**: 페이지 상단 고정 경고박스에 `no-print` 클래스가 빠져 인쇄 시 결과 박스가 통째로 2페이지로 밀려남. 수정: `no-print` 클래스 추가.

두 버그 모두 node로 재현 확인 후 수정, 사이트 전체 재스캔으로 동일 패턴 다른 곳에 없음을 확인. 이 교훈이 이번 세션 U의 QA 체크리스트에 정식으로 편입됨(아래 참고).

---

### 세션 U — 배치 1 실행: 강아지 합사 타임라인 + 신생아 준비 타임라인 (8/1, 별도 기획 대화의 12개 신규 후보 중 배치 1)

**배경**: 별도 채팅에서 GSC/GA 분석과 무관하게 신규 클러스터를 대량 발굴하는 기획 전용 세션을 진행, 웹서치로 경쟁조사까지 마친 12개 후보(S급4+A급4+B급4)를 배치로 정리해 전달받음. 이번 세션은 배치 1(S급 2개)을 그대로 실행.

**⚠️ 사용자가 지난 버그 2건을 명시적으로 QA 체크리스트에 추가해서 지시** — 아래 QA 섹션에 전부 반영.

**1. 신규 도구 A — `tools/dog-introduction-timeline.html`**

- 기존 `cat-introduction-timeline.html`을 구조 템플릿으로 삼되 내용은 완전히 새로 작성(복붙 아님 — 개와 고양이 합사 프로토콜이 실제로 다름을 웹서치로 확인 후 반영).
- 웹서치로 확인한 핵심 사실: 중립 지역 필수(집·마당에서 첫 대면은 "가장 흔한 실패 원인"), 평행 산책은 20~40ft에서 시작해 서로 무시하는 상태가 될 때까지 좁히기, 각도 접근 후 짧은 냄새 맡기(정면 대면은 대치 신호로 읽힘), 귀가 시 기존 개가 먼저 입장, 자원 보호 징후 시 2~4주 구조적 분리, 싸움 발생 시 24시간 이상 완전 분리 후 더 먼 거리에서 평행 산책부터 재시작, 공격 이력이 있으면 전문 트레이너 개입 필수.
- 입력: 합사 시작일 / 새 개 유형(강아지·성견) / 기존 개 나이대 / 기존 개 마릿수. 출력: 6단계 타임라인(중립지역 첫 대면 → 평행 산책 → 각도 접근·짧은 냄새 → 함께 귀가 → 실내 감독 상호작용 → 감독 없는 시간 점진 확대), 각 단계 "다음 단계로 넘어가도 되는 신호"/"되돌려야 하는 신호" 고정 텍스트.
- 강아지 프로필(더 빠름, day 0-21)과 성견 프로필(더 느림, day 0-45, 자원보호 이력 시 2-4주 별도 언급)을 별도 데이터셋으로 분리 — node로 날짜 계산 체인 검증 완료.
- 비교표 2개(강아지 합사 vs 성견 합사 / 순조로운 신호 vs 경고 신호), 문제해결 섹션(자원 보호·싸움 발생·공격 이력) 전부 반영. FAQ 6개, 스키마+본문 1:1.

**2. 신규 도구 B — `tools/new-baby-pet-prep-timeline.html`**

- 입력: 출산 예정일 / 종(개·고양이) / 현재 문제행동 유무. 출력: 예정일 기준 역산 마일스톤(120일 전 행동교육 기초 → 90일 전 소리 둔감화 시작 → 60일 전 도구연습·자원접근성 점검·루틴 전환 → 30일 전 안고다니기 리허설·핸들링 숙달 → 예정일 냄새 노출(병원에서 아기담요 먼저 보내기) → +2일 귀가 첫 대면).
- 종별로 완전히 다른 내용 반영(사용자 지시대로 "같게 쓰지 마라"): 개는 유모차 연습·베이비게이트·인형 안고다니기, 고양이는 소리 노출 대신 **자원 접근성 감사**(리터박스·급식·수직공간이 육아용품에 막히지 않는지)와 스스로 다가오게 두는 방식으로 완전히 다르게 작성.
- 고정 경고(결과 영역): "아무리 순한 반려동물이라도 아기와 단둘이 두지 마세요", 얼굴 핥기 금지 명시.
- 문제해결 섹션: 아기 소리에 떨거나 숨거나 배변 실수를 하면 전문가(수의행동전문가/인증 트레이너) 개입 신호라는 점 명확히 서술.
- 비교표 1개(개 준비 vs 고양이 준비). FAQ 6개, 스키마+본문 1:1.
- **의도적으로 링크 안 건 것(사용자 지시)**: 도구 B ↔ dog/cat-vaccination-schedule-calculator는 연결 안 함(관련성 약함 판단). annual-pet-cost-calculator에도 안 걸고 대신 /checklists/ 허브로 연결.

**3. 역링크(양방향, 지시사항 그대로 이행)**
- `cat-introduction-timeline` ↔ `dog-introduction-timeline`(자매 도구).
- `new-puppy-checklist` → 도구A, `puppy-socialization-checklist` → 도구A.
- `puppy-socialization-checklist` → 도구B(사람·아이 노출 항목과 직접 연결이라는 지시 반영).

**4. 공통 파일 동기화**: `index.html`(카드 2개 추가, New배지 이동) + `tools/index.html`(검색용 data 속성 포함) + `_includes/footer.html`(Tools 컬럼) + `llms.txt`(Tools 섹션 2개 항목).

**5. QA(전수, 지난 버그 2건 교훈 전부 반영)**
- **(버그1 교훈) 모든 `<script>` 블록을 인덱스 상관없이 전수 검사**: 전체 사이트 79개 파일에서 스크립트 블록 49개 전부 `node --check` 통과(0건 오류) — 신규 파일 2개뿐 아니라 사이트 전체 재검증.
- **(버그2 교훈) JS 문자열 아포스트로피 축약형 전면 금지**: 신규 2개 파일 작성 시 처음부터 축약형(aren't, isn't, don't 등)을 JS 문자열에 전혀 쓰지 않았고, `desc`/`forward`/`back` 필드가 전부 큰따옴표(") JS 문자열이라 그 안의 아포스트로피(dog's, dogs' 등)는 이스케이프가 필요 없는 안전한 상태임을 직접 확인. 예외적으로 이중 따옴표를 문자열 안에 넣어야 했던 한 곳("something small")은 정상적으로 이스케이프됐음을 grep+node로 재확인.
- **(버그3 교훈) 새 안내박스 no-print 여부 전수 스캔**: `.tool-box` 앞에 나오는 인라인 background 스타일 박스 중 `no-print` 클래스가 빠진 곳이 있는지 정규식으로 전체 tools 폴더 재스캔 — 0건.
- YAML 79개 파일 통과, JSON-LD 0오류, FAQ 스키마-본문 1:1(도구A 6/6, 도구B 6/6), div 균형(신규 2개 + 역링크 수정한 기존 4개 파일 전부), 링크 재스캔 0건 깨짐, tool-card 개수 일치(34=34=34).
- **날짜 계산 로직 node 검증**: 도구A(강아지·성견 두 프로필 각 6단계), 도구B(개·고양이 두 종 각 6개 마일스톤, offsetDays 음수 처리 포함)를 node로 직접 실행해 시간 순서와 날짜 산출이 서술 텍스트와 일치함을 확인.
- **빌드 확인은 Actions API 사용**(사용자가 지난 세션의 실제 경험을 근거로 명시적으로 지시 — legacy Pages Builds API가 최신 커밋을 못 잡는 저장소임).

**오늘(세션 U) 최종 페이지 수**: tools 34 + posts 37 + checklists 6 = 77페이지. 신규 순증 2개(`dog-introduction-timeline`, `new-baby-pet-prep-timeline`).

**다음 세션에서 확인할 것**:
- 오늘 만든 신규 2개의 GSC 노출/색인 여부 확인(최소 1-2주 필요).
- **별도 채팅에서 발굴한 배치 2(시니어 케어 체크리스트, 강아지 유치 타임라인 — 둘 다 추론 강도 High 필수), 배치 3(펫보험 청구 환급액 계산기, 반려동물 동반 이사 체크리스트), 배치 4(치아 홈케어/두 번째 반려동물 비용/크레이트 훈련/햄스터 체크리스트 — 이 배치는 만들기 전에 "만들지 말지"부터 판단해야 함)를 순서대로 진행할 것.**
- 이번에 세운 새 QA 표준(모든 스크립트 블록 전수 검사, 아포스트로피 축약형 금지, no-print 스캔)을 다음 세션들에도 계속 유지할 것 — handover.md의 "작업 방식" 섹션에 정식 반영을 고려.
- Coverage 21개 미색인 이슈는 이번 세션에도 다루지 않음 — 계속 열린 상태.

---

### 세션 V — 배치 2 실행: 시니어 반려동물 케어 체크리스트 + 강아지 유치 타임라인 (8/1, 세션 U 직후)

**배경**: 별도 채팅에서 발굴한 12개 후보 중 배치 2. 사용자가 "시니어는 건강·정서 민감 영역이라 표현 수위 판단이 계속 필요하다"며 추론 강도를 명시적으로 높게 유지하라고 지시.

**1. 신규 체크리스트 A — `checklists/senior-pet-care-checklist.html`**

- **프레이밍 원칙을 문구 전체에 엄격 적용**: "노화는 질병이 아니라 정상적인 생애 전환기"라는 톤을 헤더·디스클레이머·FAQ 전체에 일관 반영, 겁주는 표현 배제. 진단·투약·용량은 전혀 다루지 않고 "관찰 후 수의사에게 물어볼 것" 수준으로만 서술. **안락사·임종 콘텐츠는 명시적으로 배제**(기존 QoL 계산기+euthanasia 포스트 영역으로 남겨둠) — 작성 후 "euthaniz/dosage/mg per kg" 등 금지어 전수 스캔으로 0건 확인.
- 웹서치로 확인한 사실: 체급별 시니어 진입 연령(소형 10-12세/중형 8-10/대형 6-8/초대형 5-6, 고양이 대략 10-12 — 사용자 브리핑과 일치), 시니어 검진 연 2회(VCA·AAHA 등 다수 소스), 시니어 혈액검사 패널 구성(CBC·화학패널·요검사·T4 갑상선검사, ± 혈압측정) — **항목명만 나열, 수치 해석·정상범위는 전혀 다루지 않음**, 관절염·치과질환이 "그냥 노화"로 가장 흔히 오인/과소진단되는 2대 질환이라는 점 복수 소스로 확인.
- **인지기능장애(DISHA)는 의도적으로 "관찰 항목" 수준으로만 축소**: DISHA 5개 범주(방향감각상실·상호작용변화·수면주기변화·배변실수·활동량변화)를 웹서치로 정확히 확인했지만, 사용자 지시("진단 도구로 만들지 마라")에 따라 **자가 채점 체크리스트나 프레임워크로 구조화하지 않고**, 체크리스트 항목 1개("새로운 혼란·방향감각상실·배변실수 기록해서 수의사에게 공유")와 FAQ 답변 1개로만 가볍게 다룸 — 진단 도구처럼 보이지 않도록 의도적으로 얕게 처리.
- 개·고양이 공용 통합형(기존 `pet-emergency-kit-checklist.html` 패턴). 항목 19개, 6개 섹션(Understanding Your Senior Pet 2 / Vet Care & Screening 4 / Home & Mobility 5 / Nutrition 2 / Mental & Behavioral Wellness 3 / Comfort & Daily Life 3). FAQ 6개, 스키마+본문 1:1.

**2. 신규 도구 B — `tools/puppy-teething-timeline.html`**

- 입력: 강아지 나이(개월/주). 출력: 현재 유치 단계 + 다음 단계. 웹서치로 확인한 7단계 경계값을 코드에 정확히 반영(2주 유치 맹출 시작/6-8주 유치 28개 완성/12-16주 탈락 시작/16-26주 영구치 맹출/26-30주 영구 어금니/30주+ 완성) — node로 여러 주령값 대입해 경계값 전부 검증.
- **잔존유치 섹션**: 4개월(16주)부터 확인 시작 권고, 중성화 수술(통상 5-7개월)과 시기가 겹쳐 같은 마취 중에 발치하는 경우가 많다는 실용적 조언을 웹서치로 정확히 확인 후 반영 — spay-neuter-cost-calculator/spay-neuter-recovery-timeline/neuter-timing-by-breed-size 3개 도구로 연결.
- 씹기 폭증 시기(3-6개월)가 배변훈련 퇴행 시기와 겹친다는 점 → `puppy-potty-training-regression` 포스트로 연결.
- 안전한 씹을거리 vs 피할 것 비교표 — 특정 제품명 없이 "엄지손톱으로 눌렀을 때 살짝 눌리는 정도" 같은 일반 기준으로만 서술(사용자 지시 반영).
- FAQ 5개, 스키마+본문 1:1.

**3. 역링크(양방향, 지시사항 그대로 이행)**
- 체크리스트A ↔ `dog-quality-of-life-calculator`, ↔ `cat-quality-of-life-calculator`(기존 post-cta 카드 패턴에 맞춰 추가).
- 체크리스트A ↔ `dog-vet-visit-scheduler`, `cat-vet-visit-scheduler`(연 2회 검진 접점).
- 체크리스트A ↔ 시니어 급여 포스트 2개(`how-much-should-senior-dog-eat`, `how-much-should-senior-cat-eat` — slug 직접 확인 후 정확한 링크로 연결).
- 도구B ↔ `dog-vaccination-schedule-calculator`, ↔ `puppy-potty-training-calculator`, ↔ `dental-cleaning-cost-calculator`, → `new-puppy-checklist`.

**4. 공통 파일 동기화 — QA 과정에서 누락 발견 후 수정**
- 처음 QA에서 tool-card 개수 불일치(34=34 vs 실제 35개)를 발견 — `index.html`/`tools/index.html`에 `puppy-teething-timeline` 카드 추가를 빠뜨렸던 것을 확인 후 즉시 수정. `checklists/index.html`도 동일하게 `senior-pet-care-checklist` 카드 누락을 발견해 수정. **이 실수는 "공통파일 동기화를 QA 이전에 끝냈다고 착각하고 QA를 돌린 것"이 원인 — 다음 세션은 공통파일 동기화 직후 반드시 카드 개수부터 재확인할 것.**
- `_includes/footer.html`(Tools/Checklists 컬럼 각각), `llms.txt`(Tools/Checklists 섹션 각각) 정상 반영.

**5. QA(전수, 지난 세션 표준 3가지 전부 적용 + 이번 세션에서 Rule B 정밀도 개선)**
- **Rule A(모든 스크립트 블록 전수 검사)**: 81개 파일 50개 스크립트 블록 전부 `node --check` 통과, 0건 오류.
- **Rule B(아포스트로피 축약형 스캔) — 이번 세션에서 탐지 로직을 라인 단위로 정밀화**: 1차 스캔은 정규식이 여러 줄에 걸쳐 과도하게 매칭돼 오탐이 많았음(세션 U에서 이미 지적된 문제가 재발) → 라인 단위 스캔으로 교정. 교정 후에도 기존 파일(`dog/cat-quality-of-life-calculator`, `dog/cat-vaccination-schedule-calculator`, `dog/cat-vet-visit-scheduler`, `dog/cat-age-calculator`) 여러 곳에서 `it\'s`, `dog\'s` 같은 **단일 백슬래시로 정상 이스케이프된 기존 패턴**이 걸렸으나, Rule A가 이미 해당 스크립트 블록 전부를 오류 없이 통과시켰다는 사실로 안전함을 재확인 — 이번 세션에 새로 만든 파일 2개는 이 패턴이 전혀 없음(전부 큰따옴표 문자열 사용).
- **Rule C(no-print 스캔)**: 0건.
- YAML 81개 파일 통과, JSON-LD 0오류, FAQ 스키마-본문 1:1(체크리스트A 6/6, 도구B 5/5), slug 중복 없음(37개), permalink 중복 없음(42개), 링크 재스캔 0건 깨짐.
- **최종 tool-card/checklist-card 개수 일치 재확인**: `index.html`/`tools/index.html` 35=35=35, `checklists/index.html` 7=7.
- div 균형: 신규 2개 + 역링크 수정한 기존 9개 파일 전부 짝 맞음.
- 유치 단계 경계값 node 시뮬레이션 검증(0/1/2/3/5/7/8/10/12~52주 대입, 전부 사용자 브리핑 수치와 일치).

**오늘(세션 V) 최종 페이지 수**: tools 35 + posts 37 + checklists 7 = 79페이지. 신규 순증 2개(`senior-pet-care-checklist`, `puppy-teething-timeline`).

**다음 세션에서 확인할 것**:
- 오늘 만든 신규 2개의 GSC 노출/색인 여부 확인(최소 1-2주 필요).
- **별도 채팅에서 발굴한 배치 3(펫보험 청구 환급액 계산기, 반려동물 동반 이사 체크리스트), 배치 4(치아 홈케어/두 번째 반려동물 비용/크레이트 훈련/햄스터 체크리스트 — "만들지 말지"부터 판단 필요)를 순서대로 진행할 것.**
- **공통파일 동기화 직후 tool-card/checklist-card 개수를 바로 재확인하는 습관을 들일 것** — 이번 세션에 실제로 누락이 있었고 QA에서 잡아냈지만, 애초에 순서를 "동기화 → 개수확인"으로 명확히 분리했으면 두 번 작업할 필요가 없었음.
- Coverage 21개 미색인 이슈는 이번 세션에도 다루지 않음 — 계속 열린 상태.

---

### 세션 W — 배치 3 실행: 펫보험 청구 계산기 + 반려동물 동반 이사 체크리스트 (8/1, 세션 V 직후)

**배경**: 별도 채팅에서 발굴한 12개 후보 중 배치 3. 세션 V의 교훈(공통파일 동기화 직후 즉시 개수 재확인)을 이번 세션부터 실제 적용.

**⚠️ 중요 — 사용자 브리핑과 실제 조사 결과가 반대였던 부분을 발견하고 정정함**: 사용자 지시문은 "건별공제는 만성질환처럼 매년 재발하는 경우에 훨씬 불리하다"고 서술했으나, 웹서치(Spot·Trupanion·PetMD·Money.com·TailSmart 등 다수 소스)로 확인한 업계 표준 정의는 **정반대**였음 — 건별(per-incident/per-condition) 공제는 **해당 조건에 대해 평생 딱 한 번만** 내는 구조라 만성질환에는 오히려 **유리**하고, 연간(annual) 공제가 매 갱신마다 다시 내야 해서 동일 만성질환이 여러 해 재발할 경우 **더 불리**함. (반대로 건별공제는 서로 무관한 여러 질환이 새로 생길 때마다 공제를 새로 내야 해서 그 경우엔 연간공제가 유리 — 이 부분은 사용자 브리핑과 결과적으로 같은 결론.) **핵심 wedge(연간 vs 건별 나란히 비교)는 브리핑 그대로 구현했지만, "어느 쪽이 만성질환에 유리한가"의 방향은 정확한 업계 정의에 맞춰 수정해서 반영함.** 계산 로직도 이 정정된 이해를 바탕으로 구현하고 node로 5년치 시나리오를 직접 계산해 방향성이 실제로 그렇게 나오는지 검증함(연간공제 5년합계 OOP $3500 vs 건별공제 5년합계 OOP $1700 — 건별이 더 저렴하게 산출됨, 계산 로직과 서술 텍스트 일치 확인).

**1. 신규 도구 A — `tools/pet-insurance-claim-calculator.html`**

- 입력: 청구금액/공제액(100~1000 드롭다운)/공제유형(연간·건별)/올해(또는 해당 조건) 이미 충족한 공제액/환급률(70·80·90%)/올해 남은 연간한도. 출력: 예상 환급액/본인부담액/남은 공제액/남은 연간한도.
- **차별화 섹션**: 동일 조건이 5년간 매년 재발한다고 가정했을 때 연간공제 vs 건별공제 5년 누적 본인부담액을 표로 나란히 비교하는 별도 계산 버튼 — node로 여러 시나리오(정상 청구/공제액 미만 청구/공제 일부 충족 상태)를 검증 후 반영.
- 특정 보험사 추천·순위 전혀 없음, 업계 일반 범위만 중립적으로 서술. "어느 상황에 어느 구조가 유리한가" 비교표(만성질환 단일=건별 유리/여러 무관 질환=연간 유리/예측 불가=연간이 더 안전한 기본값)로 균형 잡힌 결론 제시.
- FAQ 5개, 스키마+본문 1:1.

**2. 신규 체크리스트 B — `checklists/moving-with-pets-checklist.html`**

- 날짜순 5단계(이사 4주 전/2주 전/1주 전/이사 당일/도착 후 첫 주), 총 24개 항목.
- 웹서치로 확인한 실무 사실 전부 반영: 마이크로칩 주소 변경이 "가장 흔히 잊는 항목"이라는 점(AAHA·복수 이사업체 블로그로 확인), 이사 당일 안전한 방 격리+"열지 마세요" 표지판(탈출 방지, 이사 중 실종의 가장 흔한 원인), 도착 후 한 방부터 점진적 개방, 고양이는 기존 리터박스·리터 브랜드 유지(리터 회귀 트리거), 고양이 실외 노출은 최소 2-3주 대기, 지역별 반려동물 등록·목줄·품종 규제 사전 확인.
- 고양이 리터 회귀 항목 → 기존 `kitten-litter-training-regression` 포스트로 연결(slug 직접 확인 후 정확한 링크).
- 항목 24개, FAQ 6개, 스키마+본문 1:1.

**3. 역링크(양방향, 지시사항 그대로 이행)**
- `pet-emergency-kit-checklist` ↔ `moving-with-pets-checklist`(둘 다 "비상/이동" 성격).
- `annual-pet-cost-calculator` → 도구A(단방향, 지시대로).
- `/checklists/` 허브 → 체크리스트B(카드 추가로 자연스럽게 연결).
- **추가로 3자 양방향 완성**: 도구A ↔ `pet-insurance-cost-estimator` ↔ `pet-insurance-waiting-period-tracker` 보험 클러스터 3개 도구 전부 서로 연결(지시사항의 "3자 양방향 연결" 요구 정확히 이행).

**4. 공통 파일 동기화 — 이번엔 즉시 개수 검증 적용**
- `index.html`/`tools/index.html`/`checklists/index.html` 카드 추가 직후 각각 바로 `grep -c`로 실제 파일 개수와 대조(36=36, 8=8) — 세션 V에서 지적된 "동기화 후 QA까지 가서야 발견" 패턴을 이번엔 재발시키지 않음.
- `_includes/footer.html`(Tools/Checklists 컬럼), `llms.txt`(Tools/Checklists 섹션) 정상 반영.

**5. QA(전수, 3가지 표준 규칙 전부 적용)**
- Rule A(모든 스크립트 블록 전수 검사): 83개 파일 51개 스크립트 블록 전부 `node --check` 통과, 0건 오류.
- Rule C(no-print 스캔): 0건.
- YAML 83개 파일 통과, JSON-LD 0오류, FAQ 스키마-본문 1:1(도구A 5/5, 체크리스트B 6/6), slug 중복 없음(37개), permalink 중복 없음(44개), 링크 재스캔 0건 깨짐.
- 최종 tool-card/checklist-card 개수 일치: 36=36=36, 8=8.
- div 균형: 신규 2개 + 역링크 수정한 기존 6개 파일 전부 짝 맞음.
- **보험 계산 로직 node 검증**: 정상청구/청구액이공제미만/공제일부충족 3개 시나리오 + 5년 만성질환 비교(연간 vs 건별) 전부 수동 계산과 대조해 정확성 확인.

**오늘(세션 W) 최종 페이지 수**: tools 36 + posts 37 + checklists 8 = 81페이지. 신규 순증 2개(`pet-insurance-claim-calculator`, `moving-with-pets-checklist`).

**다음 세션에서 확인할 것**:
- 오늘 만든 신규 2개의 GSC 노출/색인 여부 확인(최소 1-2주 필요).
- **별도 채팅에서 발굴한 배치 4(치아 홈케어/두 번째 반려동물 비용/크레이트 훈련/햄스터 체크리스트)만 남음 — 이 배치는 "만들기 전에 만들지 말지부터 판단"하라는 지시가 있었으니 웹서치 경쟁조사 결과에 따라 실제로 안 만드는 항목이 나올 수 있음.**
- 이번 세션으로 별도 채팅에서 발굴한 12개 후보(S급4+A급4+B급4) 중 11개 완료, 배치4(4개 후보 중 실제 제작 여부 미정)만 남음.
- Coverage 21개 미색인 이슈는 이번 세션에도 다루지 않음 — 계속 열린 상태.

---

### 세션 X — 배치 4(최종): 4개 후보 전부 "만들지 말지" 판단 → 4개 전부 신규 URL 미생성 (8/1, 세션 W 직후)

**배경**: 별도 채팅에서 발굴한 12개 후보 중 마지막 배치 4. 이번 배치는 사용자가 "만들지 말지부터 네가 판단하라"고 명시적으로 위임 — 4개 후보 전부 웹서치 경쟁조사 먼저 진행 후 판단.

**결과 요약: 4개 후보 전부 신규 URL을 만들지 않기로 판단.** 1개(치아 홈케어)는 기존 페이지에 소규모 콘텐츠로 흡수, 3개(두 번째 반려동물/크레이트 훈련/햄스터)는 완전 기각.

**후보 1) 개·고양이 치아 홈케어 스케줄 — 기존 페이지에 소규모 흡수**

- 웹서치 결과: 칫솔질 빈도(매일 이상적, 주3회도 유의미)·VOHC 인증 개념·마취없는 스케일링 반대 근거(AVDC "malpractice" 수준 표현, AAHA 2019 가이드라인도 명시적 반대) 전부 정적 콘텐츠(dvm360·AKC·AVMA·VCA 등)로는 매우 두껍게 존재하지만 인터랙티브 도구는 없음.
- **그러나 기존 `dental-cleaning-cost-calculator.html`을 직접 확인한 결과, 마취없는 스케일링 반대 내용은 이미 전용 FAQ+본문 단락으로 충실히 다루고 있었음** — 조사 포인트 중 "마취 없는 스케일링의 한계"는 사실상 이미 커버된 상태였고, 실제 빈 곳은 **칫솔질 빈도 구체 수치 + VOHC 인증마크 설명** 정도로 생각보다 좁았음.
- 판단: 신규 URL은 정당화하기엔 콘텐츠 볼륨이 부족(개인화 계산 로직이 필요 없는 순수 정적 정보라 계산기 형태와도 안 맞음) → **기존 `dental-cleaning-cost-calculator.html`에 "Home Care Between Cleanings" 섹션 + FAQ 2개 추가로 흡수**. 신규 URL 생성 안 함, 공통파일 동기화·역링크·New배지 작업 불필요(기존 페이지 보강일 뿐).
- FAQ 3개→5개로 증가, 스키마+본문 1:1 재검증(5/5).

**후보 2) 두 번째 반려동물 추가 비용 계산기 — 완전 기각(재확인)**

- **먼저 handover.md 기각 목록 확인 결과, 이 후보는 이미 과거 세션에서 "2번째 반려동물/다마리가구 비용 계산기(calcbee + AKC/Trupanion/Rover 가이드까지)"로 기각된 이력이 있었음** — 사용자에게 이 사실을 먼저 보고.
- 오늘 "증분 비용(marginal/incremental cost)" 이라는 새 각도로 재조사했으나, **CalcBee의 "Multi-Pet Household Cost Calculator"가 이미 정확히 이 각도("일부 비용은 마리수에 비례 증가, 일부는 공유되어 한계비용 체감")를 그대로 구현한 상태**임을 확인 — 제안된 차별화 앵글 자체가 이미 선점됨. AKC의 "Can I Afford a Second Dog?"도 동일 주제를 깊게 다룸.
- 판단: 자기잠식 위험(기존 `annual-pet-cost-calculator`) + 차별화 앵글 자체가 이미 경쟁사에 의해 선점됨 + 재조사해도 이전 기각 사유가 그대로 유효 → **완전 기각, 신규 URL도 흡수도 하지 않음**. 흡수(기존 계산기에 옵션 추가)도 고려했으나, 추가해도 CalcBee가 이미 하는 것과 차별점이 없어 실익이 낮다고 판단.

**후보 3) 크레이트 훈련 타임라인 — 완전 기각**

- **사용자가 미리 경고한 대로, 기존 `puppy-potty-training-calculator.html`을 확인한 결과 이미 "Crate Training vs. Pad Training" 전용 비교표 + FAQ + 계산기 입력값(훈련방식 crate/pad 선택 시 결과가 달라지는 조건부 로직)까지 갖추고 있어 상당히 겹침**을 확인.
- 외부 경쟁조사도 매우 포화(AKC 2개 페이지, Purina 2개 페이지, PAWS/Humane Society, equilibriumcanine, naturalfarmpet, puppysimply 등 7곳 이상)됐고, 전부 정적 "단계별 가이드"라 우리가 붙일 수 있는 비용 차별화 앵글도 없음(크레이트 훈련은 비용이 드는 항목이 아님).
- 판단: 자사 콘텐츠와의 중복 + 외부 레드오션 + 차별화 앵글 부재 3중으로 **완전 기각**. 기존 페이지에 이미 충분히 다뤄지고 있어 흡수할 것도 없음.

**후보 4) 새 햄스터 체크리스트 — 완전 기각 (사용자 가설과 반대 결과)**

- 사용자는 "페럿보다 햄스터가 더 열려있을 가능성이 높다"고 가정했으나, **실제 조사 결과는 정반대**였음: 페럿의 ferret-world.com에 대응하는 **햄스터 전문 사이트가 최소 2곳**(smallpetexpert.com, yourpethamster.com) 확인됨 — 둘 다 DVM 감수·매우 깊은 콘텐츠(케이지 최소면적 100×50cm, 시리안 단독사육 필수, 삼나무/소나무 베딩 금지, 굴파기용 깊은 베딩, 습식꼬리병 등 브리핑에서 요구한 모든 종 고유 항목 이미 다룸).
- **결정적으로, `yourpethamster.com`은 이미 우리가 만들려던 것과 정확히 같은 유형의 인터랙티브 도구를 보유 중** — "Build My Hamster Habitat"(드래그앤드롭 사육장 플래너), "Start Hamster Care Quiz"(7문항 개인화 서식 플랜 생성기). 토끼·기니피그 체크리스트가 성공했던 핵심 근거("정적 콘텐츠 경쟁자만 있고 인터랙티브 도구는 0곳")가 햄스터에는 적용되지 않음 — 오히려 이미 인터랙티브 경쟁자가 존재.
- 판단: 종 확장 패턴의 핵심 전제(무경쟁 인터랙티브 니치)가 깨졌으므로 **완전 기각**. 다음에 종 확장을 다시 시도한다면 햄스터·페럿 둘 다 제외하고 다른 소동물(예: 친칠라, 저빌 등)부터 조사할 것.

**공통 파일 동기화**: 신규 URL이 전혀 없으므로 `index.html`/`tools/index.html`/`checklists/index.html`/`footer.html`의 카드 추가나 New배지 이동 없음. `llms.txt`의 기존 `dental-cleaning-cost-calculator` 항목만 Home Care 섹션 추가를 반영해 갱신.

**QA(전수, 3가지 표준 규칙 적용)**
- Rule A(모든 스크립트 블록 전수 검사): 83개 파일 51개 스크립트 블록 전부 `node --check` 통과, 0건 오류(신규 URL 없어 스크립트 블록 총수는 세션 W와 동일).
- Rule C(no-print 스캔): 해당 없음(신규 박스 추가 없이 순수 텍스트 콘텐츠만 추가).
- YAML 83개 파일 통과, JSON-LD 0오류, FAQ 스키마-본문 1:1(dental-cleaning-cost-calculator 5/5), 링크 재스캔 0건 깨짐.
- tool-card/checklist-card 개수: 36=36=36, 8=8 — 신규 URL이 없으므로 세션 W와 동일하게 유지됨(변화 없음이 곧 정답).

**오늘(세션 X) 최종 페이지 수**: tools 36 + posts 37 + checklists 8 = 81페이지 — **신규 URL 0개, 기존 페이지 1곳만 콘텐츠 보강.**

**별도 채팅에서 발굴한 12개 후보(S급4+A급4+B급4) 전부 소진 완료.** 최종 결과: 신규 URL 11개 생성(배치1~3), 기존 페이지 보강 흡수 2건(구충 스케줄-세션T, 치아홈케어-세션X), 완전 기각 확정 3건(두번째반려동물 재기각, 크레이트훈련, 햄스터).

**다음 세션에서 확인할 것**:
- 지금까지 만든 신규 URL 11개(spay-neuter-recovery-timeline부터 moving-with-pets-checklist까지) 전체의 GSC 노출/색인 여부를 한번에 종합 점검할 시점 — 개별 세션마다 산발적으로 확인해왔는데, 이제 12개 후보가 전부 소진됐으니 전체 배치 성과를 한 번에 리뷰하는 게 좋음.
- **12개 후보가 모두 소진됐으므로, 다음에 신규 콘텐츠가 필요하면 다시 처음부터 신규 클러스터 발굴(웹서치 기반 후보 리스트업)부터 시작해야 함.**
- **기각 후보 갱신**: 이번 세션에 "두 번째 반려동물 비용 계산기"(재기각, CalcBee가 정확히 같은 앵글 선점 확인), "크레이트 훈련 타임라인"(자사 콘텐츠 중복+레드오션), "햄스터 체크리스트"(전문 경쟁사 2곳+인터랙티브 경쟁자 존재)가 기각 목록에 새로 추가됨 — 다음 세션은 이 3개를 재조사하지 말 것.
- Coverage 21개 미색인 이슈는 이번 세션에도 다루지 않음 — 계속 열린 상태.

---

### 세션 Y — 신규 배치 1: 강아지 차멀미/불안 둔감화 플래너 + 고양이 캐리어 훈련 플래너 (8/1, 세션 X 직후)

**배경**: 12개 후보 소진 후 별도 기획 전용 대화에서 새로 발굴한 신규 클러스터 후보군 중 배치 1(S급, 개·고양이 대칭 페어) 실행.

**1. 신규 도구 A — `tools/dog-car-anxiety-desensitization-planner.html`**

- **핵심 차별화(사용자 지시대로 최상단 배치)**: 진짜 멀미(전정기관, 차가 움직인 뒤 증상 시작) vs 불안 주도(차가 움직이기 전부터 증상)를 구분하는 판별 비교표를 계산기보다 먼저 배치. 웹서치로 확인: 강아지는 내이가 미성숙해 멀미가 흔하고 성장하며 나아지는 경우 많음, 성견의 약 15%가 진짜 멀미, 진짜 멀미는 둔감화만으로 완전히 해결 안 되고 수의사 상담 필요(VETgirl·VCA·Today's Veterinary Nurse 등 복수 소스로 확인).
- 입력: 시작일/나이대(강아지·성견·시니어)/증상유형(불안·멀미·혼합)/심각도(경미·중간·심함). 출력: 6단계 타임라인(정차한 차 → 시동만 → 30초 주행 → 블록 한바퀴 → 5분 즐거운 목적지 → 점진 연장), 심각도별 배율(0.6/1.0/1.7)을 날짜 범위에 적용 — node로 3개 심각도 전부 날짜 계산 검증 완료.
- 필수 콘텐츠 전부 반영: 진짜멀미 vs 불안 비교표, 순조로운신호 vs 경고신호 비교표, 실무팁(진행방향 착석/부드러운 운전/식사 3-4시간 전/환기), "차=병원" 학습 문제해결 섹션.
- ⚠️ 약물(Cerenia/maropitant, trazodone)은 이름만 "수의사와 상의할 옵션"으로 언급, 용량·투여법 전혀 안 씀 — 결과 영역 고정 경고에도 재차 명시.
- FAQ 6개, 스키마+본문 1:1.

**2. 신규 도구 B — `tools/cat-carrier-training-planner.html`**

- 입력: 병원 예약일/현재 캐리어 반응(무반응·경계·공황)/캐리어 유형(탑로딩·프론트로딩). 출력: **예약일 기준 역산 2주 카운트다운**(기존 `pet-travel-timeline-planner`의 `subtractDays` 역산 패턴 재사용) — 7단계(캐리어를 가구화 → 캐리어 안/근처 급식 → 자발적 진입 보상 → 문 잠깐 닫기 → 들어올려 몇걸음 → 시동없이 차에 → 짧은 연습주행), 반응 강도별 배율(0.4/1.0/1.8) 적용 — node로 3개 반응강도 전부 역산 날짜 검증 완료.
- 필수 콘텐츠(웹서치로 확인): **탑로딩/분리형 캐리어가 스트레스를 크게 줄이는 이유**(끌어내지 않고 들어올릴 수 있음, 분리형은 하단에 앉은 채 진료 가능), **Feliway는 사용 15~30분 전에 분사**해야 알코올 베이스가 증발함(구체적 수치라 좋은 차별점), Fear Free 인증병원 개념, 보호자 불안 전이.
- 문제해결 섹션(사용자 지시대로): 예약이 급해 둔감화 시간이 없을 때 차선책(페로몬 즉시 분사, 익숙한 담요, 병원에 미리 전화해 항불안제 상담) — **훈련 대체가 아니라는 점 명시**.
- 비교표: 개 차 둔감화 vs 고양이 캐리어 훈련(주요 트리거/신체적 요인/전형적 기간 차이).
- ⚠️ 가바펜틴 등은 이름만 "수의사와 상의" 수준, 용량·타이밍 전혀 안 씀.
- FAQ 6개, 스키마+본문 1:1.

**3. 역링크(양방향, 지시사항 그대로 이행)**
- 도구A ↔ 도구B(자매 도구).
- 도구A ↔ `pet-travel-timeline-planner`, ↔ `moving-with-pets-checklist`.
- 도구B ↔ `cat-vet-visit-scheduler`, ↔ `cat-introduction-timeline`, → `new-kitten-checklist`(단방향, 지시대로).
- `dog-vet-visit-scheduler` → 도구A(단방향, 지시대로).
- 전부 실제 파일에서 양쪽 링크 존재 확인 완료.

**4. 공통 파일 동기화 — 세션V의 교훈 적용(동기화 직후 즉시 카드 개수 확인)**
- `index.html` 카드 추가 직후 바로 `grep -c` 대조(38=38), `tools/index.html`도 즉시 대조(38=38) — 세션V처럼 QA 단계까지 가서야 발견하는 실수 재발 안 함.
- `_includes/footer.html`(Tools 컬럼 2개 추가), `llms.txt`(Tools 섹션 2개 항목 추가) 정상 반영. New 배지를 두 신규 도구로 이동.

**5. QA(전수, 3가지 표준 규칙 적용)**
- Rule A(모든 스크립트 블록 전수 검사): 85개 파일 53개 스크립트 블록 전부 `node --check` 통과, 0건 오류.
- Rule C(no-print 스캔): 0건 — 도구A의 판별 비교표 섹션(`.tool-box` 앞에 위치)이 `no-print` 클래스를 갖고 있는지 특히 확인(과거 세션 T 직후 사고 패턴과 동일 구조라 재확인 필요했음) — 정상.
- YAML 85개 파일 통과, JSON-LD 0오류, FAQ 스키마-본문 1:1(도구A 6/6, 도구B 6/6), slug 중복 없음(37개), permalink 중복 없음(46개), 링크 재스캔 0건 깨짐.
- 최종 tool-card/checklist-card 개수 일치: 38=38=38, 8=8.
- div 균형: 신규 2개 + 역링크 수정한 기존 6개 파일 전부 짝 맞음.
- **날짜 계산 로직 node 검증**: 도구A(심각도 3단계 × 6단계, 배율 적용 후 날짜 단조증가 확인), 도구B(반응강도 3단계 × 7단계 역산, 예약일 기준 날짜 단조증가 확인) 전부 통과.

**오늘(세션 Y) 최종 페이지 수**: tools 38 + posts 37 + checklists 8 = 83페이지. 신규 순증 2개(`dog-car-anxiety-desensitization-planner`, `cat-carrier-training-planner`).

**다음 세션에서 확인할 것**:
- 오늘 만든 신규 2개의 GSC 노출/색인 여부 확인(최소 1-2주 필요).
- **별도 기획 대화에서 이어지는 배치 2(강아지 더위 안전 계산기 — 경쟁자 있음, 차별화 3개 조건부 / 수술 후 회복 체크리스트), 배치 3(시니어 이동성/다묘가정 자원배치/투약스케줄/크레이트 IATA 흡수 — 전부 "만들지 말지"부터 판단 필요)를 순서대로 진행할 것.**
- **신규 URL 11개(배치1~3, 세션Q~W) 전체의 GSC 색인 상태를 아직 종합 점검하지 못함** — 다음에 GSC 데이터가 첨부되면 최우선으로 확인할 것.
- Coverage 21개 미색인 이슈는 이번 세션에도 다루지 않음 — 계속 열린 상태.

---

### 세션 Z — 신규 배치 2: 강아지 더위 안전 계산기 + 수술 후 회복 체크리스트 (8/1, 세션 Y 직후)

**배경**: 신규 클러스터 배치 2. 도구 A는 경쟁자가 명확히 존재하는 상태에서 진행(사용자가 "차별화 3개를 못 살리면 중단해도 된다"고 미리 조건부 허용) → 3개 차별화 전부 구현 가능해 진행 확정. 체크리스트 B는 High 추론 강도 지시(수술 회복 정보).

**1. 신규 도구 A — `tools/dog-heat-safety-calculator.html`**

- ⚠️ **경쟁자 존재를 사전에 인지하고 진행**: calculatorsfordogs에 이미 heatstroke-risk-calculator 있음 확인. 아래 3개 차별화를 전부 구현했기에 진행.
- **차별화1 — 150룰 명시적 계산**: 기온(°F)+습도(%) 값을 결과에 그대로 노출(Justine Lee DVM 인용 방식으로 다수 소스에 확인됨).
- **차별화2 — 포장도로 7초 테스트를 별도 고정 섹션으로**: 계산과 무관하게 항상 노출, 노면이 공기보다 40-60°F 높을 수 있다는 구체 수치 포함.
- **차별화3 — 개체 위험요인 가중치**: 단두종(+30)/시니어(+15)/과체중(+15)/심장호흡기질환(+20)/격렬한활동(+15)을 기본 열지수에 가산하는 방식으로 구현 — 대부분 경쟁자는 품종만 보는 것과 차별화. node로 4개 시나리오(일반 vs 고위험 프로필 × 더운날 vs 선선한날) 검증: 동일 85°F/70%습도 조건에서 일반견은 "Danger"(160), 고위험견은 "Extreme Danger"(250)로 갈리는 것 확인 — 차별화가 실제로 등급을 바꾸는 것을 검증 완료.
- 안전등급 4단계(Safe/Caution/Danger/Extreme Danger) + 권장 최대 산책시간 + 대체활동 제안.
- 필수 콘텐츠 전부 반영(웹서치 확인): 열사병 조기신호(멈추지 않는 헐떡임/밝은 붉은 잇몸/끈적한 침/혀 스푼모양/보행거부), **응급대응은 처치 수준까지만**(그늘 이동/상온물 적용/즉시 병원, 체온 수치 목표 등 의학적 처치는 전혀 안 씀), 차 안 방치 위험(70°F에서 20분 내 100°F 초과), 쿨링베스트가 습한 날엔 역효과라는 점.
- FAQ 6개, 스키마+본문 1:1.

**2. 신규 체크리스트 B — `checklists/post-surgery-recovery-checklist.html`**

- ⚠️ **최상단 고정 경고**: "수의사의 퇴원 지시가 항상 이 체크리스트보다 우선합니다" — no-print 클래스 정상 적용 확인(과거 사고 패턴 재확인).
- 기존 `spay-neuter-recovery-timeline`(10-14일 스케일)과 명확히 다른 스케일(정형외과 8-12주)로 포지셔닝 — 자기잠식 방지, 상호 링크에서도 "다른 수술 유형" 명시.
- **핵심 문제해결 섹션**: "느낌이 나아졌다고 제한을 일찍 풀면 안 된다" — 개가 3-6주차에 정상처럼 행동하기 시작해도 뼈는 아직 안 붙었을 수 있다는 점을 별도 항목+FAQ로 강조(가장 흔한 재손상 원인, 웹서치로 다수 수의학 소스 확인).
- 구성: 수술 전 준비(8) → 첫 48시간(5) → 활동제한 기간(6) → 정상 복귀(3) = 총 22개 항목.
- 웹서치로 확인한 사실 전부 반영: 8-12주 엄격 제한, 활동 감소로 인한 사료 감량 필요(1/3~1/2), 다른 반려동물과 완전 분리, 미끄럼방지·계단차단, 절개부위 관찰포인트, 8/12주 재검 X선.
- ⚠️ 투약·용량 전혀 안 씀 — 작성 후 금지어(mg/kg, dosage of 등) 스캔 0건 확인.
- **작업 중 JSON-LD 스키마 오타 발견 및 수정**: FAQPage 블록의 `"@context"` 값이 `"schema.org"`로 잘못 입력돼 있던 것을 QA 검증 단계에서 발견, `"https://schema.org"`로 즉시 수정 후 재검증 통과 — 이번 세션 QA가 실제로 버그를 잡아낸 사례.
- 항목 22개, FAQ 6개, ItemList/FAQPage 스키마 개수 = 실제 개수 일치.

**3. 역링크(양방향, 지시사항 그대로 이행)**
- 체크리스트B ↔ `spay-neuter-recovery-timeline`(서로 "다른 수술 유형" 안내), ↔ `senior-pet-care-checklist`, → `dog-quality-of-life-calculator`(단방향, 지시대로).
- 도구A ↔ `dog-vet-visit-scheduler`, → `senior-pet-care-checklist`(단방향, 지시대로 — 시니어 더위 취약).
- 전부 실제 파일에서 링크 존재 확인 완료.

**4. 공통 파일 동기화 — 매 단계 즉시 카드 개수 검증(세션V~Y 패턴 유지)**
- `index.html` 카드 추가 직후 `grep -c` 대조(39=39), `tools/index.html` 즉시 대조(39=39), `checklists/index.html` 즉시 대조(9=9) — 전부 실수 없이 1회에 통과.
- `_includes/footer.html`(Tools/Checklists 컬럼 각 1개 추가), `llms.txt`(Tools/Checklists 섹션 각 1개 항목 추가) 정상 반영. New 배지 이동.

**5. QA(전수, 3가지 표준 규칙 적용)**
- Rule A(모든 스크립트 블록 전수 검사): 87개 파일 54개 스크립트 블록 전부 `node --check` 통과, 0건 오류.
- Rule C(no-print 스캔): 도구·체크리스트 양쪽 모두 0건 — 특히 체크리스트B의 상단 고정 경고박스(`.checklist-progress-wrap` 앞에 위치, 과거 사고와 동일 구조)를 별도 스캔 로직으로 재확인.
- YAML 87개 파일 통과, JSON-LD 0오류(스키마 오타 수정 후), FAQ 스키마-본문 1:1(도구A 6/6, 체크리스트B 6/6), slug 중복 없음(37개), permalink 중복 없음(48개), 링크 재스캔 0건 깨짐.
- 최종 tool-card/checklist-card 개수 일치: 39=39=39, 9=9.
- div 균형: 신규 2개 + 역링크 수정한 기존 3개 파일 전부 짝 맞음.
- 금지어 스캔(체크리스트B에 투약/용량 언급 없는지): 0건.
- **열지수 계산 로직 node 검증**: 4개 시나리오(일반/고위험 프로필 × 더운날/선선한날) 전부 등급 분류가 의도대로 작동함을 확인.

**오늘(세션 Z) 최종 페이지 수**: tools 39 + posts 37 + checklists 9 = 85페이지. 신규 순증 2개(`dog-heat-safety-calculator`, `post-surgery-recovery-checklist`).

**다음 세션에서 확인할 것**:
- 오늘 만든 신규 2개의 GSC 노출/색인 여부 확인(최소 1-2주 필요).
- **별도 기획 대화의 배치 3(시니어 이동성 홈감사/다묘가정 자원배치/투약스케줄트래커/크레이트 IATA 흡수 — 전부 "만들지 말지"부터 판단 필요, 크레이트 사이즈 계산기 자체는 이미 재확인된 레드오션이라 재조사 금지)를 진행할 것.**
- **신규 URL 13개(배치1~3 + 신규배치1~2)의 GSC 종합 점검이 계속 밀려있음** — 다음에 GSC 데이터가 첨부되면 최우선으로 확인할 것.
- Coverage 21개 미색인 이슈는 이번 세션에도 다루지 않음 — 계속 열린 상태.
