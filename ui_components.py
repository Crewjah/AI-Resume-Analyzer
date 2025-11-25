"""
Ultra-Modern Cyberpunk UI Components for AI Resume Analyzer
Featuring 2025 trending design patterns: Glassmorphism, Neon aesthetics, and Quantum animations
"""
import streamlit as st
import pandas as pd
from typing import List, Dict, Any
import time

def load_css():
    """Load ultra-modern CSS with trending 2025 design patterns"""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@300;400;500&display=swap');
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css');
    
    :root {
        --neon-cyan: #00f5ff;
        --neon-purple: #bf00ff;
        --neon-pink: #ff0080;
        --neon-green: #39ff14;
        --neon-orange: #ff6600;
        --dark-bg: #0a0a0f;
        --glass-bg: rgba(15, 15, 25, 0.8);
        --card-bg: rgba(20, 20, 35, 0.9);
        --accent-gradient: linear-gradient(135deg, var(--neon-cyan), var(--neon-purple));
    }
    
    .stApp {
        background: 
            radial-gradient(circle at 20% 80%, #0d1117 0%, #161b22 25%, #0d1117 50%),
            radial-gradient(circle at 80% 20%, rgba(191, 0, 255, 0.15) 0%, transparent 50%),
            radial-gradient(circle at 40% 40%, rgba(0, 245, 255, 0.1) 0%, transparent 50%),
            conic-gradient(from 180deg at 50% 50%, #0d1117 0deg, #161b22 180deg, #0d1117 360deg);
        background-attachment: fixed;
        font-family: 'Space Grotesk', -apple-system, BlinkMacSystemFont, sans-serif;
        color: #ffffff;
        overflow-x: hidden;
    }
    
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-image: 
            radial-gradient(circle at 25px 25px, rgba(0, 245, 255, 0.03) 2px, transparent 0),
            radial-gradient(circle at 75px 75px, rgba(191, 0, 255, 0.02) 1px, transparent 0);
        background-size: 50px 50px, 100px 100px;
        pointer-events: none;
        z-index: 1;
        animation: driftGrid 60s linear infinite;
    }
    
    @keyframes driftGrid {
        0% { transform: translate(0, 0); }
        100% { transform: translate(50px, 50px); }
    }
    
    @keyframes neonPulse {
        0%, 100% { 
            box-shadow: 
                0 0 20px var(--neon-cyan),
                0 0 40px var(--neon-cyan),
                0 0 60px var(--neon-cyan),
                inset 0 0 20px rgba(0, 245, 255, 0.1);
        }
        50% { 
            box-shadow: 
                0 0 30px var(--neon-purple),
                0 0 60px var(--neon-purple),
                0 0 90px var(--neon-purple),
                inset 0 0 30px rgba(191, 0, 255, 0.1);
        }
    }
    
    @keyframes morphFloat {
        0%, 100% {
            transform: translateY(0px) scale(1);
            filter: blur(0px);
        }
        50% {
            transform: translateY(-10px) scale(1.02);
            filter: blur(0.5px);
        }
    }
    
    @keyframes slideInQuantum {
        0% {
            opacity: 0;
            transform: translateX(-100px) rotateY(45deg) scale(0.8);
            filter: blur(20px);
        }
        100% {
            opacity: 1;
            transform: translateX(0) rotateY(0deg) scale(1);
            filter: blur(0);
        }
    }
    
    @keyframes holographicShift {
        0%, 100% {
            background: linear-gradient(135deg, var(--neon-cyan) 0%, var(--neon-purple) 100%);
            text-shadow: 0 0 30px var(--neon-cyan);
        }
        33% {
            background: linear-gradient(135deg, var(--neon-purple) 0%, var(--neon-pink) 100%);
            text-shadow: 0 0 30px var(--neon-purple);
        }
        66% {
            background: linear-gradient(135deg, var(--neon-pink) 0%, var(--neon-green) 100%);
            text-shadow: 0 0 30px var(--neon-pink);
        }
    }
    
    @keyframes dataStream {
        0% {
            transform: translateX(-100%);
            opacity: 0;
        }
        50% {
            opacity: 1;
        }
        100% {
            transform: translateX(300%);
            opacity: 0;
        }
    }
    
    .main {
        padding: 2rem 3rem;
        max-width: 1800px;
        margin: 0 auto;
        position: relative;
        z-index: 2;
    }
    
    /* Cyberpunk Hero Header */
    .hero-header {
        background: linear-gradient(135deg, 
            rgba(0, 245, 255, 0.12) 0%,
            rgba(191, 0, 255, 0.12) 35%,
            rgba(255, 0, 128, 0.12) 70%,
            rgba(57, 255, 20, 0.12) 100%);
        backdrop-filter: blur(60px) saturate(250%);
        border: 2px solid transparent;
        background-clip: padding-box;
        border-radius: 32px;
        padding: 8rem 5rem;
        text-align: center;
        margin: 2rem 0 4rem 0;
        position: relative;
        overflow: hidden;
        animation: morphFloat 8s ease-in-out infinite;
        box-shadow: 
            0 30px 80px rgba(0, 0, 0, 0.4),
            inset 0 2px 0 rgba(255, 255, 255, 0.1);
    }
    
    .hero-header::before {
        content: '';
        position: absolute;
        inset: 0;
        padding: 2px;
        background: linear-gradient(45deg, 
            var(--neon-cyan) 0%, 
            var(--neon-purple) 25%, 
            var(--neon-pink) 50%, 
            var(--neon-green) 75%, 
            var(--neon-cyan) 100%);
        border-radius: inherit;
        mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
        mask-composite: exclude;
        -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
        -webkit-mask-composite: xor;
        animation: holographicShift 5s ease-in-out infinite;
    }
    
    .hero-header::after {
        content: '';
        position: absolute;
        inset: 2px;
        background: linear-gradient(145deg, 
            rgba(10, 10, 15, 0.95) 0%, 
            rgba(15, 15, 25, 0.9) 50%, 
            rgba(20, 20, 35, 0.95) 100%);
        border-radius: 26px;
        z-index: -1;
    }
    
    .hero-title {
        font-size: 5rem;
        font-weight: 800;
        margin: 0 0 2rem 0;
        background: linear-gradient(135deg, 
            var(--neon-cyan) 0%, 
            var(--neon-purple) 35%, 
            var(--neon-pink) 70%, 
            var(--neon-green) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        line-height: 1;
        letter-spacing: -3px;
        font-family: 'Space Grotesk', sans-serif;
        position: relative;
        animation: holographicShift 6s ease-in-out infinite;
    }
    
    .hero-title::before {
        content: attr(data-text);
        position: absolute;
        top: 0;
        left: 0;
        background: linear-gradient(135deg, var(--neon-cyan), var(--neon-purple));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        z-index: -1;
        filter: blur(3px);
        opacity: 0.7;
        transform: translate(2px, 2px);
    }
    
    .hero-subtitle {
        font-size: 1.8rem;
        font-weight: 400;
        color: rgba(255, 255, 255, 0.95);
        margin: 0 0 3rem 0;
        font-family: 'Space Grotesk', sans-serif;
        letter-spacing: 2px;
        animation: slideInQuantum 2s cubic-bezier(0.16, 1, 0.3, 1) 0.3s backwards;
    }
    
    .hero-description {
        font-size: 1.3rem;
        color: rgba(255, 255, 255, 0.8);
        margin: 0;
        line-height: 1.8;
        font-weight: 300;
        max-width: 800px;
        margin: 0 auto;
        animation: slideInQuantum 2.2s cubic-bezier(0.16, 1, 0.3, 1) 0.6s backwards;
    }
    
    .cyber-accent {
        color: var(--neon-cyan);
        font-weight: 600;
        text-shadow: 0 0 15px var(--neon-cyan);
        position: relative;
    }
    
    .cyber-accent::after {
        content: '';
        position: absolute;
        bottom: -2px;
        left: 0;
        width: 100%;
        height: 1px;
        background: var(--neon-cyan);
        box-shadow: 0 0 10px var(--neon-cyan);
    }
    
    /* Quantum Glass Cards */
    .glass-card {
        background: linear-gradient(145deg, 
            rgba(15, 15, 25, 0.95) 0%,
            rgba(25, 25, 40, 0.9) 50%,
            rgba(20, 20, 35, 0.95) 100%);
        backdrop-filter: blur(70px) saturate(250%);
        border: 1px solid rgba(0, 245, 255, 0.3);
        border-radius: 28px;
        padding: 2rem;
        margin: 2rem 0;
        position: relative;
        overflow: visible;
        animation: slideInQuantum 1.2s cubic-bezier(0.16, 1, 0.3, 1);
        transition: all 0.5s cubic-bezier(0.16, 1, 0.3, 1);
        box-shadow: 
            0 35px 70px rgba(0, 0, 0, 0.6),
            inset 0 2px 0 rgba(255, 255, 255, 0.15),
            0 0 0 1px rgba(0, 245, 255, 0.1),
            0 0 50px rgba(0, 245, 255, 0.05);
        color: white;
    }
    
    .glass-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(90deg, 
            transparent, 
            var(--neon-cyan), 
            var(--neon-purple), 
            var(--neon-cyan), 
            transparent);
        animation: dataStream 4s infinite;
    }
    
    .glass-card:hover {
        transform: translateY(-12px) scale(1.02);
        box-shadow: 
            0 40px 80px rgba(0, 0, 0, 0.7),
            0 0 0 1px rgba(0, 245, 255, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.2);
        border-color: rgba(0, 245, 255, 0.5);
        animation: neonPulse 2s infinite;
    }
    
    /* Holographic Metric Cards */
    .metric-card {
        background: linear-gradient(145deg, 
            rgba(0, 245, 255, 0.03) 0%,
            rgba(191, 0, 255, 0.03) 50%,
            rgba(255, 0, 128, 0.03) 100%);
        backdrop-filter: blur(40px);
        border: 2px solid transparent;
        background-clip: padding-box;
        border-radius: 24px;
        padding: 3rem 2.5rem;
        text-align: center;
        margin: 2rem 0;
        position: relative;
        overflow: hidden;
        animation: slideInQuantum 1.5s cubic-bezier(0.16, 1, 0.3, 1);
        transition: all 0.6s cubic-bezier(0.16, 1, 0.3, 1);
        box-shadow: 
            0 15px 40px rgba(0, 0, 0, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        inset: 0;
        padding: 2px;
        background: linear-gradient(135deg, 
            var(--neon-cyan) 0%, 
            var(--neon-purple) 50%, 
            var(--neon-pink) 100%);
        border-radius: inherit;
        mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
        mask-composite: exclude;
        -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
        -webkit-mask-composite: xor;
        opacity: 0.6;
        animation: holographicShift 4s ease-in-out infinite;
    }
    
    .metric-card:hover {
        transform: translateY(-15px) scale(1.05);
        box-shadow: 
            0 30px 70px rgba(0, 0, 0, 0.6),
            0 0 0 1px rgba(0, 245, 255, 0.5),
            0 0 50px rgba(0, 245, 255, 0.3);
        animation: neonPulse 1.5s infinite;
    }
    
    .metric-value {
        font-size: 4rem;
        font-weight: 800;
        margin: 0 0 1rem 0;
        background: linear-gradient(135deg, 
            var(--neon-cyan) 0%, 
            var(--neon-green) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-family: 'JetBrains Mono', monospace;
        position: relative;
        animation: holographicShift 3s ease-in-out infinite;
    }
    
    .metric-value::after {
        content: '';
        position: absolute;
        bottom: -8px;
        left: 50%;
        width: 60px;
        height: 3px;
        background: linear-gradient(90deg, var(--neon-cyan), var(--neon-purple));
        transform: translateX(-50%);
        border-radius: 2px;
        box-shadow: 0 0 15px currentColor;
    }
    
    .metric-label {
        font-size: 1.2rem;
        font-weight: 700;
        color: rgba(255, 255, 255, 0.9);
        text-transform: uppercase;
        letter-spacing: 3px;
        margin: 0 0 0.8rem 0;
        font-family: 'Space Grotesk', sans-serif;
    }
    
    .metric-description {
        font-size: 1rem;
        color: rgba(0, 245, 255, 0.8);
        font-weight: 400;
        margin: 0;
        font-style: italic;
        letter-spacing: 1px;
    }
    
    /* Quantum Progress Bars */
    .progress-container {
        background: linear-gradient(145deg, 
            rgba(15, 15, 25, 0.95), 
            rgba(25, 25, 40, 0.9));
        border: 1px solid rgba(0, 245, 255, 0.3);
        border-radius: 20px;
        padding: 2.5rem;
        margin: 2rem 0;
        backdrop-filter: blur(30px);
        position: relative;
        overflow: hidden;
    }
    
    .progress-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 2px;
        background: linear-gradient(90deg, 
            transparent, 
            var(--neon-cyan), 
            var(--neon-purple), 
            transparent);
        animation: dataStream 3s infinite;
    }
    
    .progress-bar {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 50px;
        height: 20px;
        overflow: hidden;
        position: relative;
        box-shadow: inset 0 2px 8px rgba(0, 0, 0, 0.4);
    }
    
    .progress-fill {
        background: linear-gradient(90deg, 
            var(--neon-cyan) 0%, 
            var(--neon-purple) 30%, 
            var(--neon-pink) 70%, 
            var(--neon-green) 100%);
        height: 100%;
        border-radius: 50px;
        transition: width 3s cubic-bezier(0.16, 1, 0.3, 1);
        position: relative;
        overflow: hidden;
        box-shadow: 0 0 30px currentColor;
    }
    
    .progress-fill::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, 
            transparent, 
            rgba(255, 255, 255, 0.4), 
            transparent);
        animation: dataStream 2s infinite;
    }
    
    /* Futuristic Buttons */
    .stButton > button {
        background: linear-gradient(135deg, 
            var(--neon-cyan) 0%, 
            var(--neon-purple) 50%, 
            var(--neon-pink) 100%) !important;
        border: none !important;
        border-radius: 20px !important;
        padding: 1.2rem 3rem !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 700 !important;
        font-size: 1.2rem !important;
        color: #000 !important;
        box-shadow: 
            0 15px 40px rgba(0, 245, 255, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.3) !important;
        transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1) !important;
        text-transform: uppercase !important;
        letter-spacing: 2px !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, 
            transparent, 
            rgba(255, 255, 255, 0.3), 
            transparent);
        transition: left 0.5s;
    }
    
    .stButton > button:hover {
        transform: translateY(-5px) scale(1.05) !important;
        box-shadow: 
            0 25px 60px rgba(0, 245, 255, 0.6),
            0 0 0 1px rgba(255, 255, 255, 0.2) !important;
        background: linear-gradient(135deg, 
            var(--neon-purple) 0%, 
            var(--neon-pink) 50%, 
            var(--neon-green) 100%) !important;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    /* Holographic Status Badges */
    .status-badge {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        padding: 1.2rem 2.5rem;
        border-radius: 35px;
        font-weight: 800;
        font-size: 1.1rem;
        margin: 1.5rem 0;
        text-transform: uppercase;
        letter-spacing: 3px;
        font-family: 'Space Grotesk', sans-serif;
        position: relative;
        overflow: hidden;
        border: 2px solid transparent;
        background: linear-gradient(145deg, 
            rgba(0, 245, 255, 0.15), 
            rgba(191, 0, 255, 0.15));
        backdrop-filter: blur(40px);
        box-shadow: 
            0 15px 40px rgba(0, 0, 0, 0.4),
            inset 0 2px 0 rgba(255, 255, 255, 0.1);
        transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
        min-width: 220px;
        text-align: center;
    }
    
    .status-badge::before {
        content: '';
        position: absolute;
        inset: 0;
        padding: 2px;
        background: linear-gradient(135deg, 
            var(--neon-cyan), 
            var(--neon-green));
        border-radius: inherit;
        mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
        mask-composite: exclude;
        -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
        -webkit-mask-composite: xor;
    }
    
    .status-badge:hover {
        transform: scale(1.05);
        box-shadow: 0 15px 40px rgba(0, 245, 255, 0.4);
    }
    
    .status-badge.success {
        color: var(--neon-green);
        text-shadow: 0 0 15px var(--neon-green);
    }
    
    .status-badge.warning {
        color: var(--neon-orange);
        text-shadow: 0 0 15px var(--neon-orange);
    }
    
    .status-badge.error {
        color: var(--neon-pink);
        text-shadow: 0 0 15px var(--neon-pink);
    }
    
    /* Skills Showcase */
    .skills-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .skill-chip {
        background: linear-gradient(145deg, 
            rgba(0, 245, 255, 0.1), 
            rgba(191, 0, 255, 0.1));
        border: 1px solid rgba(0, 245, 255, 0.3);
        border-radius: 15px;
        padding: 1rem 1.5rem;
        text-align: center;
        color: var(--neon-cyan);
        font-weight: 600;
        font-size: 0.95rem;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        backdrop-filter: blur(20px);
        position: relative;
        overflow: hidden;
    }
    
    .skill-chip::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, 
            transparent, 
            rgba(0, 245, 255, 0.2), 
            transparent);
        transition: left 0.5s;
    }
    
    .skill-chip:hover {
        transform: translateY(-3px) scale(1.05);
        border-color: var(--neon-purple);
        color: var(--neon-purple);
        box-shadow: 0 10px 30px rgba(0, 245, 255, 0.3);
    }
    
    .skill-chip:hover::before {
        left: 100%;
    }
    
    /* Cyber Sidebar */
    .css-1d391kg, [data-testid="stSidebar"] {
        background: linear-gradient(180deg, 
            rgba(10, 10, 15, 0.98) 0%, 
            rgba(15, 15, 25, 0.95) 50%, 
            rgba(20, 20, 35, 0.98) 100%) !important;
        backdrop-filter: blur(50px) !important;
        border-right: 2px solid rgba(0, 245, 255, 0.3) !important;
    }
    
    /* Holographic File Uploader */
    .uploadedFile, [data-testid="stFileUploader"] {
        border: 3px dashed var(--neon-cyan) !important;
        border-radius: 28px !important;
        background: linear-gradient(145deg, 
            rgba(0, 245, 255, 0.08), 
            rgba(191, 0, 255, 0.08)) !important;
        padding: 5rem 4rem !important;
        transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1) !important;
        position: relative !important;
        overflow: hidden !important;
        box-shadow: 
            inset 0 0 50px rgba(0, 245, 255, 0.1),
            0 10px 40px rgba(0, 0, 0, 0.3) !important;
    }
    
    .uploadedFile::before, [data-testid="stFileUploader"]::before {
        content: '';
        position: absolute;
        inset: 0;
        background: linear-gradient(45deg, 
            transparent, 
            rgba(0, 245, 255, 0.1), 
            transparent);
        animation: dataStream 3s infinite;
    }
    
    .uploadedFile:hover, [data-testid="stFileUploader"]:hover {
        border-color: var(--neon-purple) !important;
        box-shadow: 
            0 0 50px rgba(0, 245, 255, 0.4),
            inset 0 0 50px rgba(0, 245, 255, 0.1) !important;
        transform: scale(1.02) !important;
    }
    
    /* Quantum Scrollbar */
    ::-webkit-scrollbar {
        width: 14px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(15, 15, 25, 0.9);
        border-radius: 7px;
        border: 1px solid rgba(0, 245, 255, 0.1);
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, 
            var(--neon-cyan), 
            var(--neon-purple));
        border-radius: 7px;
        box-shadow: 0 0 20px var(--neon-cyan);
        border: 2px solid transparent;
        background-clip: padding-box;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, 
            var(--neon-purple), 
            var(--neon-pink));
        box-shadow: 0 0 25px var(--neon-purple);
    }
    
    /* Loading Animation */
    .loading-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 4rem;
        background: linear-gradient(145deg, 
            rgba(15, 15, 25, 0.95), 
            rgba(25, 25, 40, 0.9));
        border-radius: 24px;
        border: 2px solid rgba(0, 245, 255, 0.3);
        backdrop-filter: blur(30px);
        position: relative;
        overflow: hidden;
    }
    
    .loading-spinner {
        width: 80px;
        height: 80px;
        border: 4px solid rgba(0, 245, 255, 0.2);
        border-top: 4px solid var(--neon-cyan);
        border-right: 4px solid var(--neon-purple);
        border-radius: 50%;
        animation: quantumSpin 1.5s linear infinite;
        box-shadow: 
            0 0 30px var(--neon-cyan),
            inset 0 0 30px rgba(0, 245, 255, 0.1);
        position: relative;
    }
    
    .loading-spinner::before {
        content: '';
        position: absolute;
        inset: 10px;
        border: 2px solid transparent;
        border-top: 2px solid var(--neon-pink);
        border-radius: 50%;
        animation: quantumSpin 1s linear infinite reverse;
    }
    
    @keyframes quantumSpin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .loading-text {
        margin-top: 2rem;
        font-size: 1.3rem;
        font-weight: 600;
        color: var(--neon-cyan);
        text-align: center;
        animation: holographicShift 2s ease-in-out infinite;
    }
    
    /* Input Fields */
    .stTextInput > div > div > input, 
    .stTextArea > div > div > textarea {
        background: rgba(15, 15, 25, 0.9) !important;
        border: 2px solid rgba(0, 245, 255, 0.3) !important;
        border-radius: 16px !important;
        color: white !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 1rem !important;
        padding: 1rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus, 
    .stTextArea > div > div > textarea:focus {
        border-color: var(--neon-cyan) !important;
        box-shadow: 
            0 0 30px rgba(0, 245, 255, 0.4),
            inset 0 0 20px rgba(0, 245, 255, 0.1) !important;
        outline: none !important;
    }
    
    /* Clean UI Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    header {visibility: hidden;}
    
    /* Mobile Responsive */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 3rem;
        }
        .main {
            padding: 1rem 2rem;
        }
        .glass-card {
            padding: 2rem;
            margin: 1.5rem 0;
        }
    }
    </style>
    """, unsafe_allow_html=True)

def create_hero_header():
    """Create a futuristic cyberpunk hero header"""
    st.markdown("""
    <div class="hero-header">
        <h1 class="hero-title" data-text="⚡ AI NEXUS RESUME">⚡ AI NEXUS RESUME</h1>
        <p class="hero-subtitle">
            Next-Generation <span class="cyber-accent">Neural Intelligence</span> Career Accelerator
        </p>
        <p class="hero-description">
            Experience cutting-edge AI algorithms for <span class="cyber-accent">quantum ATS analysis</span>, 
            advanced skills mapping, and <span class="cyber-accent">holographic job matching</span> 
            that propels your career into the digital future.
        </p>
    </div>
    """, unsafe_allow_html=True)

def create_metric_card(title: str, value: str, description: str = "", icon: str = "📊"):
    """Create a holographic metric card"""
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-icon">{icon}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-label">{title}</div>
        <div class="metric-description">{description}</div>
    </div>
    """, unsafe_allow_html=True)

def create_glass_card(content: str, title: str = ""):
    """Create a quantum glass morphism card"""
    title_html = f"""
    <div style="text-align: center; margin-bottom: 2rem; padding-bottom: 1rem; border-bottom: 1px solid rgba(0, 245, 255, 0.3);">
        <h3 style='color: var(--neon-cyan); margin: 0; font-size: 1.8rem; font-weight: 800; 
         text-transform: uppercase; letter-spacing: 3px; text-shadow: 0 0 30px var(--neon-cyan);'>{title}</h3>
    </div>
    """ if title else ""
    st.markdown(f"""
    <div class="glass-card">
        {title_html}
        <div>
            {content}
        </div>
    </div>
    """, unsafe_allow_html=True)

def display_skills_showcase(skills_data: Dict[str, List[str]]):
    """Display skills in a cyberpunk grid layout"""
    if not skills_data:
        st.info("🔍 No technical skills detected. Consider adding more technology-specific terms.")
        return
    
    for category, skills in skills_data.items():
        st.markdown(f"""
        <h4 style='color: var(--neon-purple); margin: 2rem 0 1rem 0; font-size: 1.3rem; 
         text-transform: uppercase; letter-spacing: 2px; font-weight: 700;'>
            🚀 {category} Skills
        </h4>
        """, unsafe_allow_html=True)
        
        skills_html = ""
        for skill in skills:
            skills_html += f'<div class="skill-chip">{skill}</div>'
        
        st.markdown(f'<div class="skills-container">{skills_html}</div>', unsafe_allow_html=True)

def display_keywords_showcase(keywords: List[str], title: str = "Keywords", icon: str = "🔑"):
    """Display keywords in a futuristic showcase"""
    if not keywords:
        return
    
    st.markdown(f"""
    <h4 style='color: var(--neon-green); margin: 2rem 0 1rem 0; font-size: 1.3rem;
     text-transform: uppercase; letter-spacing: 2px; font-weight: 700;'>
        {icon} {title}
    </h4>
    """, unsafe_allow_html=True)
    
    keywords_html = ""
    for keyword in keywords:
        keywords_html += f'<div class="skill-chip">{keyword}</div>'
    
    st.markdown(f'<div class="skills-container">{keywords_html}</div>', unsafe_allow_html=True)

def create_progress_bar(value: int, max_value: int = 100, label: str = ""):
    """Create a quantum progress bar"""
    percentage = min(100, (value / max_value) * 100)
    
    st.markdown(f"""
    <div class="progress-container">
        <h4 style='color: white; margin-bottom: 1.5rem; font-size: 1.2rem; font-weight: 600;'>{label}</h4>
        <div class="progress-bar">
            <div class="progress-fill" style="width: {percentage}%"></div>
        </div>
        <p style='color: var(--neon-cyan); margin-top: 1rem; font-size: 1.1rem; font-weight: 600;'>
            {value}/{max_value} ({percentage:.1f}%)
        </p>
    </div>
    """, unsafe_allow_html=True)

def create_status_badge(status: str, badge_type: str = "success"):
    """Create a holographic status badge"""
    st.markdown(f"""
    <div class="status-badge {badge_type}">
        {status}
    </div>
    """, unsafe_allow_html=True)

def create_recommendation_card(title: str, content: str, icon: str = "💡"):
    """Create a recommendation card"""
    st.markdown(f"""
    <div class="glass-card">
        <h4 style='color: var(--neon-orange); margin-bottom: 1rem; font-size: 1.2rem; font-weight: 600;'>
            {icon} {title}
        </h4>
        <p style='color: rgba(255,255,255,0.9); line-height: 1.6; margin: 0;'>{content}</p>
    </div>
    """, unsafe_allow_html=True)

def show_loading_animation(text: str = "Processing..."):
    """Show a quantum loading animation"""
    st.markdown(f"""
    <div class="loading-container">
        <div class="loading-spinner"></div>
        <div class="loading-text">{text}</div>
    </div>
    """, unsafe_allow_html=True)

def create_upload_zone():
    """Create a cyberpunk upload zone"""
    st.markdown("""
    <div class="glass-card" style="text-align: center;">
        <h3 style='color: var(--neon-cyan); margin-bottom: 2rem;'>📡 NEURAL UPLOAD INTERFACE</h3>
        <p style='color: rgba(255,255,255,0.8); font-size: 1.1rem;'>
            Initialize quantum file transfer protocol
        </p>
    </div>
    """, unsafe_allow_html=True)

def create_feature_showcase():
    """Create a feature showcase for sidebar"""
    st.markdown("""
    <div style="padding: 2.5rem 1.5rem;">
        <h3 style='color: var(--neon-purple); text-align: center; margin-bottom: 3rem; 
         font-size: 1.5rem; text-transform: uppercase; letter-spacing: 3px; 
         text-shadow: 0 0 30px var(--neon-purple); font-weight: 800;'>
            🌟 NEXUS FEATURES
        </h3>
        <div style="display: flex; flex-direction: column; gap: 1.5rem;">
            <div style='background: linear-gradient(135deg, rgba(0,245,255,0.15), rgba(0,245,255,0.05)); 
             padding: 1.5rem; border-radius: 16px; border: 1px solid rgba(0,245,255,0.3); 
             position: relative; overflow: hidden; transition: all 0.3s ease;'
             onmouseover='this.style.transform="scale(1.02)"; this.style.boxShadow="0 10px 30px rgba(0,245,255,0.3)"'
             onmouseout='this.style.transform="scale(1)"; this.style.boxShadow="none"'>
                <div style='position: absolute; top: 0; left: 0; right: 0; height: 2px; 
                 background: linear-gradient(90deg, transparent, var(--neon-cyan), transparent);'></div>
                <strong style='color: var(--neon-cyan); font-size: 1.1rem; display: block; margin-bottom: 0.5rem;'>⚡ Quantum ATS Analysis</strong>
                <span style='color: rgba(255,255,255,0.85); font-size: 0.95rem; line-height: 1.4;'>Neural network compatibility scoring</span>
            </div>
            <div style='background: linear-gradient(135deg, rgba(191,0,255,0.15), rgba(191,0,255,0.05)); 
             padding: 1.5rem; border-radius: 16px; border: 1px solid rgba(191,0,255,0.3); 
             position: relative; overflow: hidden; transition: all 0.3s ease;'
             onmouseover='this.style.transform="scale(1.02)"; this.style.boxShadow="0 10px 30px rgba(191,0,255,0.3)"'
             onmouseout='this.style.transform="scale(1)"; this.style.boxShadow="none"'>
                <div style='position: absolute; top: 0; left: 0; right: 0; height: 2px; 
                 background: linear-gradient(90deg, transparent, var(--neon-purple), transparent);'></div>
                <strong style='color: var(--neon-purple); font-size: 1.1rem; display: block; margin-bottom: 0.5rem;'>🧠 AI Skills Mapping</strong>
                <span style='color: rgba(255,255,255,0.85); font-size: 0.95rem; line-height: 1.4;'>Advanced technology detection</span>
            </div>
            <div style='background: linear-gradient(135deg, rgba(255,0,128,0.15), rgba(255,0,128,0.05)); 
             padding: 1.5rem; border-radius: 16px; border: 1px solid rgba(255,0,128,0.3); 
             position: relative; overflow: hidden; transition: all 0.3s ease;'
             onmouseover='this.style.transform="scale(1.02)"; this.style.boxShadow="0 10px 30px rgba(255,0,128,0.3)"'
             onmouseout='this.style.transform="scale(1)"; this.style.boxShadow="none"'>
                <div style='position: absolute; top: 0; left: 0; right: 0; height: 2px; 
                 background: linear-gradient(90deg, transparent, var(--neon-pink), transparent);'></div>
                <strong style='color: var(--neon-pink); font-size: 1.1rem; display: block; margin-bottom: 0.5rem;'>🎯 Holographic Matching</strong>
                <span style='color: rgba(255,255,255,0.85); font-size: 0.95rem; line-height: 1.4;'>Real-time job compatibility analysis</span>
            </div>
            <div style='background: linear-gradient(135deg, rgba(57,255,20,0.15), rgba(57,255,20,0.05)); 
             padding: 1.5rem; border-radius: 16px; border: 1px solid rgba(57,255,20,0.3); 
             position: relative; overflow: hidden; transition: all 0.3s ease;'
             onmouseover='this.style.transform="scale(1.02)"; this.style.boxShadow="0 10px 30px rgba(57,255,20,0.3)"'
             onmouseout='this.style.transform="scale(1)"; this.style.boxShadow="none"'>
                <div style='position: absolute; top: 0; left: 0; right: 0; height: 2px; 
                 background: linear-gradient(90deg, transparent, var(--neon-green), transparent);'></div>
                <strong style='color: var(--neon-green); font-size: 1.1rem; display: block; margin-bottom: 0.5rem;'>🚀 Quantum Recommendations</strong>
                <span style='color: rgba(255,255,255,0.85); font-size: 0.95rem; line-height: 1.4;'>Personalized career acceleration</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_success_message(message: str):
    """Create a success message"""
    st.success(f"✨ {message}")

def create_error_message(message: str):
    """Create an error message"""
    st.error(f"⚠️ {message}")