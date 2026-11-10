#!/usr/bin/env bash
# 영상용 4분할 화면 자동 배치 (macOS).
# 1080p (1920×1080) 화면 기준. 다른 해상도면 osascript 안의 좌표 조정.
# 사용:
#   bash arrange_4pane.sh
# 듀얼 모니터 사용자: 메인 모니터에 4분할 (스크린 공유), 보조 모니터에 텔레프롬프터.

osascript <<'AS'
-- 화면 해상도 가져오기
tell application "Finder"
  set screenBounds to bounds of window of desktop
end tell
set screenW to item 3 of screenBounds
set screenH to item 4 of screenBounds
set halfW to screenW / 2
set halfH to screenH / 2

-- 좌상: Slack
tell application "Slack" to activate
delay 0.4
tell application "System Events" to tell process "Slack"
  set position of window 1 to {0, 25}
  set size of window 1 to {halfW, halfH}
end tell

-- 우상: Terminal (Ghostty)
tell application "Ghostty" to activate
delay 0.4
tell application "System Events" to tell process "Ghostty"
  set position of window 1 to {halfW, 25}
  set size of window 1 to {halfW, halfH}
end tell

-- 좌하: 브라우저 (dashboard.html)
do shell script "open -a 'Google Chrome' /Users/gyusupsim/Projects/tools/meta-ads-cli/routines/reports/dashboard.html"
delay 0.8
tell application "System Events" to tell process "Google Chrome"
  set position of window 1 to {0, halfH + 25}
  set size of window 1 to {halfW, halfH}
end tell

-- 우하: Finder (vault 폴더)
tell application "Finder"
  open folder "vault" of folder "routines" of folder "meta-ads-cli" of folder "tools" of folder "Projects" of folder "gyusupsim" of folder "Users" of startup disk
  activate
end tell
delay 0.4
tell application "System Events" to tell process "Finder"
  set position of window 1 to {halfW, halfH + 25}
  set size of window 1 to {halfW, halfH}
end tell

return "4분할 배치 완료"
AS
