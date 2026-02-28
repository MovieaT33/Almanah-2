import json  # ujson
import random
import sys
import time

LANGUAGE: str = "uk"


def clear_console() -> None:
    print("\033[H\033[J", end="")


def parse_str(str_: str, replacements: dict[str, str]) -> str:
    for replacement_name, replacement_str in replacements.items():
        str_ = str_.replace(f"<{replacement_name}>", replacement_str)
    return str_


def parse_header(
    header: str, headers: dict[str, str], replacements: dict[str, str],
) -> str:
    return parse_str(headers[header], replacements)


def parse_question(
    question_data: tuple[str, str] | tuple[str, str, list[str]],
    headers: dict[str, str],
    replacements: dict[str, str],
) -> str:
    q_str: str = parse_str(question_data[0], replacements)
    q_headers: list[str] = question_data[2] if len(question_data) > 2 else []

    display_str: str = ""
    for q_header in q_headers:
        display_str += parse_header(q_header, headers, replacements)
    display_str += q_str
    return display_str


def parse_answer(
    question_data: tuple[str, str] | tuple[str, str, list[str]],
    replacements: dict[str, str],
) -> str:
    return parse_str(question_data[1], replacements)


def learn(
    quiz_data: dict,
    language: str,
    shuffle: bool = False,
    clear: bool = True,
) -> float:
    replacements: dict[str, str] = quiz_data.get("replacements", {})
    headers: dict[str, str] = quiz_data.get("headers", {})
    questions: dict[str, list[tuple[str, str]]] | None = \
        quiz_data.get("questions")

    if questions is None:
        print(f"{__file__}: \033[31merror\033[0m: No 'questions' key found in "
              "quiz data.")
        return 0

    if language not in questions:
        print(f"{__file__}: \033[31merror\033[0m: Language '{language}' not "
              "found in quiz data.")
        return 0

    language_questions: list[tuple[str, str]] = questions[language]
    if shuffle:
        random.shuffle(language_questions)

    clear_console()

    questions_n: int = len(language_questions)
    sum_time: float = 0
    question_i: int = 0
    for question in language_questions:
        start_time: float = time.time()
        print(f"{parse_question(question, headers, replacements)}   "
              f"[{question_i + 1} / {questions_n}]")
        input("> ")
        end_time: float = time.time()
        sum_time += end_time - start_time
        question_i += 1

        print(parse_answer(question, replacements))
        input()

        if clear:
            clear_console()

    average_time: float = sum_time / question_i if question_i > 0 else 0
    print(f"\033[32m{average_time:.2f}s\033[0m")
    return average_time


def main(quiz_filename: str, statistic_filename: str | None = None) -> None:
    try:
        with open(quiz_filename, "r", encoding="utf-8") as file:
            quiz_data: dict = json.load(file)
    except OSError as exc:
        print(f"{__file__}: \033[31merror\033[0m: {exc}")
        return

    av_time: float = learn(quiz_data, LANGUAGE, shuffle=True)
    if statistic_filename is not None:
        try:
            with open(statistic_filename, "a", encoding="utf-8") as file:
                file.write(f"{av_time}\n")
        except OSError as exc:
            print(f"{__file__}: \033[31merror\033[0m: {exc}")
            return


if __name__ == "__main__":
    filename: str | None = sys.argv[1] if len(sys.argv) > 1 else None
    if filename is None:
        print(f"usage: {__file__} <quiz_filename> [statistics]")
        sys.exit(1)

    statistics_filename: str | None = \
        sys.argv[2] if len(sys.argv) > 2 else None
    main(filename, statistics_filename)
