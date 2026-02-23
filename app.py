import streamlit as st
import zipfile
import io
import json
import re
import requests

# ==========================================
# 🏛️ TITAN CORE: CONFIGURATION & STATE
# ==========================================

st.set_page_config(
    page_title="Titan Engine | Infinity Edition",
    layout="wide",
    page_icon="⚡",
    initial_sidebar_state="expanded"
)

# Initialize Session State with defaults
if 'config' not in st.session_state:
    st.session_state.config = {
        "biz_name": "Stop Web Rent",
        "tagline": "The Future is Static.",
        "primary_col": "#0f172a",
        "accent_col": "#ef4444",
        "font_head": "Space Grotesk",
        "font_body": "Inter",
        "wa_num": "966572562151",
        "data_store": "",
        "data_blog": "",
        "google_analytics": ""
    }

# ==========================================
# 🎨 TITAN CORE: CSS & JS GENERATORS
# ==========================================

class AssetGenerator:
    """Generates the liquid logic (CSS/JS) for the generated site."""
    
    @staticmethod
    def get_css(c):
        return f"""
        :root {{
            --p: {c['primary_col']}; --s: {c['accent_col']};
            --bg: #ffffff; --txt: #1e293b; --surface: #f8fafc;
            --font-h: '{c['font_head']}', sans-serif;
            --font-b: '{c['font_body']}', sans-serif;
            --shadow: 0 10px 30px -10px rgba(0,0,0,0.1);
        }}
        @media (prefers-color-scheme: dark) {{
            :root {{ --bg: #0f172a; --txt: #f1f5f9; --surface: #1e293b; }}
        }}
        * {{ box-sizing: border-box; }}
        body {{ margin: 0; font-family: var(--font-b); background: var(--bg); color: var(--txt); line-height: 1.6; overflow-x: hidden; }}
        h1, h2, h3, h4 {{ font-family: var(--font-h); color: var(--p); line-height: 1.1; margin-bottom: 1rem; }}
        .dark-mode h1, .dark-mode h2 {{ color: #fff; }}
        
        /* LAYOUT */
        .container {{ max-width: 1280px; margin: 0 auto; padding: 0 20px; }}
        section {{ padding: 4rem 0; }}
        .grid-3 {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem; }}
        
        /* COMPONENTS */
        .btn {{ 
            display: inline-flex; align-items: center; justify-content: center;
            padding: 1rem 2rem; border-radius: 8px; font-weight: 700; 
            text-decoration: none; transition: 0.3s; cursor: pointer; border: none;
        }}
        .btn-primary {{ background: var(--p); color: white; }}
        .btn-accent {{ background: var(--s); color: white; }}
        .btn:hover {{ transform: translateY(-3px); box-shadow: var(--shadow); filter: brightness(1.1); }}
        
        .card {{ 
            background: var(--surface); padding: 2rem; border-radius: 12px; 
            border: 1px solid rgba(128,128,128,0.1); transition: 0.3s; 
            display: flex; flex-direction: column;
        }}
        .card:hover {{ transform: translateY(-5px); box-shadow: var(--shadow); border-color: var(--s); }}
        
        .prod-img {{ width: 100%; height: 250px; object-fit: cover; border-radius: 8px; margin-bottom: 1rem; background: #ddd; }}
        
        /* NAVIGATION */
        nav {{ position: sticky; top: 0; z-index: 999; background: rgba(255,255,255,0.9); backdrop-filter: blur(10px); border-bottom: 1px solid rgba(0,0,0,0.05); }}
        .dark-mode nav {{ background: rgba(15,23,42,0.9); }}
        .nav-inner {{ display: flex; justify-content: space-between; align-items: center; height: 70px; }}
        .nav-links a {{ margin-left: 2rem; text-decoration: none; color: var(--txt); font-weight: 600; opacity: 0.8; transition: 0.2s; }}
        .nav-links a:hover {{ color: var(--s); opacity: 1; }}
        
        /* UTILS */
        .reveal {{ opacity: 0; transform: translateY(30px); transition: 0.8s ease; }}
        .reveal.active {{ opacity: 1; transform: translateY(0); }}
        
        /* MOBILE */
        @media (max-width: 768px) {{
            .nav-links {{ display: none; }} 
            h1 {{ font-size: 2.5rem; }}
        }}
        """

    @staticmethod
    def get_js(c):
        return f"""
        const CONFIG = {{
            store: "{c['data_store']}",
            blog: "{c['data_blog']}",
            wa: "{c['wa_num']}"
        }};
        
        // --- CSV PARSER (The Engine) ---
        function parseCSV(str) {{
            const arr = [];
            let quote = false;  // 'true' means we're inside a quoted field
            for (let row = 0, col = 0, c = 0; c < str.length; c++) {{
                let cc = str[c], nc = str[c+1];
                arr[row] = arr[row] || []; arr[row][col] = arr[row][col] || '';
                if (cc == '"' && quote && nc == '"') {{ arr[row][col] += cc; ++c; continue; }}
                if (cc == '"') {{ quote = !quote; continue; }}
                if (cc == ',' && !quote) {{ ++col; continue; }}
                if (cc == '\\r' && nc == '\\n' && !quote) {{ ++row; col = 0; ++c; continue; }}
                if (cc == '\\n' && !quote) {{ ++row; col = 0; continue; }}
                if (cc == '\\r' && !quote) {{ ++row; col = 0; continue; }}
                arr[row][col] += cc;
            }}
            return arr;
        }}

        // --- STORE LOGIC ---
        async function loadStore() {{
            const el = document.getElementById('store-grid');
            if(!el || !CONFIG.store) return;
            try {{
                const res = await fetch(CONFIG.store);
                const txt = await res.text();
                const rows = parseCSV(txt).slice(1); // Skip header
                el.innerHTML = rows.map(r => {{
                    if(r.length < 3) return '';
                    let imgs = r[3] ? r[3].split('|') : ['https://via.placeholder.com/400'];
                    return `
                    <div class="card reveal">
                        <img src="${{imgs[0]}}" class="prod-img" loading="lazy">
                        <h3>${{r[0]}}</h3>
                        <div style="color:var(--s); font-weight:bold; margin-bottom:0.5rem">${{r[1]}}</div>
                        <p>${{r[2].substring(0,80)}}...</p>
                        <div style="margin-top:auto; display:flex; gap:10px;">
                            <button onclick="addToCart('${{r[0]}}', '${{r[1]}}')" class="btn btn-primary" style="flex:1">Add</button>
                            <a href="product.html?id=${{encodeURIComponent(r[0])}}" class="btn btn-accent">View</a>
                        </div>
                    </div>`;
                }}).join('');
                triggerAnim();
            }} catch(e) {{ el.innerHTML = "Error loading store."; console.error(e); }}
        }}

        // --- BLOG LOGIC ---
        async function loadBlog() {{
            const el = document.getElementById('blog-grid');
            if(!el || !CONFIG.blog) return;
            try {{
                const res = await fetch(CONFIG.blog);
                const txt = await res.text();
                const rows = parseCSV(txt).slice(1);
                el.innerHTML = rows.map(r => {{
                    if(r.length < 4) return '';
                    return `
                    <div class="card reveal">
                        <img src="${{r[5] || 'https://via.placeholder.com/800x400'}}" class="prod-img" style="height:200px">
                        <span style="background:var(--s); color:white; padding:2px 10px; border-radius:20px; width:fit-content; font-size:0.8rem">${{r[3]}}</span>
                        <h3 style="margin-top:10px">${{r[1]}}</h3>
                        <p>${{r[4]}}</p>
                        <a href="post.html?id=${{r[0]}}" class="btn btn-primary" style="margin-top:auto">Read Article</a>
                    </div>`;
                }}).join('');
                triggerAnim();
            }} catch(e) {{ console.error(e); }}
        }}

        // --- CART LOGIC ---
        let cart = JSON.parse(localStorage.getItem('titan_cart')) || [];
        function addToCart(n, p) {{ 
            cart.push({{name:n, price:p}}); 
            localStorage.setItem('titan_cart', JSON.stringify(cart));
            updateCartUI();
            alert(n + " added!");
        }}
        function updateCartUI() {{
            const count = document.getElementById('cart-count');
            if(count) count.innerText = cart.length;
        }}
        function checkout() {{
            let msg = "Order Inquiry:%0A";
            cart.forEach(i => msg += `- ${{i.name}} (${{i.price}})%0A`);
            window.open(`https://wa.me/${{CONFIG.wa}}?text=${{msg}}`, '_blank');
            cart = []; localStorage.setItem('titan_cart', '[]'); updateCartUI();
        }}

        // --- ANIMATIONS ---
        function triggerAnim() {{
            const observer = new IntersectionObserver((entries) => {{
                entries.forEach(entry => {{
                    if (entry.isIntersecting) entry.target.classList.add('active');
                }});
            }});
            document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
        }}
        
        window.addEventListener('load', () => {{
            loadStore();
            loadBlog();
            updateCartUI();
            triggerAnim();
        }});
        """

# ==========================================
# 🧱 TITAN CORE: PAGE BUILDER
# ==========================================

class PageBuilder:
    def __init__(self, config):
        self.c = config
        self.css = AssetGenerator.get_css(config)
        self.js = AssetGenerator.get_js(config)

    def _nav(self):
        blog_link = '<a href="blog.html">Blog</a>' if self.c['data_blog'] else ''
        store_link = '<a href="index.html#store">Store</a>' if self.c['data_store'] else ''
        return f"""
        <nav><div class="container nav-inner">
            <a href="index.html" style="font-size:1.5rem; font-weight:900; text-decoration:none; color:var(--p)">{self.c['biz_name']}</a>
            <div class="nav-links">
                <a href="index.html">Home</a>
                {store_link}
                {blog_link}
                <a href="contact.html">Contact</a>
                <a href="#" onclick="document.getElementById('cart-modal').style.display='flex'">Cart (<span id="cart-count">0</span>)</a>
            </div>
        </div></nav>
        """

    def _footer(self):
        return f"""
        <footer style="background:var(--p); color:white; padding:3rem 0; margin-top:auto">
            <div class="container" style="text-align:center">
                <h3>{self.c['biz_name']}</h3>
                <p>Powered by Titan Engine v2050</p>
                <div style="margin-top:1rem; opacity:0.7">
                    <a href="privacy.html" style="color:white; margin:0 10px">Privacy</a>
                    <a href="terms.html" style="color:white; margin:0 10px">Terms</a>
                </div>
            </div>
        </footer>
        """

    def _cart_modal(self):
        return """
        <div id="cart-modal" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.5); z-index:2000; align-items:center; justify-content:center;">
            <div style="background:white; padding:2rem; border-radius:12px; width:90%; max-width:500px; color:#333">
                <h2>Your Cart</h2>
                <p>Ready to checkout?</p>
                <div style="margin-top:2rem; display:flex; gap:10px">
                    <button onclick="checkout()" class="btn btn-accent" style="flex:1">Checkout WhatsApp</button>
                    <button onclick="document.getElementById('cart-modal').style.display='none'" class="btn" style="border:1px solid #ccc">Close</button>
                </div>
            </div>
        </div>
        """

    def render_page(self, title, content, extra_head=""):
        return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{title} | {self.c['biz_name']}</title>
            <link href="https://fonts.googleapis.com/css2?family={self.c['font_head'].replace(' ','+')}:wght@700;900&family={self.c['font_body'].replace(' ','+')}:wght@300;400;600&display=swap" rel="stylesheet">
            {extra_head}
            <style>{self.css}</style>
        </head>
        <body style="min-height:100vh; display:flex; flex-direction:column;">
            {self._nav()}
            {content}
            {self._footer()}
            {self._cart_modal()}
            <script>{self.js}</script>
        </body>
        </html>
        """

# ==========================================
# 🖥️ STREAMLIT UI (CONTROL PANEL)
# ==========================================

st.title("🏗️ Titan Engine: Infinity Architect")
st.markdown("Generates **Multi-Page**, **Dynamic-Data**, **Static-Hosted** websites ready for 2050.")

with st.sidebar:
    st.header("Global Settings")
    st.session_state.config['biz_name'] = st.text_input("Business Name", st.session_state.config['biz_name'])
    st.session_state.config['wa_num'] = st.text_input("WhatsApp Number", st.session_state.config['wa_num'])
    
    st.header("🎨 Visual DNA")
    c1, c2 = st.columns(2)
    st.session_state.config['primary_col'] = c1.color_picker("Primary", st.session_state.config['primary_col'])
    st.session_state.config['accent_col'] = c2.color_picker("Accent", st.session_state.config['accent_col'])
    
    st.header("🔌 Dynamic Feeds")
    st.session_state.config['data_store'] = st.text_input("Store CSV URL")
    st.session_state.config['data_blog'] = st.text_input("Blog CSV URL")

# --- MAIN EDITOR ---
tabs = st.tabs(["Hero & Home", "About & Features", "Booking & Contact", "Review & Export"])

with tabs[0]:
    st.subheader("Hero Section")
    h_title = st.text_input("Hero Title", "Stop Paying Rent.")
    h_sub = st.text_area("Hero Subtext", "The future is static. Own your code.")
    h_img = st.text_input("Hero Image URL", "https://images.unsplash.com/photo-1600607686527-6fb886090705?q=80&w=1600")
    
    home_content = f"""
    <section style="background:linear-gradient(rgba(0,0,0,0.5),rgba(0,0,0,0.5)), url('{h_img}'); background-size:cover; height:80vh; display:flex; align-items:center; color:white; text-align:center;">
        <div class="container reveal">
            <h1 style="font-size:clamp(3rem, 5vw, 5rem); color:white; margin-bottom:1rem">{h_title}</h1>
            <p style="font-size:1.5rem; margin-bottom:2rem; opacity:0.9">{h_sub}</p>
            <a href="#store" class="btn btn-accent">Explore Now</a>
        </div>
    </section>
    
    <section id="store">
        <div class="container">
            <h2 style="text-align:center; font-size:2.5rem; margin-bottom:3rem">Latest Drops</h2>
            <div id="store-grid" class="grid-3">
                <div style="text-align:center; grid-column:1/-1; padding:3rem">
                    { "Loading Dynamic Data from Edge..." if st.session_state.config['data_store'] else "Connect a Google Sheet to see products." }
                </div>
            </div>
        </div>
    </section>
    """

with tabs[1]:
    st.subheader("About Content")
    about_txt = st.text_area("About Us Text", "We are building the future of web architecture.")
    about_img = st.text_input("About Image", "https://images.unsplash.com/photo-1522071820081-009f0129c71c?q=80&w=1600")
    
    about_content = f"""
    <section>
        <div class="container grid-3" style="grid-template-columns: 1fr 1fr; align-items:center">
            <div class="reveal">
                <h1>About Us</h1>
                <p style="font-size:1.1rem">{about_txt}</p>
            </div>
            <img src="{about_img}" class="reveal" style="width:100%; border-radius:12px;">
        </div>
    </section>
    """
    
    st.subheader("Features")
    feat_html = ""
    for i in range(3):
        c1, c2 = st.columns(2)
        ft = c1.text_input(f"Feature {i+1} Title", f"Feature {i+1}")
        fd = c2.text_input(f"Feature {i+1} Desc", "Description here")
        feat_html += f'<div class="card reveal"><h3>{ft}</h3><p>{fd}</p></div>'
    
    home_content += f'<section style="background:var(--surface)"><div class="container"><h2 style="text-align:center">Why Us</h2><div class="grid-3">{feat_html}</div></div></section>'

with tabs[2]:
    st.subheader("Booking Embed")
    booking_code = st.text_area("Calendly/Booking Embed Code", "<!-- Paste Calendly -->")
    
    contact_content = f"""
    <section>
        <div class="container" style="text-align:center; max-width:800px">
            <h1>Contact Us</h1>
            <div class="card reveal" style="text-align:left; margin-top:2rem">
                <h3>Get in Touch</h3>
                <p>Email: hello@{st.session_state.config['biz_name'].replace(' ','').lower()}.com</p>
                <p>WhatsApp: {st.session_state.config['wa_num']}</p>
                <a href="https://wa.me/{st.session_state.config['wa_num']}" class="btn btn-accent" style="margin-top:1rem; width:100%; text-align:center">Chat Now</a>
            </div>
            <div style="margin-top:4rem">
                <h2>Book a Call</h2>
                {booking_code}
            </div>
        </div>
    </section>
    """

with tabs[3]:
    st.success("Configuration Complete. Ready to compile.")
    
    if st.button("🚀 BUILD & DOWNLOAD WEBSITE", type="primary"):
        # Instantiate Builder
        builder = PageBuilder(st.session_state.config)
        
        # 1. Build Pages
        pg_home = builder.render_page("Home", home_content)
        pg_contact = builder.render_page("Contact", contact_content)
        pg_about = builder.render_page("About", about_content)
        pg_terms = builder.render_page("Terms", "<div class='container'><br><h1>Terms</h1><p>Standard terms apply.</p></div>")
        pg_privacy = builder.render_page("Privacy", "<div class='container'><br><h1>Privacy</h1><p>We value your privacy.</p></div>")
        
        # 2. Build Blog Index & Dynamic Post Page
        pg_blog = builder.render_page("Blog", """
            <section><div class="container">
                <h1 style="text-align:center">Our Blog</h1>
                <div id="blog-grid" class="grid-3" style="margin-top:3rem">Loading...</div>
            </div></section>
        """)
        
        # DYNAMIC PRODUCT DETAIL PAGE (JS handles the hydration)
        pg_product = builder.render_page("Product", """
            <section><div class="container" id="prod-container">
                <a href="index.html#store" class="btn">&larr; Back</a>
                <div class="grid-3" style="margin-top:2rem; grid-template-columns:1fr 1fr;">
                    <img id="p-img" style="width:100%; border-radius:12px;">
                    <div>
                        <h1 id="p-title">Loading...</h1>
                        <h2 id="p-price" style="color:var(--s)"></h2>
                        <p id="p-desc"></p>
                        <button id="p-btn" class="btn btn-primary">Add to Cart</button>
                    </div>
                </div>
            </div></section>
            <script>
            async function loadP() {
                const params = new URLSearchParams(window.location.search);
                const id = params.get('id');
                const res = await fetch(CONFIG.store);
                const txt = await res.text();
                const rows = parseCSV(txt);
                const p = rows.find(r => r[0] == id);
                if(p) {
                    let imgs = p[3] ? p[3].split('|') : [''];
                    document.getElementById('p-img').src = imgs[0];
                    document.getElementById('p-title').innerText = p[0];
                    document.getElementById('p-price').innerText = p[1];
                    document.getElementById('p-desc').innerText = p[2];
                    document.getElementById('p-btn').onclick = () => addToCart(p[0], p[1]);
                }
            }
            loadP();
            </script>
        """)

        # DYNAMIC BLOG POST PAGE
        pg_post = builder.render_page("Article", """
            <section><div class="container" style="max-width:800px">
                <a href="blog.html" class="btn">&larr; Back</a>
                <img id="b-img" style="width:100%; height:400px; object-fit:cover; border-radius:12px; margin-top:2rem">
                <h1 id="b-title" style="font-size:3rem; line-height:1.1; margin-top:1rem">Loading...</h1>
                <div id="b-body" style="font-size:1.2rem; line-height:1.8; color:#555"></div>
            </div></section>
            <script>
            async function loadB() {
                const params = new URLSearchParams(window.location.search);
                const id = params.get('id');
                const res = await fetch(CONFIG.blog);
                const txt = await res.text();
                const rows = parseCSV(txt);
                const p = rows.find(r => r[0] == id);
                if(p) {
                    document.getElementById('b-img').src = p[5];
                    document.getElementById('b-title').innerText = p[1];
                    document.getElementById('b-body').innerHTML = p[6] ? p[6].replace(/\\n/g, '<br>') : '';
                }
            }
            loadB();
            </script>
        """)

        # 3. Zip It
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zf:
            zf.writestr("index.html", pg_home)
            zf.writestr("contact.html", pg_contact)
            zf.writestr("about.html", pg_about)
            zf.writestr("blog.html", pg_blog)
            zf.writestr("product.html", pg_product)
            zf.writestr("post.html", pg_post)
            zf.writestr("terms.html", pg_terms)
            zf.writestr("privacy.html", pg_privacy)
            
            # PWA Manifest
            zf.writestr("manifest.json", json.dumps({
                "name": st.session_state.config['biz_name'],
                "start_url": "index.html",
                "display": "standalone",
                "theme_color": st.session_state.config['primary_col']
            }))

        st.download_button(
            label="📥 DOWNLOAD 2050 SITE PACKAGE",
            data=zip_buffer.getvalue(),
            file_name="titan_infinity_build.zip",
            mime="application/zip",
            type="primary"
        )
        
        st.subheader("Preview")
        st.components.v1.html(pg_home, height=600, scrolling=True)
