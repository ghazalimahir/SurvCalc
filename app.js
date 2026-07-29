const modules=[
['bgcoord','BG/JK ke Koordinat','Hitung koordinat baharu daripada koordinat, bearing dan jarak.',1],
['coordbg','Koordinat ke BG/JK','Hitung bearing dan jarak antara dua titik.',1],
['mid','Titik Tengah','Hitung koordinat titik tengah dua titik.',1],
['area','Koordinat ke Luas','Hitung luas poligon daripada senarai koordinat.',1],
['intersection','Titik Persilangan','Persilangan dua garisan melalui dua pasangan titik.',1],
['circle','Pusat Bulatan','Pusat bulatan melalui tiga titik.',1],
['level','Ukur Aras','Kaedah tinggi kolimatan asas.',1],
['traverse','Ukur Trabas','Hitung garisan penutup daripada beberapa bearing dan jarak.',1],
['missing','Hilang 2 Jarak','Hitung dua jarak yang hilang (1-2 dan 1-3) daripada tiga bearing dan satu jarak diketahui (2-3).',1],
['equal','Sekan Lebar Sama','Cari bearing dan jarak titik sekan apabila lebar tikai daripada bearing belakang dan hadapan adalah sama.',1],
['unequal','Sekan Lebar Beza','Cari bearing dan jarak titik sekan apabila lebar tikai daripada bearing belakang dan hadapan berbeza.',1],
['angle','Sudut Dalam','Hitung sudut dalam pada stesen tengah daripada koordinat tiga titik (belakang, tengah, hadapan).',1]];
const menu=document.querySelector('#menu'),panel=document.querySelector('#panel');
modules.forEach(m=>{const d=document.createElement('article');d.className='card';d.innerHTML=`<h2>${m[1]}</h2><p>${m[2]}</p><span class="tag ${m[3]?'':'pending'}">${m[3]?'Berfungsi':'Belum disahkan'}</span>`;d.onclick=()=>openModule(m[0]);menu.appendChild(d)});
function degFromDms(v){v=Number(v);if(!isFinite(v))throw Error('Bearing tidak sah');const sign=v<0?-1:1;v=Math.abs(v);const d=Math.floor(v),frac=(v-d)*100,m=Math.floor(frac+1e-9),s=(frac-m)*100;if(m>=60||s>=60)throw Error('Minit/saat mesti kurang 60');return sign*(d+m/60+s/3600)}
function dmsFromDeg(v){v=(v%360+360)%360;let d=Math.floor(v),mm=(v-d)*60,m=Math.floor(mm),s=(mm-m)*60;s=Math.round(s*100)/100;if(s>=60){s=0;m++}if(m>=60){m=0;d=(d+1)%360}return `${String(d).padStart(3,'0')}° ${String(m).padStart(2,'0')}' ${s.toFixed(2).padStart(5,'0')}"`}
const n=id=>{const v=Number(document.getElementById(id).value);if(!isFinite(v))throw Error('Lengkapkan semua nilai');return v};
function shell(title,body,calc){menu.classList.add('hidden');panel.classList.remove('hidden');panel.innerHTML=`<div class="toolbar"><h2>${title}</h2><button class="secondary" onclick="home()">Menu</button></div>${body}<div class="actions"><button onclick="${calc}()">Kira</button><button class="secondary" onclick="clearResult()">Padam keputusan</button></div><div id="result" class="result">Sedia.</div>`}
function fields(arr){return `<div class="fields">${arr.map(x=>`<label>${x[1]}<span class="signed"><button type="button" class="sign-toggle" onclick="toggleSign('${x[0]}')" aria-label="Tukar tanda +/-">±</button><input id="${x[0]}" inputmode="decimal" placeholder="${x[2]||''}"></span></label>`).join('')}</div>`}
function toggleSign(id){const el=document.getElementById(id);if(!el)return;const v=el.value.trim();if(v.startsWith('-'))el.value=v.slice(1);else if(v)el.value='-'+v;else el.value='-';el.focus()}
function openModule(id){if(id==='bgcoord')shell('BG/JK ke Koordinat',fields([['n1','Utara/Northing 1'],['e1','Timur/Easting 1'],['b','Bearing DDD.MMSS','123.4530'],['d','Jarak']]),'calcBgCoord');else if(id==='coordbg')shell('Koordinat ke BG/JK',fields([['n1','Utara 1'],['e1','Timur 1'],['n2','Utara 2'],['e2','Timur 2']]),'calcCoordBg');else if(id==='mid')shell('Titik Tengah',fields([['n1','Utara 1'],['e1','Timur 1'],['n2','Utara 2'],['e2','Timur 2']]),'calcMid');else if(id==='intersection')shell('Titik Persilangan',fields([['x1','Easting A1'],['y1','Northing A1'],['x2','Easting A2'],['y2','Northing A2'],['x3','Easting B1'],['y3','Northing B1'],['x4','Easting B2'],['y4','Northing B2']]),'calcIntersection');else if(id==='circle')shell('Pusat Bulatan',fields([['x1','Easting 1'],['y1','Northing 1'],['x2','Easting 2'],['y2','Northing 2'],['x3','Easting 3'],['y3','Northing 3']]),'calcCircle');else if(id==='level')shell('Ukur Aras',fields([['rl','Aras laras/RL diketahui'],['bs','Pandangan belakang (BS)'],['is','Pandangan tengah/depan (IS/FS)']]),'calcLevel');else if(id==='traverse'){shell('Ukur Trabas',`<p class="help">Masukkan setiap garisan trabas. Gunakan format bearing <b>DDD.MMSS</b>.</p><div class="table-wrap"><table class="traverse-table"><thead><tr><th>No.</th><th>Bearing</th><th>Jarak</th><th></th></tr></thead><tbody id="traverseRows"></tbody></table></div><div class="row-actions"><button type="button" class="secondary" onclick="addTraverseRow()">+ Tambah Garisan</button><button type="button" class="secondary" onclick="resetTraverseRows()">Kosongkan Semua</button></div>`,'calcTraverse');addTraverseRow('073.1330','115.990');addTraverseRow('171.3750','124.575');}else if(id==='area')shell('Koordinat ke Luas','<label>Koordinat (satu titik setiap baris: Easting,Northing)<textarea id="coords" rows="10" placeholder="1000,1000\n1100,1000\n1100,1050\n1000,1050"></textarea></label><br>','calcArea');else if(id==='missing')shell('Hilang 2 Jarak',fields([['b12','Bearing 1-2 DDD.MMSS','073.1330'],['b13','Bearing 1-3 DDD.MMSS'],['b23','Bearing 2-3 DDD.MMSS'],['d23','Jarak 2-3']]),'calcMissing');else if(id==='equal')shell('Sekan Lebar Sama',fields([['bb','Bearing Belakang DDD.MMSS'],['bh','Bearing Hadapan DDD.MMSS'],['lebar','Lebar']]),'calcEqual');else if(id==='unequal')shell('Sekan Lebar Beza',fields([['bb','Bearing Belakang DDD.MMSS'],['bh','Bearing Hadapan DDD.MMSS'],['l1','Lebar 1'],['l2','Lebar 2']]),'calcUnequal');else if(id==='angle')shell('Sudut Dalam','<p class="help">Stesen 2 ialah stesen tengah (tempat sudut dihitung). Stesen 1 = belakang, Stesen 3 = hadapan.</p>'+fields([['n1','Utara Stesen 1 (Belakang)'],['e1','Timur Stesen 1 (Belakang)'],['n2','Utara Stesen 2 (Tengah)'],['e2','Timur Stesen 2 (Tengah)'],['n3','Utara Stesen 3 (Hadapan)'],['e3','Timur Stesen 3 (Hadapan)']]),'calcAngle');else shell(modules.find(m=>m[0]===id)?.[1]||'Modul','<p>Formula modul ini belum dapat disahkan sepenuhnya daripada APK asal. Ia sengaja tidak diaktifkan bagi mengelakkan keputusan ukur yang salah.</p>','notReady')}
function out(t){document.getElementById('result').textContent=t}function safe(fn){try{fn()}catch(e){out('Ralat: '+e.message)}}

function dmsWholeSecond(v){v=(v%360+360)%360;let total=Math.round(v*3600);total%=1296000;const d=Math.floor(total/3600),m=Math.floor((total%3600)/60),sec=total%60;return `${String(d).padStart(3,'0')}.${String(m).padStart(2,'0')}${String(sec).padStart(2,'0')}`}
let traverseRowCount=0;
function addTraverseRow(bearing='',distance=''){
  const tbody=document.getElementById('traverseRows');
  if(!tbody)return;
  traverseRowCount++;
  const tr=document.createElement('tr');
  tr.innerHTML=`<td class="row-no"></td><td><input class="traverse-bearing" inputmode="decimal" placeholder="073.1330" value="${bearing}" aria-label="Bearing garisan"></td><td><input class="traverse-distance" inputmode="decimal" placeholder="115.990" value="${distance}" aria-label="Jarak garisan"></td><td><button type="button" class="danger compact" onclick="removeTraverseRow(this)" aria-label="Buang garisan">×</button></td>`;
  tbody.appendChild(tr);
  renumberTraverseRows();
}
function removeTraverseRow(btn){
  const tbody=document.getElementById('traverseRows');
  if(!tbody)return;
  if(tbody.rows.length<=1){tbody.querySelectorAll('input').forEach(i=>i.value='');return;}
  btn.closest('tr').remove();
  renumberTraverseRows();
}
function renumberTraverseRows(){document.querySelectorAll('#traverseRows tr').forEach((tr,i)=>tr.querySelector('.row-no').textContent=i+1)}
function resetTraverseRows(){const tbody=document.getElementById('traverseRows');if(!tbody)return;tbody.innerHTML='';traverseRowCount=0;addTraverseRow();clearResult()}
function calcTraverse(){safe(()=>{
  const rows=[...document.querySelectorAll('#traverseRows tr')];
  const lines=[];
  for(const [i,row] of rows.entries()){
    const btxt=row.querySelector('.traverse-bearing').value.trim();
    const dtxt=row.querySelector('.traverse-distance').value.trim();
    if(!btxt&&!dtxt)continue;
    if(!btxt||!dtxt)throw Error(`Lengkapkan bearing dan jarak pada garisan ${i+1}`);
    const bearing=degFromDms(Number(btxt));
    const distance=Number(dtxt);
    if(!isFinite(distance)||distance<0)throw Error(`Jarak garisan ${i+1} tidak sah`);
    const rad=bearing*Math.PI/180;
    lines.push({no:i+1,bearing,distance,dn:distance*Math.cos(rad),de:distance*Math.sin(rad)});
  }
  if(lines.length<2)throw Error('Masukkan sekurang-kurangnya 2 garisan');
  const sumN=lines.reduce((s,l)=>s+l.dn,0),sumE=lines.reduce((s,l)=>s+l.de,0);
  const closeN=-sumN,closeE=-sumE,linearMisclosure=Math.hypot(closeN,closeE),az=Math.atan2(closeE,closeN)*180/Math.PI;

  // Bentuk koordinat relatif daripada titik mula (E=0, N=0).
  // Translasi koordinat tidak mengubah perimeter atau keluasan.
  const points=[{e:0,n:0}];
  let currentE=0,currentN=0;
  for(const line of lines){
    currentN+=line.dn;
    currentE+=line.de;
    points.push({e:currentE,n:currentN});
  }
  let twiceArea=0;
  for(let i=0;i<points.length;i++){
    const a=points[i],b=points[(i+1)%points.length];
    twiceArea+=a.e*b.n-b.e*a.n;
  }
  const area=Math.abs(twiceArea)/2;
  const measuredDistance=lines.reduce((s,l)=>s+l.distance,0);
  const perimeter=measuredDistance+linearMisclosure;
  const precision=linearMisclosure>0?measuredDistance/linearMisclosure:Infinity;

  const details=lines.map(l=>`${String(l.no).padStart(2,'0')}  ΔN ${l.dn.toFixed(4).padStart(11)}   ΔE ${l.de.toFixed(4).padStart(11)}`).join('\n');
  out(`${details}
-----------------------------------
Jumlah ΔN = ${sumN.toFixed(4)}
Jumlah ΔE = ${sumE.toFixed(4)}
Jumlah jarak garisan = ${measuredDistance.toFixed(3)}

Bearing penutup = ${dmsWholeSecond(az)} (1″ terhampir)
Jarak penutup = ${linearMisclosure.toFixed(3)}
ΔN penutup = ${closeN.toFixed(4)}
ΔE penutup = ${closeE.toFixed(4)}

Tikaian lurus = ${linearMisclosure.toFixed(3)}
Nisbah tikaian = ${isFinite(precision)?`1 : ${Math.round(precision).toLocaleString('en-US')}`:'Tutup sempurna'}
Perimeter trabas = ${perimeter.toFixed(3)}
Keluasan trabas = ${area.toFixed(3)} unit²`)
})}
function calcBgCoord(){safe(()=>{const a=degFromDms(n('b'))*Math.PI/180,D=n('d');out(`Northing 2 = ${(n('n1')+D*Math.cos(a)).toFixed(4)}\nEasting 2  = ${(n('e1')+D*Math.sin(a)).toFixed(4)}`)})}
function calcCoordBg(){safe(()=>{const dn=n('n2')-n('n1'),de=n('e2')-n('e1'),dist=Math.hypot(dn,de),az=Math.atan2(de,dn)*180/Math.PI;out(`Bearing DDD.MMSS = ${dmsFromDeg(az)}\nBearing decimal = ${((az%360+360)%360).toFixed(8)}°\nJarak = ${dist.toFixed(4)}`)})}
function calcMid(){safe(()=>out(`Northing tengah = ${((n('n1')+n('n2'))/2).toFixed(4)}\nEasting tengah  = ${((n('e1')+n('e2'))/2).toFixed(4)}`))}
function calcLevel(){safe(()=>{const hi=n('rl')+n('bs');out(`Tinggi kolimatan = ${hi.toFixed(4)}\nAras titik = ${(hi-n('is')).toFixed(4)}`)})}
function calcArea(){safe(()=>{const pts=document.getElementById('coords').value.trim().split(/\n+/).map(l=>l.split(/[ ,;]+/).map(Number));if(pts.length<3||pts.some(p=>p.length<2||p.some(x=>!isFinite(x))))throw Error('Masukkan sekurang-kurangnya 3 titik yang sah');let a=0;pts.forEach((p,i)=>{const q=pts[(i+1)%pts.length];a+=p[0]*q[1]-q[0]*p[1]});out(`Luas = ${Math.abs(a/2).toFixed(4)} unit²\nBilangan titik = ${pts.length}`)})}
function calcIntersection(){safe(()=>{const x1=n('x1'),y1=n('y1'),x2=n('x2'),y2=n('y2'),x3=n('x3'),y3=n('y3'),x4=n('x4'),y4=n('y4');const den=(x1-x2)*(y3-y4)-(y1-y2)*(x3-x4);if(Math.abs(den)<1e-12)throw Error('Garisan selari atau bertindih');const t=((x1*y2-y1*x2)*(x3-x4)-(x1-x2)*(x3*y4-y3*x4))/den,u=((x1*y2-y1*x2)*(y3-y4)-(y1-y2)*(x3*y4-y3*x4))/den;out(`Easting = ${t.toFixed(4)}\nNorthing = ${u.toFixed(4)}`)})}
function calcCircle(){safe(()=>{const x1=n('x1'),y1=n('y1'),x2=n('x2'),y2=n('y2'),x3=n('x3'),y3=n('y3');const d=2*(x1*(y2-y3)+x2*(y3-y1)+x3*(y1-y2));if(Math.abs(d)<1e-12)throw Error('Tiga titik segaris');const ux=((x1*x1+y1*y1)*(y2-y3)+(x2*x2+y2*y2)*(y3-y1)+(x3*x3+y3*y3)*(y1-y2))/d;const uy=((x1*x1+y1*y1)*(x3-x2)+(x2*x2+y2*y2)*(x1-x3)+(x3*x3+y3*y3)*(x2-x1))/d;out(`Easting pusat = ${ux.toFixed(4)}\nNorthing pusat = ${uy.toFixed(4)}\nJejari = ${Math.hypot(ux-x1,uy-y1).toFixed(4)}`)})}
function calcMissing(){safe(()=>{
  const b12=degFromDms(n('b12'))*Math.PI/180,b13=degFromDms(n('b13'))*Math.PI/180,b23=degFromDms(n('b23'))*Math.PI/180,d23=n('d23');
  const denom=Math.sin(b13-b12);
  if(Math.abs(denom)<1e-12)throw Error('Bearing 1-2 dan 1-3 tidak boleh sama');
  const d12=Math.abs(Math.sin(b13-b23)*d23/denom),d13=Math.abs(Math.sin(b23-b12)*d23/denom);
  out(`Jarak 1-2 = ${d12.toFixed(3)}\nJarak 1-3 = ${d13.toFixed(3)}`)
})}
function calcEqual(){safe(()=>{
  const bb=degFromDms(n('bb')),bh=degFromDms(n('bh')),lebar=n('lebar');
  let j=bb-bh;if(j>180)j-=180;
  const k=j/2,rad=k*Math.PI/180;
  if(Math.abs(Math.sin(rad))<1e-12)throw Error('Sudut tidak sah');
  const jarak=lebar/Math.sin(rad);
  let bearing=bb-k;bearing=(bearing%360+360)%360;
  out(`Bearing = ${dmsFromDeg(bearing)}\nJarak = ${jarak.toFixed(3)}`)
})}
function calcUnequal(){safe(()=>{
  const bb=degFromDms(n('bb')),bh=degFromDms(n('bh')),l1=n('l1'),l2=n('l2');
  const theta=(bb-bh)*Math.PI/180;
  if(Math.abs(Math.sin(theta))<1e-12||Math.abs(Math.tan(theta))<1e-12)throw Error('Sudut tidak sah');
  const l=1/((l1/(l2*Math.sin(theta)))+1/Math.tan(theta));
  const m=Math.atan(l);
  let bearing=bh+m*180/Math.PI;if(bearing<0)bearing+=360;bearing=(bearing%360+360)%360;
  if(Math.abs(Math.sin(m))<1e-12)throw Error('Sudut tidak sah');
  const jarak=l2/Math.sin(m);
  out(`Bearing = ${dmsFromDeg(bearing)}\nJarak = ${jarak.toFixed(3)}`)
})}
function calcAngle(){safe(()=>{
  const n1=n('n1'),e1=n('e1'),n2=n('n2'),e2=n('e2'),n3=n('n3'),e3=n('e3');
  const bearing21=Math.atan2(e1-e2,n1-n2)*180/Math.PI,bearing23=Math.atan2(e3-e2,n3-n2)*180/Math.PI;
  let sudut1=bearing21-bearing23;sudut1=(sudut1%360+360)%360;
  const sudut2=360-sudut1;
  out(`Bearing 2-1 = ${dmsFromDeg((bearing21%360+360)%360)}\nBearing 2-3 = ${dmsFromDeg((bearing23%360+360)%360)}\nSudut Dalam 1 = ${dmsFromDeg(sudut1)}\nSudut Dalam 2 = ${dmsFromDeg(sudut2)}`)
})}
function notReady(){out('Belum diaktifkan — menunggu pengesahan formula asal.')}function clearResult(){out('Sedia.')}function home(){panel.classList.add('hidden');menu.classList.remove('hidden')}
if('serviceWorker'in navigator)navigator.serviceWorker.register('./sw.js?v=034');let deferred;window.addEventListener('beforeinstallprompt',e=>{e.preventDefault();deferred=e;installBtn.hidden=false});installBtn.onclick=async()=>{if(deferred){deferred.prompt();await deferred.userChoice;deferred=null;installBtn.hidden=true}};
