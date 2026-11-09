import { json, configured, sameOrigin, limited, reply } from '../lib/shared.js';

export async function onRequestPost({ request, env }) {
  if (!sameOrigin(request)) return json({ error: 'forbidden' }, 403);
  if (!configured(env).chat) return json({ error: 'not_configured' }, 503);
  if (limited(request, 12)) return json({ error: 'slow_down' }, 429);
  const body = await request.json().catch(() => null);
  const msgs = (body && Array.isArray(body.messages) ? body.messages : []).slice(-12)
    .filter(m => (m.role === 'user' || m.role === 'assistant') && typeof m.content === 'string')
    .map(m => ({ role: m.role, content: m.content.slice(0, 1200) }));
  if (!msgs.length || msgs[msgs.length - 1].role !== 'user') return json({ error: 'bad_request' }, 400);
  let text = await reply(env, msgs);
  if (text === null) return json({ error: 'upstream' }, 502);
  const handoff = text.includes('[[HANDOFF]]');
  text = text.replace('[[HANDOFF]]', '').trim();
  return json({ reply: text || 'I am not sure about that. I can pass your question to the team.', handoff });
}
