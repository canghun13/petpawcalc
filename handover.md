# PetPawCalc 인수인계 문서

최종 갱신: 2026-07-12
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
tools/                # 계산기 툴 19개 (개별 .html, front matter로 title/description/permalink 지정)
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

### 계산기 툴 19개 (tools/)
연령: dog-age, cat-age
체중: dog-weight, cat-weight, pet-weight(통합)
발정/임신: dog-heat-cycle, cat-heat-cycle, dog-pregnancy, cat-pregnancy
비용: annual-pet-cost, pet-insurance-cost-estimator, pet-food-calorie
건강/방문: dog-vet-visit-scheduler, cat-vet-visit-scheduler, dog-quality-of-life(Paw Score)
백신 (신규): dog-vaccination-schedule-calculator, cat-vaccination-schedule-calculator
수술 비용 (신규): spay-neuter-cost-calculator, dental-cleaning-cost-calculator

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

### 세션 F — 2차 보강 (7/12, 이번 세션)
GSC 7/12 데이터 확인 → 신규 콘텐츠 필요성 웹 검색으로 검증 → **"Dog Pregnancy Signs" 클러스터(13개 쿼리 변형)는 이미 강자들(Pets4Homes, Daily Paws, PetPace)이 있는 레드오션이라 새 글 대신 기존 `how-to-tell-if-dog-is-pregnant` 포스트 보강으로 처리** (자기잠식 방지). `dog-weight-calculator`도 adult 체중 체크 기능은 이미 있었는데 FAQ가 puppy 위주였던 걸 보강.

---

## 4. GSC 색인 현황 (7/12 기준)

- **심각한 문제**: "발견됨-미색인" 38개, "크롤링됨-미색인" 3개, "리디렉션 포함 페이지" 3개(→ **사용자 지시로 무시**) — 이 숫자들은 여러 세션째 거의 변화 없음. Coverage 리포트 자체가 갱신 지연이 있는 것으로 보이며, **실제 상태는 Performance 리포트(쿼리/페이지별 노출)가 더 정확한 지표**로 판단하고 있음.
- Performance 리포트 기준 노출 있는 페이지는 세션 C 이후 9개 → 21개 → 23개로 꾸준히 증가 중. 실제로 색인이 진행되고 있다는 신호.
- 사이트 전체가 아직 authority가 낮은 신생 사이트라 대부분의 쿼리가 30~90위권. Coverage 리포트의 "발견됨-미색인" 38개는 Google의 크롤 예산 배정이 아직 낮아서이며, 이건 코드로 해결 불가 — 시간 + 백링크(사용자가 별도 디렉토리 등록 진행 중) + 지속적 콘텐츠 보강으로만 개선됨.
- **"petcalculators.xyz", 헝가리어/네덜란드어 등 비영어권 쿼리는 의도적으로 무시** — 온페이지로 해결 안 되는 authority/언어 문제.

### 순위 근접 페이지 (다음 라운드에서 우선 재확인할 것)
- `dog-quality-of-life-assessment` (포스트): 4.33위 — 이미 상위권, 유지만 확인
- `how-often-vet-visits-dog-cost-by-age`: 5.8위 — 상위권 유지 확인
- `how-much-should-senior-dog-eat`: 14.1위, 노출 148개(가장 많음) — CTR 개선 여지
- `dog-age-calculator`, `cat-age-calculator`, `dog-vaccination-schedule-calculator`: 11~15위권 — 안정적, 계속 지켜볼 것
- `dog-weight-calculator`: 66위 → 최근 노출 22개로 신규 진입, 이번 세션에서 adult 체중 FAQ 보강함 — 다음 데이터에서 효과 확인 필요
- `how-to-tell-if-dog-is-pregnant`: 77위, 노출 22개로 신규 진입 — 이번 세션에서 FAQ 보강함, 효과 확인 필요

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

- 이번 세션에서 보강한 `how-to-tell-if-dog-is-pregnant`, `dog-weight-calculator`의 순위 변화를 다음 GSC 데이터로 확인
- Spay/Neuter, Dental Cleaning 계산기(7/10 생성)는 아직 GSC Performance에 노출 데이터 없음(너무 최근) — 다음 데이터에서 첫 노출 여부 확인
- `pet-euthanasia-cost-and-what-to-expect` 포스트는 영어 톤 검수를 사용자가 직접 하지 못한 상태("나 영어는 잘 몰라서 톤은 모르는데") — 필요시 재검토 여지 있음
- Coverage 리포트의 "발견됨-미색인 38개"가 다음 데이터에서도 그대로면, Performance 데이터만으로는 안 보이는 다른 근본 원인이 있을 수 있으니 재점검 필요
