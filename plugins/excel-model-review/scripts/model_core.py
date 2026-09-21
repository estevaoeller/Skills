import csv, math, re, openpyxl
from collections import Counter
from openpyxl.utils import get_column_letter, range_boundaries

def load_book(p): return openpyxl.load_workbook(p,data_only=False,keep_vba=str(p).lower().endswith('.xlsm'))
def formula(v): return isinstance(v,str) and v.startswith('=')
def text(c):
    v=c.value
    return isinstance(v,str) and v.strip() and not v.startswith('=') and len(v.strip())<=300
def kind(a,b):
    if a is None:return 'added'
    if b is None:return 'removed'
    if formula(a) and formula(b):return 'formula_changed'
    if formula(a):return 'formula_to_value'
    if formula(b):return 'value_to_formula'
    return 'value_changed'
def changed(a,b,at=0,rt=0):
    out=[]
    for r in range(1,max(a.max_row,b.max_row)+1):
      for c in range(1,max(a.max_column,b.max_column)+1):
        x,y=a.cell(r,c).value,b.cell(r,c).value
        eq=math.isclose(float(x),float(y),abs_tol=at,rel_tol=rt) if type(x) in (int,float) and type(y) in (int,float) else x==y
        if not eq: out.append({'sheet':b.title,'row':r,'col':c,'cell':f'{get_column_letter(c)}{r}','change_type':kind(x,y),'before':x,'after':y})
    return out
def clusters(ch,gap_r=2,gap_c=2):
    rem=set(range(len(ch))); out=[]
    while rem:
      q=[rem.pop()]; group=[]
      while q:
        i=q.pop(); group.append(ch[i])
        near=[j for j in rem if abs(ch[i]['row']-ch[j]['row'])<=gap_r and abs(ch[i]['col']-ch[j]['col'])<=gap_c]
        for j in near: rem.remove(j); q.append(j)
      out.append(group)
    return out
def semantic_index(wb):
    idx={'texts':[],'comments':[],'defined_names':[],'tables':[]}
    for ws in wb.worksheets:
      for row in ws.iter_rows():
        for c in row:
          if text(c):
            idx['texts'].append({'sheet':ws.title,'cell':c.coordinate,'text':str(c.value).strip(),'bold':bool(c.font.bold),'merged':any(z.min_row<=c.row<=z.max_row and z.min_col<=c.column<=z.max_col for z in ws.merged_cells.ranges)})
          if c.comment and c.comment.text:
            idx['comments'].append({'sheet':ws.title,'cell':c.coordinate,'text':c.comment.text.strip()})
      for name,t in ws.tables.items(): idx['tables'].append({'sheet':ws.title,'name':name,'ref':t.ref})
    try:
      for dn in wb.defined_names.values(): idx['defined_names'].append({'name':dn.name,'attr_text':dn.attr_text})
    except Exception: pass
    return idx
def label(ws,r1,c1,r2,c2):
    cand=[]
    def add(r,c,score,src):
      if 1<=r<=ws.max_row and 1<=c<=ws.max_column and text(ws.cell(r,c)):
        x=ws.cell(r,c); val=str(x.value).strip()
        if val.isdigit() and len(val)<=4:return
        score+=16 if x.font.bold else 0
        score+=12 if any(z.min_row<=r<=z.max_row and z.min_col<=c<=z.max_col for z in ws.merged_cells.ranges) else 0
        # Penalize likely row labels inside a dense changed block.
        if r1<=r<=r2 and c<c1: score-=12
        cand.append((score,val,src,x.coordinate))
    for d in range(1,9):
      for c in range(max(1,c1-4),c2+1): add(r1-d,c,105-d*7,'above')
    for d in range(1,7):
      for r in range(r1,min(r2,r1+4)+1): add(r,c1-d,78-d*7,'left')
    for r in range(r1,min(r2,r1+3)+1):
      for c in range(c1,min(c2,c1+5)+1): add(r,c,70,'inside')
    if not cand:return '(sem rotulo identificado)','fallback',''
    cand.sort(reverse=True); return cand[0][1],cand[0][2],cand[0][3]
def cross_references(wb,sheet,rng,idx):
    """Find explicit workbook text/comments/names that mention the sheet/range or overlapping ranges."""
    out=[]; target_sheet=sheet.lower(); norm=rng.replace('$','').upper()
    terms=[target_sheet, norm]
    for x in idx['texts']+idx['comments']:
      s=x['text'].lower()
      if target_sheet in s and (norm.lower() in s or any(w in s for w in ['bloco','linha','coluna','intervalo','metodologia','passo a passo'])):
        out.append({'type':'workbook_reference','source':f"{x['sheet']}!{x['cell']}",'text':x['text'][:500]})
    for x in idx['defined_names']:
      a=(x.get('attr_text') or '')
      if sheet in a and norm.split(':')[0] in a.replace('$',''):
        out.append({'type':'defined_name','source':x['name'],'text':a})
    for x in idx['tables']:
      if x['sheet']==sheet:
        try:
          a1,b1,a2,b2=range_boundaries(norm); c1,d1,c2,d2=range_boundaries(x['ref'])
          if not(a2<c1 or c2<a1 or b2<d1 or d2<b1): out.append({'type':'table','source':x['name'],'text':x['ref']})
        except Exception: pass
    return out[:10]
def area(g,old,new,wb,idx):
    r1,r2=min(x['row'] for x in g),max(x['row'] for x in g); c1,c2=min(x['col'] for x in g),max(x['col'] for x in g)
    rng=f'{get_column_letter(c1)}{r1}:{get_column_letter(c2)}{r2}'
    lab,src,cell=label(new,r1,c1,r2,c2)
    if lab.startswith('(sem'): lab,src,cell=label(old,r1,c1,r2,c2)
    refs=cross_references(wb,new.title,rng,idx)
    status='referenced' if refs else ('explicit' if not lab.startswith('(sem') else 'unidentified')
    ct=Counter(x['change_type'] for x in g)
    cls='logica/hardcode' if ct['formula_to_value'] else 'logica de calculo' if ct['formula_changed'] or ct['value_to_formula'] else 'bloco incluido/expandido' if ct['added']>=2 else 'bloco removido/reduzido' if ct['removed']>=2 else 'conteudo/premissas'
    interpretation=''
    confidence=''
    pending=''
    if ct['formula_to_value']:
      interpretation='Formula(s) foram substituidas por valores; pode representar hardcode ou congelamento de calculo.'
      confidence='alta'; pending='Confirmar se a substituicao por valor foi intencional.'
    elif ct['value_to_formula']>=max(5,len(g)//2):
      interpretation='O bloco parece ter passado de valores armazenados para calculo interno por formulas.'
      confidence='media'; pending='Confirmar a motivacao e a fonte/logica incorporada.'
    elif ct['formula_changed']>=max(5,len(g)//2):
      interpretation='A logica de calculo do bloco foi amplamente revisada.'
      confidence='media'; pending='Confirmar a finalidade metodologica da revisao.'
    note='; '.join(f'{ct[k]} {k}' for k in ct)
    return {'sheet':new.title,'range':rng,'label':lab,'label_source':src,'label_cell':cell,'identification_status':status,'semantic_references':refs,'change_class':cls,'severity':'critical' if ct['formula_to_value'] else 'warning' if ct['formula_changed'] or ct['removed'] else 'info','changed_cells':len(g),'formulas_changed':ct['formula_changed'],'formula_to_value':ct['formula_to_value'],'value_to_formula':ct['value_to_formula'],'values_changed':ct['value_changed'],'added':ct['added'],'removed':ct['removed'],'note':note,'interpretation':interpretation,'interpretation_status':'inferred' if interpretation else 'not_interpreted','confidence':confidence,'pending_validation':pending,'evidence_cells':[x['cell'] for x in g[:30]]}
def sheet_event(s,cls,sev):
    return {'sheet':s,'range':'A1','label':'nova aba' if cls=='aba incluida' else 'aba removida','label_source':'sheet','label_cell':'','identification_status':'explicit','semantic_references':[],'change_class':cls,'severity':sev,'changed_cells':0,'formulas_changed':0,'formula_to_value':0,'value_to_formula':0,'values_changed':0,'added':0,'removed':0,'note':cls,'interpretation':'','interpretation_status':'not_interpreted','confidence':'','pending_validation':'','evidence_cells':[]}
def compare_pair(oldp,newp,row_gap=2,col_gap=2,abs_tol=0,rel_tol=0):
    A,B=load_book(oldp),load_book(newp); idx=semantic_index(B); areas=[]; evidence=[]; old,new=set(A.sheetnames),set(B.sheetnames)
    for s in A.sheetnames:
      if s not in new: continue
      ch=changed(A[s],B[s],abs_tol,rel_tol); evidence+=ch; areas += [area(g,A[s],B[s],B,idx) for g in clusters(ch,row_gap,col_gap)]
    for s in sorted(new-old): areas.append(sheet_event(s,'aba incluida','info'))
    for s in sorted(old-new): areas.append(sheet_event(s,'aba removida','warning'))
    return {'metadata':{'old_file':str(oldp),'new_file':str(newp)},'summary':{'areas_changed':len(areas),'cell_evidence_count':len(evidence),'sheets_added':sorted(new-old),'sheets_removed':sorted(old-new),'sheet_order_changed':A.sheetnames!=B.sheetnames},'areas':areas,'cell_evidence':evidence}
def write_area_csv(r,p):
    f=['sheet','range','label','identification_status','label_source','label_cell','change_class','severity','changed_cells','formulas_changed','formula_to_value','value_to_formula','values_changed','added','removed','interpretation','interpretation_status','confidence','pending_validation','note']
    with open(p,'w',newline='',encoding='utf-8-sig') as h:
      w=csv.DictWriter(h,fieldnames=f); w.writeheader(); [w.writerow({k:a.get(k) for k in f}) for a in r['areas']]
def write_evidence_csv(r,p):
    f=['sheet','cell','change_type','before','after']
    with open(p,'w',newline='',encoding='utf-8-sig') as h:
      w=csv.DictWriter(h,fieldnames=f); w.writeheader(); [w.writerow({k:a.get(k) for k in f}) for a in r['cell_evidence']]
def write_pair_markdown(r,p):
    L=['# Excel Model Structural Diff','','> Regra: evidencia explicita/referenciada e inferencia sao apresentadas separadamente.','','| Aba | Area | Identificacao | Status | Mudanca | Interpretacao | Confianca | Pendencia |','|---|---|---|---|---|---|---|---|']
    for a in r['areas']: L.append(f"| {a['sheet']} | {a['range']} | {a['label']} | {a['identification_status']} | {a['change_class']} ({a['note']}) | {a['interpretation']} | {a['confidence']} | {a['pending_validation']} |")
    p.write_text('\n'.join(L),encoding='utf-8')
def related(a,b):
    if a['sheet']!=b['sheet']:return False
    if a['label']==b['label'] and not a['label'].startswith('(sem'):return True
    ac1,ar1,ac2,ar2=range_boundaries(a['range']); bc1,br1,bc2,br2=range_boundaries(b['range']); return not(ar2<br1-2 or br2<ar1-2 or ac2<bc1-2 or bc2<ac1-2)
def consolidate_evolution(reports,names):
    T=[]
    for i,r in enumerate(reports):
      for a in r['areas']:
        t=next((x for x in T if related(x['rep'],a)),None); e={'transition':f'{names[i]} -> {names[i+1]}',**a}
        if t:t['events'].append(e)
        else:T.append({'sheet':a['sheet'],'label':a['label'],'rep':a,'events':[e]})
    for t in T:
      t['dominant_change']=Counter(e['change_class'] for e in t['events']).most_common(1)[0][0]; t['first_seen']=t['events'][0]['transition']; t['last_seen']=t['events'][-1]['transition']; t['event_count']=len(t['events']); t.pop('rep')
    return {'versions':names,'threads':T,'pair_reports':reports}
def write_evolution_markdown(r,p):
    L=['# Excel Model Evolution','','**Versoes:** '+' -> '.join(r['versions']),'', '> Interpretacoes inferidas sao marcadas e nao devem ser tratadas como fatos documentados.','']
    for t in r['threads']:
      L += [f"## {t['sheet']} — {t['label']}"]
      for e in t['events']:
        L.append(f"- {e['transition']} — {e['range']} — {e['change_class']} — identificacao: {e['identification_status']}")
        if e.get('interpretation'): L.append(f"  - **Inferencia:** {e['interpretation']} (confianca: {e['confidence']})")
        if e.get('pending_validation'): L.append(f"  - **Confirmar:** {e['pending_validation']}")
      L+=['']
    p.write_text('\n'.join(L),encoding='utf-8')
