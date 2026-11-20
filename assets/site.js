(() => {
 'use strict';
 document.documentElement.classList.add('js');
 const $=(s,r=document)=>r.querySelector(s), $$=(s,r=document)=>[...r.querySelectorAll(s)];
 const reduced=matchMedia('(prefers-reduced-motion: reduce)').matches;
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
 function onScroll(){if(frame)return;frame=true;requestAnimationFrame(()=>{const total=document.documentElement.scrollHeight-innerHeight;bar.style.width=(total>0?scrollY/total*100:0)+'%';header.classList.toggle('scrolled',scrollY>40);if(scrollY>90)mega.classList.remove('open');frame=false;});}
 addEventListener('scroll',onScroll,{passive:true});onScroll();
 if('IntersectionObserver' in window){const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('visible');io.unobserve(e.target);}}),{threshold:.1,rootMargin:'0px 0px -6% 0px'});$$('.reveal,.reveal-img').forEach(el=>io.observe(el));}else $$('.reveal,.reveal-img').forEach(el=>el.classList.add('visible'));
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
})();
