# Drawlib 地図描画モジュール (`drawlib.geo`) 設計計画書
(DRAWLIB GEOMAP MODULE PLAN)

- **作成日**: 2026-10-09
- **対象バージョン**: Drawlib 次期マイナーリリース (`v0.3.x`)
- **対象モジュール**:
  - `src/drawlib/geo.py` (公開ファサード)
  - `src/drawlib/_geo/` (内部データモデル・GeoJSONローダ・投影計算・描画エンジン)
  - `tools/dcli/codegen/map_download.py`, `map_normalize.py` (アセット取得・正規化ツール)
  - `tools/original_assets/maps/` (取得直後の生 GeoJSON データ)
  - `src/drawlib/_cached_assets/maps/` (開発・テスト用正規化済み GeoJSON データ)
  - `tests/drawlib/geo/` (単体テスト・ビジュアル検証テスト)

---

## 1. エグゼクティブサマリー & 背景 (Executive Summary & Background)

### 1.1. 背景と目的
ドッグフーディングユーザーより、「技術ドキュメント・アーキテクチャ構成図・プレゼンスライド内で地図を描画したい」という要望が寄せられた。
具体的には以下のユースケースが想定される：
1. **マルチリージョン・インフラ構成図**: 世界地図や日本地図をベースに、東京・大阪・US・欧州などのリージョン位置へ [`drawlib.icons`](file:///usr/local/google/home/yuichiito/git_github/drawlib/src/drawlib/icons.py)（GCPアイコンやサーバーアイコン）を配置し、[`drawlib.lines`](file:///usr/local/google/home/yuichiito/git_github/drawlib/src/drawlib/lines.py)（`line_curved` 等）でリージョン間通信やレプリケーションを表現する。
2. **地域別ハイライト・統計マップ（コロプレス図）**: 国別・都道府県別・市区町村（東京23区など）別に [`Styles`](file:///usr/local/google/home/yuichiito/git_github/drawlib/src/drawlib/styles.py) のデザイントークン（基本は `Styles.Neutral`、注目領域は `Styles.PrimaryFlat` 等）を適用して塗り分ける。

### 1.2. 基本方針（なぜ `geopandas` を使わず独自実装とするか）
1. **追加依存ゼロ（Pure Python 維持）**:
   - `geopandas`（および `GDAL`, `GEOS`, `PROJ` 等の巨大な C/C++ バイナリ依存）は導入せず、Python 標準の `json` + `pydantic` + `matplotlib.patches.PathPatch` のみで軽量・高速に実装する。
2. **`l4_canvas` パイプラインとの完全統合**:
   - 各地域のポリゴン（`Polygon` / `MultiPolygon`）を [`PathPatch`](file:///usr/local/google/home/yuichiito/git_github/drawlib/src/drawlib/_core/l4_canvas/_base.py#L29) として描画することで、既存の [`Style`](file:///usr/local/google/home/yuichiito/git_github/drawlib/src/drawlib/_core/l3_styles/__init__.py)（塗り・枠線幅・線種・透過）およびキャンバスのスケーリング（[`transform`](file:///usr/local/google/home/yuichiito/git_github/drawlib/src/drawlib/_core/l4_canvas/_base.py#L86-L101)）と100%互換にする。
3. **標準フォーマット GeoJSON (RFC 7946) + 内部独自データ構造 (`GeoData`)**:
   - 外部ファイルおよびプリセットアセットの保存形式は IETF 標準の **GeoJSON (RFC 7946)** とし、読み込み時に `drawlib` 独自の正規化データ構造（`GeoData` / `GeoElement` / `GeoPolygon`）へ変換する。
4. **統一された単一クラス (`GeoMap`) と `width, height` 規約**:
   - 世界（`World`）・国（`Countries.Japan`）・都市（`Cities.Tokyo`）・ユーザー独自 GeoJSON ファイルを区別せず、単一の `GeoMap` クラスで一貫して扱う。
   - サイズ指定は AI および人間にとって座標タプル `xy` と混同しにくくレイアウト計算が容易な **`width, height` 個別引数方式** に統一する。

---

## 2. アーキテクチャ設計 (Architecture Design)

### 2.1. ディレクトリ・モジュール構成

```text
src/drawlib/
├── geo.py                        # 公開ファサード (GeoMap, World, Countries, Cities, GeoData, GeoElement)
└── _geo/                         # 内部実装パッケージ
    ├── __init__.py               # 内部シンボル集約
    ├── _types.py                 # プリセット識別子 (World, Countries, Cities) とデータ構造 (GeoPolygon, GeoElement, GeoData)
    ├── _loader.py                # GeoJSON 読み込み・GeoData への正規化変換・エイリアス解決
    ├── _projection.py            # 緯度経度 -> キャンバス座標 (xy, width, height) 投影・クリッピング計算
    └── _geomap.py                # GeoMap クラス実装 (get_elements, set_style, set_styles, draw, get_element_xy 等)
```

### 2.2. アセット管理パイプライン（3段階構成）

```text
[1. 取得直後の生データ]               [2. 開発・検証用キャッシュ]               [3. リリース配信用 (仕様確定後)]
tools/original_assets/maps/   ──>   src/drawlib/_cached_assets/maps/   ──>   tools/release_assets/v0.3/maps/
- ne_50m_admin_0_countries          - world.geojson (754 KB, 242国)          - map_preset.zip としてパッケージ化
- japan.geojson                     - japan.geojson (372 KB, 47都道府県)     - オンデマンド取得 (l3_external)
- tokyo.geojson                     - tokyo.geojson (180 KB, 62市区町村)
  (./dcli codegen map で正規化)
```

- **フェーズ1（現在〜仕様確定まで）**: `src/drawlib/_cached_assets/maps/` に配置した `world.geojson`, `japan.geojson`, `tokyo.geojson` の3つを用いて実装・テストを行い、仕様を固める。
- **フェーズ2（リリース対応時）**: 仕様確定後、`tools/release_assets/v0.3/maps/` および [`_release_assets.py`](file:///usr/local/google/home/yuichiito/git_github/drawlib/src/drawlib/_release_assets.py) に登録し、フォントやアイコンと同様に自動ダウンロード対応とする。

---

## 3. データ構造設計 (`_geo/_types.py`, `_geo/_loader.py`)

### 3.1. プリセットターゲット定義

`World`, `Countries`, `Cities` を提供し、すべて共通のプリセットターゲット型 `GeoPreset` として `GeoMap` に渡せる設計とする。

```python
class WorldPreset(StrEnum):
    WORLD = "world"

World: Final[WorldPreset] = WorldPreset.WORLD

class Countries(StrEnum):
    Japan = "japan"
    JAPAN = "japan"

class Cities(StrEnum):
    Tokyo = "tokyo"
    TOKYO = "tokyo"

GeoTarget = WorldPreset | Countries | Cities | str | Path | dict[str, Any]
```
*(※ `Countries.Japan` のような PascalCase と `Countries.JAPAN` の UPPER_CASE の双方でアクセス可能にし、AI エージェントがどちらを書いても動作するようにする)*

### 3.2. `drawlib` 内部データ構造 (`GeoPolygon`, `GeoElement`, `GeoData`)

GeoJSON の `Polygon`（3重リスト）と `MultiPolygon`（4重リスト）の階層差やプロパティ名の揺れを、ロード時に以下の正規化モデルへ変換する。

```python
class GeoPolygon(BaseModel):
    """単一の閉じた陸地ポリゴン（外周リング + 内側の穴リング）"""
    model_config = ConfigDict(frozen=True)

    exterior: list[tuple[float, float]]          # [(lon, lat), ...]
    holes: list[list[tuple[float, float]]] = []  # 湖や飛び地などの穴リング

class GeoElement(BaseModel):
    """地図上の1つの構成要素（国・都道府県・市区町村・カスタム領域）"""
    model_config = ConfigDict(frozen=True)

    id: str                                      # 正規化識別子 (例: "Japan", "Tokyo", "Chiyoda")
    name: str                                    # 英語表示名 (例: "Japan", "Tokyo", "Chiyoda")
    name_ja: str = ""                            # 日本語名 (例: "日本", "東京都", "千代田区")
    group: str = ""                              # 地域グループ (例: "Asia", "Kanto", "23wards")
    group_ja: str = ""                           # 日本語グループ (例: "関東", "23区")
    aliases: tuple[str, ...] = ()                # 検索用別名リスト (ISOコード "JP", "JPN", 短縮名 "東京", "千代田" 等)
    polygons: tuple[GeoPolygon, ...]             # 構成ポリゴン群
    center_lonlat: tuple[float, float]           # ピン・ラベル配置用の本土代表座標 (lon, lat)
    bbox: tuple[float, float, float, float]      # (min_lon, min_lat, max_lon, max_lat)
    properties: dict[str, Any] = {}              # 元 GeoJSON の属性辞書

class GeoData(BaseModel):
    """正規化済み地図データコレクション"""
    model_config = ConfigDict(frozen=True)

    name: str
    elements: dict[str, GeoElement]              # canonical_key -> GeoElement
    bbox: tuple[float, float, float, float]      # 全体の (min_lon, min_lat, max_lon, max_lat)
    default_lon_range: tuple[float, float] | None = None
    default_lat_range: tuple[float, float] | None = None
```

### 3.3. 要素名の解決（エイリアス・大文字小文字吸収）
- `get_elements()` が返す正規化名は以下の通り人間・AIにとって最も直感的な英語名とする：
  - `World`: `"Japan"`, `"United States"`, `"United Kingdom"`, `"France"`, `"Germany"`, ...
  - `Countries.Japan`: `"Hokkaido"`, `"Aomori"`, ..., `"Tokyo"`, ..., `"Kyoto"`, `"Osaka"`, ..., `"Okinawa"` (全47都道府県)
  - `Cities.Tokyo`: `"Chiyoda"`, `"Chuo"`, `"Minato"`, `"Shinjuku"`, `"Shibuya"`, ..., `"Hachioji"`, ... (全62市区町村)
- 一方で、`set_style(element=...)` や `get_element_xy(element=...)` に渡す文字列は、以下をすべて内部のエイリアス辞書で同一要素に解決する：
  - 大文字・小文字違い（`"japan"`, `"JAPAN"`, `"tokyo"`）
  - ISO コード（`"JP"`, `"JPN"`, `"US"`, `"USA"`, `"JP-13"`）
  - 日本語名・短縮日本語名（`"日本"`, `"東京都"`, `"東京"`, `"千代田区"`, `"千代田"`）
- 存在しない要素名が指定された場合は、利用可能な要素の例を添えて `ValueError` を送出する。

---

## 4. 公開クラス `GeoMap` の API 仕様 (`_geo/_geomap.py`)

### 4.1. コンストラクタ

```python
class GeoMap:
    @validate_call
    def __init__(
        self,
        target: GeoTarget,
        *,
        style: Style | None = None,
        background_style: Style | None = None,
        id_key: str | None = None,
        name_key: str | None = None,
    ) -> None:
```
- `target`: `World`, `Countries.Japan`, `Cities.Tokyo`、またはカスタム `.geojson` ファイルのパス（`str | Path`）もしくは GeoJSON 辞書（`dict`）。
- `style`: 地図内の全要素に適用されるデフォルトスタイル。省略時（`None`）は `Styles.Neutral` をデフォルト適用する。
- `background_style`: 地図の描画枠（海・背景ボックス）のスタイル。`None`（デフォルト）の場合は背景矩形を描画せず陸地ポリゴンのみを描画する。指定された場合は描画領域全体に背景矩形を描画する。
- `id_key` / `name_key`: ユーザー独自の GeoJSON を読み込む際に `properties` から要素IDとして使うキー名（未指定時は `"name"` → `"id"` → `"N03_004"` → `"N03_001"` 等を自動探索）。

### 4.2. 要素の取得・フィルタリングメソッド

| メソッド | シグネチャ | 説明 |
| :--- | :--- | :--- |
| **`get_elements()`** | `() -> list[str]` | 現在有効なすべての要素名（例: `["Hokkaido", ..., "Okinawa"]`）をリストで返す。 |
| **`get_groups()`** | `() -> list[str]` | 利用可能なグループ名（例: Worldなら大陸名 `"Asia"` 等、Japanなら `"Kanto"` 等8地方、Tokyoなら `["23wards", "tama", "islands"]`）を返す。 |
| **`include_elements()`** | `(elements: str \| Sequence[str]) -> Self` | 指定した要素のみを描画対象に残す（例: 東アジアの数ヶ国のみ描画）。 |
| **`exclude_elements()`** | `(elements: str \| Sequence[str]) -> Self` | 指定した要素を描画対象から除外する（例: `exclude_elements("Antarctica")`）。 |
| **`include_groups()`** | `(groups: str \| Sequence[str]) -> Self` | 指定したグループに属する要素のみを描画対象に残す（例: 東京23区のみ描画 `include_groups("23wards")`、関東のみ描画 `include_groups("Kanto")`）。 |
| **`exclude_groups()`** | `(groups: str \| Sequence[str]) -> Self` | 指定したグループを描画対象から除外する（例: `exclude_groups("islands")`）。 |

### 4.3. スタイル設定メソッド

| メソッド | シグネチャ | 説明 |
| :--- | :--- | :--- |
| **`set_style()`** | `(element: str \| Sequence[str], style: Style) -> Self` | 単一の要素名（または要素名のリスト）に対して `Style` を設定する。 |
| **`set_styles()`** | `(styles: Mapping[str, Style]) -> Self` | `{要素名: Style}` の辞書で複数要素のスタイルを一括設定する。 |
| **`set_group_style()`**| `(group: str \| Sequence[str], style: Style) -> Self` | グループ単位（例: `"Kanto"`, `"Asia"`, `"23wards"`）で一括して `Style` を設定する。 |

### 4.4. 描画 & キャンバス座標取得メソッド

| メソッド | シグネチャ | 説明 |
| :--- | :--- | :--- |
| **`draw()`** | `(xy: Coordinate, width: PosFloat \| None = None, height: PosFloat \| None = None, *, lon_range: tuple[float, float] \| None = None, lat_range: tuple[float, float] \| None = None, scale: PosFloat = 1.0) -> Self` | キャンバス上の左下座標 `xy` を基準に、`width` / `height` のサイズで地図を描画する。 |
| **`get_element_xy()`** | `(element: str) -> Coordinate` | 直前の `draw()` における指定要素（国・都道府県・区）の代表点キャンバス座標 `(x, y)` を返す。 |
| **`lonlat_to_xy()`** | `(lon: float, lat: float) -> Coordinate` | 直前の `draw()` における任意の `(経度, 緯度)` に対応するキャンバス座標 `(x, y)` を返す。 |

---

## 5. 投影・サイズ計算・座標範囲（Viewport）の仕様 (`_geo/_projection.py`)

### 5.1. `width` / `height` とアスペクト比維持のルール
地図は縦横比が崩れると形状が不自然になるため、地図自体の自然なアスペクト比 $R = \frac{\Delta X_{\text{proj}}}{\Delta Y_{\text{proj}}}$（中心緯度 $\phi_c$ における $\cos(\phi_c)$ 補正後の縦横比）を常に維持する。

1. **`width` のみ指定（`height=None`）**:
   - 横幅を `width` とし、`height = width / R` を自動算出して描画する。
2. **`height` のみ指定（`width=None`）**:
   - 高さを `height` とし、`width = height * R` を自動算出して描画する。
3. **`width` と `height` の両方指定**:
   - `xy` を左下とする `width × height` の矩形領域内に、アスペクト比 $R$ を保ったまま最大サイズで内接（センタリング）させて描画する。
4. **`lon_range` / `lat_range` によるクリッピング**:
   - `lon_range=(min_lon, max_lon)` または `lat_range=(min_lat, max_lat)` が指定された場合、その経緯度ボックスを表示範囲とし、枠外にはみ出るポリゴンは描画領域（クリップパス）で綺麗に切り抜く。

### 5.2. プリセット地図のスマートなデフォルト座標範囲
`lon_range` / `lat_range` が省略された場合、離島の存在によって本土が極端に小さく潰れるのを防ぐため、プリセットごとに見栄えの良いデフォルト経緯度範囲を持つ（もちろん `lon_range` / `lat_range` を明示指定すれば任意の離島まで表示可能）：
- **`World`**: `lon_range=(-180.0, 180.0), lat_range=(-60.0, 84.0)`（南極を除いた主要大陸が美しく収まる範囲。南極を含めたい場合は `lat_range=(-90, 84)` で表示可能）
- **`Countries.Japan`**: `lon_range=(127.0, 146.0), lat_range=(26.0, 46.0)`（北海道〜九州・沖縄本島までがバランスよく収まる範囲。南鳥島154°Eや沖ノ鳥島20°Nによる余白肥大化を防止）
- **`Cities.Tokyo`**:
  - デフォルトは東京都本土（23区＋多摩地域：`lon_range=(138.9, 139.95), lat_range=(35.5, 35.92)`）が大きく見やすく表示される範囲とする。
  - `m.include_groups("23wards")` を呼んだ場合は、自動的に東京23区（`lon_range=(139.55, 139.93), lat_range=(35.53, 35.83)`）にぴったりズームフィットする。

---

## 6. コード使用イメージ (Usage Examples)

### 例1：世界地図で特定の国をハイライトし、リージョン間を矢印で結ぶ
```python
from drawlib.canvas import save, setup
from drawlib.geo import GeoMap, World
from drawlib.lines import line_curved
from drawlib.shapes import circle
from drawlib.styles import Styles

setup(width=160, height=90)

m = GeoMap(World, style=Styles.Neutral)
m.set_styles({
    "Japan": Styles.PrimaryFlat,
    "United States": Styles.SecondaryFlat,
    "Germany": Styles.AccentFlat,
})
m.draw((10, 10), width=140, height=70)

jp_xy = m.get_element_xy("Japan")
us_xy = m.get_element_xy("United States")
de_xy = m.get_element_xy("Germany")

line_curved(jp_xy, us_xy, bend=-0.25, arrow_head="<->", style=Styles.PrimaryBold)
line_curved(us_xy, de_xy, bend=-0.25, arrow_head="<->", style=Styles.SecondaryBold)

save()
```

### 例2：日本地図・東京23区マップの描画
```python
from drawlib.canvas import save, setup
from drawlib.geo import Cities, Countries, GeoMap
from drawlib.styles import Styles

setup(width=160, height=80)

# 左側：日本地図（関東を薄く色付け、東京と大阪を強調）
jp = GeoMap(Countries.Japan, style=Styles.Neutral)
jp.set_group_style("Kanto", style=Styles.PrimaryNeutral)
jp.set_style("Tokyo", style=Styles.PrimaryFlat)
jp.set_style("Osaka", style=Styles.SecondaryFlat)
jp.draw((10, 10), width=65, height=60)

# 右側：東京23区マップ（23区に絞って千代田・港・渋谷を強調）
tk = GeoMap(Cities.Tokyo, style=Styles.Neutral)
tk.include_groups("23wards")
tk.set_style(["Chiyoda", "Minato", "Shibuya"], style=Styles.PrimaryFlat)
tk.draw((85, 10), width=65, height=60)

save()
```

---

## 7. 実装ステップ (Implementation Steps)

1. **`src/drawlib/_geo/_types.py`**: `World`, `Countries`, `Cities` および `GeoPolygon`, `GeoElement`, `GeoData` の定義
2. **`src/drawlib/_geo/_loader.py`**: `_cached_assets/maps/` からのプリセット GeoJSON ロード、および任意 `.geojson` ファイル・辞書の正規化ローダ実装
3. **`src/drawlib/_geo/_projection.py`**: コサイン緯度補正付き投影、アスペクト比維持フィット、バウンディングボックス・クリップパス計算
4. **`src/drawlib/_geo/_geomap.py`**: `GeoMap` クラスの実装（`PathPatch` 描画、`transform` による `scale` 対応、`get_element_xy` / `lonlat_to_xy`）
5. **`src/drawlib/geo.py` & `src/drawlib/__init__.py`**: 公開ファサードの作成とエクスポート登録
6. **単体テスト & ビジュアル検証**:
   - `tests/drawlib/geo/test_geo.py` の作成と `./dcli test` 実行
   - `./dcli code-check all` のパス確認
   - `World`, `Countries.Japan`, `Cities.Tokyo` のレンダリング画像を生成し、`view_file` で視覚検査を実施
