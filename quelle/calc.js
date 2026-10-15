// Rechenlogik der Dosierhilfe – rein, ohne DOM, damit sie getestet werden kann.
function fmt(x, maxFrac) {
  if (x === null || x === undefined || !isFinite(x)) return "–";
  const mf = maxFrac === undefined ? (Math.abs(x) < 1 ? 3 : 2) : maxFrac;
  return Number(x.toFixed(mf)).toLocaleString("de-DE", { maximumFractionDigits: mf });
}
function inBand(w, b) {
  const lowOk = b.minEx ? w > b.min : w >= b.min;
  const highOk = b.max === Infinity ? true : (b.maxEx ? w < b.max : w <= b.max);
  return lowOk && highOk;
}
function volumes(dose, conc) {
  return (conc || []).map(c => ({ label: c.label, ml: dose / c.perMl }));
}
// Liefert ein Ergebnisobjekt für eine Rechenregel bei Gewicht w (kg).
function computeRule(rule, w) {
  const r = { label: rule.label, route: rule.route || "", unit: rule.unit, note: rule.note || "", warn: rule.warn || "", kind: rule.kind, status: "ok", messages: [] };
  if (rule.kind === "agetable") { r.rows = rule.rows; return r; }
  if (!(w > 0)) { r.status = "nodata"; return r; }
  if (rule.kind === "perkg") {
    const raw = w * rule.perKg;
    r.formula = fmt(rule.perKg) + " " + rule.unit + "/kgKG × " + fmt(w, 1) + " kg";
    r.raw = raw;
    if (rule.max !== null && rule.max !== undefined && raw > rule.max) {
      r.dose = rule.max; r.capped = true;
      r.messages.push({ t: "cap", m: "Rechnerisch " + fmt(raw) + " " + rule.unit + " – begrenzt auf Maximaldosis " + fmt(rule.max) + " " + rule.unit + (rule.maxLabel ? " (" + rule.maxLabel + ")" : "") });
    } else {
      r.dose = raw;
      if (rule.max !== null && rule.max !== undefined) r.messages.push({ t: "info", m: "Maximaldosis laut Quelle: " + fmt(rule.max) + " " + rule.unit + (rule.maxLabel ? " – " + rule.maxLabel : "") });
      else if (rule.cap) r.messages.push({ t: "info", m: rule.cap });
    }
    if (rule.minKg && w < rule.minKg) { r.status = "block"; r.messages.unshift({ t: "block", m: "Unter der Gewichtsgrenze der Quelle (" + fmt(rule.minKg) + " kg) – laut Quelle keine Anwendung." }); }
    if (rule.maxKg && w > rule.maxKg) { r.status = "block"; r.messages.unshift({ t: "block", m: "Diese Regel gilt laut Quelle nur bis " + fmt(rule.maxKg) + " kg." }); }
    r.vol = volumes(r.dose, rule.conc);
    return r;
  }
  if (rule.kind === "range") {
    r.lo = rule.lo * w; r.hi = rule.hi * w;
    r.formula = fmt(rule.lo) + "–" + fmt(rule.hi) + " " + rule.unit + "/kgKG × " + fmt(w, 1) + " kg";
    return r;
  }
  if (rule.kind === "band") {
    const b = rule.bands.find(x => inBand(w, x));
    r.bands = rule.bands.map(x => ({ text: x.text, active: x === b }));
    if (!b) { r.status = "gap"; r.messages.push({ t: "block", m: "Für " + fmt(w, 1) + " kg nennt die Quelle keinen Wert (außerhalb oder zwischen den Gewichtsbändern). Tabelle unten prüfen." }); r.vol = []; return r; }
    r.band = b.text;
    if (b.perKg) { r.dose = b.perKg * w; r.formula = fmt(b.perKg) + " " + rule.unit + "/kgKG × " + fmt(w, 1) + " kg"; }
    else { r.dose = b.dose; r.formula = "Gewichtsband " + b.text.split(":")[0]; }
    r.vol = volumes(r.dose, rule.conc);
    return r;
  }
  return r;
}
if (typeof module !== "undefined") module.exports = { computeRule, fmt, inBand };
