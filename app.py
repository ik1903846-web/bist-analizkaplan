import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings("ignore")

st.set_page_config(page_title="BIST Finansal Analiz", page_icon="📊", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Inter:wght@400;500;600;700;800&display=swap');
html,body,.stApp{background-color:#0a0f1a!important;color:#e2e8f0;font-family:'Inter',sans-serif;}
.stApp>header{background-color:#0a0f1a!important;}
[data-testid="stSidebar"]{background-color:#0f1626!important;border-right:1px solid #1e2d42;}
.block-container{padding-top:1.5rem!important;max-width:1400px!important;}
.card-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:.75rem;margin-bottom:1.5rem;}
.card{background:#0f1626;border:1px solid #1e2d42;border-radius:10px;padding:1.1rem 1.25rem;position:relative;overflow:hidden;}
.card::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;}
.card.green::before{background:#22c55e;}.card.yellow::before{background:#eab308;}.card.blue::before{background:#3b82f6;}.card.red::before{background:#ef4444;}
.card-label{color:#64748b;font-size:.68rem;letter-spacing:.12em;text-transform:uppercase;font-weight:600;margin-bottom:.4rem;}
.card-value{font-size:1.9rem;font-weight:800;line-height:1;}
.card-value.green{color:#22c55e;}.card-value.yellow{color:#eab308;}.card-value.blue{color:#3b82f6;}.card-value.red{color:#ef4444;}.card-value.white{color:#f1f5f9;}
.tbl-header{display:grid;grid-template-columns:40px 90px 1fr 95px 70px 70px 110px 110px 60px;gap:.5rem;padding:.5rem 1rem;color:#475569;font-size:.67rem;letter-spacing:.1em;text-transform:uppercase;border-bottom:1px solid #1e2d42;margin-bottom:.4rem;font-weight:600;}
.tbl-row{display:grid;grid-template-columns:40px 90px 1fr 95px 70px 70px 110px 110px 60px;gap:.5rem;align-items:center;padding:.8rem 1rem;background:#0f1626;border:1px solid #1a2540;border-radius:8px;margin-bottom:.35rem;}
.tbl-ticker{color:#f1f5f9;font-weight:800;font-size:.9rem;letter-spacing:.05em;}
.tbl-sector{color:#64748b;font-size:.78rem;}
.tbl-price{color:#22c55e;font-weight:700;font-size:.9rem;font-family:'JetBrains Mono',monospace;}
.tbl-val{color:#94a3b8;font-size:.82rem;font-family:'JetBrains Mono',monospace;}
.tbl-dcf{color:#3b82f6;font-size:.82rem;font-family:'JetBrains Mono',monospace;}
.tbl-num{color:#334155;font-size:.78rem;}
.badge{display:inline-block;padding:.2rem .55rem;border-radius:5px;font-size:.75rem;font-weight:700;font-family:'JetBrains Mono',monospace;}
.badge-green{background:rgba(34,197,94,.15);color:#22c55e;border:1px solid rgba(34,197,94,.3);}
.badge-red{background:rgba(239,68,68,.15);color:#ef4444;border:1px solid rgba(239,68,68,.3);}
.badge-yellow{background:rgba(234,179,8,.15);color:#eab308;border:1px solid rgba(234,179,8,.3);}
.detail-header{background:linear-gradient(135deg,#0f1a2e 0%,#131d30 100%);border:1px solid #1e2d42;border-radius:14px;padding:1.75rem 2rem;margin-bottom:1.25rem;}
.detail-ticker{font-size:2.5rem;font-weight:900;color:#f1f5f9;letter-spacing:.05em;margin:0;}
.detail-name{color:#475569;font-size:.85rem;margin:.2rem 0 .8rem;}
.detail-price{font-size:1.8rem;font-weight:800;color:#22c55e;font-family:'JetBrains Mono',monospace;}
.val-box{background:#0a0f1a;border:1px solid #1e2d42;border-radius:10px;padding:1rem 1.25rem;text-align:center;}
.val-box-label{color:#475569;font-size:.7rem;text-transform:uppercase;letter-spacing:.1em;margin-bottom:.4rem;}
.val-box-value{font-size:1.6rem;font-weight:800;font-family:'JetBrains Mono',monospace;}
.val-box-tag{font-size:.7rem;margin-top:.3rem;}
.pb-wrap{margin-bottom:.85rem;}
.pb-header{display:flex;justify-content:space-between;margin-bottom:5px;font-size:.8rem;}
.pb-label{color:#94a3b8;}.pb-val{font-weight:700;font-family:'JetBrains Mono',monospace;}
.pb-track{height:7px;background:#1e2d42;border-radius:4px;overflow:hidden;}
.pb-fill{height:100%;border-radius:4px;}
.fin-table{width:100%;border-collapse:collapse;font-size:.83rem;}
.fin-table th{background:#0a0f1a;color:#475569;padding:.65rem .9rem;text-align:right;font-weight:600;font-size:.7rem;letter-spacing:.08em;text-transform:uppercase;border-bottom:1px solid #1e2d42;}
.fin-table th:first-child{text-align:left;}
.fin-table td{padding:.6rem .9rem;border-bottom:1px solid #0f1626;text-align:right;font-family:'JetBrains Mono',monospace;font-size:.8rem;color:#94a3b8;}
.fin-table td:first-child{text-align:left;color:#cbd5e1;font-family:'Inter',sans-serif;font-size:.78rem;font-weight:500;}
.fin-table tr:hover td{background:#0f1626;}
.fin-table .section-header td{background:#0d1525!important;color:#3b82f6;font-family:'Inter',sans-serif;font-weight:700;font-size:.72rem;letter-spacing:.1em;text-transform:uppercase;border-top:1px solid #1e2d42;}
.positive{color:#22c55e!important;}.negative{color:#ef4444!important;}
.sidebar-section{background:#131d30;border:1px solid #1e2d42;border-radius:10px;padding:1rem;margin-bottom:1rem;font-size:.8rem;color:#64748b;}
.sidebar-section b{color:#e2e8f0;}
.app-title{font-size:1.5rem;font-weight:900;color:#f1f5f9;margin:0;letter-spacing:.03em;}
.app-sub{color:#3b82f6;font-size:.82rem;margin:.2rem 0 1rem;font-weight:500;}
.stButton>button{background:#131d30!important;color:#e2e8f0!important;border:1px solid #1e2d42!important;border-radius:7px!important;font-size:.82rem!important;font-weight:600!important;}
.stTabs [data-baseweb="tab-list"]{background:#0f1626!important;border-radius:10px!important;border:1px solid #1e2d42!important;padding:.25rem!important;}
.stTabs [data-baseweb="tab"]{color:#475569!important;border-radius:7px!important;font-size:.83rem!important;font-weight:600!important;}
.stTabs [aria-selected="true"]{background:#131d30!important;color:#e2e8f0!important;}
[data-testid="stFileUploadDropzone"]{background:#0f1626!important;border:1px dashed #1e2d42!important;border-radius:10px!important;}
</style>
""", unsafe_allow_html=True)

BILANCO = ["DÖNEN VARLIKLAR","DURAN VARLIKLAR","TOPLAM VARLIKLAR","KISA VADELİ YÜKÜMLÜLÜKLER","UZUN VADELİ YÜKÜMLÜLÜKLER","ÖZKAYNAKLAR"]
GELIR = ["HASILAT","BRÜT KAR/ZARAR","ESAS FAALİYET KARI/ZARARI","FİNANSMAN GİDERİ ÖNCESİ FAALİYET KARI/ZARARI","SÜRDÜRÜLEN FAALİYETLER VERGİ ÖNCESİ KARI/ZARARI","DÖNEM KARI/ZARARI"]
LABELS = {"DÖNEN VARLIKLAR":"Dönen Varlıklar","DURAN VARLIKLAR":"Duran Varlıklar","TOPLAM VARLIKLAR":"Toplam Varlıklar","KISA VADELİ YÜKÜMLÜLÜKLER":"Kısa Vadeli Yükümlülükler","UZUN VADELİ YÜKÜMLÜLÜKLER":"Uzun Vadeli Yükümlülükler","ÖZKAYNAKLAR":"Özkaynaklar","HASILAT":"Hasılat","BRÜT KAR/ZARAR":"Brüt Kâr/Zarar","ESAS FAALİYET KARI/ZARARI":"Esas Faaliyet Kârı/Zararı","FİNANSMAN GİDERİ ÖNCESİ FAALİYET KARI/ZARARI":"Fin. Gideri Öncesi Faaliyet K/Z","SÜRDÜRÜLEN FAALİYETLER VERGİ ÖNCESİ KARI/ZARARI":"Vergi Öncesi Kâr/Zarar","DÖNEM KARI/ZARARI":"Dönem Kârı/Zararı"}

for k,v in [("financial_data",{}),("selected_stock",None),("live_data",{})]:
    if k not in st.session_state: st.session_state[k]=v

def load_excel(f):
    xl=pd.ExcelFile(f); data={}; errors=[]
    for s in xl.sheet_names:
        try:
            df=xl.parse(s,index_col=0)
            df.columns=[str(c).strip() for c in df.columns]
            df.index=[str(i).strip().upper() for i in df.index]
            for c in df.columns:
                df[c]=pd.to_numeric(df[c].astype(str).str.replace(",",".").str.replace(" ",""),errors="coerce")
            data[s.strip().upper()]=df
        except Exception as e: errors.append(f"{s}: {e}")
    return data,errors

@st.cache_data(ttl=300,show_spinner=False)
def fetch_stock(ticker):
    try:
        s=yf.Ticker(f"{ticker}.IS"); i=s.info
        return {"price":i.get("currentPrice") or i.get("regularMarketPrice") or 0,"fk":i.get("trailingPE"),"pddd":i.get("priceToBook"),"fd_favok":i.get("enterpriseToEbitda"),"market_cap":i.get("marketCap"),"shares":i.get("sharesOutstanding"),"sector":i.get("sector","—"),"name":i.get("longName",ticker),"52w_high":i.get("fiftyTwoWeekHigh"),"52w_low":i.get("fiftyTwoWeekLow")}
    except:
        return {k:None for k in ["price","fk","pddd","fd_favok","market_cap","shares","sector","name","52w_high","52w_low"]}

def calc_dcf(fin,shares,disc=0.25,tg=0.08,yrs=5):
    try:
        if "DÖNEM KARI/ZARARI" not in fin.index: return None
        ni=fin.loc["DÖNEM KARI/ZARARI"].dropna()
        if len(ni)<2: return None
        pos=ni[ni>0]
        avg_gr=float(np.clip(np.mean([(pos.iloc[i]/pos.iloc[i-1]-1) for i in range(1,len(pos))][-3:]),-0.2,0.6)) if len(pos)>=2 else 0.1
        last=float(ni.iloc[-1])
        if last<=0: return None
        cfs=[last*(1+avg_gr)**y for y in range(1,yrs+1)]
        tv=cfs[-1]*(1+tg)/(disc-tg)
        total=sum(cf/(1+disc)**i for i,cf in enumerate(cfs,1))+tv/(1+disc)**yrs
        return (round(total/shares,2),round(avg_gr*100,1)) if shares and shares>0 else None
    except: return None

def gm(fin):
    m={}
    try:
        def s(k): return fin.loc[k].dropna() if k in fin.index else pd.Series(dtype=float)
        rev,ni,gross,eq,ta=s("HASILAT"),s("DÖNEM KARI/ZARARI"),s("BRÜT KAR/ZARAR"),s("ÖZKAYNAKLAR"),s("TOPLAM VARLIKLAR")
        if len(rev)>=2 and rev.iloc[-2]!=0: m["rev_yoy"]=(rev.iloc[-1]/rev.iloc[-2]-1)*100
        if len(ni)>=2 and ni.iloc[-2]>0: m["ni_yoy"]=(ni.iloc[-1]/ni.iloc[-2]-1)*100
        if len(ta)>=2 and ta.iloc[-2]>0: m["asset_yoy"]=(ta.iloc[-1]/ta.iloc[-2]-1)*100
        if len(rev)>=1 and rev.iloc[-1]>0 and len(gross)>=1: m["gross_margin"]=(gross.iloc[-1]/rev.iloc[-1])*100
        if len(rev)>=1 and rev.iloc[-1]>0 and len(ni)>=1: m["net_margin"]=(ni.iloc[-1]/rev.iloc[-1])*100
        if len(eq)>=1 and eq.iloc[-1]>0 and len(ni)>=1: m["roe"]=(ni.iloc[-1]/eq.iloc[-1])*100
    except: pass
    return m

def fmt(val,unit="₺"):
    if val is None or (isinstance(val,float) and np.isnan(val)): return "—"
    v=float(val)
    if abs(v)>=1e9: return f"{v/1e9:.2f}B {unit}"
    if abs(v)>=1e6: return f"{v/1e6:.1f}M {unit}"
    if abs(v)>=1e3: return f"{v/1e3:.1f}K {unit}"
    return f"{v:.2f} {unit}"

def fmt2(val,dec=1):
    if val is None or (isinstance(val,float) and np.isnan(val)): return "—"
    return f"{float(val):.{dec}f}"

def card(label,value,cls="blue"):
    return f'<div class="card {cls}"><div class="card-label">{label}</div><div class="card-value {cls}">{value}</div></div>'

def vbox(label,value,cls="white",tag=""):
    t=f'<div class="val-box-tag" style="color:#475569;">{tag}</div>' if tag else ""
    return f'<div class="val-box"><div class="val-box-label">{label}</div><div class="val-box-value {cls}">{value}</div>{t}</div>'

def pbar(label,value,color="#22c55e",mx=100):
    if value is None: return ""
    pct=min(abs(value)/mx*100,100); vc="#22c55e" if value>=0 else "#ef4444"
    return f'<div class="pb-wrap"><div class="pb-header"><span class="pb-label">{label}</span><span class="pb-val" style="color:{vc};">%{value:.1f}</span></div><div class="pb-track"><div class="pb-fill" style="width:{pct}%;background:{color};"></div></div></div>'

LY=dict(paper_bgcolor="#0f1626",plot_bgcolor="#0a0f1a",font=dict(color="#94a3b8",family="Inter"),margin=dict(t=40,b=30,l=10,r=10),hoverlabel=dict(bgcolor="#131d30",bordercolor="#1e2d42",font=dict(color="#e2e8f0")))
AX=dict(gridcolor="#1e2d42",zerolinecolor="#1e2d42",tickfont=dict(size=10,color="#475569"))

def show_detail(ticker):
    fin=st.session_state.financial_data.get(ticker,pd.DataFrame())
    info=st.session_state.live_data.get(ticker,{})
    if not info:
        with st.spinner(f"{ticker} verileri çekiliyor..."):
            info=fetch_stock(ticker); st.session_state.live_data[ticker]=info
    price=info.get("price") or 0; mcap=info.get("market_cap"); shares=info.get("shares")
    g=gm(fin) if not fin.empty else {}
    dcf=calc_dcf(fin,shares) if not fin.empty and shares else None
    if st.button("← Taramaya Dön",key="back"): st.session_state.selected_stock=None; st.rerun()
    dt=dcf[0] if dcf else None; pot=((dt/price)-1)*100 if dt and price>0 else None
    pc="#22c55e" if pot and pot>0 else "#ef4444"
    st.markdown(f'<div class="detail-header"><div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:1rem;"><div><p class="detail-name">{info.get("name",ticker)} · {info.get("sector","—")}</p><h1 class="detail-ticker">{ticker}</h1><div style="display:flex;align-items:center;gap:1rem;margin-top:.5rem;"><span class="detail-price">{price:.2f} ₺</span><span style="color:#475569;font-size:.82rem;">Piyasa Değeri: {fmt(mcap)}</span></div></div><div style="text-align:right;"><div style="color:#475569;font-size:.68rem;text-transform:uppercase;letter-spacing:.1em;margin-bottom:.3rem;">DCF Hedef Fiyat</div><div style="font-size:1.6rem;font-weight:800;color:{pc};font-family:JetBrains Mono,monospace;">{f"{dt:.2f} ₺" if dt else "—"}</div><div style="color:{pc};font-size:.85rem;font-weight:700;">{f"%{pot:.1f} potansiyel" if pot else ""}</div></div></div></div>',unsafe_allow_html=True)
    t1,t2,t3=st.tabs(["💰 Özet & Değerleme","📋 Finansal Tablolar","📈 Grafikler"])
    with t1:
        fk=info.get("fk"); pddd=info.get("pddd"); fd=info.get("fd_favok")
        fkc="green" if fk and fk<15 else("yellow" if fk and fk<30 else "red")
        pdc="green" if pddd and pddd<3 else("yellow" if pddd and pddd<6 else "red")
        fdc="green" if fd and fd<10 else("yellow" if fd and fd<20 else "red")
        potc="green" if pot and pot>0 else "red"
        c1,c2,c3,c4=st.columns(4)
        c1.markdown(vbox("F/K",fmt2(fk),fkc,"✓ Ucuz" if fk and fk<15 else ""),unsafe_allow_html=True)
        c2.markdown(vbox("PD/DD",fmt2(pddd),pdc,"✓ Ucuz" if pddd and pddd<3 else ""),unsafe_allow_html=True)
        c3.markdown(vbox("FD/FAVÖK",fmt2(fd),fdc,"✓ Ucuz" if fd and fd<10 else ""),unsafe_allow_html=True)
        c4.markdown(vbox("DCF Potansiyel",f"%{pot:.1f}" if pot else "—",potc,f"{dt:.2f} ₺" if dt else ""),unsafe_allow_html=True)
        w52h=info.get("52w_high"); w52l=info.get("52w_low")
        if w52h and w52l and price:
            p52=min(max((price-w52l)/(w52h-w52l)*100 if w52h!=w52l else 50,0),100)
            st.markdown(f'<div style="background:#0f1626;border:1px solid #1e2d42;border-radius:10px;padding:1rem 1.25rem;margin:1rem 0;"><div style="display:flex;justify-content:space-between;font-size:.75rem;color:#475569;margin-bottom:.5rem;"><span>52H Min: {w52l:.2f} ₺</span><span style="color:#94a3b8;font-weight:600;">Şu an: {price:.2f} ₺</span><span>52H Max: {w52h:.2f} ₺</span></div><div class="pb-track"><div class="pb-fill" style="width:{p52:.0f}%;background:linear-gradient(90deg,#ef4444,#eab308,#22c55e);"></div></div></div>',unsafe_allow_html=True)
        cl,cr=st.columns(2)
        with cl:
            st.markdown("**📈 Büyüme & Performans**")
            h=pbar("Satış Büyümesi (YoY)",g.get("rev_yoy"),"#3b82f6",200)+pbar("Net Kâr Büyümesi (YoY)",g.get("ni_yoy"),"#22c55e",200)+pbar("Varlık Büyümesi (YoY)",g.get("asset_yoy"),"#eab308",100)
            st.markdown(h,unsafe_allow_html=True) if h else st.caption("Finansal veri yükleyin")
        with cr:
            st.markdown("**💎 Karlılık**")
            h=pbar("Brüt Kâr Marjı",g.get("gross_margin"),"#f97316",70)+pbar("Net Kâr Marjı",g.get("net_margin"),"#22c55e",40)+pbar("Özkaynak Karlılığı (ROE)",g.get("roe"),"#ec4899",60)
            st.markdown(h,unsafe_allow_html=True) if h else st.caption("Finansal veri yükleyin")
        if not fin.empty:
            st.markdown("<br>**✖ Büyüme Çarpanları**",unsafe_allow_html=True)
            mults={LABELS.get(m,m):fin.loc[m].dropna().iloc[-1]/fin.loc[m].dropna().iloc[0] for m in BILANCO+GELIR if m in fin.index and len(fin.loc[m].dropna())>=2 and fin.loc[m].dropna().iloc[0]>0}
            if mults:
                keys=list(mults.keys()); rows2=[keys[i:i+3] for i in range(0,len(keys),3)]
                for rk in rows2:
                    cols=st.columns(3)
                    for j,k in enumerate(rk):
                        v=mults[k]; cls="green" if v>=3 else("yellow" if v>=1.5 else "red")
                        cols[j].markdown(vbox(k,f"{v:.1f}x",cls),unsafe_allow_html=True)
    with t2:
        if fin.empty: st.info("Bu hisse için finansal veri yüklenmedi.")
        else:
            years=list(fin.columns)
            def mktbl(metrics,section):
                h=f'<tr class="section-header"><td colspan="{len(years)+1}">{section}</td></tr>'
                for m in metrics:
                    if m not in fin.index: continue
                    cells="".join(f'<td class="{"positive" if (v:=fin.loc[m,y] if y in fin.columns else None) and not(isinstance(v,float) and np.isnan(v)) and v>0 else "negative" if v and not(isinstance(v,float) and np.isnan(v)) and v<0 else ""}">{fmt(v,"") if v is not None and not(isinstance(v,float) and np.isnan(v)) else "—"}</td>' for y in years)
                    h+=f"<tr><td>{LABELS.get(m,m)}</td>{cells}</tr>"
                return h
            yh="".join(f"<th>{y}</th>" for y in years)
            st.markdown(f'<div style="overflow-x:auto;"><table class="fin-table"><thead><tr><th>Kalem</th>{yh}</tr></thead><tbody>{mktbl(BILANCO,"📊 BİLANÇO")}{mktbl(GELIR,"📋 GELİR TABLOSU")}</tbody></table></div>',unsafe_allow_html=True)
    with t3:
        if fin.empty: st.info("Grafik için finansal veri yükleyin.")
        else:
            years=list(fin.columns)
            def gs(k): return fin.loc[k].reindex(years).tolist() if k in fin.index else []
            fig1=make_subplots(rows=1,cols=3,subplot_titles=("Varlık Artışı","Ciro (Hasılat)","Net Kâr"),horizontal_spacing=.06)
            for key,ci,color in [("TOPLAM VARLIKLAR",1,"#3b82f6"),("HASILAT",2,"#22c55e"),("DÖNEM KARI/ZARARI",3,"#eab308")]:
                vals=gs(key)
                if vals:
                    fig1.add_trace(go.Bar(x=years,y=vals,marker_color=["#ef4444" if(v is None or(isinstance(v,float) and np.isnan(v)) or v<0) else color for v in vals],text=[fmt(v,"") for v in vals],textposition="outside",textfont=dict(size=9,color="#94a3b8"),showlegend=False),row=1,col=ci)
            fig1.update_layout(**LY,height=380); fig1.update_xaxes(**AX); fig1.update_yaxes(**AX,showticklabels=False)
            st.plotly_chart(fig1,use_container_width=True)
            rev,ni,gross=gs("HASILAT"),gs("DÖNEM KARI/ZARARI"),gs("BRÜT KAR/ZARAR")
            if rev:
                fig2=go.Figure()
                fig2.add_trace(go.Scatter(x=years,y=rev,name="Hasılat",line=dict(color="#3b82f6",width=2.5),mode="lines+markers",marker=dict(size=7)))
                if gross: fig2.add_trace(go.Scatter(x=years,y=gross,name="Brüt Kâr",line=dict(color="#f97316",width=2,dash="dot"),mode="lines+markers",marker=dict(size=7)))
                if ni: fig2.add_trace(go.Scatter(x=years,y=ni,name="Net Kâr",line=dict(color="#22c55e",width=2.5),mode="lines+markers",marker=dict(size=7)))
                fig2.update_layout(**LY,height=320,title_text="Gelir Trendi",legend=dict(bgcolor="#131d30",bordercolor="#1e2d42")); fig2.update_xaxes(**AX); fig2.update_yaxes(**AX)
                st.plotly_chart(fig2,use_container_width=True)

def show_table():
    tickers=list(st.session_state.financial_data.keys())
    missing=[t for t in tickers if t not in st.session_state.live_data]
    if missing:
        prog=st.progress(0,text=f"Canlı veriler çekiliyor...")
        for i,t in enumerate(missing):
            st.session_state.live_data[t]=fetch_stock(t); prog.progress((i+1)/len(missing),text=f"Çekiliyor: {t}")
        prog.empty()
    rows=[]
    for t in tickers:
        info=st.session_state.live_data.get(t,{}); fin=st.session_state.financial_data.get(t,pd.DataFrame())
        price=info.get("price") or 0; dcf=calc_dcf(fin,info.get("shares")) if not fin.empty and info.get("shares") else None
        pot=((dcf[0]/price)-1)*100 if dcf and price>0 else None
        rows.append({"ticker":t,"price":price,"fk":info.get("fk"),"pddd":info.get("pddd"),"sector":info.get("sector","—"),"dcf":dcf[0] if dcf else None,"pot":pot})
    total=len(rows); cheap_fk=sum(1 for r in rows if r["fk"] and r["fk"]<15); cheap_pd=sum(1 for r in rows if r["pddd"] and r["pddd"]<3); dcf_up=sum(1 for r in rows if r["pot"] and r["pot"]>20)
    st.markdown(f'<div class="card-grid">{card("Toplam Hisse",total,"blue")}{card("Ucuz F/K (<15)",cheap_fk,"green")}{card("Ucuz PD/DD (<3)",cheap_pd,"yellow")}{card("DCF Yukarı (>%20)",dcf_up,"green")}</div>',unsafe_allow_html=True)
    with st.expander("🔍 Filtreler",expanded=False):
        c1,c2,c3,c4=st.columns(4)
        search=c1.text_input("Hisse Ara",placeholder="THYAO..."); max_fk=c2.number_input("Maks F/K",value=0,step=5,min_value=0); max_pd=c3.number_input("Maks PD/DD",value=0.0,step=0.5,min_value=0.0); sort_opt=c4.selectbox("Sırala",["DCF Potansiyel ↓","F/K ↑","PD/DD ↑","Ticker A-Z"])
    filtered=rows[:]
    if search: filtered=[r for r in filtered if search.upper() in r["ticker"]]
    if max_fk>0: filtered=[r for r in filtered if r["fk"] and r["fk"]<=max_fk]
    if max_pd>0: filtered=[r for r in filtered if r["pddd"] and r["pddd"]<=max_pd]
    sk={"DCF Potansiyel ↓":(lambda x:x["pot"] or -999,True),"F/K ↑":(lambda x:x["fk"] or 9999,False),"PD/DD ↑":(lambda x:x["pddd"] or 9999,False),"Ticker A-Z":(lambda x:x["ticker"],False)}[sort_opt]
    filtered.sort(key=sk[0],reverse=sk[1])
    st.markdown('<div class="tbl-header"><span>#</span><span>HİSSE</span><span>SEKTÖR</span><span>FİYAT</span><span>F/K</span><span>PD/DD</span><span>DCF HEDEF</span><span>DCF POT%</span><span>DETAY</span></div>',unsafe_allow_html=True)
    for i,r in enumerate(filtered):
        pot_badge=""
        if r["pot"] is not None:
            cls="badge-green" if r["pot"]>20 else("badge-yellow" if r["pot"]>0 else "badge-red")
            pot_badge=f'<span class="badge {cls}">%{r["pot"]:.0f}</span>'
        cr,cb=st.columns([10,1])
        cr.markdown(f'<div class="tbl-row"><span class="tbl-num">{i+1}</span><span class="tbl-ticker">{r["ticker"]}</span><span class="tbl-sector">{r["sector"]}</span><span class="tbl-price">{r["price"]:.2f} ₺</span><span class="tbl-val">{fmt2(r["fk"])}</span><span class="tbl-val">{fmt2(r["pddd"])}</span><span class="tbl-dcf">{f"{r["dcf"]:.2f} ₺" if r["dcf"] else "—"}</span><span>{pot_badge}</span><span></span></div>',unsafe_allow_html=True)
        if cb.button("📊",key=f"b_{r['ticker']}_{i}"): st.session_state.selected_stock=r["ticker"]; st.rerun()

def main():
    st.markdown('<h1 class="app-title">📊 BIST FİNANSAL ANALİZ</h1><p class="app-sub">Dip Tarama · DCF Hesaplama · Finansal Tablolar · Canlı Veriler</p>',unsafe_allow_html=True)
    with st.sidebar:
        st.markdown("## 📁 Veri Yükle")
        st.markdown('<div class="sidebar-section"><b>Excel Formatı:</b><br><br>• Her <b>sayfa (tab)</b> = 1 hisse kodu<br>• <b>İlk sütun</b> = metrik isimleri<br>• <b>Diğer sütunlar</b> = yıllar<br><br>Fiyat, F/K, PD/DD otomatik çekilir.</div>',unsafe_allow_html=True)
        uploaded=st.file_uploader("Excel Dosyası Yükle",type=["xlsx","xls"])
        if uploaded:
            with st.spinner("Yükleniyor..."):
                data,errors=load_excel(uploaded); st.session_state.financial_data=data; st.session_state.live_data={}
            if data: st.success(f"✅ {len(data)} hisse yüklendi")
            if errors:
                with st.expander(f"⚠️ {len(errors)} hata"):
                    [st.caption(e) for e in errors]
        if st.session_state.financial_data:
            st.markdown("---")
            if st.button("🔄 Canlı Verileri Güncelle",use_container_width=True): st.session_state.live_data={}; st.cache_data.clear(); st.rerun()
    if not st.session_state.financial_data:
        st.markdown('<div style="text-align:center;padding:3rem 2rem;background:#0f1626;border:1px dashed #1e2d42;border-radius:14px;"><div style="font-size:3rem;">📁</div><h2 style="color:#f1f5f9;">Sol menüden Excel dosyanızı yükleyin</h2><p style="color:#475569;">Her sayfa = 1 hisse kodu</p></div>',unsafe_allow_html=True)
        return
    if st.session_state.selected_stock: show_detail(st.session_state.selected_stock)
    else: show_table()

main()
