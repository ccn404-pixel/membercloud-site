// Shared helpers for the MemberCloud Pages Functions (same origin as the site, so no CORS).
import { KB, SYSTEM } from '../../chat/kb.js';

export const json = (o, status = 200) => new Response(JSON.stringify(o), { status, headers: { 'content-type': 'application/json', 'cache-control': 'no-store' } });

export const configured = env => ({
  chat: !!(env.PROVIDER === 'openai' ? env.OPENAI_API_KEY : env.ANTHROPIC_API_KEY),
  email: !!(env.RESEND_API_KEY && env.FROM_EMAIL),
});

// Reject cross-site posts: when the browser sends an Origin it must match this host.
export function sameOrigin(req) {
  const o = req.headers.get('Origin');
  if (!o) return true;
  try { return new URL(o).host === new URL(req.url).host; } catch (e) { return false; }
}

const hits = new Map(); // per-isolate soft limit; add a Cloudflare rate limiting rule for a hard one
export function limited(req, max) {
  const ip = req.headers.get('CF-Connecting-IP') || 'x', now = Date.now();
  const a = (hits.get(ip) || []).filter(t => now - t < 60000);
  a.push(now); hits.set(ip, a);
  return a.length > max;
}

export async function reply(env, msgs) {
  if (env.PROVIDER === 'openai') {
    const r = await fetch('https://api.openai.com/v1/chat/completions', {
      method: 'POST',
      headers: { 'content-type': 'application/json', Authorization: `Bearer ${env.OPENAI_API_KEY}` },
      body: JSON.stringify({ model: env.MODEL || 'gpt-4o-mini', max_tokens: 300, temperature: 0.2, messages: [{ role: 'system', content: SYSTEM + KB }, ...msgs] }),
    });
    if (!r.ok) return null;
    const d = await r.json();
    return (d.choices && d.choices[0] && d.choices[0].message && d.choices[0].message.content) || '';
  }
  const r = await fetch('https://api.anthropic.com/v1/messages', {
    method: 'POST',
    headers: { 'content-type': 'application/json', 'x-api-key': env.ANTHROPIC_API_KEY, 'anthropic-version': '2023-06-01' },
    body: JSON.stringify({ model: env.MODEL || 'claude-haiku-5-5', max_tokens: 300, system: SYSTEM + KB, messages: msgs }),
  });
  if (!r.ok) return null;
  const d = await r.json();
  return ((d.content || []).find(c => c.type === 'text') || {}).text || '';
}

export async function sendMail(env, { subject, text, replyTo }) {
  const r = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: { 'content-type': 'application/json', Authorization: `Bearer ${env.RESEND_API_KEY}` },
    body: JSON.stringify({ from: env.FROM_EMAIL, to: [env.TO_EMAIL || 'info@member-cloud.com'], reply_to: replyTo, subject, text }),
  });
  return r.ok;
}
