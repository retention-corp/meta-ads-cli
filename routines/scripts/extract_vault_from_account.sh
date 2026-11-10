#!/usr/bin/env bash
# Pull active ad creatives from the live account and populate routines/vault/.
#
# - Downloads real ad images to vault/hooks/ (one per active creative)
# - Extracts CTA types to vault/ctas/
# - Skips body text (CLI does not currently expose creative body via
#   `creative get`; falls back to stored body templates if vault/bodies/
#   is empty after this script runs)
# - Writes vault/manifest.json with the full per-ad creative metadata for
#   reference (image_hash, video_id, link, etc.)
#
# Run this whenever you want the demo vault to reflect what's actually
# running in the account.
set -euo pipefail

ROUTINES="/Users/gyusupsim/Projects/tools/meta-ads-cli/routines"
CLI_VENV="/Users/gyusupsim/Projects/tools/meta-ads-cli/meta-ads-official-cli/.venv"
CLI_CWD="/Users/gyusupsim/Projects/tools/meta-ads-cli/meta-ads-official-cli"
VAULT="$ROUTINES/vault"

source "$CLI_VENV/bin/activate"
cd "$CLI_CWD"

mkdir -p "$VAULT/hooks" "$VAULT/bodies" "$VAULT/ctas" "$VAULT/queue"

# Discover and dump
node --input-type=module -e "
import { execSync } from 'child_process';
import fs from 'fs';
const META = '$CLI_VENV/bin/meta';
const VAULT = '$VAULT';
const run = c => execSync(c, {encoding:'utf8', cwd:'$CLI_CWD'});
const ads = JSON.parse(run(\`\${META} --output json ads ad list --limit 200\`));
const active = ads.filter(a => a.effective_status === 'ACTIVE');
const slug = s => String(s||'unknown').toLowerCase().replace(/[^a-z0-9가-힣_-]+/g,'_').replace(/^_|_$/g,'').slice(0,40);
const xCid = ad => (String(ad.creative||'').match(/\"id\":\\s*\"([0-9]+)\"/)||[])[1];
const manifest = [];
for (const ad of active) {
  const crid = xCid(ad);
  if (!crid) continue;
  let cr;
  try { cr = JSON.parse(run(\`\${META} --output json ads creative get \${crid}\`))[0]; } catch { continue; }
  const ossRaw = String(cr.object_story_spec || '');
  const m = ossRaw.match(/\\{[\\s\\S]*\\}/);
  let oss = {};
  try { if (m) oss = JSON.parse(m[0]); } catch {}
  const data = oss.video_data || oss.link_data || oss.photo_data || {};
  manifest.push({
    ad_id: ad.id, ad_name: ad.name, creative_id: crid,
    cta: (data.call_to_action||{}).type || null,
    link: ((data.call_to_action||{}).value||{}).link || null,
    image_hash: data.image_hash || null,
    image_url: data.image_url || cr.thumbnail_url || null,
    video_id: data.video_id || null,
    page_id: oss.page_id, instagram_user_id: oss.instagram_user_id,
    creative_name: cr.name,
  });
}
fs.writeFileSync(VAULT + '/manifest.json', JSON.stringify(manifest, null, 2));
console.log('manifest:', manifest.length, 'creatives');
const ctas = new Set();
for (const c of manifest) {
  if (!c.image_url || !c.image_hash) continue;
  try {
    const res = await fetch(c.image_url, { headers: { 'User-Agent':'Mozilla/5.0' }});
    if (!res.ok) continue;
    const buf = Buffer.from(await res.arrayBuffer());
    const ct = res.headers.get('content-type')||'';
    const ext = ct.includes('png') ? 'png' : ct.includes('webp') ? 'webp' : 'jpg';
    const fname = slug(c.ad_name)+'_'+c.image_hash.slice(0,8)+'.'+ext;
    fs.writeFileSync(VAULT+'/hooks/'+fname, buf);
    if (c.cta) ctas.add(c.cta);
  } catch {}
}
for (const cta of ctas) fs.writeFileSync(VAULT+'/ctas/'+cta, '');
console.log('hooks:', fs.readdirSync(VAULT+'/hooks').length, '· ctas:', [...ctas]);
"

echo "✅ vault refreshed from live account."
echo "   hooks:  $(ls $VAULT/hooks | wc -l) files"
echo "   bodies: $(ls $VAULT/bodies | wc -l) files (writes preserved if any)"
echo "   ctas:   $(ls $VAULT/ctas | wc -l) entries"
