import streamlit as st
import zipfile
import io
import json
import requests
import re
from jinja2 import Template

# --- 1. ARCHITECTURE DEFINITIONS ---

class TitanConfig:
    """Central Configuration for the Year 2050 Engine"""
    VERSION = "v50.0.1 (Singularity Edition)"
    DEFAULT_THEMES = {
        "Neo-Tokyo": {"bg": "#050505", "txt": "#00ff9d", "p": "#00ff9d", "s": "#ff0055", "font": "Share Tech Mono"},
        "Mars Colony": {"bg": "#2c1a1a", "txt": "#e8d5cc", "p": "#ff4d4d", "s": "#ff9f43", "font": "Orbitron"},
        "Clean Corporate": {"bg": "#ffffff", "txt": "#0f172a", "p": "#0f172a", "s": "#3b82f6", "font": "Inter"},
        "Lux": {"bg": "#000000", "txt": "#fdfdfd", "p": "#d4af37", "s": "#f1f1f1", "font": "Playfair Display"},
    }

class TitanAI:
    """The Artificial Intelligence Cortex"""
    def __init__(self, api_key):
        self.api_key = api_key
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"

    def generate_site_identity(self, niche):
        if not self.api_key: return None
        prompt = f"""
        Act as a futuristic web architect. For the business niche '{niche}', return a JSON object with:
        - hero_h (Catchy headline)
        - hero_sub (Subtext explaining value)
        - color_palette (A suggested hex code for primary color)
        - features (List of 3 distinct features with icon_name, title, description)
        """
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        data = {
            "messages": [{"role": "user", "content": prompt}],
            "model": "llama-3.1-8b-instant",
            "response_format": {"type": "json_object"}
        }
        try:
            resp = requests.post(self.api_url, headers=headers, json=data)
            return json.loads(resp.json()['choices'][0]['message']['content'])
        except:
            return None

class RenderEngine:
    """Jinja2 Powered HTML Generation System"""
    
    BASE_TEMPLATE = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{{ meta.title }}</title>
        <meta name="description" content="{{ meta.desc }}">
        <link href="https://fonts.googleapis.com/css2?family={{ style.font_url }}:wght@300;400;700;900&display=swap" rel="stylesheet">
        <style>
            :root {
                --p: {{ style.primary }}; --s: {{ style.secondary }};
                --bg: {{ style.bg }}; --txt: {{ style.text }};
                --font: '{{ style.font_name }}', sans-serif;
            }
            body { background: var(--bg); color: var(--txt); font-family: var(--font); margin: 0; line-height: 1.6; overflow-x: hidden; }
            .container { max-width: 1200px; margin: 0 auto; padding: 0 20px; }
            h1, h2, h3 { line-height: 1.1; font-weight: 900; }
            .btn { display: inline-block; padding: 1rem 2rem; background: var(--p); color: var(--bg); text-decoration: none; font-weight: bold; border-radius: 8px; transition: 0.3s; }
            .btn:hover { transform: translateY(-3px); filter: brightness(1.2); }
            
            /* Dynamic CSS Injection */
            {{ style.custom_css }}
            
            /* Section Animations */
            .reveal { opacity: 0; transform: translateY(30px); transition: 0.8s all ease; }
            .reveal.active { opacity: 1; transform: translateY(0); }
        </style>
    </head>
    <body>
        {{ content }}
        <script>
            {{ script }}
        </script>
    </body>
    </html>
    """

    @staticmethod
    def render(meta, style, components, script=""):
        # Combine all HTML components
        full_content = "\n".join(components)
        t = Template(RenderEngine.BASE_TEMPLATE)
        return t.render(meta=meta, style=style, content=full_content, script=script)

# --- 2. STREAMLIT UI SETUP ---

st.set_page_config(page_title="Titan Engine 2050", layout="wide", page_icon="⚡")

# Initialize Session State logic
if 'config' not in st.session_state:
    st.session_state['config'] = {
        "biz_name": "Stop Web Rent",
        "primary_color": "#0f172a",
        "secondary_color": "#ef4444",
        "font": "Inter",
        "hero_head": "Own Your Digital Empire.",
        "hero_sub": "No monthly fees. No database. Pure speed.",
        "theme": "Clean Corporate"
    }

# --- 3. SIDEBAR CONTROLS ---

with st.sidebar:
    st.title("⚡ Titan Engine")
    st.caption(f"{TitanConfig.VERSION}")
    
    with st.expander("🧠 AI Architect", expanded=True):
        api_key = st.text_input("Groq API Key", type="password")
        niche_input = st.text_input("Project Niche (e.g. Real Estate)")
        if st.button("Auto-Design Site") and api_key:
            ai = TitanAI(api_key)
            with st.spinner("Connecting to Neural Net..."):
                res = ai.generate_site_identity(niche_input)
                if res:
                    st.session_state['config']['hero_head'] = res.get('hero_h', "Welcome")
                    st.session_state['config']['hero_sub'] = res.get('hero_sub', "Best Service")
                    st.session_state['config']['primary_color'] = res.get('color_palette', "#000000")
                    st.success("Design System Updated")
                    st.rerun()

    with st.expander("🎨 Visual DNA"):
        theme_sel = st.selectbox("Preset Theme", list(TitanConfig.DEFAULT_THEMES.keys()))
        # Apply theme logic
        t_data = TitanConfig.DEFAULT_THEMES[theme_sel]
        
        c1, c2 = st.columns(2)
        p_col = c1.color_picker("Primary", st.session_state['config']['primary_color'])
        s_col = c2.color_picker("Accent", t_data['s'])
        bg_col = c1.color_picker("Background", t_data['bg'])
        txt_col = c2.color_picker("Text", t_data['txt'])
        
        font_sel = st.selectbox("Typography", ["Inter", "Roboto", "Playfair Display", "Space Grotesk", "Orbitron"])

# --- 4. MAIN EDITOR ---

st.title("🏗️ Construct Mode")

tabs = st.tabs(["Hero Section", "Features", "Data Grid", "Live Code"])

with tabs[0]:
    st.subheader("Hero Banner")
    h_head = st.text_input("Headline", st.session_state['config']['hero_head'])
    h_sub = st.text_area("Subtext", st.session_state['config']['hero_sub'])
    h_img = st.text_input("Background Image URL", "https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=1600")

with tabs[1]:
    st.subheader("Feature Matrix")
    feat_text = st.text_area("Features (Format: Icon | Title | Desc)", 
                             "bolt | Speed | 0.1s Load Time\nshield | Security | Unhackable Static Architecture\nwallet | Cost | $0 Monthly Fees")

with tabs[2]:
    st.subheader("Google Sheet Integration")
    sheet_url = st.text_input("Google Sheet CSV URL (Product/Blog Data)")

# --- 5. COMPILATION LOGIC ---

def build_hero_html(head, sub, img):
    return f"""
    <section style="background: linear-gradient(rgba(0,0,0,0.6),rgba(0,0,0,0.6)), url('{img}'); background-size: cover; min-height: 80vh; display: flex; align-items: center; justify-content: center; text-align: center; color: white;">
        <div class="container reveal active">
            <h1 style="font-size: clamp(2.5rem, 5vw, 5rem); margin-bottom: 1rem;">{head}</h1>
            <p style="font-size: clamp(1rem, 2vw, 1.5rem); max-width: 700px; margin: 0 auto 2rem auto;">{sub}</p>
            <a href="#contact" class="btn">Get Started</a>
        </div>
    </section>
    """

def build_features_html(raw_data):
    # Simple icon mapping for demo purposes
    icons = {"bolt": "⚡", "shield": "🛡️", "wallet": "💰"}
    
    html_cards = ""
    for line in raw_data.split('\n'):
        if "|" in line:
            parts = line.split("|")
            icon_char = icons.get(parts[0].strip(), "★")
            html_cards += f"""
            <div style="background: rgba(255,255,255,0.05); padding: 2rem; border: 1px solid rgba(128,128,128,0.2); border-radius: 12px;">
                <div style="font-size: 2rem; margin-bottom: 1rem;">{icon_char}</div>
                <h3>{parts[1]}</h3>
                <p style="opacity: 0.8;">{parts[2]}</p>
            </div>
            """
    return f"""
    <section style="padding: 5rem 0;">
        <div class="container">
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem;">
                {html_cards}
            </div>
        </div>
    </section>
    """

def build_js_engine(sheet_url):
    # The futuristic JS part: fetching data from sheets client-side
    if not sheet_url: return ""
    return f"""
    async function loadData() {{
        const res = await fetch('{sheet_url}');
        const text = await res.text();
        console.log("Titan Data Loaded:", text.length);
        // In 2050, we would hydrate web components here
    }}
    loadData();
    """

# --- 6. RENDER EXECUTION ---

# Assembly
comp_hero = build_hero_html(h_head, h_sub, h_img)
comp_feat = build_features_html(feat_text)
js_core = build_js_engine(sheet_url)

style_obj = {
    "primary": p_col, "secondary": s_col, "bg": bg_col, "text": txt_col,
    "font_name": font_sel, "font_url": font_sel.replace(" ", "+"),
    "custom_css": ""
}

meta_obj = {"title": st.session_state['config']['biz_name'], "desc": h_sub}

# Generate Final HTML
final_html = RenderEngine.render(meta_obj, style_obj, [comp_hero, comp_feat], js_core)

# --- 7. OUTPUT & DOWNLOAD ---

with tabs[3]:
    st.code(final_html, language="html")

st.divider()
c1, c2 = st.columns([3, 1])
with c1:
    st.subheader("👁️ Quantum Preview")
    st.components.v1.html(final_html, height=600, scrolling=True)

with c2:
    st.success("Build Complete")
    # Zip Generator
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zf:
        zf.writestr("index.html", final_html)
        zf.writestr("titan.json", json.dumps(st.session_state['config'])) # Save state configuration
        
    st.download_button(
        label="🚀 Launch Site (Download ZIP)",
        data=zip_buffer.getvalue(),
        file_name="titan_build.zip",
        mime="application/zip",
        type="primary"
    )
