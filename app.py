import streamlit as st
import zipfile
import io
import json
import datetime
import re
import requests

# --- 0. STATE MANAGEMENT ---
def init_state(key, default_val):
    if key not in st.session_state:
        st.session_state[key] = default_val

init_state('hero_h', "Stop Paying Rent for Your Website.")
init_state('hero_sub', "The Titan Engine is the world’s first 0.1s website architecture that runs on $0 monthly fees. Pay once. Own it forever.")
init_state('about_h', "Control Your Empire")
init_state('about_short', "No WordPress dashboard. No plugins to update. Just open your private Google Sheet, change a text, and watch your site update globally in seconds.")
init_state('feat_data', "bolt | The Performance Pillar | **0.1s High-Velocity Loading**. While traditional sites take 3–5s, Titan loads instantly.\nwallet | The Economic Pillar | **$0 Monthly Fees**. We eliminated hosting subscriptions.\ntable | The Functional Pillar | **Google Sheets CMS**. Update prices and photos directly from a simple spreadsheet.\nshield | The Authority Pillar | **Unhackable Security**. Zero-DB Architecture removes the hacker's primary entry point.\nlayers | The Reliability Pillar | **Global Edge Deployment**. Distributed across 100+ servers worldwide.\nstar | The Conversion Pillar | **One-Tap WhatsApp**. Direct-to-Chat technology.")

# --- 1. APP CONFIGURATION ---
st.set_page_config(page_title="Titan v43.0 | 13-File Core", layout="wide", page_icon="💎")

# --- 2. STREAMLIT UI ---
st.markdown("""
    <style>
    :root { --primary: #0f172a; --accent: #ef4444; }
    .stApp { background-color: #f8fafc; color: #1e293b; font-family: sans-serif; }
    [data-testid="stSidebar"] { background-color: #ffffff; border-right: 1px solid #e2e8f0; }
    .stButton>button { width: 100%; border-radius: 8px; background: linear-gradient(135deg, #0f172a 0%, #334155 100%); color: white; border: none; height: 3rem; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR ---
with st.sidebar:
    st.title("Titan Architect")
    st.caption("v43.0 | Full Restoration")
    st.divider()
    
    with st.expander("🤖 AI Generator"):
        raw_key = st.text_input("Groq API Key", type="password")
        biz_desc = st.text_input("Business Description")
        if st.button("Generate Copy"):
            if not raw_key or not biz_desc: st.error("Key & Desc required")
            else:
                # Mock AI logic for speed/safety in snippet, replace with real req if needed
                st.success("AI Generation Simulated (Add API logic here)")

    with st.expander("🎨 Design Studio", expanded=True):
        theme_mode = st.selectbox("Theme", ["Ocean Breeze (Light)", "Midnight (Dark)", "Luxury Gold"])
        c1, c2 = st.columns(2)
        p_color = c1.color_picker("Primary", "#0F172A") 
        s_color = c2.color_picker("Accent", "#EF4444")
        h_font = st.selectbox("Headings", ["Outfit", "Montserrat", "Playfair Display"])
        b_font = st.selectbox("Body", ["Plus Jakarta Sans", "Inter", "Roboto"])
        hero_layout = st.selectbox("Hero Align", ["Center", "Left"])

    with st.expander("🧩 Modules"):
        show_hero = st.checkbox("Hero", True)
        show_stats = st.checkbox("Stats", True)
        show_features = st.checkbox("Features", True)
        show_pricing = st.checkbox("Pricing", True)
        show_inventory = st.checkbox("Store", True)
        show_blog = st.checkbox("Blog", True)
        show_booking = st.checkbox("Booking", True)

# --- 4. MAIN TABS ---
tabs = st.tabs(["Brand", "Content", "Pricing", "Store", "Booking", "Blog", "Legal"])

with tabs[0]:
    c1, c2 = st.columns(2)
    with c1:
        biz_name = st.text_input("Business Name", "StopWebRent.com")
        biz_phone = st.text_input("Phone", "919007406953")
        biz_email = st.text_input("Email", "hello@kaydiem.com")
    with c2:
        prod_url = st.text_input("URL", "https://www.stopwebrent.com")
        biz_addr = st.text_area("Address", "Kolkata, India")
        logo_url = st.text_input("Logo URL")
    
    st.subheader("Socials")
    s1, s2, s3, s4 = st.columns(4)
    fb_link = s1.text_input("Facebook")
    ig_link = s2.text_input("Instagram")
    x_link = s3.text_input("Twitter")
    wa_num = s4.text_input("WhatsApp (No +)", "919007406953")
    lang_sheet = st.text_input("Lang CSV URL")

with tabs[1]:
    hero_h = st.text_input("Hero H1", key="hero_h")
    hero_sub = st.text_input("Hero Sub", key="hero_sub")
    hero_img = st.text_input("Hero Image", "https://images.unsplash.com/photo-1460925895917-afdab827c52f?q=80&w=1600")
    feat_data_input = st.text_area("Features (icon|title|desc)", key="feat_data")
    about_h = st.text_input("About Title", key="about_h")
    about_txt = st.text_area("About Text", key="about_short")
    about_img = st.text_input("About Image", "https://images.unsplash.com/photo-1556761175-5973dc0f32e7")

with tabs[2]:
    titan_price = st.text_input("Price", "$199")
    wix_name = st.text_input("Competitor", "Wix")

with tabs[3]:
    sheet_url = st.text_input("Store CSV")
    custom_feat = st.text_input("Default Product", "https://images.unsplash.com/photo-1505740420928-5e560c06d30e")
    paypal_link = st.text_input("PayPal Link")
    upi_id = st.text_input("UPI ID")

with tabs[4]:
    booking_embed = st.text_area("Calendly Embed", '<!-- Calendly -->')

with tabs[5]:
    blog_sheet_url = st.text_input("Blog CSV")

with tabs[6]:
    priv_txt = st.text_area("Privacy", "We respect privacy.")
    term_txt = st.text_area("Terms", "Terms apply.")

# ==========================================
# 5. COMPILER ENGINE (RESTORED FULL UI)
# ==========================================

def get_css():
    # Theme Logic
    bg, txt, card, nav = "#F8FAFC", "#0F172A", "rgba(255,255,255,0.8)", "rgba(255,255,255,0.95)"
    if "Midnight" in theme_mode: bg, txt, card, nav = "#0f172a", "#f8fafc", "#1e293b", "rgba(15,23,42,0.95)"
    
    align = "center" if hero_layout == "Center" else "flex-start"
    t_align = "center" if hero_layout == "Center" else "left"

    return f"""
    :root {{ --p: {p_color}; --s: {s_color}; --bg: {bg}; --txt: {txt}; --card: {card}; --nav: {nav}; --font-h: '{h_font}', sans-serif; --font-b: '{b_font}', sans-serif; }}
    * {{ box-sizing: border-box; outline: none; }}
    body {{ background: var(--bg); color: var(--txt); font-family: var(--font-b); margin: 0; line-height: 1.6; overflow-x: hidden; }}
    h1, h2, h3, h4 {{ font-family: var(--font-h); color: var(--txt); margin-bottom: 1rem; line-height: 1.2; }}
    h1 {{ font-size: clamp(2.5rem, 5vw, 4rem); font-weight: 800; }}
    a {{ text-decoration: none; color: inherit; transition: 0.3s; }}
    
    .container {{ max-width: 1200px; margin: 0 auto; padding: 0 20px; }}
    
    /* BUTTONS */
    .btn {{ display: inline-flex; align-items: center; justify-content: center; padding: 0.8rem 2rem; border-radius: 8px; font-weight: 700; text-transform: uppercase; cursor: pointer; border: none; font-size: 0.9rem; transition: 0.3s; }}
    .btn-primary {{ background: var(--p); color: white !important; }}
    .btn-primary:hover {{ transform: translateY(-3px); box-shadow: 0 10px 20px -5px rgba(0,0,0,0.3); }}
    .btn-outline {{ border: 2px solid var(--p); color: var(--p) !important; background: transparent; }}
    .btn-outline:hover {{ background: var(--p); color: white !important; }}

    /* NAV */
    nav {{ position: fixed; top: 0; width: 100%; z-index: 1000; background: var(--nav); backdrop-filter: blur(10px); border-bottom: 1px solid rgba(0,0,0,0.1); padding: 1rem 0; }}
    .nav-flex {{ display: flex; justify-content: space-between; align-items: center; }}
    .nav-links {{ display: flex; gap: 2rem; align-items: center; }}
    .nav-links a {{ font-weight: 600; opacity: 0.8; }}
    .nav-links a:hover {{ opacity: 1; color: var(--p); }}
    
    /* HERO */
    .hero {{ position: relative; min-height: 80vh; display: flex; align-items: center; justify-content: {align}; text-align: {t_align}; padding-top: 80px; background: url('{hero_img}') center/cover no-repeat; }}
    .hero::before {{ content:''; position: absolute; top:0; left:0; width:100%; height:100%; background: rgba(0,0,0,0.6); }}
    .hero-content {{ position: relative; z-index: 2; color: white; max-width: 800px; }}
    .hero h1 {{ color: white; text-shadow: 0 4px 10px rgba(0,0,0,0.3); }}
    
    /* GRID SYSTEM */
    .grid-3 {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem; margin-top: 2rem; }}
    .card {{ background: var(--card); padding: 2rem; border-radius: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.05); border: 1px solid rgba(0,0,0,0.05); transition: 0.3s; display: flex; flex-direction: column; height: 100%; }}
    .card:hover {{ transform: translateY(-5px); box-shadow: 0 15px 30px rgba(0,0,0,0.1); }}
    
    /* PRODUCT CARD SPECIFIC */
    .prod-img {{ width: 100%; height: 250px; object-fit: cover; border-radius: 12px; margin-bottom: 1rem; }}
    .prod-price {{ font-size: 1.25rem; font-weight: 800; color: var(--s); margin: 0.5rem 0; }}
    
    /* CONTACT PAGE GRID */
    .contact-grid {{ display: grid; grid-template-columns: 1fr 1.5fr; gap: 4rem; }}
    .contact-info {{ background: var(--p); color: white; padding: 2rem; border-radius: 16px; }}
    .contact-info a {{ color: white; text-decoration: underline; }}
    
    /* FOOTER PROFESSIONAL */
    footer {{ background: #0f172a; color: white; padding: 4rem 0; margin-top: 4rem; }}
    .footer-grid {{ display: grid; grid-template-columns: 1.5fr 1fr 1fr; gap: 3rem; }}
    footer a {{ display: block; margin-bottom: 0.5rem; opacity: 0.7; }}
    footer a:hover {{ opacity: 1; color: white; }}
    .social-icon {{ width: 24px; height: 24px; fill: white; margin-right: 15px; opacity: 0.8; }}
    
    /* MODAL */
    .modal {{ display: none; position: fixed; z-index: 2000; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); backdrop-filter: blur(5px); }}
    .modal-content {{ background: var(--bg); margin: 15% auto; padding: 2rem; border-radius: 16px; width: 90%; max-width: 400px; position: relative; color: var(--txt); }}
    
    /* RESPONSIVE */
    @media (max-width: 768px) {{
        .nav-links {{ display: none; }} /* Mobile menu needs JS toggle */
        .contact-grid, .footer-grid {{ grid-template-columns: 1fr; gap: 2rem; }}
        h1 {{ font-size: 2.5rem; }}
    }}
    """

def gen_nav():
    lang_btn = f'<button onclick="openModal(\'langModal\')" class="btn-outline" style="padding:0.5rem 1rem; border-radius:50px;">🌐 Lang</button>' if lang_sheet else ""
    return f"""
    <nav><div class="container nav-flex">
        <a href="index.html" style="font-size:1.5rem; font-weight:900; color:var(--p);">{biz_name}</a>
        <div class="nav-links">
            <a href="index.html">Home</a>
            <a href="product.html">Store</a>
            <a href="blog.html">Blog</a>
            <a href="contact.html">Contact</a>
            {lang_btn}
            <a href="tel:{biz_phone}" class="btn-primary">Call Now</a>
        </div>
    </div></nav>
    <div id="langModal" class="modal"><div class="modal-content"><span onclick="document.getElementById('langModal').style.display='none'" style="float:right; cursor:pointer; font-size:1.5rem;">&times;</span><h3>Select Language</h3><button onclick="toggleLang()" class="btn-primary" style="width:100%">Switch Language</button></div></div>
    """

def gen_footer():
    # PROFESSIONAL 3-COLUMN FOOTER
    return f"""
    <footer><div class="container">
        <div class="footer-grid">
            <div>
                <h3 style="color:white">{biz_name}</h3>
                <p style="opacity:0.7">{biz_addr}</p>
                <div style="margin-top:1.5rem">
                    {f'<a href="{fb_link}" style="display:inline"><svg class="social-icon" viewBox="0 0 24 24"><path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"></path></svg></a>' if fb_link else ''}
                    {f'<a href="{ig_link}" style="display:inline"><svg class="social-icon" viewBox="0 0 24 24"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2a2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6zM2 9h4v12H2zM4 2a2 2 0 1 1-2 2a2 2 0 0 1 2-2z"></path></svg></a>' if li_link else ''}
                </div>
            </div>
            <div>
                <h4 style="color:white">Links</h4>
                <a href="index.html">Home</a>
                <a href="product.html">Store</a>
                <a href="blog.html">Blog</a>
                <a href="booking.html">Book Now</a>
            </div>
            <div>
                <h4 style="color:white">Legal</h4>
                <a href="privacy.html">Privacy Policy</a>
                <a href="terms.html">Terms of Service</a>
            </div>
        </div>
        <div style="text-align:center; border-top:1px solid rgba(255,255,255,0.1); margin-top:3rem; padding-top:2rem; opacity:0.5;">
            &copy; {datetime.date.today().year} {biz_name}. Powered by Titan Engine.
        </div>
    </div></footer>
    """

def gen_js():
    return f"""
    <script>
    // CSV PARSER
    function parseCSVLine(str) {{ const res = []; let cur = ''; let inQuote = false; for (let i = 0; i < str.length; i++) {{ const c = str[i]; if (c === '"') {{ if (inQuote && str[i+1] === '"') {{ cur += '"'; i++; }} else {{ inQuote = !inQuote; }} }} else if (c === ',' && !inQuote) {{ res.push(cur.trim()); cur = ''; }} else {{ cur += c; }} }} res.push(cur.trim()); return res; }}
    
    // CART SYSTEM
    let cart = JSON.parse(localStorage.getItem('titanCart')) || [];
    function addToCart(name, price) {{ cart.push({{name, price}}); updateCart(); alert('Added to cart'); }}
    function updateCart() {{ 
        const el = document.getElementById('cart-count'); 
        if(el) el.innerText = cart.length; 
        localStorage.setItem('titanCart', JSON.stringify(cart));
    }}
    function checkoutWA() {{
        let msg = "New Order:\\n";
        cart.forEach(i => msg += i.name + " - " + i.price + "\\n");
        window.open("https://wa.me/{wa_num}?text=" + encodeURIComponent(msg), '_blank');
    }}
    
    // LANG SWITCHER
    async function toggleLang() {{
        try {{
            const res = await fetch('{lang_sheet}'); const txt = await res.text();
            const lines = txt.split(/\\r\\n|\\n/);
            for(let i=1; i<lines.length; i++) {{
                const row = parseCSVLine(lines[i]);
                if(row.length > 1) {{ 
                    const el = document.getElementById(row[0]); 
                    if(el) el.innerText = row[1]; 
                }}
            }}
            document.getElementById('langModal').style.display = 'none';
        }} catch(e) {{ alert('Language file not found or invalid'); }}
    }}
    
    function openModal(id) {{ document.getElementById(id).style.display = 'block'; }}
    window.onload = updateCart;
    </script>
    """

def gen_cart_modal():
    return """
    <div id="cart-float" onclick="openModal('cartModal')" style="position:fixed; bottom:30px; right:30px; background:var(--p); color:white; padding:15px; border-radius:50px; cursor:pointer; z-index:999; box-shadow:0 10px 20px rgba(0,0,0,0.2);">
        🛒 <span id="cart-count">0</span>
    </div>
    <div id="cartModal" class="modal"><div class="modal-content">
        <span onclick="document.getElementById('cartModal').style.display='none'" style="float:right; cursor:pointer;">&times;</span>
        <h3>Your Cart</h3>
        <button onclick="checkoutWA()" class="btn-primary" style="width:100%; margin-top:1rem;">Checkout on WhatsApp</button>
        <button onclick="localStorage.removeItem('titanCart'); location.reload();" class="btn-outline" style="width:100%; margin-top:0.5rem;">Clear Cart</button>
    </div></div>
    """

def gen_page(title, content):
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title} | {biz_name}</title><link href="https://fonts.googleapis.com/css2?family={h_font.replace(' ','+')}:wght@700&family={b_font.replace(' ','+')}:wght@400;600&display=swap" rel="stylesheet"><style>{get_css()}</style></head><body>{gen_nav()}{content}{gen_footer()}{gen_cart_modal()}{gen_js()}</body></html>"""

# --- PAGE CONTENT GENERATORS ---

def get_home_content():
    # Features
    feat_html = ""
    for line in feat_data.split('\n'):
        if "|" in line:
            parts = line.split('|')
            if len(parts) >= 3: feat_html += f'<div class="card"><h3>{parts[1]}</h3><p>{parts[2]}</p></div>'
            
    return f"""
    {gen_hero()}
    <section class="container">
        <h2 style="text-align:center; margin-bottom:2rem;">Features</h2>
        <div class="grid-3">{feat_html}</div>
    </section>
    <section style="background:var(--p); color:white; text-align:center;">
        <div class="container"><h2>Start Today</h2><a href="contact.html" class="btn" style="background:white; color:var(--p)">Get Started</a></div>
    </section>
    """

def get_product_content():
    return f"""
    <section class="container" style="padding-top:120px;">
        <h1 style="text-align:center;">Portfolio & Store</h1>
        <div id="store-grid" class="grid-3">Loading products...</div>
    </section>
    <script>
    async function loadStore() {{
        const box = document.getElementById('store-grid');
        if(!'{sheet_url}') {{
            box.innerHTML = `<div class="card"><img src="{custom_feat}" class="prod-img"><h3>Demo Product</h3><p class="prod-price">$99.00</p><button class="btn-primary btn" onclick="addToCart('Demo', '$99')">Add to Cart</button></div>`;
            return;
        }}
        try {{
            const res = await fetch('{sheet_url}'); const txt = await res.text(); const lines = txt.split(/\\r\\n|\\n/);
            box.innerHTML = '';
            for(let i=1; i<lines.length; i++) {{
                const r = parseCSVLine(lines[i]);
                if(r.length > 1) {{
                    let img = (r[3] && r[3].length > 5) ? r[3].split('|')[0] : '{custom_feat}';
                    box.innerHTML += `<div class="card"><img src="${{img}}" class="prod-img"><h3>${{r[0]}}</h3><p class="prod-price">${{r[1]}}</p><p>${{r[2]}}</p><button class="btn-primary btn" style="width:100%" onclick="addToCart('${{r[0].replace(/'/g,"\\'")}}', '${{r[1].replace(/'/g,"\\'")}}')">Add to Cart</button></div>`;
                }}
            }}
        }} catch(e) {{ console.log(e); }}
    }}
    loadStore();
    </script>
    """

def get_blog_content():
    return f"""
    <section class="container" style="padding-top:120px;">
        <h1 style="text-align:center;">{blog_hero_title}</h1>
        <div id="blog-grid" class="grid-3">Loading posts...</div>
    </section>
    <script>
    async function loadBlog() {{
        const box = document.getElementById('blog-grid');
        if(!'{blog_sheet_url}') {{ box.innerHTML = '<p style="text-align:center">No blog connected.</p>'; return; }}
        try {{
            const res = await fetch('{blog_sheet_url}'); const txt = await res.text(); const lines = txt.split(/\\r\\n|\\n/);
            box.innerHTML = '';
            for(let i=1; i<lines.length; i++) {{
                const r = parseCSVLine(lines[i]);
                if(r.length > 4) {{
                    box.innerHTML += `<div class="card"><img src="${{r[5]}}" class="prod-img"><span class="blog-badge">${{r[3]}}</span><h3><a href="post.html?id=${{r[0]}}">${{r[1]}}</a></h3></div>`;
                }}
            }}
        }} catch(e) {{}}
    }}
    loadBlog();
    </script>
    """

def get_post_content():
    return f"""
    <div id="post-content" class="container" style="padding-top:120px; max-width:800px;">Loading...</div>
    <script>
    async function loadSingle() {{
        const id = new URLSearchParams(window.location.search).get('id');
        try {{
            const res = await fetch('{blog_sheet_url}'); const txt = await res.text(); const lines = txt.split(/\\r\\n|\\n/);
            for(let i=1; i<lines.length; i++) {{
                const r = parseCSVLine(lines[i]);
                if(r[0] === id) {{
                    document.getElementById('post-content').innerHTML = `<h1>${{r[1]}}</h1><img src="${{r[5]}}" style="width:100%; border-radius:12px; margin:2rem 0;"><div style="line-height:1.8">${{r[6].replace(/\\n/g,'<br>')}}</div>`;
                }}
            }}
        }} catch(e) {{}}
    }}
    loadSingle();
    </script>
    """

def get_contact_content():
    return f"""
    <section class="container" style="padding-top:120px;">
        <h1 style="text-align:center; margin-bottom:3rem;">Contact Us</h1>
        <div class="contact-grid">
            <div class="contact-info">
                <h3>Get In Touch</h3>
                <p>📍 {biz_addr}</p>
                <p>📞 <a href="tel:{biz_phone}">{biz_phone}</a></p>
                <p>✉️ <a href="mailto:{biz_email}">{biz_email}</a></p>
                <div style="margin-top:2rem;">
                    <a href="https://wa.me/{wa_num}" class="btn" style="background:white; color:var(--p); width:100%; display:block; text-align:center;">Chat on WhatsApp</a>
                </div>
            </div>
            <div class="card">
                <h3>Send Message</h3>
                <form action="https://formsubmit.co/{biz_email}" method="POST">
                    <input type="text" name="name" placeholder="Your Name" required>
                    <input type="email" name="email" placeholder="Your Email" required>
                    <textarea name="msg" rows="5" placeholder="Message"></textarea>
                    <button type="submit" class="btn-primary btn" style="width:100%">Send</button>
                </form>
            </div>
        </div>
        <div style="margin-top:4rem; border-radius:12px; overflow:hidden;">{map_iframe}</div>
    </section>
    """

# --- 6. DOWNLOAD HANDLER (13 FILES) ---
st.divider()
st.subheader("🚀 Final Output")

# PREVIEW
preview = st.radio("Preview", ["Home", "Store", "Contact"], horizontal=True)
if preview == "Home": st.components.v1.html(gen_page("Home", get_home_content()), height=600, scrolling=True)
elif preview == "Store": st.components.v1.html(gen_page("Store", get_product_content()), height=600, scrolling=True)
elif preview == "Contact": st.components.v1.html(gen_page("Contact", get_contact_content()), height=600, scrolling=True)

# ZIP CREATION
if st.button("GENERATE FULL WEBSITE ZIP", type="primary"):
    z_b = io.BytesIO()
    with zipfile.ZipFile(z_b, "a", zipfile.ZIP_DEFLATED, False) as zf:
        # 1. HTML FILES
        zf.writestr("index.html", gen_page("Home", get_home_content()))
        zf.writestr("about.html", gen_page("About", f"<section class='container' style='padding-top:120px'><h1>{about_h}</h1><div class='grid-3'><div>{about_txt}</div><img src='{about_img}' style='width:100%;border-radius:12px'></div></section>"))
        zf.writestr("contact.html", gen_page("Contact", get_contact_content()))
        zf.writestr("product.html", gen_page("Store", get_product_content()))
        zf.writestr("blog.html", gen_page("Blog", get_blog_content()))
        zf.writestr("post.html", gen_page("Article", get_post_content()))
        zf.writestr("booking.html", gen_page("Booking", f"<section class='container' style='padding-top:120px'><h1 style='text-align:center'>Book Now</h1>{booking_embed}</section>"))
        zf.writestr("privacy.html", gen_page("Privacy Policy", f"<section class='container' style='padding-top:120px'><h1>Privacy Policy</h1><p>{priv_txt}</p></section>"))
        zf.writestr("terms.html", gen_page("Terms of Service", f"<section class='container' style='padding-top:120px'><h1>Terms</h1><p>{term_txt}</p></section>"))
        
        # 2. SYSTEM FILES
        zf.writestr("manifest.json", gen_pwa_manifest())
        zf.writestr("service-worker.js", gen_sw())
        zf.writestr("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {prod_url}/sitemap.xml")
        zf.writestr("sitemap.xml", f"""<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>{prod_url}/</loc></url></urlset>""")

    st.download_button("📥 Click to Download 13 Files", z_b.getvalue(), "titan_v43_complete.zip", "application/zip")
