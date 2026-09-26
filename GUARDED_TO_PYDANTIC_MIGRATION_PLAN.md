# Drawlib Guarded to Pydantic Full Migration Plan

## 1. 背景と目的 (Background & Motivation)

### 1.1. 現行アーキテクチャ (`@guarded` + 手書きカスタム型) の課題

1. **エラーの握りつぶしと `sys.exit(1)` による AI 自己修正の阻害**:
   - 現行の `@guarded` は例外発生時にスタックトレースを短縮し、ユーザーコードのファイル名と行番号をログ出力して `sys.exit(1)` でプロセスを終了します。
   - これは手動実行する人間のコンソール出力をすっきりさせる意図で設計されたものですが、**「AI エージェントにコードを書かせ、エラー時に自己修正（Run ➔ Error ➔ Fix）させる」現在の開発思想においては致命的な障害** となっています。
   - `sys.exit(1)` されると、AI は例外型（`ValidationError`）やどのパラメータがどのような理由（`Input should be greater than 0` 等）で弾かれたのかという構造化情報を直接受け取れず、正確な自己修正が著しく困難になります。

2. **手書きバリデータ関数の肥大化（車輪の再発明）**:
   - `src/drawlib/_core/l2_types_/` にて、`validate_coordinate`（`isinstance` や `len == 2` の泥臭いチェック）、`validate_alpha`（`0 <= v <= 1` チェック）、`validate_literal`（独自集合走査とメッセージ生成）など、多数の手書き Python 関数が記述されています。
   - Pydantic v2 はこれらのバリデーションを Rust コア（`pydantic-core`）で超高速かつ標準的に備えており、手書きコードは不要な保守コストとなっています。

3. **IDE 表示と型定義の二重管理**:
   - 関数の引数に `xy: TypeCoordinate`, `halign: TypeHAlign` などの内部型エイリアスを記述していたため、IDE（VS Code / Pyright / Cursor）でホバーした際に「`TypeCoordinate` って何？タプル？オブジェクト？」と直感的にわかりにくい状態でした。
   - その結果、`tools/scripts/check_docstring.py` を作成して「関数の型アノテーションは `TypeCoordinate` だが、docstring には `tuple[float, float]` と書かなければならない」という歪んだ二重管理を強制していました。

4. **寛容な正規化（サニタイズ）の欠如**:
   - 角度（`angle`）に `-90`（時計回り）や `450`（1回転+90度）を渡すと、数学的には明確であるにもかかわらず `ValueError` で即座にエラーとなっていました。
   - AI や人間が直感的に書いたコードを寛容に受け入れ、ライブラリ側で数学的に正しい標準形（`0.0 <= angle < 360.0`）へ自動正規化する仕組みが求められています。

---

### 1.2. 移行のゴール

1. **完全な例外送出（Fail-Fast & AI Self-Healing）**:
   - `@guarded` による `sys.exit(1)` を全廃し、Pydantic 標準の `ValidationError` をそのまま raise。
   - AI エージェントが引数名・不正値・期待形式をピンポイントで把握し、1手でコードを自動修正できるようにする。
2. **IDE 上での原始的表示（Primitive-First）と厳密バリデーションの両立**:
   - 関数シグネチャのホバー表示で `(x, y)` や `float` などの原始的型が表示され、一目で使い方がわかるようにする。
3. **寛容な自動正規化（Forgiving Normalization）**:
   - 角度の循環正規化（`450 -> 90`, `-270 -> 90`）や、リスト `[x, y]` からタプル `(x, y)` への自動変換を Pydantic の `BeforeValidator` で自動処理する。
4. **手書き検証ロジックの完全撤廃**:
   - `l2_types_` の手書き検証関数を全廃し、Pydantic の `Field` 制約・組み込み型・`BeforeValidator` のみで宣言的に記述する。

---

## 2. コア設計原則 (Core Principles)

1. **AI-First: ValidationError を第一級市民とする**:
   - ライブラリ関数は一切の `sys.exit(1)` を行わない。不適切な引数は即座に `pydantic.ValidationError` を送出する。
   - CLI ツール（`drawlib export`, `drawlib build`）で人間向けに表示したい場合のみ、CLI の最上位層（エントリーポイント）でキャッチしてフォーマットする。
2. **Primitive IDE Ergonomics (原始的型表示の優先)**:
   - PEP 593 (`Annotated[T, ...]`) を徹底活用する。静的型チェッカー（Pyright/IDE）は第1引数の `T`（`tuple[float, float]` や `float`）を表示し、実行時は Pydantic が追加検証・正規化を行う。
3. **Forgiving by Default (寛容な正規化)**:
   - 幾何学・色彩的に意味が一意に定まる入力（角度の剰余、リストからタプルへの変換、RGB から RGBA への補完等）はエラーにせず、Pydantic 層で標準形に変換して関数本体へ渡す。
4. **Clean Naming (Typeプレフィックスの廃止)**:
   - `TypeCoordinate` ➔ `Coordinate`
   - `TypeAngle` ➔ `Angle`
   - `TypeAlpha` ➔ `Alpha`
   - `TypePosFloat` ➔ `PosFloat`
   - `TypeColor` ➔ `Color`
   - `TypeHAlign` ➔ `HAlign`
   - （※後方互換性のため、`l2_types.py` で旧名エイリアスを一定期間保持）

---

## 3. 詳細アーキテクチャ仕様 (Detailed Architecture Specifications)

### 3.1. デコレータ刷新: `@guarded` の解体

#### 変更前 (`src/drawlib/_core/l1_core/_decorator.py`)
```python
def guarded(caller: Callable[P, R]) -> Callable[P, R]:
    validated_caller = None
    pydantic_config = ConfigDict(arbitrary_types_allowed=True)

    @functools.wraps(caller)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        nonlocal validated_caller
        if validated_caller is None:
            validated_caller = validate_call(config=pydantic_config)(caller)

        if dutil_settings.is_developer_debug_mode():
            return validated_caller(*args, **kwargs)

        try:
            return validated_caller(*args, **kwargs)
        except Exception as e:
            # スタックトレースを短縮してログ出力
            sys.exit(1)  # ← AIの自己修正を妨げていた原因
    return wrapper
```

#### 変更後 (`src/drawlib/_core/l1_core/_decorator.py`)
```python
"""Drawlib validation decorator module."""

from pydantic import ConfigDict, validate_call

# Standard configuration: arbitrary types (like PIL.Image, Matplotlib objects) allowed
VALIDATE_CONFIG = ConfigDict(arbitrary_types_allowed=True)

# Standard decorator for all public canvas/shape/style functions
guarded = validate_call(config=VALIDATE_CONFIG)
```
* **解説**:
  - `sys.exit(1)` や `try ... except` を完全に撤廃。
  - `guarded` 自体を `validate_call(config=VALIDATE_CONFIG)` のインスタンスとする。
  - これにより、コードベース内に存在する約 2,000 箇所の `@guarded`（Phosphor/GCP アイコン群を含む）が一挙に Pydantic の生のエラー出力に対応し、例外発生時は `ValidationError` が自然に raise されます。

---

### 3.2. ジオメトリ型 (`src/drawlib/_core/l2_types_/_geometry.py`)

#### 変更前: 手書きの型判定・長さチェック
```python
def validate_coordinate(v: Any) -> tuple[float, float]:
    if not isinstance(v, (tuple, list)) or len(v) != 2:
        raise ValueError(f"Coordinate must be a tuple of 2 floats. But {v} is given.")
    return (float(v[0]), float(v[1]))

TypeCoordinate = Annotated[tuple[float, float], AfterValidator(validate_coordinate)]
...
```

#### 変更後: 寛容な正規化（List -> Tuple, 数値変換）
```python
"""Geometry type definitions for drawlib."""

from __future__ import annotations
from typing import Annotated, Any
from pydantic import BeforeValidator

def normalize_coordinate(v: Any) -> tuple[float, float]:
    """Normalize input coordinate to a 2-tuple of floats.
    
    Accepts (x, y) or [x, y] with int/float elements.
    """
    if not isinstance(v, (tuple, list)) or len(v) != 2:
        raise ValueError(f"Coordinate must be a sequence of 2 numbers (x, y). But {v} is given.")
    return (float(v[0]), float(v[1]))

Coordinate = Annotated[tuple[float, float], BeforeValidator(normalize_coordinate)]
Coordinates = list[Coordinate]

Bezier2 = tuple[Coordinate, Coordinate]
Bezier3 = tuple[Coordinate, Coordinate, Coordinate]
PathPoint = Coordinate | Bezier2 | Bezier3
PathPoints = list[PathPoint]

# Backward compatibility aliases
TypeCoordinate = Coordinate
TypeCoordinates = Coordinates
TypeBezier2 = Bezier2
TypeBezier3 = Bezier3
TypePathPoint = PathPoint
TypePathPoints = PathPoints
```
* **IDE での表示**: `tuple[float, float]`
* **受け入れ**:
  - `(10, 20)` ➔ `(10.0, 20.0)`
  - `[10, 20]` (リスト) ➔ `(10.0, 20.0)`
  - `(10.5, 20.2)` ➔ `(10.5, 20.2)`
* **拒否**:
  - `(10,)`, `(10, 20, 30)`, `"10, 20"`, `10` ➔ `ValidationError`

---

### 3.3. スタイル型 (`src/drawlib/_core/l2_types_/_style.py`)

#### 角度の自動循環正規化 (`450 -> 90`, `-270 -> 90`)
Python の `% 360.0` 演算子を利用し、負数や 360度以上の入力を安全に `[0.0, 360.0)` にマッピングします。

```python
"""Style type definitions for drawlib."""

from __future__ import annotations
from typing import Annotated, Any, Literal
from pydantic import BeforeValidator, Field

def normalize_angle(v: Any) -> float:
    """Normalize angle in degrees to [0.0, 360.0) via modulo arithmetic.
    
    Examples:
        450.0 -> 90.0
        -90.0 -> 270.0
        -270.0 -> 90.0
        360.0 -> 0.0
    """
    return float(v) % 360.0

def normalize_angle90(v: Any) -> float:
    """Normalize angle in degrees to [0.0, 90.0)."""
    return float(v) % 90.0

Angle = Annotated[float, BeforeValidator(normalize_angle)]
Angle90 = Annotated[float, BeforeValidator(normalize_angle90)]

# Alpha: 0.0 <= alpha <= 1.0 (Pydantic 標準の Field 制約)
Alpha = Annotated[float, Field(ge=0.0, le=1.0)]

# Bend: -2.0 < bend < 2.0 (Pydantic 標準の Field 制約)
Bend = Annotated[float, Field(gt=-2.0, lt=2.0)]

# Color: RGB / RGBA タプルまたは Hex 文字列を常に RGBA (r, g, b, a) に自動正規化
def normalize_color(v: Any) -> tuple[int, int, int, float]:
    """Normalize RGB/RGBA tuple, list, or Hex string to RGBA (r, g, b, a).
    
    If RGB is provided, alpha defaults to 1.0.
    If explicit alpha property (e.g. shape_fill_alpha) is specified later in Style/Canvas,
    that alpha overrides this 'a' value at rendering time.
    """
    if isinstance(v, str):
        from drawlib._utils._color import get_rgba_from_hexcode
        return get_rgba_from_hexcode(v)

    if isinstance(v, (tuple, list)):
        if len(v) == 3:
            return (int(v[0]), int(v[1]), int(v[2]), 1.0)
        elif len(v) == 4:
            return (int(v[0]), int(v[1]), int(v[2]), float(v[3]))

    raise ValueError(f"Color must be RGB (r, g, b) or RGBA (r, g, b, a) tuple/list. But {v} is given.")

Color = Annotated[tuple[int, int, int, float], BeforeValidator(normalize_color)]
ColorRGB = tuple[int, int, int]
ColorRGBA = tuple[int, int, int, float]

# Literals: 手書き validate_literal を全廃し、Pydantic 標準 Literal を使用
HAlign = Literal["left", "center", "right"]
VAlign = Literal["bottom", "center", "top"]
LineStyle = Literal["solid", "dashed", "dotted", "dashdot"]
ArrowHead = Literal["", "->", "<-", "<->"]
TailEdge = Literal["left", "top", "right", "bottom"]
IconStyle = Literal["thin", "light", "regular", "bold", "fill"]
Size = Annotated[float, Field(ge=0.0)] | Literal["small", "medium", "large"]

# Backward compatibility aliases
TypeAngle = Angle
TypeAngle90 = Angle90
TypeAlpha = Alpha
TypeBend = Bend
TypeColor = Color
TypeColorRGB = ColorRGB
TypeColorRGBA = ColorRGBA
TypeHAlign = HAlign
TypeVAlign = VAlign
TypeLineStyle = LineStyle
TypeArrowHead = ArrowHead
TypeTailEdge = TailEdge
TypeIconStyle = IconStyle
TypeSize = Size
```

---

### 3.4. プリミティブ型 (`src/drawlib/_core/l2_types_/_primitive.py`)

手動のラッパーを整理し、Pydantic `Field` による宣言的制約に統一します。

```python
"""Primitive type definitions for drawlib."""

from __future__ import annotations
from typing import Annotated
from pydantic import Field

# Integers
PosInt = Annotated[int, Field(ge=0)]
NegInt = Annotated[int, Field(le=0)]
NumVertex = Annotated[int, Field(ge=3)]

# Floats
PosFloat = Annotated[float, Field(ge=0.0)]
NegFloat = Annotated[float, Field(le=0.0)]

# Backward compatibility aliases
TypeBool = bool
TypeInt = int
TypePosInt = PosInt
TypeNegInt = NegInt
TypeNumVertex = NumVertex
TypeFloat = float
TypePosFloat = PosFloat
TypeNegFloat = NegFloat
TypeStr = str
```

---

### 3.5. 画像型 (`src/drawlib/_core/l2_types_/_image.py`)

```python
"""Image type definitions for drawlib."""

from __future__ import annotations
from typing import Annotated, Literal
from pydantic import Field

ImageFormat = Literal["jpg", "png", "webp", "pdf"]
ImageZoom = Annotated[float, Field(gt=0.0)]
ImageQuality = Annotated[int, Field(ge=0, le=100)]
ImageResample = Literal["nearest", "box", "bilinear", "hamming", "bicubic", "lanczos"]

# Backward compatibility aliases
TypeImageFormat = ImageFormat
TypeImageZoom = ImageZoom
TypeImageQuality = ImageQuality
TypeImageResample = ImageResample
```

---

### 3.6. ユーティリティ型 (`src/drawlib/_core/l2_types_/_utils.py`)

- `validate_literal` 関数は不要となるため廃止（非推奨として空の実装または削除）。

---

## 4. 影響範囲と移行対象ファイル一覧

| カテゴリ | ファイルパス | 主な改修内容 |
| :--- | :--- | :--- |
| **デコレータ** | `src/drawlib/_core/l1_core/_decorator.py` | `sys.exit(1)` を廃止し、`validate_call(config=...)` を直接代入 |
| **型定義** | `src/drawlib/_core/l2_types_/_geometry.py` | `Coordinate`, 角度正規化, 命名整理, 旧名エイリアス提供 |
|  | `src/drawlib/_core/l2_types_/_style.py` | `Angle`, `Alpha`, `Color`, リテラル標準化, 旧名エイリアス提供 |
|  | `src/drawlib/_core/l2_types_/_primitive.py` | `PosFloat`, `PosInt` 等の Pydantic Field 統一 |
|  | `src/drawlib/_core/l2_types_/_image.py` | `ImageFormat`, `ImageResample` の標準 Literal 化 |
|  | `src/drawlib/_core/l2_types_/_utils.py` | 不要となった手書き検証関数のクリーンアップ |
|  | `src/drawlib/_core/l2_types.py` | 新命名のエクスポートと後方互換エイリアスの re-export |
| **スタイルモデル** | `src/drawlib/_core/l3_styles/_style_models.py` | `Style` の各属性が新しい型アノテーションにより自動正規化されることを確認 |
| **検証ツール** | `tools/scripts/check_docstring.py` | シグネチャが標準型に移行するため、不要ルールの緩和または新仕様への適応 |
| **テスト** | `tests/l1_core/test_decorator.py` | `sys.exit(1)` 依存テストを削除、`ValidationError` 送出テストに更新 |
|  | `tests/l2_types/test_geometry.py` | `[10, 20]` リストからタプルへの正規化テストの追加 |
|  | `tests/l2_types/test_style.py` | `450 -> 90`, `-270 -> 90` 等の角度正規化テストの追加 |

---

## 5. 段階的実装ロードマップ (Phased Execution Plan)

### フェーズ 1: 型定義 (`l2_types_`) の刷新と正規化の実装
1. `_geometry.py` の更新:
   - `normalize_coordinate` を実装（リストやタプルの受け入れ、要素数2個の検証、float 変換）。
   - `Coordinate = Annotated[tuple[float, float], BeforeValidator(normalize_coordinate)]` を定義。
   - `Bezier2`, `Bezier3`, `PathPoint` を整理。
2. `_style.py` の更新:
   - `normalize_angle` (`v % 360.0`), `normalize_angle90` (`v % 90.0`) を実装。
   - `normalize_color` を実装（RGB ➔ RGBA (A=1.0) 補完、Hex ➔ RGBA 変換）。
   - `Alpha`, `Bend`, `Color`, `Literal` 定義を Pydantic 標準に置換。
3. `_primitive.py`, `_image.py` の更新。
4. `_core/l2_types.py` で新旧両方の型シンボルを re-export。
5. `tests/l2_types/` のテストケースを拡充（角度正規化テスト、リスト座標テスト、RGB->RGBA正規化テストの追加）。

### フェーズ 2: デコレータ (`_decorator.py`) の Pydantic 標準化
1. `_decorator.py` をリファクタリング:
   - `guarded = validate_call(config=ConfigDict(arbitrary_types_allowed=True))` に置き換え。
   - `sys.exit(1)` および `inspect.stack()` による短縮ロギングを撤廃。
2. `tests/l1_core/test_decorator.py` の更新:
   - パラメータ不正時に Pydantic の `ValidationError` が直接送出されることを検証。
   - `test_guarded_non_developer_mode_intercepts_exception` などの `sys.exit(1)` 前提テストを廃止。

### フェーズ 3: Docstring チェッカーと保守スクリプトの調整
1. `tools/scripts/check_docstring.py`:
   - `TypeCoordinate` 等の独自型がシグネチャから段階的に標準型（`tuple[float, float]`）へ置き換わるため、チェッカーの動作を整合。
2. `./dcli check all` を実行し、全静的解析（Ruff, Ty, docstring check）をパスすることを確認。

### フェーズ 4: 全体結合検証とテスト実行
1. 全ユニットテストを実行（`uv run pytest tests/`）。
2. `Style` や `canvas.arc`, `canvas.circle` 等に異常値（`radius=-10`, `xy=[1, 2, 3]`）を渡した際に、明確な `ValidationError` が raise されることを確認。
3. 角度に `450` や `-270` を渡した描画コードが、エラーにならず `90.0` として正常描画されることを確認。

---

## 6. AI 開発者体験（DX）の向上シミュレーション

### シナリオ: AI が誤った型のパラメータを指定した場合

#### これまで (Before)
```bash
$ uv run python scratch/test_diagram.py
CRITICAL drawlib - ValueError at file:"scratch/test_diagram.py", line:"15"
CRITICAL drawlib - Coordinate must be a tuple of 2 floats. But (10, 20, 30) is given.
Process exited with code 1
```
* **課題**: 例外が握りつぶされ、プロセスが強制終了。AI エージェントが pytest やインプロセス実行している場合、テストプロセスごと死んでしまう。

#### これから (After)
```python
pydantic_core._pydantic_core.ValidationError: 1 validation error for circle
xy
  Coordinate must be a sequence of 2 numbers (x, y). But (10, 20, 30) is given. [type=value_error, input_value=(10, 20, 30), input_type=tuple]
```
* **効果**:
  - Python 標準の例外としてインプロセスで捕捉可能。
  - エラーの発生関数（`circle`）、対象引数（`xy`）、渡された値（`(10, 20, 30)`）が機械可読な構造化情報として得られるため、AI は即座にコードを自己修正できる。
