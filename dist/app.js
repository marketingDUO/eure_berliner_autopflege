const menu=document.querySelector('.menu'),nav=document.querySelector('.navlinks');menu?.addEventListener('click',()=>{const open=nav.classList.toggle('open');menu.setAttribute('aria-expanded',String(open));menu.setAttribute('aria-label',open?'Menü schließen':'Menü öffnen')});
const dialog=document.querySelector('#lightbox');document.querySelectorAll('[data-image]').forEach(b=>b.addEventListener('click',()=>{dialog.querySelector('img').src=b.dataset.image;dialog.querySelector('img').alt=b.querySelector('img').alt;dialog.showModal()}));dialog?.querySelector('button').addEventListener('click',()=>dialog.close());dialog?.addEventListener('click',e=>{if(e.target===dialog)dialog.close()});
const form=document.querySelector('#request');if(form){const value=new URLSearchParams(location.search).get('leistung');if(value){const option=[...form.service.options].find(x=>x.value===value||x.textContent===value);if(option)form.service.value=option.value}const chosenClass=new URLSearchParams(location.search).get('klasse');if(['Kleinwagen','Mittelklasse','Oberklasse'].includes(chosenClass))form.message.value='Fahrzeugklasse: '+chosenClass+'\n';form.addEventListener('submit',e=>{e.preventDefault();const data=new FormData(form),body=`Guten Tag,\n\nich interessiere mich für: ${data.get('service')}\n\nFahrzeug und Pflegewunsch:\n${data.get('message')}\n\nName: ${data.get('name')}\nTelefon: ${data.get('phone')}\nE-Mail: ${data.get('email')}\n\nBitte melden Sie sich zur Terminabstimmung. Vielen Dank.`;location.href='mailto:info@eure-berlinerautopflege.de?subject='+encodeURIComponent('Terminanfrage – '+data.get('service'))+'&body='+encodeURIComponent(body);document.querySelector('#form-status').textContent='Ihre Anfrage wurde für Ihr E-Mail-Programm vorbereitet. Falls sich kein Programm öffnet, senden Sie Ihre Anfrage bitte direkt an info@eure-berlinerautopflege.de.'})}
// Grouped catalogue tabs, including keyboard and deep-link navigation.
document.querySelectorAll('[data-catalog]').forEach(catalog=>{
 const tabs=[...catalog.querySelectorAll('[data-tab]')],panels=[...catalog.querySelectorAll('[data-panel]')];
 const activate=(key,focus=false)=>{if(!tabs.some(t=>t.dataset.tab===key))return;tabs.forEach(t=>{const selected=t.dataset.tab===key;t.setAttribute('aria-selected',String(selected));t.tabIndex=selected?0:-1;if(selected&&focus)t.focus()});panels.forEach(p=>p.hidden=p.dataset.panel!==key)};
 const hash=location.hash.replace('#','');activate(tabs.some(t=>t.dataset.tab===hash)?hash:catalog.dataset.initial);catalog.classList.add('catalog-ready');
 tabs.forEach((t,i)=>{t.addEventListener('click',()=>activate(t.dataset.tab));t.addEventListener('keydown',e=>{let next;if(e.key==='ArrowRight')next=(i+1)%tabs.length;else if(e.key==='ArrowLeft')next=(i+tabs.length-1)%tabs.length;else if(e.key==='Home')next=0;else if(e.key==='End')next=tabs.length-1;else return;e.preventDefault();activate(tabs[next].dataset.tab,true)})});
});

// Each card owns its class selection and price; neighbouring cards stay unchanged.
document.querySelectorAll('.offer').forEach(offer=>{
 const buttons=[...offer.querySelectorAll('[data-vehicle]')],price=offer.querySelector('[data-prices]'),caption=offer.querySelector('[data-vehicle-caption]'),inquiry=offer.querySelector('[data-offer-inquiry]');
 if(!price||!buttons.length)return;
 buttons.forEach(button=>button.addEventListener('click',()=>{
  const index=Number(button.dataset.vehicle),name=['Kleinwagen','Mittelklasse','Oberklasse'][index];
  buttons.forEach(b=>{const selected=b===button;b.classList.toggle('selected',selected);b.setAttribute('aria-pressed',String(selected))});
  price.textContent=price.dataset.prices.split(',')[index];caption.textContent='Für '+name;
  if(inquiry){const url=new URL(inquiry.href,location.origin);url.searchParams.set('klasse',name);inquiry.href=url.pathname+url.search}
 }));
});
