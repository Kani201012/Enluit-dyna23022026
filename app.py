import streamlit as st
import pandas as pd
import requests
import json
import zipfile
import io

# --- 0. ENGINE CONFIGURATION ---
ST_PAGE_TITLE = "Titan Architect | 2050 Edition"
ST_ICON = "🧬"

st.set_page_config(layout="wide", page_title=ST_PAGE_TITLE, page_icon=ST_ICON)

# --- 1. STATE MANAGEMENT (MEMORY) ---
if 'site_data' not in st.session_state:
    st.session_state.site_data = {
        "brand": "StopWebRent",
        "tagline": "The Future is Static.",
        "colors": {"primary": "#2563eb", "secondary": "#ec4899", "bg": "#0f172a", "text": "#f8fafc"},
        "hero": {"title": "Own Your Digital Empire", "sub": "Zero monthly fees. Infinite scalability.", "img": "https://images.unsplash.com/photo-1620641788421-7f1a91b80e84?q=80&w=1600"},
        "features": [
            {"icon": "⚡", "title": "0.1s Load Time", "desc": "Edge-computed architecture."},
            {"icon": "🛡️", "title": "Zero-DB Security", "desc": "No database to hack."},
            {"icon": "💸", "title": "One-Time Payment", "desc": "Stop renting your existence."}
        ],
        "data_sources": {
            "store_csv": "", 
            "blog_csv": ""
        },
        "contact": {"phone": "", "email": "hello@stopwebrent.com", "wa": ""}
    }

# --- 2. THE GENERATOR ENGINE (CORE LOGIC) ---
class TitanEngine:
    def __init__(self, data):
        self.d = data

    def _get_tailwind_config(self):
        # Inject dynamic colors into Tailwind
        return f"""
        <script src="https://cdn.tailwindcss.com"></script>
        <script>
            tailwind.config = {{
                theme: {{
                    extend: {{
                        colors: {{
                            brand: '{self.d['colors']['primary']}',
                            accent: '{self.d['colors']['secondary']}',
                            dark: '{self.d['colors']['bg']}',
                            light: '{self.d['colors']['text']}'
                        }},
                        fontFamily: {{
                            sans: ['Inter', 'sans-serif'],
                        }}
                    }}
                }}
            }}
        </script>
        <style>
            body {{ background-color: {self.d['colors']['bg']}; color: {self.d['colors']['text']}; }}
            .glass {{ background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.1); }}
            .gradient-text {{ background: linear-gradient(to right, {self.d['colors']['primary']}, {self.d['colors']['secondary']}); -webkit-background-clip: text; color: transparent; }}
        </style>
        """

    def _get_alpine_logic(self):
        # The Brain of the 2050 Site (Client-Side Logic)
        store_url = self.d['data_sources']['store_csv']
        return f"""
        <script src="//unpkg.com/alpinejs" defer></script>
        <script>
            function app() {{
                return {{
                    view: 'home',
                    cart: [],
                    products: [],
                    loading: false,
                    
                    async init() {{
                        this.cart = JSON.parse(localStorage.getItem('titan_cart')) || [];
                        const csvUrl = '{store_url}';
                        if(csvUrl) {{
                            this.loading = true;
                            try {{
                                const res = await fetch(csvUrl);
                                const text = await res.text();
                                this.products = this.parseCSV(text);
                            }} catch(e) {{ console.log(e); }}
                            this.loading = false;
                        }}
                    }},
                    
                    parseCSV(str) {{
                        const rows = str.split('\\n').slice(1);
                        return rows.map(row => {{
                            const c = row.split(','); // Simple parser
                            if(c.length < 3) return null;
                            return {{ name: c[0], price: c[1], desc: c[2], img: c[3] || 'https://via.placeholder.com/300' }};
                        }}).filter(Boolean);
                    }},

                    addToCart(item) {{
                        this.cart.push(item);
                        localStorage.setItem('titan_cart', JSON.stringify(this.cart));
                        alert('Added to Cart');
                    }},
                    
                    checkout() {{
                        let msg = "Order Inquiry:\\n";
                        this.cart.forEach(i => msg += i.name + " (" + i.price + ")\\n");
                        window.open('https://wa.me/{self.d['contact']['wa']}?text=' + encodeURIComponent(msg));
                    }}
                }}
            }}
        </script>
        """

    def generate_html(self):
        # SINGLE FILE COMPONENT ASSEMBLY
        return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{self.d['brand']}</title>
            <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700;900&display=swap" rel="stylesheet">
            {self._get_tailwind_config()}
            {self._get_alpine_logic()}
        </head>
        <body x-data="app()" class="antialiased selection:bg-accent selection:text-white">
            
            <!-- NAVBAR -->
            <nav class="fixed w-full z-50 glass">
                <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div class="flex items-center justify-between h-16">
                        <div class="text-2xl font-black tracking-tighter cursor-pointer" @click="view = 'home'">
                            {self.d['brand']}
                        </div>
                        <div class="hidden md:block">
                            <div class="ml-10 flex items-baseline space-x-4">
                                <button @click="view = 'home'" class="hover:text-brand px-3 py-2 rounded-md text-sm font-medium">Home</button>
                                <button @click="view = 'store'" class="hover:text-brand px-3 py-2 rounded-md text-sm font-medium">Store</button>
                                <button @click="view = 'cart'" class="bg-brand hover:bg-opacity-80 px-4 py-2 rounded-full text-white font-bold transition">
                                    Cart (<span x-text="cart.length"></span>)
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </nav>

            <!-- VIEW: HOME -->
            <div x-show="view === 'home'" x-transition.opacity class="pt-16">
                <!-- HERO -->
                <div class="relative overflow-hidden">
                    <div class="max-w-7xl mx-auto">
                        <div class="relative z-10 pb-8 sm:pb-16 md:pb-20 lg:max-w-2xl lg:w-full lg:pb-28 xl:pb-32 pt-20 px-4">
                            <h1 class="text-4xl tracking-tight font-extrabold sm:text-5xl md:text-6xl">
                                <span class="block">{self.d['hero']['title']}</span>
                                <span class="block gradient-text">{self.d['brand']}</span>
                            </h1>
                            <p class="mt-3 text-base text-gray-400 sm:mt-5 sm:text-lg sm:max-w-xl sm:mx-auto md:mt-5 md:text-xl lg:mx-0">
                                {self.d['hero']['sub']}
                            </p>
                            <div class="mt-5 sm:mt-8 sm:flex sm:justify-center lg:justify-start">
                                <div class="rounded-md shadow">
                                    <button @click="view = 'store'" class="w-full flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-white bg-brand hover:bg-accent transition md:py-4 md:text-lg">
                                        Launch Store
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="lg:absolute lg:inset-y-0 lg:right-0 lg:w-1/2">
                        <img class="h-56 w-full object-cover sm:h-72 md:h-96 lg:w-full lg:h-full opacity-80" src="{self.d['hero']['img']}" alt="">
                    </div>
                </div>

                <!-- FEATURES -->
                <div class="py-12 glass mt-10">
                    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                        <div class="grid grid-cols-1 gap-8 sm:grid-cols-3">
                            {''.join([f'''
                            <div class="pt-6">
                                <div class="flow-root glass rounded-lg px-6 pb-8">
                                    <div class="-mt-6">
                                        <div class="inline-flex items-center justify-center p-3 bg-brand rounded-md shadow-lg text-3xl">
                                            {f['icon']}
                                        </div>
                                        <h3 class="mt-8 text-lg font-medium tracking-tight">{f['title']}</h3>
                                        <p class="mt-5 text-base text-gray-400">{f['desc']}</p>
                                    </div>
                                </div>
                            </div>
                            ''' for f in self.d['features']])}
                        </div>
                    </div>
                </div>
            </div>

            <!-- VIEW: STORE -->
            <div x-show="view === 'store'" x-transition.opacity class="pt-24 min-h-screen px-4">
                <div class="max-w-7xl mx-auto">
                    <h2 class="text-3xl font-extrabold mb-8 gradient-text">Live Inventory</h2>
                    
                    <div x-show="loading" class="text-center py-20 animate-pulse">
                        Connecting to Satellite Stream...
                    </div>

                    <div x-show="!loading && products.length === 0" class="text-center py-10 border border-dashed border-gray-700 rounded-lg">
                        <p>No inventory found. Check CSV Connection.</p>
                        <p class="text-sm text-gray-500 mt-2">Example: name,price,description,image_url</p>
                    </div>

                    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                        <template x-for="product in products">
                            <div class="glass rounded-xl overflow-hidden hover:border-brand transition duration-300">
                                <img :src="product.img" class="h-48 w-full object-cover">
                                <div class="p-6">
                                    <div class="flex justify-between items-baseline">
                                        <h3 class="text-xl font-bold" x-text="product.name"></h3>
                                        <span class="text-brand font-mono text-lg" x-text="product.price"></span>
                                    </div>
                                    <p class="mt-2 text-gray-400 text-sm h-12 overflow-hidden" x-text="product.desc"></p>
                                    <button @click="addToCart(product)" class="mt-4 w-full bg-white bg-opacity-10 hover:bg-brand text-white font-bold py-2 rounded transition">
                                        Add to Cart
                                    </button>
                                </div>
                            </div>
                        </template>
                    </div>
                </div>
            </div>

            <!-- VIEW: CART -->
            <div x-show="view === 'cart'" x-transition.opacity class="pt-24 min-h-screen px-4">
                <div class="max-w-3xl mx-auto glass rounded-xl p-8">
                    <h2 class="text-3xl font-bold mb-6">Your Cart</h2>
                    <template x-for="(item, index) in cart">
                        <div class="flex justify-between items-center border-b border-gray-700 py-4">
                            <div>
                                <h4 class="font-bold" x-text="item.name"></h4>
                                <p class="text-sm text-gray-400" x-text="item.price"></p>
                            </div>
                            <button @click="cart.splice(index, 1); localStorage.setItem('titan_cart', JSON.stringify(cart))" class="text-red-500 hover:text-red-400">Remove</button>
                        </div>
                    </template>
                    <div class="mt-8 pt-4 border-t border-gray-600">
                        <button @click="checkout()" class="w-full bg-green-600 hover:bg-green-500 text-white font-bold py-4 rounded-lg shadow-lg transform hover:-translate-y-1 transition">
                            Checkout via WhatsApp
                        </button>
                    </div>
                </div>
            </div>

        </body>
        </html>
        """

# --- 3. UI DASHBOARD ---
with st.sidebar:
    st.title("Titan 2050")
    st.markdown("---")
    
    with st.expander("🎨 Global Design", expanded=True):
        st.session_state.site_data['brand'] = st.text_input("Brand Name", st.session_state.site_data['brand'])
        c1, c2 = st.columns(2)
        st.session_state.site_data['colors']['primary'] = c1.color_picker("Brand Color", st.session_state.site_data['colors']['primary'])
        st.session_state.site_data['colors']['secondary'] = c2.color_picker("Accent Color", st.session_state.site_data['colors']['secondary'])
        st.session_state.site_data['colors']['bg'] = c1.color_picker("Background", st.session_state.site_data['colors']['bg'])
        st.session_state.site_data['colors']['text'] = c2.color_picker("Text Color", st.session_state.site_data['colors']['text'])

    with st.expander("🔌 Dynamic Data"):
        st.info("Paste your published Google Sheet CSV link here.")
        st.session_state.site_data['data_sources']['store_csv'] = st.text_input("Store CSV URL", st.session_state.site_data['data_sources']['store_csv'])
        st.session_state.site_data['contact']['wa'] = st.text_input("WhatsApp Number", st.session_state.site_data['contact']['wa'])

# --- 4. MAIN WORKSPACE ---
st.title("🚀 StopWebRent: Construct Mode")

tabs = st.tabs(["Hero Section", "Features", "Preview & Export"])

with tabs[0]:
    c1, c2 = st.columns([2, 1])
    with c1:
        st.session_state.site_data['hero']['title'] = st.text_input("Hero Title", st.session_state.site_data['hero']['title'])
        st.session_state.site_data['hero']['sub'] = st.text_area("Hero Subtitle", st.session_state.site_data['hero']['sub'])
    with c2:
        st.session_state.site_data['hero']['img'] = st.text_input("Background Image", st.session_state.site_data['hero']['img'])
        st.caption("Use Unsplash URL for best results")

with tabs[1]:
    st.markdown("### The Three Pillars")
    for i in range(3):
        c1, c2, c3 = st.columns([1, 2, 3])
        st.session_state.site_data['features'][i]['icon'] = c1.text_input(f"Icon {i+1}", st.session_state.site_data['features'][i]['icon'])
        st.session_state.site_data['features'][i]['title'] = c2.text_input(f"Title {i+1}", st.session_state.site_data['features'][i]['title'])
        st.session_state.site_data['features'][i]['desc'] = c3.text_input(f"Desc {i+1}", st.session_state.site_data['features'][i]['desc'])

with tabs[2]:
    # GENERATION LOGIC
    engine = TitanEngine(st.session_state.site_data)
    html_output = engine.generate_html()
    
    col_a, col_b = st.columns([3, 1])
    with col_a:
        st.subheader("Live Quantum Preview")
        st.components.v1.html(html_output, height=600, scrolling=True)
    
    with col_b:
        st.subheader("Deploy")
        st.success("System Optimized.")
        
        # Zip Logic
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zf:
            zf.writestr("index.html", html_output)
            zf.writestr("README.txt", "Titan 2050 Build.\nUpload index.html to Netlify/Vercel/GitHub Pages.")
        
        st.download_button(
            label="Download Application",
            data=zip_buffer.getvalue(),
            file_name="titan_2050_build.zip",
            mime="application/zip",
            type="primary"
        )
