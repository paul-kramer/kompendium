const KOMP_NOTE = "Aus dem Textauszug des Kompendiums übertragen; die Farbfelder des Originals fehlen, Seitenangaben können um eine Seite abweichen. Ein leeres Feld heißt nur: Die Tabelle nennt für diesen Bereich keine Qualifikation. Was das für den Einsatz bedeutet, regelt die lokale Verfahrensanweisung.";
const KOMP_LEGEND = [
  "Das genannte Level (RS / RettAss / NotSan / Notarzt) ist die erforderliche Mindestqualifikation des Durchführenden (KP S. 12).",
  "★ = vorabdelegierte Maßnahme nach § 4 Abs. 2 Nr. 2c NotSanG; zusätzliche Information ausschließlich für NotSan, mit Kompetenzüberprüfung nach lokaler Verfahrensanweisung (KP S. 12).",
  "„RettAss | ★“ steht so in der Tabelle: Mindestqualifikation RettAss, für NotSan zusätzlich mit ★ gekennzeichnet.",
  "► = Schulung von SAA und BPR / Maßnahme in Planung (KP S. 12).",
  "TNA / NA = Telenotarzt oder Notarzt. Umsetzung des Telenotarztes per lokaler Verfahrensanweisung (KP S. 12).",
  "Sternchen (*) am Wert verweisen auf eine Fußnote der Quelle; sie steht direkt darunter."
];
// Notfallbilder, die laut Kompendium in bestimmten Bereichen nicht gelten („außer: …“)
const NF_EXCL = {
  als: { r: ["D"], t: "Reanimation Erwachsene – ALS (KP S. 91)" },
  pls: { r: ["D"], t: "Reanimation Kinder – PLS (KP S. 93)" },
  nls: { r: ["D"], t: "Reanimation Neugeborene – NLS (KP S. 97)" },
  intox: { r: ["D"], t: "Intoxikation (KP S. 142)" },
  stroke: { r: ["D"], t: "Schlaganfall (KP S. 152)" },
  dtrauma: { r: ["SR AC"], t: "D-Problem Trauma (KP S. 161)" },
  immo: { r: ["SR AC"], t: "Immo-Ampel (KP S. 162)" },
  rettung: { r: ["D"], t: "Patientenzentrierte Rettung (KP S. 165–166)" },
  co: { r: ["D"], t: "Intoxikation mit Kohlenstoffmonoxid (KP S. 171–174)" }
};
const MSTART_EXCL = [
  { r: ["DO", "HSK", "D", "HA", "HAM"], t: "Vorsichtung mit roten / weißen Kennzeichnungsbändern (KP S. 167–168)" },
  { r: ["KR", "GE", "HSK", "D", "HA", "HAM"], t: "mSTaRT-Ablaufschema (KP S. 169)" }
];
