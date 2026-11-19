#!/usr/bin/env python3
"""依 src/meta/*.yaml 產生某一冊的內容：
  src/generated/vol<N>-body.tex   依主題（和《資料結構與演算法》同章號）排的題目與詳解
  src/generated/vol<N>-papers.tex 附錄「依考卷查題」：每份考卷每一題在第幾頁
用法：scripts/assemble.py 1
"""
import sys, glob, yaml, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHAPTERS = {
    1: '演算法分析與漸近符號', 2: '遞迴式', 3: '平攤分析', 4: '陣列、矩陣與多項式',
    5: '鏈結串列', 6: '堆疊與佇列', 7: '樹與二元樹', 8: '堆積與優先佇列', 9: '二元搜尋樹',
    10: '平衡搜尋樹：AVL 樹、紅黑樹、伸展樹與跳躍串列',
    11: r'多路搜尋樹與 trie：2-3 樹、B 樹、\texorpdfstring{B$^{+}$}{B+} 樹與數位搜尋樹',
    12: '雜湊', 13: '互斥集合', 14: '排序', 15: '排序的下界、線性時間排序與外部排序',
    16: '選擇問題', 17: '分治', 18: '動態規劃', 19: '貪心', 20: '回溯與分支限界',
    21: '圖的表示、BFS 與 DFS', 22: '拓樸排序、AOV 與 AOE 網路',
    23: '連通性：強連通元件、割點、橋與雙連通元件', 24: '最小生成樹', 25: '最短路徑',
    26: '網路流與二分匹配', 27: '字串比對', 28: 'NP 完備', 29: '近似演算法',
}
SCHOOLS = ['臺大', '清大', '交大', '陽明交大', '政大', '臺科大', '北科大', '中央', '中興',
           '中正', '中山', '成大', '臺聯大']

def load(vol):
    papers = []
    for f in sorted(glob.glob(os.path.join(ROOT, 'src/meta/*.yaml'))):
        m = yaml.safe_load(open(f, encoding='utf-8'))
        if int(m['volume']) == vol:
            papers.append(m)
    key = lambda m: (SCHOOLS.index(m['school']) if m['school'] in SCHOOLS else 99, int(m['year']), m['paper'])
    return sorted(papers, key=key)

def source(m, q):
    return f"{m['school']}{m['dept']} {m['year']} 學年度 {q['label']}"

def main():
    vol = int(sys.argv[1])
    papers = load(vol)
    bych = {}
    for pi, m in enumerate(papers):
        for qi, q in enumerate(m['questions']):
            path = os.path.join(ROOT, 'src/questions', q['id'] + '.tex')
            if not os.path.exists(path):
                sys.exit(f'missing {path}')
            bych.setdefault(int(q['chapter']), []).append((pi, qi, m, q))
    out = ['% 由 scripts/assemble.py 產生，不要手改。']
    for ch in sorted(bych):
        out.append(f'\\setcounter{{chapter}}{{{ch - 1}}}')
        out.append(f'\\chapter{{{CHAPTERS[ch]}}}')
        out.append(f'本章的題目對應《資料結構與演算法：C 語言、虛擬碼與研究所考試》第~{ch}~章。'
                   '依學校、學年度排列。\n')
        for _, _, m, q in sorted(bych[ch], key=lambda x: (x[0], x[1])):
            out.append(f'\\input{{questions/{q["id"]}}}')
        out.append('')
    gen = os.path.join(ROOT, 'src/generated')
    os.makedirs(gen, exist_ok=True)
    open(os.path.join(gen, f'vol{vol}-body.tex'), 'w').write('\n'.join(out) + '\n')

    ap = ['% 由 scripts/assemble.py 產生，不要手改。', '\\chapter{依考卷查題}',
          '想用整份考卷計時練習時，照下表找出每一題在書裡的頁碼。'
          '只列資料結構與演算法的題目；合卷裡其他科目的題目沒有收。\n']
    for m in papers:
        ap.append(f"\\section*{{{m['school']}{m['dept']} {m['year']} 學年度　{m['subject']}}}")
        if m.get('instructions'):
            ap.append('\\begin{paperinfo}原卷說明：' + m['instructions'].strip() + '\\end{paperinfo}')
        ap.append('\\begin{tabular}{llr}\\toprule 題號 & 主題（章） & 頁 \\\\ \\midrule')
        for q in m['questions']:
            ap.append(f"{q['label']} & 第~{q['chapter']}~章 & \\pageref{{px:{q['id']}}} \\\\")
        ap.append('\\bottomrule\\end{tabular}\n')
    open(os.path.join(gen, f'vol{vol}-papers.tex'), 'w').write('\n'.join(ap) + '\n')
    n = sum(len(m['questions']) for m in papers)
    print(f'vol{vol}: {len(papers)} papers, {n} questions, chapters {sorted(bych)}')

if __name__ == '__main__':
    main()
