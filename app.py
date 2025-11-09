import streamlit as st
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_bloch_multivector
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# Configure matplotlib for better dark mode support
# This will use a style that looks good in both light and dark modes
plt.rcParams['figure.facecolor'] = 'none'  # Transparent figure background
plt.rcParams['axes.facecolor'] = 'none'  # Transparent axes background
plt.rcParams['savefig.facecolor'] = 'none'  # Transparent saved figure background

# Page configurationhttps://github.com/ivanho-git/qubit-gates/edit/main/app.py
st.set_page_config(
    page_title="Quantum Gate Simulator",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Premium Custom CSS with Dark Mode Support
st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

    /* CSS Variables for Light Mode (Default) */
    :root {
        --bg-gradient-start: #667eea;
        --bg-gradient-end: #764ba2;
        --container-bg: rgba(255, 255, 255, 0.95);
        --text-primary: #000000;
        --text-secondary: #666;
        --text-tertiary: #333;
        --card-bg: white;
        --info-box-bg: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        --info-box-text: #000000;
        --tab-bg: white;
        --tab-list-bg: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        --metric-color: #667eea;
        --shadow-color: rgba(0, 0, 0, 0.3);
        --shadow-light: rgba(0, 0, 0, 0.1);
        --border-color: rgba(102, 126, 234, 0.1);
        --expander-bg: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        --input-bg: white;
    }

    /* Dark Mode Variables */
    @media (prefers-color-scheme: dark) {
        :root {
            --bg-gradient-start: #1a1a2e;
            --bg-gradient-end: #16213e;
            --container-bg: rgba(30, 30, 46, 0.95);
            --text-primary: #e0e0e0;
            --text-secondary: #b0b0b0;
            --text-tertiary: #d0d0d0;
            --card-bg: #2a2a3e;
            --info-box-bg: linear-gradient(135deg, #2a2a3e 0%, #363652 100%);
            --info-box-text: #e0e0e0;
            --tab-bg: #2a2a3e;
            --tab-list-bg: linear-gradient(135deg, #2a2a3e 0%, #363652 100%);
            --metric-color: #8b9dff;
            --shadow-color: rgba(0, 0, 0, 0.6);
            --shadow-light: rgba(0, 0, 0, 0.4);
            --border-color: rgba(139, 157, 255, 0.2);
            --expander-bg: linear-gradient(135deg, #2a2a3e 0%, #363652 100%);
            --input-bg: #2a2a3e;
        }
    }

    /* Global Styles */
    * {
        font-family: 'Poppins', sans-serif;
    }

    .main {
        background: linear-gradient(135deg, var(--bg-gradient-start) 0%, var(--bg-gradient-end) 100%);
        background-attachment: fixed;
    }

    .block-container {
        padding: 2rem 3rem;
        background: var(--container-bg);
        border-radius: 20px;
        box-shadow: 0 20px 60px var(--shadow-color);
        margin: 2rem auto;
        backdrop-filter: blur(10px);
    }
    
    /* Main Header */
    .main-header {
        font-size: 3.5rem;
        font-weight: 700;
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        animation: fadeIn 1s ease-in;
    }
    
    .subtitle {
        text-align: center;
        color: var(--text-secondary);
        font-size: 1.2rem;
        margin-bottom: 2rem;
        font-weight: 300;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: var(--tab-list-bg);
        padding: 1rem;
        border-radius: 15px;
        box-shadow: inset 0 2px 10px var(--shadow-light);
    }

    .stTabs [data-baseweb="tab"] {
        height: 60px;
        background: var(--tab-bg);
        border-radius: 10px;
        color: var(--text-tertiary);
        font-weight: 600;
        font-size: 1.1rem;
        padding: 0 2rem;
        border: 2px solid transparent;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        box-shadow: 0 5px 20px rgba(102, 126, 234, 0.5);
    }
    
    /* Buttons */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
        border-radius: 12px;
        padding: 0.8rem 1.5rem;
        border: none;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 25px rgba(102, 126, 234, 0.5);
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    /* Info Boxes */
    .info-box {
        background: var(--info-box-bg);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        color: var(--info-box-text);
        box-shadow: 0 5px 20px var(--shadow-light);
        border-left: 5px solid #667eea;
        transition: all 0.3s ease;
    }

    .info-box:hover {
        transform: translateX(5px);
        box-shadow: 0 8px 30px rgba(102, 126, 234, 0.2);
    }

    .info-box h3, .info-box h4, .info-box p, .info-box ul, .info-box li {
        color: var(--info-box-text) !important;
    }

    .info-box h3 {
        font-weight: 700;
        font-size: 1.4rem;
        margin-bottom: 0.8rem;
        color: #667eea !important;
    }

    .info-box h4 {
        font-weight: 600;
        font-size: 1.2rem;
        margin-bottom: 0.5rem;
        color: #764ba2 !important;
    }
    
    /* Card Styling */
    .card {
        background: var(--card-bg);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 10px 30px var(--shadow-light);
        margin: 1rem 0;
        border: 1px solid var(--border-color);
        transition: all 0.3s ease;
    }

    .card:hover {
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.2);
        transform: translateY(-5px);
    }
    
    /* Gradient Boxes */
    .gradient-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2.5rem;
        border-radius: 20px;
        color: white;
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.4);
        margin: 1.5rem 0;
        text-align: center;
    }
    
    .gradient-box h1, .gradient-box h2, .gradient-box h3, .gradient-box p {
        color: white !important;
    }
    
    /* Select boxes and inputs */
    .stSelectbox, .stRadio {
        background: var(--input-bg);
        border-radius: 10px;
        padding: 0.5rem;
    }
    
    /* Sliders */
    .stSlider {
        padding: 1rem 0;
    }
    
    /* Metric styling */
    [data-testid="stMetricValue"] {
        font-size: 1.8rem;
        font-weight: 700;
        color: var(--metric-color);
    }
    
    /* Progress bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Section headers */
    .section-header {
        font-size: 2rem;
        font-weight: 700;
        color: #667eea;
        margin: 2rem 0 1rem 0;
        text-align: center;
        position: relative;
    }
    
    .section-header::after {
        content: '';
        display: block;
        width: 100px;
        height: 4px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        margin: 0.5rem auto;
        border-radius: 2px;
    }
    
    /* Feature boxes */
    .feature-box {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 10px 30px rgba(245, 87, 108, 0.3);
    }
    
    .feature-box h4, .feature-box p {
        color: white !important;
    }
    
    /* Custom link button */
    .custom-link-button {
        display: inline-block;
        width: 100%;
        padding: 1.2rem 2rem;
        font-size: 1.3rem;
        font-weight: 700;
        color: white;
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        border: none;
        border-radius: 15px;
        cursor: pointer;
        text-align: center;
        text-decoration: none;
        box-shadow: 0 8px 25px rgba(245, 87, 108, 0.4);
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    .custom-link-button:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 35px rgba(245, 87, 108, 0.6);
        background: linear-gradient(135deg, #f5576c 0%, #f093fb 100%);
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: var(--expander-bg);
        border-radius: 10px;
        font-weight: 600;
        color: #667eea;
    }
    
    /* Dark mode text color overrides for Streamlit elements */
    @media (prefers-color-scheme: dark) {
        .stMarkdown, .stMarkdown p, .stMarkdown div, .stMarkdown span {
            color: var(--text-primary);
        }

        /* Ensure headings are visible in dark mode */
        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
            color: var(--text-primary);
        }

        /* Update input fields for dark mode */
        .stTextInput input, .stTextArea textarea, .stNumberInput input {
            background-color: var(--input-bg);
            color: var(--text-primary);
            border-color: var(--border-color);
        }

        /* Selectbox dark mode */
        .stSelectbox > div > div {
            background-color: var(--input-bg);
            color: var(--text-primary);
        }

        /* Radio buttons dark mode */
        .stRadio label {
            color: var(--text-primary);
        }

        /* Slider labels dark mode */
        .stSlider label {
            color: var(--text-primary);
        }

        /* Info/success/warning/error messages */
        .stAlert {
            background-color: var(--card-bg);
            color: var(--text-primary);
        }
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Responsive Design */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2.5rem;
        }
        .block-container {
            padding: 1rem;
        }
    }
    </style>
""", unsafe_allow_html=True)

# Animated Header
st.markdown('<h1 class="main-header">⚛ Quantum Gate Simulator</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Explore the fascinating world of quantum computing with interactive visualizations</p>', unsafe_allow_html=True)

# Create tabs with icons
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🎯 Standard Gates",
    "🌀 Rotation Gates",
    "🔮 Faraday Rotator",
    "🔐 BB84 Protocol",
    "🧑‍🔬 About Us"
])

with tab1:
    st.markdown('<p class="section-header">Standard Quantum Gates</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 🎛️ Control Panel")
        
        original_bit = st.selectbox(
            "**Initial Qubit State:**",
            ["|0⟩", "|1⟩", "|+⟩", "|-⟩"],
            help="Choose the starting state of your qubit"
        )
        
        st.markdown("---")
        
        st.markdown("**Select Quantum Gate:**")
        gate_category = st.radio(
            "Gate Category:",
            ["⚡ Pauli Gates", "🌟 Hadamard & Phase", "🚀 Advanced Gates"],
            label_visibility="collapsed"
        )
        
        if gate_category == "⚡ Pauli Gates":
            gate = st.selectbox("", ["Identity", "X (NOT)", "Y", "Z"], label_visibility="collapsed")
        elif gate_category == "🌟 Hadamard & Phase":
            gate = st.selectbox("", ["H (Hadamard)", "S (Phase)", "T", "S† (S-dagger)", "T† (T-dagger)"], label_visibility="collapsed")
        else:
            gate = st.selectbox("", ["SX (√X)", "SY (√Y)", "RZ(π/2)"], label_visibility="collapsed")
        
        st.markdown("---")
        apply_button = st.button("🚀 Apply Gate", use_container_width=True)
        
        # Gate information
        gate_info_dict = {
            "Identity": "No change - Identity operation",
            "X (NOT)": "Bit flip: |0⟩↔|1⟩ (Quantum NOT)",
            "Y": "Bit & phase flip combination",
            "Z": "Phase flip: |1⟩→-|1⟩",
            "H (Hadamard)": "Creates superposition states",
            "S (Phase)": "90° phase rotation (π/2)",
            "T": "45° phase rotation (π/4)",
            "S† (S-dagger)": "Inverse S gate (-π/2)",
            "T† (T-dagger)": "Inverse T gate (-π/4)",
            "SX (√X)": "Square root of X gate",
            "SY (√Y)": "Square root of Y gate",
            "RZ(π/2)": "Z-axis rotation by π/2"
        }
        
        st.markdown(f"""
        <div class="info-box">
        <h4>📖 Gate Information</h4>
        <p><strong>{gate}</strong></p>
        <p>{gate_info_dict.get(gate, "")}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 📊 Quantum State Visualization")
        
        if apply_button:
            qc = QuantumCircuit(1)
            
            # Set initial state
            if original_bit == "|1⟩":
                qc.x(0)
            elif original_bit == "|+⟩":
                qc.h(0)
            elif original_bit == "|-⟩":
                qc.x(0)
                qc.h(0)
            
            # Apply gate
            if gate != "Identity":
                if gate == "X (NOT)":
                    qc.x(0)
                elif gate == "Y":
                    qc.y(0)
                elif gate == "Z":
                    qc.z(0)
                elif gate == "H (Hadamard)":
                    qc.h(0)
                elif gate == "S (Phase)":
                    qc.s(0)
                elif gate == "T":
                    qc.t(0)
                elif gate == "S† (S-dagger)":
                    qc.sdg(0)
                elif gate == "T† (T-dagger)":
                    qc.tdg(0)
                elif gate == "SX (√X)":
                    qc.sx(0)
                elif gate == "SY (√Y)":
                    qc.sy(0)
                elif gate == "RZ(π/2)":
                    qc.rz(np.pi/2, 0)
            
            state = Statevector.from_instruction(qc)
            state_array = state.data
            
            # Display state info
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.metric("α (|0⟩)", f"{state_array[0]:.3f}")
            with col_b:
                st.metric("β (|1⟩)", f"{state_array[1]:.3f}")
            with col_c:
                st.metric("Phase", f"{np.angle(state_array[1]):.3f} rad")
            
            st.markdown("---")
            
            col_p1, col_p2 = st.columns(2)
            with col_p1:
                st.metric("P(|0⟩)", f"{abs(state_array[0])**2:.4f}")
            with col_p2:
                st.metric("P(|1⟩)", f"{abs(state_array[1])**2:.4f}")
            
            st.markdown("---")
            
            # Bloch sphere
            fig = plot_bloch_multivector(state)
            st.pyplot(fig)
            plt.close()
            
            # Circuit diagram
            st.markdown("#### 🔧 Quantum Circuit")
            try:
                circuit_fig = qc.draw(output='mpl', style='iqp')
                st.pyplot(circuit_fig)
                plt.close()
            except:
                st.code(qc.draw(output='text'), language='text')
        
        else:
            st.info("👆 Configure your quantum gate and click 'Apply Gate' to see the magic!")
        
        st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<p class="section-header">Rotation Gates with Animation</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 🎚️ Rotation Controls")
        
        initial_state = st.selectbox("**Initial State:**", ["|0⟩", "|1⟩", "|+⟩", "|-⟩"], key="rot_state")
        
        st.markdown("---")
        
        rotation_axis = st.radio("**Rotation Axis:**", ["X", "Y", "Z"])
        
        angle_degrees = st.slider(
            "**Rotation Angle (degrees):**",
            min_value=0,
            max_value=360,
            value=90,
            step=15
        )
        
        angle_radians = np.deg2rad(angle_degrees)
        
        st.markdown(f"""
        <div class="info-box">
        <h4>📐 Angle Information</h4>
        <p><strong>Degrees:</strong> {angle_degrees}°</p>
        <p><strong>Radians:</strong> {angle_radians:.4f} rad</p>
        <p><strong>In terms of π:</strong> {angle_degrees/180:.2f}π</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        animate = st.checkbox("🎬 Show rotation animation", value=False)
        
        if animate:
            num_steps = st.slider("Animation steps:", 5, 50, 20)
            animation_speed = st.slider("Animation speed:", 1, 10, 5)
        
        apply_rotation = st.button("🔄 Apply Rotation", use_container_width=True, key="apply_rot")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 📊 Rotation Visualization")
        
        if apply_rotation:
            if animate:
                angles = np.linspace(0, angle_radians, num_steps)
                
                initial_qc = QuantumCircuit(1)
                if initial_state == "|1⟩":
                    initial_qc.x(0)
                elif initial_state == "|+⟩":
                    initial_qc.h(0)
                elif initial_state == "|-⟩":
                    initial_qc.x(0)
                    initial_qc.h(0)
                
                initial_statevector = Statevector.from_instruction(initial_qc)
                
                animation_placeholder = st.empty()
                progress_bar = st.progress(0)
                
                import time
                
                for i, current_angle in enumerate(angles):
                    rotation_qc = QuantumCircuit(1)
                    
                    if rotation_axis == "X":
                        rotation_qc.rx(current_angle, 0)
                    elif rotation_axis == "Y":
                        rotation_qc.ry(current_angle, 0)
                    else:
                        rotation_qc.rz(current_angle, 0)
                    
                    state = initial_statevector.evolve(rotation_qc)
                    state_array = state.data
                    
                    fig = plot_bloch_multivector(state)
                    
                    with animation_placeholder.container():
                        col_a, col_b, col_c = st.columns(3)
                        with col_a:
                            st.metric("Step", f"{i+1}/{num_steps}")
                        with col_b:
                            st.metric("Angle", f"{np.rad2deg(current_angle):.1f}°")
                        with col_c:
                            st.metric("Progress", f"{((i+1)/num_steps)*100:.0f}%")
                        
                        st.pyplot(fig)
                        
                        col_1, col_2 = st.columns(2)
                        with col_1:
                            st.metric("|α|²", f"{abs(state_array[0])**2:.3f}")
                        with col_2:
                            st.metric("|β|²", f"{abs(state_array[1])**2:.3f}")
                    
                    plt.close()
                    progress_bar.progress((i + 1) / num_steps)
                    time.sleep(0.1 / animation_speed)
                
                progress_bar.empty()
                st.success("✅ Animation complete!")
                
            else:
                qc = QuantumCircuit(1)
                
                if initial_state == "|1⟩":
                    qc.x(0)
                elif initial_state == "|+⟩":
                    qc.h(0)
                elif initial_state == "|-⟩":
                    qc.x(0)
                    qc.h(0)
                
                if rotation_axis == "X":
                    qc.rx(angle_radians, 0)
                elif rotation_axis == "Y":
                    qc.ry(angle_radians, 0)
                else:
                    qc.rz(angle_radians, 0)
                
                state = Statevector.from_instruction(qc)
                state_array = state.data
                
                col_a, col_b = st.columns(2)
                with col_a:
                    st.metric("α (|0⟩)", f"{state_array[0]:.4f}")
                with col_b:
                    st.metric("β (|1⟩)", f"{state_array[1]:.4f}")
                
                st.markdown("---")
                
                fig = plot_bloch_multivector(state)
                st.pyplot(fig)
                plt.close()
                
                st.markdown("#### 🔧 Circuit Diagram")
                try:
                    circuit_fig = qc.draw(output='mpl', style='iqp')
                    st.pyplot(circuit_fig)
                    plt.close()
                except:
                    st.code(qc.draw(output='text'), language='text')
        
        else:
            st.info("👆 Set your rotation parameters and click 'Apply Rotation'")
        
        st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.markdown('<p class="section-header">Faraday Rotator Simulator</p>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box" style="text-align: center;">
    <h4>🔬 About the Faraday Effect</h4>
    <p>
    The Faraday effect causes the polarization plane of light to rotate when passing through a medium 
    in a magnetic field. This quantum phenomenon is fundamental to optical isolators and magnetic field sensors.
    </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### ⚙️ Physical Parameters")
        
        initial_polarization = st.radio(
            "**Initial Polarization:**",
            ["Horizontal (|H⟩)", "Vertical (|V⟩)", "Diagonal (+45°)", "Anti-diagonal (-45°)"]
        )
        
        st.markdown("---")
        
        verdet_constant = st.slider(
            "**Verdet Constant (rad/T·m):**",
            min_value=1.0,
            max_value=100.0,
            value=50.0,
            step=1.0
        )
        
        magnetic_field = st.slider(
            "**Magnetic Field (Tesla):**",
            min_value=0.0,
            max_value=5.0,
            value=1.0,
            step=0.1
        )
        
        path_length = st.slider(
            "**Path Length (meters):**",
            min_value=0.0,
            max_value=1.0,
            value=0.1,
            step=0.01
        )
        
        faraday_angle = verdet_constant * magnetic_field * path_length
        faraday_angle_deg = np.rad2deg(faraday_angle) % 360
        
        st.markdown(f"""
        <div class="gradient-box">
        <h3>🧮 Faraday Rotation</h3>
        <h2>θ = {faraday_angle_deg:.1f}°</h2>
        <p>θ = V × B × L = {faraday_angle:.3f} rad</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        show_faraday_animation = st.checkbox("🎬 Animate propagation", value=True, key="faraday_anim")
        
        if show_faraday_animation:
            propagation_steps = st.slider("Steps:", 10, 50, 25, key="faraday_steps")
            animation_speed = st.slider("Speed:", 1, 10, 5, key="anim_speed")
        
        simulate_faraday = st.button("🔬 Run Simulation", use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 📊 Polarization Evolution")
        
        if simulate_faraday:
            if initial_polarization == "Horizontal (|H⟩)":
                initial_angle = 0
            elif initial_polarization == "Vertical (|V⟩)":
                initial_angle = 90
            elif initial_polarization == "Diagonal (+45°)":
                initial_angle = 45
            else:
                initial_angle = -45
            
            if show_faraday_animation:
                angles_through_medium = np.linspace(0, faraday_angle_deg, propagation_steps)
                distances = np.linspace(0, path_length, propagation_steps)
                
                animation_placeholder = st.empty()
                progress_bar = st.progress(0)
                
                import time
                
                for i, (rotation_angle, current_distance) in enumerate(zip(angles_through_medium, distances)):
                    current_pol_angle = initial_angle + rotation_angle
                    
                    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
                    
                    # 3D wave visualization
                    ax1 = plt.subplot(121, projection='3d')
                    z = np.linspace(0, 2*np.pi, 100)
                    angle_rad = np.deg2rad(current_pol_angle)
                    Ex = np.cos(angle_rad) * np.sin(z)
                    Ey = np.sin(angle_rad) * np.sin(z)
                    
                    ax1.plot(Ex, Ey, z, 'b-', linewidth=2.5, label='E-field', alpha=0.8)
                    
                    arrow_length = 1.2
                    ax1.quiver(0, 0, 0, 
                              arrow_length * np.cos(angle_rad), 
                              arrow_length * np.sin(angle_rad), 
                              0,
                              color='red', arrow_length_ratio=0.3, linewidth=4,
                              label=f'Pol: {current_pol_angle:.1f}°')
                    
                    ax1.set_xlabel('Ex (H)', fontsize=11, fontweight='bold')
                    ax1.set_ylabel('Ey (V)', fontsize=11, fontweight='bold')
                    ax1.set_zlabel('Propagation', fontsize=11, fontweight='bold')
                    ax1.set_title(f'Light Wave\nDistance: {current_distance*100:.1f} cm', 
                                 fontsize=13, fontweight='bold', color='#667eea')
                    ax1.set_xlim([-1.5, 1.5])
                    ax1.set_ylim([-1.5, 1.5])
                    ax1.set_zlim([0, 2*np.pi])
                    ax1.legend(loc='upper right', fontsize=9)
                    ax1.view_init(elev=20, azim=45)
                    ax1.grid(True, alpha=0.3)
                    
                    # Polarization plane view
                    ax2.set_aspect('equal')
                    
                    # Reference axes
                    ax2.arrow(0, 0, 1.2, 0, head_width=0.1, head_length=0.1, 
                             fc='gray', ec='gray', alpha=0.3)
                    ax2.arrow(0, 0, 0, 1.2, head_width=0.1, head_length=0.1, 
                             fc='gray', ec='gray', alpha=0.3)
                    ax2.text(1.35, 0, 'H', fontsize=13, ha='left', va='center', fontweight='bold')
                    ax2.text(0, 1.35, 'V', fontsize=13, ha='center', va='bottom', fontweight='bold')
                    
                    # Initial polarization
                    initial_rad = np.deg2rad(initial_angle)
                    ax2.arrow(0, 0, np.cos(initial_rad), np.sin(initial_rad), 
                             head_width=0.15, head_length=0.15, 
                             fc='blue', ec='blue', alpha=0.3, linewidth=2.5,
                             label=f'Initial: {initial_angle}°')
                    
                    # Current polarization
                    ax2.arrow(0, 0, np.cos(angle_rad), np.sin(angle_rad), 
                             head_width=0.15, head_length=0.15, 
                             fc='red', ec='red', alpha=1.0, linewidth=3.5,
                             label=f'Current: {current_pol_angle:.1f}°')
                    
                    # Rotation arc
                    if rotation_angle > 0:
                        arc_angles = np.linspace(initial_rad, angle_rad, 50)
                        arc_x = 0.5 * np.cos(arc_angles)
                        arc_y = 0.5 * np.sin(arc_angles)
                        ax2.plot(arc_x, arc_y, 'g--', linewidth=2.5, alpha=0.8)
                        ax2.text(0, -0.8, f'Rotation: {rotation_angle:.1f}°', 
                                fontsize=12, ha='center', color='green', 
                                fontweight='bold', bbox=dict(boxstyle='round', 
                                facecolor='lightgreen', alpha=0.5))
                    
                    ax2.set_xlim([-1.6, 1.6])
                    ax2.set_ylim([-1.6, 1.6])
                    ax2.set_title(f'Polarization Plane\nB = {magnetic_field:.1f} T', 
                                 fontsize=13, fontweight='bold', color='#667eea')
                    ax2.legend(loc='upper right', fontsize=10)
                    ax2.grid(True, alpha=0.3, linestyle='--')
                    ax2.axhline(y=0, color='k', linewidth=0.8, alpha=0.3)
                    ax2.axvline(x=0, color='k', linewidth=0.8, alpha=0.3)
                    
                    plt.tight_layout()
                    
                    with animation_placeholder.container():
                        col_a, col_b, col_c = st.columns(3)
                        with col_a:
                            st.metric("Distance", f"{current_distance*100:.1f} cm", 
                                     f"{(current_distance/path_length)*100:.0f}%")
                        with col_b:
                            st.metric("Rotation", f"{rotation_angle:.1f}°")
                        with col_c:
                            st.metric("Polarization", f"{current_pol_angle:.1f}°")
                        
                        st.pyplot(fig)
                    
                    plt.close()
                    progress_bar.progress((i + 1) / propagation_steps)
                    time.sleep(0.1 / animation_speed)
                
                progress_bar.empty()
                st.success(f"✅ Polarization rotated from {initial_angle}° to {initial_angle + faraday_angle_deg:.1f}°")
                
                # Quantum state representation
                st.markdown("---")
                st.markdown("#### ⚛️ Quantum State Representation")
                
                qc_initial = QuantumCircuit(1)
                if initial_polarization == "Horizontal (|H⟩)":
                    pass
                elif initial_polarization == "Vertical (|V⟩)":
                    qc_initial.x(0)
                elif initial_polarization == "Diagonal (+45°)":
                    qc_initial.h(0)
                else:
                    qc_initial.x(0)
                    qc_initial.h(0)
                
                initial_state = Statevector.from_instruction(qc_initial)
                rotation_qc = QuantumCircuit(1)
                rotation_qc.rz(2 * faraday_angle, 0)
                final_state = initial_state.evolve(rotation_qc)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**Initial State**")
                    fig = plot_bloch_multivector(initial_state)
                    st.pyplot(fig)
                    plt.close()
                with col2:
                    st.markdown("**Final State**")
                    fig = plot_bloch_multivector(final_state)
                    st.pyplot(fig)
                    plt.close()
                
            else:
                # Static visualization
                final_pol_angle = initial_angle + faraday_angle_deg
                
                fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
                
                # 3D wave
                ax1 = plt.subplot(121, projection='3d')
                z = np.linspace(0, 2*np.pi, 100)
                angle_rad = np.deg2rad(final_pol_angle)
                Ex = np.cos(angle_rad) * np.sin(z)
                Ey = np.sin(angle_rad) * np.sin(z)
                
                ax1.plot(Ex, Ey, z, 'b-', linewidth=2.5, alpha=0.8)
                arrow_length = 1.2
                ax1.quiver(0, 0, 0, 
                          arrow_length * np.cos(angle_rad), 
                          arrow_length * np.sin(angle_rad), 
                          0,
                          color='red', arrow_length_ratio=0.3, linewidth=4)
                
                ax1.set_xlabel('Ex (H)', fontsize=11, fontweight='bold')
                ax1.set_ylabel('Ey (V)', fontsize=11, fontweight='bold')
                ax1.set_zlabel('Propagation', fontsize=11, fontweight='bold')
                ax1.set_title(f'Final Light Wave\nAfter {path_length*100:.1f} cm', 
                             fontsize=13, fontweight='bold', color='#667eea')
                ax1.set_xlim([-1.5, 1.5])
                ax1.set_ylim([-1.5, 1.5])
                ax1.set_zlim([0, 2*np.pi])
                ax1.view_init(elev=20, azim=45)
                ax1.grid(True, alpha=0.3)
                
                # Polarization comparison
                ax2.set_aspect('equal')
                ax2.arrow(0, 0, 1.2, 0, head_width=0.1, head_length=0.1, 
                         fc='gray', ec='gray', alpha=0.3)
                ax2.arrow(0, 0, 0, 1.2, head_width=0.1, head_length=0.1, 
                         fc='gray', ec='gray', alpha=0.3)
                ax2.text(1.35, 0, 'H', fontsize=13, fontweight='bold')
                ax2.text(0, 1.35, 'V', fontsize=13, fontweight='bold')
                
                # Initial
                initial_rad = np.deg2rad(initial_angle)
                ax2.arrow(0, 0, np.cos(initial_rad), np.sin(initial_rad), 
                         head_width=0.15, head_length=0.15, 
                         fc='blue', ec='blue', alpha=0.3, linewidth=2.5,
                         label=f'Initial: {initial_angle}°')
                
                # Final
                ax2.arrow(0, 0, np.cos(angle_rad), np.sin(angle_rad), 
                         head_width=0.15, head_length=0.15, 
                         fc='red', ec='red', linewidth=3.5,
                         label=f'Final: {final_pol_angle:.1f}°')
                
                # Arc
                arc_angles = np.linspace(initial_rad, angle_rad, 50)
                arc_x = 0.5 * np.cos(arc_angles)
                arc_y = 0.5 * np.sin(arc_angles)
                ax2.plot(arc_x, arc_y, 'g--', linewidth=2.5, alpha=0.8)
                ax2.text(0, -0.8, f'Rotation: {faraday_angle_deg:.1f}°', 
                        fontsize=12, ha='center', color='green', fontweight='bold',
                        bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.5))
                
                ax2.set_xlim([-1.6, 1.6])
                ax2.set_ylim([-1.6, 1.6])
                ax2.set_title(f'Polarization Rotation\nB = {magnetic_field:.1f} T, L = {path_length*100:.1f} cm', 
                             fontsize=13, fontweight='bold', color='#667eea')
                ax2.legend(loc='upper right', fontsize=10)
                ax2.grid(True, alpha=0.3, linestyle='--')
                ax2.axhline(y=0, color='k', linewidth=0.8, alpha=0.3)
                ax2.axvline(x=0, color='k', linewidth=0.8, alpha=0.3)
                
                plt.tight_layout()
                st.pyplot(fig)
                plt.close()
                
                st.success(f"✅ Polarization rotated by {faraday_angle_deg:.1f}°")
        
        else:
            st.info("👆 Configure parameters and click 'Run Simulation'")
        
        st.markdown('</div>', unsafe_allow_html=True)

with tab4:
    st.markdown('<p class="section-header">BB84 Quantum Key Distribution</p>', unsafe_allow_html=True)
    
    # Hero section
    st.markdown("""
    <div class="gradient-box">
        <h1 style='font-size: 2.8rem; margin-bottom: 1rem;'>🔐 BB84 Protocol</h1>
        <p style='font-size: 1.3rem; opacity: 0.95;'>
            The First Quantum Cryptography Protocol - Absolutely Secure Communication
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Introduction
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="info-box" style="height: 100%;">
        <h3 style="color: #667eea !important;">📚 What is BB84?</h3>
        <p style="color: #000000;">
        <strong>BB84</strong> (Bennett-Brassard 1984) is the first and most famous quantum key distribution protocol. 
        It allows two parties, Alice and Bob, to generate a shared secret key that is provably secure against 
        any eavesdropper, even one with unlimited computing power.
        </p>
        <p style="color: #000000;">
        The security comes from the fundamental laws of quantum mechanics - any attempt to measure or intercept 
        the quantum states will inevitably disturb them, alerting Alice and Bob to the presence of an eavesdropper.
        </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="info-box" style="height: 100%;">
        <h3 style="color: #667eea !important;">🎯 Key Features</h3>
        <ul style="font-size: 1.05rem; color: #000000;">
            <li><strong>Unconditional Security:</strong> Based on quantum physics, not computational complexity</li>
            <li><strong>Eavesdropping Detection:</strong> Any interception attempt is detectable</li>
            <li><strong>Perfect Forward Secrecy:</strong> Each session uses a new quantum key</li>
            <li><strong>Photon Polarization:</strong> Uses quantum states of light particles</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # How it works
    st.markdown("""
    <div style='background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); 
                padding: 2rem; border-radius: 15px; border-left: 5px solid #667eea;
                box-shadow: 0 5px 20px rgba(0,0,0,0.1);'>
        <h3 style='color: #667eea; margin-bottom: 1rem; font-size: 1.8rem;'>🔬 How Does BB84 Work?</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Protocol steps
    steps_col1, steps_col2 = st.columns(2)
    
    with steps_col1:
        st.markdown("""
        <div class="info-box" style="background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);">
        <h4 style="color: #764ba2 !important;">1️⃣ Quantum Transmission</h4>
        <p style="color: #000000;">Alice encodes random bits using two different bases (rectilinear and diagonal) and sends photons to Bob.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="info-box" style="background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);">
        <h4 style="color: #764ba2 !important;">2️⃣ Random Measurement</h4>
        <p style="color: #000000;">Bob randomly chooses bases to measure the received photons, recording the results.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="info-box" style="background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);">
        <h4 style="color: #764ba2 !important;">3️⃣ Basis Reconciliation</h4>
        <p style="color: #000000;">Alice and Bob publicly compare their bases (not the bit values) and keep only matching measurements.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with steps_col2:
        st.markdown("""
        <div class="info-box" style="background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);">
        <h4 style="color: #764ba2 !important;">4️⃣ Error Checking</h4>
        <p style="color: #000000;">They sacrifice some bits to check for eavesdropping. High error rate indicates interference.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="info-box" style="background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);">
        <h4 style="color: #764ba2 !important;">5️⃣ Privacy Amplification</h4>
        <p style="color: #000000;">The remaining bits are processed to remove any partial information an eavesdropper might have.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="info-box" style="background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);">
        <h4 style="color: #764ba2 !important;">6️⃣ Secure Key</h4>
        <p style="color: #000000;">Alice and Bob now share an identical, secret key for encrypting communications!</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Two bases
    st.markdown("""
    <div style='background: linear-gradient(135deg, #fff3cd 0%, #ffe8a1 100%); 
                padding: 1.8rem; border-radius: 15px; border-left: 5px solid #ffc107; 
                margin-bottom: 2rem; box-shadow: 0 5px 20px rgba(0,0,0,0.1);'>
        <h4 style='color: #856404; margin-bottom: 1rem; font-size: 1.5rem;'>💡 The Two Bases</h4>
        <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem;'>
            <div style='background: white; padding: 1rem; border-radius: 10px;'>
                <strong style='color: #856404; font-size: 1.1rem;'>Rectilinear Basis (+):</strong><br>
                <span style='color: #000;'>Horizontal (|0⟩) and Vertical (|1⟩) polarizations</span>
            </div>
            <div style='background: white; padding: 1rem; border-radius: 10px;'>
                <strong style='color: #856404; font-size: 1.1rem;'>Diagonal Basis (×):</strong><br>
                <span style='color: #000;'>+45° (|0⟩) and -45° (|1⟩) polarizations</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Security section
    st.markdown("""
    <div style='background: linear-gradient(135deg, #d1ecf1 0%, #bee5eb 100%); 
                padding: 1.8rem; border-radius: 15px; border-left: 5px solid #0c5460; 
                margin-bottom: 2rem; box-shadow: 0 5px 20px rgba(0,0,0,0.1);'>
        <h4 style='color: #0c5460; margin-bottom: 1rem; font-size: 1.5rem;'>🛡️ Why is BB84 Unbreakable?</h4>
        <p style='margin-bottom: 0.8rem; color: #000;'><strong style='color: #0c5460;'>Heisenberg Uncertainty Principle:</strong> Measuring a quantum state in the wrong basis disturbs it.</p>
        <p style='margin-bottom: 0.8rem; color: #000;'><strong style='color: #0c5460;'>No-Cloning Theorem:</strong> It's impossible to create identical copies of unknown quantum states.</p>
        <p style='margin-bottom: 0; color: #000;'><strong style='color: #0c5460;'>Observable Disturbance:</strong> Any eavesdropping attempt introduces detectable errors in the transmission.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Applications
    st.markdown("""
    <div style='background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%); 
                padding: 1.8rem; border-radius: 15px; border-left: 5px solid #155724; 
                margin-bottom: 2rem; box-shadow: 0 5px 20px rgba(0,0,0,0.1);'>
        <h4 style='color: #155724; margin-bottom: 1rem; font-size: 1.5rem;'>🌍 Real-World Applications</h4>
        <ul style='margin-bottom: 0; color: #000;'>
            <li style='margin-bottom: 0.5rem;'><strong style='color: #155724;'>Banking & Finance:</strong> Securing high-value financial transactions</li>
            <li style='margin-bottom: 0.5rem;'><strong style='color: #155724;'>Government Communications:</strong> Protecting classified information</li>
            <li style='margin-bottom: 0.5rem;'><strong style='color: #155724;'>Quantum Internet:</strong> Building the foundation for quantum networks</li>
            <li><strong style='color: #155724;'>Satellite QKD:</strong> China's Micius satellite demonstrated space-based BB84</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Call to action
    st.markdown("""
    <div class="feature-box" style="text-align: center; margin: 3rem 0;">
        <h2 style='font-size: 2.2rem; margin-bottom: 1rem;'>
            🧪 Ready to Experience BB84 in Action?
        </h2>
        <p style='font-size: 1.2rem; margin-bottom: 2rem; opacity: 0.95;'>
            Try our interactive BB84 simulator and see quantum key distribution working in real-time!
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Center the button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
            <a href="https://bb84.srijan.dpdns.org/" target="_blank" style="text-decoration: none;">
                <button class="custom-link-button">
                    🚀 ENTER THE SIMULATION LAB
                </button>
            </a>
        """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Additional resources
    with st.expander("📖 Learn More About BB84"):
        st.markdown("""
        ### Further Reading
        
        - **Original Paper:** Bennett, C. H., & Brassard, G. (1984). "Quantum cryptography: Public key distribution and coin tossing"
        - **Key Concepts:** Quantum mechanics, photon polarization, basis reconciliation, privacy amplification
        - **Modern Implementations:** Commercial QKD systems are now available with distances up to 100+ km
        
        ### Historical Context
        
        BB84 was proposed by Charles Bennett and Gilles Brassard in 1984, making it one of the earliest applications 
        of quantum mechanics to information theory. It laid the foundation for the entire field of quantum cryptography.
        
        ### Recent Achievements
        
        - **2017:** China's Micius satellite achieved intercontinental quantum key distribution
        - **2020:** Commercial quantum networks deployed in major cities worldwide
        - **2023:** Record-breaking QKD distances achieved with trusted node networks
        """)

with tab5:
    st.markdown('<p class="section-header">Meet The Team</p>', unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>The innovators dedicated to making quantum concepts accessible to all.</p>", unsafe_allow_html=True)

    # Custom CSS for team profiles
    st.markdown("""
    <style>
    .profile-card {
        background: var(--card-bg);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 10px 30px var(--shadow-light);
        text-align: center;
        transition: all 0.3s ease;
        border: 1px solid var(--border-color);
        display: flex; /* Use flexbox for alignment */
        flex-direction: column; /* Stack items vertically */
        justify-content: flex-start; /* Align content to the top */
        height: 100%; /* Make cards in a row have the same height */
    }
    .profile-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.25);
    }
    .profile-img {
        width: 150px;
        height: 150px;
        border-radius: 50%;
        object-fit: cover;
        border: 5px solid #667eea;
        margin-bottom: 1rem;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        margin-left: auto;
        margin-right: auto;
    }
    .profile-name {
        font-size: 1.5rem;
        font-weight: 700;
        color: #667eea;
        margin-bottom: 0.25rem;
    }
    .profile-role {
        font-size: 1.1rem;
        font-weight: 600;
        color: #764ba2;
        margin-bottom: 1rem;
    }
    .profile-bio {
        font-size: 0.95rem;
        color: var(--text-secondary);
        line-height: 1.6;
    }
    </style>
    """, unsafe_allow_html=True)

    # --- ROW 1 ---
    col1, col2, col3 = st.columns(3, gap="large")

    with col1:
        st.markdown("""
        <div class="profile-card">
            <img src="https://github.com/ivanho-git/qubit-gates/blob/main/abhinav.jpeg?raw=true" class="profile-img">
            <p class="profile-name">ABHINAV SUNEESH</p>
            <p class="profile-role">BB84 in DFS Researcher</p>
            <p class="profile-bio">
                Explores how BB84 operates within a Decoherence-Free Subspace to protect information from environmental noise.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="profile-card">
            <img src="https://github.com/ivanho-git/qubit-gates/blob/main/ibhann.jpeg?raw=true" class="profile-img">
            <p class="profile-name">IBHAN MUKHERJEE</p>
            <p class="profile-role">How To Catch the Thief?</p>
            <p class="profile-bio">
                The sneaky tester who tries to intercept the quantum key, showing how BB84 detects intrusions..
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="profile-card">
            <img src="https://github.com/ivanho-git/qubit-gates/blob/main/IMG-20251106-WA0032.jpg?raw=true" class="profile-img">
            <p class="profile-name">HARI ASHWIN</p>
            <p class="profile-role">Qubits and Gates Expert</p>
            <p class="profile-bio">
                The technical mind explaining how qubits are prepared, transmitted, and measured using quantum logic gates.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)

    # --- ROW 2 (Centered) ---
    _, col4, col5, _ = st.columns([0.5, 1, 1, 0.5], gap="large")

    with col4:
        st.markdown("""
        <div class="profile-card">
            <img src="https://github.com/ivanho-git/qubit-gates/blob/main/gucci.jpeg?raw=true" class="profile-img">
            <p class="profile-name">SRIJAN GUCHHAIT</p>
            <p class="profile-role">BB84 Explainer & Ideal Conditions Specialist</p>
            <p class="profile-bio">
                Introduces the BB84 protocol and demonstrates how it works perfectly in an ideal, noise-free setting.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col5:
        st.markdown("""
        <div class="profile-card">
            <img src="https://github.com/ivanho-git/qubit-gates/blob/main/IMG-20251106-WA0008.jpg?raw=true" class="profile-img">
            <p class="profile-name">OM THAVARI</p>
            <p class="profile-role">Faraday Rotator Technician</p>
            <p class="profile-bio">
                Manages optical components, ensuring polarization rotations are precise and consistent..
            </p>
        </div>
        """, unsafe_allow_html=True)


# Footer
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
    <div style='text-align: center; color: var(--text-secondary); padding: 2rem 0; border-top: 2px solid var(--border-color); margin-top: 3rem;'>
        <p style='font-size: 1.1rem; margin-bottom: 0.5rem; color: var(--text-secondary);'>Made By Engineers 👷🏻‍♂️ For Curiosity Not Just For Credits 😉</p>
        <p style='font-size: 0.9rem; opacity: 0.8; color: var(--text-secondary);'>Visualizing quantum states on the Bloch sphere | Ibhan Mukherjee</p>
    </div>
""", unsafe_allow_html=True)
