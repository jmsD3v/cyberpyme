from dataclasses import dataclass, field


def risk_level_for(score: float) -> str:
    if score >= 80:
        return "BAJO"
    if score >= 60:
        return "MEDIO"
    if score >= 40:
        return "ALTO"
    return "CRITICO"


@dataclass
class DomainResult:
    domain: str
    score: float
    risk_level: str = field(init=False)

    def __post_init__(self) -> None:
        self.risk_level = risk_level_for(self.score)


@dataclass
class AssessmentResult:
    global_score: float
    risk_level: str
    domains: dict[str, DomainResult]
    top_actions: list[dict]
