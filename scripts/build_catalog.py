#!/usr/bin/env python3
"""知識ファイルの front matter を読み、検査と派生物の生成を行う。

外部依存なし（Python 3.9 以上）。理由は docs/adr/0004-metadata-schema.md を参照。

使い方:
    python3 scripts/build_catalog.py            # 検査 + 生成
    python3 scripts/build_catalog.py --check    # 検査のみ
    python3 scripts/build_catalog.py --base-url https://example.github.io/repo

生成物:
    catalog.json        全エントリのメタデータ
    patterns.json       パターンのみのメタデータ
    all-patterns.md     全パターン本文の連結（サイト上では /all-patterns.html）
    llms.txt            llmstxt.org 形式の目次
    llms-full.txt       全知識の本文を連結したプレーンテキスト
    _data/catalog.json  Jekyll のテンプレートから site.data.catalog として読む同じ内容

生成物はリポジトリにコミットしない（.gitignore 済み）。サイトのビルド時に生成する。
"""

from __future__ import annotations

import argparse
import json
import posixpath
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# 走査対象のディレクトリと、その表示名
KNOWLEDGE_DIRS = {
    "episodes": "Episodes",
    "heuristics": "Heuristics",
    "patterns": "Patterns",
    "sources": "Sources",
}

VALID_TYPES = {"episode", "heuristic", "pattern", "source"}
VALID_STATUS = {"draft", "reviewed", "stub"}
REQUIRED_KEYS = ("id", "type", "title")
# 他エントリの id を指すフィールド
LINK_KEYS = ("related", "sources", "episodes")

DEFAULT_BASE_URL = "https://kosuke-fujisawa.github.io/software-exploration-patterns"

# このスクリプトが生成するファイル（リンク検査の対象から外す）
GENERATED = {"catalog.json", "patterns.json", "all-patterns.md", "llms.txt", "llms-full.txt"}
# 検査しないディレクトリ
SKIP_DIRS = {".git", "_site", ".jekyll-cache", "_data"}

LINK_RE = re.compile(r"(\]\()([^)\s]+)(\))")


# --------------------------------------------------------------------------
# front matter パーサ（最小サブセット）
# --------------------------------------------------------------------------

def _strip_quotes(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def parse_front_matter(text: str) -> tuple[dict, str]:
    """front matter と本文を返す。

    対応する形:
        key: value
        key: []
        key: [a, b]
        key:
          - a
          - b
    ネストしたマッピングやブロックスカラーには対応しない。
    """
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, text

    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return {}, text

    meta: dict = {}
    current_list_key: str | None = None

    for raw in lines[1:end]:
        line = raw.rstrip()
        if not line.strip() or line.strip().startswith("#"):
            continue

        # リストの項目
        if line.startswith((" ", "\t")) and line.strip().startswith("- "):
            if current_list_key is not None:
                meta[current_list_key].append(_strip_quotes(line.strip()[2:].strip()))
            continue

        if ":" not in line:
            continue

        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip()
        current_list_key = None

        if value == "":
            # 後続の行がリスト項目になる
            meta[key] = []
            current_list_key = key
        elif value.startswith("[") and value.endswith("]"):
            inner = value[1:-1].strip()
            meta[key] = (
                [_strip_quotes(v.strip()) for v in inner.split(",") if v.strip()]
                if inner
                else []
            )
        else:
            meta[key] = _strip_quotes(value)

    body = "\n".join(lines[end + 1:]).lstrip("\n")
    return meta, body


# --------------------------------------------------------------------------
# 収集
# --------------------------------------------------------------------------

def collect_entries() -> list[dict]:
    """知識ファイルを集める。`_` 始まりと README.md は対象外。"""
    entries: list[dict] = []
    for dirname in KNOWLEDGE_DIRS:
        directory = REPO_ROOT / dirname
        if not directory.is_dir():
            continue
        for path in sorted(directory.glob("*.md")):
            # `_` 始まりはテンプレート、`.` 始まりは macOS などが作る隠しファイル
            if path.name.startswith(("_", ".")) or path.name == "README.md":
                continue
            meta, body = parse_front_matter(path.read_text(encoding="utf-8"))
            rel = path.relative_to(REPO_ROOT).as_posix()
            entries.append(
                {
                    "meta": meta,
                    "body": body,
                    "path": rel,
                    "dir": dirname,
                    "slug": path.stem,
                }
            )
    return entries


# --------------------------------------------------------------------------
# 検査
# --------------------------------------------------------------------------

def check(entries: list[dict]) -> list[str]:
    errors: list[str] = []
    seen_ids: dict[str, str] = {}

    for entry in entries:
        meta, path = entry["meta"], entry["path"]

        if not meta:
            errors.append(f"{path}: front matter がありません")
            continue

        for key in REQUIRED_KEYS:
            if not meta.get(key):
                errors.append(f"{path}: 必須フィールド '{key}' がありません")

        entry_id = meta.get("id")
        if entry_id:
            if entry_id != entry["slug"]:
                errors.append(
                    f"{path}: id '{entry_id}' がファイル名 '{entry['slug']}' と一致しません"
                )
            if entry_id in seen_ids:
                errors.append(f"{path}: id '{entry_id}' が {seen_ids[entry_id]} と重複しています")
            else:
                seen_ids[entry_id] = path

        entry_type = meta.get("type")
        if entry_type and entry_type not in VALID_TYPES:
            errors.append(
                f"{path}: type '{entry_type}' は未知の値です（{'/'.join(sorted(VALID_TYPES))}）"
            )

        status = meta.get("status")
        if status and status not in VALID_STATUS:
            errors.append(
                f"{path}: status '{status}' は未知の値です（{'/'.join(sorted(VALID_STATUS))}）"
            )

        for key in LINK_KEYS:
            value = meta.get(key, [])
            if isinstance(value, str):
                errors.append(f"{path}: '{key}' はリストで書いてください")

    # リンク先の存在確認（id が出揃ってから）
    known = set(seen_ids)
    for entry in entries:
        for key in LINK_KEYS:
            for target in entry["meta"].get(key, []) or []:
                if isinstance(target, str) and target not in known:
                    errors.append(
                        f"{entry['path']}: {key} の '{target}' に対応するエントリがありません"
                    )

    return errors



def check_links() -> list[str]:
    """Markdown 内の相対リンクが実在するかを確認する。

    GitHub 上でもサイト上でも同じリンクを使う構成なので、
    リンク切れは両方で同時に壊れる。外部依存なしで検査できる範囲として
    リポジトリ内のファイルを指すリンクだけを見る。
    """
    errors: list[str] = []
    for path in sorted(REPO_ROOT.rglob("*.md")):
        rel = path.relative_to(REPO_ROOT)
        if set(rel.parts) & SKIP_DIRS or path.name.startswith("."):
            continue
        if rel.as_posix() in GENERATED:
            continue

        text = path.read_text(encoding="utf-8")
        for match in LINK_RE.finditer(text):
            target = match.group(2)
            if target.startswith(("http://", "https://", "#", "mailto:")):
                continue
            target = target.split("#")[0]
            if not target:
                continue
            if not (path.parent / target).resolve().exists():
                errors.append(f"{rel.as_posix()}: リンク先 '{target}' が存在しません")
    return errors


# --------------------------------------------------------------------------
# 生成
# --------------------------------------------------------------------------

def to_record(entry: dict, base_url: str) -> dict:
    meta = entry["meta"]
    return {
        "id": meta.get("id", entry["slug"]),
        "type": meta.get("type", ""),
        "title": meta.get("title", entry["slug"]),
        "status": meta.get("status", "draft"),
        "tags": meta.get("tags", []) or [],
        "related": meta.get("related", []) or [],
        "sources": meta.get("sources", []) or [],
        "episodes": meta.get("episodes", []) or [],
        "created": meta.get("created", ""),
        "updated": meta.get("updated", ""),
        "summary": _first_sentence(entry["body"]),
        "path": entry["path"],
        # サイト内の位置。Liquid 側で relative_url フィルタに通して使う
        "site_path": f"/{entry['dir']}/{entry['slug']}.html",
        "url": f"{base_url}/{entry['dir']}/{entry['slug']}.html",
    }


def write(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")
    print(f"generated: {path.relative_to(REPO_ROOT)}")


def generate(entries: list[dict], base_url: str, out_dir: Path) -> None:
    records = [to_record(e, base_url) for e in entries]
    patterns = [e for e in entries if e["meta"].get("type") == "pattern"]

    counts = {key: 0 for key in ("pattern", "heuristic", "episode", "source")}
    for record in records:
        if record["type"] in counts:
            counts[record["type"]] += 1

    catalog = {
        "name": "Software Exploration Patterns",
        "description": "ソフトウェア開発の「探索知」を共同で蓄積・更新する Living Knowledge Base",
        "license": "CC0-1.0",
        "base_url": base_url,
        "count": len(records),
        "counts": counts,
        "entries": records,
    }
    catalog_json = json.dumps(catalog, ensure_ascii=False, indent=2) + "\n"

    write(out_dir / "catalog.json", catalog_json)

    # Jekyll のテンプレートから site.data.catalog として参照する。
    # id からタイトル・URL を引くために使うので、HTML 側に知識を書かずに済む。
    data_dir = out_dir / "_data"
    data_dir.mkdir(exist_ok=True)
    write(data_dir / "catalog.json", catalog_json)

    pattern_ids = {e["meta"].get("id") for e in patterns}
    write(
        out_dir / "patterns.json",
        json.dumps(
            [r for r in records if r["id"] in pattern_ids],
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
    )

    # all-patterns.md（サイト上では /all-patterns.html として読める）
    parts = [
        "# 全パターン",
        "",
        "`scripts/build_catalog.py` が自動生成したページです。編集しても次のビルドで上書きされます。",
        "個々のパターンは [patterns/](patterns/) にあります。",
        "",
    ]
    for entry in patterns:
        meta = entry["meta"]
        parts.append("---")
        parts.append("")
        parts.append(f"<!-- source: {entry['path']} -->")
        parts.append("")
        parts.append(f"## {meta.get('title', entry['slug'])}")
        parts.append("")
        parts.append(
            f"id: `{meta.get('id', '')}` / status: `{meta.get('status', 'draft')}`"
            + (f" / tags: {', '.join(meta.get('tags', []) or [])}" if meta.get("tags") else "")
        )
        parts.append("")
        # 本文の先頭見出しは ## を重ねないよう1段下げる
        rebased = _rebase_links(_strip_first_heading(entry["body"]), entry["dir"])
        parts.append(_demote_headings(rebased))
        parts.append("")
    write(out_dir / "all-patterns.md", "\n".join(parts))

    # llms.txt — 目次（llmstxt.org 形式）
    lines = [
        "# Software Exploration Patterns",
        "",
        "> ソフトウェア開発における「探索知」（ズレ・未知・リスクに早く気づき、理解を更新するための知識）を"
        "共同で蓄積・更新する Living Knowledge Base。要求工学・テスト・QA・アジャイル・UX・PdM などに"
        "分散した知識を横断的に整理している。",
        "",
        "掲載内容は検証済みの正解ではなく、更新され続ける途中の知識である。"
        "ライセンスは CC0 1.0。全文は llms-full.txt にある。",
        "",
    ]
    for dirname, label in KNOWLEDGE_DIRS.items():
        group = [e for e in entries if e["dir"] == dirname]
        if not group:
            continue
        lines.append(f"## {label}")
        lines.append("")
        for entry in group:
            r = to_record(entry, base_url)
            summary = _first_sentence(entry["body"])
            lines.append(f"- [{r['title']}]({r['url']}): {summary}" if summary else f"- [{r['title']}]({r['url']})")
        lines.append("")
    write(out_dir / "llms.txt", "\n".join(lines))

    # llms-full.txt — 全文
    full = [
        "# Software Exploration Patterns — 全文",
        "",
        f"出典: {base_url}/ （CC0 1.0）",
        "自動生成されたファイルです。正本は各 Markdown ファイルです。",
        "",
    ]
    for dirname, label in KNOWLEDGE_DIRS.items():
        group = [e for e in entries if e["dir"] == dirname]
        if not group:
            continue
        full.append(f"# {label}")
        full.append("")
        for entry in group:
            meta = entry["meta"]
            full.append(f"## {meta.get('title', entry['slug'])}")
            full.append("")
            full.append(f"id: {meta.get('id', '')}")
            full.append(f"type: {meta.get('type', '')}")
            full.append(f"status: {meta.get('status', 'draft')}")
            full.append(f"source: {entry['path']}")
            full.append("")
            full.append(
                _rebase_links(
                    _strip_first_heading(entry["body"]),
                    entry["dir"],
                    prefix=f"{base_url}/",
                    to_html=True,
                ).strip()
            )
            full.append("")
    write(out_dir / "llms-full.txt", "\n".join(full))


def _rebase_links(body: str, entry_dir: str, prefix: str = "", to_html: bool = False) -> str:
    """本文中の相対リンクを、連結後の出力から見た位置に書き換える。

    各ファイルの相対リンクは自分のディレクトリ基準で書かれているため、
    リポジトリルートに連結すると壊れる。これを直す。
    """

    def repl(match: re.Match) -> str:
        target = match.group(2)
        if target.startswith(("http://", "https://", "#", "mailto:", "/")):
            return match.group(0)

        anchor = ""
        if "#" in target:
            target, _, fragment = target.partition("#")
            anchor = "#" + fragment

        trailing_slash = target.endswith("/")
        resolved = posixpath.normpath(posixpath.join(entry_dir, target))
        if trailing_slash:
            resolved += "/"
        elif to_html and resolved.endswith(".md"):
            resolved = resolved[: -len(".md")] + ".html"

        return f"{match.group(1)}{prefix}{resolved}{anchor}{match.group(3)}"

    return LINK_RE.sub(repl, body)


def _strip_first_heading(body: str) -> str:
    """本文先頭の `# 見出し` を落とす（タイトルは別に出力しているため）。"""
    lines = body.splitlines()
    for i, line in enumerate(lines):
        if line.strip() == "":
            continue
        if line.startswith("# "):
            return "\n".join(lines[i + 1:]).lstrip("\n")
        break
    return body


def _demote_headings(body: str) -> str:
    """`##` 以下の見出しを1段下げる（連結ページで階層が壊れないように）。"""
    out = []
    in_code = False
    for line in body.splitlines():
        if line.lstrip().startswith("```"):
            in_code = not in_code
        if not in_code and line.startswith("#"):
            line = "#" + line
        out.append(line)
    return "\n".join(out)


def _first_sentence(body: str) -> str:
    """本文から1行の要約を取り出す（引用ブロックと見出しを飛ばす）。"""
    for line in body.splitlines():
        s = line.strip()
        if not s or s.startswith(("#", ">", "-", "|", "`")):
            continue
        return s if len(s) <= 120 else s[:117] + "..."
    return ""


# --------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="検査のみ行い、生成しない")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL, help="サイトのベース URL")
    parser.add_argument("--out", default=str(REPO_ROOT), help="生成物の出力先ディレクトリ")
    args = parser.parse_args()

    entries = collect_entries()
    print(f"{len(entries)} 件の知識ファイルを読み込みました")

    errors = check(entries) + check_links()
    if errors:
        print("", file=sys.stderr)
        for error in errors:
            print(f"ERROR {error}", file=sys.stderr)
        print(f"\n{len(errors)} 件の問題が見つかりました", file=sys.stderr)
        return 1
    print("front matter と内部リンクの検査: 問題なし")

    if args.check:
        return 0

    generate(entries, args.base_url.rstrip("/"), Path(args.out).resolve())
    return 0


if __name__ == "__main__":
    sys.exit(main())
