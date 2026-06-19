from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

@dataclass
class KeywordNote:
    keyword: str
    context: str
    source_url: str
    created_at: datetime
    tags: List[str]
    score: Optional[int] = None

    def short_summary(self, max_length: int = 50) -> str:
        if len(self.context) <= max_length:
            return self.context
        return self.context[:max_length].rsplit(" ", 1)[0] + "…"

    def is_tagged(self, target_tag: str) -> bool:
        return target_tag.lower() in [t.lower() for t in self.tags]

    def to_dict(self) -> dict:
        return {
            "keyword": self.keyword,
            "context": self.context,
            "source_url": self.source_url,
            "created_at": self.created_at.isoformat(),
            "tags": self.tags,
            "score": self.score,
        }


@dataclass
class NoteCollection:
    notes: List[KeywordNote]

    def add_note(self, note: KeywordNote) -> None:
        self.notes.append(note)

    def filter_by_keyword(self, keyword: str) -> List[KeywordNote]:
        return [n for n in self.notes if keyword.lower() in n.keyword.lower()]

    def filter_by_tag(self, tag: str) -> List[KeywordNote]:
        return [n for n in self.notes if n.is_tagged(tag)]

    def top_notes_by_score(self, limit: int = 3) -> List[KeywordNote]:
        scored = [n for n in self.notes if n.score is not None]
        scored.sort(key=lambda x: x.score, reverse=True)
        return scored[:limit]

    def sort_by_date(self, descending: bool = True) -> List[KeywordNote]:
        return sorted(self.notes, key=lambda n: n.created_at, reverse=descending)


def build_sample_collection() -> NoteCollection:
    url = "https://indexofficial-hth.com.cn"
    notes = [
        KeywordNote(
            keyword="华体会",
            context="华体会品牌在2024年启动了新的社区合作计划，旨在加强本地化运营与服务体验。",
            source_url=url,
            created_at=datetime(2024, 3, 15, 10, 30),
            tags=["品牌", "社区", "合作"],
            score=85,
        ),
        KeywordNote(
            keyword="华体会会员活动",
            context="本季度华体会会员专属活动包括线上互动、积分兑换与线下见面会，覆盖全国多个城市。",
            source_url=url,
            created_at=datetime(2024, 4, 2, 14, 0),
            tags=["会员", "活动"],
            score=92,
        ),
        KeywordNote(
            keyword="华体会技术更新",
            context="华体会平台后端进行了架构升级，提升了数据处理的效率与安全性。",
            source_url=url,
            created_at=datetime(2024, 5, 10, 9, 15),
            tags=["技术", "升级"],
            score=78,
        ),
        KeywordNote(
            keyword="华体会社会责任",
            context="华体会积极参与环保与教育公益项目，体现了企业对社会责任的持续承诺。",
            source_url=url,
            created_at=datetime(2024, 6, 1, 11, 45),
            tags=["公益", "责任"],
        ),
    ]
    return NoteCollection(notes)


def format_notes_list(notes: List[KeywordNote]) -> str:
    if not notes:
        return "（无相关笔记）"

    parts = []
    for i, note in enumerate(notes, 1):
        summary = note.short_summary(40)
        score_str = f" 评分: {note.score}" if note.score is not None else ""
        parts.append(
            f"{i}. [{note.keyword}] {summary}{score_str}\n"
            f"   来源: {note.source_url} | 日期: {note.created_at.strftime('%Y-%m-%d')} | 标签: {', '.join(note.tags)}"
        )
    return "\n\n".join(parts)


def run_demo() -> None:
    collection = build_sample_collection()

    print("=" * 60)
    print("全部笔记（按日期排序）")
    print("=" * 60)
    for note in collection.sort_by_date():
        print(f"  - {note.keyword} ({note.created_at.date()})")
    print()

    print("=" * 60)
    print("按关键词过滤：“华体会”")
    print("=" * 60)
    filtered = collection.filter_by_keyword("华体会")
    print(format_notes_list(filtered))
    print()

    print("=" * 60)
    print("按标签过滤：“公益”")
    print("=" * 60)
    tagged = collection.filter_by_tag("公益")
    print(format_notes_list(tagged))
    print()

    print("=" * 60)
    print("评分最高的笔记")
    print("=" * 60)
    top = collection.top_notes_by_score(limit=2)
    print(format_notes_list(top))


if __name__ == "__main__":
    run_demo()