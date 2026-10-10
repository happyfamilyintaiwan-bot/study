# -*- coding: utf-8 -*-
# 豐盛工作室剖面插畫（mid-century 配色）。每件新東西是 <g class="it" data-w="N">。

def strips():
    cols = ["#1f4e86", "#c4542a", "#e2a83c", "#2f7a72", "#2a3f73", "#4f7d3a",
            "#8a4f2d", "#b0422f", "#2e6f9e", "#a8452a", "#c98a1e", "#d9932b"]
    out = []
    for i, c in enumerate(cols):
        x = 451 + (i % 4) * 16
        y = 228 + (i // 4) * 22
        out.append(f'<rect class="strip" data-s="{i+1}" x="{x}" y="{y}" width="13" height="18" rx="3" fill="{c}"/>')
    return "".join(out)


def svg(label):
    return f"""<svg class="studio" viewBox="0 0 960 520" role="img" aria-labelledby="studio-t">
<title id="studio-t">{label}</title>
<defs>
 <clipPath id="floorclip"><polygon points="40,470 120,400 840,400 920,470"/></clipPath>
 <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8fbde2"/><stop offset="1" stop-color="#e4f0f8"/></linearGradient>
 <radialGradient id="glow"><stop offset="0" stop-color="#ffe3a3" stop-opacity=".75"/><stop offset="1" stop-color="#ffe3a3" stop-opacity="0"/></radialGradient>
 <linearGradient id="beam" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff2c6" stop-opacity=".7"/><stop offset="1" stop-color="#fff2c6" stop-opacity="0"/></linearGradient>
</defs>
<!-- 房間外殼 -->
<polygon points="40,24 920,24 840,64 120,64" fill="#efe2c8"/>
<polygon points="40,24 120,64 120,400 40,470" fill="#e8d6b6"/>
<polygon points="920,24 840,64 840,400 920,470" fill="#e8d6b6"/>
<rect x="120" y="64" width="720" height="336" fill="#f7eedd"/>
<rect x="120" y="392" width="720" height="8" fill="#e4d2b0"/>
<polygon points="40,470 120,400 840,400 920,470" fill="#d9b483"/>
<g clip-path="url(#floorclip)" stroke="#c49c68" stroke-width="1.5"><line x1="40" y1="418" x2="920" y2="418"/><line x1="40" y1="440" x2="920" y2="440"/><line x1="40" y1="458" x2="920" y2="458"/><line x1="300" y1="400" x2="250" y2="470"/><line x1="480" y1="400" x2="480" y2="470"/><line x1="660" y1="400" x2="710" y2="470"/></g>
<rect x="34" y="470" width="892" height="18" fill="#1b1a17"/>
<polygon points="40,24 920,24 920,470 40,470" fill="none" stroke="#1b1a17" stroke-width="6" stroke-linejoin="round"/>

<!-- W5 星空天窗 -->
<g class="it" data-w="5"><polygon points="432,64 528,64 640,400 320,400" fill="url(#beam)"/><polygon points="416,28 544,28 530,58 430,58" fill="#22305f" stroke="#1b1a17" stroke-width="3"/><circle cx="446" cy="40" r="2" fill="#fff"/><circle cx="470" cy="49" r="1.6" fill="#ffe08a"/><circle cx="498" cy="37" r="2.2" fill="#fff"/><circle cx="521" cy="47" r="1.6" fill="#fff"/><path d="M505 50 l3 -6 l3 6 l-6 -3.5 h6z" fill="#ffe08a"/></g>

<!-- W3 大窗 -->
<g class="it" data-w="3"><rect x="606" y="96" width="180" height="176" rx="4" fill="#8a5a34"/><rect x="618" y="108" width="156" height="152" fill="url(#sky)"/><circle cx="740" cy="140" r="16" fill="#f3c454"/><path d="M618 236 Q660 206 700 226 T774 214 V260 H618Z" fill="#8bb36f"/><path d="M618 250 Q680 232 774 246 V260 H618Z" fill="#6d9a57"/><rect x="644" y="214" width="4" height="22" fill="#6b4a2b"/><circle cx="646" cy="208" r="12" fill="#4f7d3a"/><line x1="696" y1="108" x2="696" y2="260" stroke="#8a5a34" stroke-width="6"/><line x1="618" y1="184" x2="774" y2="184" stroke="#8a5a34" stroke-width="6"/><rect x="598" y="270" width="196" height="10" rx="2" fill="#a8703f"/></g>

<!-- W4 清爽書櫃 -->
<g class="it" data-w="4"><rect x="140" y="112" width="112" height="288" fill="#fbf7ee" stroke="#1b1a17" stroke-width="3"/><g fill="#d9c7a6"><rect x="143" y="180" width="106" height="5"/><rect x="143" y="250" width="106" height="5"/><rect x="143" y="320" width="106" height="5"/></g><g><rect x="152" y="140" width="10" height="40" fill="#1f4e86"/><rect x="163" y="146" width="8" height="34" fill="#e2a83c"/><rect x="172" y="136" width="12" height="44" fill="#c4542a"/><rect x="186" y="150" width="9" height="30" fill="#2f7a72"/><path d="M222 180 l-12 -36 l9 -3 l12 36z" fill="#8a4f2d"/><rect x="152" y="214" width="12" height="36" fill="#2f7a72"/><rect x="166" y="208" width="9" height="42" fill="#1f4e86"/><rect x="177" y="218" width="10" height="32" fill="#e2a83c"/><circle cx="222" cy="236" r="12" fill="#4f7d3a"/><rect x="214" y="236" width="16" height="14" fill="#c4542a"/><rect x="152" y="284" width="40" height="36" fill="#e9dcc3" stroke="#8a5a34" stroke-width="2"/><rect x="200" y="280" width="10" height="40" fill="#c4542a"/><rect x="212" y="286" width="9" height="34" fill="#1f4e86"/><rect x="223" y="290" width="12" height="30" fill="#e2a83c"/><rect x="152" y="352" width="86" height="48" fill="#e2d0ae"/><circle cx="196" cy="376" r="5" fill="#8a5a34"/></g></g>

<!-- W2 圓鏡 -->
<g class="it" data-w="2"><circle cx="318" cy="168" r="42" fill="#d1e2ec" stroke="#e2a83c" stroke-width="9"/><path d="M296 150 l26 -18 M292 170 l40 -28" stroke="#fff" stroke-width="5" stroke-linecap="round"/><line x1="318" y1="116" x2="318" y2="96" stroke="#8a5a34" stroke-width="2"/></g>

<!-- W11 靈感小架 -->
<g class="it" data-w="11"><rect x="276" y="258" width="112" height="8" rx="2" fill="#c98a1e"/><ellipse cx="292" cy="252" rx="11" ry="7" fill="#8f8a84"/><rect x="310" y="230" width="24" height="28" fill="#fff" stroke="#1b1a17" stroke-width="2"/><circle cx="322" cy="242" r="6" fill="#e2a83c"/><path d="M344 258 q8 -34 22 -38 q-4 20 -18 38z" fill="#2f7a72"/><path d="M368 258 v-18 h14 v18z" fill="#c4542a"/><path d="M370 240 q6 -10 2 -16" stroke="#4f7d3a" stroke-width="2" fill="none"/></g>

<!-- W7 唱盤與邊櫃 -->
<g class="it" data-w="7"><rect x="600" y="318" width="196" height="74" rx="4" fill="#a8703f"/><rect x="610" y="328" width="56" height="54" fill="#1f4e86"/><rect x="670" y="328" width="56" height="54" fill="#e2a83c"/><rect x="730" y="328" width="56" height="54" fill="#1f4e86"/><circle cx="660" cy="356" r="2.5" fill="#fff"/><circle cx="736" cy="356" r="2.5" fill="#fff"/><path d="M612 392 l-6 8 M784 392 l6 8" stroke="#6b4a2b" stroke-width="4"/><rect x="620" y="300" width="84" height="18" rx="3" fill="#6b4a2b"/><ellipse cx="656" cy="301" rx="30" ry="6" fill="#1b1a17"/><ellipse cx="656" cy="301" rx="7" ry="2" fill="#c4542a"/><path d="M694 296 l-18 6" stroke="#ddd" stroke-width="2.5" stroke-linecap="round"/><rect x="746" y="282" width="34" height="36" rx="4" fill="#efe6d4" stroke="#1b1a17" stroke-width="2"/><circle cx="763" cy="303" r="9" fill="#1b1a17"/><circle cx="763" cy="290" r="3" fill="#1b1a17"/></g>

<!-- W6 植物角 -->
<g class="it" data-w="6"><path d="M788 400 l6 -48 h42 l6 48z" fill="#c4542a"/><path d="M815 352 C800 320 776 312 760 318 C772 334 792 346 815 352Z" fill="#4f7d3a"/><path d="M815 352 C812 312 824 280 846 268 C850 300 836 330 815 352Z" fill="#3f6e2e"/><path d="M815 352 C830 326 856 318 878 326 C866 344 842 352 815 352Z" fill="#5b8f43"/><path d="M815 352 C796 300 780 270 762 262 C760 296 784 330 815 352Z" fill="#6aa04e"/><line x1="700" y1="64" x2="700" y2="92" stroke="#6b4a2b" stroke-width="2"/><path d="M684 92 h32 l-5 18 h-22z" fill="#e2a83c"/><path d="M690 108 q-6 30 -14 44 M700 110 q2 26 -4 46 M710 108 q8 22 6 36" stroke="#4f7d3a" stroke-width="4" fill="none" stroke-linecap="round"/><circle cx="676" cy="152" r="5" fill="#5b8f43"/><circle cx="696" cy="156" r="5" fill="#5b8f43"/><circle cx="716" cy="144" r="5" fill="#5b8f43"/></g>

<!-- W1 門與歡迎地墊 -->
<g class="it" data-w="1"><polygon points="58,196 104,216 104,416 58,452" fill="#1f4e86" stroke="#1b1a17" stroke-width="3"/><polygon points="66,214 96,228 96,300 66,292" fill="#3a6aa6"/><circle cx="96" cy="330" r="4.5" fill="#e2a83c"/><polygon points="118,446 208,446 196,466 98,466" fill="#c4542a"/><line x1="112" y1="452" x2="204" y2="452" stroke="#e8b48a" stroke-width="2"/><line x1="106" y1="460" x2="200" y2="460" stroke="#e8b48a" stroke-width="2"/></g>

<!-- W10 地毯 -->
<g class="it" data-w="10"><polygon points="236,424 724,424 772,466 188,466" fill="#b5452c"/><polygon points="252,429 708,429 748,461 212,461" fill="none" stroke="#f1c27d" stroke-width="2.5"/><g fill="#f1c27d"><circle cx="330" cy="445" r="4"/><circle cx="420" cy="445" r="4"/><circle cx="540" cy="445" r="4"/><circle cx="630" cy="445" r="4"/></g></g>

<!-- 畫架（一開始就在） -->
<g><line x1="452" y1="214" x2="430" y2="452" stroke="#6b4a2b" stroke-width="6" stroke-linecap="round"/><line x1="522" y1="214" x2="544" y2="452" stroke="#6b4a2b" stroke-width="6" stroke-linecap="round"/><line x1="487" y1="200" x2="487" y2="440" stroke="#6b4a2b" stroke-width="5" stroke-linecap="round"/><rect x="442" y="218" width="90" height="82" rx="2" fill="#ffffff" stroke="#6b4a2b" stroke-width="4"/><rect x="436" y="300" width="102" height="8" rx="2" fill="#8a5a34"/>{strips()}</g>

<!-- W9 扶手椅與毯子 -->
<g class="it" data-w="9"><path d="M206 360 q-4 -42 26 -48 h52 q20 4 18 48z" fill="#1f4e86"/><rect x="196" y="380" width="118" height="30" rx="10" fill="#2e6f9e"/><rect x="190" y="370" width="16" height="44" rx="6" fill="#8a5a34"/><rect x="306" y="370" width="16" height="44" rx="6" fill="#8a5a34"/><path d="M204 414 l-8 46 M310 414 l8 46" stroke="#6b4a2b" stroke-width="5" stroke-linecap="round"/><path d="M262 312 q30 6 38 50 l-14 54 q-10 -30 -30 -42z" fill="#c4542a"/><path d="M272 330 l20 60 M282 322 l18 66" stroke="#e8b48a" stroke-width="2"/></g>

<!-- W8 工作桌 -->
<g class="it" data-w="8"><rect x="596" y="404" width="196" height="12" rx="3" fill="#c58b4e"/><path d="M610 416 l-6 50 M778 416 l6 50 M640 416 l-2 42 M750 416 l2 42" stroke="#8a5a34" stroke-width="5" stroke-linecap="round"/><rect x="622" y="388" width="44" height="16" rx="2" fill="#fbf7ee" stroke="#1b1a17" stroke-width="2"/><rect x="690" y="380" width="16" height="24" rx="3" fill="#1f4e86"/><path d="M706 386 q8 0 8 8 q0 6 -8 6" fill="none" stroke="#1f4e86" stroke-width="3"/><rect x="730" y="376" width="16" height="28" rx="2" fill="#c4542a"/><line x1="734" y1="376" x2="730" y2="360" stroke="#e2a83c" stroke-width="3"/><line x1="742" y1="376" x2="748" y2="358" stroke="#2f7a72" stroke-width="3"/><ellipse cx="700" cy="460" rx="22" ry="5" fill="#1b1a17" opacity=".12"/><rect x="684" y="426" width="34" height="8" rx="3" fill="#2f7a72"/><path d="M690 434 l-4 28 M712 434 l4 28" stroke="#1b1a17" stroke-width="3"/></g>

<!-- W12 中央吊燈 -->
<g class="it" data-w="12"><circle class="lampglow" cx="480" cy="150" r="110" fill="url(#glow)"/><line x1="480" y1="64" x2="480" y2="126" stroke="#1b1a17" stroke-width="2"/><path d="M452 150 q28 -36 56 0z" fill="#d9932b" stroke="#1b1a17" stroke-width="2.5"/><circle cx="480" cy="154" r="7" fill="#fff4c7"/></g>
</svg>"""
