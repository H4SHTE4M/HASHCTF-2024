from Crypto.Util.number import *
import sys
sys.setrecursionlimit(3000)
#flag=b'HASHCTF{M4Yb3_y0u_C@n_7ry_DepTH_1st_5earCH}'
n= 2936727719886069477497627101697302311867989372693276976148230239439358127115321028371261654711446063336859527274248698650235001234659411015351761160229532657630139621952592806099085712017531597183993252846119752140524397972100824553290738042783052616648565836234128844330847112297318494353928888777235152778984600474581654612013814936690800783447894921230687221876967308855166138994505985675591447840511621253641148476619952561851590274489487452159941574501615757861674045691539393552863763103377768477898996520483040075916635837683238994639460918528597360498433249843694481439713407840364065517397294022682378080860252165725788398701095543133951426899160349277052419482127130962442446095968558154642580711913263663194182839450421705585184966593319353821665118415382575668558596605186428125849578499363980307312688864347654863325058015930974654461871068930912343502730359637405813210173154301702675601155741733338372302744430628135696774349135608191663945519744724886044251425806573615182268976324557423609543674795323057962704339520923689560249658003318502521583933425309585977469150839008689862160513205822824694937890566267485543666301945465212014417014162574770950111986312635561478909056376205363873685446878054948022108046449668631084617145416592189528300806783713390174209828721912116343175760879687243483305084879488534274516656162775142009892546121528896884679385416254759487779091809525742036981713301674544783076717033165476361947557830474210660381481078038941643267811340710952934078358245960438494691685881311090042017632426484261729
e= 65537
c= 818691168081426059029814609336366930683489195438384219163653765354715034220344424719236169980480134909989709301092866607209504499297478224662765926081744320270283704436497964685834758118019775706676498393154678896668184070923883044306878840132679246282017160138808914609592824044547531751232020629493371116669263204482221914517017048249407109184223292217554885701262666874041549641451144421547351679407565043807794562501311726122872692838928632690249458263201520505024370053109116985885434594614680536111838380934248045809915857523722196320521712737243741817223352979355164528711735938618970354389817696960955207391672270136887024368577783182487452596022408392583445631369255204343459489787761180025646585917871164635670916102823835208346950259007119313122048875643963766460370292507640886933056411626180936231778234686261772665880563988102725530163144745908719629291356481907626461477775485270356113805348618530644187006238590989015250797931392372560373312581686401575977435394990057448156195917132660771807533832086661269885624944921374426762214156236123523664174440146544747369522555785675534302505810306355035876357352150474216380579203703952622847044466854390345940223237156603869249736613019460027697407010313892244406879417442531797733617517939693707414212819761406464884949041971659425499153871042698928344091947795029742402813915139808753977879989115897491148479398798390304064730615116365652499476846030347948456050989017998199123221858439204473656386203490333925477865545719014498516668233611862438869375970803812795585879213323250713

def dfs(p, q):
    l = len(p)
    if l == 773:
        plist.append(p)
    else:
        pp = int(p)
        qq = int(q)
        if pp * qq % 10 ** l == n % 10 ** l:
            dfs('3' + p, '7' + q)
            dfs('3' + p, '3' + q)
            dfs('7' + p, '3' + q)
            dfs('7' + p, '7' + q)


plist = []
dfs('7', '7')
for p in plist:
    q = n // int(p)
    if len(set(str(q)))==2:

        print(q)
        p=int(p)
        phi = (p - 1) * (q - 1)
        d = inverse(e, phi)
        m = pow(c, d, n)
        print(long_to_bytes(int(m)))

# -----------------------------------------------------------------------------------------------------------------------

