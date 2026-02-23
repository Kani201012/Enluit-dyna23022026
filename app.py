import streamlit as st
import zipfile
import io
import json
import re

# --- TITAN ENGINE CONFIGURATION ---
VERSION = "v50.0.0-Phoenix"

st.set_page_config(
    page_title=f"Titan Engine {VERSION}",
    layout="wide",
    page_icon="⚡",
    initial_sidebar_state="expanded"
)

# --- 1. CORE GENERATORS (JAVASCRIPT RUNTIME) ---
# This JS Engine is injected into the HTML. It handles Routing, Data Fetching, and UI Rendering on the client side.
TITAN_JS_CORE = """
<script>
/** 
 * TITAN CLIENT ENGINE v50 
 * 2050 Architecture: Zero-DB, Edge-Computed, CSV-Hydrated
 */

const STATE = {
    cart: JSON.parse(localStorage.getItem('titanCart')) || [],
    products: [],
    posts: [],
    config: {},
    route: 'home'
};

// --- ROUTER ---
function router() {
    const hash = window.location.hash.slice(1) || 'home';
    STATE.route = hash;
    document.querySelectorAll('.view-section').forEach(el => el.style.display = 'none');
    document.querySelectorAll('.nav-link').forEach(el => el.classList.remove('active'));
    
    // Handle Specific Routes
    if (hash.startsWith('product/')) {
        renderProductDetail(hash.split('/')[1]);
        document.getElementById('view-product-detail').style.display = 'block';
    } else if (hash.startsWith('post/')) {
        renderPostDetail(hash.split('/')[1]);
        document.getElementById('view-post-detail').style.display = 'block';
    } else {
        const view = document.getElementById('view-' + hash);
        if (view) {
            view.style.display = 'block';
            if (hash === 'store') renderStore();
            if (hash === 'blog') renderBlog();
        } else {
            document.getElementById('view-home').style.display = 'block';
        }
    }
    window.scrollTo(0,0);
}
window.addEventListener('hashchange', router);
window.addEventListener('load', () => { init(); router(); });

// --- DATA LAYER ---
async function fetchCSV(url) {
    if(!url) return [];
    try {
        const res = await fetch(url);
        const text = await res.text();
        const rows = text.split(/\\r\\n|\\n/);
        return rows.slice(1).map(row => {
            // Simple CSV parser that respects quotes
            const regex = /(?:^|,)(?:"([^"]*)"|([^",]*))/g;
            let match, res = [];
            while (match = regex.exec(row)) res.push(match[1] || match[2] || "");
            return res;
        }).filter(r => r.length > 1);
    } catch (e) { console.error("Data Fetch Error", e); return []; }
}

async function init() {
    updateCartCount();
    // Load Data in Background
    if(CONFIG.storeUrl) STATE.products = await fetchCSV(CONFIG.storeUrl);
    if(CONFIG.blogUrl) STATE.posts = await fetchCSV(CONFIG.blogUrl);
}

// --- RENDERERS ---
function renderStore() {
    const grid = document.getElementById('store-grid');
    if(!STATE.products.length) { grid.innerHTML = '<p>Loading Inventory...</p>'; return; }
    grid.innerHTML = STATE.products.map(p => `
        <div class="card reveal">
            <div class="card-img" style="background-image:url('${p[3]?.split('|')[0] || CONFIG.placeholderImg}')"></div>
            <div class="card-body">
                <h3>${p[0]}</h3>
                <div class="price">${p[1]}</div>
                <p>${p[2].substring(0, 80)}...</p>
                <button onclick="addToCart('${p[0]}', '${p[1]}')" class="btn btn-sm">Add to Cart</button>
                <a href="#product/${encodeURIComponent(p[0])}" class="btn btn-sm btn-outline">Details</a>
            </div>
        </div>
    `).join('');
}

function renderBlog() {
    const grid = document.getElementById('blog-grid');
    if(!STATE.posts.length) { grid.innerHTML = '<p>Loading Articles...</p>'; return; }
    grid.innerHTML = STATE.posts.map(p => `
        <div class="card reveal horizontal">
            <div class="card-img" style="width:150px; background-image:url('${p[5] || CONFIG.placeholderImg}')"></div>
            <div class="card-body">
                <span class="badge">${p[3]}</span>
                <h3>${p[1]}</h3>
                <p>${p[4]}</p>
                <a href="#post/${p[0]}" class="read-more">Read Article &rarr;</a>
            </div>
        </div>
    `).join('');
}

function renderProductDetail(name) {
    const decoded = decodeURIComponent(name);
    const p = STATE.products.find(x => x[0] === decoded);
    if(!p) return;
    const imgs = p[3] ? p[3].split('|') : [CONFIG.placeholderImg];
    document.getElementById('pd-img').src = imgs[0];
    document.getElementById('pd-title').innerText = p[0];
    document.getElementById('pd-price').innerText = p[1];
    document.getElementById('pd-desc').innerText = p[2];
    // Setup Add to Cart Button
    const btn = document.getElementById('pd-add');
    btn.onclick = () => addToCart(p[0], p[1]);
}

function renderPostDetail(id) {
    const p = STATE.posts.find(x => x[0] === id);
    if(!p) return;
    document.getElementById('bp-img').src = p[5] || CONFIG.placeholderImg;
    document.getElementById('bp-title').innerText = p[1];
    document.getElementById('bp-content').innerHTML = p[6].replace(/\\n/g, '<br>');
}

// --- CART SYSTEM ---
function addToCart(name, price) {
    STATE.cart.push({name, price});
    localStorage.setItem('titanCart', JSON.stringify(STATE.cart));
    updateCartCount();
    showToast("Added to Cart");
}

function updateCartCount() {
    document.getElementById('cart-count').innerText = STATE.cart.length;
}

function checkout() {
    if(STATE.cart.length === 0) return alert("Cart is empty");
    let msg = "New Order:%0A";
    let total = 0;
    STATE.cart.forEach(i => {
        msg += `- ${i.name} (${i.price})%0A`;
        total += parseFloat(i.price.replace(/[^0-9.]/g, '')) || 0;
    });
    msg += `%0ATotal Value: ${total.toFixed(2)}`;
    window.open(`https://wa.me/${CONFIG.whatsapp}?text=${msg}`, '_blank');
    STATE.cart = [];
    localStorage.setItem('titanCart', JSON.stringify(STATE.cart));
    updateCartCount();
    toggleCart();
}

function toggleCart() {
    const modal = document.getElementById('cart-modal');
    modal.style.display = modal.style.display === 'flex' ? 'none' : 'flex';
    if(modal.style.display === 'flex') {
        const list = document.getElementById('cart-list');
        list.innerHTML = STATE.cart.map((i, idx) => `
            <div class="cart-item">
                <span>${i.name}</span>
                <span>${i.price} <b style="color:red;cursor:pointer" onclick="STATE.cart.splice(${idx},1); localStorage.setItem('titanCart', JSON.stringify(STATE.cart)); toggleCart(); toggleCart();">x</b></span>
            </div>
        `).join('');
    }
}

// --- UI UTILS ---
function showToast(msg) {
    const t = document.createElement('div');
    t.className = 'toast'; t.innerText = msg;
    document.body.appendChild(t);
    setTimeout(() => t.remove(), 2000);
}

// Intersection Observer for Animations
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) entry.target.classList.add('active');
    });
});
setTimeout(() => document.querySelectorAll('.reveal').forEach(el => observer.observe(el)), 500);

</script>
"""

TITAN_CSS = """
<style>
:root {
    --primary: {{P_COLOR}};
    --accent: {{S_COLOR}};
    --bg: {{BG_COLOR}};
    --text: {{TXT_COLOR}};
    --card: {{CARD_COLOR}};
    --font-head: '{{FONT_HEAD}}', sans-serif;
    --font-body: '{{FONT_BODY}}', sans-serif;
}

/* RESET */
* { box-sizing: border-box; margin: 0; padding: 0; }
body { background: var(--bg); color: var(--text); font-family: var(--font-body); line-height: 1.6; overflow-x: hidden; }
a { text-decoration: none; color: inherit; transition: 0.3s; }
ul { list-style: none; }

/* LAYOUT */
.container { max-width: 1200px; margin: 0 auto; padding: 0 20px; }
section { padding: 4rem 0; }
.grid-3 { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem; }

/* TYPOGRAPHY */
h1, h2, h3, h4 { font-family: var(--font-head); line-height: 1.1; margin-bottom: 1rem; color: var(--primary); }
h1 { font-size: clamp(2.5rem, 5vw, 4.5rem); }
h2 { font-size: 2.5rem; text-align: center; margin-bottom: 3rem; }

/* COMPONENTS */
.btn { display: inline-block; padding: 0.8rem 1.8rem; background: var(--primary); color: white; border-radius: 8px; font-weight: bold; border: none; cursor: pointer; }
.btn:hover { filter: brightness(1.1); transform: translateY(-2px); }
.btn-accent { background: var(--accent); }
.btn-outline { background: transparent; border: 2px solid var(--primary); color: var(--primary); }
.btn-sm { padding: 0.5rem 1rem; font-size: 0.9rem; }

.card { background: var(--card); border-radius: 12px; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.05); transition: 0.3s; border: 1px solid rgba(128,128,128,0.1); }
.card:hover { transform: translateY(-5px); box-shadow: 0 20px 40px rgba(0,0,0,0.1); }
.card-img { height: 220px; background-size: cover; background-position: center; }
.card-body { padding: 1.5rem; display: flex; flex-direction: column; gap: 0.5rem; }
.card.horizontal { display: flex; flex-direction: row; }
.card.horizontal .card-img { width: 40%; height: auto; }

/* NAVIGATION */
nav { position: fixed; top: 0; width: 100%; background: rgba(255,255,255,0.9); backdrop-filter: blur(10px); z-index: 1000; border-bottom: 1px solid rgba(0,0,0,0.05); }
.nav-flex { display: flex; justify-content: space-between; align-items: center; height: 70px; }
.nav-links { display: flex; gap: 2rem; font-weight: 600; }
.nav-links a:hover { color: var(--accent); }

/* HERO */
.hero { min-height: 80vh; display: flex; align-items: center; background-size: cover; background-position: center; position: relative; color: white; }
.hero-overlay { position: absolute; inset: 0; background: linear-gradient(90deg, rgba(0,0,0,0.8) 0%, rgba(0,0,0,0.3) 100%); }
.hero-content { position: relative; z-index: 2; max-width: 600px; }

/* UTILS */
.reveal { opacity: 0; transform: translateY(30px); transition: 0.8s all ease; }
.reveal.active { opacity: 1; transform: translateY(0); }
.badge { background: var(--accent); color: white; padding: 0.2rem 0.6rem; border-radius: 50px; font-size: 0.8rem; width: fit-content; }
.toast { position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%); background: var(--primary); color: white; padding: 1rem 2rem; border-radius: 50px; z-index: 2000; animation: fadeUp 0.3s; }

/* CART MODAL */
#cart-float { position: fixed; bottom: 30px; right: 30px; background: var(--accent); color: white; width: 60px; height: 60px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.5rem; cursor: pointer; box-shadow: 0 10px 30px rgba(0,0,0,0.2); z-index: 1001; }
#cart-modal { display: none; position: fixed; inset: 0; background: rgba(0,0,0,0.6); z-index: 2000; align-items: center; justify-content: center; }
.modal-content { background: var(--card); padding: 2rem; border-radius: 12px; width: 90%; max-width: 500px; color: var(--text); }

/* DARK MODE OVERRIDES */
@media (prefers-color-scheme: dark) {
    nav { background: rgba(15, 23, 42, 0.9); }
}
@media (max-width: 768px) {
    .nav-links { display: none; } /* Simplified mobile for demo */
    .hero h1 { font-size: 2.5rem; }
    .card.horizontal { flex-direction: column; }
    .card.horizontal .card-img { width: 100%; height: 200px; }
}
</style>
"""

# --- 2. BUILDER UI (STREAMLIT) ---

def init_state(key, val):
    if key not in st.session_state: st.session_state[key] = val

init_state('biz_name', "Stop Web Rent")
init_state('hero_h', "Stop Paying Rent for Your Website.")
init_state('hero_sub', "The Titan Engine is the world’s first 0.1s website architecture that runs on $0 monthly fees.")

with st.sidebar:
    st.title("Titan Engine 2050")
    st.caption("v50.0 - Phoenix Edition")
    
    st.header("🎨 Visual DNA")
    # THEME PRESETS
    theme = st.selectbox("Design Theme", ["Clean Corp", "Dark Mode SaaS", "Cyberpunk", "Luxury Gold"])
    
    col_def = {"p": "#0f172a", "s": "#ef4444", "bg": "#ffffff", "txt": "#1e293b", "card": "#ffffff"}
    if theme == "Dark Mode SaaS": col_def = {"p": "#3b82f6", "s": "#10b981", "bg": "#0f172a", "txt": "#f8fafc", "card": "#1e293b"}
    elif theme == "Cyberpunk": col_def = {"p": "#d946ef", "s": "#06b6d4", "bg": "#09090b", "txt": "#e4e4e7", "card": "#18181b"}
    
    p_color = st.color_picker("Primary", col_def["p"])
    s_color = st.color_picker("Accent", col_def["s"])
    bg_color = st.color_picker("Background", col_def["bg"])
    txt_color = st.color_picker("Text", col_def["txt"])
    card_color = st.color_picker("Card BG", col_def["card"])
    
    h_font = st.selectbox("Header Font", ["Space Grotesk", "Inter", "Playfair Display", "Montserrat"])
    b_font = st.selectbox("Body Font", ["Inter", "Roboto", "Open Sans", "Lato"])

st.title("🏗️ StopWebRent Site Builder (v50)")
st.markdown("Generating a **Single Page Application (SPA)** with client-side hydration. No database required.")

tabs = st.tabs(["1. Identity", "2. Content", "3. Store/Blog", "4. Marketing", "5. Booking/Legal"])

with tabs[0]:
    c1, c2 = st.columns(2)
    biz_name = c1.text_input("Business Name", "StopWebRent")
    wa_num = c2.text_input("WhatsApp Number (for checkout)", "919876543210")
    
    st.subheader("Hero Section")
    hero_h = st.text_input("Headline", "Stop Paying Rent for Your Website.")
    hero_sub = st.text_area("Subtext", "The Titan Engine runs on $0 monthly fees. Pay once. Own it forever.")
    hero_img = st.text_input("Hero BG Image", "https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=1600")

with tabs[1]:
    st.subheader("Features Grid")
    feat_1 = st.text_input("Feat 1 (Icon|Title|Desc)", "bolt|Blazing Fast|0.1s load times.")
    feat_2 = st.text_input("Feat 2 (Icon|Title|Desc)", "wallet|Zero Fees|No monthly hosting bills.")
    feat_3 = st.text_input("Feat 3 (Icon|Title|Desc)", "shield|Unhackable|Static architecture security.")

with tabs[2]:
    st.subheader("Dynamic Data Sources")
    st.info("Paste your Google Sheet CSV Links here. The site will fetch data live.")
    store_url = st.text_input("Store CSV URL")
    blog_url = st.text_input("Blog CSV URL")
    def_img = st.text_input("Default Placeholder Image", "https://via.placeholder.com/400")

with tabs[3]:
    st.subheader("SEO & Analytics")
    ga_id = st.text_input("Google Analytics ID (G-XXXX)")
    seo_desc = st.text_input("Meta Description", "The best web development service.")

with tabs[4]:
    st.subheader("Booking & Legal")
    calendly = st.text_input("Calendly/Booking URL", "https://calendly.com")
    legal_txt = st.text_area("Footer Legal Text", "© 2050 StopWebRent. All rights reserved.")

# --- 3. COMPILATION ENGINE ---

def build_spa():
    # 1. PROCESS CSS
    css = TITAN_CSS.replace("{{P_COLOR}}", p_color).replace("{{S_COLOR}}", s_color)\
                   .replace("{{BG_COLOR}}", bg_color).replace("{{TXT_COLOR}}", txt_color)\
                   .replace("{{CARD_COLOR}}", card_color).replace("{{FONT_HEAD}}", h_font)\
                   .replace("{{FONT_BODY}}", b_font)
    
    # 2. GENERATE STATIC HTML SECTIONS
    nav_html = f"""
    <nav>
        <div class="container nav-flex">
            <a href="#home" style="font-size:1.5rem; font-weight:900;">{biz_name}</a>
            <div class="nav-links">
                <a href="#home" class="nav-link">Home</a>
                <a href="#store" class="nav-link">Store</a>
                <a href="#blog" class="nav-link">Blog</a>
                <a href="#booking" class="nav-link">Book</a>
                <a href="#contact" class="nav-link btn btn-sm">Contact</a>
            </div>
        </div>
    </nav>
    """
    
    hero_html = f"""
    <div id="view-home" class="view-section">
        <section class="hero" style="background-image: url('{hero_img}');">
            <div class="hero-overlay"></div>
            <div class="container hero-content reveal active">
                <h1>{hero_h}</h1>
                <p style="font-size:1.2rem; opacity:0.9; margin-bottom:2rem;">{hero_sub}</p>
                <a href="#store" class="btn btn-accent">Explore Store</a>
                <a href="#contact" class="btn btn-outline" style="color:white; border-color:white;">Contact Us</a>
            </div>
        </section>
        
        <section>
            <div class="container">
                <div class="grid-3">
                    <div class="card reveal active"><div class="card-body"><h3>⚡ {feat_1.split('|')[1]}</h3><p>{feat_1.split('|')[2]}</p></div></div>
                    <div class="card reveal active"><div class="card-body"><h3>💰 {feat_2.split('|')[1]}</h3><p>{feat_2.split('|')[2]}</p></div></div>
                    <div class="card reveal active"><div class="card-body"><h3>🛡️ {feat_3.split('|')[1]}</h3><p>{feat_3.split('|')[2]}</p></div></div>
                </div>
            </div>
        </section>
    </div>
    """
    
    store_html = f"""<div id="view-store" class="view-section" style="display:none; padding-top:80px;"><div class="container"><h2>Our Products</h2><div id="store-grid" class="grid-3"></div></div></div>"""
    blog_html = f"""<div id="view-blog" class="view-section" style="display:none; padding-top:80px;"><div class="container"><h2>Latest Insights</h2><div id="blog-grid" style="display:flex; flex-direction:column; gap:2rem; max-width:800px; margin:0 auto;"></div></div></div>"""
    
    booking_html = f"""
    <div id="view-booking" class="view-section" style="display:none; padding-top:80px;">
        <div class="container" style="text-align:center;">
            <h2>Schedule a Call</h2>
            <iframe src="{calendly}" width="100%" height="700" frameborder="0"></iframe>
        </div>
    </div>
    """
    
    contact_html = f"""
    <div id="view-contact" class="view-section" style="display:none; padding-top:80px;">
        <div class="container" style="max-width:600px;">
            <h2>Contact Us</h2>
            <div class="card"><div class="card-body">
                <p><strong>WhatsApp:</strong> {wa_num}</p>
                <p><strong>Email:</strong> support@{biz_name.lower()}.com</p>
                <a href="https://wa.me/{wa_num}" class="btn btn-accent" style="text-align:center;">Chat on WhatsApp</a>
            </div></div>
        </div>
    </div>
    """
    
    # PRODUCT DETAIL VIEW
    pd_html = f"""
    <div id="view-product-detail" class="view-section" style="display:none; padding-top:100px;">
        <div class="container">
            <a href="#store" class="btn btn-sm btn-outline" style="margin-bottom:2rem;">&larr; Back to Store</a>
            <div class="grid-3" style="grid-template-columns: 1fr 1fr;">
                <img id="pd-img" style="width:100%; border-radius:12px;">
                <div>
                    <h1 id="pd-title"></h1>
                    <h3 id="pd-price" style="color:var(--accent)"></h3>
                    <p id="pd-desc" style="margin-bottom:2rem;"></p>
                    <button id="pd-add" class="btn btn-accent">Add to Cart</button>
                </div>
            </div>
        </div>
    </div>
    """

    # BLOG DETAIL VIEW
    bp_html = f"""
    <div id="view-post-detail" class="view-section" style="display:none; padding-top:100px;">
        <div class="container" style="max-width:800px;">
            <a href="#blog" class="btn btn-sm btn-outline" style="margin-bottom:2rem;">&larr; Back to Blog</a>
            <img id="bp-img" style="width:100%; height:400px; object-fit:cover; border-radius:12px; margin-bottom:2rem;">
            <h1 id="bp-title"></h1>
            <div id="bp-content" style="line-height:1.8; font-size:1.1rem;"></div>
        </div>
    </div>
    """

    # CART HTML
    cart_html = f"""
    <div id="cart-float" onclick="toggleCart()">🛒 <span id="cart-count" style="font-size:0.8rem; position:absolute; top:0; right:0; background:red; width:20px; height:20px; border-radius:50%; display:flex; align-items:center; justify-content:center;">0</span></div>
    <div id="cart-modal">
        <div class="modal-content">
            <h3>Your Cart <span style="float:right; cursor:pointer;" onclick="toggleCart()">&times;</span></h3>
            <div id="cart-list" style="margin:1rem 0; max-height:300px; overflow-y:auto;"></div>
            <button onclick="checkout()" class="btn btn-accent" style="width:100%;">Checkout via WhatsApp</button>
        </div>
    </div>
    """

    # 3. ASSEMBLE JS CONFIG
    js_config = f"""
    <script>
    const CONFIG = {{
        storeUrl: "{store_url}",
        blogUrl: "{blog_url}",
        whatsapp: "{wa_num}",
        placeholderImg: "{def_img}"
    }};
    </script>
    """

    # 4. FINAL HTML
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{biz_name} | Titan Engine</title>
        <meta name="description" content="{seo_desc}">
        <link href="https://fonts.googleapis.com/css2?family={h_font.replace(' ','+')}:wght@700;900&family={b_font.replace(' ','+')}:wght@300;400;600&display=swap" rel="stylesheet">
        {css}
        <!-- Google Analytics -->
        <script async src="https://www.googletagmanager.com/gtag/js?id={ga_id}"></script>
        <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','{ga_id}');</script>
    </head>
    <body>
        {nav_html}
        {hero_html}
        {store_html}
        {blog_html}
        {booking_html}
        {contact_html}
        {pd_html}
        {bp_html}
        {cart_html}
        <footer style="background:var(--primary); color:white; padding:2rem; text-align:center; margin-top:4rem;">
            <p>{legal_txt}</p>
        </footer>
        {js_config}
        {TITAN_JS_CORE}
    </body>
    </html>
    """
    return html

# --- 4. OUTPUT ---
st.divider()

if st.button("🚀 IGNITE TITAN ENGINE (GENERATE SITE)", type="primary"):
    final_html = build_spa()
    
    # ZIP CREATION
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zf:
        zf.writestr("index.html", final_html)
        zf.writestr("manifest.json", json.dumps({
            "name": biz_name, "short_name": biz_name, "start_url": ".", "display": "standalone",
            "background_color": bg_color, "theme_color": p_color, 
            "icons": [{"src": def_img, "sizes": "512x512", "type": "image/png"}]
        }))
        zf.writestr("sw.js", "self.addEventListener('fetch', e => e.respondWith(fetch(e.request).catch(() => caches.match(e.request))));")
    
    c1, c2 = st.columns([2, 1])
    with c1:
        st.success("✅ Build Successful: 100/100 Lighthouse Score Architecture")
        st.markdown(f"**Stats:** 0 Database Calls | Client-Side Hydration | SPA Routing Active")
    with c2:
        st.download_button("📥 DOWNLOAD DEPLOYABLE ZIP", zip_buffer.getvalue(), "titan_v50_site.zip", "application/zip")
    
    # PREVIEW
    st.components.v1.html(final_html, height=800, scrolling=True)
