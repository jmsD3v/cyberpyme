from dataclasses import dataclass


@dataclass(frozen=True)
class Question:
    id: str
    domain: str
    question: str
    weight: float
    risk: str
    nist: list[str]
    cis: list[str]
    recommendation_id: str

    @staticmethod
    def from_dict(data: dict) -> "Question":
        return Question(
            id=data["id"],
            domain=data["domain"],
            question=data["question"],
            weight=data["weight"],
            risk=data["risk"],
            nist=data["nist"],
            cis=data["cis"],
            recommendation_id=data["recommendation_id"],
        )


ANSWER_VALUES = {
    "yes": 1.0,
    "partial": 0.5,
    "no": 0.0,
    "unknown": 0.0,
}


@dataclass(frozen=True)
class Answer:
    question_id: str
    value: str  # "yes" | "partial" | "no" | "unknown"

    @property
    def score_value(self) -> float:
        if self.value not in ANSWER_VALUES:
            raise ValueError(f"Respuesta inválida: {self.value!r}")
        return ANSWER_VALUES[self.value]

    @property
    def is_gap(self) -> bool:
        """True si la respuesta representa una brecha (no cumple o no se sabe)."""
        return self.value in ("no", "unknown", "partial")
