d='app/'
t=open(d+'template.html').read()
data='\n'.join(open(d+f).read() for f in ['calc.js','meds.js','notfaelle.js','komp.js','komp_meta.js'])
data=data.replace('if (typeof module !== "undefined") module.exports = { computeRule, fmt, inBand };','')
open(d+'rd-kompendium.html','w').write(t.replace('/*__DATA__*/',data))
