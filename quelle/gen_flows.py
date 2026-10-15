import json,glob,os,sys
MAP={81:'xabcde',83:'schockraum',88:'atemweg',91:'als',93:'pls',95:'nbversorgung',97:'nls',99:'postrosc',103:'dyspnoe',104:'tloc',105:'schmerz',106:'schmerz',113:'schock',114:'zns',115:'fremdkoerper',116:'aproblem',117:'aorta',119:'acs',121:'anaphylaxie',125:'arteriell',126:'tracheostoma',128:'bronch',131:'dehydratation',132:'geburt',136:'hypertensiv',138:'hypoglyk',140:'brady',141:'tachy',142:'intox',143:'lungenoedem',145:'krampf_erw',146:'krampf_kind',149:'lae',151:'krupp',152:'stroke',154:'sepsis',157:'trauma',158:'btrauma',159:'blutung',161:'dtrauma',162:'immo',163:'thermisch',165:'rettung',169:'mstart',171:'co'}
errs=[]
def chk(nodes,where):
    for nd in nodes:
        if 'q' in nd and nd['q'].startswith('('): nd['q']=''
        for b in nd.get('b',[]):
            if b.get('l','').startswith('('): b['l']=''
        keys=set(nd)
        if 'q' in nd:
            if not nd.get('b'): errs.append(where+': Frage ohne Zweige '+nd['q'][:40])
            for b in nd.get('b',[]):
                if 'l' not in b or 'n' not in b: errs.append(where+': Zweig ohne l/n')
                chk(b.get('n',[]),where)
        elif 's' in nd:
            if nd.get('k') not in (None,'med','opt','info'): errs.append(where+': k='+str(nd.get('k')))
        elif 'end' in nd or 'go' in nd: pass
        else: errs.append(where+': unbekannter Knoten '+json.dumps(nd)[:80])
out={}
for f in sorted(glob.glob('pdf/flow/*.json')):
    d=json.load(open(f)); p=d['page']
    if p not in MAP: continue
    if not d.get('flows'): continue
    for fl in d['flows']: chk(fl.get('steps',[]),str(p))
    out.setdefault(MAP[p],[]).append({'page':p,'title':d.get('title',''),'flows':d['flows'],'notes':d.get('notes',[])})
for k in out: out[k].sort(key=lambda x:x['page'])
open('app/flows.js','w').write('// Flussdiagramme aus dem Kompendium RD 2026 mit allen Verzweigungen (aus den PDF-Seiten übertragen)\nconst FLOWS = '+json.dumps(out,ensure_ascii=False)+';\n')
print(len(out),'Notfälle mit Ablauf;',sum(len(v) for v in out.values()),'Seiten'); print('\n'.join(errs) or 'Schema ok')
