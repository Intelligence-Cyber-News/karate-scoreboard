from app.models import KataPerformance


def submit_judge_score(performance: KataPerformance, judge_index: int, score: float) -> None:
    performance.judgeScores[judge_index] = score

    if all(s is not None for s in performance.judgeScores):
        sorted_scores = sorted(performance.judgeScores)
        trimmed = sorted_scores[1:-1]
        performance.finalScore = round(sum(trimmed) / len(trimmed), 2)
        performance.status = "scored"


def reset_scores(performance: KataPerformance) -> None:
    performance.judgeScores = [None] * len(performance.judgeScores)
    performance.finalScore = None
    performance.status = "scoring"
