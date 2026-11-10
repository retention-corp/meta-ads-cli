"""Build a 17-slide PPTX from slides.md outline. Korean labels, dark theme.

Run inside .tools/.venv:
  source /Users/gyusupsim/Projects/tools/meta-ads-cli/routines/.tools/.venv/bin/activate
  python /Users/gyusupsim/Projects/tools/meta-ads-cli/routines/.tools/build_slides.py
"""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

DARK = RGBColor(0x0b, 0x0d, 0x10)
PANEL = RGBColor(0x14, 0x18, 0x1d)
BORDER = RGBColor(0x22, 0x28, 0x31)
TEXT = RGBColor(0xe6, 0xe9, 0xef)
MUTED = RGBColor(0x7c, 0x86, 0x94)
ACCENT = RGBColor(0x4f, 0x8c, 0xff)
POS = RGBColor(0x22, 0xc5, 0x5e)
WARN = RGBColor(0xf5, 0x9e, 0x0b)
NEG = RGBColor(0xef, 0x44, 0x44)


def fill(shape, color):
    shape.fill.solid()
    shape.fill.fore_color.rgb = color


def add_bg(slide, color=DARK):
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    fill(bg, color)
    bg.line.fill.background()
    return bg


def text_box(slide, x, y, w, h, text, *, size=24, bold=False, color=TEXT, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, mono=False):
    tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    p = tf.paragraphs[0]
    p.alignment = align
    r = p.add_run()
    r.text = text
    r.font.name = 'Menlo' if mono else 'Helvetica Neue'
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.color.rgb = color
    return tb


def card(slide, x, y, w, h, color=PANEL):
    sh = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h)
    fill(sh, color)
    sh.line.color.rgb = BORDER
    sh.line.width = Pt(1)
    return sh


def slack_msg_slide(title_text, lines):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    add_bg(s)
    text_box(s, Inches(0.5), Inches(0.3), Inches(12.3), Inches(0.6), title_text, size=28, bold=True)
    card(s, Inches(1.0), Inches(1.4), Inches(11.3), Inches(5.6))
    tb = s.shapes.add_textbox(Inches(1.4), Inches(1.7), Inches(10.5), Inches(5.0))
    tf = tb.text_frame
    tf.word_wrap = True
    for i, (style, txt) in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        p.space_after = Pt(8)
        r = p.add_run()
        r.text = txt
        r.font.name = 'Menlo'
        r.font.size = Pt(15) if style == 'body' else Pt(18)
        r.font.bold = (style == 'header')
        r.font.color.rgb = TEXT if style != 'mute' else MUTED


# ---------- 17 slides ----------

# 1: 후킹
s = prs.slides.add_slide(prs.slide_layouts[6]); add_bg(s)
text_box(s, Inches(0.5), Inches(2.5), Inches(12.3), Inches(2),
         "똑똑하고 게으른 사람이\n가장 멀리 간다", size=72, bold=True, align=PP_ALIGN.CENTER)
text_box(s, Inches(0.5), Inches(5.6), Inches(12.3), Inches(0.6),
         "마케터를 똑똑하고 게으르게 만드는 시스템", size=22, color=MUTED, align=PP_ALIGN.CENTER)

# 2: 4분할 placeholder
s = prs.slides.add_slide(prs.slide_layouts[6]); add_bg(s)
text_box(s, Inches(0.5), Inches(0.3), Inches(12.3), Inches(0.6),
         "매일 자동으로 도는 시스템", size=28, bold=True)
quads = [("Slack", "#ads-routines · 4 routines 알림"),
         ("Terminal", "Claude routines fired"),
         ("Dashboard", "dashboard.html 자동 갱신"),
         ("Vault", "creative_plan_*.json")]
for i, (t, sub) in enumerate(quads):
    col, row = i % 2, i // 2
    x, y = Inches(0.5 + col * 6.4), Inches(1.2 + row * 2.95)
    card(s, x, y, Inches(6.0), Inches(2.7))
    text_box(s, x + Inches(0.3), y + Inches(0.25), Inches(5.5), Inches(0.5), t, size=18, bold=True, color=ACCENT)
    text_box(s, x + Inches(0.3), y + Inches(1.2), Inches(5.5), Inches(1.2), sub, size=14, color=MUTED)

# 3: 학습 공동체
s = prs.slides.add_slide(prs.slide_layouts[6]); add_bg(s)
text_box(s, Inches(0.5), Inches(2.5), Inches(12.3), Inches(1.5),
         "이 영상은 강의가 아니에요", size=64, bold=True, align=PP_ALIGN.CENTER)
text_box(s, Inches(0.5), Inches(4.5), Inches(12.3), Inches(0.6),
         "학습 공동체를 같이 만들어요", size=22, color=MUTED, align=PP_ALIGN.CENTER)
text_box(s, Inches(0.5), Inches(5.6), Inches(12.3), Inches(0.5),
         "코액티브 얼라이언스 · 다오랩 학습 커뮤니티 · 부트캠프 5개월차 builder mode", size=14, color=MUTED, align=PP_ALIGN.CENTER)

# 4: UI vs CLI vs MCP
s = prs.slides.add_slide(prs.slide_layouts[6]); add_bg(s)
text_box(s, Inches(0.5), Inches(0.3), Inches(12.3), Inches(0.7),
         "UI vs CLI vs MCP — 도구별 역할", size=28, bold=True)
header = ["", "Ads Manager (UI)", "Ads CLI", "Ads MCP"]
rows = [
    ("무엇", "웹 + 마우스", "터미널 + 명령", "에이전트 + 자연어"),
    ("속도", "가장 느림", "가장 빠름", "빠름"),
    ("반복", "매번 클릭", "한 번 짜면 영원", "매번 자연어"),
    ("재현성", "사람마다 다름", "100% 동일", "비결정적"),
    ("장점", "학습 / 탐색", "자동화", "ad-hoc 분석"),
    ("진입 장벽", "낮음 (누구나)", "중간 (엔지니어)", "낮음 (자연어)"),
]
col_w = [Inches(2.0), Inches(3.4), Inches(3.4), Inches(3.4)]
x0 = Inches(0.5); y = Inches(1.3); xx = x0
for i, h in enumerate(header):
    text_box(s, xx, y, col_w[i], Inches(0.5), h, size=16, bold=True, color=ACCENT if i > 0 else MUTED)
    xx += col_w[i]
y += Inches(0.6)
for r in rows:
    xx = x0
    for i, val in enumerate(r):
        text_box(s, xx, y, col_w[i], Inches(0.5), val, size=14, color=TEXT if i > 0 else MUTED)
        xx += col_w[i]
    y += Inches(0.55)

# 5: OpenClaw 한 줄
s = prs.slides.add_slide(prs.slide_layouts[6]); add_bg(s)
text_box(s, Inches(0.5), Inches(1.0), Inches(12.3), Inches(0.7),
         "Claude Code 안 쓰셔도 — OpenClaw / Cursor / ChatGPT 다 됨",
         size=22, bold=True, color=MUTED, align=PP_ALIGN.CENTER)
card(s, Inches(0.8), Inches(2.8), Inches(11.7), Inches(2.0))
text_box(s, Inches(1.0), Inches(3.4), Inches(11.3), Inches(1.0),
         'openclaw mcp set meta-ads \'{"type":"http","url":"https://mcp.facebook.com/ads"}\'',
         size=16, color=ACCENT, align=PP_ALIGN.CENTER, mono=True)
text_box(s, Inches(0.5), Inches(5.6), Inches(12.3), Inches(0.6),
         "MCP는 표준 — 명령어 한 줄만 다름", size=18, color=MUTED, align=PP_ALIGN.CENTER)

# 6: 시스템 아키텍처 (use generated PNG)
s = prs.slides.add_slide(prs.slide_layouts[6]); add_bg(s)
text_box(s, Inches(0.5), Inches(0.3), Inches(12.3), Inches(0.6), "시스템 아키텍처", size=28, bold=True)
import os
arch = '/Users/gyusupsim/Projects/tools/meta-ads-cli/routines/assets/architecture.png'
if os.path.exists(arch):
    s.shapes.add_picture(arch, Inches(2.6), Inches(1.0), height=Inches(6.2))
else:
    text_box(s, Inches(0.5), Inches(3.5), Inches(12.3), Inches(0.6),
             "[architecture.png missing]", size=18, color=NEG, align=PP_ALIGN.CENTER)

# 7: Claude Routines 등록
s = prs.slides.add_slide(prs.slide_layouts[6]); add_bg(s)
text_box(s, Inches(0.5), Inches(0.3), Inches(12.3), Inches(0.6),
         "Claude Routines 등록 화면", size=28, bold=True)
text_box(s, Inches(0.5), Inches(1.0), Inches(12.3), Inches(0.5),
         "https://claude.ai/code/routines", size=16, color=MUTED)
routines = [
    ("🌅 meta-ads-morning-signal-daily", "매일 KST 8:03"),
    ("🚨 meta-ads-fatigue-scan-daily", "매일 KST 0:02"),
    ("📊 meta-ads-incrementality-weekly", "매주 월 KST 9:07"),
    ("🎨 meta-ads-creative-flywheel-weekly", "매주 월 KST 10:12"),
]
for i, (name, when) in enumerate(routines):
    y = Inches(2.0 + i * 1.1)
    card(s, Inches(1.5), y, Inches(10.3), Inches(0.95))
    text_box(s, Inches(1.8), y + Inches(0.1), Inches(7.5), Inches(0.5), name, size=18, bold=True)
    text_box(s, Inches(9.0), y + Inches(0.2), Inches(2.7), Inches(0.5), when, size=14, color=ACCENT)

# 8: Routine 1 Slack
slack_msg_slide("Routine 1 — 아침 시그널 브리핑 (Slack)", [
    ('header', '🌅 아침 시그널 브리핑 — get.ship.done-campaign'),
    ('mute', 'baseline 30일 일평균 $41.92'),
    ('body', ''),
    ('body', '✅ 오디언스 연령 누수 — 18-24세 3.5% (baseline 3.9%)'),
    ('body', '✅ Placement 분포 — 인스타 91% / FB 9% (정상)'),
    ('body', '✅ 일일 spend — 어제 $51.95 (z=+0.68σ)'),
])

# 9: Fatigue 시그널
s = prs.slides.add_slide(prs.slide_layouts[6]); add_bg(s)
text_box(s, Inches(0.5), Inches(0.3), Inches(12.3), Inches(0.6),
         "Fatigue 시그널 4종 — Routine 2", size=28, bold=True)
sigs = [
    ("frequency", "≥ 2.0", "≥ 2.5"),
    ("CTR decay (오늘 / 7일전)", "< 0.85", "< 0.75"),
    ("CPM inflation (오늘 / 7일전)", "> 1.20", "> 1.40"),
    ("reach 일평균 성장률", "—", "< 5% (saturation)"),
]
text_box(s, Inches(0.8), Inches(1.5), Inches(5.5), Inches(0.5), "시그널", size=16, bold=True, color=MUTED)
text_box(s, Inches(7.0), Inches(1.5), Inches(2.5), Inches(0.5), "경고", size=16, bold=True, color=WARN)
text_box(s, Inches(10.0), Inches(1.5), Inches(2.5), Inches(0.5), "Critical", size=16, bold=True, color=NEG)
for i, (sig, w, c) in enumerate(sigs):
    y = Inches(2.2 + i * 0.95)
    text_box(s, Inches(0.8), y, Inches(5.5), Inches(0.5), sig, size=15)
    text_box(s, Inches(7.0), y, Inches(2.5), Inches(0.5), w, size=15, color=WARN)
    text_box(s, Inches(10.0), y, Inches(2.5), Inches(0.5), c, size=15, color=NEG)

# 10: Routine 2 Slack
slack_msg_slide("Routine 2 — Fatigue + HITL 메뉴 (Slack)", [
    ('header', '🚨 Fatigue 경고 — 1개 광고 검토 필요'),
    ('body', ''),
    ('body', '• meta-reel-compilation-G-v5 (주의)'),
    ('body', '  freq 1.14, CTR 0%→0%, CPM $35→$17'),
    ('body', '    - A. 광고 일시정지 (오디언스 saturate)'),
    ('body', '      `meta ads ad update 120241700755610025 --status PAUSED`'),
    ('body', '    - Skip — false positive 판단 시 오늘 건너뛰기'),
    ('body', ''),
    ('mute', '※ 자동 실행 안 함. 사람이 paste 후 직접 실행 (HITL).'),
])

# 11: Attribution Setting
s = prs.slides.add_slide(prs.slide_layouts[6]); add_bg(s)
text_box(s, Inches(0.5), Inches(0.3), Inches(12.3), Inches(0.6),
         "Attribution Setting Gap — Routine 3", size=28, bold=True)
card(s, Inches(2.0), Inches(1.8), Inches(9.3), Inches(1.4))
text_box(s, Inches(2.3), Inches(2.0), Inches(8.7), Inches(0.5),
         "7d_click + 1d_view", size=22, bold=True, color=ACCENT)
text_box(s, Inches(2.3), Inches(2.6), Inches(8.7), Inches(0.4),
         "전통적 default — 많은 마케터가 여전히 사용", size=14, color=MUTED)
text_box(s, Inches(0.5), Inches(3.4), Inches(12.3), Inches(0.5),
         "↕  gap (보고 방식 차이)", size=20, color=WARN, align=PP_ALIGN.CENTER)
card(s, Inches(2.0), Inches(4.1), Inches(9.3), Inches(1.4))
text_box(s, Inches(2.3), Inches(4.3), Inches(8.7), Inches(0.5), "incremental", size=22, bold=True, color=POS)
text_box(s, Inches(2.3), Inches(4.9), Inches(8.7), Inches(0.4),
         "Meta 권장 setting — 진짜 광고 기여도", size=14, color=MUTED)
text_box(s, Inches(0.5), Inches(6.0), Inches(12.3), Inches(0.6),
         "두 setting 차이 크면 = attribution setting 검토 권장 신호", size=16, color=MUTED, align=PP_ALIGN.CENTER)
text_box(s, Inches(0.5), Inches(6.6), Inches(12.3), Inches(0.5),
         "※ 진짜 incrementality는 Conversion Lift 연구 필요", size=12, color=MUTED, align=PP_ALIGN.CENTER)

# 12: Routine 3 Slack
slack_msg_slide("Routine 3 — Incrementality Gap (Slack)", [
    ('header', '📊 주간 Incrementality Gap — 최근 30일'),
    ('mute', 'attribution setting 비교. 진짜 incrementality는 Conversion Lift 연구 필요.'),
    ('body', ''),
    ('body', '캠페인: get.ship.done-campaign'),
    ('body', '• 7d_c + 1d_v ROAS: 7.46배 (전통적 리포팅)'),
    ('body', '• incremental ROAS: 9.72배 (Meta 권장 setting)'),
    ('body', '• gap ratio: 0.77 → ✅ true_winner'),
    ('body', ''),
    ('body', '해석: 두 setting 차이가 크지 않음. click-driven 가능성 높음.'),
    ('body', 'attribution setting 검토 권장.'),
])

# 13: Admiral 5단계
s = prs.slides.add_slide(prs.slide_layouts[6]); add_bg(s)
text_box(s, Inches(0.5), Inches(0.3), Inches(12.3), Inches(0.6),
         "Admiral Creative Testing Flywheel", size=28, bold=True)
steps = [
    ("1", "Hypothesis", "가설 설계"),
    ("2", "AI Production", "100+ variant/월"),
    ("3", "Balanced Deployment", "균형 노출 강제"),
    ("4", "Signal Interpretation", "하위 전환 기준"),
    ("5", "Brief Development", "우승 요소 → 다음 가설"),
]
for i, (n, t, sub) in enumerate(steps):
    x = Inches(0.4 + i * 2.6); y = Inches(2.5)
    card(s, x, y, Inches(2.4), Inches(2.5))
    text_box(s, x, y + Inches(0.2), Inches(2.4), Inches(0.7), n, size=36, bold=True, color=ACCENT, align=PP_ALIGN.CENTER)
    text_box(s, x + Inches(0.15), y + Inches(1.0), Inches(2.1), Inches(0.6), t, size=14, bold=True, align=PP_ALIGN.CENTER)
    text_box(s, x + Inches(0.15), y + Inches(1.6), Inches(2.1), Inches(0.8), sub, size=11, color=MUTED, align=PP_ALIGN.CENTER)
text_box(s, Inches(0.5), Inches(5.5), Inches(12.3), Inches(0.5),
         "각 사이클이 다음 사이클의 가설을 만든다 — compounding", size=16, color=MUTED, align=PP_ALIGN.CENTER)

# 14: Admiral 핵심 4
s = prs.slides.add_slide(prs.slide_layouts[6]); add_bg(s)
text_box(s, Inches(0.5), Inches(0.3), Inches(12.3), Inches(0.6),
         "Admiral 핵심 원칙 4개", size=28, bold=True)
principles = [
    ("1", "한 번에 한 변수만", "훅/바디/CTA 동시 변경 금지\n(뭐 때문에 이긴지 못 알게 됨)"),
    ("2", "1,000 imp 도달 전 판정 금지", "5,000+ 권장\n(노이즈에 끌려가기 방지)"),
    ("3", "하위 전환 우선, CTR은 보조", "purchase CVR > CTR\n(잘못된 사람한테 보여주는 광고 거름)"),
    ("4", "Advantage+ 편향 차단", "초기 leader 노출 몰빵 방지\n(테스트 구간엔 균형 노출)"),
]
for i, (n, t, sub) in enumerate(principles):
    col, row = i % 2, i // 2
    x = Inches(0.5 + col * 6.3); y = Inches(1.4 + row * 2.85)
    card(s, x, y, Inches(6.1), Inches(2.7))
    text_box(s, x + Inches(0.3), y + Inches(0.2), Inches(0.8), Inches(0.7), n, size=32, bold=True, color=ACCENT)
    text_box(s, x + Inches(1.3), y + Inches(0.3), Inches(4.6), Inches(0.7), t, size=18, bold=True)
    text_box(s, x + Inches(0.3), y + Inches(1.3), Inches(5.5), Inches(1.3), sub, size=13, color=MUTED)

# 15: Routine 4 Slack
slack_msg_slide("Routine 4 — Creative Flywheel (Slack)", [
    ('header', '🎨 주간 Creative Flywheel — Admiral framework'),
    ('body', ''),
    ('body', '테스트 자격 (imp ≥ 1,000): 3개'),
    ('body', '⏳ Still learning (imp < 1,000): 2개'),
    ('body', ''),
    ('body', '✅ Winner candidates (하위 전환 상위 30%):'),
    ('body', '  • ad_postit_winner_260427 — purchase CVR 4.2%, imp 12,300'),
    ('body', '    핵심: 손글씨 hook + 검은 배경 + 12초 길이'),
    ('body', ''),
    ('body', '⛔ Loser candidates:'),
    ('body', '  • jinny-capcut-260420 — purchase CVR 1.1%, imp 8,400'),
    ('body', ''),
    ('body', '다음 사이클 가설:'),
    ('body', '검은 배경 + 손글씨 hook이 잔존. 다음 batch에서 변형 4개 추가.'),
])

# 16: 글로벌 마스터 3명
s = prs.slides.add_slide(prs.slide_layouts[6]); add_bg(s)
text_box(s, Inches(0.5), Inches(0.3), Inches(12.3), Inches(0.6),
         "매일 보는 글로벌 마스터 3명", size=28, bold=True)
masters = [
    ("Thomas Petit", "@thomasbcn", "signal engineering의 창시자\n광고 시그널 설계 매주 글"),
    ("Marcus Burke", "@MrMarcusBurke", "Meta 광고의 살아있는 백과사전\n알고리즘 / attribution / beta"),
    ("Admiral Media", "admiral.media", "€500M+ ad spend 운영\nAI Creative Factory 만든 곳"),
]
for i, (name, handle, desc) in enumerate(masters):
    x = Inches(0.5 + i * 4.3); y = Inches(1.5)
    card(s, x, y, Inches(4.1), Inches(5.0))
    text_box(s, x + Inches(0.3), y + Inches(0.5), Inches(3.5), Inches(0.7), name, size=22, bold=True, align=PP_ALIGN.CENTER)
    text_box(s, x + Inches(0.3), y + Inches(1.4), Inches(3.5), Inches(0.5), handle, size=14, color=ACCENT, align=PP_ALIGN.CENTER)
    text_box(s, x + Inches(0.3), y + Inches(2.5), Inches(3.5), Inches(2.3), desc, size=14, color=MUTED, align=PP_ALIGN.CENTER)

# 17: 마무리
s = prs.slides.add_slide(prs.slide_layouts[6]); add_bg(s)
text_box(s, Inches(0.5), Inches(2.0), Inches(12.3), Inches(2),
         "직접 만들어보세요", size=80, bold=True, align=PP_ALIGN.CENTER)
text_box(s, Inches(0.5), Inches(4.8), Inches(12.3), Inches(0.7),
         "막히면 댓글로 — 만들면 결과 공유 — 학습 공동체 같이",
         size=20, color=MUTED, align=PP_ALIGN.CENTER)
text_box(s, Inches(0.5), Inches(6.0), Inches(12.3), Inches(0.5),
         "좋아요 / 구독", size=14, color=ACCENT, align=PP_ALIGN.CENTER)

import os
out = '/Users/gyusupsim/Projects/tools/meta-ads-cli/routines/assets/slides.pptx'
os.makedirs(os.path.dirname(out), exist_ok=True)
prs.save(out)
print('saved:', out, '·', os.path.getsize(out), 'bytes')
print('slide count:', len(prs.slides._element))
