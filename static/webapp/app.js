const tg = window.Telegram?.WebApp;
if (tg) {
  tg.ready();
  tg.expand();
  tg.enableClosingConfirmation();
  tg.setHeaderColor("#0f172a");
  tg.setBackgroundColor("#0f172a");
}

const state = {
  initData: tg?.initData || "",
  user: tg?.initDataUnsafe?.user || null,
  cart: [],
  mode: "pickup",
  menu: []
};

const $ = (id) => document.getElementById(id);

function money(n){ return `${n} ₽`; }

function setUserLine(){
  const u = state.user;
  $("userLine").textContent = u ? `Hello, ${u.first_name || "User"} · id=${u.id}` : "Opened outside Telegram";
}

function renderMenu(){
  const grid = $("menuGrid");
  grid.innerHTML = "";
  state.menu.forEach(p => {
    const el = document.createElement("div");
    el.className = "item";
    el.innerHTML = `
  ${p.image_url ? `<img class="itemImg" src="${p.image_url}" alt="${p.name}">` : ""}
  <div class="itemTop">
    <div>
      <div class="itemName">${p.name}</div>
      <div class="muted">${p.category ? (p.category + " · ") : ""}${p.desc || ""}</div>
    </div>
    <div class="badge">${money(p.price)}</div>
  </div>
  <button class="btn">Add to cart</button>
`;
    el.querySelector("button").onclick = () => addToCart(p);
    grid.appendChild(el);
  });
}

function addToCart(p){
  const it = state.cart.find(x => x.id === p.id);
  if (it) it.qty += 1;
  else state.cart.push({id:p.id,name:p.name,price:p.price,qty:1});
  renderCart();
}

function renderCart(){
  const list = $("cartList");
  list.innerHTML = "";
  if (state.cart.length === 0){
    list.innerHTML = `<div class="muted">Cart is empty</div>`;
    $("totalPrice").textContent = money(0);
    return;
  }
  state.cart.forEach((it, idx) => {
    const line = document.createElement("div");
    line.className = "line";
    line.innerHTML = `
      <div>
        <div style="font-weight:900">${it.name}</div>
        <div class="muted">${money(it.price)} · qty ${it.qty}</div>
      </div>
      <div style="display:flex;gap:8px;align-items:center">
        <button class="pill">-</button>
        <button class="pill">+</button>
        <button class="pill" style="border-color:rgba(239,68,68,.4)">🗑</button>
      </div>
    `;
    const [bMinus,bPlus,bDel] = line.querySelectorAll("button");
    bMinus.onclick = () => { it.qty = Math.max(1, it.qty-1); renderCart(); };
    bPlus.onclick = () => { it.qty += 1; renderCart(); };
    bDel.onclick = () => { state.cart.splice(idx,1); renderCart(); };
    list.appendChild(line);
  });

  const total = state.cart.reduce((s,x)=>s + x.price*x.qty, 0);
  $("totalPrice").textContent = money(total);
}

function setMode(mode){
  state.mode = mode;
  document.querySelectorAll(".segBtn").forEach(b=>{
    b.classList.toggle("active", b.dataset.mode === mode);
  });
  $("deliveryForm").classList.toggle("hidden", mode !== "delivery");
}

async function api(path, body){
  const res = await fetch(path, {
    method: "POST",
    headers: {"Content-Type":"application/json"},
    body: JSON.stringify(body)
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || "Request failed");
  return data;
}
async function loadMenu(){
    const grid = $("menuGrid");
    grid.innerHTML = `<div class="muted">Loading menu…</div>`;
  
    try {
      const res = await fetch("/api/catalog/menu/");
      const data = await res.json();
  
      if (!res.ok) throw new Error(data.error || "Failed to load menu");
  
      state.menu = (data.items || []).map(p => ({
        id: p.id,
        name: p.name,
        price: Number(p.price),
        desc: p.desc || "",
        category: typeof p.category === "string" ? p.category : (p.category?.name || ""),
        image_url: p.image_url || ""
      }));
  
      if (!state.menu.length) {
        grid.innerHTML = `<div class="muted">No items in menu yet</div>`;
        return;
      }
  
      renderMenu();
    } catch (e) {
      grid.innerHTML = `<div class="muted">❌ ${e.message}</div>`;
    }
  }
async function checkout(){
  $("hint").textContent = "";
  if (!tg) { $("hint").textContent = "Open inside Telegram"; return; }
  if (state.cart.length === 0){ $("hint").textContent = "Cart is empty"; return; }

  const payload = {
    init_data: state.initData,
    cart: state.cart,
    mode: state.mode,
    address: state.mode === "delivery" ? $("addr").value.trim() : "",
    phone: state.mode === "delivery" ? $("phone").value.trim() : "",
  };

  if (state.mode === "delivery"){
    if (!payload.address || !payload.phone){
      $("hint").textContent = "Please fill address and phone";
      return;
    }
  }

  try{
    const data = await api("/api/orders/create/", payload);
    state.cart = [];
    renderCart();
    tg.showPopup({title:"✅ Order placed", message:`Order #${data.order_id} created`, buttons:[{type:"ok"}]});
    // можно закрыть WebApp:
    // tg.close();
  }catch(e){
    $("hint").textContent = "❌ " + e.message;
  }
}

async function openOrders(){
  $("ordersModal").classList.remove("hidden");
  $("ordersList").innerHTML = `<div class="muted">Loading…</div>`;
  try{
    const data = await api("/api/orders/list/", {init_data: state.initData});
    if (!data.orders.length){
      $("ordersList").innerHTML = `<div class="muted">No orders yet</div>`;
      return;
    }
    $("ordersList").innerHTML = data.orders.map(o => `
      <div class="line">
        <div>
          <div style="font-weight:900">#${o.id} · ${o.status}</div>
          <div class="muted">${o.total} ₺ · ${o.mode}</div>
        </div>
        <div class="muted">${o.created_at}</div>
      </div>
    `).join("");
  }catch(e){
    $("ordersList").innerHTML = `<div class="muted">❌ ${e.message}</div>`;
  }
}

function bind(){
  document.querySelectorAll(".segBtn").forEach(b => b.onclick = () => setMode(b.dataset.mode));
  $("btnCheckout").onclick = checkout;
  $("btnOrders").onclick = openOrders;
  $("btnCloseOrders").onclick = () => $("ordersModal").classList.add("hidden");
  $("ordersModal").onclick = (e) => { if (e.target.id === "ordersModal") $("ordersModal").classList.add("hidden"); }
}

setUserLine();
bind();
setMode("pickup");
loadMenu();
renderCart();