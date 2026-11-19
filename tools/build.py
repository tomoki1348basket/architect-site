#!/usr/bin/env python3
"""Static site generator. usage: build.py OUTDIR [--preview]
--preview : links use .html (for local/preview hosting). Default: clean URLs (Cloudflare Pages)."""
import sys, os, shutil, html, json
OUT = sys.argv[1]; PREVIEW = '--preview' in sys.argv
EXT = '.html' if PREVIEW else ''
SHOW_WORKS = False  # WORKS(自邸)は写真の撮り直し後に True にして公開する
BASE = 'https://tomo-architect.com'
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LINE = 'https://lin.ee/RltCpPb'
tax = lambda p: f'{round(p*1.1):,}'
yen = lambda p: f'{p:,}'
e = html.escape
PFX = ''
def L(slug):
    if slug == '': return PFX + 'index.html' if EXT else (PFX or './')
    return PFX + slug + EXT

# ---------------- content ----------------
ZOOM = dict(slug='zoom-consultation', no='00', en='ZOOM CONSULTATION', name='Zoom相談', area='全国対応', price=15000,
  img='zoom', unit='60分',
  short='家づくりの相談窓口。間取りや内装など、お悩みを60分お話しください。',
  title='Zoom相談|家づくり・間取りのご相談を建築士に(60分)',
  desc='建築士に間取り・内装など家づくりの悩みを60分オンラインで相談できるZoom相談。本申込の場合、相談料は全額充当されます。',
  lead='間取りや内装など、家づくりのお悩みを、建築士に直接ご相談いただけます。',
  fit=['間取りや内装について、建築士の意見を聞いてみたい','住宅会社の提案に、少し不安がある','土地や暮らし方に合う家のかたちを整理したい','設計やデザインの進め方を、一度相談してみたい'],
  points=['オンライン(Zoom)60分','間取り・外観・内装・照明など、家づくり全般のご相談','お手持ちの間取り図・敷地資料・参考画像をもとにご相談'],
  credit='ご相談のあと、間取り添削・間取り作成を正式にお申し込みいただく場合は、相談料を全額、サービス料金に充当します。',
  flow=[['公式LINEでご連絡','「Zoom相談を希望」とお送りください。日程を調整します。'],['ご入金','ご予約確定後、相談料をお振込みいただきます。'],['Zoom相談(60分)','お悩みやご要望を伺い、建築士の視点でアドバイスします。'],['必要に応じてサービスをご案内','ご希望があれば、設計サービスをご案内します。お申し込みは任意です。']],
  fix=None)
REVIEW = dict(slug='floorplan-review', no='01', en='FLOOR PLAN REVIEW', name='間取り添削', area='全国対応', price=50000, img='s2',
  short='提案済みの間取りを、建築士の視点で見直します。',
  title='間取り添削|住宅会社の間取りを建築士がオンラインで改善提案',
  desc='工務店・ハウスメーカーから提案された間取りを、建築士が生活動線・採光・収納・デザインの視点で赤ペン添削。税抜50,000円、全国オンライン対応。',
  lead='現在ご提案されている間取りをもとに、生活動線や空間のつながり、採光、家具の配置、デザイン性など、さまざまな視点から改善点をご提案します。',
  more=['工務店やハウスメーカーから提案された間取りに不安がある方や、より良い間取りを検討したい方に向けたサービスです。'],
  fit=['提案された間取りにしっくりこない','間取りをもっと良くできないか知りたい','別の建築士の意見を聞きたい','住宅会社との打ち合わせ前に改善点を整理したい'],
  points=['現在の間取りの確認・分析','生活動線・収納・採光・デザインの検討','間取り図への赤ペン添削','改善案のご提案','添削資料PDF納品','Zoomでのご説明'],
  deliv='間取り図に赤ペンで添削します。',
  flow=[['お問い合わせ・お申し込み','公式LINEよりお問い合わせいただき、ご依頼内容を確認します。'],['ご入金・資料のご提出','現在の間取り図や参考資料、気になっている点、ご要望などを公式LINEにてお送りいただきます。'],['間取り添削','いただいた資料やご要望をもとに、間取りの改善点や変更案をご提案します。'],['納品・オンライン解説','添削資料をPDFにて納品し、Zoomにて詳しくご説明します。']],
  fix=None)
DESIGN = dict(slug='floorplan-design', no='02', en='FLOOR PLAN DESIGN', name='間取り作成', area='全国対応', price=180000, img='plan',
  short='暮らし方と敷地に合わせて、間取りを一からご提案します。',
  title='間取り作成|建築士が間取り・外観パース・内装パースをオンラインで提案',
  desc='暮らし方・ご要望・敷地条件をもとに、建築士が間取りを一から作成。外観パース・LDK内装パース付き、税抜180,000円、全国オンライン対応。',
  lead='お客様の暮らし方やご要望、敷地条件に合わせて、間取りを一からご提案します。',
  more=['間取りだけでなく、外観や内装とのつながりも意識し、建築とインテリアが調和する空間を目指します。','すでに工務店やハウスメーカーが決まっている方もご利用いただけます。'],
  fit=['間取りを一から考えてほしい','住宅会社からの提案に満足できない','間取りと外観を統一してデザインしたい','内装まで含めて空間全体を考えてほしい','自分たちらしい住まいを実現したい'],
  points=['Zoomによる事前ヒアリング','間取りの新規作成','外観パース作成','LDK内装パース2カット','間取り・デザインの修正2回','図面・パースのPDF納品','Zoomでのご説明','住宅会社からの指摘を踏まえたブラッシュアップ(修正回数内)'],
  deliv='間取り図・外観パース・LDK内装パース(2カット)をPDFで納品します。',
  flow=[['お問い合わせ','公式LINEよりお問い合わせください。'],['ヒアリングシート・資料のご提出','簡単なヒアリングシート(A4用紙1〜2枚程度)へのご回答と、敷地図や参考資料などをご提出いただきます。'],['オンラインヒアリング(Zoom)','暮らし方やご要望、お好みのデザイン、家づくりで大切にされていることなどを詳しくお伺いします。'],['お申し込み・ご入金','ヒアリング後、サービス内容をご確認いただき、正式なお申し込みとご入金をお願いいたします。'],['プラン作成','ヒアリング内容や敷地条件をもとに、お客様の暮らしに合わせたプランを作成します。'],['納品・オンライン解説','作成した資料をPDFにて納品し、Zoomにて間取りやデザインの意図を詳しくご説明します。']],
  fix='修正は、間取り・デザインで合計2回までを基本とします。住宅会社からの指摘を踏まえたブラッシュアップも、この修正回数内で対応します。修正回数を超える変更や大幅な再設計は、別途お見積もりとなる場合があります。')
SUPPORT = dict(slug='design-support', no='03', en='DESIGN SUPPORT', name='設計デザインサポート', area='全国対応', priceText='個別お見積もり', img='mat',
  short='設計・デザインのお悩みに、範囲を決めて柔軟に対応します。',
  title='設計デザインサポート|間取りから内装計画までの伴走サポート',
  desc='間取りから内装計画までの伴走サポート、照明・素材選定など、必要な範囲を組み合わせて建築士がサポート。個別お見積もり、全国オンライン対応。',
  lead='家づくりにおける設計やデザインのお悩みに、ご要望に合わせて柔軟に対応いたします。',
  more=['部分的なデザインのご相談から、住まい全体のトータルデザインまで、お客様一人ひとりに合わせたサポートをご提案します。'],
  fit=['照明や内装など、一部分だけ相談したい','複数の項目をまとめて任せたい','家づくりの進行に合わせて継続的に相談したい'],
  chips=['間取りから内装までの伴走','内装・インテリア','照明','素材・設備','継続サポート'],
  points=['外観デザインの改善提案','内装・インテリアデザイン','照明計画・照明添削','素材や住宅設備の選定','家づくりの進捗に合わせた伴走サポート'],
  pointsTitle='サポート内容例',
  extra=['上記は一例であり、ご要望に合わせて必要なサポートを柔軟に組み合わせることができます。','サポート内容・期間・費用については、ご相談内容に応じて個別にご提案いたします。'],
  quote=['料金は個別お見積もりです。ご相談内容やご希望のサポート範囲に応じて、お見積もりいたします。','業務範囲・納品物・修正回数・対応期間は、ご依頼内容に応じて決定します。','まずは公式LINEよりお気軽にご相談ください。'],
  flow=[['お問い合わせ','公式LINEより、ご相談内容やご希望のサポート内容をお聞かせください。'],['資料のご提出・オンラインヒアリング(Zoom)','必要な資料をご提出いただき、現在の家づくりの状況やお悩み、ご要望などを詳しくお伺いします。'],['お見積もり','ヒアリング内容をもとに、サポート範囲や料金をご提案します。'],['お申し込み・ご入金','お見積もり内容をご確認いただき、正式なお申し込みとご入金をお願いいたします。'],['デザイン提案','ご依頼内容に合わせたデザインをご提案します。'],['納品・オンライン解説','Zoomにてご提案内容やデザインの意図を詳しくご説明します。継続的なサポートの場合は、ご契約内容に応じて進めていきます。']],
  fix='修正回数は、ご依頼内容に応じてお見積もり時にご案内します。')
FULL = dict(slug='full-support', no='03', en='TOTAL HOME DESIGN', name='家づくりフルサポート', area='徳島県内限定', priceText='Zoomでご案内', img='ext',
  short='所属工務店と連携し、お家の完成までを一貫してサポートします。',
  title='家づくりフルサポート|徳島県内で建築士と工務店が連携して家づくり',
  desc='徳島県内限定。建築士が所属工務店と連携し、間取り・外観・内装・照明まで一貫したデザインでお家の完成までサポートします。',
  lead='これから徳島県内で家づくりを検討されている方に向けたサービスです。',
  more=['所属する工務店と連携し、間取り・外観・内装・照明まで一貫性のあるデザインをご提案し、お家の完成までサポートいたします。','建築とインテリアをひとつのデザインとして考え、お客様にとって一番お気に入りの空間となる住まいを目指します。'],
  fit=['徳島県内で家づくりを検討している','設計から完成まで一貫して任せたい','デザインにこだわった家をつくりたい'],
  points=['間取り・外観・内装・照明まで、一貫性のあるデザイン提案','所属する工務店と連携し、お家の完成までサポート'],
  pointsTitle='サービスの特徴',
  extra=['全国対応のオンラインサービスとは異なり、所属する工務店と連携して、お家の完成までサポートするサービスです。'],
  notes=['本サービスは、所属工務店と連携して提供するものです。施工・工事は工務店が担当します。','全国対応のオンラインサービスとは異なり、徳島県内限定のサービスです。'],
  flow=[['お問い合わせ','公式LINEからお問い合わせください。'],['オンライン相談(Zoom)','お問い合わせいただいた後、オンライン相談(Zoom)にて詳細をご案内いたします。']],
  fix=None, btn='家づくりについて相談する')
SERVICES = [ZOOM, REVIEW, DESIGN, FULL]

CONCEPT = dict(catch='引き算から生まれる、空間の美しさ。', paras=['自分たちが暮らす家が、どこよりもお気に入りの空間であってほしい。','そんな想いを大切に、一人ひとりの暮らし方や価値観に耳を傾けながら、その人らしい暮らしを提案しています。','建築とインテリアを分けず、空間全体をひとつのデザインとして考える。','余計な装飾を加えるのではなく、光の入り方や素材の質感、細部の納まりを大切に、時を重ねても愛着の深まる暮らしを目指しています。'])
THEMES = [
 ('01','空間構成とつながり',['hero'],['建物の内と外を別々に考えるのではなく、ひとつの空間として設計する。','天井や軒先、窓のラインを丁寧にそろえることで、視線が自然と外へ抜け、空間に広がりが生まれます。','中庭や植栽も室内との関係から計画し、建築全体に統一感を持たせます。']),
 ('02','素材とディテール',['m1','m2'],['美しい空間をつくるために、必ずしも多くの装飾は必要ありません。','木、塗り壁、タイルなど、素材そのものの質感を大切にし、色数や素材の切り替えを抑える。','巾木や建具の枠、壁と天井の取り合いなど、細部の納まりまで丁寧に整えることで、シンプルでありながら奥行きのある空間を目指します。']),
 ('03','光と陰影',['contact'],['照明は、空間全体を均一に明るくするためだけのものではないと考えています。','塗り壁の質感を引き立てる間接照明、植栽やアートを照らすスポットライト、家具やテーブルを美しく見せる光。','何を照らし、何を照らさないか。','光と影のバランスを考え、昼と夜で異なる表情を楽しめる空間を設計します。']),
 ('04','家具とインテリア',['d3'],['建物が完成したときではなく、家具が入り、暮らしが始まったときの美しさまで考える。','ソファやダイニングテーブルの配置、家具の高さや素材、アートや小物とのバランス。','必要に応じて具体的な家具やメーカー・品番まで選定し、建築とインテリアが自然に調和する空間を目指します。']),
 ('05','建築と自然',['m3','m4'],['庭や植栽は、建築を完成させる大切な要素のひとつです。','室内から見える樹木の位置、窓から切り取る景色、季節によって変化する光と影。','建物と庭を一体で考え、自然を身近に感じられる住まいをつくります。']),
]
APPROACH = {'title':'デザインにこだわった家づくりを、もっと身近に。','paras':['建築家や設計事務所に住宅の設計・監理を依頼する場合、工事費の8〜10%程度、あるいはそれ以上の設計監理料が必要となるケースがあります。','例えば建築工事費3,000万円の場合、8〜10%で約240〜300万円。','一般的な設計事務所では、デザイン提案だけでなく、実施設計・各種申請・工事監理なども担当します。','一方、私のサービスでは、間取り・外観・インテリアのデザイン提案に業務を絞り、{P}円(税抜)でご提供しています。','実施設計・構造計算・建築確認申請・工事監理などは、お客様が選ばれた住宅会社にご担当いただく形です。','それぞれの役割を分担することで、デザインにこだわった住まいづくりを、より身近な形でサポートします。'],'note':'※設計監理料の割合は一例です。一般的な設計監理サービスとは業務範囲が異なり、住宅会社側で別途費用が必要になる場合があります。'}
ABOUT = ['家づくりは、単に間取りを決めることではなく、「その土地で、どんな暮らしをしたいか」を考えることだと思っています。','建築士として、敷地の特性や暮らし方を丁寧に読み解き、デザインと暮らしやすさのバランスがとれた空間をご提案します。','私自身も自邸を設計し、日々の暮らしを通して、設計段階では気づかなかった発見や学びがあります。','建築士としての知識や経験だけでなく、実際に暮らしているからこそ感じることも、皆さまの家づくりにお伝えできればと思っています。']
FAQ = [
 ('対応エリアは?','オンラインで全国対応しています。徳島県内の方には、所属工務店と連携した家づくりのサポートも、オンライン相談でご案内します。'),
 ('住宅会社が決まっていなくても相談できますか?','はい。まずは公式LINEからご相談ください。'),
 ('Zoom相談の料金は、その後のサービスに充当されますか?','間取り添削・間取り作成を正式にお申し込みいただく場合、Zoom相談料(60分)は全額充当されます。Zoom相談を経ずに、各サービスへ直接お申し込みいただくことも可能です。'),
 ('提案を住宅会社でそのまま採用できますか?','住宅会社によって、外部設計者の提案を採用できない場合があります。事前に住宅会社へご確認ください。'),
 ('現地調査はありますか?','現地調査は行いません。ご提供いただく敷地資料・現地写真・ご要望などをもとに提案します。'),
 ('上記以外の設計やデザインの相談もできますか?','内装や照明など、ご要望に応じた個別のご相談にも対応できます。内容に応じて、別途お見積もりをご案内します。まずは公式LINEよりご相談ください。'),
 ('構造計算や申請、工事監理もお願いできますか?','構造計算・建築確認申請・実施設計・工事監理は含みません。お客様が選ばれた住宅会社にご確認ください。'),
 ('支払いはいつですか?','具体的な設計・デザイン提案は、ご入金確認後に開始します。間取り作成は、ご入金前にZoomでヒアリングを行い、内容をご確認いただいてから、正式なお申し込みをお願いします。間取り添削は、ご入金のあと資料をお送りいただきます。'),
 ('修正回数を超える場合は?','修正回数を超える変更や大幅な再設計は、別途お見積もりとなる場合があります。'),
]
NOTICE = ['本サービスはオンラインでの提案です。','現地調査は含みません。','提案内容の実現可能性は、住宅会社による確認が必要です。','構造計算・建築確認申請・実施設計・工事監理は含みません。','住宅会社の施工ルールや予算によって、変更が必要になる場合があります。','修正回数を超える変更や大幅な再設計は、別途お見積もりとなる場合があります。','お客様からご提供いただいた資料をもとに検討します。']
NOTES = ['料金は税抜価格です。税込価格(10%)も併記しています。','制作開始前にお振込みをお願いしております。','著作権は当方に帰属します。事例として公開する場合は事前に許可をいただきます。']

# ---------------- helpers ----------------
def price_html(s, big=False):
    if 'price' in s:
        u = f'<span class="u">/{s["unit"]}</span>' if s.get('unit') else ''
        return f'<span class="pr"><b>{yen(s["price"])}</b>円{u}<small>(税抜)・税込{tax(s["price"])}円</small></span>'
    return f'<span class="pr"><b class="t">{s["priceText"]}</b></span>'
def ul(items, cls=''): return f'<ul class="{cls}">' + ''.join(f'<li>{e(i)}</li>' for i in items) + '</ul>'
def ps(items): return ''.join(f'<p>{e(p)}</p>' for p in items)
def img(k, alt='', cls='', lazy=True, w=None, h=None):
    return f'<img src="{PFX}img/{k}.jpg" alt="{e(alt)}" class="{cls}"{" loading=lazy" if lazy else ""} decoding="async">'
def line_btn(label='公式LINEで相談する', cls='btn'):
    return f'<a class="{cls}" href="{LINE}" target="_blank" rel="noopener"><span>{label}</span><i aria-hidden="true">→</i></a>'
def sec(id_, en, ja, body, cls=''):
    return f'<section id="{id_}" class="sec {cls}"><div class="wrap"><header class="sh"><span class="en">{en}</span><h2>{ja}</h2></header>{body}</div></section>'

NAV = [('concept','考え方','/#concept'),('services','サービス','/#services'),('profile','プロフィール','/#profile'),('faq','よくある質問','/#faq'),('contact','お問い合わせ','/#contact')]
if SHOW_WORKS: NAV.insert(2, ('works','設計事例','/#works'))
def navlink(a): return (L('') + a[2][1:]) if a[2].startswith('/#') else a[2]

def head(title, desc, path, ogimg='ogp.jpg', jsonld=None, noindex=False):
    url = BASE + ('/' if path == '' else '/' + path)
    ld = ''.join(f'<script type="application/ld+json">{json.dumps(j, ensure_ascii=False)}</script>' for j in (jsonld or []))
    return f'''<!doctype html><html lang="ja"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{e(title)}</title><meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#f3efe9">
<meta property="og:type" content="website"><meta property="og:site_name" content="宇山朋希 建築士"><meta property="og:locale" content="ja_JP">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}/{ogimg}"><meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+JP:wght@400;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{PFX}assets/style.css">{ld}</head>'''

def header(home=False):
    links = ''.join(f'<a href="{navlink(a)}">{a[1]}</a>' for a in NAV)
    return f'''<body><a class="skip" href="#main">本文へ</a>
<header class="hd{' hd-home' if home else ''}" id="hd"><div class="wrap hdin">
<a class="logo" href="{L('')}"><span>宇山 朋希 <i>/</i> 建築士</span></a>
<nav class="pcnav" aria-label="メイン">{links}</nav>
<button class="mb" id="mb" aria-expanded="false" aria-controls="drawer"><b>MENU</b></button></div></header>
<div class="drawer" id="drawer" hidden><nav aria-label="メニュー">{''.join(f'<a href="{navlink(a)}">{a[1]}</a>' for a in NAV)}
<div class="dsv"><span class="en">SERVICES</span>{''.join(f'<a href="{L(s["slug"])}">{s["name"]}</a>' for s in SERVICES)}</div></nav>
{line_btn()}</div>'''

def footer():
    WORKS_FT = f'<a href="{L("works/jitei")}">設計事例 自邸</a>' if SHOW_WORKS else ''
    sv = ''.join(f'<a href="{L(s["slug"])}">{s["name"]}</a>' for s in SERVICES)
    return f'''<footer class="ft"><div class="wrap"><div class="ftg"><div><div class="logo"><span>宇山 朋希 <i>/</i> 建築士</span></div><p class="ftp">間取り・外観・照明まで、心地よく、美しい住まいを。</p></div>
<div class="ftl"><span class="en">SERVICES</span>{sv}{WORKS_FT}</div></div>
<p class="copy">© 宇山 朋希 / Tomoki Uyama Architect</p></div></footer>
<div class="fab"><a href="{LINE}" target="_blank" rel="noopener"><span>公式LINEで相談する</span></a></div>
<script>(function(){{var b=document.getElementById('mb'),d=document.getElementById('drawer');if(!b)return;
function t(o){{b.setAttribute('aria-expanded',o);d.hidden=!o;document.body.classList.toggle('lock',o)}}
b.onclick=function(){{t(b.getAttribute('aria-expanded')!=='true')}};d.addEventListener('click',function(e){{if(e.target.tagName==='A')t(false)}});
var h=document.getElementById('hd');function s(){{h.classList.toggle('on',window.scrollY>40)}};s();addEventListener('scroll',s,{{passive:true}});}})();</script></body></html>'''

def crumbs(items):  # items: [(name, path)]
    return {'@context':'https://schema.org','@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':i+1,'name':n,'item':BASE+('/' if p=='' else '/'+p)} for i,(n,p) in enumerate(items)]}
ORG = {'@context':'https://schema.org','@type':'ProfessionalService','name':'宇山朋希 建築士','url':BASE+'/','image':BASE+'/ogp.jpg','description':'オンラインで全国対応。間取り相談・間取り添削・間取り作成。徳島県内は家づくりフルサポート。','areaServed':'JP','founder':{'@type':'Person','name':'宇山 朋希','jobTitle':'建築士'},'sameAs':[LINE]}

# ---------------- pages ----------------
pages = {}

def service_cards(lst):
    out = ''
    for s in lst:
        loc = s["area"].startswith("徳島")
        z = s['slug'] == 'zoom-consultation'
        out += f'''<a class="sc{' sc-z' if z else ''}" href="{L(s['slug'])}"><span class="scbg">{img(s['img'], s['name'])}</span>
<span class="scin"><span class="sce">{s['no']} | {s['en']}</span><b>{s['name']}</b>
<span class="scm"><span class="tag{' loc' if loc else ''}">{s['area']}</span>{('<span class="tag">家づくりの相談窓口</span>' if z else '')}</span>
<span class="scd">{e(s['short'])}</span>{price_html(s)}<span class="pill">詳細を見る</span></span></a>'''
    return out

def top():
    hero = f'''<section class="hero"><div class="heroimg">{img('hero','',lazy=False)}</div><div class="heroin wrap">
<p class="eyebrow">ARCHITECT / UYAMA TOMOKI</p><h1>理想の暮らしを、<br>建築士と一緒に。</h1>
<p class="herosub">間取り・外観・照明まで、<br>心地よく、美しい住まいをご提案します。</p>
<a class="btn btn-w" href="#services"><span>サービスを見る</span><i aria-hidden="true">↓</i></a></div></section>'''
    concept = sec('concept','DESIGN CONCEPT','デザインの考え方', f'''<div class="ctx"><p class="lead">{CONCEPT['catch']}</p>{ps(CONCEPT['paras'])}</div>''')
    services = sec('services','SERVICE','サービス・料金一覧', f'''<p class="intro">まずはZoom相談で、家づくりのお悩みをお聞かせください。各サービスへ直接お申し込みいただくことも可能です。</p>
<div class="sgrp"><div class="sgh"><h3>オンライン設計サービス</h3><span class="tag">全国対応</span></div><p class="sgd">ご自宅にいながら、Zoomと公式LINEで、建築士に相談・ご依頼いただけます。</p>
<div class="scl">{service_cards([ZOOM, REVIEW, DESIGN])}</div>
<p class="indiv">上記のほか、内装や照明など、ご要望に応じた個別のご相談にも対応します。内容に応じて、別途お見積もりをご案内します。</p></div>
<div class="sgrp"><div class="sgh"><h3>家づくりフルサポート</h3><span class="tag loc">徳島県内</span></div><p class="sgd">設計から完成まで、一貫してサポートします。</p>
<div class="scl">{service_cards([FULL])}</div></div>
<p class="svnote">料金は税抜表示、税込を併記しています。Zoom相談料は、間取り添削・間取り作成の本申込時に全額充当されます。</p>''', 'tint')
    works = sec('works','WORKS','設計事例', f'''<a class="wk" href="{L('works/jitei')}"><span class="wkimg">{img('w-ext','自邸の外観')}</span>
<span class="wkstrip"><span>{img('w-d2','自邸 昼の室内')}</span><span>{img('w-n4','自邸 夜の室内')}</span></span>
<span class="wkt"><b>自邸</b><small>中庭のある住まい</small></span><span class="pill pill-d">詳しく見る</span></a>''')
    profile = sec('profile','ABOUT','私について', f'''<div class="pf"><div class="pimg">{img('about','宇山朋希')}</div><div class="ptx"><span class="role">建築士</span><p class="name">宇山 朋希</p><span class="rom">Tomoki Uyama</span><span class="org" aria-hidden="true"></span><p class="lead">その土地で、どんな暮らしをしたいか。</p>{ps(ABOUT)}</div></div>''')
    faq = sec('faq','FAQ','よくある質問', '<div class="faq">' + ''.join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q,a in FAQ) + '</div>' + f'<div class="notice"><b>ご利用にあたって</b>{ul(NOTICE)}{ul(NOTES,"notes")}</div>', 'tint')
    contact = f'''<section id="contact" class="sec contact"><div class="cbg">{img('s2','')}</div><div class="wrap cin"><span class="en">CONTACT</span><h2>まずは、公式LINEから。</h2>
<p>ご相談・ご質問だけでも大丈夫です。<br>住宅会社が決まっていなくても、お気軽にご連絡ください。</p>{line_btn('公式LINEで相談する','btn btn-w')}<small>お返事は順次、LINEにてご連絡します。</small></div></section>'''
    body = header(True) + f'<main id="main">{hero}{concept}{services}{works if SHOW_WORKS else ''}{profile}{faq}{contact}</main>' + footer()
    jl = [ORG]
    return head('間取り相談・間取り添削をオンラインで|建築士 宇山朋希','建築士・宇山朋希による、オンライン(全国対応)の間取り相談・間取り添削・間取り作成。Zoom相談から、公式LINEで気軽にご相談いただけます。','',jsonld=jl) + body
pages['index'] = top()

def service_page(s):
    z = s['slug'] == 'zoom-consultation'
    tag = f'<span class="tag{" loc" if s["area"].startswith("徳島") else ""}">{s["area"]}</span>'
    h = f'''<section class="phero"><div class="wrap pheroin"><nav class="bc" aria-label="パンくず"><a href="{L('')}">TOP</a> / <a href="{L('')}#services">サービス</a> / {s['name']}</nav>
<p class="eyebrow">{s['en']}</p><h1>{s['name']}{tag}</h1>
<div class="pbox">{price_html(s)}</div></div></section>'''
    b = ''
    b += f'<div class="blk"><h3>こんな方に</h3>{ul(s["fit"],"chk")}</div>'
    if s['slug']=='floorplan-design': b += '<div class="blk approach"><h3>'+APPROACH['title']+'</h3>'+ps([x.replace('{P}',yen(s['price'])) for x in APPROACH['paras']])+'<p class="sm">'+APPROACH['note']+'</p></div>'
    if z: b += f'<div class="blk"><h3>相談料の充当について</h3><p>{e(s["credit"])}</p><p class="sm">Zoom相談を経ずに、各サービスへ直接お申し込みいただくことも可能です。</p></div>'
    if s.get('chips'): b += f'<div class="blk"><h3>対応できること</h3><div class="chips">{"".join(f"<span>{c}</span>" for c in s["chips"])}</div><p class="sm">必要な項目を、自由に組み合わせられます。</p></div>'
    b += f'<div class="blk"><h3>{s.get("pointsTitle","サービス内容")}</h3>{ul(s["points"],"dot")}</div>'
    if s.get('extra'): b += f'<div class="blk">{ps(s["extra"])}</div>'
    if s.get('deliv'): b += f'<div class="blk"><h3>納品物</h3><p>{e(s["deliv"])}</p></div>'
    if s['slug']=='floorplan-design':
        sm=[('d-plan','間取り図','間取り図'),('d-ext','外観パース','外観パース'),('d-in1','LDK内装パース①','LDK内装パース 1カット目'),('d-in2','LDK内装パース②','LDK内装パース 2カット目')]
        b += '<div class="blk"><h3>納品イメージ</h3><div class="smp">' + ''.join(f'<figure><img src="img/{k}.jpg" alt="{a}" loading="lazy" decoding="async"><figcaption>{c}</figcaption></figure>' for k,c,a in sm) + '</div><p class="sm">※納品物のイメージです。実際の内容は、お客様のご要望や敷地条件に合わせて作成します。</p></div>'
    if s.get('quote'): b += f'<div class="blk"><h3>料金について</h3>{ps(s["quote"])}</div>'
    if s.get('notes'): b += f'<div class="blk"><h3>ご確認ください</h3>{ul(s["notes"],"dot")}</div>'
    b += '<div class="blk"><h3>ご利用の流れ</h3><ol class="flow">' + ''.join(f'<li><b>{e(t)}</b><span>{e(d)}</span></li>' for t,d in s['flow']) + '</ol></div>'
    if s.get('fix'): b += f'<div class="blk"><h3>修正について</h3><p>{e(s["fix"])}</p></div>'
    if 'price' in s and not z: b += f'<p class="sm">料金は税抜{yen(s["price"])}円(税込{tax(s["price"])}円)です。制作開始前にお振込みをお願いしております。</p>'
    cta = f'<div class="cta">{line_btn(s.get("btn","このサービスについて相談する"),"btn btn-w")}</div>'
    others = '<div class="others"><span class="en">OTHER SERVICES</span><div class="svl">' + ''.join(
        f'''<a class="sv" href="{L(o['slug'])}"><span class="svn">{o['no']}</span><span class="svb"><span class="svt"><b>{o['name']}</b></span>{price_html(o)}</span><i class="arw">→</i></a>''' for o in SERVICES if o is not s) + '</div></div>'
    main = f'<main id="main">{h}<section class="sec"><div class="wrap narrow">{b}</div></section><section class="sec cta-sec"><div class="wrap narrow">{cta}</div></section><section class="sec tint"><div class="wrap narrow">{others}</div></section></main>'
    svc = {'@context':'https://schema.org','@type':'Service','name':s['name'],'description':s['desc'],'provider':{'@type':'ProfessionalService','name':'宇山朋希 建築士','url':BASE+'/'},'areaServed':'徳島県' if '徳島' in s['area'] else 'JP','url':BASE+'/'+s['slug']}
    if 'price' in s: svc['offers']={'@type':'Offer','price':str(s['price']),'priceCurrency':'JPY'}
    return head(s['title'], s['desc'], s['slug'], jsonld=[svc, crumbs([('TOP',''),(s['name'],s['slug'])])]) + header() + main + footer()
for s in SERVICES: pages[s['slug']] = service_page(s)

def work_page():
    global PFX
    PFX = '../'
    sec_g = lambda en, ja, keys: f'<div class="wg"><header class="sh"><span class="en">{en}</span><h2>{ja}</h2></header><div class="gal">' + ''.join(f'<figure>{img(k, "自邸 "+ja)}</figure>' for k in keys) + '</div></div>'
    main = f'''<main id="main" class="mwork"><section class="phero"><div class="wrap pheroin"><nav class="bc" aria-label="パンくず"><a href="{L('')}">TOP</a> / <a href="{L('')}#works">設計事例</a> / 自邸</nav>
<p class="eyebrow">WORKS</p><h1>自邸</h1><p class="lead">木の天井、塗り壁、大判タイルと間接照明。中庭を囲んで、空間がつながる住まいです。</p>
<dl class="spec"><div><dt>用途</dt><dd>専用住宅(自邸)</dd></div><div><dt>設計</dt><dd>宇山 朋希</dd></div></dl></div></section>
<section class="sec wsec"><div class="wrap">{sec_g('EXTERIOR','外観',['w-ext'])}{sec_g('DAY','昼の室内',['w-d1','w-d2','w-d3','w-d4','w-d5','w-d6','w-d7'])}{sec_g('NIGHT','夜の室内',['w-n1','w-n2','w-n3','w-n4','w-n5'])}</div></section>
<section class="sec cta-sec"><div class="wrap narrow"><div class="cta">{line_btn('公式LINEで相談する','btn btn-w')}</div></div></section></main>'''
    out = head('自邸|設計事例|建築士 宇山朋希','建築士・宇山朋希が設計した自邸。木の天井、塗り壁、大判タイル、間接照明で構成した、中庭のある住まいの設計事例。','works/jitei',ogimg='img/w-ext.jpg',jsonld=[crumbs([('TOP',''),('設計事例','#works'),('自邸','works/jitei')])]) + header() + main + footer()
    PFX = ''
    return out
if SHOW_WORKS: pages['works/jitei'] = work_page()

def design_page():
    blocks = ''
    for no,t,imgs,paras in THEMES:
        im = ''.join(img(k,t) for k in imgs)
        blocks += f'<article class="theme"><div class="tim n{len(imgs)}">{im}</div><div class="tx"><span class="tn">{no}</span><h3>{t}</h3>{ps(paras)}</div></article>'
    main = f'''<main id="main"><section class="phero"><div class="wrap pheroin"><nav class="bc"><a href="{L('')}">TOP</a> / デザインの考え方</nav><p class="eyebrow">DESIGN CONCEPT</p><h1>{CONCEPT['catch']}</h1>{ps(CONCEPT['paras'])}</div></section>
<section class="sec"><div class="wrap">{blocks}</div></section><section class="sec cta-sec"><div class="wrap narrow"><div class="cta">{line_btn('公式LINEで相談する','btn btn-w')}</div></div></section></main>'''
    return head('デザインの考え方|引き算から生まれる空間の美しさ|建築士 宇山朋希','空間構成、素材とディテール、光と陰影、家具とインテリア、建築と自然。建築士・宇山朋希が大切にしているデザインの考え方。','design',jsonld=[crumbs([('TOP',''),('デザインの考え方','design')])]) + header() + main + footer()

# ---------------- write ----------------
shutil.rmtree(OUT, ignore_errors=True); os.makedirs(OUT + '/assets')
shutil.copytree(ROOT + '/img', OUT + '/img')
shutil.copy(ROOT + '/assets/style.css', OUT + '/assets/style.css')
for f in ('ogp.jpg','robots.txt'): shutil.copy(ROOT + '/' + f, OUT + '/' + f)
for k, v in pages.items():
    os.makedirs(os.path.dirname(f'{OUT}/{k}.html'), exist_ok=True)
    open(f'{OUT}/{k}.html', 'w', encoding='utf8').write(v)
open(OUT + '/_redirects', 'w').write('/design-support / 301\n')
urls = [''] + [s['slug'] for s in SERVICES] + (['works/jitei'] if SHOW_WORKS else []) 
open(OUT + '/sitemap.xml','w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'<url><loc>{BASE}/{u}</loc></url>\n' for u in urls) + '</urlset>\n')
print('ok', len(pages), 'pages')
