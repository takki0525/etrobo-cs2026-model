# 日本語改訂版のトレーサビリティ

元モデルの全ID・要求と設計の関係・検証候補の関係・分析責務の割当・情報経路を保持。図の表示名を日本語化し、実装名は[対応表](実装名対応表.md)で照合する。以下は原版のコード名を用いた対応表。正式P2との未接続・情報不足は継続課題。

# 要求・分析・設計・実装・検証の対応 v1

基準：走行コード`07b26ca0d67dedf07a736cec14eda77f0d2eff1b`。静的照合。DS-Rは今回作成した暫定設計要求であり、正式提出版P2の要求IDではない。

## 今回作成した対応

| 暫定要求 | 分析責務 | 構成要素 | 振る舞い・情報契約 | コード（2026-Alpha基準） | 検証候補（未実施） |
|---|---|---|---|---|---|
| DS-R01 非同期交換 | タスク管理／走行経路作成 | WithStrategyExchange、StrategyExchange、transport | D04・D06 | robot_program/services/strategy_tree.py、robot_program/services/strategy_exchange.py、wireless_device/transport.py | TC-01 通信中のBT応答計測 |
| DS-R02 有効応答のみ受理 | タスク管理 | StrategyExchange、RaceContext | D05・D06・D08 | robot_program/services/strategy_exchange.py、shared_communication/protocol.py | TC-02 他mission、不正、期限後の応答 |
| DS-R03 一度だけ指令展開 | 走行体制御 | DeferredStrategySequence、execute_strategy、補償モジュール | D03・D07・D10 | robot_program/features/execute_strategy.py、robot_program/et_rally_compensation.py | TC-03 複数tickで子ノードの生成・登録回数 |
| DS-R04 直進と距離終了の分担 | 走行体制御 | Parallel、EtRallyRunByGyro、IsDistanceEarned | D03・D10 | robot_program/behaviours/et_rally_drive.py、robot_program/behaviours/conditions.py | TC-04 距離終了、次指令への移行、終了時の出力 |
| DS-R05 二段旋回 | 走行体制御 | EtRallySpinAroundByEncoder | D03・D09 | robot_program/behaviours/et_rally_drive.py | TC-05 片輪到達、両輪到達、仕上げ、進捗不足、terminate |
| DS-R06 未取得時の縮退 | タスク管理／走行体制御 | WaitForStrategy、DeferredStrategySequence | D07・D08 | robot_program/features/receive_strategy.py、robot_program/features/execute_strategy.py、robot_program/et_rally_fallback.py | TC-06 fallback有効／無効、固定経路も無効 |

モデル内ではD01のsatisfy／verify、D02のallocateで対応を保持。D03の依存関係は呼出し・生成・参照の向きに合わせる。D04は型付きポートとItemFlowを使用。D06/D10のライフラインは同じBlock型を参照。D07～10は構造要素へのモデルハイパーリンクを持つ。

## 正式提出済みP1～3からのつながりと差分

原本：`references/source-materials/2026-09-25_地区大会提出版/APL140ＭＳ＆ＡＤモード２Ａ・Ａ.pdf`。照合入口：`work/cs-pages1-3-gap-audit-v2/README.md`。元の要求名称・本文は正式PDFを正とし、下記は対応判断を要約する。

| 提出版の箇所 | 今回の設計での扱い | 修正・確定が必要な内容 |
|---|---|---|
| P3：タスク管理 | D02のWithStrategyExchange／RaceContext／WaitForStrategyへ割当 | 保持者と判断主体を区別。実走周回時間による判断は採用していない |
| P3：ヒントカード読取 | D02のReadHintCardへ割当 | 今回は通信への接続を示す。読取状態図の詳細は別候補 |
| P3：走行経路作成 | D02/D06のPC側Application・PlannerProcessへ割当 | PC計算と通信窓口の責務を分離。周回数はPC起動設定を正とする |
| P3：走行体制御 | D03/D07/D09/D10へ詳細化 | SEQ生成・実行・補償・各走行Behaviourを分ける |
| P2 RTE-08／09／10：送信失敗・再送・上限 | DS-R01／02、D06/D08で実装方式を表現 | 実装は走行体HINTS要求を最大3送信。PC側STRATEGYの単純な再送と同一ではない |
| P2 RTE-11：走行体側で攻略経路作成 | DS-R06、固定退避に変更する候補 | 固定ゴール経路はゲート情報からの攻略経路再計算ではない。旧RTE-11へsatisfyを付けない |
| P2 HNT-05：失敗時の距離・角度探索 | 今回の採用設計へ追加しない | 未実装の再撮影探索を削除・修正する候補 |
| P2 CTR-01／02／03：赤ゲート画像による補正 | 採用設計から除外 | ユーザーの削除方針に従う。ジャイロPID・機体ずれ補償で満たしたとは扱わない |
| P2 CTR-04：実走周回数のカウント | 事前に選んだ全周回SEQの一度実行へ変更する候補 | selected_rally_lapsは予定数。実走中のカウントと区別 |
| P2 CTR-05／06／07：周回測時・予測・継続判断 | 採用設計へ追加しない | 予定周回数の設定と、実走時間による判断を混同しない |

この表は改訂候補であり、旧要求をモデル内で承認済みとして変更したものではない。要求の正式改訂後に正式IDとDS-Rを統合し、今の対応を置き換える。

## 保存済みClaude 4～6枚目との対応

| 保存版の項目 | 今回の対応図・判断 |
|---|---|
| 4-1／4-2：責務・I/F | D02/D04/D05。取得・保持・計算・受理・生成・実行を区別 |
| 4-3：走行体制御の構造 | D03。現行SpinAroundByEncoder採用。補償はfactoryから生成前に呼ぶ |
| 5-0：PC側の詳細化対象外 | D06ではPCとの連携を含む。PC内部アルゴリズム詳細は後続候補 |
| 5-1～5-6：OneShot補正・状態・終了 | D09は確認できた現行旋回クラスで作成。OneShotの採用状態は情報不足 |
| 6枚目：OneShot／カメラ／LQI・比較 | 今回の設計図に性能実証や採用済みとして転記しない。制御モデルの別作業 |

## 情報不足と次の作業

- このHEADがCS大会で使う採用版かどうか。別PCのOneShot・カメラ補正のコード、採用コミット、設定が必要。
- 無線通信デバイスの製品名、無線規格、実機通信経路の構成。ソフトウェアのTCP接続は確認できる。
- 直進ノードはRUNNINGを返し、距離条件がParallelを成功させる。終了瞬間にモータ出力0となることは、ライブラリと実行基盤を含む追加確認が必要。設計図から自動停止を推定しない。
- 状態図はupdate内部のphase・フラグを抽象化したもの。状態間の遷移ごとに必ず別tickが必要という意味ではない。
- D06/D10は呼出し・データ返却・Status観測を要約した相互作用ビュー。全メッセージの実装APIや戻りイベントを一対一で表すものではない。
- 性能の合否値、通信の成功率・遅延、旋回精度、実走時間の生ログは不足。検証候補の合格を推測しない。
- 後続図候補：ReadHintCard状態図、PC経路生成アクティビティ、固定退避の詳細、座標変換・補償データフロー、直進制御の詳細。これらは今回10図で全面的に詳細化したものではない。
