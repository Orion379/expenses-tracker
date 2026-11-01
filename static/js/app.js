
const $ = (s, root=document) => root.querySelector(s);
const $$ = (s, root=document) => [...root.querySelectorAll(s)];
const page = document.body.dataset.page;
const store = {
  get(key){try{return JSON.parse(localStorage.getItem('et_'+key)||'[]')}catch{return []}},
  set(key,value){localStorage.setItem('et_'+key,JSON.stringify(value))},
  user(){try{return JSON.parse(localStorage.getItem('et_user')||'{}')}catch{return {}}}
};
const money = n => new Intl.NumberFormat('en-NG',{style:'currency',currency:store.user().currency||'NGN',maximumFractionDigits:2}).format(Number(n)||0);
function toast(message){const el=$('#toast');if(!el)return;el.textContent=message;el.classList.add('show');setTimeout(()=>el.classList.remove('show'),2400)}
function setUser(user){localStorage.setItem('et_user',JSON.stringify(user))}
function updateUserUI(){
 const u=store.user(), name=u.name||u.username||'Your account', initial=name.trim().charAt(0).toUpperCase()||'U';
 ['sideName','topName','profileDisplayName'].forEach(id=>{const e=document.getElementById(id);if(e)e.textContent=name});
 ['sideEmail','profileEmail'].forEach(id=>{const e=document.getElementById(id);if(e)e.textContent=u.email||'Personal workspace'});
 ['sideAvatar','topAvatar','profileAvatar'].forEach(id=>{const e=document.getElementById(id);if(e)e.textContent=initial});
 const welcome=$('#welcomeName');if(welcome)welcome.textContent=(u.name||'there').split(' ')[0];
}
function initTheme(){const theme=localStorage.getItem('et_theme')||'ocean';document.body.dataset.theme=theme;$$('[data-theme]').forEach(b=>b.classList.toggle('selected',b.dataset.theme===theme))}
function initShell(){
 updateUserUI();initTheme();
 const toggle=$('#menuToggle'), sidebar=$('#sidebar');if(toggle&&sidebar)toggle.addEventListener('click',()=>sidebar.classList.toggle('open'));
 $$('[data-theme]').forEach(b=>b.addEventListener('click',()=>{localStorage.setItem('et_theme',b.dataset.theme);initTheme();toast('Theme updated')}));
}
function initAuth(){
 const login=$('#loginForm');if(login)login.addEventListener('submit',e=>{e.preventDefault();const d=Object.fromEntries(new FormData(login));const old=store.user();setUser({...old,username:d.identity,name:old.name||d.identity.split('@')[0],email:d.identity.includes('@')?d.identity:(old.email||''),loggedIn:true});location.href='dashboard.html'});
 const reg=$('#registerForm');if(reg)reg.addEventListener('submit',e=>{e.preventDefault();const d=Object.fromEntries(new FormData(reg));setUser({...d,loggedIn:true,currency:'NGN'});location.href='dashboard.html'});
 const out=$('#confirmLogout');if(out)out.addEventListener('click',()=>{const u=store.user();setUser({...u,loggedIn:false});location.href='login.html'});
}
const schema={
 accounts:{key:'accounts',fields:['name','account_type','balance'],labels:['Account name','Account type','Balance']},
 income:{key:'income',fields:['source','amount','date','account_id'],labels:['Source','Amount','Date','Account']},
 expenses:{key:'expenses',fields:['title','amount','date','category','account','note'],labels:['Title','Amount','Date','Category','Account','Note']},
 categories:{key:'categories',fields:['name','color'],labels:['Category name','Color']},
 budgets:{key:'budgets',fields:['name','month','limit_amount','category'],labels:['Budget name','Month','Limit amount','Category']},
 recurring:{key:'recurring',fields:['title','amount','frequency','next_due_date','category'],labels:['Title','Amount','Frequency','Next due date','Category']},
 wishlist:{key:'wishlist',fields:['name','target_price','priority','status'],labels:['Item name','Target price','Priority','Status']}
};
function initRecords(){
 const cfg=schema[page];if(!cfg)return;
 const form=$('#recordForm'), panel=$('#entryPanel'), rows=$('#recordRows');
 const open=()=>{panel.hidden=false;form.reset();delete form.dataset.editId;$('#formFeedback').textContent='';};
 $('#toggleForm')?.addEventListener('click',open);
 $('#closeForm')?.addEventListener('click',()=>panel.hidden=true);
 $('#cancelForm')?.addEventListener('click',()=>panel.hidden=true);
 function render(){
  const all=store.get(cfg.key), query=($('#tableSearch')?.value||'').toLowerCase();
  const filtered=all.filter(r=>cfg.fields.some(f=>String(r[f]??'').toLowerCase().includes(query)));
  $('#recordCount').textContent=`${all.length} record${all.length===1?'':'s'}`;
  rows.innerHTML=filtered.length?filtered.map(r=>`<tr>${cfg.fields.map(f=>`<td>${f==='amount'||f==='balance'||f==='limit_amount'||f==='target_price'?money(r[f]):(r[f]??'—')}</td>`).join('')}<td><button class="row-action" data-edit="${r.id}">Edit</button><button class="row-action delete" data-delete="${r.id}">Delete</button></td></tr>`).join(''):`<tr><td colspan="${cfg.fields.length+1}" class="empty-cell">${query?'No matching records.':'No records yet. Add your first record.'}</td></tr>`;
 }
 form.addEventListener('submit',e=>{
  e.preventDefault();const data=Object.fromEntries(new FormData(form));let all=store.get(cfg.key);
  if(form.dataset.editId){all=all.map(r=>r.id===form.dataset.editId?{...r,...data}:r);toast('Record updated')}
  else{all.unshift({id:crypto.randomUUID?crypto.randomUUID():String(Date.now()),...data,createdAt:new Date().toISOString()});toast('Record added')}
  store.set(cfg.key,all);form.reset();delete form.dataset.editId;panel.hidden=true;render();updateDashboard();
 });
 rows.addEventListener('click',e=>{
  const id=e.target.dataset.edit||e.target.dataset.delete;if(!id)return;
  let all=store.get(cfg.key);
  if(e.target.dataset.delete){if(confirm('Delete this record?')){store.set(cfg.key,all.filter(r=>r.id!==id));render();updateDashboard();toast('Record deleted')}}
  else{const r=all.find(x=>x.id===id);if(!r)return;open();form.dataset.editId=id;cfg.fields.forEach(f=>{const input=form.elements[f];if(input)input.value=r[f]??''});}
 });
 $('#tableSearch')?.addEventListener('input',render);render();
}
function updateDashboard(){
 const income=store.get('income'),expenses=store.get('expenses'),accounts=store.get('accounts'),budgets=store.get('budgets');
 const sum=(arr,field)=>arr.reduce((s,x)=>s+(Number(x[field])||0),0);
 const set=(id,v)=>{const e=document.getElementById(id);if(e)e.textContent=v};
 set('totalBalance',money(sum(accounts,'balance')+sum(income,'amount')-sum(expenses,'amount')));
 set('totalIncome',money(sum(income,'amount')));set('totalExpenses',money(sum(expenses,'amount')));
 set('budgetRemaining',money(sum(budgets,'limit_amount')-sum(expenses,'amount')));
 const recent=$('#recentTransactions');if(recent){const items=[...income.map(x=>({...x,kind:'Income',label:x.source,sign:'+'})),...expenses.map(x=>({...x,kind:'Expense',label:x.title,sign:'−'}))].slice(0,5);recent.innerHTML=items.length?items.map(x=>`<div class="notification-item"><div class="notification-mark">${x.kind==='Income'?'↗':'↘'}</div><div style="flex:1"><p><strong>${x.label||x.kind}</strong></p><small>${x.kind} · ${x.date||'No date'}</small></div><strong>${x.sign}${money(x.amount)}</strong></div>`).join(''):'No transactions yet. Add your first income or expense.'}
 const bs=$('#budgetSummary');if(bs)bs.innerHTML=budgets.length?budgets.slice(0,4).map(b=>{const spent=expenses.filter(e=>!b.category||e.category===b.category).reduce((s,e)=>s+(Number(e.amount)||0),0);const pct=Math.min(100,b.limit_amount?spent/Number(b.limit_amount)*100:0);return `<div style="margin:15px 0"><div style="display:flex;justify-content:space-between;font-size:11px;margin-bottom:7px"><strong>${b.name}</strong><span>${money(spent)} / ${money(b.limit_amount)}</span></div><div style="height:7px;border-radius:9px;background:#edf2ef;overflow:hidden"><div style="width:${pct}%;height:100%;background:var(--green);border-radius:9px"></div></div></div>`}).join(''):'No budgets yet. Create one to track your spending.';
}
function initProfile(){
 const u=store.user(),form=$('#profileForm');if(!form)return;
 ['name','email','username','currency'].forEach(k=>{if(form.elements[k])form.elements[k].value=u[k]|| (k==='currency'?'NGN':'')});
 form.addEventListener('submit',e=>{e.preventDefault();setUser({...u,...Object.fromEntries(new FormData(form))});$('#profileFeedback').textContent='Profile saved successfully.';updateUserUI()});
}
function initNotifications(){
 const list=$('#notificationList');if(!list)return;
 let ns=store.get('notifications');if(!ns.length){ns=[{id:'n1',message:'Welcome to ExpenseTrack. Add your first account to get started.',read:false,createdAt:new Date().toISOString()},{id:'n2',message:'Tip: create monthly budgets to keep spending on track.',read:false,createdAt:new Date().toISOString()}];store.set('notifications',ns)}
 function render(){list.innerHTML=ns.length?ns.map(n=>`<div class="notification-item ${n.read?'':'unread'}"><div class="notification-mark">♧</div><div style="flex:1"><p>${n.message}</p><small>${new Date(n.createdAt).toLocaleString()}</small></div><button class="row-action" data-read="${n.id}">${n.read?'Read':'Mark read'}</button></div>`).join(''):'You’re all caught up.'}
 list.addEventListener('click',e=>{const id=e.target.dataset.read;if(!id)return;ns=ns.map(n=>n.id===id?{...n,read:true}:n);store.set('notifications',ns);render()});
 $('#markAllRead')?.addEventListener('click',()=>{ns=ns.map(n=>({...n,read:true}));store.set('notifications',ns);render();toast('All notifications marked as read')});render();
}
document.addEventListener('DOMContentLoaded',()=>{
 if(['login','register','logout'].includes(page)){initAuth();return}
 initShell();initRecords();initProfile();initNotifications();updateDashboard();
});
