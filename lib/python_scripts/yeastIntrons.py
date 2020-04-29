# purpose:  provide a data structure (dict) of all yeast introns in yeast SGD reference
#            genome.
#
# This was created using gffutils (https://pythonhosted.org/gffutils/contents.html)
# 
# import gffutils
# from collections import defaultdict
# import yeast_Gene_name_to_ORF as yg
#
# tdb = gffutils.FeatureDB('yeast.db', keep_order=True)
# introns = defaultdict(dict)
#
#
# with open('yeast-intron-list.txt','w') as out:
#    for gene in yg.geneToOrf.itervalues():
#        for f in tdb.children( gene):
#            if f.featuretype == 'intron':
#                if gene not in introns:
#                    introns[gene]['chrom'] = f.chrom
#                    introns[gene]['start'] = []
#                    introns[gene]['start'].append(f.start)
#                   introns[gene]['stop']   = []
#                    introns[gene]['stop'].append(f.stop)
#                else:
#                    introns[gene]['start'].append(f.start)
#                    introns[gene]['stop'].append(f.stop)
#    ct = 0
#    for k,v in introns.iteritems():
#        ct += 1
#       out.write( '\"%s\" : %s,' %( k, v) )
#        if ct == 3:
#            out.write("\n")
#            ct = 0
#
# Author: Mike Place
#
introns = { "YHR218W" : {'stop': [558714], 'start': [558616], 'chrom': 'VIII'},"YLR445W" : {'stop': [1024654], 'start': [1024573], 'chrom': 'XII'},"YBL026W" : {'stop': [170804], 'start': [170677], 'chrom': 'II'},
"YPR187W" : {'stop': [911352], 'start': [911277], 'chrom': 'XVI'},"YGL087C" : {'stop': [346893], 'start': [346809], 'chrom': 'VII'},"YBR181C" : {'stop': [592768], 'start': [592417], 'chrom': 'II'},
"YBR090C" : {'stop': [426873], 'start': [426517], 'chrom': 'II'},"YDR025W" : {'stop': [491898], 'start': [491560], 'chrom': 'IV'},"YGR001C" : {'stop': [497458, 497999], 'start': [497366, 497938], 'chrom': 'VII'},
"YDR535C" : {'stop': [1507314], 'start': [1507059], 'chrom': 'IV'},"YMR125W" : {'stop': [517885], 'start': [517564], 'chrom': 'XIII'},"YML124C" : {'stop': [23658], 'start': [23361], 'chrom': 'XIII'},
"YIL156W-B" : {'stop': [47760], 'start': [47699], 'chrom': 'IX'},"YKR057W" : {'stop': [552002], 'start': [551681], 'chrom': 'XI'},"YGR296W" : {'stop': [1085030], 'start': [1084883], 'chrom': 'VII'},
"YJR145C" : {'stop': [703054], 'start': [702799], 'chrom': 'X'},"YDL125C" : {'stop': [239509], 'start': [239399], 'chrom': 'IV'},"YPL249C-A" : {'stop': [76223], 'start': [75986], 'chrom': 'XVI'},
"YML017W" : {'stop': [236953], 'start': [236592], 'chrom': 'XIII'},"YKL006C-A" : {'stop': [430596], 'start': [430456], 'chrom': 'XI'},"YNL301C" : {'stop': [64450], 'start': [64019], 'chrom': 'XIV'},
"YML036W" : {'stop': [206203], 'start': [206098], 'chrom': 'XIII'},"YBR111W-A" : {'stop': [462289, 462499], 'start': [462210, 462430], 'chrom': 'II'},"YHR077C" : {'stop': [255750], 'start': [255638], 'chrom': 'VIII'},
"YKL006W" : {'stop': [432432], 'start': [432035], 'chrom': 'XI'},"YDR424C" : {'stop': [1319697, 1319816], 'start': [1319618, 1319721], 'chrom': 'IV'},"YLR048W" : {'stop': [242680], 'start': [242322], 'chrom': 'XII'},
"YBR119W" : {'stop': [479434], 'start': [479346], 'chrom': 'II'},"YMR292W" : {'stop': [854898], 'start': [854817], 'chrom': 'XIII'},"Q0255" : {'stop': [75662, 75903], 'start': [75623, 75873], 'chrom': 'Mito'},
"YLR464W" : {'stop': [1067363], 'start': [1067085], 'chrom': 'XII'},"YJL191W" : {'stop': [74204], 'start': [73797], 'chrom': 'X'},"YDR129C" : {'stop': [715358], 'start': [715248], 'chrom': 'IV'},
"YKL190W" : {'stop': [83074], 'start': [82999], 'chrom': 'XI'},"YEL076C-A" : {'stop': [4601], 'start': [4323], 'chrom': 'V'},"YPL090C" : {'stop': [378389], 'start': [377996], 'chrom': 'XVI'},
"YFL034C-B" : {'stop': [63973], 'start': [63860], 'chrom': 'VI'},"YNL302C" : {'stop': [62923], 'start': [62373], 'chrom': 'XIV'},"YBL027W" : {'stop': [168808], 'start': [168425], 'chrom': 'II'},
"YLR448W" : {'stop': [1029252], 'start': [1028869], 'chrom': 'XII'},"YNL096C" : {'stop': [444171], 'start': [443827], 'chrom': 'XIV'},"YLR275W" : {'stop': [694472], 'start': [694383], 'chrom': 'XII'},
"YGR034W" : {'stop': [556307], 'start': [555831], 'chrom': 'VII'},"YHR076W" : {'stop': [251248], 'start': [251156], 'chrom': 'VIII'},"YGL232W" : {'stop': [62189], 'start': [62132], 'chrom': 'VII'},
"YJL205C" : {'stop': [50411], 'start': [50269], 'chrom': 'X'},"YLR078C" : {'stop': [286556], 'start': [286468], 'chrom': 'XII'},"YHR041C" : {'stop': [189850], 'start': [189750], 'chrom': 'VIII'},
"YCR097W" : {'stop': [293993, 294291], 'start': [293940, 294240], 'chrom': 'III'},"YDL064W" : {'stop': [337634], 'start': [337525], 'chrom': 'IV'},"YPL129W" : {'stop': [305411], 'start': [305307], 'chrom': 'XVI'},
"YIL148W" : {'stop': [69149], 'start': [68716], 'chrom': 'IX'},"YLR054C" : {'stop': [250947], 'start': [250861], 'chrom': 'XII'},"YPL079W" : {'stop': [407067], 'start': [406647], 'chrom': 'XVI'},
"YDR397C" : {'stop': [1266861], 'start': [1266770], 'chrom': 'IV'},"YKR005C" : {'stop': [450020], 'start': [449952], 'chrom': 'XI'},"YLR211C" : {'stop': [564513], 'start': [564455], 'chrom': 'XII'},
"YPL175W" : {'stop': [218746], 'start': [218647], 'chrom': 'XVI'},"YER179W" : {'stop': [548644], 'start': [548553], 'chrom': 'V'},"YJL136C" : {'stop': [157249], 'start': [156790], 'chrom': 'X'},
"YOR096W" : {'stop': [506338], 'start': [505938], 'chrom': 'XV'},"YBL050W" : {'stop': [125270], 'start': [125155], 'chrom': 'II'},"YOR312C" : {'stop': [901193], 'start': [900768], 'chrom': 'XV'},
"Q0055" : {'stop': [16434], 'start': [13987], 'chrom': 'Mito'},"YDR450W" : {'stop': [1360404], 'start': [1359970], 'chrom': 'IV'},"YER133W" : {'stop': [433196], 'start': [432672], 'chrom': 'V'},
"YBL087C" : {'stop': [60697], 'start': [60194], 'chrom': 'II'},"YPR202W" : {'stop': [943198], 'start': [943051], 'chrom': 'XVI'},"YER093C-A" : {'stop': [348276], 'start': [348202], 'chrom': 'V'},
"YAL001C" : {'stop': [151096], 'start': [151007], 'chrom': 'I'},"YHR203C" : {'stop': [505516], 'start': [505248], 'chrom': 'VIII'},"YIL018W" : {'stop': [317171], 'start': [316772], 'chrom': 'IX'},
"YDL075W" : {'stop': [322703], 'start': [322283], 'chrom': 'IV'},"YDL130W" : {'stop': [230320], 'start': [230020], 'chrom': 'IV'},"YFL039C" : {'stop': [54686], 'start': [54378], 'chrom': 'VI'},
"YMR142C" : {'stop': [551203], 'start': [550802], 'chrom': 'XIII'},"YCR028C-A" : {'stop': [173198], 'start': [173116], 'chrom': 'III'},"YEL012W" : {'stop': [131899], 'start': [131777], 'chrom': 'V'},
"YLR093C" : {'stop': [327399], 'start': [327259], 'chrom': 'XII'},"YDL029W" : {'stop': [399484], 'start': [399362], 'chrom': 'IV'},"YJR079W" : {'stop': [581052], 'start': [580348], 'chrom': 'X'},
"YPR043W" : {'stop': [654570], 'start': [654168], 'chrom': 'XVI'},"YPL198W" : {'stop': [173571, 174072], 'start': [173163, 173666], 'chrom': 'XVI'},"YBL040C" : {'stop': [142846], 'start': [142750], 'chrom': 'II'},
"YIL111W" : {'stop': [155310], 'start': [155223], 'chrom': 'IX'},"YLL067C" : {'stop': [4014], 'start': [3916], 'chrom': 'XII'},"YGL178W" : {'stop': [167994], 'start': [167355], 'chrom': 'VII'},
"YHR039C-A" : {'stop': [187676], 'start': [187515], 'chrom': 'VIII'},"YKL156W" : {'stop': [158966], 'start': [158616], 'chrom': 'XI'},"YJL001W" : {'stop': [435343], 'start': [435228], 'chrom': 'X'},
"YDR447C" : {'stop': [1355550], 'start': [1355237], 'chrom': 'IV'},"YGR118W" : {'stop': [727357], 'start': [727039], 'chrom': 'VII'},"YML085C" : {'stop': [99375], 'start': [99260], 'chrom': 'XIII'},
"YLR202C" : {'stop': [550574], 'start': [550459], 'chrom': 'XII'},"YGR214W" : {'stop': [921119], 'start': [920665], 'chrom': 'VII'},"YOR318C" : {'stop': [912432], 'start': [912086], 'chrom': 'XV'},
"YGR225W" : {'stop': [946420], 'start': [946328], 'chrom': 'VII'},"YOL127W" : {'stop': [80774], 'start': [80361], 'chrom': 'XV'},"YOR234C" : {'stop': [779386], 'start': [778860], 'chrom': 'XV'},
"YOL120C" : {'stop': [94290], 'start': [93844], 'chrom': 'XV'},"YHR199C-A" : {'stop': [498786], 'start': [498720], 'chrom': 'VIII'},"YOR293W" : {'stop': [867586], 'start': [867150], 'chrom': 'XV'},
"YML056C" : {'stop': [163716], 'start': [163309], 'chrom': 'XIII'},"YMR143W" : {'stop': [552495], 'start': [551952], 'chrom': 'XIII'},"YDL191W" : {'stop': [118157], 'start': [117667], 'chrom': 'IV'},
"YDR064W" : {'stop': [580017], 'start': [579479], 'chrom': 'IV'},"YIL106W" : {'stop': [166519], 'start': [166435], 'chrom': 'IX'},"YHR101C" : {'stop': [315858], 'start': [315772], 'chrom': 'VIII'},
"YML067C" : {'stop': [140183], 'start': [140091], 'chrom': 'XIII'},"YIL004C" : {'stop': [348494], 'start': [348364], 'chrom': 'IX'},"YBR084C-A" : {'stop': [415259], 'start': [414754], 'chrom': 'II'},
"YLL050C" : {'stop': [40400], 'start': [40222], 'chrom': 'XII'},"YLR344W" : {'stop': [819777], 'start': [819331], 'chrom': 'XII'},"YIL177C" : {'stop': [4986], 'start': [4599], 'chrom': 'IX'},
"YBR215W" : {'stop': [653452], 'start': [653369], 'chrom': 'II'},"YHL001W" : {'stop': [104803], 'start': [104406], 'chrom': 'VIII'},"YJL031C" : {'stop': [387435], 'start': [387349], 'chrom': 'X'},
"YDR005C" : {'stop': [458097], 'start': [458018], 'chrom': 'IV'},"YER003C" : {'stop': [159087], 'start': [158995], 'chrom': 'V'},"YNL147W" : {'stop': [351053], 'start': [350958], 'chrom': 'XIV'},
"YJL041W" : {'stop': [365902], 'start': [365785], 'chrom': 'X'},"YER044C-A" : {'stop': [239711], 'start': [239624], 'chrom': 'V'},"YER074W-A" : {'stop': [307848, 308067], 'start': [307747, 307957], 'chrom': 'V'},
"YMR225C" : {'stop': [721345], 'start': [721199], 'chrom': 'XIII'},"YMR033W" : {'stop': [337903], 'start': [337818], 'chrom': 'XIII'},"Q0070" : {'stop': [16434, 18953, 20507, 21994], 'start': [13987, 16471, 18992, 20985], 'chrom': 'Mito'},
"YIL069C" : {'stop': [232366], 'start': [231958], 'chrom': 'IX'},"YNL265C" : {'stop': [145254], 'start': [145150], 'chrom': 'XIV'},"YFR024C-A" : {'stop': [203386], 'start': [203293], 'chrom': 'VI'},
"YGL183C" : {'stop': [157282], 'start': [157200], 'chrom': 'VII'},"YMR133W" : {'stop': [537564], 'start': [537449], 'chrom': 'XIII'},"Q0065" : {'stop': [16434, 18953, 20507], 'start': [13987, 16471, 18992], 'chrom': 'Mito'},
"YKR095W-A" : {'stop': [625976], 'start': [625902], 'chrom': 'XI'},"YFR031C-A" : {'stop': [221414], 'start': [221268], 'chrom': 'VI'},"YBR230C" : {'stop': [680039], 'start': [679943], 'chrom': 'II'},
"YOL121C" : {'stop': [92830], 'start': [92441], 'chrom': 'XV'},"YNL138W-A" : {'stop': [366157], 'start': [366036], 'chrom': 'XIV'},"Q0110" : {'stop': [37722], 'start': [36955], 'chrom': 'Mito'},
"YLR128W" : {'stop': [398626], 'start': [398533], 'chrom': 'XII'},"YDR059C" : {'stop': [569723], 'start': [569634], 'chrom': 'IV'},"YMR242C" : {'stop': [754219], 'start': [753743], 'chrom': 'XIII'},
"YPR132W" : {'stop': [795394], 'start': [795030], 'chrom': 'XVI'},"YNL050C" : {'stop': [534965], 'start': [534875], 'chrom': 'XIV'},"YNL112W" : {'stop': [415913], 'start': [414912], 'chrom': 'XIV'},
"YBR191W" : {'stop': [606668], 'start': [606281], 'chrom': 'II'},"YBR062C" : {'stop': [366584], 'start': [366503], 'chrom': 'II'},"YOR122C" : {'stop': [552874], 'start': [552666], 'chrom': 'XV'},
"YGL033W" : {'stop': [435749], 'start': [435680], 'chrom': 'VII'},"YML073C" : {'stop': [124157], 'start': [123743], 'chrom': 'XIII'},"YCR031C" : {'stop': [178213], 'start': [177907], 'chrom': 'III'},
"YMR201C" : {'stop': [667017], 'start': [666934], 'chrom': 'XIII'},"YNL339C" : {'stop': [6079], 'start': [5932], 'chrom': 'XIV'},"YBR082C" : {'stop': [407122], 'start': [407028], 'chrom': 'II'},
"YML094W" : {'stop': [82373], 'start': [82291], 'chrom': 'XIII'},"YBL018C" : {'stop': [186427], 'start': [186353], 'chrom': 'II'},"YGL251C" : {'stop': [31578], 'start': [31427], 'chrom': 'VII'},
"YDL108W" : {'stop': [267806], 'start': [267726], 'chrom': 'IV'},"YJR112W-A" : {'stop': [637858], 'start': [637810], 'chrom': 'X'},"YKR094C" : {'stop': [618742], 'start': [618375], 'chrom': 'XI'},
"YNR053C" : {'stop': [722302], 'start': [721771], 'chrom': 'XIV'},"YBR078W" : {'stop': [393510], 'start': [393181], 'chrom': 'II'},"YIL133C" : {'stop': [99385], 'start': [99096], 'chrom': 'IX'},
"YML024W" : {'stop': [226289], 'start': [225892], 'chrom': 'XIII'},"YLR367W" : {'stop': [857057], 'start': [856575], 'chrom': 'XII'},"Q0060" : {'stop': [16434, 18953], 'start': [13987, 16471], 'chrom': 'Mito'},
"YDR381C-A" : {'stop': [1238824], 'start': [1238631], 'chrom': 'IV'},"YBL111C" : {'stop': [4215], 'start': [4117], 'chrom': 'II'},"YJL189W" : {'stop': [76324], 'start': [75939], 'chrom': 'X'},
"YIL052C" : {'stop': [257026], 'start': [256555], 'chrom': 'IX'},"YNL012W" : {'stop': [609874], 'start': [609791], 'chrom': 'XIV'},"YML133C" : {'stop': [3890], 'start': [3792], 'chrom': 'XIII'},
"YER007C-A" : {'stop': [166874], 'start': [166772], 'chrom': 'V'},"YCL002C" : {'stop': [111633], 'start': [111558], 'chrom': 'III'},"YDR139C" : {'stop': [733775], 'start': [733703], 'chrom': 'IV'},
"YBR219C" : {'stop': [663002], 'start': [662582], 'chrom': 'II'},"YMR116C" : {'stop': [500151], 'start': [499879], 'chrom': 'XIII'},"Q0105" : {'stop': [37722, 39140, 40840, 42507, 43296], 'start': [36955, 37737, 39218, 41091, 42559], 'chrom': 'Mito'},
"YHL050C" : {'stop': [2670], 'start': [1898], 'chrom': 'VIII'},"YGL137W" : {'stop': [250086], 'start': [249887], 'chrom': 'VII'},"YLR061W" : {'stop': [263594], 'start': [263206], 'chrom': 'XII'},
"YLR306W" : {'stop': [744287], 'start': [744154], 'chrom': 'XII'},"YGL030W" : {'stop': [439323], 'start': [439094], 'chrom': 'VII'},"YIL073C" : {'stop': [225899], 'start': [225810], 'chrom': 'IX'},
"YPL075W" : {'stop': [413012], 'start': [412262], 'chrom': 'XVI'},"YFR045W" : {'stop': [242081], 'start': [242010], 'chrom': 'VI'},"YER074W" : {'stop': [306791], 'start': [306326], 'chrom': 'V'},
"YBL059W" : {'stop': [110948], 'start': [110880], 'chrom': 'II'},"YNL069C" : {'stop': [494973], 'start': [494525], 'chrom': 'XIV'},"YGR029W" : {'stop': [543721], 'start': [543639], 'chrom': 'VII'},
"YJL024C" : {'stop': [396570], 'start': [396494], 'chrom': 'X'},"YFL034C-A" : {'stop': [64920], 'start': [64600], 'chrom': 'VI'},"YHR141C" : {'stop': [382747], 'start': [382307], 'chrom': 'VIII'},
"YOL047C" : {'stop': [242504], 'start': [242442], 'chrom': 'XV'},"Q0075" : {'stop': [24905], 'start': [24871], 'chrom': 'Mito'},"YPR010C-A" : {'stop': [582701], 'start': [582559], 'chrom': 'XVI'},
"YHR012W" : {'stop': [129647], 'start': [129529], 'chrom': 'VIII'},"YNL312W" : {'stop': [48401], 'start': [48294], 'chrom': 'XIV'},"YHR123W" : {'stop': [354955], 'start': [354865], 'chrom': 'VIII'},
"YBL059C-A" : {'stop': [110505], 'start': [110421], 'chrom': 'II'},"YFL031W" : {'stop': [76091], 'start': [75840], 'chrom': 'VI'},"YPL241C" : {'stop': [96233], 'start': [96154], 'chrom': 'XVI'},
"YMR194C-B" : {'stop': [652847], 'start': [652776], 'chrom': 'XIII'},"YBL091C-A" : {'stop': [47146], 'start': [47059], 'chrom': 'II'},"YPR153W" : {'stop': [833827], 'start': [833694], 'chrom': 'XVI'},
"Q0045" : {'stop': [16434, 18953, 20507, 21994, 23611, 25317, 26228], 'start': [13987, 16471, 18992, 20985, 22247, 23747, 25343], 'chrom': 'Mito'},"YKL157W" : {'stop': [155654], 'start': [155272], 'chrom': 'XI'},"YJL225C" : {'stop': [4969], 'start': [4582], 'chrom': 'X'},
"YLL066C" : {'stop': [9549], 'start': [9451], 'chrom': 'XII'},"YPR063C" : {'stop': [678279], 'start': [678194], 'chrom': 'XVI'},"YPL143W" : {'stop': [282665], 'start': [282141], 'chrom': 'XVI'},
"YKR004C" : {'stop': [447810], 'start': [447707], 'chrom': 'XI'},"YAL030W" : {'stop': [87500], 'start': [87388], 'chrom': 'I'},"YOL048C" : {'stop': [241025], 'start': [240948], 'chrom': 'XV'},
"YDR367W" : {'stop': [1212978], 'start': [1212878], 'chrom': 'IV'},"YDL012C" : {'stop': [431472], 'start': [431387], 'chrom': 'IV'},"Q0115" : {'stop': [37722, 39140], 'start': [36955, 37737], 'chrom': 'Mito'},
"YGL226C-A" : {'stop': [73137], 'start': [72989], 'chrom': 'VII'},"YNL004W" : {'stop': [623286], 'start': [622945], 'chrom': 'XIV'},"YDR471W" : {'stop': [1402184], 'start': [1401801], 'chrom': 'IV'},
"YHR021C" : {'stop': [148666], 'start': [148117], 'chrom': 'VIII'},"YDL082W" : {'stop': [308792], 'start': [308428], 'chrom': 'IV'},"YJR021C" : {'stop': [469263], 'start': [469184], 'chrom': 'X'},
"YHR001W-A" : {'stop': [107894], 'start': [107832], 'chrom': 'VIII'},"YJL177W" : {'stop': [91411], 'start': [91095], 'chrom': 'X'},"YLR185W" : {'stop': [523028], 'start': [522670], 'chrom': 'XII'},
"YMR230W" : {'stop': [732875], 'start': [732466], 'chrom': 'XIII'},"YMR194W" : {'stop': [651623], 'start': [651161], 'chrom': 'XIII'},"YDL219W" : {'stop': [65377], 'start': [65307], 'chrom': 'IV'},
"YBR189W" : {'stop': [604927], 'start': [604515], 'chrom': 'II'},"YPL081W" : {'stop': [405457], 'start': [404957], 'chrom': 'XVI'},"YHR079C-A" : {'stop': [262440], 'start': [262355], 'chrom': 'VIII'},
"YGR183C" : {'stop': [859473], 'start': [859261], 'chrom': 'VII'},"YLR329W" : {'stop': [786712], 'start': [786616], 'chrom': 'XII'},"YLR199C" : {'stop': [548763], 'start': [548678], 'chrom': 'XII'},
"YHR016C" : {'stop': [138408], 'start': [138241], 'chrom': 'VIII'},"YER117W" : {'stop': [397281], 'start': [396811], 'chrom': 'V'},"YLR426W" : {'stop': [987212], 'start': [987142], 'chrom': 'XII'},
"YCL012C" : {'stop': [101700], 'start': [101634], 'chrom': 'III'},"YBR048W" : {'stop': [333386], 'start': [332876], 'chrom': 'II'},"YPL283C" : {'stop': [5988], 'start': [5841], 'chrom': 'XVI'},
"YNL130C" : {'stop': [380781], 'start': [380690], 'chrom': 'XIV'},"YNL162W" : {'stop': [331837], 'start': [331326], 'chrom': 'XIV'},"YLR406C" : {'stop': [931698], 'start': [931350], 'chrom': 'XII'},
"YDR318W" : {'stop': [1103892], 'start': [1103810], 'chrom': 'IV'},"YPL031C" : {'stop': [493020], 'start': [492919], 'chrom': 'XVI'},"YPR098C" : {'stop': [729481], 'start': [729386], 'chrom': 'XVI'},
"YAL003W" : {'stop': [142619], 'start': [142254], 'chrom': 'I'},"YML026C" : {'stop': [223781], 'start': [223381], 'chrom': 'XIII'},"YGL076C" : {'stop': [365432, 365985], 'start': [364965, 365527], 'chrom': 'VII'},
"YMR079W" : {'stop': [425153], 'start': [424998], 'chrom': 'XIII'},"YDR305C" : {'stop': [1073401], 'start': [1073313], 'chrom': 'IV'},"YPL218W" : {'stop': [138864], 'start': [138726], 'chrom': 'XVI'},
"YPL109C" : {'stop': [345596], 'start': [345445], 'chrom': 'XVI'},"Q0120" : {'stop': [37722, 39140, 40840], 'start': [36955, 37737, 39218], 'chrom': 'Mito'},"YBR186W" : {'stop': [602216], 'start': [602104], 'chrom': 'II'},
"YKL180W" : {'stop': [109883], 'start': [109578], 'chrom': 'XI'},"YHR010W" : {'stop': [127112], 'start': [126552], 'chrom': 'VIII'},"YDR381W" : {'stop': [1237608], 'start': [1236843], 'chrom': 'IV'},
"YGL103W" : {'stop': [311526], 'start': [311016], 'chrom': 'VII'},"YPR028W" : {'stop': [623710], 'start': [623578], 'chrom': 'XVI'},"YER056C-A" : {'stop': [270148], 'start': [269752], 'chrom': 'V'},
"YKL002W" : {'stop': [437905], 'start': [437838], 'chrom': 'XI'},"YCL005W-A" : {'stop': [107110, 107287], 'start': [107034, 107192], 'chrom': 'III'},"YDL083C" : {'stop': [307765], 'start': [307334], 'chrom': 'IV'},
"YBR255C-A" : {'stop': [727011], 'start': [726918], 'chrom': 'II'},"YML034W" : {'stop': [211570], 'start': [211445], 'chrom': 'XIII'},"YOR182C" : {'stop': [678790], 'start': [678380], 'chrom': 'XV'},
"YJR094W-A" : {'stop': [608581], 'start': [608307], 'chrom': 'X'},"YEL003W" : {'stop': [148282], 'start': [148195], 'chrom': 'V'},"YNL038W" : {'stop': [557684], 'start': [557611], 'chrom': 'XIV'},
"YDL136W" : {'stop': [218007], 'start': [217603], 'chrom': 'IV'},"YDL115C" : {'stop': [255044], 'start': [254975], 'chrom': 'IV'},"YKL081W" : {'stop': [283421], 'start': [283096], 'chrom': 'XI'},
"YDR092W" : {'stop': [630173], 'start': [629906], 'chrom': 'IV'},"YDR500C" : {'stop': [1450846], 'start': [1450458], 'chrom': 'IV'},"YNL044W" : {'stop': [545370], 'start': [545292], 'chrom': 'XIV'},
"YPR170W-B" : {'stop': [883486], 'start': [883388], 'chrom': 'XVI'},"YER014C-A" : {'stop': [184677], 'start': [184170], 'chrom': 'V'},"YHR097C" : {'stop': [298484], 'start': [298361], 'chrom': 'VIII'},
"YLR287C-A" : {'stop': [713155], 'start': [712726], 'chrom': 'XII'},"YML025C" : {'stop': [225338], 'start': [225240], 'chrom': 'XIII'},"YLR316C" : {'stop': [766129, 766249], 'start': [766074, 766182], 'chrom': 'XII'},
"YNL246W" : {'stop': [185586], 'start': [185492], 'chrom': 'XIV'},"YDL079C" : {'stop': [314336], 'start': [314045], 'chrom': 'IV'} 
}