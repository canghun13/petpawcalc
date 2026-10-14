# Generates front-facing sitting dog/cat symbols. Everything is placed on ground y=96, centered x=60.
def T(s, k, cx=60, cy=96):
    # scale group s by k around (cx,cy)
    return f'<g transform="translate({cx} {cy}) scale({k}) translate({-cx} {-cy})">{s}</g>'

def dog_sit(body, dark, light, muzzle, k_body=1.0, k_head=1.0, head_y=40, senior=False, eyes_closed=False):
    shadow = '<ellipse cx="60" cy="96" rx="30" ry="3.5" fill="#E6DCCB"/>'
    tail = f'<path d="M77 90C90 90 97 80 93 68" stroke="{body}" stroke-width="7" stroke-linecap="round" fill="none"/>'
    torso = (f'<ellipse cx="45" cy="88" rx="11" ry="8.5" fill="{body}"/>'
             f'<ellipse cx="75" cy="88" rx="11" ry="8.5" fill="{body}"/>'
             f'<path d="M42 95C38 76 45 54 60 54C75 54 82 76 78 95Z" fill="{body}"/>'
             f'<path d="M60 58C53 60 50.5 66 52.5 72C55.5 77 64.5 77 67.5 72C69.5 66 67 60 60 58Z" fill="{light}"/>'
             f'<rect x="50.5" y="70" width="8" height="26" rx="4" fill="{body}"/>'
             f'<rect x="61.5" y="70" width="8" height="26" rx="4" fill="{body}"/>'
             f'<path d="M60 77V93" stroke="{dark}" stroke-opacity="0.35" stroke-width="1.4" stroke-linecap="round"/>'
             f'<ellipse cx="54.5" cy="94.5" rx="5.2" ry="2.8" fill="{light}"/>'
             f'<ellipse cx="65.5" cy="94.5" rx="5.2" ry="2.8" fill="{light}"/>')
    hy = head_y
    eye = (f'<path d="M51.5 {hy-1}c1.6 1.3 3.4 1.3 5 0M63.5 {hy-1}c1.6 1.3 3.4 1.3 5 0" stroke="#2C1A0E" stroke-width="1.7" stroke-linecap="round" fill="none"/>'
           if eyes_closed else
           f'<circle cx="54" cy="{hy-1}" r="2.3" fill="#2C1A0E"/><circle cx="66" cy="{hy-1}" r="2.3" fill="#2C1A0E"/>'
           f'<circle cx="54.8" cy="{hy-1.8}" r="0.7" fill="#fff"/><circle cx="66.8" cy="{hy-1.8}" r="0.7" fill="#fff"/>')
    brows = (f'<path d="M50.5 {hy-6}q3.5-2 7 0M62.5 {hy-6}q3.5-2 7 0" stroke="#E9E4DC" stroke-width="2.2" stroke-linecap="round" fill="none"/>' if senior else '')
    head = (f'<path d="M45 {hy-12}C36 {hy-10} 34 {hy+6} 40 {hy+13}C44 {hy+10} 46 {hy} 48 {hy-8}Z" fill="{dark}"/>'
            f'<path d="M75 {hy-12}C84 {hy-10} 86 {hy+6} 80 {hy+13}C76 {hy+10} 74 {hy} 72 {hy-8}Z" fill="{dark}"/>'
            f'<ellipse cx="60" cy="{hy}" rx="16" ry="15.5" fill="{body}"/>'
            f'<ellipse cx="60" cy="{hy+7}" rx="9.5" ry="7.2" fill="{muzzle}"/>'
            f'<ellipse cx="60" cy="{hy+3.6}" rx="3.6" ry="2.7" fill="#2C1A0E"/>'
            f'<path d="M60 {hy+6.3}v2.4M56.8 {hy+9.2}q3.2 2.2 6.4 0" stroke="#2C1A0E" stroke-width="1.3" stroke-linecap="round" fill="none"/>'
            + eye + brows)
    return shadow + T(tail + torso, k_body) + T(head, k_head, 60, 96 - (96 - hy) * (1 - 0) )

def cat_sit(body, dark, light, stripe, k_body=1.0, k_head=1.0, head_y=42, eyes='open', face_patch=None):
    shadow = '<ellipse cx="60" cy="96" rx="28" ry="3.5" fill="#E6DCCB"/>'
    tail = f'<path d="M74 93C88 95 97 86 92 74C90 70 86 70 85 73" stroke="{body}" stroke-width="6.5" stroke-linecap="round" fill="none"/>'
    torso = (f'<ellipse cx="47" cy="89" rx="10" ry="7.5" fill="{body}"/>'
             f'<ellipse cx="73" cy="89" rx="10" ry="7.5" fill="{body}"/>'
             f'<path d="M44 95C40 77 47 57 60 57C73 57 80 77 76 95Z" fill="{body}"/>'
             f'<path d="M60 60C55 62 52.5 68 54.5 74C57 78 63 78 65.5 74C67.5 68 65 62 60 60Z" fill="{light}"/>'
             f'<path d="M45 70q4 1 6 4M75 70q-4 1-6 4M44 78q4 1 6 4M76 78q-4 1-6 4" stroke="{stripe}" stroke-width="2.2" stroke-linecap="round" fill="none"/>'
             f'<rect x="52" y="73" width="7" height="23" rx="3.5" fill="{body}"/>'
             f'<rect x="61" y="73" width="7" height="23" rx="3.5" fill="{body}"/>'
             f'<path d="M60 79V93" stroke="{dark}" stroke-opacity="0.45" stroke-width="1.3" stroke-linecap="round"/>'
             f'<ellipse cx="55.5" cy="94.6" rx="4.6" ry="2.6" fill="{light}"/>'
             f'<ellipse cx="64.5" cy="94.6" rx="4.6" ry="2.6" fill="{light}"/>')
    hy = head_y
    if eyes == 'open':
        eye = (f'<ellipse cx="54" cy="{hy}" rx="2.3" ry="3" fill="#2C1A0E"/><ellipse cx="66" cy="{hy}" rx="2.3" ry="3" fill="#2C1A0E"/>'
               f'<circle cx="54.8" cy="{hy-1}" r="0.7" fill="#fff"/><circle cx="66.8" cy="{hy-1}" r="0.7" fill="#fff"/>')
    else:
        eye = f'<path d="M51.5 {hy}c1.6 1.2 3.4 1.2 5 0M63.5 {hy}c1.6 1.2 3.4 1.2 5 0" stroke="#2C1A0E" stroke-width="1.7" stroke-linecap="round" fill="none"/>'
    patch = f'<ellipse cx="60" cy="{hy+6}" rx="8.5" ry="6" fill="{face_patch}"/>' if face_patch else ''
    head = (f'<path d="M45 {hy-6}L43 {hy-22}L56 {hy-12}Z" fill="{body}"/>'
            f'<path d="M75 {hy-6}L77 {hy-22}L64 {hy-12}Z" fill="{body}"/>'
            f'<path d="M46.5 {hy-9}L45.5 {hy-18}L53 {hy-12.5}Z" fill="#E7A79B"/>'
            f'<path d="M73.5 {hy-9}L74.5 {hy-18}L67 {hy-12.5}Z" fill="#E7A79B"/>'
            f'<ellipse cx="60" cy="{hy}" rx="17" ry="15" fill="{body}"/>'
            f'<path d="M56 {hy-13}v5M60 {hy-14}v6M64 {hy-13}v5" stroke="{stripe}" stroke-width="2" stroke-linecap="round"/>'
            + patch + eye +
            f'<path d="M58.4 {hy+5}h3.2l-1.6 1.8z" fill="#D9897C"/>'
            f'<path d="M60 {hy+6.8}q-1.6 2.2-3.4 1.2M60 {hy+6.8}q1.6 2.2 3.4 1.2" stroke="#2C1A0E" stroke-width="1.1" stroke-linecap="round" fill="none"/>'
            f'<path d="M50 {hy+5}h-9M50 {hy+7.5}l-8 2M70 {hy+5}h9M70 {hy+7.5}l8 2" stroke="{stripe}" stroke-width="0.9" stroke-linecap="round"/>')
    return shadow + T(tail + torso, k_body) + T(head, k_head, 60, 96)

def dog_lying(body, dark, light, muzzle):
    return ('<ellipse cx="60" cy="96" rx="32" ry="3.5" fill="#E6DCCB"/>'
            f'<path d="M80 88C92 88 96 82 92 78" stroke="{body}" stroke-width="6" stroke-linecap="round" fill="none"/>'
            f'<ellipse cx="60" cy="86" rx="26" ry="10" fill="{body}"/>'
            f'<ellipse cx="52" cy="93" rx="6" ry="3" fill="{light}"/><ellipse cx="66" cy="93" rx="6" ry="3" fill="{light}"/>'
            f'<path d="M47 66C40 68 39 80 44 85C47 82 48 76 49 70Z" fill="{dark}"/>'
            f'<path d="M73 66C80 68 81 80 76 85C73 82 72 76 71 70Z" fill="{dark}"/>'
            f'<ellipse cx="60" cy="74" rx="13" ry="12" fill="{body}"/>'
            f'<ellipse cx="60" cy="80" rx="7.5" ry="5.5" fill="{muzzle}"/>'
            '<ellipse cx="60" cy="77.4" rx="2.8" ry="2.1" fill="#2C1A0E"/>'
            '<path d="M52 72c1.5 1.1 3 1.1 4.5 0M63.5 72c1.5 1.1 3 1.1 4.5 0" stroke="#2C1A0E" stroke-width="1.5" stroke-linecap="round" fill="none"/>')

def cat_lying(body, light, stripe):
    return ('<ellipse cx="60" cy="96" rx="32" ry="3.5" fill="#E6DCCB"/>'
            f'<path d="M84 90C94 92 98 86 94 82" stroke="{body}" stroke-width="5.5" stroke-linecap="round" fill="none"/>'
            f'<ellipse cx="60" cy="86" rx="26" ry="10" fill="{body}"/>'
            f'<path d="M70 80q3 3 2 7M78 81q3 3 2 7" stroke="{stripe}" stroke-width="2" stroke-linecap="round" fill="none"/>'
            f'<ellipse cx="52" cy="93" rx="5.5" ry="3" fill="{light}"/><ellipse cx="66" cy="93" rx="5.5" ry="3" fill="{light}"/>'
            f'<path d="M48 70L46 58L56 65Z" fill="{body}"/><path d="M72 70L74 58L64 65Z" fill="{body}"/>'
            '<path d="M49.5 67.5L48.8 61L54 65Z" fill="#E7A79B"/><path d="M70.5 67.5L71.2 61L66 65Z" fill="#E7A79B"/>'
            f'<ellipse cx="60" cy="75" rx="14" ry="12" fill="{body}"/>'
            '<path d="M52 75c1.5 1.1 3 1.1 4.5 0M63.5 75c1.5 1.1 3 1.1 4.5 0" stroke="#2C1A0E" stroke-width="1.5" stroke-linecap="round" fill="none"/>'
            '<path d="M58.6 79h2.8l-1.4 1.6z" fill="#D9897C"/>')

D = dict(body="#C98A55", dark="#8E5B30", light="#F1DCC2", muzzle="#EAD2B4")
DS = dict(body="#B98656", dark="#7E5634", light="#EDE2D4", muzzle="#DCD6CE")
C = dict(body="#8D96A2", dark="#6F7884", light="#D9DDE2", stripe="#6C7480")
CS = dict(body="#A3AAB4", dark="#828A95", light="#E3E5E8", stripe="#848C97")

syms = {
 'dog-newborn': dog_lying(D['body'], D['dark'], D['light'], D['muzzle']),
 'dog-young': dog_sit(D['body'], D['dark'], D['light'], D['muzzle'], k_body=0.72, k_head=0.86, head_y=54),
 'dog-adult': dog_sit(D['body'], D['dark'], D['light'], D['muzzle'], head_y=44),
 'dog-senior': dog_sit(DS['body'], DS['dark'], DS['light'], DS['muzzle'], head_y=45, senior=True),
 'cat-newborn': cat_lying(C['body'], C['light'], C['stripe']),
 'cat-young': cat_sit(C['body'], C['dark'], C['light'], C['stripe'], k_body=0.72, k_head=0.86, head_y=56),
 'cat-adult': cat_sit(C['body'], C['dark'], C['light'], C['stripe'], head_y=46),
 'cat-senior': cat_sit(CS['body'], CS['dark'], CS['light'], CS['stripe'], head_y=47, eyes='closed', face_patch="#E3E5E8"),
}
out = ['<svg class="pp-sprite" aria-hidden="true" focusable="false" xmlns="http://www.w3.org/2000/svg">', '  <defs>']
for k, v in syms.items():
    out.append(f'    <symbol id="{k}" viewBox="0 0 120 100">{v}</symbol>')
out += ['  </defs>', '</svg>', '']
open('/home/claude/petpawcalc/_includes/pet-sprite.html', 'w').write('\n'.join(out))
print('written')
