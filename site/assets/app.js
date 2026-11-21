/* Psychopath Whisperer site: shared front-end helpers (no build step). Same conventions as the Kiehl Lab site's app.js:
   window.CL holds the generic helpers; window.PW holds the few renderers specific to this site. */
window.CL = (function () {
  async function getJSON(path) {
    const r = await fetch(path, { cache: "no-cache" });
    if (!r.ok) throw new Error(path + ": " + r.status);
    return r.json();
  }
  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c])); }
  function fmtDate(d) {
    if (!d) return "";
    const [y, m, day] = String(d).split("-");
    if (!m) return y;
    const mon = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"][(+m || 1) - 1];
    return day ? `${+day} ${mon} ${y}` : `${mon} ${y}`;
  }
  function updateListBadge() {}
  return { getJSON, esc, fmtDate, updateListBadge };
})();

window.PW = (function () {
  const esc = CL.esc, n = x => Number(x).toLocaleString("en-US");
  const KINDS = { press: "Press", tv: "Television", podcast: "Podcast", interview: "Interview", talk: "Talk", award: "Award", book: "The book", essay: "Essay" };
  const kind = k => KINDS[k] || "News";
  // newest first; a year-only date ("2026") sorts as the end of that year, a year-month date as the end of that month
  const key = d => { const s = String(d || ""); return s.length === 4 ? s + "-12-31" : s.length === 7 ? s + "-31" : s; };
  const byDate = (a, b) => key(b.date).localeCompare(key(a.date));

  // one entry on the Top science / Top books pages
  function work(w, i, isBook) {
    const then = w.scholar_2014, grow = then ? Math.round(w.scholar_citations / then * 10) / 10 : null;
    const title = isBook && w.link ? w.cite_html.replace(/<i>(.*?)<\/i>/, `<a href="${esc(w.link)}"${/^https?:/.test(w.link) ? ' target="_blank" rel="noopener"' : ""}><i>$1</i></a>`) : w.cite_html;
    return `<article class="work${w.img ? " has-img" : ""}" id="${esc(w.id)}"><div class="n">${i}</div>${w.img ? `<img class="bk" src="assets/img/${esc(w.img)}" alt="" loading="lazy">` : ""}
      <div><p class="c">${title}${w.doi ? ` <a href="https://doi.org/${esc(w.doi)}" target="_blank" rel="noopener">doi ↗</a>` : ""}</p><p class="d">${w.note}</p></div>
      <div class="m"><b>${n(w.scholar_citations)}</b><span>Google Scholar citations</span>
        <small>as of ${CL.fmtDate(w.scholar_as_of)}${then ? `<br>${n(then)} in March 2014 <span class="up" style="display:inline;text-transform:none;letter-spacing:0;font-size:inherit">(×${grow})</span>` : ""}${w.openalex_citations != null ? `<br>OpenAlex: ${n(w.openalex_citations)} (${CL.fmtDate(w.openalex_as_of)})` : ""}${w.scholar_note ? `<br>${esc(w.scholar_note)}` : ""}</small></div></article>`;
  }
  const workNote = d => `Google Scholar counts were read on ${CL.fmtDate(d.updated)}. A second count from OpenAlex is added automatically each month for works that have a DOI.`;

  // swap a placeholder for an image from assets/img once the file exists (book cover, merchandise photo)
  function probe(file, ok) { const im = new Image(); im.onload = () => ok(im); im.src = "assets/img/" + file; }
  function cover(id) { probe("psychopath-whisperer-cover.jpg", im => { const el = document.getElementById(id); if (!el) return; im.className = "coverimg"; im.alt = "Cover of The Psychopath Whisperer"; el.replaceWith(im); }); }
  function img(id, file, alt) { probe(file, im => { const el = document.getElementById(id); if (el) { im.alt = alt; el.appendChild(im); } }); }
  return { kind, byDate, work, workNote, cover, img };
})();
