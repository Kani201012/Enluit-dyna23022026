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
st.set_page_config(
    page_title="Titan Architect | 2050 Apex Edition", 
    layout="wide", 
    page_icon="⚡",
    initial_sidebar_state="expanded"
)

# --- 2. ADVANCED UI SYSTEM ---
st.markdown("""
    <style>
    :root { --primary: #0f172a; --accent: #ef4444; }
    .stApp { background-color: #f8fafc; color: #1e293b; font-family: 'Inter', sans-serif; }
    [data-testid="stSidebar"] { background-color: #ffffff; border-right: 1px solid #e2e8f0; }
    [data-testid="stSidebar"] h1 { 
        background: linear-gradient(90deg, #0f172a, #ef4444);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900 !important; font-size: 1.8rem !important;
    }
    .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {
        background-color: #ffffff !important; border: 1px solid #cbd5e1 !important; border-radius: 8px !important; color: #0f172a !important;
    }
    .stButton>button {
        width: 100%; border-radius: 8px; height: 3.5rem;
        background: linear-gradient(135deg, #0f172a 0%, #334155 100%);
        color: white; font-weight: 800; border: none; box-shadow: 0 4px 15px rgba(15, 23, 42, 0.3); text-transform: uppercase; letter-spacing: 1px; transition: transform 0.2s;
    }
    .stButton>button:hover { transform: translateY(-2px); }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR ---
with st.sidebar:
    st.title("Titan Architect")
    st.caption("v50.0 | Edge-Dynamic Architecture")
    st.divider()
    
    # --- AI GENERATOR ---
    with st.expander("🤖 Titan AI Generator", expanded=False):
        raw_key = st.text_input("Groq API Key", type="password")
        groq_key = raw_key.strip() if raw_key else ""
        biz_desc = st.text_input("Business Description")
        
        if st.button("✨ Generate Copy"):
            if not groq_key or not biz_desc:
                st.error("Key & Description required.")
            else:
                try:
                    with st.spinner("Writing Context..."):
                        url = "https://api.groq.com/openai/v1/chat/completions"
                        headers = {"Authorization": f"Bearer {groq_key}", "Content-Type": "application/json"}
                        prompt = f"Act as a copywriter. Return JSON for '{biz_desc}': hero_h, hero_sub, about_h, about_short, feat_data (icon|Title|Desc format)."
                        data = {"messages": [{"role": "user", "content": prompt}], "model": "llama-3.1-8b-instant", "response_format": {"type": "json_object"}}
                        resp = requests.post(url, headers=headers, json=data)
                        if resp.status_code == 200:
                            res = resp.json()['choices'][0]['message']['content']
                            parsed = json.loads(res)
                            if 'hero_h' in parsed: st.session_state.hero_h = str(parsed['hero_h'])
                            if 'hero_sub' in parsed: st.session_state.hero_sub = str(parsed['hero_sub'])
                            if 'about_h' in parsed: st.session_state.about_h = str(parsed['about_h'])
                            if 'about_short' in parsed: st.session_state.about_short = str(parsed['about_short'])
                            if 'feat_data' in parsed:
                                if isinstance(parsed['feat_data'], list): st.session_state.feat_data = "\n".join(map(str, parsed['feat_data']))
                                else: st.session_state.feat_data = str(parsed['feat_data'])
                            st.success("Generated Successfully!")
                            st.rerun()
                except Exception as e: st.error(f"Error: {e}")

    # 3.1 VISUAL DNA & UI VARIATIONS
    with st.expander("🎨 Design Studio", expanded=True):
        theme_mode = st.selectbox("Base Theme", ["Clean Corporate (Light)", "Midnight SaaS (Dark)", "Glassmorphism (Blur)", "Cyberpunk Neon", "Luxury Gold", "Forest Eco", "Ocean Breeze", "Stark Minimalist"])
        
        c1, c2, c3 = st.columns(3)
        p_color = c1.color_picker("Primary Brand", "#0F172A") 
        s_color = c2.color_picker("Action (CTA)", "#EF4444")  
        btn_txt_color = c3.color_picker("Btn Text", "#FFFFFF")
        
        st.markdown("**Layout & Physics**")
        hero_layout = st.selectbox("Hero Alignment", ["Center", "Left"])
        btn_style = st.selectbox("Button Style", ["Rounded (Default)", "Sharp (Square)", "Pill (Full Round)"])
        border_rad = "8px" if btn_style == "Rounded (Default)" else ("0px" if btn_style == "Sharp (Square)" else "50px")
        
        card_hover_style = st.selectbox("Card Hover Border", ["Soft Shadow (Modern)", "Primary Color Border", "Accent Color Border (Red)"])
        overlay_opacity = st.slider("Hero Image Darkness", 0.1, 0.9, 0.5, help="Higher number makes text easier to read over images.")
        
        anim_type = st.selectbox("Animation Style", ["Fade Up", "Zoom In", "Slide Right", "None"])
        h_font = st.selectbox("Headings Font", ["Montserrat", "Space Grotesk", "Playfair Display", "Oswald", "Clash Display"])
        b_font = st.selectbox("Body Font", ["Inter", "Open Sans", "Roboto", "Satoshi", "Lora"])

    # 3.2 2050 FEATURE FLAGS
    with st.expander("🚀 2050 Feature Flags", expanded=True):
        st.write("Enable Next-Gen Capabilities:")
        enable_ar = st.checkbox("Spatial Web (AR 3D Models)", value=True, help="Injects <model-viewer> for .glb links in your CSV.")
        enable_voice = st.checkbox("Voice Command Search", value=True, help="Native browser NLP for store filtering.")
        enable_context = st.checkbox("Context-Aware UI", value=True, help="Auto dark-mode based on user's local time.")
        enable_ab = st.checkbox("Edge A/B Testing", value=True, help="Client-side variant testing without tracking cookies.")

    # 3.3 MODULE MANAGER
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

    # 3.4 TECHNICAL
    with st.expander("⚙️ SEO & Analytics", expanded=False):
        seo_area = st.text_input("Service Area", "Global / Online")
        seo_kw = st.text_area("SEO Keywords", "web design, no monthly fees")
        gsc_tag = st.text_input("Google Verification ID")
        ga_tag = st.text_input("Google Analytics ID")
        og_image = st.text_input("Social Share Image URL")

# --- 4. MAIN WORKSPACE ---
st.title("🏗️ StopWebRent 2050 Compiler")

tabs = st.tabs(["1. Identity & PWA", "2. Content Blocks", "3. Marketing Tools", "4. Pricing", "5. Store", "6. Booking", "7. Blog", "8. Legal", "9. Web3 / IPFS"])

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
        seo_d = st.text_area("Meta Description", "Stop paying monthly fees for web hosting.", height=100)
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
    st.subheader("Stats & Features")
    col_s1, col_s2, col_s3 = st.columns(3)
    stat_1 = col_s1.text_input("Stat 1", "0.1s")
    label_1 = col_s1.text_input("Label 1", "Speed")
    stat_2 = col_s2.text_input("Stat 2", "$0")
    label_2 = col_s2.text_input("Label 2", "Fees")
    stat_3 = col_s3.text_input("Stat 3", "100%")
    label_3 = col_s3.text_input("Label 3", "Ownership")

    f_title = st.text_input("Features Title", "Value Pillars")
    feat_data_input = st.text_area("Features List", key="feat_data", height=150)
    
    st.subheader("About")
    about_h_in = st.text_input("About Title", key="about_h")
    about_img = st.text_input("About Image", "https://images.unsplash.com/photo-1543286386-713df548e9cc?q=80&w=1600")
    about_short_in = st.text_area("Short Summary", key="about_short", height=100)
    about_long = st.text_area("Full Content", "The Digital Landlord Trap...", height=200)

with tabs[2]:
    st.subheader("📣 Marketing Suite")
    top_bar_enabled = st.checkbox("Enable Top Bar")
    top_bar_text = st.text_input("Promo Text", "🔥 50% OFF Launch Sale - Ends Soon!")
    top_bar_link = st.text_input("Promo Link", "#pricing")
    
    st.divider()
    popup_enabled = st.checkbox("Enable Popup")
    popup_delay = st.slider("Delay (seconds)", 1, 30, 5)
    popup_title = st.text_input("Popup Headline", "Wait! Don't leave empty handed.")
    popup_text = st.text_input("Popup Body", "Get our free pricing guide on WhatsApp.")
    popup_cta = st.text_input("Popup Button", "Get it Now")

with tabs[3]:
    st.subheader("💰 Pricing")
    col_p1, col_p2, col_p3 = st.columns(3)
    titan_price = col_p1.text_input("Setup Price", "$199")
    titan_mo = col_p1.text_input("Monthly Fee", "$0")
    wix_name = col_p2.text_input("Competitor", "Wix")
    wix_mo = col_p2.text_input("Comp. Monthly", "$29/mo")
    save_val = col_p3.text_input("Savings", "$1,466")

with tabs[4]:
    st.subheader("🛒 Store & Payments")
    st.info("💡 **2050 AR Protocol:** In your Store CSV, make Column F (the 6th column) a link to a `.glb` 3D model to enable native Augmented Reality.")
    sheet_url = st.text_input("Store CSV", placeholder="https://docs.google.com/spreadsheets/d/e/.../pub?output=csv")
    custom_feat = st.text_input("Default Product Img", "https://images.unsplash.com/photo-1460925895917-afdab827c52f?q=80&w=800")
    col_pay1, col_pay2 = st.columns(2)
    paypal_link = col_pay1.text_input("PayPal Link", "https://paypal.me/yourid")
    upi_id = col_pay2.text_input("UPI ID", "name@upi")

with tabs[5]:
    st.subheader("📅 Booking Engine")
    booking_embed = st.text_area("Embed Code", height=150, value='<!-- Calendly inline widget begin -->\n<div class="calendly-inline-widget" data-url="https://calendly.com/titan-demo/30min" style="min-width:320px;height:630px;"></div>\n<script type="text/javascript" src="https://assets.calendly.com/assets/external/widget.js" async></script>\n<!-- Calendly inline widget end -->')
    booking_title = st.text_input("Booking Title", "Book an Appointment")
    booking_desc = st.text_input("Booking Subtext", "Select a time slot.")

with tabs[6]:
    st.subheader("📰 Blog")
    blog_sheet_url = st.text_input("Blog CSV", placeholder="https://docs.google.com/spreadsheets/d/e/.../pub?output=csv")
    blog_hero_title = st.text_input("Blog Title", "Latest Insights")
    blog_hero_sub = st.text_input("Blog Subtext", "Thoughts on tech.")

with tabs[7]:
    st.subheader("Legal")
    testi_data = st.text_area("Testimonials", "Rajesh Gupta | Titan stopped the bleeding.\nSarah Jenkins | Easy updates.", height=100)
    faq_data = st.text_area("FAQ", "Do I pay $0? ? Yes.\nIs it secure? ? Yes.", height=100)
    priv_txt = st.text_area("Privacy", "We collect minimum data.", height=100)
    term_txt = st.text_area("Terms", "You own the code.", height=100)

with tabs[8]:
    st.subheader("🪐 InterPlanetary File System (IPFS) Deployment")
    st.markdown("Host your site on the decentralized Web3 network. It can never be taken down, and costs $0/month.")
    pinata_jwt = st.text_input("Pinata API JWT (Leave blank for standard ZIP download)", type="password")


# --- 5. COMPILER ENGINE (READABLE & COMPLETE) ---

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
            if not in_list: 
                html_out += '<ul style="margin-bottom:1rem; padding-left:1.5rem;">'
                in_list = True
            html_out += f'<li style="margin-bottom:0.5rem; opacity:0.9; color:inherit;">{clean_line[2:]}</li>'
        else:
            if in_list: 
                html_out += "</ul>"
                in_list = False
            html_out += f"<p style='margin-bottom:1rem; opacity:0.9; color:inherit;'>{clean_line}</p>"
    if in_list: html_out += "</ul>"
    return html_out

def gen_schema():
    schema = {
        "@context": "https://schema.org", 
        "@type": "LocalBusiness", 
        "name": biz_name, 
        "image": logo_url or hero_img_1, 
        "telephone": biz_phone, 
        "email": biz_email, 
        "url": prod_url, 
        "description": seo_d
    }
    return f'<script type="application/ld+json">{json.dumps(schema)}</script>'

def gen_pwa_manifest():
    return json.dumps({
        "name": biz_name, 
        "short_name": pwa_short, 
        "start_url": "./index.html",
        "display": "standalone", 
        "background_color": "#ffffff", 
        "theme_color": p_color,
        "description": pwa_desc, 
        "icons": [{"src": pwa_icon, "sizes": "512x512", "type": "image/png", "purpose": "any maskable"}]
    })

def gen_sw():
    return """
    const CACHE_NAME = 'titan-v50-cache';
    const urlsToCache = ['./index.html', './about.html', './contact.html', './product.html', './blog.html', './post.html'];
    
    self.addEventListener('install', (e) => { 
        e.waitUntil(caches.open(CACHE_NAME).then((cache) => cache.addAll(urlsToCache))); 
        self.skipWaiting(); 
    });
    
    self.addEventListener('fetch', (e) => { 
        if (e.request.url.includes('google.com/spreadsheets')) {
            e.respondWith(fetch(e.request).then(res => {
                const resClone = res.clone(); 
                caches.open('titan-data').then(cache => cache.put(e.request, resClone)); 
                return res;
            }).catch(() => caches.match(e.request)));
        } else {
            e.respondWith(caches.match(e.request).then((response) => response || fetch(e.request)));
        }
    });
    """

def get_theme_css():
    bg_color, text_color, card_bg, glass_nav = "#ffffff", "#0f172a", "#ffffff", "rgba(255, 255, 255, 0.95)"
    
    if "Midnight" in theme_mode: 
        bg_color, text_color, card_bg, glass_nav = "#0f172a", "#f8fafc", "#1e293b", "rgba(15, 23, 42, 0.9)"
    elif "Cyberpunk" in theme_mode: 
        bg_color, text_color, card_bg, glass_nav = "#050505", "#00ff9d", "#111", "rgba(0,0,0,0.8)"
    elif "Luxury" in theme_mode: 
        bg_color, text_color, card_bg, glass_nav = "#1c1c1c", "#D4AF37", "#2a2a2a", "rgba(28,28,28,0.95)"
    elif "Forest" in theme_mode: 
        bg_color, text_color, card_bg, glass_nav = "#f1f8e9", "#1b5e20", "#ffffff", "rgba(241,248,233,0.9)"
    elif "Ocean" in theme_mode: 
        bg_color, text_color, card_bg, glass_nav = "#e0f7fa", "#006064", "#ffffff", "rgba(224,247,250,0.9)"
    elif "Stark" in theme_mode: 
        bg_color, text_color, card_bg, glass_nav = "#ffffff", "#000000", "#ffffff", "rgba(255,255,255,1)"

    anim_css = ""
    if anim_type == "Fade Up":
        anim_css = ".reveal { opacity: 0; transform: translateY(30px); transition: all 0.8s ease-out; } .reveal.active { opacity: 1; transform: translateY(0); }"
    elif anim_type == "Zoom In":
        anim_css = ".reveal { opacity: 0; transform: scale(0.95); transition: all 0.8s cubic-bezier(0.175, 0.885, 0.32, 1.275); } .reveal.active { opacity: 1; transform: scale(1); }"
    
    hero_align = "text-align: center; justify-content: center;"
    if hero_layout == "Left":
        hero_align = "text-align: left; justify-content: flex-start; align-items: center;"

    card_hover_css = "box-shadow: 0 20px 40px -10px rgba(0,0,0,0.15); transform: translateY(-5px);"
    if card_hover_style == "Primary Color Border": 
        card_hover_css += f" border-color: var(--p);"
    elif card_hover_style == "Accent Color Border (Red)": 
        card_hover_css += f" border-color: var(--s);"
    else: 
        card_hover_css += f" border-color: transparent;"

    return f"""
    :root {{
        --p: {p_color}; --s: {s_color}; --btn-txt: {btn_txt_color};
        --bg: {bg_color}; --txt: {text_color}; --card: {card_bg};
        --radius: {border_rad}; --nav: {glass_nav};
        --h-font: '{h_font}', sans-serif; --b-font: '{b_font}', sans-serif;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    html {{ scroll-behavior: smooth; font-size: 16px; }}
    body {{ background-color: var(--bg); color: var(--txt); font-family: var(--b-font); line-height: 1.6; overflow-x: hidden; transition: background 0.3s, color 0.3s; }}
    
    body.dark-mode {{ --bg: #0f172a; --txt: #f8fafc; --card: #1e293b; --nav: rgba(15, 23, 42, 0.95); }}
    
    p, h1, h2, h3, h4, h5, h6, span, li, div {{ color: inherit; }}
    h1, h2, h3, h4 {{ font-family: var(--h-font); color: var(--p); line-height: 1.2; margin-bottom: 1rem; }}
    strong {{ color: var(--p); font-weight: 800; }}
    h1 {{ font-size: clamp(2.5rem, 5vw, 4.5rem); }}
    h2 {{ font-size: clamp(2rem, 4vw, 3rem); }}
    p {{ margin-bottom: 1rem; }}
    
    .hero {{ position: relative; min-height: 90vh; overflow: hidden; display: flex; {hero_align} color: white; padding-top: 180px; background-color: var(--p); }}
    .carousel-slide {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; background-size: cover; background-position: center; opacity: 0; transition: opacity 1.5s ease-in-out; z-index: 0; }}
    .carousel-slide.active {{ opacity: 1; }}
    .hero-overlay {{ background: rgba(0,0,0,{overlay_opacity}); position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 1; }}
    .hero-content {{ z-index: 2; position: relative; width: 100%; padding: 0 20px; }}
    .hero h1 {{ color: #ffffff !important; text-shadow: 0 4px 20px rgba(0,0,0,0.4); }}
    .hero p {{ color: rgba(255,255,255,0.95) !important; font-size: clamp(1.1rem, 2vw, 1.3rem); max-width: 700px; margin: 0 auto 2rem auto; text-shadow: 0 2px 10px rgba(0,0,0,0.4); }}
    
    input, textarea, select {{ width: 100%; padding: 0.8rem; margin-bottom: 1rem; border: 1px solid #ccc; border-radius: 6px; font-family: inherit; }}
    label {{ color: var(--txt); font-weight: bold; margin-bottom: 0.5rem; display: block; }}
    .container {{ max-width: 1280px; margin: 0 auto; padding: 0 20px; }}
    
    .btn {{ 
        display: inline-flex; align-items: center; justify-content: center;
        padding: 1rem 2rem; border-radius: var(--radius); 
        font-weight: 700; text-decoration: none; transition: 0.3s; 
        text-transform: uppercase; cursor: pointer; border: none; text-align: center;
        line-height: 1.4; min-height: 3.5rem; word-wrap: break-word;
    }}
    .btn-primary {{ background: var(--p); color: var(--btn-txt) !important; }}
    .btn-accent {{ background: var(--s); color: var(--btn-txt) !important; box-shadow: 0 10px 25px -5px var(--s); }}
    .btn:hover {{ transform: translateY(-3px); filter: brightness(1.15); }}
    
    nav#main-navbar {{ position: fixed; top: 0; width: 100%; z-index: 1000; background: var(--nav); backdrop-filter: blur(12px); border-bottom: 1px solid rgba(100,100,100,0.1); padding: 1rem 0; transition: top 0.3s; }}
    .nav-flex {{ display: flex; justify-content: space-between; align-items: center; }}
    .nav-links {{ display: flex; align-items: center; gap: 1.5rem; }}
    .nav-links a {{ text-decoration: none; font-weight: 600; color: var(--txt); font-size: 0.9rem; transition:0.2s; }}
    .nav-links a:hover {{ color: var(--s); }}
    .mobile-menu {{ display: none; font-size: 1.5rem; cursor: pointer; }}
    
    main section {{ padding: clamp(2rem, 4vw, 4rem) 0; }}
    .section-head {{ text-align: center; margin-bottom: clamp(1rem, 3vw, 2.5rem); }}
    .grid-3 {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem; }}
    .about-grid, .detail-view {{ display: grid; grid-template-columns: 1fr 1fr; gap: 4rem; align-items: center; }}
    .contact-grid {{ display: grid; grid-template-columns: 1fr 2fr; gap: 3rem; }}
    
    .card {{ background: var(--card); border-radius: var(--radius); border: 1px solid rgba(100,100,100,0.1); transition: 0.3s; display: flex; flex-direction: column; overflow: hidden; }}
    .card:hover {{ {card_hover_css} }}
    
    .card h3, .card h4, .card a:not(.btn) {{ color: var(--txt) !important; text-decoration: none; }}
    
    .card-body {{ padding: 1.5rem; display: flex; flex-direction: column; flex-grow: 1; }}
    .card-desc {{ font-size: 0.9rem; opacity: 0.8; margin-bottom: 1.5rem; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }}
    .prod-img {{ width: 100%; height: 250px; object-fit: cover; background: #f1f5f9; }}
    
    .gallery-thumbs {{ display: flex; gap: 10px; margin-top: 15px; overflow-x: auto; }}
    .thumb {{ width: 60px; height: 60px; border-radius: 8px; object-fit: cover; cursor: pointer; border: 2px solid transparent; opacity: 0.7; transition: 0.2s; }}
    .thumb:hover, .thumb.active {{ border-color: var(--s); opacity: 1; }}

    .pricing-wrapper {{ overflow-x: auto; -webkit-overflow-scrolling: touch; width: 100%; margin: 0 auto; }}
    .pricing-table {{ width: 100%; border-collapse: collapse; min-width: 100%; }}
    .pricing-table th {{ background: var(--p); color: white; padding: 1.5rem 1rem; text-align: left; }}
    .pricing-table td {{ padding: 1.5rem 1rem; border-bottom: 1px solid rgba(100,100,100,0.1); background: var(--card); color: var(--txt); }}

    details {{ background: var(--card); border: 1px solid rgba(100,100,100,0.1); border-radius: 8px; margin-bottom: 1rem; padding: 1rem; cursor: pointer; color: var(--txt); }}
    details summary {{ font-weight: bold; font-size: 1.1rem; color: var(--txt); }}

    footer {{ background: var(--p); color: white; padding: 4rem 0; margin-top: auto; }}
    .footer-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 3rem; }}
    footer a {{ color: rgba(255,255,255,0.8) !important; text-decoration: none; display: block; margin-bottom: 0.5rem; transition: 0.3s; }}
    footer a:hover {{ color: #ffffff !important; text-decoration: underline; }}
    .social-icon {{ width: 24px; height: 24px; fill: rgba(255,255,255,0.7); transition: 0.3s; }}
    .social-icon:hover {{ fill: #ffffff; transform: scale(1.1); }}

    .blog-badge {{ background: var(--s); color: var(--btn-txt); padding: 0.3rem 0.8rem; border-radius: 50px; font-size: 0.75rem; text-transform: uppercase; font-weight: bold; width: fit-content; margin-bottom: 1rem; display:inline-block; }}
    
    #cart-float {{ position: fixed; bottom: 100px; right: 30px; background: var(--p); color: var(--btn-txt); padding: 15px 20px; border-radius: 50px; box-shadow: 0 10px 20px rgba(0,0,0,0.2); cursor: pointer; z-index: 998; display: flex; align-items: center; gap: 10px; font-weight: bold; }}
    #cart-modal {{ display: none; position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); background: var(--card); width: 90%; max-width: 500px; padding: 2rem; border-radius: 16px; box-shadow: 0 20px 50px rgba(0,0,0,0.3); z-index: 1001; border: 1px solid rgba(128,128,128,0.2); color: var(--txt); }}
    #cart-overlay, #lang-overlay {{ display: none; position: fixed; inset: 0; background: rgba(0,0,0,0.5); z-index: 1000; }}
    .cart-item {{ display: flex; justify-content: space-between; border-bottom: 1px solid #eee; padding: 10px 0; }}
    
    .local-vault {{ background: rgba(128,128,128,0.05); padding: 1rem; border-radius: 8px; margin-top: 1rem; border: 1px solid rgba(128,128,128,0.1); }}
    .local-vault input {{ width: 100%; padding: 0.8rem; margin-top: 0.5rem; border-radius: 6px; border: 1px solid #ccc; background: var(--bg); color: var(--txt); }}
    
    #voice-btn {{ position: fixed; bottom: 170px; right: 30px; background: var(--p); color: var(--btn-txt); border-radius: 50px; width: 50px; height: 50px; display: flex; align-items: center; justify-content: center; font-size: 1.2rem; cursor: pointer; box-shadow: 0 10px 20px rgba(0,0,0,0.2); z-index: 998; border: none; }}
    .listening {{ animation: pulse 1s infinite; background: var(--s) !important; }}
    @keyframes pulse {{ 0% {{ transform: scale(1); }} 50% {{ transform: scale(1.1); }} 100% {{ transform: scale(1); }} }}
    model-viewer {{ width: 100%; height: 400px; background-color: transparent; border-radius: 12px; }}

    #lang-modal {{ display: none; position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); background: var(--card); width: 90%; max-width: 400px; padding: 2rem; border-radius: 12px; z-index: 1002; color: var(--txt); text-align: center; }}
    .lang-opt {{ display: block; width: 100%; padding: 1rem; border: 1px solid #eee; margin-bottom: 0.5rem; border-radius: 8px; cursor: pointer; font-weight: bold; text-decoration: none; color: var(--txt); }}
    .lang-opt:hover {{ background: var(--s); color: white; }}
    
    .share-row {{ display: flex; gap: 10px; margin-top: 20px; flex-wrap: wrap; }}
    .share-btn {{ width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; border-radius: 50%; color: white; transition: 0.3s; cursor: pointer; border: none; text-decoration: none; }}
    .share-btn svg {{ width: 20px; height: 20px; fill: white; }}
    .bg-fb {{ background: #1877F2; }} .bg-x {{ background: #000000; }} .bg-li {{ background: #0A66C2; }} .bg-wa {{ background: #25D366; }} .bg-rd {{ background: #FF4500; }} .bg-link {{ background: #64748b; }}
    
    #top-bar {{ position: fixed; top: 0; width: 100%; background: var(--s); color: var(--btn-txt); text-align: center; padding: 10px; z-index: 1002; font-weight: bold; font-size: 0.9rem; transition: transform 0.3s; }}
    #top-bar a {{ color: var(--btn-txt); text-decoration: underline; }}
    
    #lead-popup {{ display: none; position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); background: var(--card); padding: 3rem; text-align: center; border-radius: var(--radius); z-index: 2000; box-shadow: 0 25px 100px rgba(0,0,0,0.5); width: 90%; max-width: 450px; border: 1px solid rgba(0,0,0,0.1); color: var(--txt); }}
    .close-popup {{ position: absolute; top: 15px; right: 15px; cursor: pointer; font-size: 1.5rem; opacity: 0.5; }}
    
    #theme-toggle {{ position: fixed; bottom: 30px; left: 30px; width: 40px; height: 40px; background: var(--card); border-radius: 50%; display: flex; align-items: center; justify-content: center; box-shadow: 0 5px 15px rgba(0,0,0,0.1); cursor: pointer; z-index: 999; font-size: 1.2rem; border: 1px solid rgba(0,0,0,0.1); }}
    
    {anim_css}
    @media (max-width: 768px) {{
        nav#main-navbar .nav-links {{ position: fixed; top: 60px; left: -100%; width: 100%; height: calc(100vh - 60px); background: var(--bg); flex-direction: column; padding: 2rem; transition: 0.3s; align-items: flex-start; gap: 1.5rem; overflow-y: auto; }}
        nav#main-navbar .nav-links.active {{ left: 0; }}
        .mobile-menu {{ display: block; }}
        .about-grid, .contact-grid, .detail-view, .grid-3 {{ grid-template-columns: 1fr !important; }}
    }}
    /* 👉 ADD THIS NEW LINE HERE: */
        .pricing-table th, .pricing-table td {{ padding: 1rem 0.5rem; font-size: 0.85rem; }}
    }}
    """

def gen_2050_scripts():
    context_js = "if(new Date().getHours() >= 19 || new Date().getHours() <= 6) document.body.classList.add('dark-mode');" if enable_context else ""
    ab_js = "let variant = localStorage.getItem('titan_ab') || (Math.random() > 0.5 ? 'A' : 'B'); localStorage.setItem('titan_ab', variant); if(variant === 'B') document.documentElement.style.setProperty('--s', '#10b981');" if enable_ab else ""
    voice_js = "function startVoiceSearch() { if (!('webkitSpeechRecognition' in window)) return alert('Voice search not supported in this browser.'); const rec = new webkitSpeechRecognition(); rec.lang = 'en-US'; const btn = document.getElementById('voice-btn'); btn.classList.add('listening'); rec.onresult = (e) => { const transcript = e.results[0][0].transcript.toLowerCase(); alert('Searching for: ' + transcript); document.querySelectorAll('.card').forEach(c => { c.style.display = c.innerText.toLowerCase().includes(transcript) ? 'flex' : 'none'; }); }; rec.onend = () => btn.classList.remove('listening'); rec.start(); }" if enable_voice else ""
    return f"<script defer>{context_js} {ab_js} {voice_js}</script>"

def gen_nav():
    logo_display = f'<img src="{logo_url}" height="40" alt="{biz_name} Logo" loading="lazy">' if logo_url else f'<span style="font-weight:900; font-size:1.5rem; color:var(--p)">{biz_name}</span>'
    blog_link = '<a href="blog.html" onclick="toggleMenu()">Blog</a>' if show_blog else ''
    book_link = '<a href="booking.html" onclick="toggleMenu()">Book Now</a>' if show_booking else ''
    lang_btn = f'<a href="#" onclick="openLangModal()" aria-label="Switch Language">🌐 ES</a>' if lang_sheet else ''
    
    return f"""
    {f'<div id="top-bar"><a href="{top_bar_link}">{top_bar_text}</a></div>' if top_bar_enabled else ''}
    <nav id="main-navbar">
        <div class="container nav-flex">
            <a href="index.html" aria-label="Home" style="text-decoration:none;">{logo_display}</a>
            <div class="mobile-menu" onclick="document.querySelector('.nav-links').classList.toggle('active')">☰</div>
            <div class="nav-links">
                <a href="index.html" onclick="toggleMenu()">Home</a>
                {'<a href="index.html#features" onclick="toggleMenu()">Features</a>' if show_features else ''}
                {'<a href="index.html#pricing" onclick="toggleMenu()">Savings</a>' if show_pricing else ''}
                {'<a href="index.html#inventory" onclick="toggleMenu()">Store</a>' if show_inventory else ''}
                {blog_link}
                {book_link}
                {lang_btn}
                <a href="contact.html" onclick="toggleMenu()">Contact</a>
                <a href="tel:{biz_phone}" class="btn btn-accent" style="padding:0.6rem 1.5rem; border-radius:50px;">Call Now</a>
            </div>
        </div>
    </nav>
    <div id="theme-toggle" onclick="document.body.classList.toggle('dark-mode')" aria-label="Toggle Dark Mode">🌓</div>
    <script>
        function toggleMenu() {{ document.querySelector('.nav-links').classList.remove('active'); }}
        if({str(top_bar_enabled).lower()}) {{ document.querySelector('#main-navbar').style.top = '40px'; }}
    </script>
    """

def gen_hero():
    bg_media = f"""
    <div class="carousel-slide active" style="background-image: url('{hero_img_1}')"></div>
    <div class="carousel-slide" style="background-image: url('{hero_img_2}')"></div>
    <div class="carousel-slide" style="background-image: url('{hero_img_3}')"></div>
    <script defer>
        let slides = document.querySelectorAll('.carousel-slide'); let currentSlide = 0; 
        setInterval(() => {{ slides[currentSlide].classList.remove('active'); currentSlide = (currentSlide + 1) % slides.length; slides[currentSlide].classList.add('active'); }}, 4000);
    </script>
    """
    if hero_video_id: 
        bg_media = f'<iframe src="https://www.youtube.com/embed/{hero_video_id}?autoplay=1&mute=1&loop=1&playlist={hero_video_id}&controls=0&showinfo=0&rel=0" style="position:absolute; top:50%; left:50%; width:100vw; height:100vh; transform:translate(-50%, -50%); pointer-events:none; object-fit:cover; z-index:0; min-width:177.77vh; min-height:56.25vw;" frameborder="0" allow="autoplay; encrypted-media"></iframe>'
    
    return f"""
    <section class="hero">
        <div class="hero-overlay"></div>
        {bg_media}
        <div class="container hero-content">
            <h1 id="hero-title">{hero_h}</h1>
            <p id="hero-sub">{hero_sub}</p>
            <div style="display:flex; gap:1rem; flex-wrap:wrap; {'justify-content:center;' if hero_layout == 'Center' else ''}">
                <a href="#inventory" class="btn btn-accent">Explore Now</a>
                <a href="contact.html" class="btn" style="background:rgba(255,255,255,0.2); backdrop-filter:blur(10px); color:white !important;">Contact Us</a>
            </div>
        </div>
    </section>
    """

def get_simple_icon(name):
    icon_map = {
        "bolt": "M11 21h-1l1-7H7.5c-.58 0-.57-.32-.38-.66.19-.34.05-.08.07-.12C8.48 10.94 10.42 7.54 13 3h1l-1 7h3.5c.49 0 .56.33.47.51l-.07.15C12.96 17.55 11 21 11 21z", 
        "wallet": "M21 18v1c0 1.1-.9 2-2 2H5c-1.11 0-2-.9-2-2V5c0-1.1.89-2 2-2h14c1.1 0 2 .9 2 2v1h-9c-1.11 0-2 .9-2 2v8c0 1.1.89 2 2 2h9zm-9-2h10V8H12v8zm4-2.5c-.83 0-1.5-.67-1.5-1.5s.67-1.5 1.5-1.5 1.5.67 1.5 1.5-.67 1.5-1.5 1.5z", 
        "table": "M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zM5 19V5h14v14H5zm2-2h10v-2H7v2zm0-4h10v-2H7v2zm0-4h10V7H7v2z", 
        "shield": "M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4zm0 10.99h7c-.53 4.12-3.28 7.79-7 8.94V12H5V6.3l7-3.11v8.8z"
    }
    path = icon_map.get(name.lower().strip(), "M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z")
    return f'<svg viewBox="0 0 24 24" width="32" height="32" fill="currentColor"><path d="{path}"/></svg>'

def gen_features():
    cards = "".join([f'<div class="card reveal"><div style="color:var(--s); margin-bottom:1rem;">{get_simple_icon(p[0])}</div><h3>{p[1].strip()}</h3><div>{format_text(p[2].strip())}</div></div>' for l in feat_data_input.split('\n') if (p:=l.split('|')) and len(p)>=3])
    return f'<section id="features"><div class="container"><div class="section-head reveal"><h2 id="feature-title">{f_title}</h2></div><div class="grid-3">{cards}</div></div></section>'

def gen_stats():
    return f"""
    <div style="background:var(--p); color:white; padding:3rem 0; text-align:center;">
        <div class="container grid-3">
            <div class="reveal"><h3 style="color:#ffffff; margin:0; font-size:3rem;">{stat_1}</h3><p style="color:rgba(255,255,255,0.7);">{label_1}</p></div>
            <div class="reveal"><h3 style="color:#ffffff; margin:0; font-size:3rem;">{stat_2}</h3><p style="color:rgba(255,255,255,0.7);">{label_2}</p></div>
            <div class="reveal"><h3 style="color:#ffffff; margin:0; font-size:3rem;">{stat_3}</h3><p style="color:rgba(255,255,255,0.7);">{label_3}</p></div>
        </div>
    </div>
    """

def gen_pricing_table():
    if not show_pricing: return ""
    return f"""
    <section id="pricing">
        <div class="container">
            <div class="section-head reveal"><h2>Pricing</h2></div>
            <div class="pricing-wrapper reveal">
                <table class="pricing-table">
                    <thead><tr><th style="width:40%">Expense Category</th><th style="background:var(--s);">Titan</th><th>{wix_name}</th></tr></thead>
                    <tbody>
                        <tr><td>Initial Setup Fee</td><td><strong>{titan_price}</strong></td><td>$0</td></tr>
                        <tr><td>Annual Costs</td><td><strong>{titan_mo}</strong></td><td>{wix_mo}</td></tr>
                        <tr><td><strong>5-Year Savings</strong></td><td style="color:var(--s); font-size:1.3rem;">You Save {save_val}</td><td>$0</td></tr>
                    </tbody>
                </table>
            </div>
        </div>
    </section>
    """

def gen_csv_parser():
    return """
    <script defer>
    function parseCSVLine(str) { 
        const res = []; let cur = ''; let inQuote = false; 
        for (let i = 0; i < str.length; i++) { 
            const c = str[i]; 
            if (c === '"') { if (inQuote && str[i+1] === '"') { cur += '"'; i++; } else { inQuote = !inQuote; } } 
            else if (c === ',' && !inQuote) { res.push(cur.trim()); cur = ''; } 
            else { cur += c; } 
        } 
        res.push(cur.trim()); return res; 
    } 
    function parseMarkdown(text) { return text ? text.replace(/\\r\\n/g, '\\n').replace(/\\n/g, '<br>').replace(/\\*\\*(.*?)\\*\\*/g, '<strong>$1</strong>') : ''; }
    </script>
    """

def gen_cart_system():
    if not wa_num: return ""
    clean_wa = wa_num.replace("+", "").replace(" ", "").replace("-", "")
    return f"""
    <div id="cart-float" onclick="toggleCart()" style="display:none;" aria-label="Cart">🛒 <span id="cart-count">0</span></div>
    <div id="cart-overlay" onclick="toggleCart()"></div>
    <div id="cart-modal">
        <h3>Your Cart</h3><div id="cart-items" style="max-height:200px; overflow-y:auto; margin:1rem 0;"></div>
        <div style="font-weight:bold; font-size:1.2rem; margin-bottom:1rem; text-align:right;">Total: <span id="cart-total">0.00</span></div>
        <div class="local-vault">
            <h4 style="font-size:0.9rem;">🔒 Fast Checkout Vault</h4>
            <input type="text" id="vault-name" placeholder="Full Name">
            <input type="text" id="vault-address" placeholder="Delivery Address">
        </div>
        <button onclick="checkoutWhatsApp()" class="btn btn-accent" style="width:100%; margin-top:1rem;">1-Click Checkout via WhatsApp</button>
    </div>
    <script defer>
    let cart = JSON.parse(localStorage.getItem('titanCart')) || [];
    document.getElementById('vault-name').value = localStorage.getItem('t_name') || ''; document.getElementById('vault-address').value = localStorage.getItem('t_addr') || '';
    
    function renderCart() {{
        const box = document.getElementById('cart-items'); if(!box) return; box.innerHTML = ''; let total = 0;
        cart.forEach((item, i) => {{ 
            total += parseFloat(item.price.replace(/[^0-9.]/g, '')) || 0; 
            box.innerHTML += `<div class="cart-item"><span>${{item.name}}</span><span>${{item.price}} <span onclick="remItem(${{i}})" style="color:red;cursor:pointer;">x</span></span></div>`; 
        }});
        document.getElementById('cart-count').innerText = cart.length; 
        document.getElementById('cart-total').innerText = total.toFixed(2);
        document.getElementById('cart-float').style.display = cart.length > 0 ? 'flex' : 'none';
        localStorage.setItem('titanCart', JSON.stringify(cart));
    }}
    
    function addToCart(name, price) {{ cart.push({{name, price}}); renderCart(); alert(name + " added!"); }}
    function remItem(i) {{ cart.splice(i,1); renderCart(); }}
    function toggleCart() {{ const m = document.getElementById('cart-modal'); m.style.display = m.style.display === 'block' ? 'none' : 'block'; document.getElementById('cart-overlay').style.display = m.style.display; }}
    
    function checkoutWhatsApp() {{
        const n = document.getElementById('vault-name').value; const a = document.getElementById('vault-address').value;
        localStorage.setItem('t_name', n); localStorage.setItem('t_addr', a);
        let msg = "New Order:%0A"; let total = 0;
        cart.forEach(i => {{ msg += `- ${{i.name}} (${{i.price}})%0A`; total += parseFloat(i.price.replace(/[^0-9.]/g,'')) || 0; }});
        msg += `%0ATotal: ${{total.toFixed(2)}}%0A`; 
        if(n) msg += `%0ADeliver to: ${{n}}, ${{a}}`;
        {f"msg += '%0A(Variant: ' + localStorage.getItem('titan_ab') + ')';" if enable_ab else ""}
        msg += `%0A%0AUPI: {upi_id} | PayPal: {paypal_link}`;
        window.open(`https://wa.me/{clean_wa}?text=${{msg}}`, '_blank');
        cart = []; renderCart(); toggleCart();
    }}
    window.addEventListener('load', renderCart);
    </script>
    """

def gen_wa_widget():
    if not wa_num: return ""
    clean_wa = wa_num.replace("+", "").replace(" ", "").replace("-", "")
    return f"""
    <a href="https://wa.me/{clean_wa}" target="_blank" id="wa-widget" aria-label="Chat on WhatsApp">
        <svg viewBox="0 0 24 24" fill="white" width="32" height="32"><path d="M12.04 2c-5.46 0-9.91 4.45-9.91 9.91c0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38c1.45.79 3.08 1.21 4.74 1.21c5.46 0 9.91-4.45 9.91-9.91c0-2.65-1.03-5.14-2.9-7.01A9.816 9.816 0 0 0 12.04 2m.01 1.67c2.2 0 4.26.86 5.82 2.42a8.225 8.225 0 0 1 2.41 5.83c0 4.54-3.7 8.23-8.24 8.23c-1.48 0-2.93-.39-4.19-1.15l-.3-.17l-3.12.82l.83-3.04l-.2-.32a8.188 8.188 0 0 1-1.26-4.38c.01-4.54 3.7-8.24 8.25-8.24m-3.53 3.16c-.13 0-.35.05-.54.26c-.19.2-.72.7-.72 1.72s.73 2.01.83 2.14c.1.13 1.44 2.19 3.48 3.07c.49.21.87.33 1.16.43c.49.16.94.13 1.29.08c.4-.06 1.21-.5 1.38-.98c.17-.48.17-.89.12-.98c-.05-.09-.18-.13-.37-.23c-.19-.1-.1.13-.1.13s-1.13-.56-1.32-.66c-.19-.1-.32-.15-.45.05c-.13.2-.51.65-.62.78c-.11.13-.23.15-.42.05c-.19-.1-.8-.3-1.53-.94c-.57-.5-1.02-1.12-1.21-1.45c-.11-.19-.01-.29.09-.38c.09-.08.19-.23.29-.34c.1-.11.13-.19.19-.32c.06-.13.03-.24-.01-.34c-.05-.1-.45-1.08-.62-1.48c-.16-.4-.36-.34-.51-.35c-.11-.01-.25-.01-.4-.01Z"/></path></svg>
    </a>
    <style>
        #wa-widget {{ position: fixed; bottom: 30px; right: 30px; background: #25D366; width: 60px; height: 60px; border-radius: 50%; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 12px rgba(0,0,0,0.3); z-index: 999; transition: transform 0.3s; }}
        #wa-widget:hover {{ transform: scale(1.1); }}
    </style>
    """

def gen_lang_script():
    if not lang_sheet: return ""
    return f"""
    <div id="lang-overlay" onclick="closeLangModal()"></div>
    <div id="lang-modal">
        <h3 style="margin-bottom:1.5rem; border-bottom:1px solid #eee; padding-bottom:10px;">Select Language</h3>
        <div class="lang-grid" style="display:grid; grid-template-columns: 1fr 1fr; gap:10px;">
            <div onclick="switchLang('en', 0)" class="lang-opt">🇺🇸 English</div>
            <div onclick="switchLang('es', 1)" class="lang-opt">🇪🇸 Español</div>
            <div onclick="switchLang('fr', 2)" class="lang-opt">🇫🇷 Français</div>
            <div onclick="switchLang('de', 3)" class="lang-opt">🇩🇪 Deutsch</div>
            <div onclick="switchLang('hi', 4)" class="lang-opt">🇮🇳 हिन्दी</div>
            <div onclick="switchLang('bn', 5)" class="lang-opt">🇧🇩 বাংলা</div>
        </div>
    </div>
    <script defer>
    function openLangModal() {{ document.getElementById('lang-modal').style.display='block'; document.getElementById('lang-overlay').style.display='block'; }} 
    function closeLangModal() {{ document.getElementById('lang-modal').style.display='none'; document.getElementById('lang-overlay').style.display='none'; }} 
    
    async function switchLang(langCode, colIndex) {{ 
        closeLangModal(); 
        
        // Save user preference
        localStorage.setItem('titan_lang', langCode);
        localStorage.setItem('titan_col', colIndex);

        // If English, reload to reset (default)
        if(langCode === 'en') {{ location.reload(); return; }} 
        
        try {{ 
            const res = await fetch('{lang_sheet}'); 
            const txt = await res.text(); 
            const lines = txt.split(/\\r\\n|\\n/); 
            
            for(let i=1; i<lines.length; i++) {{ 
                const row = parseCSVLine(lines[i]); 
                // Ensure the row has enough columns for the selected language
                if(row.length > colIndex) {{ 
                    const el = document.getElementById(row[0]); 
                    // Update text if element exists and translation is not empty
                    if(el && row[colIndex]) el.innerText = row[colIndex]; 
                }} 
            }} 
            
            // Update HTML lang attribute for SEO
            document.documentElement.lang = langCode;
            
        }} catch(e) {{ console.log("Lang Error", e); }} 
    }}

    // Auto-load saved language on page refresh
    window.addEventListener('load', () => {{
        const savedLang = localStorage.getItem('titan_lang');
        const savedCol = localStorage.getItem('titan_col');
        if(savedLang && savedLang !== 'en') {{
            switchLang(savedLang, parseInt(savedCol));
        }}
    }});
    </script>
    """

def gen_popup():
    if not popup_enabled: return ""
    return f"""
    <div id="lead-popup">
        <div class="close-popup" onclick="document.getElementById('lead-popup').style.display='none'">&times;</div>
        <h3>{popup_title}</h3><p>{popup_text}</p><a href="https://wa.me/{wa_num}?text=I want the offer" class="btn btn-accent" target="_blank">{popup_cta}</a>
    </div>
    <script defer>
    setTimeout(() => {{ 
        if(!localStorage.getItem('popupShown')) {{ document.getElementById('lead-popup').style.display = 'block'; localStorage.setItem('popupShown', 'true'); }} 
    }}, {popup_delay * 1000});
    </script>
    """

def gen_inventory_js(is_demo=False):
    demo_flag = "const isDemo = true;" if is_demo else "const isDemo = false;"
    return f"""
    {gen_csv_parser()}
    <script defer>
    {demo_flag}
    async function loadInv() {{
        try {{
            const res = await fetch('{sheet_url}'); const txt = await res.text(); const lines = txt.split(/\\r\\n|\\n/);
            const box = document.getElementById('inv-grid'); if(!box) return; box.innerHTML = '';
            for(let i=1; i<lines.length; i++) {{
                if(!lines[i].trim()) continue;
                const c = parseCSVLine(lines[i]);
                let allImgs = c[3] ? c[3].split('|') : []; let mainImg = allImgs.length > 0 ? allImgs[0] : '{custom_feat}';
                if(c.length > 1) {{
                    const pName = encodeURIComponent(c[0]);
                    box.innerHTML += `<div class="card reveal"><img src="${{mainImg}}" class="prod-img" loading="lazy" alt="${{c[0]}}"><div class="card-body"><h3>${{c[0]}}</h3><p style="font-weight:bold; color:var(--s); font-size:1.1rem;">${{c[1]}}</p><p class="card-desc">${{c[2]}}</p><div style="margin-top:auto; display:grid; grid-template-columns:1fr 1fr; gap:10px;"><button onclick="addToCart('${{c[0]}}', '${{c[1]}}')" class="btn btn-primary" style="padding:0.5rem; font-size:0.8rem;">Add</button><a href="product.html?item=${{pName}}" class="btn btn-accent" style="padding:0.5rem; font-size:0.8rem;">View Details</a></div></div></div>`;
                }}
            }}
        }} catch(e) {{ console.log(e); }}
    }}
    if(document.getElementById('inv-grid')) window.addEventListener('load', loadInv);
    </script>
    """

def gen_inventory():
    if not show_inventory: return ""
    voice_btn = '<button id="voice-btn" onclick="startVoiceSearch()" aria-label="Voice Search">🎤</button>' if enable_voice else ''
    return f'<section id="inventory" style="background:rgba(0,0,0,0.02)"><div class="container"><div class="section-head reveal"><h2 id="store-title">Store</h2></div><div id="inv-grid" class="grid-3"><div>Loading Edge Data...</div></div></div>{voice_btn}</section>{gen_inventory_js(is_demo=False)}'

def gen_about_section():
    if not show_gallery: return ""
    return f'<section id="about"><div class="container"><div class="about-grid"><div class="reveal"><h2 id="about-title">{about_h_in}</h2><div>{format_text(about_short_in)}</div><a href="about.html" class="btn btn-primary" style="margin-top:1rem;">Read More</a></div><img src="{about_img}" class="reveal" style="width:100%; border-radius:var(--radius);" loading="lazy" alt="About Us"></div></div></section>'

def gen_faq_section():
    if not show_faq: return ""
    items = "".join([f"<details class='reveal'><summary>{l.split('?')[0]}?</summary><p>{l.split('?')[1]}</p></details>" for l in faq_data.split('\n') if "?" in l])
    return f'<section id="faq"><div class="container" style="max-width:800px;"><div class="section-head reveal"><h2 id="faq-title">Frequently Asked Questions</h2></div>{items}</div></section>'

def gen_footer():
    icons = ""
    if fb_link: icons += f'<a href="{fb_link}" target="_blank" style="display:inline-block; margin-right:15px;" aria-label="Facebook"><svg class="social-icon" viewBox="0 0 24 24"><path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"></path></svg></a>'
    if ig_link: icons += f'<a href="{ig_link}" target="_blank" style="display:inline-block; margin-right:15px;" aria-label="Instagram"><svg class="social-icon" viewBox="0 0 24 24"><path d="M16.98 0a6.9 6.9 0 0 1 5.08 1.98A6.94 6.94 0 0 1 24 7.02v9.96c0 2.08-.68 3.87-1.98 5.13A7.14 7.14 0 0 1 16.94 24H7.06a7.06 7.06 0 0 1-5.03-1.89A6.96 6.96 0 0 1 0 16.94V7.02C0 2.8 2.8 0 7.02 0h9.96zM7.17 2.1c-1.4 0-2.6.48-3.46 1.33c-.85.85-1.33 2.06-1.33 3.46v10.3c0 1.3.47 2.5 1.33 3.36c.86.85 2.06 1.33 3.46 1.33h9.66c1.4 0 2.6-.48 3.46-1.33c.85-.85 1.33-2.06 1.33-3.46V6.89c0-1.4-.47-2.6-1.33-3.46c-.86-.85-2.06-1.33-3.46-1.33H7.17zm11.97 3.33c.77 0 1.4.63 1.4 1.4c0 .77-.63 1.4-1.4 1.4c-.77 0-1.4-.63-1.4-1.4c0-.77.63-1.4 1.4-1.4zM12 5.76c3.39 0 6.14 2.75 6.14 6.14c0 3.39-2.75 6.14-6.14 6.14c-3.39 0-6.14-2.75-6.14-6.14c0-3.39 2.75-6.14 6.14-6.14zm0 2.1c-2.2 0-3.99 1.79-3.99 4.04c0 2.25 1.79 4.04 3.99 4.04c2.2 0 3.99-1.79 3.99-4.04c0-2.25-1.79-4.04-3.99-4.04c0-2.25-1.79-4.04-3.99-4.04c0-2.25-1.79-4.04-3.99-4.04c0-2.25-1.79-4.04-3.99-4.04z"/></svg></a>'
    if x_link: icons += f'<a href="{x_link}" target="_blank" style="display:inline-block; margin-right:15px;" aria-label="X"><svg class="social-icon" viewBox="0 0 24 24"><path d="M18.901 1.153h3.68l-8.04 9.19L24 22.846h-7.406l-5.8-7.584l-6.638 7.584H.474l8.6-9.83L0 1.154h7.594l5.243 6.932ZM17.61 20.644h2.039L6.486 3.24H4.298Z"></path></svg></a>'
    if li_link: icons += f'<a href="{li_link}" target="_blank" style="display:inline-block; margin-right:15px;" aria-label="LinkedIn"><svg class="social-icon" viewBox="0 0 24 24"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2a2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6zM2 9h4v12H2zM4 2a2 2 0 1 1-2 2a2 2 0 0 1 2-2z"></path></svg></a>'
    
    return f"""
    <footer><div class="container"><div class="footer-grid">
    <div><h3 style="color:white; margin-bottom:1.5rem;">{biz_name}</h3><p style="color:rgba(255,255,255,0.7); opacity:1;">{biz_addr}</p><div style="margin-top:1.5rem;">{icons}</div></div>
    <div><h4 style="color:white; text-transform:uppercase;">Links</h4><a href="index.html" style="color:white!important; display:block; margin-bottom:0.5rem;" id="footer-home">Home</a><a href="blog.html" style="color:white!important; display:block; margin-bottom:0.5rem;" id="footer-blog">Blog</a><a href="booking.html" style="color:white!important; display:block; margin-bottom:0.5rem;" id="footer-book">Book Now</a></div>
    <div><h4 style="color:white; text-transform:uppercase;">Legal</h4><a href="privacy.html" style="color:white!important; display:block; margin-bottom:0.5rem;">Privacy</a><a href="terms.html" style="color:white!important; display:block; margin-bottom:0.5rem;">Terms</a></div>
    </div><div style="border-top:1px solid rgba(255,255,255,0.1); margin-top:3rem; padding-top:2rem; text-align:center; color:rgba(255,255,255,0.5);">&copy; {datetime.datetime.now().year} {biz_name}. Powered by Titan Engine.</div></div></footer>
    """

def gen_scripts():
    return "<script defer>window.addEventListener('scroll', () => { var r = document.querySelectorAll('.reveal'); for (var i = 0; i < r.length; i++) { if (r[i].getBoundingClientRect().top < window.innerHeight - 100) r[i].classList.add('active'); } }); window.dispatchEvent(new Event('scroll'));</script>"

def build_page(title, content, extra_js=""):
    # This line captures the ID from your sidebar
    gsc_meta = f'<meta name="google-site-verification" content="{gsc_tag}">' if gsc_tag else ""
    
    og_meta = f'<meta property="og:title" content="{title} | {biz_name}"><meta property="og:description" content="{seo_d}"><meta property="og:image" content="{og_image or logo_url}"><meta name="twitter:card" content="summary_large_image">'
    pwa_tags = f'<link rel="manifest" href="manifest.json"><meta name="theme-color" content="{p_color}"><link rel="apple-touch-icon" href="{pwa_icon}">'
    sw_script = "<script>if ('serviceWorker' in navigator) { navigator.serviceWorker.register('service-worker.js'); }</script>"
    ga_script = f"<script async src='https://www.googletagmanager.com/gtag/js?id={ga_tag}'></script><script>window.dataLayer = window.dataLayer || []; function gtag(){{dataLayer.push(arguments);}} gtag('js', new Date()); gtag('config', '{ga_tag}');</script>" if ga_tag else ""
    
    # I have inserted {gsc_meta} right after the description meta tag below
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>{title} | {biz_name}</title><meta name="description" content="{seo_d}">{gsc_meta}{og_meta}{pwa_tags}{gen_schema()}<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family={h_font.replace(' ', '+')}:wght@400;700;900&family={b_font.replace(' ', '+')}:wght@300;400;600&display=swap" rel="stylesheet"><style>{get_theme_css()}</style>{ga_script}{gen_2050_scripts()}</head><body><main>{gen_nav()}{content}{gen_footer()}{gen_wa_widget()}{gen_cart_system()}{gen_scripts()}{gen_lang_script()}{sw_script}{gen_popup()}{extra_js}</main></body></html>"""
# --- PAGE SPECIFIC GENERATORS ---

def gen_booking_content():
    if not show_booking: return ""
    return f'<section class="hero" style="min-height:30vh; background:var(--p);"><div class="container hero-content"><h1>{booking_title}</h1><p>{booking_desc}</p></div></section><section><div class="container" style="text-align:center;"><div style="background:white; border-radius:12px; overflow:hidden; box-shadow:0 10px 40px rgba(0,0,0,0.1); width:100%;">{booking_embed}</div></div></section>'

def gen_blog_index_html():
    if not show_blog: return ""
    return f"""
    <section class="hero" style="min-height:40vh; background-image: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('{hero_img_1}'); background-size: cover;">
        <div class="container hero-content"><h1>{blog_hero_title}</h1><p>{blog_hero_sub}</p></div>
    </section>
    <section><div class="container"><div id="blog-grid" class="grid-3">Loading Posts...</div></div></section>
    {gen_csv_parser()}
    <script defer>
    async function loadBlog() {{ 
        try {{ 
            const res = await fetch('{blog_sheet_url}'); const txt = await res.text(); const lines = txt.split(/\\r\\n|\\n/); 
            const box = document.getElementById('blog-grid'); box.innerHTML = ''; 
            for(let i=1; i<lines.length; i++) {{ 
                const r = parseCSVLine(lines[i]); 
                if(r.length > 4) {{ 
                    box.innerHTML += `<article class="card reveal" style="display:flex; flex-direction:column; justify-content:space-between;"><div><img src="${{r[5]}}" class="prod-img" loading="lazy" alt="${{r[1]}}"><span class="blog-badge" style="margin-top:1rem;">${{r[3]}}</span><h3 style="margin-top:0.5rem;"><a href="post.html?id=${{r[0]}}">${{r[1]}}</a></h3><p>${{r[4]}}</p></div><a href="post.html?id=${{r[0]}}" class="btn btn-primary" style="margin-top:1rem; width:100%;">Read More</a></article>`; 
                }} 
            }} 
        }} catch(e) {{ console.log(e); }} 
    }} 
    window.addEventListener('load', loadBlog);
    </script>
    """

def gen_product_page_content(is_demo=False):
    demo_flag = "const isDemo = true;" if is_demo else "const isDemo = false;"
    ar_script = '<script type="module" src="https://ajax.googleapis.com/ajax/libs/model-viewer/3.4.0/model-viewer.min.js"></script>' if enable_ar else ''
    return f"""
    {ar_script}
    <section style="padding-top:150px;"><div class="container"><a href="index.html#inventory" class="btn btn-outline" style="margin-bottom:2rem; border:2px solid var(--p);">&larr; Back to Store</a><div id="product-detail">Loading Product Data...</div></div></section>
    {gen_csv_parser()}
    <script defer>
    {demo_flag}
    function changeImg(src) {{ document.getElementById('main-img').src = src; }}
    async function loadProduct() {{
        const params = new URLSearchParams(window.location.search); let targetName = params.get('item'); if(isDemo && !targetName) targetName = "Demo Item";
        try {{
            const res = await fetch('{sheet_url}'); const txt = await res.text(); const lines = txt.split(/\\r\\n|\\n/);
            for(let i=1; i<lines.length; i++) {{
                const clean = parseCSVLine(lines[i]); if(isDemo) targetName = clean[0];
                if(clean[0] === targetName) {{
                    let allImgs = clean[3] ? clean[3].split('|') : ['{custom_feat}'];
                    let mainImg = allImgs[0]; let thumbHtml = '';
                    allImgs.forEach(img => {{ thumbHtml += `<img src="${{img.trim()}}" class="thumb" onclick="changeImg('${{img.trim()}}')" alt="Thumbnail">`; }});
                    
                    let mainMedia = `<img src="${{mainImg}}" id="main-img" style="width:100%; border-radius:12px; height:400px; object-fit:cover;" alt="${{clean[0]}}">`;
                    if({str(enable_ar).lower()} && clean.length > 5 && clean[5].includes('.glb')) {{
                        mainMedia = `<model-viewer src="${{clean[5]}}" ar ar-modes="webxr scene-viewer quick-look" camera-controls tone-mapping="neutral" shadow-intensity="1" auto-rotate></model-viewer><p style="text-align:center; font-size:0.8rem; margin-top:10px;">👆 Drag to rotate. Click AR icon to view in your space.</p>`;
                    }}

                    let stripe = (clean.length > 4 && clean[4].includes('http')) ? clean[4] : '';
                    let btn = stripe ? `<a href="${{stripe}}" class="btn btn-primary" style="width:100%;">Buy Now</a>` : `<button onclick="addToCart('${{clean[0]}}', '${{clean[1]}}')" class="btn btn-primary" style="width:100%; height:4rem; font-size:1.2rem;">Add to Cart</button>`;
                    const u = encodeURIComponent(window.location.href); const t = encodeURIComponent(clean[0]);
                    
                    document.getElementById('product-detail').innerHTML = `
                        <div class="detail-view">
                            <div>${{mainMedia}}<div class="gallery-thumbs">${{thumbHtml}}</div></div>
                            <div>
                                <h1 style="font-size:3rem; line-height:1.1;">${{clean[0]}}</h1><p style="font-size:1.5rem; color:var(--s); font-weight:bold; margin-bottom:1.5rem;">${{clean[1]}}</p><p>${{clean[2]}}</p>${{btn}}
                                
                                <div style="margin-top:2rem; border-top:1px solid rgba(128,128,128,0.2); padding-top:1.5rem;">
                                    <p style="font-size:0.9rem; font-weight:bold; margin-bottom:0.5rem;">Share this product:</p>
                                    <div class="share-row">
                                        <a href="https://wa.me/?text=Check%20out%20${{t}}%20${{u}}" target="_blank" class="share-btn bg-wa" title="Share on WhatsApp"><svg viewBox="0 0 24 24"><path d="M12.04 2c-5.46 0-9.91 4.45-9.91 9.91c0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38c1.45.79 3.08 1.21 4.74 1.21c5.46 0 9.91-4.45 9.91-9.91c0-2.65-1.03-5.14-2.9-7.01A9.816 9.816 0 0 0 12.04 2m.01 1.67c2.2 0 4.26.86 5.82 2.42a8.225 8.225 0 0 1 2.41 5.83c0 4.54-3.7 8.23-8.24 8.23c-1.48 0-2.93-.39-4.19-1.15l-.3-.17l-3.12.82l.83-3.04l-.2-.32a8.188 8.188 0 0 1-1.26-4.38c.01-4.54 3.7-8.24 8.25-8.24m-3.53 3.16c-.13 0-.35.05-.54.26c-.19.2-.72.7-.72 1.72s.73 2.01.83 2.14c.1.13 1.44 2.19 3.48 3.07c.49.21.87.33 1.16.43c.49.16.94.13 1.29.08c.4-.06 1.21-.5 1.38-.98c.17-.48.17-.89.12-.98c-.05-.09-.18-.13-.37-.23c-.19-.1-.1.13-.1.13s-1.13-.56-1.32-.66c-.19-.1-.32-.15-.45.05c-.13.2-.51.65-.62.78c-.11.13-.23.15-.42.05c-.19-.1-.8-.3-1.53-.94c-.57-.5-1.02-1.12-1.21-1.45c-.11-.19-.01-.29.09-.38c.09-.08.19-.23.29-.34c.1-.11.13-.19.19-.32c.06-.13.03-.24-.01-.34c-.05-.1-.45-1.08-.62-1.48c-.16-.4-.36-.34-.51-.35c-.11-.01-.25-.01-.4-.01Z"/></path></svg></a>
                                        <a href="https://www.facebook.com/sharer/sharer.php?u=${{u}}" target="_blank" class="share-btn bg-fb" title="Share on Facebook"><svg viewBox="0 0 24 24"><path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"></path></svg></a>
                                        <a href="https://twitter.com/intent/tweet?url=${{u}}&text=${{t}}" target="_blank" class="share-btn bg-x" title="Share on X"><svg viewBox="0 0 24 24"><path d="M18.901 1.153h3.68l-8.04 9.19L24 22.846h-7.406l-5.8-7.584l-6.638 7.584H.474l8.6-9.83L0 1.154h7.594l5.243 6.932ZM17.61 20.644h2.039L6.486 3.24H4.298Z"></path></svg></a>
                                        <a href="https://www.linkedin.com/shareArticle?mini=true&url=${{u}}&title=${{t}}" target="_blank" class="share-btn bg-li" title="Share on LinkedIn"><svg viewBox="0 0 24 24"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2a2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6zM2 9h4v12H2zM4 2a2 2 0 1 1-2 2a2 2 0 0 1 2-2z"></path></svg></a>
                                        <button onclick="navigator.clipboard.writeText(window.location.href); alert('Link Copied to Clipboard!');" class="share-btn bg-link" title="Copy Link" style="border:none; cursor:pointer;"><svg viewBox="0 0 24 24" fill="white"><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"/></svg></button>
                                    </div>
                                </div>
                            </div>
                        </div>`;
                    document.title = clean[0] + " | {biz_name}";
                    break;
                }}
            }}
        }} catch(e) {{}}
    }}
    window.addEventListener('load', loadProduct);
    </script>
    """

def gen_blog_post_html():
    if not show_blog: return ""
    return f"""
    <article id="post-container" style="padding-top:0px;">Loading Content...</article>
    {gen_csv_parser()}
    <script defer>
    async function loadPost() {{
        const params = new URLSearchParams(window.location.search); const slug = params.get('id');
        try {{
            const res = await fetch('{blog_sheet_url}'); const txt = await res.text(); const lines = txt.split(/\\r\\n|\\n/);
            const container = document.getElementById('post-container');
            for(let i=1; i<lines.length; i++) {{
                const r = parseCSVLine(lines[i]);
                if(r[0] === slug) {{
                    const contentHtml = parseMarkdown(r[6]); const u = encodeURIComponent(window.location.href); const t = encodeURIComponent(r[1]);
                    document.title = r[1] + " | {biz_name}";
                    
                    container.innerHTML = `
                        <header style="background:var(--p); padding: 120px 1rem 4rem 1rem; color:var(--btn-txt); text-align:center;">
                            <div class="container"><span class="blog-badge">${{r[3]}}</span><h1 style="font-size:clamp(1.8rem, 5vw, 3.5rem); margin-top:1rem; color:var(--btn-txt) !important;">${{r[1]}}</h1></div>
                        </header>
                        <div class="container" style="max-width:800px; padding:3rem 1.5rem;">
                            <img src="${{r[5]}}" style="width:100%; border-radius:12px; margin-bottom:2rem;" alt="${{r[1]}}">
                            <div style="line-height:1.8;">${{contentHtml}}</div>
                            
                            <div style="margin-top:4rem; border-top:1px solid rgba(128,128,128,0.2); padding-top:2rem;">
                                <p style="font-weight:bold; font-size:1.1rem; margin-bottom:0.5rem;">Share this article:</p>
                                <div class="share-row">
                                    <a href="https://wa.me/?text=${{t}}%20${{u}}" target="_blank" class="share-btn bg-wa" title="Share on WhatsApp"><svg viewBox="0 0 24 24"><path d="M12.04 2c-5.46 0-9.91 4.45-9.91 9.91c0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38c1.45.79 3.08 1.21 4.74 1.21c5.46 0 9.91-4.45 9.91-9.91c0-2.65-1.03-5.14-2.9-7.01A9.816 9.816 0 0 0 12.04 2m.01 1.67c2.2 0 4.26.86 5.82 2.42a8.225 8.225 0 0 1 2.41 5.83c0 4.54-3.7 8.23-8.24 8.23c-1.48 0-2.93-.39-4.19-1.15l-.3-.17l-3.12.82l.83-3.04l-.2-.32a8.188 8.188 0 0 1-1.26-4.38c.01-4.54 3.7-8.24 8.25-8.24m-3.53 3.16c-.13 0-.35.05-.54.26c-.19.2-.72.7-.72 1.72s.73 2.01.83 2.14c.1.13 1.44 2.19 3.48 3.07c.49.21.87.33 1.16.43c.49.16.94.13 1.29.08c.4-.06 1.21-.5 1.38-.98c.17-.48.17-.89.12-.98c-.05-.09-.18-.13-.37-.23c-.19-.1-.1.13-.1.13s-1.13-.56-1.32-.66c-.19-.1-.32-.15-.45.05c-.13.2-.51.65-.62.78c-.11.13-.23.15-.42.05c-.19-.1-.8-.3-1.53-.94c-.57-.5-1.02-1.12-1.21-1.45c-.11-.19-.01-.29.09-.38c.09-.08.19-.23.29-.34c.1-.11.13-.19.19-.32c.06-.13.03-.24-.01-.34c-.05-.1-.45-1.08-.62-1.48c-.16-.4-.36-.34-.51-.35c-.11-.01-.25-.01-.4-.01Z"/></path></svg></a>
                                    <a href="https://www.facebook.com/sharer/sharer.php?u=${{u}}" target="_blank" class="share-btn bg-fb" title="Share on Facebook"><svg viewBox="0 0 24 24"><path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"></path></svg></a>
                                    <a href="https://twitter.com/intent/tweet?url=${{u}}&text=${{t}}" target="_blank" class="share-btn bg-x" title="Share on X"><svg viewBox="0 0 24 24"><path d="M18.901 1.153h3.68l-8.04 9.19L24 22.846h-7.406l-5.8-7.584l-6.638 7.584H.474l8.6-9.83L0 1.154h7.594l5.243 6.932ZM17.61 20.644h2.039L6.486 3.24H4.298Z"></path></svg></a>
                                    <a href="https://www.linkedin.com/shareArticle?mini=true&url=${{u}}&title=${{t}}" target="_blank" class="share-btn bg-li" title="Share on LinkedIn"><svg viewBox="0 0 24 24"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2a2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6zM2 9h4v12H2zM4 2a2 2 0 1 1-2 2a2 2 0 0 1 2-2z"></path></svg></a>
                                    <button onclick="navigator.clipboard.writeText(window.location.href); alert('Link Copied to Clipboard!');" class="share-btn bg-link" title="Copy Link" style="border:none; cursor:pointer;"><svg viewBox="0 0 24 24" fill="white"><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"/></svg></button>
                                </div>
                            </div>
                            <hr style="margin:2rem 0; border:0; border-top:1px solid rgba(128,128,128,0.2);">
                            <a href="blog.html" class="btn btn-primary" style="display:inline-block; margin-top:1rem;">&larr; Back to Blog</a>
                        </div>`;
                    break;
                }}
            }}
        }} catch(e) {{}}
    }}
    window.addEventListener('load', loadPost);
    </script>
    """

def gen_inner_header(title):
    return f'<div class="hero" style="min-height: 40vh; background:var(--p);"><div class="container hero-content"><h1>{title}</h1></div></div>'

# --- 6. PAGE ASSEMBLY ---
home_content = ""
if show_hero: home_content += gen_hero()
if show_stats: home_content += gen_stats()
if show_features: home_content += gen_features()
if show_pricing: home_content += gen_pricing_table()
if show_inventory: home_content += gen_inventory()
if show_gallery: home_content += gen_about_section()
if show_testimonials: 
    t_cards = "".join([f'<div class="card reveal" style="text-align:center;"><i>"{x.split("|")[1]}"</i><br><b>- {x.split("|")[0]}</b></div>' for x in testi_data.split('\n') if "|" in x])
    home_content += f'<section style="background:#f8fafc"><div class="container"><div class="section-head reveal"><h2>Client Stories</h2></div><div class="grid-3">{t_cards}</div></div></section>'
if show_faq: home_content += gen_faq_section()
if show_cta: home_content += f'<section style="background:var(--s); color:white; text-align:center;"><div class="container reveal"><h2>Start Owning Your Future</h2><p style="margin-bottom:2rem;">Stop paying rent.</p><a href="contact.html" class="btn" style="background:white; color:var(--s) !important;">Get Started</a></div></section>'

# --- 7. DEPLOYMENT ---
st.divider()
st.subheader("🚀 2050 Launchpad")
preview_mode = st.radio("Preview Page:", ["Home", "About", "Contact", "Blog Index", "Blog Post (Demo)", "Privacy", "Terms", "Product Detail (Demo)", "Booking Page"], horizontal=True)

contact_content = f"""{gen_inner_header("Contact Us")}<section><div class="container"><div class="contact-grid"><div><div style="background:var(--card); padding:2rem; border-radius:12px; border:1px solid #eee;"><h3>Get In Touch</h3><p>{biz_addr}</p><p><a href="tel:{biz_phone}">{biz_phone}</a></p><p>{biz_email}</p><br><a href="https://wa.me/{wa_num}" target="_blank" class="btn btn-accent" style="width:100%;">WhatsApp Us</a></div></div><div class="card"><h3>Send Message</h3><form action="https://formsubmit.co/{biz_email}" method="POST"><label>Name</label><input type="text" name="name" required><label>Email</label><input type="email" name="email" required><label>Message</label><textarea name="msg" rows="4" required></textarea><button class="btn btn-primary" type="submit">Send</button></form></div></div><br><div style="border-radius:12px;overflow:hidden;">{map_iframe}</div></div></section>"""

c1, c2 = st.columns([3, 1])
with c1:
    if preview_mode == "Home": st.components.v1.html(build_page("Home", home_content), height=600, scrolling=True)
    # ADDED <section> tag here:
    elif preview_mode == "About": st.components.v1.html(build_page("About", f"{gen_inner_header('About')}<section><div class='container'>{format_text(about_long)}</div></section>"), height=600, scrolling=True)
    elif preview_mode == "Contact": st.components.v1.html(build_page("Contact", contact_content), height=600, scrolling=True)
    # ADDED <section> tag here:
    elif preview_mode == "Privacy": st.components.v1.html(build_page("Privacy", f"{gen_inner_header('Privacy')}<section><div class='container'>{format_text(priv_txt)}</div></section>"), height=600, scrolling=True)
    # ADDED <section> tag here:
    elif preview_mode == "Terms": st.components.v1.html(build_page("Terms", f"{gen_inner_header('Terms')}<section><div class='container'>{format_text(term_txt)}</div></section>"), height=600, scrolling=True)
    elif preview_mode == "Blog Index": st.components.v1.html(build_page("Blog", gen_blog_index_html()), height=600, scrolling=True)
    elif preview_mode == "Blog Post (Demo)": st.components.v1.html(build_page("Article", gen_blog_post_html()), height=600, scrolling=True)
    elif preview_mode == "Product Detail (Demo)":
        st.info("ℹ️ Demo Mode Active: Showing the first available product from your CSV.")
        st.components.v1.html(build_page("Product", gen_product_page_content(is_demo=True)), height=600, scrolling=True)
    elif preview_mode == "Booking Page":
        st.components.v1.html(build_page("Book Now", gen_booking_content()), height=600, scrolling=True)

with c2:
    st.success("2050 Architecture Compiled.")
    
    # Generate Zip in Memory
    z_b = io.BytesIO()
    with zipfile.ZipFile(z_b, "a", zipfile.ZIP_DEFLATED, False) as zf:
        zf.writestr("index.html", build_page("Home", home_content))
        zf.writestr("about.html", build_page("About", f"{gen_inner_header('About')}<section><div class='container'>{format_text(about_long)}</div></section>"))
        zf.writestr("contact.html", build_page("Contact", contact_content))
         zf.writestr("privacy.html", build_page("Privacy", f"{gen_inner_header('Privacy')}<section><div class='container'>{format_text(priv_txt)}</div></section>"))
        zf.writestr("terms.html", build_page("Terms", f"{gen_inner_header('Terms')}<section><div class='container'>{format_text(term_txt)}</div></section>"))
        if show_booking: zf.writestr("booking.html", build_page("Book Now", gen_booking_content()))
        if show_inventory: zf.writestr("product.html", build_page("Product Details", gen_product_page_content(is_demo=False)))
        if show_blog: 
            zf.writestr("blog.html", build_page("Blog", gen_blog_index_html()))
            zf.writestr("post.html", build_page("Article", gen_blog_post_html()))
        
        zf.writestr("manifest.json", gen_pwa_manifest())
        zf.writestr("service-worker.js", gen_sw())
        zf.writestr("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {prod_url}/sitemap.xml")
        zf.writestr("sitemap.xml", f"""<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>{prod_url}/</loc></url></urlset>""")

    # IPFS OR ZIP DOWNLOAD
    if pinata_jwt:
        if st.button("🌌 PUSH TO Web3 (IPFS)", type="primary"):
            with st.spinner("Encrypting and uploading to IPFS Blockchain..."):
                try:
                    url = "https://api.pinata.cloud/pinning/pinFileToIPFS"
                    headers = {"Authorization": f"Bearer {pinata_jwt}"}
                    files = {"file": ("titan_site.zip", z_b.getvalue())}
                    res = requests.post(url, headers=headers, files=files)
                    if res.status_code == 200:
                        cid = res.json()['IpfsHash']
                        st.success(f"Deployed! Live forever on IPFS.")
                        st.markdown(f"**Gateway Link:** [ipfs.io/ipfs/{cid}](https://ipfs.io/ipfs/{cid})")
                    else:
                        st.error(f"IPFS Error: {res.text}")
                except Exception as e:
                    st.error(f"Upload failed: {e}")
    else:
        st.download_button("📥 DOWNLOAD 2050 PACKAGE", z_b.getvalue(), f"{biz_name.lower().replace(' ','_')}_apex.zip", "application/zip", type="primary")
