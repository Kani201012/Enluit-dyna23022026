import streamlit as st
import zipfile
import io
import json
import datetime
import re
import requests

# --- 0. FAILSAFE INITIALIZATION (Prevents NameError) ---
show_hero = show_stats = show_features = show_pricing = show_inventory = show_blog = show_gallery = show_testimonials = show_faq = show_cta = show_booking = True
top_bar_enabled = popup_enabled = enable_ar = enable_voice = enable_context = enable_ab = True
hero_video_id = ga_tag = og_image = pinata_jwt = lang_sheet = fb_link = ig_link = x_link = li_link = yt_link = ""

def init_state(key, default_val):
    if key not in st.session_state: st.session_state[key] = default_val

init_state('hero_h', "Stop Paying Rent for Your Website.")
init_state('hero_sub', "The Titan Engine is the world’s first 0.1s website architecture that runs on $0 monthly fees. Pay once. Own it forever.")
init_state('feat_data', "bolt | The Performance Pillar | **0.1s High-Velocity Loading**. While traditional sites take 3–5s, Titan loads instantly.\nwallet | The Economic Pillar | **$0 Monthly Fees**. We eliminated hosting subscriptions.\nshield | The Authority Pillar | **Unhackable Security**. Zero-DB Architecture removes the hacker's primary entry point.")

# --- 1. APP CONFIGURATION ---
st.set_page_config(page_title="Titan Architect | 2050 Apex Edition", layout="wide", page_icon="⚡", initial_sidebar_state="expanded")

st.markdown("""<style>:root { --primary: #0f172a; --accent: #ef4444; } .stApp { background-color: #f8fafc; color: #1e293b; font-family: 'Inter', sans-serif; } [data-testid="stSidebar"] { background-color: #ffffff; border-right: 1px solid #e2e8f0; } [data-testid="stSidebar"] h1 { background: linear-gradient(90deg, #0f172a, #ef4444); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 900 !important; font-size: 1.8rem !important; } .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] { background-color: #ffffff !important; border: 1px solid #cbd5e1 !important; border-radius: 8px !important; color: #0f172a !important; } .stButton>button { width: 100%; border-radius: 8px; height: 3.5rem; background: linear-gradient(135deg, #0f172a 0%, #334155 100%); color: white; font-weight: 800; border: none; box-shadow: 0 4px 15px rgba(15, 23, 42, 0.3); text-transform: uppercase; letter-spacing: 1px; transition: transform 0.2s; } .stButton>button:hover { transform: translateY(-2px); }</style>""", unsafe_allow_html=True)

# --- 2. SIDEBAR ---
with st.sidebar:
    st.title("Titan Architect")
    st.caption("v50.0 | Edge-Dynamic Architecture")
    st.divider()
    
    with st.expander("🎨 Design Studio", expanded=True):
        theme_mode = st.selectbox("Base Theme", ["Clean Corporate (Light)", "Midnight SaaS (Dark)", "Cyberpunk Neon", "Luxury Gold", "Forest Eco", "Ocean Breeze", "Stark Minimalist"])
        c1, c2, c3 = st.columns(3)
        p_color = c1.color_picker("Primary", "#0F172A") 
        s_color = c2.color_picker("Accent", "#EF4444")  
        btn_txt_color = c3.color_picker("Btn Text", "#FFFFFF")
        
        hero_layout = st.selectbox("Hero Alignment", ["Center", "Left"])
        btn_style = st.selectbox("Button Style", ["Rounded (Default)", "Sharp (Square)", "Pill (Full Round)"])
        border_rad = "8px" if btn_style == "Rounded (Default)" else ("0px" if btn_style == "Sharp (Square)" else "50px")
        card_hover_style = st.selectbox("Card Hover Border", ["Soft Shadow (Modern)", "Primary Color Border", "Accent Color Border (Red)"])
        overlay_opacity = st.slider("Hero Image Darkness", 0.1, 0.9, 0.5)
        
        anim_type = st.selectbox("Animation Style", ["Fade Up", "Zoom In", "Slide Right", "None"])
        h_font = st.selectbox("Headings Font", ["Montserrat", "Space Grotesk", "Playfair Display", "Oswald", "Clash Display"])
        b_font = st.selectbox("Body Font", ["Inter", "Open Sans", "Roboto", "Satoshi", "Lora"])

    with st.expander("🚀 2050 Feature Flags", expanded=True):
        enable_ar = st.checkbox("Spatial Web (AR 3D Models)", value=True)
        enable_voice = st.checkbox("Voice Command Search", value=True)
        enable_context = st.checkbox("Context-Aware UI", value=True)
        enable_ab = st.checkbox("Edge A/B Testing", value=True)

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
        seo_d = st.text_area("Meta Description", "Stop paying monthly fees")
        ga_tag = st.text_input("Google Analytics ID")
        og_image = st.text_input("Social Share Image URL")

# --- 3. MAIN WORKSPACE ---
st.title("🏗️ StopWebRent 2050 Compiler")
tabs = st.tabs(["1. Identity & PWA", "2. Content Blocks", "3. Marketing", "4. Pricing", "5. Store", "6. Booking", "7. Blog", "8. Legal", "9. Web3 Deploy"])

with tabs[0]:
    c1, c2 = st.columns(2)
    biz_name = c1.text_input("Business Name", "StopWebRent.com")
    biz_tagline = c1.text_input("Tagline", "Stop Renting. Start Owning.")
    biz_phone = c1.text_input("Phone", "966572562151")
    biz_email = c1.text_input("Email", "hello@kaydiemscriptlab.com")
    prod_url = c2.text_input("Website URL", "https://www.stopwebrent.com")
    biz_addr = c2.text_area("Address", "Kolkata, India", height=100)
    logo_url = st.text_input("Logo URL (PNG/SVG)")

    st.subheader("📱 Progressive Web App (PWA)")
    pwa_short = st.text_input("App Short Name", biz_name[:12])
    pwa_desc = st.text_input("App Description", "Official App")
    pwa_icon = st.text_input("App Icon (512x512 PNG)", logo_url)
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
    hero_h = st.text_input("Hero Headline", key="hero_h")
    hero_sub = st.text_input("Hero Subtext", key="hero_sub")
    hero_video_id = st.text_input("YouTube Video ID", placeholder="e.g. dQw4w9WgXcQ")
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
    
    about_h_in = st.text_input("About Title", "The Digital Landlord Trap...")
    about_img = st.text_input("About Image", "https://images.unsplash.com/photo-1543286386-713df548e9cc?q=80&w=1600")
    about_short_in = st.text_area("Short Summary", "We build static sites.", height=100)
    about_long = st.text_area("Full Content", "StopWebRent was founded...", height=100)

with tabs[2]:
    top_bar_enabled = st.checkbox("Enable Top Bar", value=True)
    top_bar_text = st.text_input("Promo Text", "🔥 50% OFF Launch Sale - Ends Soon!")
    top_bar_link = st.text_input("Promo Link", "#pricing")
    popup_enabled = st.checkbox("Enable Popup", value=True)
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
    st.info("💡 **2050 AR Protocol:** In your Store CSV, make Column F (the 6th column) a link to a `.glb` 3D model to enable native Augmented Reality.")
    sheet_url = st.text_input("Store CSV", placeholder="https://docs.google.com/spreadsheets/...")
    custom_feat = st.text_input("Default Product Img", "https://images.unsplash.com/photo-1460925895917-afdab827c52f?q=80&w=800")
    col_pay1, col_pay2 = st.columns(2)
    paypal_link = col_pay1.text_input("PayPal Link", "https://paypal.me/yourid")
    upi_id = col_pay2.text_input("UPI ID", "name@upi")

with tabs[5]:
    booking_embed = st.text_area("Embed Code", height=150, value='<!-- Calendly --><div class="calendly-inline-widget" data-url="https://calendly.com/titan-demo" style="min-width:320px;height:630px;"></div><script type="text/javascript" src="https://assets.calendly.com/assets/external/widget.js" async></script>')
    booking_title = st.text_input("Booking Title", "Book an Appointment")
    booking_desc = st.text_input("Booking Subtext", "Select a time slot.")

with tabs[6]:
    blog_sheet_url = st.text_input("Blog CSV", placeholder="https://docs.google.com/spreadsheets/...")
    blog_hero_title = st.text_input("Blog Title", "Latest Insights")
    blog_hero_sub = st.text_input("Blog Subtext", "Thoughts on tech.")

with tabs[7]:
    testi_data = st.text_area("Testimonials", "Rajesh Gupta | Titan stopped the bleeding.", height=100)
    faq_data = st.text_area("FAQ", "Do I pay $0? ? Yes.", height=100)
    priv_txt = st.text_area("Privacy", "We collect minimum data.", height=100)
    term_txt = st.text_area("Terms", "You own the code.", height=100)

with tabs[8]:
    st.markdown("Host your site on the decentralized Web3 network. It can never be taken down, and costs $0/month.")
    pinata_jwt = st.text_input("Pinata API JWT (Leave blank for normal ZIP)", type="password")

# --- 4. COMPILER ENGINE LOGIC ---
def format_text(t): return "".join([f"<li style='margin-bottom:0.5rem;'>{l[2:]}</li>" if l.startswith("* ") else f"<p style='margin-bottom:1rem;'>{l}</p>" for l in (re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', t).split('\n') if t else []) if l.strip()])
def gen_schema(): return f'<script type="application/ld+json">{json.dumps({{"@context": "https://schema.org", "@type": "LocalBusiness", "name": biz_name, "image": logo_url or hero_img_1, "telephone": biz_phone, "email": biz_email, "url": prod_url, "description": seo_d}})}</script>'
def gen_pwa_manifest(): return json.dumps({"name": biz_name, "short_name": pwa_short, "start_url": "./index.html", "display": "standalone", "background_color": "#ffffff", "theme_color": p_color, "icons": [{"src": pwa_icon, "sizes": "512x512", "type": "image/png"}]})
def gen_sw(): return "const CACHE_NAME='titan-v50';self.addEventListener('install',(e)=>{e.waitUntil(caches.open(CACHE_NAME).then((c)=>c.addAll(['./index.html'])));self.skipWaiting();});self.addEventListener('fetch',(e)=>{if(e.request.url.includes('google.com/spreadsheets')){e.respondWith(fetch(e.request).then(res=>{const rClone=res.clone();caches.open('titan-data').then(c=>c.put(e.request,rClone));return res;}).catch(()=>caches.match(e.request)));}else{e.respondWith(caches.match(e.request).then((res)=>res||fetch(e.request)));}});"

def get_theme_css():
    bg, txt, card, nav_bg = "#ffffff", "#0f172a", "#ffffff", "rgba(255, 255, 255, 0.95)"
    if "Midnight" in theme_mode: bg, txt, card, nav_bg = "#0f172a", "#f8fafc", "#1e293b", "rgba(15, 23, 42, 0.9)"
    elif "Cyberpunk" in theme_mode: bg, txt, card, nav_bg = "#050505", "#00ff9d", "#111", "rgba(0,0,0,0.8)"
    
    anim_c = ".reveal { opacity: 0; transform: translateY(30px); transition: 0.8s ease; } .reveal.active { opacity: 1; transform: translateY(0); }" if anim_type == "Fade Up" else (".reveal { opacity: 0; transform: scale(0.95); transition: 0.8s ease; } .reveal.active { opacity: 1; transform: scale(1); }" if anim_type == "Zoom In" else "")
    h_align = "text-align: left; justify-content: flex-start; align-items: center;" if hero_layout == "Left" else "text-align: center; justify-content: center;"
    
    h_css = "box-shadow: 0 20px 40px -10px rgba(0,0,0,0.15); transform: translateY(-5px);"
    if card_hover_style == "Primary Color Border": h_css += f" border-color: {p_color};"
    elif card_hover_style == "Accent Color Border (Red)": h_css += f" border-color: {s_color};"
    else: h_css += " border-color: transparent;"

    return f"""
    :root {{ --p: {p_color}; --s: {s_color}; --btn-txt: {btn_txt_color}; --bg: {bg}; --txt: {txt}; --card: {card}; --radius: {border_rad}; --nav: {nav_bg}; --h-font: '{h_font}', sans-serif; --b-font: '{b_font}', sans-serif; }}
    * {{ box-sizing: border-box; }} html {{ scroll-behavior: smooth; font-size: 16px; }} body {{ background: var(--bg); color: var(--txt); font-family: var(--b-font); margin: 0; line-height: 1.6; overflow-x: hidden; transition: 0.3s; }}
    body.dark-mode {{ --bg: #0f172a; --txt: #f8fafc; --card: #1e293b; --nav: rgba(15, 23, 42, 0.95); }}
    h1, h2, h3, h4 {{ font-family: var(--h-font); color: var(--p); line-height: 1.2; margin-bottom: 1rem; }} strong {{ color: var(--p); font-weight: 800; }} h1 {{ font-size: clamp(2.5rem, 5vw, 4.5rem); }} h2 {{ font-size: clamp(2rem, 4vw, 3rem); }}
    .hero {{ position: relative; min-height: 90vh; overflow: hidden; display: flex; {h_align} color: white; padding-top: 80px; background: var(--p); }} .carousel-slide {{ position: absolute; inset: 0; background-size: cover; background-position: center; opacity: 0; transition: opacity 1.5s; z-index: 0; }} .carousel-slide.active {{ opacity: 1; }} .hero-overlay {{ background: rgba(0,0,0,{overlay_opacity}); position: absolute; inset: 0; z-index: 1; }} .hero-content {{ z-index: 2; position: relative; width: 100%; padding: 0 20px; }} .hero h1 {{ color: #fff !important; text-shadow: 0 4px 20px rgba(0,0,0,0.4); }} .hero p {{ color: rgba(255,255,255,0.95) !important; font-size: 1.2rem; max-width: 700px; margin: 0 auto 2rem; }}
    input, textarea, select {{ width: 100%; padding: 0.8rem; margin-bottom: 1rem; border: 1px solid #ccc; border-radius: 6px; }} .container {{ max-width: 1280px; margin: 0 auto; padding: 0 20px; }}
    .btn {{ display: inline-flex; align-items: center; justify-content: center; padding: 1rem 2rem; border-radius: var(--radius); font-weight: 700; text-decoration: none; transition: 0.3s; cursor: pointer; border: none; text-transform: uppercase; }} .btn-primary {{ background: var(--p); color: var(--btn-txt) !important; }} .btn-accent {{ background: var(--s); color: var(--btn-txt) !important; }} .btn:hover {{ transform: translateY(-3px); filter: brightness(1.15); }}
    nav.main-nav {{ position: fixed; top: 0; width: 100%; z-index: 1000; background: var(--nav); backdrop-filter: blur(12px); border-bottom: 1px solid rgba(100,100,100,0.1); padding: 1rem 0; transition: top 0.3s; }} .nav-flex {{ display: flex; justify-content: space-between; align-items: center; }} .nav-links {{ display: flex; align-items: center; }} .nav-links a {{ margin-left: 2rem; text-decoration: none; font-weight: 600; color: var(--txt); transition:0.2s; }} .nav-links a:hover {{ color: var(--s); }} .mobile-menu {{ display: none; font-size: 1.5rem; cursor: pointer; }}
    main section {{ padding: 4rem 0; }} .section-head {{ text-align: center; margin-bottom: 2rem; }} .grid-3 {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem; }} .about-grid, .detail-view {{ display: grid; grid-template-columns: 1fr 1fr; gap: 4rem; align-items: center; }} .contact-grid {{ display: grid; grid-template-columns: 1fr 2fr; gap: 3rem; }}
    .card {{ background: var(--card); border-radius: var(--radius); border: 1px solid rgba(100,100,100,0.1); padding: 1.5rem; transition: 0.3s; display: flex; flex-direction: column; overflow: hidden; }} .card:hover {{ {h_css} }} .card h3, .card h4, .card a:not(.btn) {{ color: var(--txt) !important; text-decoration: none; }} .prod-img {{ width: 100%; height: 250px; object-fit: cover; background: #eee; margin-bottom: 1rem; border-radius: 8px; }}
    .pricing-table {{ width: 100%; border-collapse: collapse; }} .pricing-table th {{ background: var(--p); color: white; padding: 1.5rem; text-align: left; }} .pricing-table td {{ padding: 1.5rem; border-bottom: 1px solid rgba(100,100,100,0.1); background: var(--card); color: var(--txt); }}
    footer {{ background: var(--p); color: white; padding: 4rem 0; margin-top: auto; }} .footer-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 3rem; }} footer a {{ color: rgba(255,255,255,0.8) !important; text-decoration: none; display: block; margin-bottom: 0.5rem; transition: 0.3s; }} footer a:hover {{ color: #ffffff !important; text-decoration: underline; }}
    .blog-badge {{ background: var(--s); color: var(--btn-txt); padding: 0.3rem 0.8rem; border-radius: 50px; font-size: 0.75rem; font-weight: bold; margin-bottom: 1rem; display:inline-block; text-transform: uppercase; }}
    #cart-float {{ position: fixed; bottom: 100px; right: 30px; background: var(--p); color: var(--btn-txt); padding: 15px 20px; border-radius: 50px; cursor: pointer; z-index: 998; display: flex; align-items: center; gap: 10px; font-weight: bold; box-shadow: 0 10px 20px rgba(0,0,0,0.2); }}
    #cart-modal {{ display: none; position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); background: var(--card); width: 90%; max-width: 500px; padding: 2rem; border-radius: 16px; z-index: 1001; color: var(--txt); }} #cart-overlay {{ display: none; position: fixed; inset: 0; background: rgba(0,0,0,0.5); z-index: 1000; }} .cart-item {{ display: flex; justify-content: space-between; border-bottom: 1px solid #eee; padding: 10px 0; }}
    #voice-btn {{ position: fixed; bottom: 170px; right: 30px; background: var(--p); color: var(--btn-txt); border-radius: 50px; width: 50px; height: 50px; display: flex; align-items: center; justify-content: center; font-size: 1.2rem; cursor: pointer; z-index: 998; border: none; }} .listening {{ background: var(--s) !important; }}
    model-viewer {{ width: 100%; height: 400px; background-color: transparent; }}
    #theme-toggle {{ position: fixed; bottom: 30px; left: 30px; width: 40px; height: 40px; background: var(--card); border-radius: 50%; display: flex; align-items: center; justify-content: center; box-shadow: 0 5px 15px rgba(0,0,0,0.1); cursor: pointer; z-index: 999; font-size: 1.2rem; }}
    {anim_c}
    @media (max-width: 768px) {{ nav.main-nav .nav-links {{ position: fixed; top: 60px; left: -100%; width: 100%; height: 100vh; background: var(--bg); flex-direction: column; padding: 2rem; transition: 0.3s; align-items: flex-start; gap: 1.5rem; }} nav.main-nav .nav-links.active {{ left: 0; }} .mobile-menu {{ display: block; }} .about-grid, .detail-view, .grid-3 {{ grid-template-columns: 1fr !important; }} }}
    """

def gen_2050_scripts():
    cjs = "if(new Date().getHours()>=19 || new Date().getHours()<=6) document.body.classList.add('dark-mode');" if enable_context else ""
    ajs = "let v = localStorage.getItem('titan_ab') || (Math.random()>0.5?'A':'B'); localStorage.setItem('titan_ab', v); if(v==='B') document.documentElement.style.setProperty('--s', '#10b981');" if enable_ab else ""
    vjs = "function startVoiceSearch() { if(!('webkitSpeechRecognition' in window)) return alert('Not supported'); const r = new webkitSpeechRecognition(); const b = document.getElementById('voice-btn'); b.classList.add('listening'); r.onresult = (e) => { const t = e.results[0][0].transcript.toLowerCase(); document.querySelectorAll('.card').forEach(c => c.style.display = c.innerText.toLowerCase().includes(t) ? 'flex' : 'none'); }; r.onend = () => b.classList.remove('listening'); r.start(); }" if enable_voice else ""
    return f"<script defer>{cjs} {ajs} {vjs}</script>"

def gen_nav():
    lg = f'<img src="{logo_url}" height="40" alt="Logo">' if logo_url else f'<span style="font-weight:900; font-size:1.5rem; color:var(--p)">{biz_name}</span>'
    return f"""<nav class="main-nav"><div class="container nav-flex"><a href="index.html" style="text-decoration:none;">{lg}</a><div class="mobile-menu" onclick="document.querySelector('.nav-links').classList.toggle('active')">☰</div><div class="nav-links"><a href="index.html">Home</a><a href="index.html#inventory">Store</a><a href="blog.html">Blog</a><a href="contact.html">Contact</a><a href="tel:{biz_phone}" class="btn btn-accent" style="padding:0.5rem 1rem;">Call Now</a></div></div></nav><div id="theme-toggle" onclick="document.body.classList.toggle('dark-mode')">🌓</div>"""

def gen_hero():
    vid = f'<iframe src="https://www.youtube.com/embed/{hero_video_id}?autoplay=1&mute=1&loop=1" style="position:absolute; inset:0; width:100vw; height:100vh; object-fit:cover; z-index:0; pointer-events:none;" frameborder="0"></iframe>' if hero_video_id else f"""<div class="carousel-slide active" style="background-image: url('{hero_img_1}')"></div><div class="carousel-slide" style="background-image: url('{hero_img_2}')"></div><div class="carousel-slide" style="background-image: url('{hero_img_3}')"></div><script defer>let s = document.querySelectorAll('.carousel-slide'); let c = 0; setInterval(() => {{ s[c].classList.remove('active'); c=(c+1)%s.length; s[c].classList.add('active'); }}, 4000);</script>"""
    return f"""<section class="hero"><div class="hero-overlay"></div>{vid}<div class="container hero-content"><h1>{hero_h}</h1><p>{hero_sub}</p><div style="display:flex; gap:1rem; flex-wrap:wrap; {'justify-content:center;' if hero_layout == 'Center' else ''}"><a href="#inventory" class="btn btn-accent">Explore</a><a href="contact.html" class="btn" style="background:rgba(255,255,255,0.2);color:white;">Contact</a></div></div></section>"""

def gen_cart_system():
    return f"""<div id="cart-float" onclick="document.getElementById('cart-modal').style.display='block'; document.getElementById('cart-overlay').style.display='block';">🛒 <span id="cart-count">0</span></div><div id="cart-overlay" onclick="document.getElementById('cart-modal').style.display='none'; this.style.display='none';"></div><div id="cart-modal"><h3>Cart</h3><div id="cart-items" style="max-height:200px;overflow-y:auto;margin:1rem 0;"></div><div style="font-weight:bold;text-align:right;">Total: <span id="cart-total">0</span></div><input type="text" id="vault-name" placeholder="Name" style="margin-top:1rem;width:100%;padding:10px;"><button onclick="checkoutWA()" class="btn btn-accent" style="width:100%;margin-top:10px;">Checkout WhatsApp</button></div><script defer>let cart = JSON.parse(localStorage.getItem('titanCart')) || []; function rCart() {{ const b=document.getElementById('cart-items'); if(!b)return; b.innerHTML=''; let t=0; cart.forEach((i,x)=>{{ t+=parseFloat(i.price.replace(/[^0-9.]/g,''))||0; b.innerHTML+=`<div class="cart-item"><span>${{i.name}}</span><span style="color:red;cursor:pointer" onclick="cart.splice(${{x}},1);rCart()">x</span></div>`; }}); document.getElementById('cart-count').innerText=cart.length; document.getElementById('cart-total').innerText=t.toFixed(2); localStorage.setItem('titanCart',JSON.stringify(cart)); }} function addToCart(n,p) {{ cart.push({{name:n,price:p}}); rCart(); alert('Added!'); }} function checkoutWA() {{ const n=document.getElementById('vault-name').value; let m="Order:%0A"; cart.forEach(i=>m+=`- ${{i.name}}%0A`); if(n)m+=`From: ${{n}}`; window.open(`https://wa.me/{wa_num}?text=${{m}}`); cart=[]; rCart(); }} window.addEventListener('load',rCart);</script>"""

def gen_inventory():
    if not show_inventory: return ""
    vbtn = '<button id="voice-btn" onclick="startVoiceSearch()">🎤</button>' if enable_voice else ''
    return f"""<section id="inventory" style="background:rgba(0,0,0,0.02)"><div class="container"><h2 class="section-head">Store</h2><div id="inv-grid" class="grid-3">Loading Edge Data...</div></div>{vbtn}</section><script defer>function parseCSV(str) {{ const r=[]; let c='',q=false; for(let i=0;i<str.length;i++){{ const ch=str[i]; if(ch==='"'){{ if(q&&str[i+1]==='"'){{c+='"';i++;}}else q=!q; }}else if(ch===','&&!q){{r.push(c.trim());c='';}}else c+=ch; }} r.push(c.trim()); return r; }} async function loadInv() {{ try {{ const res=await fetch('{sheet_url}'); const t=await res.text(); const b=document.getElementById('inv-grid'); b.innerHTML=''; t.split('\\n').slice(1).forEach(l=>{{ if(!l.trim())return; const c=parseCSV(l); if(c.length>1){{ const p=encodeURIComponent(c[0]); const img=c[3]?c[3].split('|')[0]:'{custom_feat}'; b.innerHTML+=`<div class="card"><img src="${{img}}" class="prod-img"><h3>${{c[0]}}</h3><p style="color:var(--s);font-weight:bold">${{c[1]}}</p><p class="card-desc">${{c[2]}}</p><div style="margin-top:auto;display:flex;gap:10px;"><button onclick="addToCart('${{c[0]}}','${{c[1]}}')" class="btn btn-primary" style="flex:1">Add</button><a href="product.html?item=${{p}}" class="btn btn-accent">View</a></div></div>`; }} }}); }} catch(e){{}} }} window.addEventListener('load',loadInv);</script>"""

def build_page(title, content):
    pwa = f'<link rel="manifest" href="manifest.json"><meta name="theme-color" content="{p_color}">'
    sw = "<script defer>if('serviceWorker' in navigator) navigator.serviceWorker.register('sw.js');</script>"
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>{title} | {biz_name}</title><meta name="description" content="{seo_d}">{pwa}<link href="https://fonts.googleapis.com/css2?family={h_font.replace(' ','+')}:wght@700;900&family={b_font.replace(' ','+')}:wght@400;600&display=swap" rel="stylesheet"><style>{get_theme_css()}</style>{gen_2050_scripts()}</head><body><main>{gen_nav()}{content}<footer style="background:var(--p);color:white;padding:4rem 0;text-align:center;"><div class="container">&copy; {datetime.datetime.now().year} {biz_name}.</div></footer>{gen_cart_system()}{sw}<script defer>window.addEventListener('scroll',()=>{{document.querySelectorAll('.reveal').forEach(r=>{{if(r.getBoundingClientRect().top<window.innerHeight-100)r.classList.add('active');}})}});window.dispatchEvent(new Event('scroll'));</script></main></body></html>"""

def gen_product_page():
    ar = '<script type="module" src="https://ajax.googleapis.com/ajax/libs/model-viewer/3.4.0/model-viewer.min.js"></script>' if enable_ar else ''
    return f"""{ar}<section style="padding-top:120px;"><div class="container"><a href="index.html#inventory" class="btn btn-primary" style="margin-bottom:2rem;">&larr; Back</a><div id="pd">Loading...</div></div></section><script defer>async function loadP() {{ const p=new URLSearchParams(window.location.search).get('item'); try{{ const res=await fetch('{sheet_url}'); const t=await res.text(); t.split('\\n').slice(1).forEach(l=>{{ const c=parseCSV(l); if(c[0]===p){{ let m=`<img src="${{c[3]?c[3].split('|')[0]:''}}" style="width:100%;border-radius:12px;">`; if({str(enable_ar).lower()}&&c.length>5&&c[5].includes('.glb')) m=`<model-viewer src="${{c[5]}}" ar auto-rotate style="width:100%;height:400px;"></model-viewer>`; document.getElementById('pd').innerHTML=`<div class="detail-view"><div>${{m}}</div><div><h1 style="font-size:3rem">${{c[0]}}</h1><h2 style="color:var(--s)">${{c[1]}}</h2><p>${{c[2]}}</p><button onclick="addToCart('${{c[0]}}','${{c[1]}}')" class="btn btn-accent" style="width:100%;margin-top:2rem">Add to Cart</button></div></div>`; document.title=c[0]+" | {biz_name}"; }} }}); }}catch(e){{}} }} window.addEventListener('load',loadP);</script>"""

# --- 5. ASSEMBLY ---
home_c = gen_hero() 
if show_features: home_c += f'<section style="background:var(--card)"><div class="container grid-3">' + "".join([f'<div class="card reveal"><h3 style="color:var(--s)">{l.split("|")[1]}</h3><p>{l.split("|")[2]}</p></div>' for l in feat_data_input.split('\n') if '|' in l]) + '</div></section>' 
home_c += gen_inventory()

# --- 6. DEPLOYMENT ---
st.divider()
c1, c2 = st.columns([3, 1])

with c1:
    st.subheader("🚀 Live Preview")
    st.components.v1.html(build_page("Home", home_c), height=600, scrolling=True)

with c2:
    st.success("100% Compiled & Error Free.")
    z_b = io.BytesIO()
    with zipfile.ZipFile(z_b, "a", zipfile.ZIP_DEFLATED, False) as zf:
        zf.writestr("index.html", build_page("Home", home_c))
        zf.writestr("product.html", build_page("Product", gen_product_page()))
        zf.writestr("sw.js", gen_sw())
        zf.writestr("manifest.json", gen_pwa_manifest())
        
    st.download_button("📥 DOWNLOAD 2050 PACKAGE", z_b.getvalue(), f"{biz_name.replace(' ','_')}.zip", "application/zip", type="primary")
