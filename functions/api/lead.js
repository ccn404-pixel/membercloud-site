// Demo requests and chat hand-offs: emailed to TO_EMAIL (info@member-cloud.com) through Resend.
import { json, configured, sameOrigin, limited, sendMail } from '../lib/shared.js';

const clean = (v, n) => String(v == null ? '' : v).replace(/[\u0000-\u001f\u007f]+/g, ' ').trim().slice(0, n);

export async function onRequestPost({ request, env }) {
  if (!sameOrigin(request)) return json({ error: 'forbidden' }, 403);
  const b = await request.json().catch(() => null) || {};
  if (b.website) return json({ ok: true }); // honeypot field: bots fill it, people never see it
  if (!configured(env).email) return json({ error: 'not_configured' }, 503);
  if (limited(request, 4)) return json({ error: 'slow_down' }, 429);

  const name = clean(b.name, 120), email = clean(b.email, 200), kind = b.kind === 'chat' ? 'chat' : 'demo';
  if (!name || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) return json({ error: 'invalid' }, 400);
  const rows = [['Name', name], ['Email', email], ['Business', clean(b.business, 160)], ['Type', clean(b.type, 40)], ['Phone', clean(b.phone, 40)],
    ['Preferred time', clean(b.slot, 80)], ['Page', clean(b.page, 200)]].filter(r => r[1]).map(r => `${r[0]}: ${r[1]}`).join('\n');
  const notes = String(b.message || b.notes || '').slice(0, 3000).trim();
  let text = `${kind === 'chat' ? 'Message from the website chat' : 'New demo request from the website'}\n\n${rows}\n`;
  if (notes) text += `\n${kind === 'chat' ? 'Message' : 'Notes'}:\n${notes}\n`;
  if (kind === 'chat') {
    const t = (Array.isArray(b.transcript) ? b.transcript : []).slice(-20).map(m => `${m.role === 'user' ? 'Visitor' : 'Assistant'}: ${clean(m.content, 600)}`).join('\n');
    text += `\n--- Chat so far (AI-assisted replies) ---\n${t || '(none)'}\n`;
  }
  const ok = await sendMail(env, { subject: kind === 'chat' ? `Website chat: ${name}` : `Demo request: ${clean(b.business, 80) || name}`, text, replyTo: email });
  return ok ? json({ ok: true }) : json({ error: 'send_failed' }, 502);
}
