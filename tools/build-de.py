"""Write de/index.html from index.html.

The two language versions are two documents, not one document with a
switch, so they have to be kept in step. This script is how: it replaces
known English passages with their German counterparts and fails loudly on
any passage it no longer finds. An edit to index.html therefore surfaces
here as a failed assertion naming the passage that changed, instead of
silently leaving the German page a version behind.

The framework figure is not translated here. Its German labels are the
ones settled for img/de/ in the book repository, and are looked up in
tools/svg-i18n/de.json there.

    python3 tools/build-de.py
"""

import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
DEJSON = os.path.join(SITE, '..', 'agentic-ai', 'tools', 'svg-i18n', 'de.json')
FIGURE = 'ai-agent-framework-v2.svg|'

src = open(os.path.join(SITE, 'index.html'), encoding='utf-8').read()
out = src


def swap(old, new, n=1):
    global out
    c = out.count(old)
    assert c == n, 'found %d occurrences (expected %d) of %.80r' % (c, n, old)
    out = out.replace(old, new)


def inner(tag_open, new_inner, close):
    """Replace the content between a unique opening tag and its close."""
    global out
    a = out.index(tag_open) + len(tag_open)
    b = out.index(close, a)
    out = out[:a] + new_inner + out[b:]


# --------------------------------------------------------------- the figure
tr = json.load(open(DEJSON, encoding='utf-8'))
a = src.index('<svg class="framework"')
b = src.index('</svg>', a) + 6
missing = []


def sub_text(m):
    tag, attrs, body = m.group(1), m.group(2), m.group(3)
    plain = ' '.join(re.sub(r'<[^>]+>', '', body).replace('&amp;', '&').split())
    de = tr.get(FIGURE + plain, tr.get(plain))
    if de is None:
        missing.append(plain)
        return m.group(0)
    return '<%s%s>%s</%s>' % (tag, attrs, de.replace('&', '&amp;'), tag)


svg_de = re.sub(r'<(text|title|desc)(\b[^>]*)>(.*?)</\1>', sub_text,
                src[a:b], flags=re.S)
assert not missing, 'no German label for: %s' % missing
swap(src[a:b], svg_de)

# ---------------------------------------------------------------- the shell
swap('<html lang="en">', '<html lang="de">')
swap('content="A book by Michael Bücker and Michael Hewing on building '
     'LLM-based agents an organization can run, audit, and maintain. '
     'Springer Nature, hardcover 24 February 2027."',
     'content="Ein Buch von Michael Bücker und Michael Hewing über '
     'LLM-basierte Agenten, die eine Organisation betreiben, prüfen und '
     'warten kann. Springer Nature, Hardcover am 24. Februar 2027."')
swap('<meta property="og:description" content="Getting useful output from a '
     'language model is easy. Building a system around one that an '
     'organization can run, audit, and maintain is not.">',
     '<meta property="og:description" content="Aus einem Sprachmodell etwas '
     'Brauchbares herauszuholen ist einfach. Ein System darum herum zu '
     'bauen, das eine Organisation betreiben, prüfen und warten kann, ist '
     'es nicht.">')
swap('<meta property="og:url" content="https://aiagentsbook.org/">',
     '<meta property="og:url" content="https://aiagentsbook.org/de/">\n'
     '<meta property="og:locale" content="de_DE">')
swap('<link rel="canonical" href="https://aiagentsbook.org/">',
     '<link rel="canonical" href="https://aiagentsbook.org/de/">')
for a_, b_ in (('href="favicon.svg"', 'href="../favicon.svg"'),
               ('href="apple-touch-icon.png"', 'href="../apple-touch-icon.png"'),
               ('href="fonts/source-serif-4.woff2"',
                'href="../fonts/source-serif-4.woff2"'),
               ('href="style.css"', 'href="../style.css"'),
               ('src="img/cover-3d.webp"', 'src="../img/cover-3d.webp"'),
               ('src="img/buecker.webp"', 'src="../img/buecker.webp"'),
               ('src="img/hewing.webp"', 'src="../img/hewing.webp"'),
               ('href="imprint.html"', 'href="../imprint.html"'),
               ('href="privacy.html"', 'href="../privacy.html"')):
    swap(a_, b_)

# -------------------------------------------------------------- navigation
swap('<a class="lang" href="de/" hreflang="de" lang="de">'
     '<span class="lang-full">Deutsch</span>'
     '<span class="lang-abbr">DE</span></a>',
     '<a class="lang" href="../" hreflang="en" lang="en">'
     '<span class="lang-full">English</span>'
     '<span class="lang-abbr">EN</span></a>')
swap('<li><a href="#about">About</a></li>',
     '<li><a href="#about">Das Buch</a></li>')
swap('<li><a href="#contents">Contents</a></li>',
     '<li><a href="#contents">Inhalt</a></li>')
swap('<li><a href="#audience">Who it is for</a></li>',
     '<li><a href="#audience">Für wen</a></li>')
swap('<li><a href="#readers">Readers</a></li>',
     '<li><a href="#readers">Stimmen</a></li>')
swap('<li><a href="#authors">Authors</a></li>',
     '<li><a href="#authors">Autoren</a></li>')
swap('<li><a href="#material">Material</a></li>',
     '<li><a href="#material">Material</a></li>')
# Shorter than the English labels on purpose: the German words are longer,
# and the topbar is tightest exactly where they would cost the most.
swap('<span data-when="light">Dark mode</span><span data-when="dark">Light mode</span>',
     '<span data-when="light">Dunkel</span><span data-when="dark">Hell</span>')
swap('current() === "dark" ? "Switch to light mode" : "Switch to dark mode"',
     'current() === "dark" ? "Zum Hellmodus wechseln" : "Zum Dunkelmodus wechseln"')

# -------------------------------------------------------------------- hero
swap('''      <p class="eyebrow">Springer Nature
        <span aria-hidden="true">&middot;</span> Hardcover 24 February 2027</p>''',
     '''      <!-- The page is German, the book is not. Saying so in the eyebrow puts
           it where nobody can miss it, rather than in a note further down. -->
      <p class="eyebrow">Springer Nature
        <span aria-hidden="true">&middot;</span> Hardcover am 24. Februar 2027
        <span aria-hidden="true">&middot;</span> englischsprachig</p>''')
swap('<p class="foreword-by">With a foreword by Jan vom Brocke, University of Münster</p>',
     '<p class="foreword-by">Mit einem Vorwort von Jan vom Brocke, Universität Münster</p>')
swap('''      <p class="lede">Getting useful output from a language model is easy. Building a
        system around one that an organization can run, audit, and maintain is not.
        This book is about the distance between those two things.</p>''',
     '''      <p class="lede">Aus einem Sprachmodell etwas Brauchbares herauszuholen ist
        einfach. Ein System darum herum zu bauen, das eine Organisation betreiben,
        prüfen und warten kann, ist es nicht. Von dem Abstand zwischen beidem
        handelt dieses Buch.</p>''')
swap('>At Springer Nature</a>', '>Bei Springer Nature</a>')
swap('''        <span class="preorder">Pre-order at''',
     '''        <span class="preorder">Vorbestellen bei''')
swap('''<a href="https://www.thalia.de/shop/home/artikeldetails/A1082389863">Thalia</a> or''',
     '''<a href="https://www.thalia.de/shop/home/artikeldetails/A1082389863">Thalia</a> oder''')
swap('alt="AI Agents: Designing, Orchestrating, and Governing LLM-Based Systems, '
     'by Michael Bücker and Michael Hewing, published by Springer."',
     'alt="AI Agents: Designing, Orchestrating, and Governing LLM-Based Systems '
     'von Michael Bücker und Michael Hewing, erschienen bei Springer."')

# ------------------------------------------------------------------- prose
# Keyed by a hash of the English passage rather than by the passage itself,
# so a rewrite upstream fails here by name instead of passing unnoticed.
import hashlib

BLOCK = re.compile(r'<(p|h2|h3|figcaption|blockquote)(\b[^>]*)>(.*?)</\1>',
                   re.S)

# Quotations are left in the language they were given in. Translating what a
# named person said, into a language they did not say it in, would put words
# in their mouth; and the book they are quoting is English anyway.
KEEP = {
    '27b1680433',   # Armin Müller
    'a33ebd335c',   # Jan vom Brocke
    '19f5a5719a',   # Michael Bücker
    'ae536d1352',   # Michael Hewing
    'adac69379a',   # Code
}

DE = {
 'cd811450e1': 'Worum es geht',
 'dca72b32f8':
    '''Ein agentisches System koppelt ein Sprachmodell mit Tools, Memory und
    einer Orchestrierungsschicht, die entscheidet, was als Nächstes geschieht.
    Aus einem Modell, das antwortet, wird damit ein System, das handelt. Die
    schwierigen Fragen verschieben sich dabei vom Prompting in die Technik,
    die Ökonomie und die Governance.''',
 'ee76ee23ee':
    '''Das Buch arbeitet diese Fragen in drei Teilen ab. Der erste baut die
    Architektur auf: wie Sprachmodelle sich verhalten, wie Tools sie
    erweitern, was Memory über einen Lauf hinweg festhält und wie der
    Kontrollfluss eines Agenten geformt wird. Der zweite stellt diese
    Architektur in eine Organisation hinein und behandelt die Integration in
    bestehende Systeme, die Strategie, die Ökonomie des Agentenbetriebs, die
    Richtlinien, die ihn begrenzen, und die Prozesse, die er berührt. Der
    dritte handelt von Operations: mehrere Agenten zu orchestrieren, sie zur
    Laufzeit zu steuern, sie zu warten, während Modelle und Abhängigkeiten
    sich verändern, und sie gegen eine Angriffsklasse abzusichern, die es
    vorher nicht gab.''',
 '8642587792':
    '''Entstanden ist es aus Forschung, Lehre und Unternehmenskooperationen am
    Institut für Prozessmanagement und Digitale Transformation der FH Münster.
    Die Codebeispiele sind lauffähiges Python, und die im Buch abgedruckten
    Ausgaben sind die, die dieser Code erzeugt hat. Jedes Kapitel beginnt mit
    einer Stimme aus der Praxis.''',
 '83830ae186': 'Wie das Buch aufgebaut ist',
 'eefc7b9347': 'Die drei Teile sind die drei Ebenen eines Frameworks.',
 '8905acd3d6':
    '''Teil&nbsp;I baut den architektonischen Kern: das Modell, sein Memory,
    seine Tools. Teil&nbsp;III ist die Operations-Ebene, die ihn betreibt, mit
    Orchestrierung, Governance, Wartung und Sicherheit. Teil&nbsp;II ist die
    Organisation, der beide Rechenschaft schulden. Der gestrichelte Rahmen ist
    das Harness, die Laufzeitumgebung, die den Kern und die Operations-Ebene
    gemeinsam trägt.''',
 'f5cbdf6bfb': 'Inhalt',
 'd44d7e5906':
    '''Eine Einführung, dann dreizehn Kapitel in drei Teilen. Die Titel stehen
    hier auf Deutsch; das Buch selbst erscheint auf Englisch.''',
 '64c132812c': '<span class="part-no">I</span> Design und Architektur',
 'f208f621b6': '<span class="part-no">II</span> Organisation und Ökonomie',
 '6e42adcadb': '<span class="part-no">III</span> Operations',
 '0c5ba882ee': 'Für wen das Buch ist',
 '90a79c4b76':
    '''Studierende in Master-Programmen der Wirtschafts-, Informations- und
    Datenwissenschaften, und Praktikerinnen und Praktiker, die Entscheidungen
    treffen müssen statt Demonstrationen zu bauen: die Entwickler, die Agenten
    bauen, die Architekten, die sie integrieren, und diejenigen, die Budget
    und Risiko tragen.''',
 '025f4f5aae':
    '''Die Überlegungen sind durchgehend an ausgearbeiteten Python-Beispielen
    verankert, jedes davon als
    <a href="https://github.com/ai-agents-book/code">lauffähiges Notebook</a>
    verfügbar. Die meisten lesen sich wie das folgende, und der Argumentation
    lässt sich ebenso gut folgen, ohne je eine Zeile auszuführen. Wer die
    Grundlagen zuerst möchte:
    <a href="https://aiagentsbook.org/appendices/b-python.html">Anhang&nbsp;B</a>
    ist eine kurze Einführung in das Python und die Web-APIs, die die Listings
    verwenden, frei online lesbar. Das Buch setzt nicht voraus, dass Sie schon
    einmal ein Modell in Betrieb genommen haben.''',
 '62f29126e8':
    '''Ein Beispiel aus dem Buch: Listing&nbsp;4.1 aus dem Kapitel zu Agent
    Flow''',
 '07379076fa':
    '''Sechs Zeilen, und jedes Argument des Buches steckt irgendwo darin: was
    als Zustand zählt, wer die nächste Aktion wählt, wer sie ausführen darf
    und was den Lauf beendet. Kein Listing steht für sich allein. Jedes wird
    im Text eingeführt und durchgearbeitet, und auf die lauffähigen folgt die
    Ausgabe, die sie tatsächlich erzeugt haben.''',
 '47b6e0036e': 'Stimmen zum Buch',
 '07c3d48823':
    '<strong>Armin Müller</strong>, Global Head of Data &amp; AI, Kaufland',
 '0544ab3fa2':
    '''<strong>Jan vom Brocke</strong>, Lehrstuhl für Wirtschaftsinformatik und
    Geschäftsprozessmanagement, Universität Münster — <em>aus dem
    Vorwort</em>''',
 '9bd50ed52f': 'Die Autoren',
 'afd41c9317':
    '''Professor für Data Science, Mathematik und Wirtschaftsinformatik an der
    Münster School of Business der FH Münster, wo er den Studiengang Digital
    Business and Innovation Management leitet und dem Vorstand des Instituts
    für Prozessmanagement und Digitale Transformation angehört. Seine Arbeit
    umfasst angewandte Data Science, Machine Learning, erklärbare KI und
    statistische Methoden, die Theorie und organisationale Praxis verbinden.
    Vor seiner Zeit in der Wissenschaft war er Berater und Projektleiter bei
    McKinsey &amp; Company.''',
 '21253e2138':
    '''Professor für Wirtschaftsinformatik und Digitale Technologien an der
    Münster School of Business der FH Münster und Vorstandsmitglied des
    Instituts für Prozessmanagement und Digitale Transformation. Er forscht
    und lehrt zu Informationsmanagement, digitaler Transformation,
    Geschäftsprozessmanagement und der Integration fortgeschrittener
    Technologien in organisationale Zusammenhänge. Vor seiner Zeit in der
    Wissenschaft war er Senior Managing Consultant bei IBM und leitete
    Digitalisierungs- und IT-Transformationsprojekte für öffentliche
    Auftraggeber und Unternehmen.''',
 '914e5c7d56': 'Beide Autorenfotos: FH Münster/Hannah Jasiewitz',
 '454a0ca5b6': 'Material zum Buch',
 '7830c3cf2f':
    '''Jedes Beispiel aus dem Buch als lauffähiges Notebook, eines je Kapitel,
    mit einer Umgebung, die auf die Versionen festgelegt ist, die die
    abgedruckten Ausgaben erzeugt haben.''',
 '73973cfd16': 'Anhänge',
 '1f7ef885f6':
    '''Python-Setup, eine Referenz zu Python und Web-APIs sowie die
    Deep-Learning-Grundlagen, auf denen das Modellkapitel aufbaut. Online
    lesbar oder als PDF.''',
}

used = set()
for sid in ('about', 'framework', 'contents', 'audience', 'readers',
            'authors', 'material'):
    i = out.index('id="%s"' % sid)
    i = out.rindex('<section', 0, i)
    j = out.index('</section>', i)
    body = out[i:j]
    pieces, last = [], 0
    for m in BLOCK.finditer(body):
        key = hashlib.sha1(
            ' '.join(m.group(3).split()).encode()).hexdigest()[:10]
        if key in KEEP:
            continue
        assert key in DE, 'untranslated in #%s: %.60r (%s)' % (
            sid, ' '.join(m.group(3).split()), key)
        used.add(key)
        pieces.append(body[last:m.start(3)])
        pieces.append(' '.join(DE[key].split()))
        last = m.end(3)
    pieces.append(body[last:])
    out = out[:i] + ''.join(pieces) + out[j:]

assert used == set(DE), 'unused German blocks: %s' % (set(DE) - used)

# ------------------------------------------------------------ the contents
CH = [
 ('Large Language Models', 'Large Language Models',
  'How the models behave, and where their limits actually sit.',
  'Wie die Modelle sich verhalten und wo ihre Grenzen tatsächlich liegen.'),
 ('Tools', 'Tools',
  'Function calling, MCP, skills, CLI, GUI — five mechanisms, one cycle.',
  'Function Calling, MCP, Skills, CLI, GUI: fünf Mechanismen, ein Zyklus.'),
 ('Memory', 'Memory',
  'What persists between turns, and what keeping it commits you to.',
  'Was zwischen zwei Schritten bestehen bleibt und worauf man sich damit '
  'festlegt.'),
 ('Agent flow', 'Agent Flow',
  'The control structure of a single run: loops, budgets, recovery.',
  'Die Kontrollstruktur eines einzelnen Laufs: Schleifen, Budgets, '
  'Wiederanlauf.'),
 ('Integration', 'Integration',
  'How an agent reaches the systems and the people around it.',
  'Wie ein Agent die Systeme und die Menschen um ihn herum erreicht.'),
 ('Strategy', 'Strategie',
  'Where agents fit an organization\'s plans, and where they do not.',
  'Wo Agenten in die Pläne einer Organisation passen und wo nicht.'),
 ('Economics', 'Ökonomie',
  'Cost per successful outcome, not cost per run.',
  'Kosten pro erfolgreichem Ergebnis, nicht Kosten pro Lauf.'),
 ('Organizational policies', 'Organisatorische Richtlinien',
  'The constraints an agent must not be able to talk its way past.',
  'Die Grenzen, an denen ein Agent sich nicht vorbeiformulieren darf.'),
 ('Business processes', 'Geschäftsprozesse',
  'Where deployments actually pay off, domain by domain.',
  'Wo sich der Einsatz tatsächlich lohnt, Domäne für Domäne.'),
 ('Orchestration', 'Orchestrierung',
  'Coordinating several agents, and keeping runs alive between sessions.',
  'Mehrere Agenten koordinieren und Läufe über Sitzungen hinweg am Leben '
  'halten.'),
 ('Runtime governance', 'Laufzeit-Governance',
  'Governance as a second loop, running alongside the first.',
  'Governance als zweite Schleife, die neben der ersten läuft.'),
 ('Build and maintenance', 'Aufbau und Wartung',
  'Building an agent, and keeping it working as models move.',
  'Einen Agenten bauen und ihn funktionsfähig halten, während die Modelle '
  'sich bewegen.'),
 ('Security', 'Sicherheit',
  'Prompt injection and the attack surface a tool-using agent opens.',
  'Prompt Injection und die Angriffsfläche, die ein Agent mit Tools '
  'öffnet.'),
]
for en_name, de_name, en_blurb, de_blurb in CH:
    swap('<span class="ch-name">%s</span>' % en_name,
         '<span class="ch-name">%s</span>' % de_name)
    swap('<span class="ch-blurb">%s</span>' % en_blurb,
         '<span class="ch-blurb">%s</span>' % de_blurb)

# ------------------------------------------------------------------ footer
swap('''  <p class="footer-note">AI Agents: Designing, Orchestrating, and Governing
    LLM-Based Systems &middot; Michael Bücker and Michael Hewing
    &middot; Springer Nature, Cham &middot; 461 pages</p>''',
     '''  <p class="footer-note">AI Agents: Designing, Orchestrating, and Governing
    LLM-Based Systems &middot; Michael Bücker und Michael Hewing
    &middot; Springer Nature, Cham &middot; 461 Seiten</p>''')
swap('&middot; 24 February 2027', '&middot; 24. Februar 2027')
swap('&middot; 18 April 2027', '&middot; 18. April 2027')
swap('&middot; 24 February 2028', '&middot; 24. Februar 2028')
swap('&middot; live at publication', '&middot; ab Erscheinen aktiv')
swap('>Imprint</a>', '>Impressum</a>')
swap('&copy; 2026 Michael Bücker and Michael Hewing',
     '&copy; 2026 Michael Bücker und Michael Hewing')

# The two quotations stay English, so the page says why rather than leaving
# a German reader to wonder.
swap('''<section class="band" id="readers">
  <h2>Stimmen zum Buch</h2>''',
     '''<section class="band" id="readers">
  <h2>Stimmen zum Buch</h2>
  <p class="intro">Die Zitate stehen im englischen Original.</p>''')
swap('>Privacy</a>', '>Datenschutz</a>')

banner = ('<!-- Generated by tools/build-de.py from index.html. Edit the\n'
          '     English page and that script, not this file. -->\n')
out = out.replace('<!doctype html>', '<!doctype html>\n' + banner, 1)

os.makedirs(os.path.join(SITE, 'de'), exist_ok=True)
with open(os.path.join(SITE, 'de', 'index.html'), 'w', encoding='utf-8') as fh:
    fh.write(out)
print('wrote de/index.html, %d bytes' % len(out))
