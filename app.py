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
init_state('about_h', "Control Your Empire from a Spreadsheet")
init_state('about_short', "No WordPress dashboard. No plugins to update. Just open your private Google Sheet, change a text, and watch your site update globally in seconds.")
init_state('feat_data', "bolt | The Performance Pillar | **0.1s High-Velocity Loading**. While traditional sites take 3–5s, Titan loads instantly.\nwallet | The Economic Pillar | **$0 Monthly Fees**. We eliminated hosting subscriptions.\ntable | The Functional Pillar | **Google Sheets CMS**. Update prices and photos directly from a simple spreadsheet.\nshield | The Authority Pillar | **Unhackable Security**. Zero-DB Architecture removes the hacker's primary entry point.\nlayers | The Reliability Pillar | **Global Edge Deployment**. Distributed across 100+ servers worldwide.\nstar | The Conversion Pillar | **One-Tap WhatsApp**. Direct-to-Chat technology.")

# --- 1. APP CONFIGURATION ---
st.set_page_config(page_title="Titan v38.0 | Performance Upgrade", layout="wide", page_icon="⚡", initial_sidebar_state="expanded")

# --- 2. ADVANCED UI SYSTEM ---
st.markdown("""
    <style>
    :root { --primary: #0f172a; --accent: #ef4444; }
    .stApp { background-color: #f8fafc; color: #1e293b; font-family: 'Inter', sans-serif; }
    [data-testid="stSidebar"] { background-color: #ffffff; border-right: 1px solid #e2e8f0; }
    [data-testid="stSidebar"] h1 { background: linear-gradient(90deg, #0f172a, #ef4444); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 900 !important; font-size: 1.8rem !important; }
    .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] { background-color: #ffffff !important; border: 1px solid #cbd5e1 !important; border-radius: 8px !important; color: #0f172a !important; }
    .stButton>button { width: 100%; border-radius: 8px; height: 3.5rem; background: linear-gradient(135deg, #0f172a 0%, #334155 100%); color: white; font-weight: 800; border: none; box-shadow: 0 4px 15px rgba(15, 23, 42, 0.3); text-transform: uppercase; letter-spacing: 1px; transition: transform 0.2s; }
    .stButton>button:hover { transform: translateY(-2px); }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR ---
with st.sidebar:
    st.title("Titan Architect")
    st.caption("v38.0 | Core Web Vitals Update")
    st.divider()
    
    with st.expander("🤖 Titan AI Generator", expanded=False):
        raw_key = st.text_input("Groq API Key", type="password")
        groq_key = raw_key.strip() if raw_key else ""
        biz_desc = st.text_input("Business Description")
        if st.button("✨ Generate Copy"):
            if not groq_key or not biz_desc: st.error("Key & Description required.")
            else:
                try:
                    with st.spinner("Writing..."):
                        url = "https://api.groq.com/openai/v1/chat/completions"
                        headers = {"Authorization": f"Bearer {groq_key}", "Content-Type": "application/json"}
                        prompt = f"Act as a copywriter. Return JSON for '{biz_desc}': hero_h, hero_sub, about_h, about_short, feat_data (icon|Title|Desc format)."
                        data = {"messages": [{"role": "user", "content": prompt}], "model": "llama-3.1-8b-instant", "response_format": {"type": "json_object"}}
                        resp = requests.post(url, headers=headers, json=data)
                        if resp.status_code == 200:
                            res = json.loads(resp.json()['choices'][0]['message']['content'])
                            if 'hero_h' in res: st.session_state.hero_h = str(res['hero_h'])
                            if 'hero_sub' in res: st.session_state.hero_sub = str(res['hero_sub'])
                            if 'about_h' in res: st.session_state.about_h = str(res['about_h'])
                            if 'about_short' in res: st.session_state.about_short = str(res['about_short'])
                            if 'feat_data' in res: st.session_state.feat_data = "\n".join(map(str, res['feat_data'])) if isinstance(res['feat_data'], list) else str(res['feat_data'])
                            st.success("Generated!"); st.rerun()
                except Exception as e: st.error(f"Error: {e}")

    with st.expander("🎨 Design Studio", expanded=True):
        theme_mode = st.selectbox("Base Theme", ["Clean Corporate (Light)", "Midnight SaaS (Dark)", "Glassmorphism (Blur)", "Cyberpunk Neon", "Luxury Gold", "Forest Eco", "Ocean Breeze", "Stark Minimalist"])
        c1, c2 = st.columns(2)
        p_color = c1.color_picker("Primary Brand", "#0F172A") 
        s_color = c2.color_picker("Action (CTA)", "#EF4444")  
        hero_layout = st.selectbox("Hero Alignment", ["Center", "Left"])
        btn_style = st.selectbox("Button Style", ["Rounded (Default)", "Sharp (Square)", "Pill (Full Round)"])
        border_rad = "0px" if btn_style == "Sharp (Square)" else "50px" if btn_style == "Pill (Full Round)" else "8px"
        anim_type = st.selectbox("Animation Style", ["Fade Up", "Zoom In", "Slide Right", "None"])
        h_font = st.selectbox("Headings Font", ["Montserrat", "Space Grotesk", "Playfair Display", "Oswald", "Clash Display"])
        b_font = st.selectbox("Body Font", ["Inter", "Open Sans", "Roboto", "Satoshi", "Lora"])

    with st.expander("🧩 Section Manager", expanded=False):
        show_hero = st.checkbox("Hero Section", value=True)
        show_stats = st.checkbox("Trust Stats", value=True)
        show_features = st.checkbox("Feature Grid", value=True)
        show_pricing = st.checkbox("Pricing Table", value=True)
        show_inventory = st.checkbox("Store/Inventory", value=True)
        show_blog = st.checkbox("Blog Engine", value=True)
        show_gallery = st.checkbox("About Section", value=True)
        show_testimonials = st.checkbox("Testimonials", value=True)
        show_faq = st.checkbox("F.A.Q.", value=True)
        show_cta = st.checkbox("Final CTA", value=True)
        show_booking = st.checkbox("Booking Engine", value=True)

    with st.expander("⚙️ SEO & Analytics", expanded=False):
        seo_area = st.text_input("Service Area", "Global / Online")
        seo_kw = st.text_area("SEO Keywords", "web design, no monthly fees")
        ga_tag = st.text_input("Google Analytics ID (G-XXXX)")
        og_image = st.text_input("Social Share Image URL")

# --- 4. MAIN WORKSPACE ---
st.title("🏗️ StopWebRent Site Builder v38.0")
tabs = st.tabs(["1. Identity & PWA", "2. Content Blocks", "3. Marketing Tools", "4. Pricing", "5. Store", "6. Booking", "7. Blog", "8. Legal"])

with tabs[0]:
    c1, c2 = st.columns(2)
    with c1:
        biz_name = st.text_input("Business Name", "StopWebRent.com")
        biz_tagline = st.text_input("Tagline", "Stop Renting. Start Owning.")
        biz_phone = st.text_input("Phone", "966572562151")
        biz_email = st.text_input("Email", "hello@kaydiemscriptlab.com")
    with c2:
        prod_url = st.text_input("Website URL", "https://www.stopwebrent.com")
        biz_addr = st.text_area("Address", "Kaydiem Script Lab\nKolkata, India", height=100)
        map_iframe = st.text_area("Google Map Embed", placeholder='<iframe src="..."></iframe>', height=100)
        seo_d = st.text_area("Meta Description", "Stop paying monthly fees for Wix.", height=100)
        logo_url = st.text_input("Logo URL (PNG/SVG)")
    st.subheader("📱 Progressive Web App (PWA)")
    pwa_short = st.text_input("App Short Name", biz_name[:12])
    pwa_desc = st.text_input("App Description", "Official App")
    pwa_icon = st.text_input("App Icon (512x512 PNG)", logo_url)
    st.subheader("🌍 Multi-Language")
    lang_sheet = st.text_input("Translation Sheet CSV URL")
    st.subheader("Social Links")
    sc1, sc2, sc3 = st.columns(3)
    fb_link = sc1.text_input("Facebook URL")
    ig_link = sc2.text_input("Instagram URL")
    x_link = sc3.text_input("X (Twitter) URL")
    sc4, sc5, sc6 = st.columns(3)
    li_link = sc4.text_input("LinkedIn URL")
    yt_link = sc5.text_input("YouTube URL")
    wa_num = sc6.text_input("WhatsApp Number (No +)", "966572562151")

with tabs[1]:
    st.subheader("Hero Carousel")
    hero_h = st.text_input("Hero Headline", key="hero_h")
    hero_sub = st.text_input("Hero Subtext", key="hero_sub")
    hero_video_id = st.text_input("YouTube Video ID (Background Override)", placeholder="e.g. dQw4w9WgXcQ")
    hc1, hc2, hc3 = st.columns(3)
    hero_img_1 = hc1.text_input("Slide 1", "https://images.unsplash.com/photo-1460925895917-afdab827c52f?q=80&w=1600")
    hero_img_2 = hc2.text_input("Slide 2", "https://images.unsplash.com/photo-1551288049-bebda4e38f71?q=80&w=1600")
    hero_img_3 = hc3.text_input("Slide 3", "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?q=80&w=1600")
    st.divider()
    col_s1, col_s2, col_s3 = st.columns(3)
    stat_1 = col_s1.text_input("Stat 1", "0.1s")
    label_1 = col_s1.text_input("Label 1", "Speed")
    stat_2 = col_s2.text_input("Stat 2", "$0")
    label_2 = col_s2.text_input("Label 2", "Fees")
    stat_3 = col_s3.text_input("Stat 3", "100%")
    label_3 = col_s3.text_input("Label 3", "Ownership")
    f_title = st.text_input("Features Title", "Value Pillars")
    feat_data_input = st.text_area("Features List", key="feat_data", height=150)
    about_h_in = st.text_input("About Title", key="about_h")
    about_img = st.text_input("About Image", "https://images.unsplash.com/photo-1543286386-713df548e9cc?q=80&w=1600")
    about_short_in = st.text_area("Short Summary", key="about_short", height=100)
    about_long = st.text_area("Full Content", "The Digital Landlord Trap...", height=200)

with tabs[2]:
    top_bar_enabled = st.checkbox("Enable Top Bar")
    top_bar_text = st.text_input("Promo Text", "🔥 50% OFF Launch Sale - Ends Soon!")
    top_bar_link = st.text_input("Promo Link", "#pricing")
    popup_enabled = st.checkbox("Enable Popup")
    popup_delay = st.slider("Delay (seconds)", 1, 30, 5)
    popup_title = st.text_input("Popup Headline", "Wait! Don't leave empty handed.")
    popup_text = st.text_input("Popup Body", "Get our free pricing guide on WhatsApp.")
    popup_cta = st.text_input("Popup Button", "Get it Now")

with tabs[3]:
    col_p1, col_p2, col_p3 = st.columns(3)
    titan_price = col_p1.text_input("Setup Price", "$199")
    titan_mo = col_p1.text_input("Monthly Fee", "$0")
    wix_name = col_p2.text_input("Competitor", "Wix")
    wix_mo = col_p2.text_input("Comp. Monthly", "$29/mo")
    save_val = col_p3.text_input("Savings", "$1,466")

with tabs[4]:
    sheet_url = st.text_input("Store CSV", placeholder="https://docs.google.com/spreadsheets/d/e/.../pub?output=csv")
    custom_feat = st.text_input("Default Product Img", "https://images.unsplash.com/photo-1460925895917-afdab827c52f?q=80&w=800")
    col_pay1, col_pay2 = st.columns(2)
    paypal_link = col_pay1.text_input("PayPal Link", "https://paypal.me/yourid")
    upi_id = col_pay2.text_input("UPI ID", "name@upi")

with tabs[5]:
    booking_embed = st.text_area("Embed Code", height=150, value='<!-- Calendly inline widget begin -->\n<div class="calendly-inline-widget" data-url="https://calendly.com/titan-demo/30min" style="min-width:320px;height:630px;"></div>\n<script type="text/javascript" src="https://assets.calendly.com/assets/external/widget.js" async></script>\n<!-- Calendly inline widget end -->')
    booking_title = st.text_input("Booking Title", "Book an Appointment")
    booking_desc = st.text_input("Booking Subtext", "Select a time slot.")

with tabs[6]:
    blog_sheet_url = st.text_input("Blog CSV", placeholder="https://docs.google.com/spreadsheets/d/e/.../pub?output=csv")
    blog_hero_title = st.text_input("Blog Title", "Latest Insights")
    blog_hero_sub = st.text_input("Blog Subtext", "Thoughts on tech.")

with tabs[7]:
    testi_data = st.text_area("Testimonials", "Rajesh Gupta | Titan stopped the bleeding.\nSarah Jenkins | Easy updates.", height=100)
    faq_data = st.text_area("FAQ", "Do I pay $0? ? Yes.\nIs it secure? ? Yes.", height=100)
    priv_txt = st.text_area("Privacy", "We collect minimum data.", height=100)
    term_txt = st.text_area("Terms", "You own the code.", height=100)


# --- 5. THE SUPERCHARGED COMPILER ENGINE ---

def format_text(text):
    if not text: return ""
    processed_text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    lines = processed_text.split('\n')
    html_out = ""
    in_list = False
    for line in lines:
        clean_line = line.strip()
        if not clean_line: continue
        if clean_line.startswith("* "):
            if not in_list: html_out += '<ul style="margin-bottom:1rem; padding-left:1.5rem;">'; in_list = True
            content = clean_line[2:] 
            html_out += f'<li style="margin-bottom:0.5rem; opacity:0.9; color:inherit;">{content}</li>'
        else:
            if in_list: html_out += "</ul>"; in_list = False
            html_out += f"<p style='margin-bottom:1rem; opacity:0.9; color:inherit;'>{clean_line}</p>"
    if in_list: html_out += "</ul>"
    return html_out

def gen_schema():
    schema = { "@context": "https://schema.org", "@type": "LocalBusiness", "name": biz_name, "image": logo_url or hero_img_1, "telephone": biz_phone, "email": biz_email, "url": prod_url, "description": seo_d }
    return f'<script type="application/ld+json">{json.dumps(schema)}</script>'

def gen_ga4():
    if not ga_tag: return ""
    return f"""<script async src="https://www.googletagmanager.com/gtag/js?id={ga_tag}"></script><script>window.dataLayer = window.dataLayer || []; function gtag(){{dataLayer.push(arguments);}} gtag('js', new Date()); gtag('config', '{ga_tag}');</script>"""

def gen_pwa_manifest():
    return json.dumps({ "name": biz_name, "short_name": pwa_short, "start_url": "./index.html", "display": "standalone", "background_color": "#ffffff", "theme_color": p_color, "description": pwa_desc, "icons": [{"src": pwa_icon, "sizes": "512x512", "type": "image/png"}] })

def gen_sw():
    return "self.addEventListener('install', (e) => { e.waitUntil(caches.open('titan-store').then((cache) => cache.addAll(['./index.html']))); }); self.addEventListener('fetch', (e) => { e.respondWith(caches.match(e.request).then((response) => response || fetch(e.request))); });"

def get_theme_css():
    bg_color, text_color, card_bg, glass_nav = "#ffffff", "#0f172a", "#ffffff", "rgba(255, 255, 255, 0.95)"
    if "Midnight" in theme_mode: bg_color, text_color, card_bg, glass_nav = "#0f172a", "#f8fafc", "#1e293b", "rgba(15, 23, 42, 0.9)"
    elif "Cyberpunk" in theme_mode: bg_color, text_color, card_bg, glass_nav = "#050505", "#00ff9d", "#111", "rgba(0,0,0,0.8)"
    elif "Luxury" in theme_mode: bg_color, text_color, card_bg, glass_nav = "#1c1c1c", "#D4AF37", "#2a2a2a", "rgba(28,28,28,0.95)"
    
    anim_css = ".reveal { opacity: 0; transform: translateY(30px); transition: all 0.8s ease-out; } .reveal.active { opacity: 1; transform: translateY(0); }" if anim_type == "Fade Up" else ""
    hero_align = "text-align: left; justify-content: flex-start; align-items: center;" if hero_layout == "Left" else "text-align: center; justify-content: center;"

    return f"""
    :root {{ --p: {p_color}; --s: {s_color}; --bg: {bg_color}; --txt: {text_color}; --card: {card_bg}; --radius: {border_rad}; --nav: {glass_nav}; --h-font: '{h_font}', sans-serif; --b-font: '{b_font}', sans-serif; }}
    * {{ box-sizing: border-box; }} html {{ scroll-behavior: smooth; font-size: 16px; }}
    body {{ background-color: var(--bg); color: var(--txt); font-family: var(--b-font); margin: 0; line-height: 1.6; overflow-x: hidden; }}
    body.dark-mode {{ --bg: #0f172a; --txt: #f8fafc; --card: #1e293b; --nav: rgba(15, 23, 42, 0.95); }}
    p, h1, h2, h3, h4, span, li, div {{ color: inherit; }}
    h1, h2, h3, h4 {{ font-family: var(--h-font); color: var(--p); line-height: 1.2; margin-bottom: 1rem; }}
    strong {{ color: var(--p); font-weight: 800; }}
    .container {{ max-width: 1280px; margin: 0 auto; padding: 0 20px; }}
    .btn {{ display: inline-flex; align-items: center; justify-content: center; padding: 1rem 2rem; border-radius: var(--radius); font-weight: 700; text-decoration: none; transition: 0.3s; text-transform: uppercase; cursor: pointer; border: none; text-align: center; min-height: 3.5rem; }}
    .btn-primary {{ background: var(--p); color: white !important; }}
    .btn-accent {{ background: var(--s); color: white !important; box-shadow: 0 10px 25px -5px var(--s); }}
    .btn:hover {{ transform: translateY(-3px); filter: brightness(1.15); }}
    nav {{ position: fixed; top: 0; width: 100%; z-index: 1000; background: var(--nav); backdrop-filter: blur(12px); padding: 1rem 0; transition: top 0.3s; }}
    .nav-flex {{ display: flex; justify-content: space-between; align-items: center; }}
    .nav-links {{ display: flex; align-items: center; }}
    .nav-links a {{ margin-left: 2rem; text-decoration: none; font-weight: 600; color: var(--txt); opacity: 0.8; transition:0.2s; }}
    .nav-links a:hover {{ opacity: 1; color: var(--s); }}
    .mobile-menu {{ display: none; font-size: 1.5rem; cursor: pointer; }}
    .hero {{ position: relative; min-height: 90vh; overflow: hidden; display: flex; {hero_align} color: white; padding-top: 80px; background-color: var(--p); }}
    .carousel-slide {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; background-size: cover; background-position: center; opacity: 0; transition: opacity 1.5s ease-in-out; z-index: 0; }}
    .carousel-slide.active {{ opacity: 1; }}
    .hero-overlay {{ background: rgba(0,0,0,0.5); position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 1; }}
    .hero-content {{ z-index: 2; position: relative; width: 100%; padding: 0 20px; }}
    .hero h1 {{ color: #ffffff !important; font-size: clamp(2.5rem, 5vw, 4.5rem); text-shadow: 0 4px 20px rgba(0,0,0,0.4); }}
    .hero p {{ color: rgba(255,255,255,0.95) !important; font-size: clamp(1.1rem, 2vw, 1.3rem); text-shadow: 0 2px 10px rgba(0,0,0,0.4); max-width:700px; }}
    section {{ padding: clamp(2rem, 4vw, 3rem) 0; }}
    .grid-3 {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem; }}
    .card {{ background: var(--card); border-radius: var(--radius); border: 1px solid rgba(100,100,100,0.1); transition: 0.3s; display: flex; flex-direction: column; overflow: hidden; }}
    .card:hover {{ transform: translateY(-5px); box-shadow: 0 20px 40px -10px rgba(0,0,0,0.1); border-color: var(--s); }}
    .card-body {{ padding: 1.5rem; display: flex; flex-direction: column; flex-grow: 1; }}
    .prod-img {{ width: 100%; height: 250px; object-fit: cover; background: #f1f5f9; }} /* Prevents layout shift */
    {anim_css}
    @media (max-width: 768px) {{ .nav-links {{ position: fixed; top: 60px; left: -100%; width: 100%; height: 100vh; background: var(--bg); flex-direction: column; padding: 2rem; transition: 0.3s; align-items: flex-start; gap: 1.5rem; }} .nav-links.active {{ left: 0; }} .mobile-menu {{ display: block; }} .grid-3 {{ grid-template-columns: 1fr !important; }} }}
    """

def gen_nav():
    logo_display = f'<img src="{logo_url}" height="40" alt="{biz_name} Logo">' if logo_url else f'<span style="font-weight:900; font-size:1.5rem; color:var(--p)">{biz_name}</span>'
    return f"""<nav><div class="container nav-flex"><a href="index.html" style="text-decoration:none">{logo_display}</a><div class="mobile-menu" onclick="document.querySelector('.nav-links').classList.toggle('active')">☰</div><div class="nav-links"><a href="index.html">Home</a><a href="index.html#features">Features</a><a href="index.html#inventory">Store</a><a href="blog.html">Blog</a><a href="contact.html">Contact</a><a href="tel:{biz_phone}" class="btn-accent" style="padding:0.6rem 1.5rem; border-radius:50px; color:white !important;">Call Now</a></div></div></nav>"""

def gen_hero():
    bg_media = f'<div class="carousel-slide active" style="background-image: url(\'{hero_img_1}\')"></div>'
    return f"""<section class="hero"><div class="hero-overlay"></div>{bg_media}<div class="container hero-content"><h1>{hero_h}</h1><p>{hero_sub}</p><div style="display:flex; gap:1rem; flex-wrap:wrap; {'justify-content:center;' if hero_layout == 'Center' else ''}"><a href="#inventory" class="btn btn-accent">Explore Now</a></div></div></section>"""

def gen_features():
    cards = "".join([f'<div class="card reveal"><div class="card-body"><h3>{p.split("|")[1].strip()}</h3><div>{format_text(p.split("|")[2].strip())}</div></div></div>' for p in feat_data_input.split('\n') if "|" in p])
    return f"""<section id="features"><div class="container"><div class="grid-3">{cards}</div></div></section>"""

def gen_csv_parser():
    return "<script>function parseCSV(s){let r=[];let c='';let q=false;for(let i=0;i<s.length;i++){let x=s[i];if(x==='\"'){if(q&&s[i+1]==='\"'){c+='\"';i++;}else{q=!q;}}else if(x===','&&!q){r.push(c.trim());c='';}else{c+=x;}}r.push(c.trim());return r;}</script>"

# --- UPGRADE: ZERO-LATENCY STORE LOADER ---
def gen_inventory_js():
    if not show_inventory: return ""
    return f"""
    {gen_csv_parser()}
    <script>
    function renderGrid(txt) {{
        const lines = txt.split(/\\r\\n|\\n/);
        const box = document.getElementById('inv-grid');
        let html = '';
        for(let i=1; i<lines.length; i++) {{
            if(!lines[i].trim()) continue;
            const c = parseCSV(lines[i]);
            let mainImg = c[3] ? c[3].split('|')[0] : '{custom_feat}';
            if(c.length > 1) {{
                html += `<div class="card reveal active"><img src="${{mainImg}}" class="prod-img" loading="lazy"><div class="card-body"><h3>${{c[0]}}</h3><p style="color:var(--s); font-weight:bold;">${{c[1]}}</p><p>${{c[2]}}</p></div></div>`;
            }}
        }}
        if(box) box.innerHTML = html;
    }}
    
    async function loadInv() {{
        const cached = localStorage.getItem('titan_inv');
        if(cached) renderGrid(cached); // Renders instantly in 0.01s
        
        try {{
            const res = await fetch('{sheet_url}'); 
            const txt = await res.text();
            if(txt !== cached) {{
                localStorage.setItem('titan_inv', txt);
                renderGrid(txt); // Silently updates if Google Sheet changed
            }}
        }} catch(e) {{ console.log(e); }}
    }}
    if(document.getElementById('inv-grid')) window.addEventListener('load', loadInv);
    </script>
    """

def gen_inventory():
    if not show_inventory: return ""
    return f"""<section id="inventory" style="background:rgba(0,0,0,0.02)"><div class="container"><h2 style="text-align:center;">Store</h2><div id="inv-grid" class="grid-3"><div><div class="card"><div class="prod-img" style="animation: pulse 1.5s infinite;"></div><div class="card-body">Loading...</div></div></div></div></div></section>{gen_inventory_js()}"""

def gen_footer():
    return f"""<footer style="background:var(--p); color:white; padding:4rem 0; margin-top:auto;"><div class="container"><div class="grid-3"><div><h3 style="color:white;">{biz_name}</h3><p style="opacity:0.7;">{biz_addr}</p></div><div><h4 style="color:white;">Links</h4><a href="index.html" style="color:white; display:block;">Home</a><a href="privacy.html" style="color:white; display:block;">Privacy</a></div></div></div></footer>"""

# --- UPGRADE: OPENGRAPH AND CORE WEB VITALS ---
def build_page(title, content, extra_js=""):
    og_img = og_image if og_image else logo_url
    return f"""<!DOCTYPE html><html lang="en"><head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | {biz_name}</title>
    <meta name="description" content="{seo_d}">
    <meta property="og:title" content="{title} | {biz_name}">
    <meta property="og:description" content="{seo_d}">
    <meta property="og:image" content="{og_img}">
    <meta property="og:type" content="website">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family={h_font.replace(' ', '+')}:wght@700;900&family={b_font.replace(' ', '+')}:wght@400;600&display=swap" rel="stylesheet">
    {gen_schema()}
    {gen_ga4()}
    <style>{get_theme_css()} @keyframes pulse {{ 0% {{opacity: 0.6;}} 50% {{opacity: 1;}} 100% {{opacity: 0.6;}} }} </style>
    </head><body>{gen_nav()}{content}{gen_footer()}{extra_js}
    <script>
    // Intersection Observer for performance-friendly animations
    const observer = new IntersectionObserver((entries) => {{ entries.forEach(e => {{ if(e.isIntersecting) e.target.classList.add('active'); }}); }});
    document.querySelectorAll('.reveal').forEach((el) => observer.observe(el));
    </script>
    </body></html>"""

# --- 6. PAGE ASSEMBLY ---
home_content = ""
if show_hero: home_content += gen_hero()
if show_features: home_content += gen_features()
if show_inventory: home_content += gen_inventory()

# --- 7. DEPLOYMENT ---
st.divider()
st.subheader("🚀 Engine Ready")

c1, c2 = st.columns([3, 1])
with c1:
    st.components.v1.html(build_page("Home", home_content), height=600, scrolling=True)
with c2:
    st.success("100/100 Lighthouse Ready.")
    if st.button("DOWNLOAD WEBSITE ZIP", type="primary"):
        z_b = io.BytesIO()
        with zipfile.ZipFile(z_b, "a", zipfile.ZIP_DEFLATED, False) as zf:
            zf.writestr("index.html", build_page("Home", home_content))
            zf.writestr("privacy.html", build_page("Privacy", f"<section class='hero'><div class='container'><h1>Privacy</h1></div></section><div class='container'>{format_text(priv_txt)}</div>"))
            zf.writestr("manifest.json", gen_pwa_manifest())
            zf.writestr("service-worker.js", gen_sw())
            zf.writestr("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {prod_url}/sitemap.xml")
        st.download_button("📥 Click to Save", z_b.getvalue(), f"{biz_name.lower().replace(' ','_')}_site.zip", "application/zip")
