(() => {
 'use strict';
 document.documentElement.classList.add('js');
 const $=(s,r=document)=>r.querySelector(s), $$=(s,r=document)=>[...r.querySelectorAll(s)];
 const reduced=matchMedia('(prefers-reduced-motion: reduce)').matches;
 const lite=matchMedia('(max-width: 1100px), (hover: none)').matches;
 const fine=matchMedia('(hover: hover) and (pointer: fine)').matches;
 /* menú móvil */
 const menu=$('.mobile-menu'),toggle=$('.menu-toggle');
 function closeMenu(){menu.hidden=true;toggle.setAttribute('aria-expanded','false');toggle.setAttribute('aria-label','Abrir menú');document.body.classList.remove('menu-open');}
 toggle.addEventListener('click',()=>{const o=menu.hidden;menu.hidden=!o;toggle.setAttribute('aria-expanded',String(o));toggle.setAttribute('aria-label',o?'Cerrar menú':'Abrir menú');document.body.classList.toggle('menu-open',o);if(o)$('a',menu).focus();});
 menu.addEventListener('keydown',ev=>{if(ev.key==='Tab'&&!menu.hidden){const els=$$('a,button',menu);if(ev.shiftKey&&document.activeElement===els[0]){ev.preventDefault();toggle.focus();}else if(!ev.shiftKey&&document.activeElement===els.at(-1)){ev.preventDefault();toggle.focus();}}});
 document.addEventListener('keydown',ev=>{if(ev.key==='Escape'&&!menu.hidden){closeMenu();toggle.focus();}});
 matchMedia('(min-width: 1101px)').addEventListener('change',ev=>{if(ev.matches)closeMenu();});
 /* menú de servicios */
 const mega=$('#service-menu'),serviceNav=$('.desktop-nav a[href="servicios.html"]'),header=$('.header');let megaTimer;
 const showMega=()=>{clearTimeout(megaTimer);mega.style.top=header.getBoundingClientRect().bottom+'px';mega.classList.add('open');};
 const hideMega=()=>{megaTimer=setTimeout(()=>mega.classList.remove('open'),140);};
 if(serviceNav){serviceNav.addEventListener('mouseenter',showMega);serviceNav.addEventListener('mouseleave',hideMega);mega.addEventListener('mouseenter',showMega);mega.addEventListener('mouseleave',hideMega);
  serviceNav.addEventListener('keydown',ev=>{if(ev.key==='ArrowDown'){ev.preventDefault();showMega();$('a',mega).focus();}});
  mega.addEventListener('focusout',ev=>{if(!mega.contains(ev.relatedTarget))mega.classList.remove('open');});
  mega.addEventListener('keydown',ev=>{if(ev.key==='Escape'){mega.classList.remove('open');serviceNav.focus();}});}
 /* scroll: cabecera, progreso, revelado */
 let frame=false;const bar=$('.reading-progress');
 function onScroll(){if(frame)return;frame=true;requestAnimationFrame(()=>{const total=document.documentElement.scrollHeight-innerHeight;bar.style.transform='scaleX('+(total>0?scrollY/total:0).toFixed(4)+')';header.classList.toggle('scrolled',scrollY>40);if(scrollY>90)mega.classList.remove('open');frame=false;});}
 addEventListener('scroll',onScroll,{passive:true});onScroll();
 if('IntersectionObserver' in window){const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('visible');io.unobserve(e.target);}}),{threshold:.1,rootMargin:'0px 0px -6% 0px'});$$('.reveal,.reveal-img,.steps').forEach(el=>io.observe(el));}else $$('.reveal,.reveal-img,.steps').forEach(el=>el.classList.add('visible'));
 /* contadores */
 const nums=$$('[data-count]');
 const run=el=>{const end=parseFloat(el.dataset.count),dec=(el.dataset.count.split('.')[1]||'').length,suffix=el.dataset.suffix||'';if(reduced){el.firstChild.textContent=end.toFixed(dec).replace('.',',');return;}const t0=performance.now(),dur=1800;(function step(t){const k=Math.min((t-t0)/dur,1),v=end*(1-Math.pow(1-k,3));el.firstChild.textContent=v.toFixed(dec).replace('.',',');if(k<1)requestAnimationFrame(step);})(t0);};
 if('IntersectionObserver' in window){const io2=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){run(e.target);io2.unobserve(e.target);}}),{threshold:.6});nums.forEach(n=>io2.observe(n));}else nums.forEach(run);
 /* paralaje del hero con el cursor */
 const hero=$('.hero'),arch=$('.hero-arches');
 if(hero&&arch&&fine&&!reduced){hero.addEventListener('pointermove',ev=>{const r=hero.getBoundingClientRect();arch.style.setProperty('--px',((ev.clientX-r.left)/r.width-.5).toFixed(3));arch.style.setProperty('--py',((ev.clientY-r.top)/r.height-.5).toFixed(3));});}
 /* botones magnéticos */
 if(fine&&!reduced)$$('.btn').forEach(b=>{b.addEventListener('pointermove',ev=>{const r=b.getBoundingClientRect();b.style.translate=((ev.clientX-r.left-r.width/2)*.12)+'px '+((ev.clientY-r.top-r.height/2)*.22)+'px';});b.addEventListener('pointerleave',()=>b.style.translate='');});
 /* transformaciones */
 const stage=$('.compare-frame');
 if(stage){const range=$('#compare'),bi=$('[data-before]',stage),ai=$('[data-after]',stage),cap=$('.tf-caption'),thumbs=$$('[data-pair]');
  const setSplit=v=>{stage.style.setProperty('--split',v+'%');range.setAttribute('aria-valuetext',(100-v)+' % del después visible');};
  range.addEventListener('input',()=>setSplit(range.value));
  thumbs.forEach(t=>t.addEventListener('click',()=>{thumbs.forEach(x=>x.setAttribute('aria-pressed',String(x===t)));bi.src='assets/img/'+t.dataset.pair+'-antes.webp';ai.src='assets/img/'+t.dataset.pair+'-despues.webp';cap.textContent=t.dataset.label;range.value=50;setSplit(50);}));
  if(!reduced&&'IntersectionObserver' in window){const io3=new IntersectionObserver(es=>{if(es[0].isIntersecting){io3.disconnect();let k=0;const t0=performance.now();(function demo(t){k=(t-t0)/1800;const v=k<1?50+30*Math.sin(k*Math.PI*2):50;range.value=v;setSplit(v);if(k<1&&document.activeElement!==range)requestAnimationFrame(demo);else{range.value=50;setSplit(50);}})(t0);}},{threshold:.7});io3.observe(stage);}}
 /* recomendador */
 const finder={color:['La luz empieza en un buen diagnóstico.','Explora el color personalizado y el cuidado de rubios. Te ayudamos a elegir el tono y el proceso que encajen con tu cabello.','rubios','Explorar rubios y matices'],soft:['Un cabello más suave, una rutina más fácil.','Conoce los cuidados de nutrición y keratina. El equipo valorará tu cabello para orientar el tratamiento y el acabado.','keratina','Conocer la keratina'],event:['Ese día merece una propuesta muy tuya.','Explora nuestros recogidos y el cuidado de novias e invitadas. Cuéntanos la fecha para consultar disponibilidad.','novias','Preparar mi día'],care:['Un momento para bajar el ritmo.','Manos, pies, piel y bienestar. Descubre los cuidados de estética y consulta qué propuesta encaja contigo.','estetica','Descubrir estética']};
 $$('[data-find]').forEach(btn=>btn.addEventListener('click',()=>{$$('[data-find]').forEach(el=>{el.classList.toggle('active',el===btn);el.setAttribute('aria-pressed',String(el===btn));});const [title,text,slug,label]=finder[btn.dataset.find],result=$('#finder-result');result.replaceChildren();const h=document.createElement('h3'),p=document.createElement('p'),a=document.createElement('a');h.textContent=title;p.textContent=text;a.href=slug+'.html';a.className='link';a.innerHTML=label+' <span>→</span>';result.append(h,p,a);}));
 /* galería */
 $$('[data-filter]').forEach(btn=>btn.addEventListener('click',()=>{$$('[data-filter]').forEach(el=>{el.classList.toggle('active',el===btn);el.setAttribute('aria-pressed',String(el===btn));});let c=0;$$('.gallery-item[data-category]').forEach(el=>{el.hidden=btn.dataset.filter!=='Todo'&&el.dataset.category!==btn.dataset.filter;if(!el.hidden){c++;el.classList.add('visible');}});const s=$('.filter-status');if(s)s.textContent=`${c} fotografías en ${btn.dataset.filter}.`;}));
 const lightbox=$('#lightbox');let items=[],idx=0,opener;
 function setPhoto(i){idx=(i+items.length)%items.length;const b=items[idx];$('figure>img',lightbox).src=b.dataset.image;$('figure>img',lightbox).alt=b.dataset.caption;$('#lightbox-caption').textContent=b.dataset.caption;$('#lightbox-source').href=b.dataset.source;}
 $$('.gallery-open').forEach(btn=>btn.addEventListener('click',()=>{items=$$('.gallery-open').filter(el=>!el.closest('[hidden]'));opener=btn;setPhoto(items.indexOf(btn));lightbox.showModal();document.body.classList.add('dialog-open');}));
 $('.lightbox-prev').addEventListener('click',()=>setPhoto(idx-1));$('.lightbox-next').addEventListener('click',()=>setPhoto(idx+1));
 lightbox.addEventListener('keydown',ev=>{if(ev.key==='ArrowLeft')setPhoto(idx-1);if(ev.key==='ArrowRight')setPhoto(idx+1);});
 /* cita por WhatsApp */
 const booking=$('#booking'),form=$('#booking-form'),preview=$('.message-preview');let bookOpener;
 const date=$('input[type="date"]',form),now=new Date();date.min=[now.getFullYear(),String(now.getMonth()+1).padStart(2,'0'),String(now.getDate()).padStart(2,'0')].join('-');
 $$('[data-book]').forEach(btn=>btn.addEventListener('click',()=>{bookOpener=btn;closeMenu();mega.classList.remove('open');preview.hidden=true;const s=$('select[name="service"]',form),r=btn.dataset.book;s.value=[...s.options].some(o=>o.value===r)?r:'';booking.showModal();document.body.classList.add('dialog-open');}));
 form.addEventListener('input',()=>{preview.hidden=true;date.setCustomValidity('');});
 form.addEventListener('submit',ev=>{ev.preventDefault();date.setCustomValidity('');if(date.value&&date.value<date.min){date.setCustomValidity('Elige hoy o una fecha posterior.');date.reportValidity();return;}if(!form.reportValidity())return;const f=new FormData(form);const parts=[`Hola AURA, soy ${String(f.get('name')).trim()}.`,`Me gustaría consultar una cita para: ${f.get('service')}.`];if(f.get('date')){const [y,m,d]=String(f.get('date')).split('-');parts.push(`Día preferido: ${d}/${m}/${y}.`);}parts.push(`Franja: ${f.get('time')}.`);if(String(f.get('notes')).trim())parts.push(String(f.get('notes')).trim());parts.push('¿Podéis confirmarme disponibilidad y presupuesto? Gracias.');const text=parts.join('\n');$('#message-text').textContent=text;$('#send-whatsapp').href='https://wa.me/34642636970?text='+encodeURIComponent(text);preview.hidden=false;preview.scrollIntoView({behavior:reduced?'instant':'smooth',block:'nearest'});});
 $$('dialog').forEach(d=>{d.addEventListener('click',ev=>{if(ev.target===d){const r=d.getBoundingClientRect();if(ev.clientX<r.left||ev.clientX>r.right||ev.clientY<r.top||ev.clientY>r.bottom)d.close();}});$('[data-close]',d).addEventListener('click',()=>d.close());d.addEventListener('close',()=>{document.body.classList.remove('dialog-open');const t=d===booking?bookOpener:opener;if(t?.isConnected)t.focus();});});
 $$('[data-review]').forEach(btn=>btn.addEventListener('click',()=>{const tr=$('.review-track'),c=$('.review',tr);tr.scrollBy({left:(c.getBoundingClientRect().width+24)*(btn.dataset.review==='next'?1:-1),behavior:reduced?'instant':'smooth'});}));
 /* pestañas de servicio con avance automático */
 $$('.xp').forEach(xp=>{
  const tabs=$$('.xp-tab',xp),panels=$$('.xp-panel',xp),dur=8000;let cur=0,timer,visible=false;
  if(matchMedia('(max-width: 1100px)').matches){
   const box=$('.xp-panels',xp),bar=$('.xp-tabs',xp);let raf=0,idx=0,lock=0,lockT;
   const mk=(label,txt)=>{const x=document.createElement('button');x.type='button';x.className='xp-arrow';x.setAttribute('aria-label',label);x.textContent=txt;return x;};
   const prev=mk('Apartado anterior','‹'),next=mk('Apartado siguiente','›');
   bar.prepend(prev);bar.append(next);
   const off=k=>panels[k].offsetLeft-18;
   const pad=()=>{box.style.paddingRight=Math.max(18,box.clientWidth-panels[0].offsetWidth-18)+'px';};
   const mark=i=>{tabs.forEach((t,k)=>{t.setAttribute('aria-selected',String(k===i));t.tabIndex=k===i?0:-1;});panels.forEach((p,k)=>p.classList.toggle('is-active',k===i));prev.disabled=i===0;next.disabled=i===panels.length-1;};
   const go=k=>{k=Math.max(0,Math.min(panels.length-1,k));idx=k;mark(k);lock=1;clearTimeout(lockT);lockT=setTimeout(()=>{lock=0;},reduced?60:750);box.scrollTo({left:off(k),behavior:reduced?'auto':'smooth'});};
   tabs.forEach((t,k)=>t.addEventListener('click',()=>go(k)));
   prev.addEventListener('click',()=>go(idx-1));next.addEventListener('click',()=>go(idx+1));
   box.addEventListener('scroll',()=>{if(lock)return;cancelAnimationFrame(raf);raf=requestAnimationFrame(()=>{let best=0,d=1e9;panels.forEach((p,k)=>{const x=Math.abs(off(k)-box.scrollLeft);if(x<d){d=x;best=k;}});if(best!==idx){idx=best;mark(idx);}});},{passive:true});
   $$('.xp-more',xp).forEach(btn=>btn.addEventListener('click',()=>{const p=btn.closest('.xp-panel'),o=p.classList.toggle('open');btn.setAttribute('aria-expanded',String(o));$('span',btn).textContent=o?'Leer menos':'Leer más';}));
   pad();addEventListener('resize',pad);mark(0);
   return;
  }
  xp.style.setProperty('--dur',dur+'ms');
  const show=i=>{cur=(i+tabs.length)%tabs.length;tabs.forEach((t,k)=>{t.setAttribute('aria-selected',String(k===cur));t.tabIndex=k===cur?0:-1;});panels.forEach((pn,k)=>pn.classList.toggle('is-active',k===cur));const bar=$('.bar',tabs[cur]);if(bar){const c=bar.cloneNode(true);bar.replaceWith(c);}};
  const loop=()=>{clearTimeout(timer);if(reduced||!visible||xp.classList.contains('paused'))return;timer=setTimeout(()=>{show(cur+1);loop();},dur);};
  tabs.forEach((t,k)=>{t.addEventListener('click',()=>{show(k);loop();});t.addEventListener('keydown',ev=>{if(ev.key==='ArrowDown'||ev.key==='ArrowRight'){ev.preventDefault();show(cur+1);tabs[cur].focus();loop();}if(ev.key==='ArrowUp'||ev.key==='ArrowLeft'){ev.preventDefault();show(cur-1);tabs[cur].focus();loop();}});});
  ['mouseenter','focusin'].forEach(e=>xp.addEventListener(e,()=>{xp.classList.add('paused');clearTimeout(timer);}));
  ['mouseleave','focusout'].forEach(e=>xp.addEventListener(e,()=>{xp.classList.remove('paused');loop();}));
  if('IntersectionObserver' in window)new IntersectionObserver(es=>{visible=es[0].isIntersecting;if(visible){show(cur);loop();}else clearTimeout(timer);},{threshold:.35}).observe(xp);
  show(0);
 });
 /* paralaje suave de las bandas fotográficas */
 const bands=$$('.band-photo>img');
 if(bands.length&&!reduced&&!lite)addEventListener('scroll',()=>requestAnimationFrame(()=>bands.forEach(im=>{const r=im.parentElement.getBoundingClientRect();if(r.bottom>0&&r.top<innerHeight)im.style.transform='translate3d(0,'+((r.top+r.height/2-innerHeight/2)*-.12).toFixed(1)+'px,0)';})),{passive:true});

 /* ───── v3.2: transiciones, carga, parallax, titulares, horario, reseñas, test ───── */
 /* pantalla de carga (solo la primera vez por sesión) */
 const loader=$('#loader');
 if(loader){
  const root=document.documentElement;
  const done=()=>{loader.classList.add('done');try{sessionStorage.setItem('auraSeen','1');}catch(e){}setTimeout(()=>loader.remove(),900);};
  if(root.classList.contains('seen'))loader.remove();
  else{const t0=performance.now(),min=reduced?0:(lite?700:1200),fin=()=>setTimeout(done,Math.max(0,min-(performance.now()-t0)));
   if(document.readyState==='complete')fin();else addEventListener('load',fin);setTimeout(done,3000);}
 }
 /* fundido entre páginas */
 document.addEventListener('click',ev=>{
  const a=ev.target.closest&&ev.target.closest('a[href]');
  if(!a||ev.defaultPrevented||ev.button!==0||ev.metaKey||ev.ctrlKey||ev.shiftKey||ev.altKey||a.target||a.hasAttribute('download'))return;
  let u;try{u=new URL(a.href,location.href);}catch(e){return;}
  if(u.origin!==location.origin||!/\.html$|\/$/.test(u.pathname))return;
  if(u.pathname===location.pathname&&(u.hash||!u.search))return;
  ev.preventDefault();document.body.classList.add('leaving');setTimeout(()=>{location.href=a.href;},reduced?0:300);
 });
 addEventListener('pageshow',e=>{if(e.persisted)document.body.classList.remove('leaving');});
 /* cabeceras con profundidad al hacer scroll */
 const heroEl=$('.hero');
 if(heroEl&&!reduced&&!lite){let pend=false;const upd=()=>{pend=false;heroEl.style.setProperty('--sy',Math.min(scrollY,heroEl.offsetHeight).toFixed(0));};
  addEventListener('scroll',()=>{if(!pend){pend=true;requestAnimationFrame(upd);}},{passive:true});upd();}
 /* titulares que se desvelan palabra a palabra */
 if(!reduced&&!lite&&'IntersectionObserver' in window){
  const ioW=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');ioW.unobserve(e.target);}}),{threshold:.35});
  $$('main h2, .closing h2').forEach(h=>{
   if(h.closest('.hero'))return;let i=0;
   const walk=n=>[...n.childNodes].forEach(c=>{
    if(c.nodeType===3){const f=document.createDocumentFragment();c.textContent.split(/(\s+)/).forEach(p=>{if(!p)return;if(/^\s+$/.test(p))f.append(p);else{const s=document.createElement('span');s.className='w';s.style.setProperty('--wi',i++);s.textContent=p;f.append(s);}});c.replaceWith(f);}
    else if(c.nodeType===1&&c.tagName!=='BR')walk(c);});
   walk(h);h.classList.add('wr');ioW.observe(h);});
 }
 /* galería: saltar a una categoría */
 $$('[data-goto]').forEach(b=>b.addEventListener('click',()=>{const f=$('[data-filter="'+b.dataset.goto+'"]');if(f)f.click();const t=$('#album');if(t)t.scrollIntoView({behavior:reduced?'auto':'smooth',block:'start'});}));
 /* abierto ahora */
 const hd=$('#hours-data');
 if(hd){
  const H=JSON.parse(hd.textContent),fmt=m=>Math.floor(m/60)+':'+String(m%60).padStart(2,'0');
  const names=['domingo','lunes','martes','miércoles','jueves','viernes','sábado'];
  const nowLocal=()=>new Date(new Date().toLocaleString('en-US',{timeZone:H.tz}));
  const compute=()=>{
   const n=nowLocal(),d=n.getDay(),m=n.getHours()*60+n.getMinutes(),segs=H.days[d]||[];
   for(const [s,e] of segs){if(m>=s&&m<e){const left=e-m;return{state:left<=45?'soon':'open',d,m,text:'Abierto ahora',sub:'Cierra a las '+fmt(e)+(left<=45?' · quedan '+left+' min':''),short:'Abierto ahora · cierra a las '+fmt(e)};}}
   for(let k=0;k<8;k++){const dd=(d+k)%7,sg=H.days[dd]||[];for(const [s] of sg){if(k===0&&m>=s)continue;const when=k===0?'hoy':k===1?'mañana':'el '+names[dd];return{state:'closed',d,m,text:'Cerrado ahora',sub:'Abre '+when+' a las '+fmt(s),short:'Cerrado ahora · abre '+when+' a las '+fmt(s)};}}
   return{state:'closed',d,m,text:'Cerrado ahora',sub:'Consulta el horario',short:'Cerrado ahora'};
  };
  const paint=()=>{
   const r=compute();
   $$('[data-open-badge]').forEach(b=>{b.dataset.state=r.state;$('.txt',b).textContent=r.short;});
   $$('[data-open-status]').forEach(b=>{b.dataset.state=r.state;$('.big',b).textContent=r.text;$('.sub',b).textContent=r.sub;});
   const week=$('.week');
   if(week){const s0=+week.dataset.s0,s1=+week.dataset.s1;$$('li',week).forEach(li=>{const today=+li.dataset.day===r.d;li.classList.toggle('today',today);const nw=$('.now',li);if(today&&r.m>=s0&&r.m<=s1){nw.style.left=((r.m-s0)/(s1-s0)*100)+'%';nw.hidden=false;}else nw.hidden=true;});}
  };
  paint();setInterval(paint,60000);
 }
 /* reseñas: avance automático */
 const rt=$('.review-track');
 if(rt&&!reduced&&!lite){let vis=false;if('IntersectionObserver' in window)new IntersectionObserver(es=>{vis=es[0].isIntersecting;}).observe(rt);
  setInterval(()=>{if(!vis||rt.matches(':hover,:focus-within'))return;const c=$('.review',rt),step=c.getBoundingClientRect().width+24;if(rt.scrollLeft+rt.clientWidth>=rt.scrollWidth-6)rt.scrollTo({left:0,behavior:'smooth'});else rt.scrollBy({left:step,behavior:'smooth'});},5500);}
 /* test «¿Qué necesita tu pelo hoy?» */
 const qz=$('[data-quiz]');
 if(qz){
  const D=JSON.parse($('#quiz-data').textContent);
  const Q=[
   {q:'¿Qué te apetece hoy?',o:[['color','Dar luz o cambiar mi color'],['suave','Un cabello más suave y manejable'],['corte','Un corte o estilo nuevo'],['evento','Prepararme para un evento'],['mimo','Cuidar manos, piel o bienestar']]},
   {q:'¿Cómo está tu cabello ahora?',o:[['natural','Natural, sin tratamientos'],['teñido','Teñido'],['aclarado','Aclarado o con mechas'],['alisado','Con alisado o keratina'],['na','No aplica: voy por estética']]},
   {q:'¿Cuánto mantenimiento quieres?',o:[['min','El mínimo posible'],['med','Un término medio'],['max','Me gusta cuidarlo con mimo']]},
   {q:'¿Para cuándo lo quieres?',o:[['semana','Esta semana'],['semanas','En las próximas semanas'],['fecha','Tengo una fecha concreta'],['libre','Sin prisa, estoy explorando']]}];
  const WHY={coloracion:'Un color a tu medida empieza por tu base: tono, raíz y mantenimiento.',rubios:'Para aclarar con cabeza: matices, etapas y cuidado de la fibra.',keratina:'Para un cabello más manejable y un acabado pulido, valorando antes tu fibra.',peluqueria:'Un corte y un cuidado pensados para tu forma de peinarte, empezando por un diagnóstico.',novias:'Peinado y maquillaje con prueba y con tiempo, para que tú solo disfrutes.',estetica:'Manos, piel y bienestar: un rato para ti, con valoración previa.'};
  const N2={natural:'Partes de tu base natural: es un buen punto de partida.',teñido:'Cuéntanos tus tintes anteriores para elegir el tono con criterio.',aclarado:'El estado de la fibra marcará el plan: puede requerir varias visitas.',alisado:'Indícanos cuándo te hiciste el alisado o la keratina: influye en el orden de los servicios.',na:''};
  const N3={min:'Buscaremos una propuesta fácil de mantener.',med:'Te propondremos retoques espaciados y una rutina sencilla.',max:'Te recomendaremos una rutina completa para casa.'};
  const N4={semana:'Pide cita cuanto antes: el equipo confirma la disponibilidad.',semanas:'Aún hay margen para hacerlo con calma.',fecha:'Para una fecha concreta, reserva con tiempo y plantea una prueba.',libre:'Sin prisa: puedes empezar con un asesoramiento personalizado.'};
  const body=$('.qbody',qz),count=$('.qcount',qz),bar=$('.qbar i',qz),back=$('.qback',qz);
  let step=0,ans=[];
  const esc=s=>s.replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
  const ask=()=>{
   const q=Q[step];count.textContent='Pregunta '+(step+1)+' de '+Q.length;bar.style.width=((step)/Q.length*100)+'%';back.hidden=step===0;
   body.innerHTML='<h3>'+esc(q.q)+'</h3><div class="qopts">'+q.o.map(([k,t],i)=>'<button type="button" class="qopt" data-k="'+k+'" style="--i:'+i+'"><span>'+esc(t)+'</span><i aria-hidden="true">→</i></button>').join('')+'</div>';
  };
  const result=()=>{
   count.textContent='Tu resultado';bar.style.width='100%';back.hidden=false;
   const [a1,a2,a3,a4]=ans;
   let s=a1==='color'?(a2==='aclarado'?'rubios':'coloracion'):a1==='suave'?'keratina':a1==='corte'?'peluqueria':a1==='evento'?'novias':'estetica';
   const sv=D[s],txt=[WHY[s],a1==='mimo'?'':N2[a2],N3[a3],N4[a4]].filter(Boolean);
   const labels=ans.map((k,i)=>Q[i].o.find(o=>o[0]===k)[1]);
   body.innerHTML='<div class="qres"><figure class="arch"><img src="assets/img/'+sv.img+'.webp" alt=""></figure><div><span class="eyebrow">Tu propuesta</span><h3>'+esc(sv.title)+'</h3>'+txt.map(t=>'<p>'+esc(t)+'</p>').join('')+'<div class="actions"><button type="button" class="btn" id="quiz-book" data-book="'+esc(sv.title)+'">Pedir mi cita</button><a class="link" href="'+sv.url+'">Ver '+esc(sv.title.toLowerCase())+' <span>→</span></a></div>'+(a3==='max'?'<p class="muted" style="margin-top:16px">Mira también el <a href="cuidados.html" style="text-decoration:underline">cuidado en casa</a>.</p>':'')+'<button type="button" class="link qreset" style="margin-top:18px">Repetir el test</button></div></div>';
   const qb=$('#quiz-book',body);qb.addEventListener('click',()=>{bookOpener=qb;preview.hidden=true;const s=$('select[name="service"]',form),r=qb.dataset.book;s.value=[...s.options].some(o=>o.value===r)?r:'';const n=$('textarea[name="notes"]',form);if(n)n.value='Mi test AURA: '+labels.join(' · ')+'.';booking.showModal();document.body.classList.add('dialog-open');});
   $('.qreset',body).addEventListener('click',()=>{step=0;ans=[];ask();});
  };
  body.addEventListener('click',ev=>{const b=ev.target.closest('.qopt');if(!b)return;ans[step]=b.dataset.k;b.classList.add('on');setTimeout(()=>{step++;if(step<Q.length)ask();else result();},reduced?0:260);});
  back.addEventListener('click',()=>{if(step>=Q.length){step=Q.length-1;ans.length=step;}else{step=Math.max(0,step-1);ans.length=step;}ask();});
  ask();
 }

 /* pasos de la visita: paneles en abanico */
 $$('[data-journey]').forEach(j=>{
  const ps=$$('.jp',j),dur=6500;let cur=0,timer,vis=false;
  j.style.setProperty('--dur',dur+'ms');
  const show=i=>{cur=(i+ps.length)%ps.length;ps.forEach((p,k)=>{p.classList.toggle('is-active',k===cur);p.setAttribute('aria-expanded',String(k===cur));});};
  const loop=()=>{clearTimeout(timer);if(reduced||lite||!vis||j.classList.contains('paused'))return;timer=setTimeout(()=>{show(cur+1);loop();},dur);};
  ps.forEach((p,k)=>{
   p.addEventListener('click',()=>{if(k!==cur){show(k);loop();}});
   if(fine)p.addEventListener('mouseenter',()=>{if(k!==cur)show(k);});
   p.addEventListener('keydown',ev=>{
    if(ev.key==='Enter'||ev.key===' '){ev.preventDefault();show(k);}
    else if(ev.key==='ArrowRight'||ev.key==='ArrowDown'){ev.preventDefault();show(cur+1);ps[cur].focus();}
    else if(ev.key==='ArrowLeft'||ev.key==='ArrowUp'){ev.preventDefault();show(cur-1);ps[cur].focus();}});
  });
  ['mouseenter','focusin'].forEach(e=>j.addEventListener(e,()=>{j.classList.add('paused');clearTimeout(timer);}));
  ['mouseleave','focusout'].forEach(e=>j.addEventListener(e,()=>{j.classList.remove('paused');loop();}));
  if('IntersectionObserver' in window)new IntersectionObserver(es=>{vis=es[0].isIntersecting;if(vis){loop();}else clearTimeout(timer);},{threshold:.4}).observe(j);
 });

 /* enredadera: el tallo crece con el scroll y las flores se abren */
 $$('[data-vine]').forEach(v=>{
  const rows=$$('.vrow',v);
  if(reduced||!('IntersectionObserver' in window)){rows.forEach(r=>{r.style.setProperty('--p',1);r.classList.add('on');});return;}
  let active=false,pend=false;
  const upd=()=>{pend=false;const vh=innerHeight;rows.forEach(r=>{const b=r.getBoundingClientRect();const p=Math.max(0,Math.min(1,(vh*.86-b.top)/(b.height*1.05)));r.style.setProperty('--p',p.toFixed(3));if(p>.45)r.classList.add('on');});};
  const sched=()=>{if(active&&!pend){pend=true;requestAnimationFrame(upd);}};
  addEventListener('scroll',sched,{passive:true});addEventListener('resize',sched);
  new IntersectionObserver(es=>{active=es[0].isIntersecting;if(active)upd();},{rootMargin:'200px 0px'}).observe(v);
  upd();
 });

 /* compartir por WhatsApp: mensaje + enlace de la página en la que estás */
 $$('[data-share]').forEach(a=>{
  const url=location.href.split('#')[0];
  a.href='https://wa.me/?text='+encodeURIComponent((a.dataset.msg||'AURA Organic Salón')+' '+url);
 });

 /* menú móvil: «Servicios» desplegable */
 $$('.m-acc-btn').forEach(btn=>{
  const box=btn.closest('.m-acc');
  btn.addEventListener('click',()=>{const open=!box.classList.contains('open');box.classList.toggle('open',open);btn.setAttribute('aria-expanded',String(open));
   if(open)setTimeout(()=>box.scrollIntoView({block:'nearest',behavior:reduced?'auto':'smooth'}),120);});
 });
})();
