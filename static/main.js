document.getElementById('generate').addEventListener('click', async () => {
  const data = {
    name: document.getElementById('name').value,
    title: document.getElementById('title').value,
    experience: document.getElementById('experience').value,
    skills: document.getElementById('skills').value,
    target_job: document.getElementById('target_job').value,
    tone: document.getElementById('tone').value,
  }
  const out = document.getElementById('output')
  out.innerHTML = '<em>Generating…</em>'
  try {
    const res = await fetch('/api/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    })
    const j = await res.json()
    if (!j.ok) throw new Error(j.error || 'Unknown error')
    const r = j.result
    if (r.raw_text) {
      out.innerHTML = `<pre>${escapeHtml(r.raw_text)}</pre>`
    } else {
      // Pretty-print JSON keys if available
      const summary = r.summary || ''
      const bullets = r.experience_bullets || r.experience || []
      const skills = r.skills || []
      let html = ''
      if (summary) html += `<h3>Summary</h3><p>${escapeHtml(summary)}</p>`
      if (bullets && bullets.length) {
        html += '<h3>Experience</h3><ul>' + bullets.map(b => `<li>${escapeHtml(b)}</li>`).join('') + '</ul>'
      }
      if (skills && skills.length) html += '<h3>Skills</h3><p>' + escapeHtml(skills.join(', ')) + '</p>'
      out.innerHTML = html || `<pre>${escapeHtml(JSON.stringify(r, null, 2))}</pre>`
    }
  } catch (e) {
    out.innerHTML = `<pre style="color:red">Error: ${escapeHtml(e.message)}</pre>`
  }
})

function escapeHtml(s) {
  if (!s) return ''
  return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')
}
