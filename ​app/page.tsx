'use client';

import { useState } from 'react';

export default function Home() {
  // 家具の寸法
  const [width, setWidth] = useState<string>('');
  const [depth, setDepth] = useState<string>('');
  const [height, setHeight] = useState<string>('');

  // 搬入先のドア・通路の寸法
  const [doorWidth, setDoorWidth] = useState<string>('');
  const [doorHeight, setDoorHeight] = useState<string>('');

  // 計算結果の判定
  const [result, setResult] = useState<{
    diagonal: number;
    canPass: boolean;
    message: string;
  } | null>(null);

  const calculateTransport = (e: React.FormEvent) => {
    e.preventDefault();
    const w = parseFloat(width) || 0;
    const d = parseFloat(depth) || 0;
    const h = parseFloat(height) || 0;
    const dw = parseFloat(doorWidth) || 0;
    const dh = parseFloat(doorHeight) || 0;

    if (w <= 0 || d <= 0 || h <= 0) return;

    // 三平方の定理で立体対角線を計算 (√(w^2 + d^2 + h^2))
    const diagonal = Math.sqrt(w * w + d * d + h * h);

    // 簡易的な判定ロジック（最小の辺、または斜めの対角線がドアを通るか）
    // 最も細い辺がドアの幅・高さの小さい方より小さく、かつ対角線が許容範囲かなど
    const minSide = Math.min(w, d, h);
    const maxDoor = Math.max(dw, dh);
    const minDoor = Math.min(dw, dh);

    let canPass = false;
    let message = '';

    if (dw > 0 && dh > 0) {
      if (minSide <= minDoor && diagonal <= Math.sqrt(dw * dw + dh * dh)) {
        canPass = true;
        message = '諦めないで！斜め（対角線）に傾ければ搬入できる可能性が高いです！';
      } else {
        message = 'そのままではドアや通路の寸法をオーバーしている可能性があります。分解を検討してください。';
      }
    } else {
      message = '家具の立体対角線が計算できました。';
    }

    setResult({
      diagonal: Math.round(diagonal * 10) / 10,
      canPass,
      message,
    });
  };

  return (
    <main className="min-h-screen bg-slate-50 text-slate-800 p-4 sm:p-8">
      <div className="max-w-md mx-auto bg-white rounded-2xl shadow-xl p-6 sm:p-8 border border-slate-100">
        
        {/* ヘッダー */}
        <div className="text-center mb-6">
          <span className="bg-indigo-50 text-indigo-600 text-xs font-semibold px-3 py-1 rounded-full uppercase tracking-wider">
            家具の数学電卓
          </span>
          <h1 className="text-2xl font-bold mt-2 text-slate-900">
            搬入シミュレーター
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            諦めてた家具、三平方の定理で通るかもしれません。
          </p>
        </div>

        {/* フォーム */}
        <form onSubmit={calculateTransport} className="space-y-4">
          
          {/* 家具の寸法 */}
          <div className="bg-slate-50 p-4 rounded-xl border border-slate-200">
            <label className="block text-xs font-bold text-slate-700 mb-2">
              📦 家具のサイズ (cm)
            </label>
            <div className="grid grid-cols-3 gap-2">
              <div>
                <span className="text-[10px] text-slate-500">幅 (W)</span>
                <input
                  type="number"
                  placeholder="例: 80"
                  value={width}
                  onChange={(e) => setWidth(e.target.value)}
                  className="w-full mt-1 p-2 bg-white border border-slate-300 rounded-lg text-sm text-center focus:ring-2 focus:ring-indigo-500 outline-none"
                  required
                />
              </div>
              <div>
                <span className="text-[10px] text-slate-500">奥行 (D)</span>
                <input
                  type="number"
                  placeholder="例: 45"
                  value={depth}
                  onChange={(e) => setDepth(e.target.value)}
                  className="w-full mt-1 p-2 bg-white border border-slate-300 rounded-lg text-sm text-center focus:ring-2 focus:ring-indigo-500 outline-none"
                  required
                />
              </div>
              <div>
                <span className="text-[10px] text-slate-500">高さ (H)</span>
                <input
                  type="number"
                  placeholder="例: 180"
                  value={height}
                  onChange={(e) => setHeight(e.target.value)}
                  className="w-full mt-1 p-2 bg-white border border-slate-300 rounded-lg text-sm text-center focus:ring-2 focus:ring-indigo-500 outline-none"
                  required
                />
              </div>
            </div>
          </div>

          {/* ドア・通路の寸法 */}
          <div className="bg-slate-50 p-4 rounded-xl border border-slate-200">
            <label className="block text-xs font-bold text-slate-700 mb-2">
              🚪 通り道のサイズ (cm) <span className="font-normal text-slate-400">※任意</span>
            </label>
            <div className="grid grid-cols-2 gap-2">
              <div>
                <span className="text-[10px] text-slate-500">ドアの幅</span>
                <input
                  type="number"
                  placeholder="例: 75"
                  value={doorWidth}
                  onChange={(e) => setDoorWidth(e.target.value)}
                  className="w-full mt-1 p-2 bg-white border border-slate-300 rounded-lg text-sm text-center focus:ring-2 focus:ring-indigo-500 outline-none"
                />
              </div>
              <div>
                <span className="text-[10px] text-slate-500">ドアの高さ</span>
                <input
                  type="number"
                  placeholder="例: 190"
                  value={doorHeight}
                  onChange={(e) => setDoorHeight(e.target.value)}
                  className="w-full mt-1 p-2 bg-white border border-slate-300 rounded-lg text-sm text-center focus:ring-2 focus:ring-indigo-500 outline-none"
                />
              </div>
            </div>
          </div>

          {/* 計算ボタン */}
          <button
            type="submit"
            className="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-3 px-4 rounded-xl shadow-lg shadow-indigo-200 transition-all duration-200 text-sm"
          >
            数学で判定する
          </button>
        </form>

        {/* 結果表示エリア */}
        {result && (
          <div className="mt-6 p-4 rounded-xl bg-indigo-50 border border-indigo-100 animate-fadeIn">
            <div className="text-xs text-indigo-700 font-semibold mb-1">📐 計算結果</div>
            <div className="text-lg font-bold text-indigo-900 mb-2">
              立体対角線: <span className="text-2xl text-indigo-600">{result.diagonal}</span> cm
            </div>
            <p className="text-xs text-slate-700 leading-relaxed">
              {result.message}
            </p>
          </div>
        )}

      </div>
    </main>
  );
}
